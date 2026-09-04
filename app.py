import os
import html
import textwrap

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# HTML 렌더링 함수
# =========================================================

def render_html(content):
    """
    들여쓰기 때문에 Streamlit이 HTML을 코드블록으로
    인식하는 문제를 방지
    """
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )


# =========================================================
# 경로 설정
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


def get_image_path(filename):
    return os.path.join(ASSET_DIR, filename)


def show_local_image(filename, caption=None):
    path = get_image_path(filename)

    if os.path.isfile(path):
        st.image(
            path,
            caption=caption,
            use_container_width=True
        )
    else:
        render_html(f"""
        <div class="image-placeholder">
            <div class="placeholder-icon">🖼️</div>
            <div>이미지를 준비 중입니다</div>
            <small>assets/{html.escape(filename)}</small>
        </div>
        """)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family:
        "Pretendard",
        "Noto Sans KR",
        "Malgun Gothic",
        sans-serif;
}

.stApp {
    background: #f3f7f5;
}

/* ---------------------------------------------------------
   전체 영역
--------------------------------------------------------- */

.main .block-container {
    max-width: 1450px !important;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* ---------------------------------------------------------
   사이드바
--------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: #eaf2ee;
    border-right: 1px solid #dce8e2;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #17352b;
    margin-bottom: 8px;
}

.sidebar-subtitle {
    color: #6c7f76;
    font-size: 13px;
    margin-bottom: 28px;
}

.sidebar-label {
    font-size: 13px;
    font-weight: 700;
    color: #6c7f76;
    margin-top: 18px;
    margin-bottom: 7px;
}

/* ---------------------------------------------------------
   메인 타이틀
--------------------------------------------------------- */

.title-card {
    background: #ffffff;
    border-radius: 22px;
    padding: 34px 40px;
    margin-bottom: 28px;
    box-shadow: 0 8px 28px rgba(39, 72, 59, 0.07);
    border: 1px solid #e4ece8;
}

.main-title-small {
    color: #ff4f5f;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.main-title {
    color: #17352b;
    font-size: 36px;
    font-weight: 900;
    line-height: 1.25;
    margin-bottom: 10px;
}

.main-subtitle {
    color: #718078;
    font-size: 15px;
}

/* ---------------------------------------------------------
   섹션 제목
--------------------------------------------------------- */

.section-title {
    color: #17352b;
    font-size: 24px;
    font-weight: 900;
    margin-top: 20px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #7b8983;
    font-size: 13px;
    margin-bottom: 20px;
}

/* ---------------------------------------------------------
   Metric 카드
--------------------------------------------------------- */

.metric-card {
    background: #ffffff;
    border: 1px solid #e1ebe6;
    border-radius: 18px;
    padding: 23px 24px;
    min-height: 155px;
    box-shadow: 0 5px 18px rgba(39, 72, 59, 0.05);
}

.metric-title {
    color: #6f7e77;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 18px;
}

.metric-value {
    color: #17352b;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 8px;
}

.metric-sub {
    color: #8a9690;
    font-size: 12px;
}

/* ---------------------------------------------------------
   지역 카드
--------------------------------------------------------- */

.region-card {
    background: #ffffff;
    border: 1px solid #e1ebe6;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(39, 72, 59, 0.05);
}

.region-card-inner {
    padding: 22px;
}

.region-name {
    color: #17352b;
    font-size: 21px;
    font-weight: 900;
    margin-bottom: 5px;
}

.region-location {
    color: #8a9690;
    font-size: 12px;
    margin-bottom: 17px;
}

.region-score-label {
    color: #66756e;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 6px;
}

.score-number {
    color: #ff4f5f;
    font-size: 25px;
    font-weight: 900;
}

.score-bar {
    height: 8px;
    background: #edf1ef;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 7px;
    margin-bottom: 15px;
}

.score-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff6b75, #ff4f5f);
    border-radius: 10px;
}

.info-row {
    display: flex;
    gap: 7px;
    margin-top: 8px;
    color: #5e6d66;
    font-size: 13px;
}

.info-label {
    font-weight: 800;
    color: #34463e;
}

/* ---------------------------------------------------------
   정보 박스
--------------------------------------------------------- */

.food-box,
.tour-box,
.special-box {
    border-radius: 16px;
    padding: 18px;
    min-height: 130px;
}

