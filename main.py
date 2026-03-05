import asyncio
import json
import os
import random
import re
from datetime import datetime
from openai import AsyncOpenAI

# ================= 配置区 =================
API_KEY = "sk-f5cba6b00a2642fd80bf6fa8bc464b36"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-max" # 替换为云端实际的模型名称

DATA_DIR = "bright_queries" # 存放原始 JSONL 文件的目录
SAMPLE_RATIO = 0.05          # 抽样比例
CONCURRENCY_LIMIT = 5       # 并发数

# 要测试的初始 Prompt 文件列表
PROMPT_FILES = ["classify_prompt_v1.txt", "classify_prompt_v2.txt"]

# ================= 新增：计费与 Token 配置 =================
PRICE_PER_1K_INPUT = 0.04   # Qwen-max 输入价格：人民币/千tokens (可根据官方实际价格调整)
PRICE_PER_1K_OUTPUT = 0.12  # Qwen-max 输出价格：人民币/千tokens
COST_HISTORY_FILE = "token_cost_history.json" # 保存历史消耗的文件名
# =======================================================

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
write_lock = asyncio.Lock()  
cost_lock = asyncio.Lock()  # 新增：用于安全写入计费文件的锁

def read_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

async def update_cost_history(usage):
    """累加并保存 Token 消耗和人民币成本到本地文件，避免丢失"""
    if not usage:
        return
        
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    cost_rmb = (input_tokens / 1000) * PRICE_PER_1K_INPUT + (output_tokens / 1000) * PRICE_PER_1K_OUTPUT
    
    async with cost_lock:
        history = {"total_input_tokens": 0, "total_output_tokens": 0, "total_cost_rmb": 0.0}
        
        # 尝试读取历史数据
        if os.path.exists(COST_HISTORY_FILE):
            try:
                with open(COST_HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass
                
        # 累加当前消耗
        history["total_input_tokens"] += input_tokens
        history["total_output_tokens"] += output_tokens
        history["total_cost_rmb"] += cost_rmb
        
        # 写回文件
        with open(COST_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

def extract_tag_content(text, tag_name):
    """使用正则表达式提取指定标签中的内容"""
    pattern = f"<{tag_name}>(.*?)</{tag_name}>"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

async def call_llm(system_prompt, user_content):
    """并发控制的 LLM 调用，修改为返回内容及 usage 字典"""
    async with semaphore:
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content, response.usage
        except Exception as e:
            print(f"LLM Call Error: {e}")
            return None, None

async def process_sample(sample, prompt_template, prompt_dir, prompt_name):
    """处理单条数据，并在生成后写入对应的 Prompt 子文件夹中"""
    query = sample.get("query", "")
    
    # 获取 LLM 回复和 Token 消耗
    result_str, usage = await call_llm(system_prompt=prompt_template, user_content=query)
    
    # 记录 Token 和计费消耗
    if usage:
        await update_cost_history(usage)
    
    merged_data = dict(sample)
    # 在数据中显式记录使用了哪个 prompt
    merged_data["used_prompt"] = prompt_name 
    
    if result_str:
        # Try JSON parsing first (new format), fall back to tag extraction (old format)
        try:
            import json as json_lib
            json_data = json_lib.loads(result_str.strip())
            if "reasoning" in json_data and "category" in json_data:
                # 兼容旧的JSON格式，将其映射到新的四个字典键中
                merged_data["solution_space_exhaustion"] = ""
                merged_data["logical_supergraph_construction"] = ""
                merged_data["topology_reasoning"] = json_data.get("reasoning", "")
                merged_data["classification_result"] = "[" + json_data.get("category", "") + "]"
                merged_data["parse_status"] = "Success"
            else:
                raise ValueError("Missing required JSON keys")
        except:
            # Fall back to tag extraction (修改为最新的4个XML阶段标签)
            merged_data["solution_space_exhaustion"] = extract_tag_content(result_str, "solution_space_exhaustion")
            merged_data["logical_supergraph_construction"] = extract_tag_content(result_str, "logical_supergraph_construction")
            merged_data["topology_reasoning"] = extract_tag_content(result_str, "topology_reasoning")
            merged_data["classification_result"] = extract_tag_content(result_str, "classification_result")
            
            # 校验是否成功提取了最新的4个标签中的任意一个
            if not any([merged_data["solution_space_exhaustion"], merged_data["logical_supergraph_construction"], merged_data["topology_reasoning"], merged_data["classification_result"]]):
                merged_data["parse_status"] = "Tag Extraction Failed"
                merged_data["raw_llm_response"] = result_str
            else:
                merged_data["parse_status"] = "Success"
    else:
        merged_data["parse_status"] = "API Timeout/Error"
                
    # 动态确定输出文件路径
    source_file = sample.get("source_file", "unknown_dataset.jsonl")
    output_file = os.path.join(prompt_dir, source_file)
    
    async with write_lock:
        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(merged_data, ensure_ascii=False) + "\n")

def load_and_mix_datasets():
    if not os.path.exists(DATA_DIR):
        print(f"错误: 找不到数据文件夹 '{DATA_DIR}'")
        return []

    all_sampled_data = []
    file_list = [f for f in os.listdir(DATA_DIR) if f.endswith(".jsonl")]
    
    print(f"========== 开始加载并混合数据集 (共 {len(file_list)} 个文件) ==========")
    
    for filename in file_list:
        filepath = os.path.join(DATA_DIR, filename)
        file_data = []
        
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    obj = json.loads(line)
                    obj["source_file"] = filename
                    file_data.append(obj)
                except json.JSONDecodeError:
                    pass
        
        sample_size = int(len(file_data) * SAMPLE_RATIO)
        if sample_size == 0 and len(file_data) > 0:
            sample_size = 1 
            
        sampled = random.sample(file_data, sample_size)
        all_sampled_data.extend(sampled)
        print(f"- {filename}: 总量 {len(file_data)}, 抽样 {sample_size}")

    random.shuffle(all_sampled_data)
    print(f"\n[OK] 数据集混合完成，全局抽样数据总量: {len(all_sampled_data)}")
    return all_sampled_data

async def main():
    for pf in PROMPT_FILES:
        if not os.path.exists(pf):
            print(f"错误: 找不到 Prompt 文件 '{pf}'")
            return

    mixed_data = load_and_mix_datasets()
    if not mixed_data:
        return

    # 创建主输出文件夹
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_output_dir = f"results_{timestamp}"
    os.makedirs(main_output_dir, exist_ok=True)
    print(f"\n[DIR] 已创建主输出文件夹: {main_output_dir}")

    for prompt_file in PROMPT_FILES:
        prompt_name = os.path.splitext(prompt_file)[0]
        
        # 为当前 Prompt 创建专门的子文件夹
        prompt_dir = os.path.join(main_output_dir, prompt_name)
        os.makedirs(prompt_dir, exist_ok=True)
        
        print(f"\n>>> 开始使用 [{prompt_file}] 并发处理全局混合数据集 <<<")
        prompt_template = read_prompt(prompt_file)
        
        # 将子文件夹路径 prompt_dir 传给 process_sample
        tasks = [process_sample(sample, prompt_template, prompt_dir, prompt_name) for sample in mixed_data]
        
        await asyncio.gather(*tasks)
        
        print(f"[OK] [{prompt_file}] 跑批完成，结果已存入子文件夹: [{prompt_dir}/]")
        
    # 跑批结束后，可选打印一下当前总消耗
    if os.path.exists(COST_HISTORY_FILE):
        with open(COST_HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
            print(f"\n[COST] 历史总消耗: {history['total_cost_rmb']:.4f} 元")

if __name__ == "__main__":
    asyncio.run(main())