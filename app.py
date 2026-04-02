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

def load_system_prompt(filename):
    """
    지정된 파일명에서 시스템 프롬프트를 읽어옵니다.
    """
    try:
        # 파일을 읽기 모드로 열어 전체 내용을 반환합니다.
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # 파일이 없을 경우 에러 메시지를 출력하거나 기본값을 설정합니다.
        st.error(f"⚠️ '{filename}' 파일을 찾을 수 없습니다.")
        return "당신은 친절한 AI 어시스턴트입니다."
    except Exception as e:
        st.error(f"⚠️ 파일을 읽는 중 오류가 발생했습니다: {e}")
        return ""

if "chat_session" not in st.session_state:
    system_prompt = load_system_prompt("system_prompt.md")
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction= system_prompt
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