.food-box {
    background: #fffaf3;
    border: 1px solid #f4e9d6;
}

.tour-box {
    background: #f3f8ff;
    border: 1px solid #dfebfa;
}

.special-box {
    background: #f8f4ff;
    border: 1px solid #e9dffc;
}

.box-title {
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 8px;
    color: #59655f;
}

.box-main {
    font-size: 18px;
    font-weight: 900;
    color: #26372f;
    margin-bottom: 5px;
}

.box-sub {
    font-size: 12px;
    color: #849089;
}

/* ---------------------------------------------------------
   상세 영역
--------------------------------------------------------- */

.detail-card {
    background: #ffffff;
    border: 1px solid #e1ebe6;
    border-radius: 20px;
    padding: 25px;
    margin-top: 18px;
    box-shadow: 0 5px 18px rgba(39, 72, 59, 0.05);
}

.detail-title {
    color: #17352b;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 5px;
}

.detail-location {
    color: #89958f;
    font-size: 13px;
    margin-bottom: 20px;
}

/* ---------------------------------------------------------
   리뷰
--------------------------------------------------------- */

.review-card {
    background: #f8faf9;
    border-radius: 14px;
    padding: 15px 17px;
    margin-bottom: 10px;
    border: 1px solid #e9efec;
    color: #53625b;
    font-size: 13px;
}

.review-icon {
    margin-right: 7px;
}

/* ---------------------------------------------------------
   TOP 5
--------------------------------------------------------- */

