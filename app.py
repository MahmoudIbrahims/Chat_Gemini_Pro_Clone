import streamlit as st
import google.generativeai as genai
import time
import random
from secret_key import API_key

st.set_page_config(
    page_title="Chat with Sara",
    page_icon="🔥"
)

st.title("Chat with Sara")
st.caption(""" Prepare to experience the future of communication with the groundbreaking chatbot meticulously crafted by Mahmoud Ibrahim. This state-of-the-art technology empowers you to:
Engage in seamless and natural conversations
Access real-time information and assistance
Automate tasks and streamline workflows
Enhance customer engagement and satisfaction
Push the boundaries of AI-powered communication
Discover the transformative power of Mahmoud Ibrahim's chatbot, designed to revolutionize the way you connect, interact, and optimize your digital experiences.""")

if "history" not in st.session_state:
    st.session_state.history = []

try:
    genai.configure(api_key= API_key)
except AttributeError as e:
    st.warning("Please Put Your Gemini API Key First")

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = []
        #st.experimental_rerun()

for message in chat.history:
    role = "assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input(""):
    prompt = prompt.replace('\n', ' \n')
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            full_response = ""
            for chunk in chat.send_message(prompt, stream=True):
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            message_placeholder.markdown(full_response)
        except genai.types.generation_types.BlockedPromptException as e:
            st.exception(e)
        except Exception as e:
            st.exception(e)
        st.session_state.history = chat.history
        chat.send_message("My name is Sara and I was created by Mahmoud Ibrahim.")
