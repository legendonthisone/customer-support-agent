"""Streamlit UI for the AnyCompany customer support agent"""

import streamlit as st
import customer_support_logic

st.set_page_config(page_title="AnyCompany Support", page_icon="🛍️")
st.title("🛍️ AnyCompany Customer Support")
st.caption("Ask me about your orders, refunds, or store policies.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_container = st.container()

for message in st.session_state.chat_history:
    with chat_container.chat_message(message.role):
        st.markdown(message.text)

input_text = st.chat_input("How can I help you today?")

if input_text:
    with chat_container.chat_message("user"):
        st.markdown(input_text)

    with st.spinner("Looking into that for you..."):
        response = customer_support_logic.chat_with_agent(
            message_history=st.session_state.chat_history,
            new_text=input_text,
        )
        with chat_container.chat_message("assistant"):
            st.markdown(response)
