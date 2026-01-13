import streamlit as st
from google import genai

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="네일샵 원장님 전용 AI 비서", layout="wide")

st.title("💅 네일샵 원장님 전용 AI 비서")
st.caption("최신 엔진(Flash) - 다이렉트 연결 버전")

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("새 구글 API 키를 입력하세요", type="password")
    st.caption("주의: Google AI Studio에서 발급한 API Key를 권장합니다.")
    show_models = st.checkbox("모델 목록 보기(진단)", value=False)

col1, col2 = st.columns(2)
with col1:
    design_keywords = st.text_area("디자인 키워드", placeholder="예: 자석젤, 글리터, 미니멀, 프렌치...")
with col2:
    emphasis_points = st.text_area("강조할 점", placeholder="예: 유지력 좋음, 손이 예뻐 보이게, 고급스러움...")

generate_btn = st.button("인스타 글 생성하기 ✨", type="primary")

# -----------------------------
# Helper: pick an available flash model safely
# -----------------------------
def pick_flash_model(client: genai.Client) -> str:
    """
    API 키로 실제 사용 가능한 모델 목록에서
    flash 계열을 우선순위로 골라 반환합니다.
    """
    names = [m.name for m in client.models.list()]

    # 우선순위(가능하면 여기서 바로 선택)
    priorities = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-002",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ]
    for p in priorities:
        if p in names:
            return p

    # 그래도 없으면 "flash" 포함 아무 모델
    for n in names:
        if "flash" in n:
            return n

    # 아무것도 없으면 키/권한/프로젝트 문제일 가능성 큼
    raise RuntimeError(
        "이 API 키로 사용 가능한 Flash 모델을 찾지 못했습니다.\n"
        "1) Google AI Studio 키인지 확인\n"
        "2) 모델 목록 보기(진단)를 켜서 실제 모델명이 무엇인지 확인\n"
        "3) 키가 올바르다면 API 사용 권한/정책 문제 가능"
    )


def build_prompt(design: str, emphasis: str) -> str:
    return f"""
당신은 네일샵 인스타그램 마케팅 카피라이터입니다.
아래 정보를 바탕으로, 원장님이 바로 올릴 수 있는 '인스타 글'을 한국어로 작성하세요.

[요구사항]
- 톤: 세련되고 신뢰감, 과장 없이 고급스럽게
- 구성: (1) 첫 줄 훅 1줄 (2) 핵심 포인트 3~5줄 (3) 예약/문의 CTA 1줄
- 이모지는 과하지 않게 2~5개만 사용
- 해시태그 8~15개 (네일/지역/스타일 키워드 중심)
- 너무 긴 문장 피하기 (가독성 최우선)

[디자인 키워드]
{design.strip()}

[강조할 점]
{emphasis.strip()}
""".strip()


# -----------------------------
# Main flow
# -----------------------------
if api_key:
    try:
        client = genai.Client(api_key=api_key)

        if show_models:
            st.subheader("진단: 이 API 키로 보이는 모델 목록")
            model_names = [m.name for m in client.models.list()]
            st.write(model_names)

    except Exception as e:
        st.error(f"API 초기화 중 오류가 발생했습니다: {e}")
        st.stop()


if generate_btn:
    if not api_key:
        st.error("사이드바에 구글 API 키를 먼저 입력하세요.")
        st.stop()

    if not design_keywords.strip() and not emphasis_points.strip():
        st.error("디자인 키워드/강조할 점 중 하나는 입력해 주세요.")
        st.stop()

    try:
        client = genai.Client(api_key=api_key)
        model_name = pick_flash_model(client)

        prompt = build_prompt(design_keywords, emphasis_points)

        with st.spinner(f"생성 중... (모델: {model_name})"):
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

        st.success("생성 완료")
        st.text_area("결과", value=resp.text or "", height=400)

    except Exception as e:
        st.error(
            "오류가 발생했습니다.\n\n"
            f"{e}\n\n"
            "해결 팁:\n"
            "- '모델 목록 보기(진단)'를 켜서 flash 모델이 실제로 뜨는지 확인\n"
            "- 안 뜨면 API 키가 AI Studio 키인지 확인\n"
            "- 뜨면 모델명이 바뀐 경우이므로, 자동 선택이 되도록 이미 처리되어야 합니다"
        )
