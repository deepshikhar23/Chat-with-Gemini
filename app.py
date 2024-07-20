import os
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-pro")

# Streamlit app here
st.set_page_config(page_title="AI Chatbot (Gemini-Pro)", page_icon="robot", layout="centered")


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("Chat with Gemini-Pro hosted on 🤗 spaces")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


user_prompt = st.chat_input("Ask anything...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
else:
    st.warning("Please type your question.")  # Inform user about empty input