import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

st.title(":orange[:material/pets:] 고양이 챗봇")

st.caption("복잡한 시스템 프롬프트를 별도의 파일로 분리해 관리합니다.")

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


def load_system_prompt(file_name):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_dir, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"{file_path}를 찾을 수 없습니다.")
        st.stop()


if "chat_session" not in st.session_state:
    system_prompt = load_system_prompt("system_prompt.md")
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )


for content in st.session_state.chat_session.get_history():
    with st.chat_message("assistant" if content.role == "model" else "user"):
        for part in content.parts:
            st.markdown(part.text)


if prompt := st.chat_input("챗봇에게 물어보기"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)


with st.sidebar:
    if st.button(":material/refresh: 프롬프트 초기화"):
        st.session_state.pop("chat_session", None)
        st.rerun()