.rank-card {
    display: flex;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e2ebe7;
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

.rank-number {
    font-size: 24px;
    font-weight: 900;
    color: #ff5865;
    width: 50px;
}

.rank-name {
    font-weight: 800;
    color: #263a31;
    flex: 1;
}

.rank-score {
    font-size: 20px;
    font-weight: 900;
    color: #17352b;
}

/* ---------------------------------------------------------
   이미지
--------------------------------------------------------- */

.image-placeholder {
    height: 210px;
    background: #eef3f0;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #829089;
    font-size: 13px;
}

.placeholder-icon {
    font-size: 35px;
    margin-bottom: 7px;
}

/* ---------------------------------------------------------
   Streamlit 버튼
--------------------------------------------------------- */

div.stButton > button {
    border-radius: 12px;
    border: 1px solid #dce7e1;
    background: #ffffff;
    color: #30443a;
    font-weight: 700;
}

div.stButton > button:hover {
    border-color: #ff5965;
    color: #ff5965;
}

/* ---------------------------------------------------------
   탭
--------------------------------------------------------- */

button[data-baseweb="tab"] {
    font-weight: 700;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ff4f5f;
}

/* ---------------------------------------------------------
   지도
--------------------------------------------------------- */

.map-wrapper {
    background: #ffffff;
    border-radius: 20px;
    padding: 12px;
    border: 1px solid #e1ebe6;
    box-shadow: 0 5px 18px rgba(39, 72, 59, 0.05);
}

/* ---------------------------------------------------------
   Footer
--------------------------------------------------------- */

.footer {
    text-align: center;
    color: #9aa59f;
    font-size: 12px;
    padding: 35px 0 10px 0;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# 지역 데이터
# =========================================================

regions = [
    {
        "지역": "강원도 정선군",
        "시도": "강원도",
        "위도": 37.3806,
        "경도": 128.6608,
        "인구": 35000,
        "인구변화": -2.8,
        "음식점수": 90,
        "관광인지도": 46,
        "지역특색": 90,
        "대표음식": "곤드레밥",
        "음식점": "정선 곤드레마을",
        "관광지": "민둥산",
        "지역행사": "정선 5일장",
        "특산품": "곤드레",
        "음식이미지": "jeongseon_food.jpg",
        "관광이미지": "jeongseon_tour.jpg",
        "특산품이미지": "jeongseon_specialty.jpg",
        "리뷰": [
            "곤드레밥이 생각보다 훨씬 맛있었습니다.",
            "관광객이 너무 많지 않아서 여유롭게 여행하기 좋았습니다.",
            "정선 5일장과 같이 방문하면 볼거리가 많습니다."
        ]
    },
    {
        "지역": "충청북도 단양군",
        "시도": "충청북도",
        "위도": 36.9845,
        "경도": 128.3657,
        "인구": 28000,
        "인구변화": -1.7,
        "음식점수": 85,
        "관광인지도": 52,
        "지역특색": 88,
        "대표음식": "마늘떡갈비",
        "음식점": "단양 마늘골목",
        "관광지": "도담삼봉",
        "지역행사": "단양 마늘축제",
        "특산품": "단양마늘",
        "음식이미지": "danyang_food.jpg",
        "관광이미지": "danyang_tour.jpg",
        "특산품이미지": "danyang_specialty.jpg",
        "리뷰": [
            "마늘을 활용한 음식이 생각보다 다양해서 좋았습니다.",
            "도담삼봉 주변 풍경이 정말 좋았습니다.",
            "사람이 너무 붐비지 않아 조용하게 하루 여행하기 좋았습니다."
        ]
    },
    {
        "지역": "전라남도 구례군",
        "시도": "전라남도",
        "위도": 35.2025,
        "경도": 127.4628,
        "인구": 25000,
        "인구변화": -2.2,
        "음식점수": 88,
        "관광인지도": 41,
        "지역특색": 94,
        "대표음식": "산채비빔밥",
        "음식점": "구례 산채마을",
        "관광지": "지리산 노고단",
        "지역행사": "구례 산수유축제",
        "특산품": "산수유",
        "음식이미지": "gurye_food.jpg",
        "관광이미지": "gurye_tour.jpg",
        "특산품이미지": "gurye_specialty.jpg",
        "리뷰": [
            "산나물을 활용한 음식이 신선하고 맛있었습니다.",
            "지리산 풍경을 보면서 천천히 여행하기 좋았습니다.",
            "봄철 산수유가 정말 예뻐서 다시 방문하고 싶습니다."
        ]
    },
    {
        "지역": "경상북도 영덕군",
        "시도": "경상북도",
        "위도": 36.4150,
        "경도": 129.3650,
        "인구": 34000,
        "인구변화": -2.0,
        "음식점수": 91,
        "관광인지도": 48,
        "지역특색": 87,
        "대표음식": "대게",
        "음식점": "영덕 대게거리",
        "관광지": "해맞이공원",
        "지역행사": "영덕 대게축제",
        "특산품": "영덕대게",
        "음식이미지": "yeongdeok_food.jpg",
        "관광이미지": "yeongdeok_tour.jpg",
        "특산품이미지": "yeongdeok_specialty.jpg",
        "리뷰": [
            "대게가 정말 신선하고 맛있었습니다.",
            "해안도로를 따라 드라이브하기 좋았습니다.",
            "유명 관광지보다 한적한 느낌이 마음에 들었습니다."
        ]
    },
    {
        "지역": "전라북도 무주군",
        "시도": "전라북도",
        "위도": 36.0072,
        "경도": 127.6607,
        "인구": 24000,
        "인구변화": -2.5,
        "음식점수": 82,
        "관광인지도": 39,
        "지역특색": 92,
        "대표음식": "어죽",
        "음식점": "무주 어죽마을",
        "관광지": "덕유산",
        "지역행사": "무주 반딧불축제",
        "특산품": "머루",
        "음식이미지": "muju_food.jpg",
        "관광이미지": "muju_tour.jpg",
        "특산품이미지": "muju_specialty.jpg",
        "리뷰": [
            "어죽이라는 음식을 처음 먹어봤는데 정말 독특했습니다.",
            "덕유산의 자연환경이 아름답습니다.",
            "조용하게 힐링하고 싶은 사람에게 추천합니다."
        ]
    },
    {
        "지역": "충청남도 서천군",
        "시도": "충청남도",
        "위도": 36.0803,
        "경도": 126.6917,
        "인구": 47000,
        "인구변화": -1.3,
        "음식점수": 84,
        "관광인지도": 44,
        "지역특색": 86,
        "대표음식": "서천김",
        "음식점": "서천 바다밥상",
        "관광지": "국립생태원",
        "지역행사": "서천 한산모시축제",
        "특산품": "한산모시",
        "음식이미지": "seocheon_food.jpg",
        "관광이미지": "seocheon_tour.jpg",
        "특산품이미지": "seocheon_specialty.jpg",
        "리뷰": [
            "바다에서 나는 식재료가 신선해서 좋았습니다.",
            "국립생태원은 가족과 함께 방문하기 좋았습니다.",
            "지역 특산품을 구경하는 재미가 있었습니다."
        ]
    },
    {
        "지역": "경상남도 의령군",
        "시도": "경상남도",
        "위도": 35.3222,
        "경도": 128.2617,
        "인구": 26000,
        "인구변화": -2.7,
        "음식점수": 86,
        "관광인지도": 36,
        "지역특색": 91,
        "대표음식": "의령소바",
        "음식점": "의령 소바거리",
        "관광지": "자굴산",
        "지역행사": "의령 홍의장군축제",
        "특산품": "망개떡",
        "음식이미지": "uiryeong_food.jpg",
        "관광이미지": "uiryeong_tour.jpg",
        "특산품이미지": "uiryeong_specialty.jpg",
        "리뷰": [
            "의령소바가 담백하고 맛있었습니다.",
            "유명하지 않지만 지역만의 분위기가 좋았습니다.",
            "망개떡은 선물용으로도 괜찮았습니다."
        ]
    },
    {
        "지역": "강원도 삼척시",
        "시도": "강원도",
        "위도": 37.4499,
        "경도": 129.1658,
        "인구": 62000,
        "인구변화": -1.9,
        "음식점수": 89,
        "관광인지도": 50,
        "지역특색": 89,
        "대표음식": "곰치국",
        "음식점": "삼척 바다밥상",
        "관광지": "장호항",
        "지역행사": "삼척 장미축제",
        "특산품": "삼척 장뇌삼",
        "음식이미지": "samcheok_food.jpg",
        "관광이미지": "samcheok_tour.jpg",
        "특산품이미지": "samcheok_specialty.jpg",
        "리뷰": [
            "곰치국이 생각보다 담백하고 맛있었습니다.",
            "장호항 주변 풍경이 아름답습니다.",
            "바다와 맛집을 함께 즐기기 좋은 지역입니다."
        ]
    }
]


# =========================================================
# DataFrame
# =========================================================

df = pd.DataFrame(regions)


# =========================================================
# 숨은 지역 점수 계산
# =========================================================

def calculate_hidden_score(row):
    score = (
        (100 - row["관광인지도"]) * 0.35
        + row["음식점수"] * 0.30
        + row["지역특색"] * 0.35
    )
    return round(score, 1)


df["숨은지역점수"] = df.apply(
    calculate_hidden_score,
    axis=1
)


# =========================================================
# 사이드바
# =========================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-title">
        📍 숨은 로컬 발견
    </div>

    <div class="sidebar-subtitle">
        데이터로 찾는 대한민국의<br>
        알려지지 않은 지역
    </div>
    """)

    st.markdown(
        '<div class="sidebar-label">지역 선택</div>',
        unsafe_allow_html=True
    )

    region_options = ["전체"] + sorted(df["시도"].unique().tolist())

    selected_region = st.selectbox(
        "지역",
        region_options,
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="sidebar-label">최소 숨은지역 점수</div>',
        unsafe_allow_html=True
    )

    min_hidden_score = st.slider(
        "숨은지역 점수",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="sidebar-label">최소 음식 점수</div>',
        unsafe_allow_html=True
    )

    min_food_score = st.slider(
        "음식 점수",
        min_value=0,
        max_value=100,
        value=80,
        step=5,
        label_visibility="collapsed"
    )

    st.markdown("---")

    render_html("""
    <div style="
        color:#78867f;
        font-size:12px;
        line-height:1.7;
    ">
        💡 <b>숨은지역 점수</b>는<br>
        관광 인지도, 음식 경쟁력,<br>
        지역 특색을 종합하여 계산합니다.
    </div>
    """)


# =========================================================
# 필터
# =========================================================

filtered_df = df.copy()

if selected_region != "전체":
    filtered_df = filtered_df[
        filtered_df["시도"] == selected_region
    ]

filtered_df = filtered_df[
    (filtered_df["숨은지역점수"] >= min_hidden_score)
    & (filtered_df["음식점수"] >= min_food_score)
]


# =========================================================
# 메인 타이틀
# =========================================================

render_html("""
<div class="title-card">

    <div class="main-title-small">
        📍 LOCAL DISCOVERY
    </div>

    <div class="main-title">
        숨은 로컬 발견
    </div>

    <div class="main-subtitle">
        데이터로 발견하는 대한민국의 숨은 지역과 로컬 경험
    </div>

</div>
""")


# =========================================================
# 섹션 1 - 숨은 로컬
# =========================================================

render_html("""
<div class="section-title">
    📍 숨은 로컬
</div>

<div class="section-subtitle">
    지역을 데이터로 탐색해보세요
</div>
""")


# =========================================================
# Metric
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            📍 발견 지역
        </div>

        <div class="metric-value">
            {len(filtered_df)}
        </div>

        <div class="metric-sub">
            현재 조건에 맞는 지역
        </div>

    </div>
    """)


with col2:
    avg_hidden = (
        round(filtered_df["숨은지역점수"].mean(), 1)
        if len(filtered_df) > 0 else 0
    )

    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            ✨ 평균 숨은지역 점수
        </div>

        <div class="metric-value">
            {avg_hidden}
        </div>

        <div class="metric-sub">
            지역 발견 가능성
        </div>

    </div>
    """)


with col3:
    avg_food = (
        round(filtered_df["음식점수"].mean(), 1)
        if len(filtered_df) > 0 else 0
    )

    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            🍚 평균 음식 점수
        </div>

        <div class="metric-value">
            {avg_food}
        </div>

        <div class="metric-sub">
            로컬 음식 매력도
        </div>

    </div>
    """)


