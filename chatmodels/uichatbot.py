from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
from langchain_mistralai import ChatMistralAI

# -----------------------------
# LLM
# -----------------------------
llm = ChatMistralAI(
    model="mistral-small-2506"
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
)

st.title("🤖 AI Personality Chatbot")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Choose Personality")

personality = st.sidebar.radio(
    "Select AI Mode",
    (
        "😡 Angry",
        "😂 Funny",
        "😢 Sad",
    )
)

if personality == "😡 Angry":
    system_prompt = (
        "You are an angry AI agent. "
        "You respond aggressively and impatiently."
    )

elif personality == "😂 Funny":
    system_prompt = (
        "You are a very funny AI agent. "
        "You respond with humor and jokes."
    )

else:
    system_prompt = (
        "You are a very sad AI agent. "
        "You respond in a depressed and emotional tone."
    )

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=system_prompt)
    ]

# Reset chat when personality changes
if (
    st.session_state.messages[0].content
    != system_prompt
):
    st.session_state.messages = [
        SystemMessage(content=system_prompt)
    ]

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages[1:]:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

# -----------------------------
# Chat Input
# -----------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    # Generate response
    response = llm.invoke(st.session_state.messages)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response.content)

# -----------------------------
# Clear Chat Button
# -----------------------------
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        SystemMessage(content=system_prompt)
    ]
    st.rerun()