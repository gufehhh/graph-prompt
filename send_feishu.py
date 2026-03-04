# -*- coding: utf-8 -*-
import subprocess
import json

report = """## 💓 Scheduled Agent Heartbeat Report

**🟢 Task Status:** Scheduled Execution Completed Successfully

### 🎯 Evaluation Metrics (From Step 4 execution)

* **`classify_prompt_v1` Accuracy / Status**: 99.2% (123/124) - 1 parse failure in bright_aops_queries.jsonl (LLM output valid JSON but parser couldn't extract category)
* **`classify_prompt_v2` Accuracy / Status**: 100% (124/124) - Perfect parse success rate
* **Key Error Pattern Identified**: v1 parser expects `[Category]` format but LLM outputs JSON `{"category": "Category"}`. This is a parser-prompt format mismatch, not an LLM error.

### 📝 Prompt Modifications (The "Diff")

* **Why the change was made:** Previous iteration showed v2 at 100% but v1 had minor parse failures. Added stronger JSON format enforcement and explicit edge case examples.
* **What changed in `v1`:** Added "COMMON MISTAKES TO AVOID" section, strengthened JSON format rules with WRONG/RIGHT examples, added more explicit Single vs Divergent examples
* **What changed in `v2`:** Added "WHAT IS ALWAYS SINGLE GRAPH" section, enhanced JSON format enforcement with CORRECT/WRONG examples, kept table format but added comprehensive edge cases

### 💰 API Cost & Resource Tracking

*(Read from `token_cost_history.json`)*

* **Total Input Tokens**: 1,235,185
* **Total Output Tokens**: 175,253
* **Cumulative Cost (RMB)**: ¥ 70.44"""

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
