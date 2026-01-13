import streamlit as st
import requests
import json

# 1. 페이지 설정
st.set_page_config(page_title="네일 매니저 AI", page_icon="💅")
st.title("💅 네일샵 원장님 전용 AI 비서")
st.caption("최신 엔진(Flash 1.5) - 다이렉트 연결 버전 🚀")

# 2. 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("새 구글 API 키를 입력하세요", type="password")

# 3. 입력 화면
col1, col2 = st.columns(2)
with col1:
    keywords = st.text_area("디자인 키워드", placeholder="예: 자석젤, 겨울왕국")
with col2:
    points = st.text_area("강조할 점", placeholder="예: 유지력 좋음, 이달의 아트")

# 4. AI 생성 로직 (라이브러리 없이 직접 통신)
if st.button("인스타 글 생성하기 ✨", type="primary"):
    if not api_key:
        st.error("API 키를 입력해주세요!")
    else:
        # ★ 여기가 핵심! 도구 없이 구글 본사 서버로 바로 쏩니다.
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{
                    "text": f"""
                    당신은 10년 차 뷰티 마케터입니다. 인스타그램 피드 글을 작성해주세요.
                    
                    [정보]
                    - 디자인: {keywords}
                    - 강조점: {points}
                    
                    [요청]
                    1. 헤드라인 (이모지 포함)
                    2. 감성적인 본문 (3~4줄)
                    3. 예약 유도
                    4. 해시태그 5개
                    """
                }]
            }]
        }
        
        with st.spinner("AI가 글을 작성 중입니다..."):
            try:
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    # 결과만 쏙 뽑아오기
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("작성 성공!")
                    st.write(text)
                else:
                    st.error(f"오류가 발생했습니다: {response.text}")
                    
            except Exception as e:
                st.error(f"연결 오류: {e}")
