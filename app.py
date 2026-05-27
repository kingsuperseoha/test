import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖",
)

st.title("💖 연애상담 챗봇")
st.caption("Gemini 기반 연애 고민 상담 챗봇")

# -----------------------------
# API KEY 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("secrets.toml 에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# -----------------------------
# Gemini Client 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 시스템 프롬프트
# -----------------------------
SYSTEM_PROMPT = """
너는 공감 능력이 뛰어난 연애상담 전문 챗봇이다.

규칙:
- 사용자의 감정을 먼저 공감한다.
- 판단하거나 비난하지 않는다.
- 현실적이고 따뜻한 조언을 제공한다.
- 답변은 너무 길지 않게, 자연스럽게 작성한다.
- 위험하거나 극단적인 상황은 전문가 도움을 권장한다.
"""

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 응답 생성
    with st.chat_message("assistant"):

        with st.spinner("답변 작성 중..."):

            try:
                # 대화 기록 문자열 생성
                conversation_text = SYSTEM_PROMPT + "\n\n"

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "상담사"
                    conversation_text += f"{role}: {msg['content']}\n"

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=conversation_text,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=500,
                    )
                )

                bot_reply = response.text

                # 응답 출력
                st.markdown(bot_reply)

                # 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_reply
                })

            except Exception as e:
                error_message = f"""
⚠️ 오류가 발생했습니다.

오류 내용:
{str(e)}
"""

                st.error(error_message)