with col4:
    avg_awareness = (
        round(filtered_df["관광인지도"].mean(), 1)
        if len(filtered_df) > 0 else 0
    )

    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            👀 평균 관광 인지도
        </div>

        <div class="metric-value">
            {avg_awareness}
        </div>

        <div class="metric-sub">
            낮을수록 숨은 지역
        </div>

    </div>
    """)


# =========================================================
# 데이터 없음
# =========================================================

if filtered_df.empty:

    render_html("""
    <div style="
        background:#ffffff;
        border:1px solid #e1ebe6;
        border-radius:18px;
        padding:45px;
        margin-top:25px;
        text-align:center;
        color:#7d8983;
    ">
        <div style="font-size:40px;">🔍</div>
        <div style="
            font-size:18px;
            font-weight:800;
            color:#405149;
            margin-top:10px;
        ">
            조건에 맞는 지역이 없습니다.
        </div>
        <div style="margin-top:7px;">
            필터 조건을 조금 낮춰보세요.
        </div>
    </div>
    """)

    st.stop()


# =========================================================
# 지도
# =========================================================

render_html("""
<div class="section-title" style="margin-top:35px;">
    🗺️ 숨은 지역 지도
</div>

<div class="section-subtitle">
    지도에서 지역의 위치를 확인해보세요
