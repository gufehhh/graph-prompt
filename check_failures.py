import os
import json

results_dir = 'B:/git/graph-prompt/results_20260304_184633'
v1_dir = os.path.join(results_dir, 'classify_prompt_v1')

failures = []
for fname in sorted(os.listdir(v1_dir)):
    if fname.endswith('.jsonl'):
        with open(os.path.join(v1_dir, fname), 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get('parse_status') != 'Success':
                        failures.append({
                            'file': fname,
                            'id': data.get('id'),
                            'parse_status': data.get('parse_status'),
                            'raw_response': data.get('raw_llm_response', '')[:200]
                        })
                except:
                    pass

print(f"Found {len(failures)} failures:\n")
for f in failures:
    print(f"File: {f['file']}, ID: {f['id']}, Status: {f['parse_status']}")
    print(f"Raw: {f['raw_response']}")
    print('---')
