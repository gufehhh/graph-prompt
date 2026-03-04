import os
import json
from datasets import load_dataset

def download_bright_queries(save_dir):
    """
    下载 BRIGHT 数据集所有子集的 query 并保存到指定目录
    """

    print("Loading BRIGHT dataset from HuggingFace...")
    dataset = load_dataset("xlangai/bright", "examples")  # "examples" 配置

    os.makedirs(save_dir, exist_ok=True)

    for subset in dataset.keys():  # 遍历每个子集
        save_path = os.path.join(save_dir, f"bright_{subset}_queries.jsonl")
        print(f"Saving queries for subset '{subset}' to: {save_path}")
        with open(save_path, "w", encoding="utf-8") as f:
            for example in dataset[subset]:
                record = {
                    "id": example["id"],
                    "query": example["query"]
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"Saved {len(dataset[subset])} queries for subset '{subset}'")

    print("Done for all subsets.")


if __name__ == "__main__":
    download_bright_queries(save_dir="./bright_queries")