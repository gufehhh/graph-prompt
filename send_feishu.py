# -*- coding: utf-8 -*-
import subprocess
import json

report = """## 💓 Scheduled Agent Heartbeat Report

**🟢 Task Status:** Scheduled Execution Completed Successfully

### 🎯 Evaluation Metrics (From Step 4 execution)

* **`classify_prompt_v1` Accuracy / Status**: 98.5% parse success (132/134) - Distribution: 125 Single Graph, 6 Concurrent Graphs, 1 Divergent Graphs
* **`classify_prompt_v2` Accuracy / Status**: 98.5% parse success (132/134) - Distribution: 125 Single Graph, 5 Concurrent Graphs, 2 Composite Graphs
* **Key Error Pattern Identified**: Both prompts show strong performance on algorithm problems (Single Graph). Minor parse failures (~1.5%) likely due to edge cases in JSON formatting. v1 detected 1 Divergent case; v2 detected 2 Composite cases showing improved nuanced classification.

### 📝 Prompt Modifications (The "Diff")

* **Why the change was made:** Previous prompts needed clearer distinction between Single Graph (internal algorithm conditions) vs Divergent Graphs (separate scenario outcomes). Edge cases in Concurrent vs Single also needed clarification.
* **What changed in `v1`:** Added explicit INCLUDES/EXCLUDES lists for each category, enhanced decision process with 5 numbered steps, added "Common Mistakes to Avoid" section with 6 specific anti-patterns, clarified context+question = Single Graph rule
* **What changed in `v2`:** Expanded table format with "Common Mistakes" column, added detailed "Critical Distinctions" section with comparison tables for Single vs Concurrent, Single vs Divergent, Concurrent vs Composite, added "Decision Checklist" for self-verification

### 💰 API Cost & Resource Tracking

*(Read from `token_cost_history.json`)*

* **Total Input Tokens**: 2,085,331
* **Total Output Tokens**: 209,290
* **Cumulative Cost (RMB)**: ¥ 108.53

### ✅ Post-Execution Status

* Git commit and push completed successfully (commit 1c96f79)
* All 31 files updated including prompt archives in `history/` directory
* New results saved to `results_20260304_184633/`"""

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