</div>
""")

m = folium.Map(
    location=[36.3, 127.8],
    zoom_start=7,
    tiles="OpenStreetMap",
    control_scale=True
)

for _, row in filtered_df.iterrows():

    popup_html = f"""
    <div style="
        width:220px;
        font-family:'Malgun Gothic',sans-serif;
    ">

        <h4 style="
            margin:0 0 8px 0;
            color:#17352b;
        ">
            {html.escape(row["지역"])}
        </h4>

        <div>
            숨은지역 점수:
            <b style="color:#ff4f5f;">
                {row["숨은지역점수"]}
            </b>
        </div>

        <div style="margin-top:5px;">
            대표음식:
            <b>{html.escape(row["대표음식"])}</b>
        </div>

        <div style="margin-top:5px;">
            관광지:
            <b>{html.escape(row["관광지"])}</b>
        </div>

    </div>
    """

    folium.Marker(
        location=[row["위도"], row["경도"]],
        tooltip=f'{row["지역"]} · {row["숨은지역점수"]}점',
        popup=folium.Popup(
            popup_html,
            max_width=280
        ),
        icon=folium.Icon(
            color="red",
            icon="map-marker"
        )
    ).add_to(m)


m.fit_bounds(
    [
        [33.0, 124.0],
        [38.8, 132.0]
    ]
)

m.options["maxBounds"] = [
    [32.0, 123.0],
    [40.5, 134.0]
]

render_html("""
<div class="map-wrapper">
""")

st_folium(
    m,
    width=None,
    height=550,
    returned_objects=[]
)

render_html("""
</div>
""")


# =========================================================
# 지역 탐색
# =========================================================

render_html("""
<div class="section-title" style="margin-top:38px;">
    🌿 지역 탐색
