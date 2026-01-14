import streamlit as st
import requests
import json

# 1. 페이지 설정
st.set_page_config(page_title="네일 매니저 AI", page_icon="💅")

# 2. 디자인 및 상단 꾸미기
st.title("💅 네일샵 원장님 전용 AI 비서")
st.markdown("---")
st.caption("사장님들을 위해 제가 미리 결제해뒀어요! 무료로 맘껏 쓰세요. 🎁")

# 3. 비밀 금고(Secrets)에서 사장님 키 가져오기
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.sidebar.error("비밀 금고(Secrets) 설정을 확인해주세요!")
    st.stop()

# 4. 입력 화면 구성
col1, col2 = st.columns(2)
with col1:
    keywords = st.text_area("✨ 어떤 디자인인가요?", placeholder="예: 자석젤, 얼음네일, 실버파츠", height=100)
with col2:
    points = st.text_area("💎 강조하고 싶은 점은?", placeholder="예: 유지력 깡패, 실물 갑, 선착순 할인", height=100)

# 5. AI 생성 로직
if st.button("인스타 감성 문구 생성하기 🚀", type="primary", use_container_width=True):
    if not keywords:
        st.warning("디자인 키워드를 입력해주셔야 제가 글을 써드려요! 🥺")
    else:
        # AI 연기 지도 (말투 설정)
        prompt = f"""
        당신은 인스타그램에서 소통을 잘하는 10년 차 센스 있는 네일샵 원장님입니다. 
        아래 정보를 바탕으로 손님들이 '예약문의'를 하고 싶게끔 매력적인 피드 글을 써주세요.
        
        [정보]
        - 디자인: {keywords}
        - 특징: {points}
        
        [가이드라인]
        1. 첫 문장은 시선을 확 끄는 감성적인 문구로 시작 (이모지 활용)
        2. 말투는 '~했어요', '~에요' 같은 다정하고 부드러운 말투 사용
        3. 기계적인 느낌 절대 금지! 찐 후기나 일상 공유 같은 자연스러운 흐름
        4. 중간중간 가독성 좋게 줄바꿈(엔터) 필수
        5. 유입이 잘 되는 핵심 해시태그 7개를 마지막에 포함
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("사장님의 감성을 AI가 열공하는 중... ✍️"):
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    result = response.json()
                    final_text = result['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("작성 완료! 아래 박스 오른쪽 위의 버튼을 눌러 복사하세요! 👇")
                    # 복사하기 편하도록 st.code 사용
                    st.code(final_text, language=None)
                else:
                    st.error("구글 서버가 잠시 바쁘네요. 10초 뒤에 다시 시도해주세요!")
            except Exception as e:
                st.error("연결 중 문제가 생겼어요. 새로고침 후 다시 해주세요!")

# 하단 정보
st.markdown("---")
st.caption("© 2026 유니픽스 네일 매니저 AI | 피드백은 언제나 환영입니다! ✨")
