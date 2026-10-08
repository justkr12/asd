import streamlit as st
from openai import OpenAI

st.title("🤖 나만의 24시간 무료 챗봇")

# 사이드바에 API 키 입력창 만들기 (보안용)
with st.sidebar:
    api_key = st.text_input("OpenRouter 또는 OpenAI API Key를 입력하세요", type="password")
    model_name = st.text_input("사용할 모델 (예: meta-llama/llama-3-8b-instruct:free)", value="meta-llama/llama-3-8b-instruct:free")

if not api_key:
    st.info("시작하려면 사이드바에 API 키를 입력해주세요.")
    st.stop()

# AI 클라이언트 초기화 (기본 세팅은 OpenRouter 무료 모델 기준)
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1.",
    api_key=st.secrets["NVIDIA_API_KEY"]
)

# 대화 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 화면에 이전 대화 내용 그리기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 유저 입력창 처리
if prompt := st.chat_input("무엇이든 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 받아오기
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
