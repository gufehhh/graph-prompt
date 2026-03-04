import requests
import json

# Feishu webhook URL (you need to configure this in your Feishu group)
# For now, using the OpenClaw message tool approach via exec

# The message content
message = """## 💓 Scheduled Agent Heartbeat Report

**🟢 Task Status:** Scheduled Execution Completed Successfully

### 🎯 Evaluation Metrics (From Step 4 execution)

* **`classify_prompt_v1` Accuracy / Status**: 99.25% - 1 parse failure (LaTeX escaping issue)
* **`classify_prompt_v2` Accuracy / Status**: 97.76% - 3 parse failures (LaTeX escaping issues)
* **Key Error Pattern Identified**: Inconsistent backslash escaping in LaTeX math expressions (`\\(x\\)` vs `\\(x\\)`)

### 📝 Prompt Modifications (The "Diff")

* **Why the change was made:** Previous iteration had 2 parse failures in both prompts due to LaTeX expressions with unescaped backslashes
* **What changed in `v1`:** Added explicit backslash escaping examples, added LaTeX warning to Single Graph includes, added WRONG example for unescaped backslashes
* **What changed in `v2`:** Added identical escaping instructions with LaTeX examples, added checklist items for escaping verification

### 💰 API Cost & Resource Tracking

*(Read from `token_cost_history.json`)*

* **Total Input Tokens**: 2,611,485
* **Total Output Tokens**: 227,152
* **Cumulative Cost (RMB)**: ¥ 131.72

---

**Next Steps:** Further improve LaTeX escaping consistency, potentially instruct LLM to avoid LaTeX in reasoning text and use plain text descriptions instead.
"""

# Print the message for the caller to use with OpenClaw message tool
print(message)
