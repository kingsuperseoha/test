import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="하트시그널 챗봇", page_icon="💖", layout="centered")
st.title("💖 달콤쌉싸름한 연애상담소")
st.caption("gemini-2.5-flash-lite로 구동되는 스마트한 연애 코치입니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
if "GEMINI_API_KEY" not in st.secrets:
    st.error(".streamlit/secrets.toml 파일에 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

# 최신 구글 GenAI 클라이언트 생성
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 챗봇의 페르소나(System Instruction) 설정
SYSTEM_INSTRUCTION = """
너는 따뜻하고 공감 능력이 뛰어난 전문 연애 상담사야. 
사용자의 연애 고민(짝사랑, 이별, 썸, 갈등 등)을 진지하게 들어주고, 
친구처럼 다정하면서도 때로는 객관적이고 실용적인 조언을 해줘. 
답변은 너무 길지 않게 핵심을 짚어서 친근한 말투(해요체)로 작성해줘.
"""

# 4. 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 기존 채팅 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 받기
if user_input := st.chat_input("연애 고민을 편하게 털어놓으세요..."):
    
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 7. API 호출 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 💭")
        
        try:
            # 대화 기록 포맷 변환 (Gemini SDK 형식에 맞춤)
            history = []
            for msg in st.session_state.messages[:-1]:  # 현재 입력 직전까지의 기록
                role = "user" if msg["role"] == "user" else "model"
                history.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))
            
            # 채팅 세션 시작
            chat = client.chats.create(
                model="gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                ),
                history=history
            )
            
            # 답변 생성 (스트리밍은 생략하고 안정적인 일반 응답 사용)
            response = chat.send_message(user_input)
            ai_response = response.text
            
            # 결과 출력 및 저장
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as e:
            message_placeholder.empty()
            st.error(f"구글 API 오류가 발생했습니다: {e.message}")
        except Exception as e:
            message_placeholder.empty()
            st.error(f"예상치 못한 오류가 발생했습니다: {str(e)}")

# 8. 대화 초기화 버튼 (사이드바)
if st.sidebar.button("대화 기록 초기화 🔄"):
    st.session_state.messages = []
    st.rerun()
