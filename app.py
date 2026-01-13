import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="네일 매니저 AI", page_icon="💅")

st.title("💅 네일샵 원장님 전용 AI 비서")
st.caption("키워드만 넣으면 인스타 피드, 해시태그가 3초 만에 완성됩니다.")

# 2. 사이드바에 API 키 입력 (배포 시 비밀번호처럼 관리 가능)
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("구글 API 키를 입력하세요", type="password")
    st.info("구글 AI Studio에서 무료로 발급받을 수 있습니다.")

# 3. 입력 화면
col1, col2 = st.columns(2)
with col1:
    keywords = st.text_area("디자인 키워드", placeholder="예: 자석젤, 겨울왕국, 실버, 화려함")
with col2:
    points = st.text_area("강조할 점", placeholder="예: 유지력 좋음, 실물 깡패, 이달의 아트 할인")

# 4. AI 생성 로직
if st.button("인스타 글 생성하기 ✨", type="primary"):
    if not api_key:
        st.error("API 키를 먼저 입력해주세요!")
    elif not keywords:
        st.warning("키워드를 입력해주세요!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            당신은 10년 차 뷰티 마케터입니다. 아래 정보를 바탕으로 인스타그램 피드 글을 작성해주세요.
            
            [정보]
            - 디자인 특징: {keywords}
            - 강조할 점: {points}
            
            [요청사항]
            1. 헤드라인: 고객의 시선을 끄는 첫 문장 (이모지 포함)
            2. 본문: 감성적이고 친근한 말투 (3~4줄)
            3. CTA: 예약 문의 유도
            4. 해시태그: 인스타 최신 로직에 맞춰 유입이 가장 잘 될 핵심 키워드 5개만 선정 (#)
            """
            
            with st.spinner("AI가 문구를 작성 중입니다..."):
                response = model.generate_content(prompt)
                st.success("작성 완료! 복사해서 사용하세요.")
                st.text_area("결과물", response.text, height=400)
                
        except Exception as e:

            st.error(f"오류가 발생했습니다: {e}")
