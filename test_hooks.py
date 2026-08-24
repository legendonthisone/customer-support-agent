"""Test the ToolCallRecorderHookProvider by asking about an order"""

import json
import sys
sys.path.insert(0, ".")

from customer_support_agent import create_agent

agent = create_agent()

result = agent("Can you look up order ORD-1001 for me?")

print("=" * 50)
print("Agent response:")
print(str(result))
print("=" * 50)
print("Tool requests:")
print(json.dumps(result.state.get("tool_requests", []), indent=2))
