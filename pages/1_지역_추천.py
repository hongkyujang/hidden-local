
import streamlit as st

st.set_page_config(
    page_title="지역 추천 등록 | 로컬 쉼표",
    page_icon="🌿",
    layout="wide",
)

# ---------------------------------------------------------
# 디자인
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #121a15;
        color: #f1f5f2;
    }

    .recommend-header {
        background: linear-gradient(135deg, #254b3a, #3e7355);
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 25px;
        border: 1px solid #60866d;
    }

    .recommend-header h1 {
        color: white;
        font-size: 32px;
        font-weight: 800;
    }

    .recommend-header p {
        color: #e5f1e8;
        font-size: 17px;
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 상단 소개
# ---------------------------------------------------------

st.markdown(
    """
    <div class="recommend-header">
        <h1>🌿 우리 동네 알리기</h1>
        <p>
            아직 많은 사람에게 알려지지 않은 지역의 매력을 소개해 주세요.<br>
            지역 주민과 단체, 여행자 누구나 숨은 명소와 먹거리를 추천할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 메인 화면
# ---------------------------------------------------------

if st.button("← 로컬 쉼표 메인으로 돌아가기"):
    st.switch_page("app.py")

st.markdown("## 📝 지역 추천 등록")
st.caption("지역에 관한 정보를 입력하고 추천 내용을 등록해 주세요.")

with st.form("local_recommend_form", clear_on_submit=True):

    st.markdown("### 📍 지역 정보")

    region_name = st.text_input(
        "지역명 *",
        placeholder="예: 전라남도 담양군",
    )

    recommender = st.text_input(
        "추천자 또는 단체명",
        placeholder="예: 담양 주민 / 지역 관광협회",
    )

    st.markdown("---")
    st.markdown("### 📷 지역 대표 사진")

    region_photo = st.file_uploader(
        "지역을 대표하는 사진을 올려주세요.",
        type=["jpg", "jpeg", "png", "webp"],
    )

    st.markdown("---")
    st.markdown("### 🍴 대표 먹거리")

    food_name = st.text_input(
        "먹거리 이름",
        placeholder="예: 담양 떡갈비",
    )

    food_description = st.text_area(
        "먹거리 소개",
        placeholder="지역 음식의 특징과 추천 이유를 적어주세요.",
        height=120,
    )

    st.markdown("---")
    st.markdown("### 🏞️ 구경거리")

    attraction_name = st.text_input(
        "관광지 또는 명소 이름",
        placeholder="예: 숨겨진 산책로, 전망대, 지역 명소",
    )

    attraction_description = st.text_area(
        "구경거리 소개",
        placeholder="어떤 곳인지, 어떤 매력이 있는지 소개해 주세요.",
        height=120,
    )

    st.markdown("---")
    st.markdown("### ✍️ 우리 지역 소개")

    introduction = st.text_area(
        "지역 소개글 *",
        placeholder=(
            "이 지역만의 매력과 사람들에게 알려주고 싶은 이야기를 적어주세요."
        ),
        height=180,
    )

    submitted = st.form_submit_button(
        "🌱 지역 추천 등록하기",
        use_container_width=True,
    )

    if submitted:

        if not region_name.strip():
            st.error("지역명을 입력해 주세요.")

        elif not introduction.strip():
            st.error("지역 소개글을 입력해 주세요.")

        else:

            if "local_recommendations" not in st.session_state:
                st.session_state["local_recommendations"] = []

            st.session_state["local_recommendations"].append(
                {
                    "지역명": region_name.strip(),
                    "추천자": recommender.strip(),
                    "사진": (
                        region_photo.getvalue()
                        if region_photo is not None
                        else None
                    ),
                    "사진형식": (
                        region_photo.type
                        if region_photo is not None
                        else None
                    ),
                    "먹거리": food_name.strip(),
                    "먹거리소개": food_description.strip(),
                    "구경거리": attraction_name.strip(),
                    "구경거리소개": attraction_description.strip(),
                    "지역소개": introduction.strip(),
                }
            )

            st.success("지역 추천이 등록되었습니다!")
            st.balloons()

# ---------------------------------------------------------
# 등록된 추천 확인
# ---------------------------------------------------------

st.markdown("---")
st.markdown("## 📌 이번 세션에 등록된 추천")

recommendations = st.session_state.get(
    "local_recommendations",
    [],
)

if not recommendations:

    st.info("아직 등록된 지역 추천이 없습니다.")

else:

    for item in reversed(recommendations):

        with st.container(border=True):

            st.markdown(f"### 📍 {item['지역명']}")

            if item["사진"] is not None:
                st.image(
                    item["사진"],
                    width="stretch",
                )

            if item["추천자"]:
                st.caption(f"추천자: {item['추천자']}")

            if item["먹거리"]:
                st.markdown(f"#### 🍴 {item['먹거리']}")
                st.write(item["먹거리소개"])

            if item["구경거리"]:
                st.markdown(f"#### 🏞️ {item['구경거리']}")
                st.write(item["구경거리소개"])

            st.markdown("#### ✍️ 지역 소개")
            st.write(item["지역소개"])
