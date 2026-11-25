
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="MY AI Coding Companion",
    page_icon="🤖",
    layout="centered"
)

# App title
st.title("🤖 MY AI Coding Companion")
st.caption("Powered by Groq | Ask me about Python, APIs, and Generative AI!")

# Initialize conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear conversation button
with st.sidebar:
    st.title("Settings")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.info("Your conversation is stored during your current app session.")

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Groq API key is missing. Please configure it in Streamlit Secrets.")
    st.stop()

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything about programming..."):

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                api_messages = [
                    {
                        "role": "system",
                        "content": "You are a witty, helpful AI programming companion."
                    }
                ] + st.session_state.messages

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=api_messages,
                    max_tokens=500
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")

