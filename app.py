import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="스케줄 관리 앱", page_icon="📅")

st.title("📅 스케줄 관리 웹앱")

# 세션 상태 초기화
if "schedules" not in st.session_state:
    st.session_state.schedules = []

# 일정 입력 폼
with st.form("schedule_form"):
    title = st.text_input("일정 제목")
    date = st.date_input("날짜")
    time = st.time_input("시간")
    memo = st.text_area("메모")

    submitted = st.form_submit_button("일정 추가")

    if submitted:
        if title:
            schedule = {
                "제목": title,
                "날짜": str(date),
                "시간": str(time),
                "메모": memo,
            }

            st.session_state.schedules.append(schedule)
            st.success("일정이 추가되었습니다!")
        else:
            st.warning("일정 제목을 입력해주세요.")

st.divider()

# 일정 목록 출력
st.subheader("📋 일정 목록")

if st.session_state.schedules:
    df = pd.DataFrame(st.session_state.schedules)

    # 날짜+시간 기준 정렬
    df["정렬용"] = pd.to_datetime(df["날짜"] + " " + df["시간"])
    df = df.sort_values("정렬용").drop(columns=["정렬용"])

    st.dataframe(df, use_container_width=True)

    st.divider()

    # 일정 삭제
    delete_index = st.number_input(
        "삭제할 일정 번호 입력 (0부터 시작)",
        min_value=0,
        max_value=len(st.session_state.schedules) - 1,
        step=1
    )

    if st.button("일정 삭제"):
        deleted = st.session_state.schedules.pop(delete_index)
        st.success(f"'{deleted['제목']}' 일정이 삭제되었습니다.")
        st.rerun()

else:
    st.info("등록된 일정이 없습니다.")
