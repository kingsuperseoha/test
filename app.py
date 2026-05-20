import streamlit as st
import random

st.set_page_config(page_title="슬롯 머신", page_icon="🎰")

st.title("🎰 슬롯 머신 게임")

# 심볼 목록
symbols = ["🍒", "🍋", "🍇", "⭐", "7️⃣"]

# 초기 자금
if "money" not in st.session_state:
    st.session_state.money = 1000

# 현재 돈 표시
st.subheader(f"💰 보유 코인: {st.session_state.money}")

# 베팅 금액
bet = st.number_input(
    "베팅 금액",
    min_value=10,
    max_value=st.session_state.money if st.session_state.money > 0 else 10,
    step=10
)

# 슬롯 돌리기
if st.button("🎲 슬롯 돌리기"):

    if st.session_state.money <= 0:
        st.error("코인이 부족합니다!")
    else:
        # 베팅 차감
        st.session_state.money -= bet

        # 랜덤 슬롯
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

        st.markdown(
            f"""
            # {slot1} | {slot2} | {slot3}
            """
        )

        # 결과 판정
        if slot1 == slot2 == slot3:
            win = bet * 5
            st.session_state.money += win
            st.success(f"🎉 JACKPOT! +{win} 코인")

        elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
            win = bet * 2
            st.session_state.money += win
            st.success(f"✨ 당첨! +{win} 코인")

        else:
            st.error("😢 꽝!")

# 리셋 버튼
if st.button("🔄 게임 리셋"):
    st.session_state.money = 1000
    st.rerun()

# 게임 종료 안내
if st.session_state.money <= 0:
    st.warning("게임 오버! 리셋해서 다시 시작하세요.")
