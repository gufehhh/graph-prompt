# Graph Prompt - 查询拓扑分类系统

基于图论和因果推理的查询意图分类系统，通过构建逻辑拓扑图来分析用户问题的深层结构。

## 📁 项目结构

```
graph-prompt/
├── main.py                              # 主流水线脚本（并发测试）
├── download_bright.py                   # 数据下载脚本
├── classify_prompt_v1.txt               # 分类器 Prompt v1
├── classify_prompt_v2.txt               # 分类器 Prompt v2
├── agent_prompt.txt                     # Agent 系统 Prompt
├── query_classification_system_prompt_*.txt  # 历史版本 Prompt
└── README.md
```

## 🔧 核心功能

### 查询拓扑分类器

将用户查询映射为逻辑图 `G = (V, E)`：
- **节点 (V)**：离散事实、初始状态、结果
- **边 (E)**：因果关系、数学定理、逻辑演化机制

#### 分类拓扑类型

| 类型 | 说明 |
|------|------|
| **Single Graph** | 单一逻辑图可完整回答 |
| **Concurrent Graphs** | 多个独立不连通的图 |
| **Divergent Graphs** | 同一起终点，并行推理路径 |
| **Composite Graphs** | 混合结构 |
| **Unclassifiable** | 过于模糊无法分类 |

## 🚀 使用方法

### 1. 配置

编辑 `main.py` 配置区：

```python
API_KEY = "your-api-key"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-max"

DATA_DIR = "bright_queries"    # 数据目录
SAMPLE_RATIO = 0.1             # 抽样比例
CONCURRENCY_LIMIT = 5          # 并发数

PROMPT_FILES = ["classify_prompt_v1.txt", "classify_prompt_v2.txt"]
```

### 2. 运行测试

```bash
cd B:\git\graph-prompt
python main.py
```

### 3. 查看结果

结果输出到 `results_YYYYMMDD_HHMMSS/` 目录，按 Prompt 版本分子文件夹：

```
results_20260304_112000/
├── classify_prompt_v1/
│   └── bright_aops_queries.jsonl
└── classify_prompt_v2/
    └── bright_aops_queries.jsonl
```

## 📊 输出格式

每条结果包含：
- `query`: 原始查询
- `llm_reasoning`: LLM 推理过程
- `llm_category`: 分类结果
- `used_prompt`: 使用的 Prompt 版本
- `source_file`: 数据来源

## 🔄 版本迭代

- **v1**: 基础拓扑分类器（图论方法）
- **v2**: 优化版本（改进边/节点定义）

## 📝 依赖

```bash
pip install openai asyncio
```

## 🔐 注意事项

- API Key 包含在 `main.py` 中，生产环境请使用环境变量
- 数据目录 `bright_queries/` 需预先准备 JSONL 格式查询数据
