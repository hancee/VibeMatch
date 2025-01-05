from swarm import Swarm
from src.service.agents import (
    triage_agent,
    expert_agent,
    researcher_agent,
    analyst_agent,
)

import streamlit as st
from src.utils import pretty_print_messages

st.set_page_config(
    page_title="VibeMatch",
    page_icon="✨",
    initial_sidebar_state="expanded",
)

st.title("VibeMatch")

client = Swarm()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can we help you curate your perfect fragrance vibe?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.run(agent=triage_agent, messages=st.session_state.messages)
    message = response.messages
    agent = response.agent
    to_display = pretty_print_messages(messages=message)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(to_display)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": to_display})
