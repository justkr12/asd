import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="24시간 무료 AI 챗봇", page_icon="🤖")
st.title("🤖 나만의 24시간 무료 NIM 챗봇")

# 사이드바 입력 제어
with st.sidebar:
    # 기본값으로 네모트론 550b 세팅
    model_name = st.text_input(
        "사용할 모델명", 
        value="nvidia/nemotron-3-ultra-550b-a55b"
    )

# Secrets에 등록된 엔비디아 API 키 확인
if "NVIDIA_API_KEY" not in st.secrets:
    st.error("Streamlit Advanced Settings(Secrets)에 NVIDIA_API_KEY를 설정해주세요.")
    st.stop()

# 엔비디아 NIM 호스팅 API 설정
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["NVIDIA_API_KEY"]
)

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 렌더링
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력창 가동
if prompt := st.chat_input("무엇이든 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 엔비디아 NIM 서버로 사용자가 선택한 모델(model_name)을 정확히 전달하여 요청합니다.
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=model_name, # ⭕ 이제 입력창에 적은 모델명이 제대로 전달됩니다!
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        answer = response.choices.message.content
        st.markdown(answer)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
