import json
import glob
import os

def analyze_results(results_dir):
    stats = {
        'v1': {'total': 0, 'success': 0, 'fail': 0, 'types': {'[Single Graph]': 0, '[Concurrent Graphs]': 0, '[Divergent Graphs]': 0, '[Composite Graphs]': 0, '[Unclassifiable]': 0}, 'datasets': {}},
        'v2': {'total': 0, 'success': 0, 'fail': 0, 'types': {'[Single Graph]': 0, '[Concurrent Graphs]': 0, '[Divergent Graphs]': 0, '[Composite Graphs]': 0, '[Unclassifiable]': 0}, 'datasets': {}}
    }
    
    for version in ['v1', 'v2']:
        path_pattern = os.path.join(results_dir, f'classify_prompt_{version}', '*.jsonl')
        for file_path in glob.glob(path_pattern):
            dataset_name = os.path.basename(file_path)
            stats[version]['datasets'][dataset_name] = {'total': 0, 'success': 0, 'fail': 0, 'types': {}}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    stats[version]['total'] += 1
                    stats[version]['datasets'][dataset_name]['total'] += 1
                    
                    try:
                        data = json.loads(line)
                        graph_type = data.get('classification_result', '').strip()
                        # Some versions might output without brackets, try to map them if needed, or strictly check
                        if graph_type not in stats[version]['types']:
                            # try formatting
                            if f"[{graph_type}]" in stats[version]['types']:
                                graph_type = f"[{graph_type}]"
                            elif graph_type in ["Single Graph", "Concurrent Graphs", "Divergent Graphs", "Composite Graphs", "Unclassifiable"]:
                                graph_type = f"[{graph_type}]"
                            elif graph_type == "":
                                graph_type = "[Unclassifiable]" # Fallback for empty
                            else:
                                graph_type = "[Unclassifiable]"
                                
                        if data.get('error'):
                            stats[version]['fail'] += 1
                            stats[version]['datasets'][dataset_name]['fail'] += 1
                        else:
                            stats[version]['success'] += 1
                            stats[version]['datasets'][dataset_name]['success'] += 1
                            
                        stats[version]['types'][graph_type] = stats[version]['types'].get(graph_type, 0) + 1
                        stats[version]['datasets'][dataset_name]['types'][graph_type] = stats[version]['datasets'][dataset_name]['types'].get(graph_type, 0) + 1
                    except Exception as e:
                        stats[version]['fail'] += 1
                        stats[version]['datasets'][dataset_name]['fail'] += 1
                        
    return stats

if __name__ == '__main__':
    results_dir = 'results_20260305_170654'
    stats = analyze_results(results_dir)
    print(json.dumps(stats, indent=2))
