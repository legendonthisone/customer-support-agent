"""Supporting logic bridging the Streamlit UI and the customer support agent"""

from customer_support_agent import create_agent

class ChatMessage:
    """Stores a single chat message for the UI"""

    def __init__(self, role: str, text: str):
        self.role = role
        self.text = text

agent = create_agent()

def chat_with_agent(message_history: list, new_text: str) -> tuple:
    """Sends a user message to the agent and returns (response_text, result_state)"""
    message_history.append(ChatMessage("user", new_text))

    result = agent(new_text)

    message_history.append(ChatMessage("assistant", str(result)))
    return str(result), result.state
