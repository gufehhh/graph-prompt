# -*- coding: utf-8 -*-
import subprocess
import json

report = """## 💓 Scheduled Agent Heartbeat Report

**🟢 Task Status:** Scheduled Execution Completed Successfully

### 🎯 Evaluation Metrics (From Step 4 execution)

* **`classify_prompt_v1` Accuracy / Status**: 100% (134/134) - Perfect parse success rate, improved from 99.25%
* **`classify_prompt_v2` Accuracy / Status**: 98.5% (132/134) - 2 parse failures due to LaTeX escaping issues (\\( \\) not properly escaped in JSON)
* **Key Error Pattern Identified**: v2 LLM outputs single backslashes in LaTeX math notation (\\(a\\)) which should be double-escaped (\\\\(a\\\\)) in JSON strings. v1 avoids this issue.

### 📝 Prompt Modifications (The "Diff")

* **Why the change was made:** Previous iteration had v1 at 99.25% (1 parse failure). Added stricter JSON format enforcement with explicit rules.
* **What changed in `v1`:** Added "ABSOLUTELY STRICT - PARSER DEPENDS ON THIS" header, 6 numbered CRITICAL FORMAT RULES, visual CORRECT/WRONG examples with annotations, single-line JSON requirement, explicit backslash escaping instruction
* **What changed in `v2`:** Added identical format enforcement rules while maintaining table format. However, v2 still produces LaTeX with improper escaping.

### 💰 API Cost & Resource Tracking

*(Read from `token_cost_history.json`)*

* **Total Input Tokens**: 1,583,373
* **Total Output Tokens**: 192,205
* **Cumulative Cost (RMB)**: ¥ 86.40

### ⚠️ Notes

* Git push failed due to network connectivity issues (github.com port 443 connection reset). Local commit successful (dbf1029). Manual push recommended.
* Next iteration should add explicit LaTeX escaping examples to v2 prompt."""

# Use OpenClaw message tool via subprocess
cmd = [
    "openclaw", "message", "send",
    "--target", "oc_66247ebb048745438e67ce49248868ad",
    "--channel", "feishu",
    "--message", report
]

result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")
