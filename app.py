import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="24시간 무료 AI 챗봇", page_icon="🤖")
st.title("🤖 나만의 24시간 무료 NIM 챗봇")

# 1. 사용할 모델명을 관리하는 입력창 구성 (기본값을 nemotron으로 세팅)
if "current_model" not in st.session_state:
    st.session_state.current_model = "nvidia/nemotron-3-ultra-550b-a55b"

with st.sidebar:
    # 사용자가 입력창 값을 바꾸면 즉시 st.session_state.current_model에 동기화됩니다.
    model_name = st.text_input(
        "사용할 모델명 입력", 
        value=st.session_state.current_model,
        key="current_model"
    )

# 2. Secrets에 등록된 엔비디아 API 키 확인
if "NVIDIA_API_KEY" not in st.secrets:
    st.error("Streamlit Advanced Settings(Secrets)에 NVIDIA_API_KEY를 설정해주세요.")
    st.stop()

# 3. 엔비디아 NIM 호스팅 API 클라이언트 정의
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["NVIDIA_API_KEY"]
)

# 4. 대화 기록 초기화 및 렌더링
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력창 가동 및 API 전송
if prompt := st.chat_input("무엇이든 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 사용자가 입력창에 적은 모델명(st.session_state.current_model)을 강제로 직접 꽂아 넣습니다.
        response = client.chat.completions.create(
            model=st.session_state.current_model,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        # 첫 번째 답변 선택 인덱스 [0] 정상 수정 완료
        answer = response.choices[0].message.content
        st.markdown(answer)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
