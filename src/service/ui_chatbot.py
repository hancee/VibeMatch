import streamlit as st
from swarm import Swarm

from src.service.agents import (
    triage_agent,
)
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

    try:
        # Call the triage agent (this might throw an exception)
        response = client.run(agent=triage_agent, messages=st.session_state.messages)
        message = response.messages
        agent = response.agent
        to_display = pretty_print_messages(messages=message)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(to_display)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": to_display})

    except Exception as e:
        # In case of an error, inform the user and ask for their email
        st.chat_message("assistant").markdown(
            "Oops, something went wrong on our end. We're currently processing your request, but it might take a little longer than expected. "
            "Could you please share your email address so our team can get back to you once everything is resolved?"
        )

        # Prompt the user to enter their email
        email = st.text_input("Enter your email address:")

        if email:
            # Store the email in session (or handle appropriately)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Thank you for providing your email: {email}. Our team will follow up with you shortly.",
                }
            )
            st.session_state.messages.append(
                {"role": "user", "content": f"User email: {email}"}
            )

            # Log or send email details as needed for follow-up (you could also send to an email system here)
            # For example, add the email to a database, or trigger a follow-up email process.