</div>

<div class="section-subtitle">
    음식 · 관광 · 특산품을 한눈에 확인해보세요
</div>
""")


# =========================================================
# 지역 카드
# =========================================================

for start in range(0, len(filtered_df), 2):

    cols = st.columns(2)

    for col_index in range(2):

        row_index = start + col_index

        if row_index >= len(filtered_df):
            break

        row = filtered_df.iloc[row_index]

        with cols[col_index]:

            render_html(f"""
            <div class="region-card">

                <div class="region-card-inner">

                    <div class="region-name">
                        {html.escape(row["지역"])}
                    </div>

                    <div class="region-location">
                        📍 {html.escape(row["시도"])}
                    </div>

                    <div class="region-score-label">
                        숨은지역 점수
                    </div>

                    <div class="score-number">
                        {row["숨은지역점수"]}
                    </div>

                    <div class="score-bar">
                        <div
                            class="score-fill"
                            style="width:{min(row["숨은지역점수"], 100)}%;"
                        ></div>
                    </div>

                    <div class="info-row">
                        <span class="info-label">🍚 음식</span>
                        <span>{html.escape(row["대표음식"])}</span>
                    </div>

                    <div class="info-row">
                        <span class="info-label">🏞️ 관광</span>
                        <span>{html.escape(row["관광지"])}</span>
                    </div>

                    <div class="info-row">
                        <span class="info-label">🎁 특산품</span>
                        <span>{html.escape(row["특산품"])}</span>
                    </div>

                </div>

            </div>
            """)


# =========================================================
# 상세 지역
# =========================================================

render_html("""
<div class="section-title" style="margin-top:35px;">
    🔎 지역 상세 탐색
</div>

<div class="section-subtitle">
    관심 있는 지역의 로컬 경험을 자세히 확인해보세요
</div>
""")


selected_detail = st.selectbox(
    "상세 지역 선택",
    filtered_df["지역"].tolist(),
    label_visibility="collapsed"
)

selected_row = filtered_df[
    filtered_df["지역"] == selected_detail
].iloc[0]


# =========================================================
# 상세 카드
# =========================================================

render_html(f"""
<div class="detail-card">

    <div class="detail-title">
        {html.escape(selected_row["지역"])}
    </div>

    <div class="detail-location">
        📍 {html.escape(selected_row["시도"])}
    </div>

</div>
""")


# =========================================================
# 상세 탭
# =========================================================

tab_food, tab_tour, tab_special, tab_review = st.tabs(
    [
        "🍚 로컬 음식",
        "🏞️ 관광지",
        "🎁 특산품",
        "💬 방문자 리뷰"
    ]
)


# ---------------------------------------------------------
# 음식
# ---------------------------------------------------------

with tab_food:

    col1, col2 = st.columns([1.1, 1])

    with col1:
        show_local_image(
            selected_row["음식이미지"],
            caption=selected_row["대표음식"]
        )

    with col2:

        render_html(f"""
        <div class="food-box">

            <div class="box-title">
                🍚 대표 음식
            </div>

            <div class="box-main">
                {html.escape(selected_row["대표음식"])}
            </div>

            <div class="box-sub">
                추천 장소 · {html.escape(selected_row["음식점"])}
            </div>

            <div style="
                margin-top:20px;
                color:#8a7560;
                font-size:13px;
            ">
                음식 점수
            </div>

            <div style="
                font-size:30px;
                font-weight:900;
                color:#d88932;
                margin-top:3px;
            ">
                {selected_row["음식점수"]}점
            </div>

        </div>
        """)


# ---------------------------------------------------------
# 관광
# ---------------------------------------------------------

with tab_tour:

    col1, col2 = st.columns([1.1, 1])

    with col1:
        show_local_image(
            selected_row["관광이미지"],
            caption=selected_row["관광지"]
        )

    with col2:

        render_html(f"""
        <div class="tour-box">

            <div class="box-title">
                🏞️ 대표 관광지
            </div>

            <div class="box-main">
                {html.escape(selected_row["관광지"])}
            </div>

            <div class="box-sub">
                지역 행사 · {html.escape(selected_row["지역행사"])}
            </div>

            <div style="
                margin-top:20px;
                color:#6e7f90;
                font-size:13px;
            ">
                관광 인지도
            </div>

            <div style="
                font-size:30px;
                font-weight:900;
                color:#4284c4;
                margin-top:3px;
            ">
                {selected_row["관광인지도"]}점
            </div>

        </div>
        """)


# ---------------------------------------------------------
# 특산품
# ---------------------------------------------------------

with tab_special:

    col1, col2 = st.columns([1.1, 1])

    with col1:
        show_local_image(
            selected_row["특산품이미지"],
            caption=selected_row["특산품"]
        )

    with col2:

        render_html(f"""
        <div class="special-box">

            <div class="box-title">
                🎁 지역 특산품
            </div>

            <div class="box-main">
                {html.escape(selected_row["특산품"])}
            </div>

            <div class="box-sub">
                {html.escape(selected_row["지역"])}만의
                지역 특색을 만나보세요.
            </div>

            <div style="
                margin-top:20px;
                color:#7c6b91;
                font-size:13px;
            ">
                지역 특색 점수
            </div>

            <div style="
                font-size:30px;
                font-weight:900;
                color:#8757b8;
                margin-top:3px;
            ">
                {selected_row["지역특색"]}점
            </div>

        </div>
        """)


# ---------------------------------------------------------
# 리뷰
# ---------------------------------------------------------

with tab_review:

    render_html("""
    <div style="
        color:#66736d;
        font-size:14px;
        margin-bottom:15px;
        font-weight:700;
    ">
        💬 지역을 방문한 사람들이 남긴 이야기
    </div>
    """)

    for review in selected_row["리뷰"]:

        render_html(f"""
        <div class="review-card">
            <span class="review-icon">💬</span>
            {html.escape(review)}
        </div>
        """)


# =========================================================
# 지역 데이터 분석
# =========================================================

render_html("""
<div class="section-title" style="margin-top:42px;">
    📊 지역 데이터
