import asyncio
import json
import os
import random
from datetime import datetime
from openai import AsyncOpenAI

# ================= 配置区 =================
API_KEY = "sk-f5cba6b00a2642fd80bf6fa8bc464b36"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-max" # 替换为云端实际的模型名称

DATA_DIR = "bright_queries" # 存放原始 JSONL 文件的目录
SAMPLE_RATIO = 0.1          # 抽样比例
CONCURRENCY_LIMIT = 5       # 并发数

# 要测试的初始 Prompt 文件列表
PROMPT_FILES = ["classify_prompt_v1.txt", "classify_prompt_v2.txt"]
# ==========================================

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
write_lock = asyncio.Lock()  

def read_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

async def call_llm(system_prompt, user_content):
    """并发控制的 LLM 调用"""
    
    # 修复 API 400 报错：强制要求 prompt 中包含 "json" 关键字
    safe_system_prompt = system_prompt + "\n\nNote: You must output strictly in JSON format."
    
    async with semaphore:
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": safe_system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Call Error: {e}")
            return None

async def process_sample(sample, prompt_template, prompt_dir, prompt_name):
    """处理单条数据，并在生成后写入对应的 Prompt 子文件夹中"""
    query = sample.get("query", "")
    
    result_str = await call_llm(system_prompt=prompt_template, user_content=query)
    
    merged_data = dict(sample)
    # 在数据中显式记录使用了哪个 prompt
    merged_data["used_prompt"] = prompt_name 
    
    if result_str:
        try:
            # Strip markdown code blocks if present
            cleaned = result_str.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            llm_json = json.loads(cleaned)
            merged_data["llm_reasoning"] = llm_json.get("reasoning", "")
            merged_data["llm_category"] = llm_json.get("category", "")
        except json.JSONDecodeError:
            merged_data["llm_reasoning"] = "Parse Error"
            merged_data["llm_category"] = "Parse Error"
            merged_data["raw_llm_response"] = result_str
    else:
        merged_data["llm_reasoning"] = "API Timeout/Error"
        merged_data["llm_category"] = "API Timeout/Error"
        
    # 动态确定输出文件路径
    # 例如：保存到 results_xxx/classify_prompt_v1/bright_aops_queries.jsonl
    source_file = sample.get("source_file", "unknown_dataset.jsonl")
    output_file = os.path.join(prompt_dir, source_file)
    
    async with write_lock:
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
    print(f"\n✅ 数据集混合完成，全局抽样数据总量: {len(all_sampled_data)}")
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
    print(f"\n📁 已创建主输出文件夹: {main_output_dir}")

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
        
        print(f"✅ [{prompt_file}] 跑批完成，结果已存入子文件夹: [{prompt_dir}/]")

if __name__ == "__main__":
    asyncio.run(main())