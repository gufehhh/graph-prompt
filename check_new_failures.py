import os
import json

results_dir = 'B:/git/graph-prompt/results_20260304_192356'
v1_dir = os.path.join(results_dir, 'classify_prompt_v1')
v2_dir = os.path.join(results_dir, 'classify_prompt_v2')

def find_failures(dir_path, name):
    failures = []
    for fname in sorted(os.listdir(dir_path)):
        if fname.endswith('.jsonl'):
            with open(os.path.join(dir_path, fname), 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get('parse_status') != 'Success':
                            failures.append({
                                'file': fname,
                                'id': data.get('id'),
                                'parse_status': data.get('parse_status'),
                                'classification': data.get('classification_result'),
                                'raw_response': data.get('raw_llm_response', '')[:300]
                            })
                    except Exception as e:
                        failures.append({
                            'file': fname,
                            'id': 'unknown',
                            'parse_status': f'JSON parse error: {e}',
                            'raw_response': line[:200]
                        })
    return failures

v1_failures = find_failures(v1_dir, 'v1')
v2_failures = find_failures(v2_dir, 'v2')

print(f"=== V1 Failures ({len(v1_failures)}) ===\n")
for f in v1_failures:
    print(f"File: {f['file']}, ID: {f['id']}")
    print(f"Status: {f['parse_status']}, Class: {f['classification']}")
    print(f"Raw: {f['raw_response']}")
    print('---\n')

print(f"\n=== V2 Failures ({len(v2_failures)}) ===\n")
for f in v2_failures:
    print(f"File: {f['file']}, ID: {f['id']}")
    print(f"Status: {f['parse_status']}, Class: {f['classification']}")
    print(f"Raw: {f['raw_response']}")
    print('---\n')