</div>

<div class="section-subtitle">
    숨은 지역을 판단하는 주요 지표입니다
</div>
""")


analysis_col1, analysis_col2, analysis_col3 = st.columns(3)


with analysis_col1:

    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            👀 관광 인지도
        </div>

        <div class="metric-value">
            {selected_row["관광인지도"]}
        </div>

        <div class="metric-sub">
            낮을수록 덜 알려진 지역
        </div>

    </div>
    """)


with analysis_col2:

    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            🍚 음식 경쟁력
        </div>

        <div class="metric-value">
            {selected_row["음식점수"]}
        </div>

        <div class="metric-sub">
            지역 음식 매력도
        </div>

    </div>
    """)


with analysis_col3:

    render_html(f"""
    <div class="metric-card">

        <div class="metric-title">
            🌿 지역 특색
        </div>

        <div class="metric-value">
            {selected_row["지역특색"]}
        </div>

        <div class="metric-sub">
            지역 고유성
        </div>

    </div>
    """)


# =========================================================
# TOP 5
# =========================================================

render_html("""
<div class="section-title" style="margin-top:42px;">
    🏆 숨은 지역 TOP 5
</div>

<div class="section-subtitle">
    현재 데이터 기준 숨은 매력이 높은 지역
</div>
""")


top5 = df.sort_values(
    "숨은지역점수",
    ascending=False
).head(5)


for rank, (_, row) in enumerate(top5.iterrows(), start=1):

    render_html(f"""
    <div class="rank-card">

        <div class="rank-number">
            {rank}
        </div>

        <div class="rank-name">
            {html.escape(row["지역"])}
        </div>

        <div class="rank-score">
            {row["숨은지역점수"]}점
        </div>

    </div>
    """)


# =========================================================
# 데이터 테이블
# =========================================================

with st.expander("📋 전체 지역 데이터 보기"):

    display_df = filtered_df[
        [
            "지역",
            "인구",
            "인구변화",
            "음식점수",
            "관광인지도",
            "지역특색",
            "숨은지역점수"
        ]
    ].copy()

    display_df.columns = [
        "지역",
        "인구",
        "인구 변화(%)",
        "음식 점수",
        "관광 인지도",
        "지역 특색",
        "숨은지역 점수"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# Footer
# =========================================================

render_html("""
<div class="footer">
    📍 숨은 로컬 발견 · 데이터로 찾는 대한민국의 새로운 여행지
</div>
""")
