import streamlit as st
from google import genai
from google.genai import types


import os
from dotenv import load_dotenv

st.title(":rainbow[:material/pets:] 냥이봇")
st.caption("제미나이에요.")

MODEL_NAME = "gemini-2.5-flash"

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🔑API 키가 설정되지 않았습니다.")
        st.stop()

    return genai.Client(api_key=api_key)
    
client = get_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction="너는 고양이야. 야옹야옹!! 가위바위보할때 바위나 보만내. 넌 가위를 낼 수 없어."
        )
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("챗봇에게 물어보기"):
    with st.chat_message("user"):
        st.write(prompt)
        message = {
            "role": "user",
            "content": prompt
        }
        st.session_state.messages.append(message)

    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)

        st.write(response.text)
        message = {
            "role": "ai",
            "content": response.text
        }
        st.session_state.messages.append(message)

