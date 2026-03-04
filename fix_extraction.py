import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the process_sample function's extraction logic
old_extraction = '''    if result_str:
        # 修改为按照 4 个标签进行精准提取
        merged_data["query_intent_analysis"] = extract_tag_content(result_str, "query_intent_analysis")
        merged_data["logical_graph_construction"] = extract_tag_content(result_str, "logical_graph_construction")
        merged_data["topology_reasoning"] = extract_tag_content(result_str, "topology_reasoning")
        merged_data["classification_result"] = extract_tag_content(result_str, "classification_result")
        
        # 异常捕获：如果全都没提取出来，大概率是模型没按格式输出，保留原始输出方便排查
        if not any([merged_data["query_intent_analysis"], merged_data["logical_graph_construction"], merged_data["topology_reasoning"], merged_data["classification_result"]]):
            merged_data["parse_status"] = "Tag Extraction Failed"
            merged_data["raw_llm_response"] = result_str
        else:
            merged_data["parse_status"] = "Success"'''

new_extraction = '''    if result_str:
        # Try JSON parsing first (new format), fall back to tag extraction (old format)
        try:
            import json as json_lib
            json_data = json_lib.loads(result_str.strip())
            if "reasoning" in json_data and "category" in json_data:
                merged_data["query_intent_analysis"] = ""
                merged_data["logical_graph_construction"] = ""
                merged_data["topology_reasoning"] = json_data.get("reasoning", "")
                merged_data["classification_result"] = "[" + json_data.get("category", "") + "]"
                merged_data["parse_status"] = "Success"
            else:
                raise ValueError("Missing required JSON keys")
        except:
            # Fall back to tag extraction
            merged_data["query_intent_analysis"] = extract_tag_content(result_str, "query_intent_analysis")
            merged_data["logical_graph_construction"] = extract_tag_content(result_str, "logical_graph_construction")
            merged_data["topology_reasoning"] = extract_tag_content(result_str, "topology_reasoning")
            merged_data["classification_result"] = extract_tag_content(result_str, "classification_result")
            
            if not any([merged_data["query_intent_analysis"], merged_data["logical_graph_construction"], merged_data["topology_reasoning"], merged_data["classification_result"]]):
                merged_data["parse_status"] = "Tag Extraction Failed"
                merged_data["raw_llm_response"] = result_str
            else:
                merged_data["parse_status"] = "Success"'''

content = content.replace(old_extraction, new_extraction)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('main.py updated to support JSON output format')
