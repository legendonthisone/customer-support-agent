"""Customer support agent with order lookup, refund, and FAQ tools"""

from typing import Annotated, Literal
from strands import Agent, tool
from tool_call_recorder import ToolCallRecorderHookProvider

# --- Mock database ---

# Replace with real database calls in production
ORDERS = {
    "ORD-1001": {"status": "delivered", "product": "Wireless Headphones", "amount": 89.99, "date": "2026-08-18", "refunded": False},
    "ORD-1002": {"status": "shipped",   "product": "Mechanical Keyboard",  "amount": 129.99, "date": "2026-08-22", "refunded": False},
    "ORD-1003": {"status": "processing","product": "USB-C Hub",             "amount": 39.99, "date": "2026-08-24", "refunded": False},
    "ORD-1004": {"status": "delivered", "product": "Webcam HD 1080p",       "amount": 74.99, "date": "2026-08-10", "refunded": True},
}

FAQ = {
    "return_policy":  "You can return any item within 30 days of delivery for a full refund, provided it is in its original condition.",
    "shipping":       "Standard shipping takes 3-5 business days. Express shipping (1-2 days) is available at checkout.",
    "warranty":       "All products come with a 1-year manufacturer warranty covering defects in materials and workmanship.",
    "payment":        "We accept Visa, Mastercard, Amex, PayPal, and Apple Pay.",
    "track_order":    "You can track your order using the tracking number emailed to you after shipment.",
}

# --- Tools ---

@tool(description="Look up the details and status of a customer order by order ID")
def lookup_order(
    order_id: Annotated[str, "The order ID to look up, e.g. ORD-1001"],
) -> dict:
    order = ORDERS.get(order_id.upper())
    if not order:
        return {"error": f"Order {order_id} not found."}
    return {"order_id": order_id.upper(), **order}


@tool(description="Process a refund for a customer order")
def process_refund(
    order_id: Annotated[str, "The order ID to refund, e.g. ORD-1001"],
    reason: Annotated[
        Literal["damaged", "wrong_item", "not_delivered", "changed_mind"],
        "The reason for the refund",
    ],
) -> dict:
    order_id = order_id.upper()
    order = ORDERS.get(order_id)

    if not order:
        return {"success": False, "message": f"Order {order_id} not found."}
    if order["refunded"]:
        return {"success": False, "message": f"Order {order_id} has already been refunded."}
    if order["status"] not in ("delivered", "shipped"):
        return {"success": False, "message": f"Order {order_id} cannot be refunded — status is '{order['status']}'."}

    order["refunded"] = True
    return {
        "success": True,
        "message": f"Refund of ${order['amount']:.2f} for order {order_id} ({order['product']}) has been processed. Reason: {reason}.",
    }


@tool(description="Answer a frequently asked question about store policies")
def get_faq(
    topic: Annotated[
        Literal["return_policy", "shipping", "warranty", "payment", "track_order"],
        "The FAQ topic to look up",
    ],
) -> str:
    return FAQ.get(topic, "I don't have information on that topic.")


# --- Agent factory ---

SYSTEM_PROMPT = """You are a helpful and professional customer support agent for AnyCompany Store.

You can help customers with:
- Checking order status and details
- Processing refunds
- Answering questions about store policies

Guidelines:
- Always look up order details before discussing them — never guess order status.
- Confirm refund details with the customer before processing.
- Be concise, warm, and professional.
- If you cannot help with something, politely say so and suggest they contact support@anycompany.com.
"""

def create_agent():
    """Creates and returns the customer support agent"""
    return Agent(
        tools=[lookup_order, process_refund, get_faq],
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        system_prompt=SYSTEM_PROMPT,
        hooks=[ToolCallRecorderHookProvider(record_requests=True, record_results=True)],
    )
