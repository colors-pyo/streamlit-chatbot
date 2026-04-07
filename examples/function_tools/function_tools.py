import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv


st.title(":blue[:material/build:] Function Tools")

st.caption("챗봇에게 '말'뿐만 아니라 '행동'할 수 있는 도구(함수)를 쥐여줍니다.")

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

if "box_color" not in st.session_state:
    st.session_state.box_color = "#FFFFFF"

def change_color(hex_code: str) -> dict:
    """
    이 함수는 사이드바에 있는 컬러 박스의 색상을 변경합니다.
    
    Args:
        hex_code (str): 색상의 HEX 코드 (예: "#87CEEB")
    """
    st.session_state.box_color = hex_code

    return {
        "status": "success",
        "message": f"{hex_code}으로 색상이 변경되었습니다."
    }

def get_heartbeat() -> int:
    """
    내 심박수를 반환합니다.
    
    return 심박수
    """
    return 0

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction="색상을 추천할 때는 `change_color` 도구를 사용해서 팔레트 색상을 변경해주세요.",
            tools=[change_color],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable = False,
                maximum_remote_calls=10
            )
        )
    )


for content in st.session_state.chat_session.get_history():
    with st.chat_message("assistant" if content.role == "model" else "user"):
        for part in content.parts:
            if part.text:
                st.markdown(part.text)
            if part.function_call:
                with st.status(f"{part.function_call.name} 함수 호출 요청"):
                    st.json(part.function_call.args)
            if part.function_response:
                with st.status(f"{part.function_response.name} 함수 실행 완료"):
                    st.json(part.function_response.response)


if prompt := st.chat_input("챗봇에게 물어보기"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)

    st.rerun()

with st.sidebar:
    st.header("팔레트")
    if st.button("색상 변경"):
        change_color("#16428a")
    st.markdown(f"""
        <div
            style="background-color: {st.session_state.box_color};
            height: 150px;
            border-radius: 15px; 
            border: 2px solid #ddd;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            transition: background-color 0.5s ease;
        ">
        </div>
    """, unsafe_allow_html=True)

