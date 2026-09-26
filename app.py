import html
import urllib.parse

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import Fullscreen
from streamlit_folium import st_folium


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="로컬 쉼표",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 세션 기본값
# =========================================================

defaults = {
    "age_group": "전체",
    "group_size": "전체",
    "travel_duration": "전체",
    "travel_theme": "전체",
    "food_type": "전체",
    "keyword": "",
    "selected_region": "강원특별자치도 정선군",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background: #101916;
    color: #f1f5f3;
}

[data-testid="stSidebar"] {
    background: #17251f;
}

[data-testid="stSidebar"] * {
    color: #edf5f0;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem !important;
    padding-bottom: 2rem;
}


/* ---------------------------------------------------------
   사이드바
--------------------------------------------------------- */

.filter-heading {
    font-size: 20px;
    font-weight: 900;
    color: #dff6e7;
    margin-bottom: 16px;
}


/* ---------------------------------------------------------
   기본 카드
--------------------------------------------------------- */

.section-card {
    background: #16221d;
    border: 1px solid #30483c;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 18px;
}


/* ---------------------------------------------------------
   사진 카드
--------------------------------------------------------- */

.photo-card {
    background: #18251f;
    border: 1px solid #30483c;
    border-radius: 16px;
    padding: 10px;
}


/* ---------------------------------------------------------
   일정
--------------------------------------------------------- */

.schedule-time {
    color: #9fe0b6;
    font-weight: 900;
    font-size: 13px;
}

.schedule-text {
    color: #e4eee8;
    font-size: 13px;
    line-height: 1.55;
    word-break: keep-all;
}


/* ---------------------------------------------------------
   Expander
--------------------------------------------------------- */

div[data-testid="stExpander"] {
    border: 1px solid #30483c !important;
    border-radius: 13px !important;
    background: #16221d !important;
}

div[data-testid="stExpander"] summary {
    font-weight: 800;
}


/* ---------------------------------------------------------
   탭
--------------------------------------------------------- */

button[data-baseweb="tab"] {
    font-weight: 800;
}


/* ---------------------------------------------------------
   추천 배너 이미지
--------------------------------------------------------- */

.recommend-image img {
    border-radius: 18px;
}


/* ---------------------------------------------------------
   Streamlit metric
--------------------------------------------------------- */

div[data-testid="stMetric"] {
    background: #18251f;
    border: 1px solid #2e463a;
    border-radius: 16px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #91a99c !important;
}

div[data-testid="stMetricValue"] {
    color: #f1f7f3 !important;
}


/* ---------------------------------------------------------
   버튼
--------------------------------------------------------- */

.stButton > button,
.stLinkButton > a {
    border-radius: 10px !important;
    font-weight: 800 !important;
}


/* ---------------------------------------------------------
   모바일/좁은 화면
--------------------------------------------------------- */

@media (max-width: 900px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 데이터
# =========================================================

@st.cache_data
def load_data():

    data = [

        {
            "지역": "강원특별자치도 정선군",
            "위도": 37.3806,
            "경도": 128.6608,
            "인구": 34419,
            "인구변화율": -2.1,
            "음식점수": 91,
            "관광인지도": 43,
            "지역특색": 94,
            "대표음식": "곤드레밥",
            "음식점": "정선 곤드레밥 로컬식당",
            "관광지": "정선 아리랑시장 · 가리왕산",
            "지역행사": "정선 아리랑제",
            "특산품": "곤드레",
            "관광유형": "자연·문화",
            "랜드마크유형": "산·시장",
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["맛집·미식", "사진 명소", "역사·문화"],
            "나이대별_추천": ["20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["1인", "2인", "3인", "4인 이상"],
            "소개": "산과 전통시장을 함께 즐길 수 있는 강원도의 대표적인 로컬 여행지입니다.",
        },

        {
            "지역": "전라남도 구례군",
            "위도": 35.2025,
            "경도": 127.4628,
            "인구": 24500,
            "인구변화율": -1.8,
            "음식점수": 92,
            "관광인지도": 39,
            "지역특색": 96,
            "대표음식": "산채정식",
            "음식점": "구례 산채 로컬밥상",
            "관광지": "지리산 · 화엄사",
            "지역행사": "구례 산수유꽃축제",
            "특산품": "산수유",
            "관광유형": "자연·힐링",
            "랜드마크유형": "산·사찰",
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["맛집·미식", "사진 명소", "가족 여행"],
            "나이대별_추천": ["20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["1인", "2인", "3인", "4인 이상"],
            "소개": "지리산과 산채음식을 중심으로 자연 속에서 여유롭게 여행하기 좋은 지역입니다.",
        },

        {
            "지역": "경상남도 의령군",
            "위도": 35.3222,
            "경도": 128.2617,
            "인구": 26300,
            "인구변화율": -1.4,
            "음식점수": 89,
            "관광인지도": 36,
            "지역특색": 92,
            "대표음식": "의령 소바",
            "음식점": "의령 로컬 소바집",
            "관광지": "의령 구름다리 · 충익사",
            "지역행사": "의병제전",
            "특산품": "의령망개떡",
            "관광유형": "역사·문화",
            "랜드마크유형": "역사·전통",
            "추천기간": ["당일치기", "1박 2일"],
            "여행테마": ["맛집·미식", "역사·문화"],
            "나이대별_추천": ["20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["1인", "2인", "3인", "4인 이상"],
            "소개": "의병 역사와 로컬 먹거리를 함께 경험할 수 있는 경남의 숨은 지역입니다.",
        },

        {
            "지역": "전북특별자치도 무주군",
            "위도": 36.0071,
            "경도": 127.6608,
            "인구": 23800,
            "인구변화율": -1.6,
            "음식점수": 88,
            "관광인지도": 45,
            "지역특색": 91,
            "대표음식": "어죽",
            "음식점": "무주 로컬 어죽집",
            "관광지": "덕유산 · 반디랜드",
            "지역행사": "무주 반딧불축제",
            "특산품": "머루",
            "관광유형": "자연·체험",
            "랜드마크유형": "산·체험",
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["액티비티", "가족 여행", "사진 명소"],
            "나이대별_추천": ["10대", "20대", "30~40대"],
            "인원수별_추천": ["2인", "3인", "4인 이상"],
            "소개": "덕유산 자연과 체험형 관광을 함께 즐길 수 있는 지역입니다.",
        },

        {
            "지역": "충청북도 단양군",
            "위도": 36.9845,
            "경도": 128.3657,
            "인구": 27500,
            "인구변화율": -1.1,
            "음식점수": 87,
            "관광인지도": 50,
            "지역특색": 94,
            "대표음식": "마늘정식",
            "음식점": "단양 마늘 로컬식당",
            "관광지": "도담삼봉 · 만천하스카이워크",
            "지역행사": "단양 마늘축제",
            "특산품": "단양마늘",
            "관광유형": "자연·액티비티",
            "랜드마크유형": "강·전망대",
            "추천기간": ["당일치기", "1박 2일"],
            "여행테마": ["액티비티", "사진 명소", "맛집·미식"],
            "나이대별_추천": ["10대", "20대", "30~40대"],
            "인원수별_추천": ["2인", "3인", "4인 이상"],
            "소개": "강변 풍경과 액티비티, 마늘 먹거리를 함께 즐길 수 있습니다.",
        },

        {
            "지역": "경상북도 영양군",
            "위도": 36.6667,
            "경도": 129.1125,
            "인구": 16000,
            "인구변화율": -2.8,
            "음식점수": 90,
            "관광인지도": 29,
            "지역특색": 95,
            "대표음식": "산채비빔밥",
            "음식점": "영양 산나물 로컬식당",
            "관광지": "검마산 · 국제밤하늘보호공원",
            "지역행사": "영양 산나물축제",
            "특산품": "고추·산나물",
            "관광유형": "자연·힐링",
            "랜드마크유형": "산·별빛",
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["사진 명소", "맛집·미식", "자연"],
            "나이대별_추천": ["20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["1인", "2인", "3인", "4인 이상"],
            "소개": "관광객이 비교적 적고 밤하늘과 산나물 등 지역 고유의 매력이 강한 곳입니다.",
        },

        {
            "지역": "경상북도 청송군",
            "위도": 36.4363,
            "경도": 129.0571,
            "인구": 24500,
            "인구변화율": -1.9,
            "음식점수": 89,
            "관광인지도": 34,
            "지역특색": 94,
            "대표음식": "닭백숙",
            "음식점": "청송 닭백숙 로컬식당",
            "관광지": "주왕산 · 용연폭포",
            "지역행사": "청송 사과축제",
            "특산품": "청송사과",
            "관광유형": "자연·힐링",
            "랜드마크유형": "산·폭포",
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["자연·힐링", "사진 명소", "가족 여행"],
            "나이대별_추천": ["30~40대", "50대 이상"],
            "인원수별_추천": ["2인", "3인", "4인 이상"],
            "소개": "주왕산의 자연경관과 청송사과를 중심으로 여유로운 여행을 즐길 수 있습니다.",
        },

        {
            "지역": "충청남도 태안군",
            "위도": 36.7456,
            "경도": 126.2979,
            "인구": 61000,
            "인구변화율": -0.7,
            "음식점수": 88,
            "관광인지도": 48,
            "지역특색": 90,
            "대표음식": "꽃게",
            "음식점": "태안 꽃게 로컬맛집",
            "관광지": "꽃지해수욕장 · 안면도",
            "지역행사": "태안 빛축제",
            "특산품": "해산물",
            "관광유형": "바다·힐링",
            "랜드마크유형": "해변·섬",
            "추천기간": ["당일치기", "1박 2일"],
            "여행테마": ["사진 명소", "맛집·미식", "가족 여행"],
            "나이대별_추천": ["10대", "20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["2인", "3인", "4인 이상"],
            "소개": "서해안의 바다 풍경과 해산물을 함께 즐기기 좋은 여행지입니다.",
        },

        {
            "지역": "전라남도 고흥군",
            "위도": 34.6112,
            "경도": 127.2851,
            "인구": 61000,
            "인구변화율": -1.5,
            "음식점수": 91,
            "관광인지도": 31,
            "지역특색": 96,
            "대표음식": "장어구이",
            "음식점": "고흥 장어 로컬맛집",
            "관광지": "나로우주센터 · 팔영산",
            "지역행사": "고흥 유자축제",
            "특산품": "유자",
            "관광유형": "바다·우주",
            "랜드마크유형": "우주·산",
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["사진 명소", "액티비티", "맛집·미식"],
            "나이대별_추천": ["10대", "20대", "30~40대"],
            "인원수별_추천": ["2인", "3인", "4인 이상"],
            "소개": "우주센터와 바다, 유자 등 다른 지역에서 쉽게 경험하기 어려운 콘텐츠가 있습니다.",
        },

        {
            "지역": "경상북도 울릉군",
            "위도": 37.4844,
            "경도": 130.9057,
            "인구": 9000,
            "인구변화율": -1.2,
            "음식점수": 93,
            "관광인지도": 57,
            "지역특색": 99,
            "대표음식": "오징어",
            "음식점": "울릉도 오징어 로컬식당",
            "관광지": "독도전망대 · 성인봉",
            "지역행사": "울릉도 오징어축제",
            "특산품": "오징어·호박엿",
            "관광유형": "섬·자연",
            "랜드마크유형": "섬·바다",
            "추천기간": ["2박 3일", "3박 이상"],
            "여행테마": ["자연·힐링", "사진 명소", "맛집·미식"],
            "나이대별_추천": ["20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["2인", "3인", "4인 이상"],
            "소개": "섬이라는 지리적 특성과 독특한 자연환경을 활용한 특별한 로컬 여행지입니다.",
        },
    ]

    return pd.DataFrame(data)


df = load_data()


# =========================================================
# 이미지
# =========================================================

IMAGE_DATA = {

    "강원특별자치도 정선군": {
        "여행지": "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=80",
    },

    "전라남도 구례군": {
        "여행지": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1000&q=80",
    },

    "경상남도 의령군": {
        "여행지": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1555126634-323283e090fa?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=1000&q=80",
    },

    "전북특별자치도 무주군": {
        "여행지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1473445361085-b9a07f55608b?auto=format&fit=crop&w=1000&q=80",
    },

    "충청북도 단양군": {
        "여행지": "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=80",
    },

    "경상북도 영양군": {
        "여행지": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=1000&q=80",
    },

    "경상북도 청송군": {
        "여행지": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1000&q=80",
    },

    "충청남도 태안군": {
        "여행지": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1000&q=80",
    },

    "전라남도 고흥군": {
        "여행지": "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1000&q=80",
    },

    "경상북도 울릉군": {
        "여행지": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85",
        "먹거리": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1000&q=80",
        "구경거리": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1000&q=80",
    },
}


# =========================================================
# 추천 점수
# =========================================================

def calculate_hidden_score(row):

    hidden_score = 100 - row["관광인지도"]

    population_score = min(
        abs(row["인구변화율"]) * 5,
        20,
    )

    return round(
        hidden_score * 0.4
        + population_score * 0.1
        + row["음식점수"] * 0.25
        + row["지역특색"] * 0.25,
        1,
    )


df["추천점수"] = df.apply(
    calculate_hidden_score,
    axis=1,
)


# =========================================================
# 일정 문자열 분리
# =========================================================

def split_schedule_item(value):

    parts = str(value).split(
        "·",
        1,
    )

    if len(parts) == 2:

        return (
            parts[0].strip(),
            parts[1].strip(),
        )

    return (
        "",
        str(value).strip(),
    )


# =========================================================
# 이미지 카드
# =========================================================

def render_image_card(
    title,
    image_url,
    description,
):

    safe_title = html.escape(
        str(title)
    )

    safe_desc = html.escape(
        str(description)
    )

    safe_url = html.escape(
        str(image_url)
    )

    st.markdown(
        f"""
        <div class="photo-card">

            <img src="{safe_url}"
                 style="
                    width:100%;
                    height:190px;
                    object-fit:cover;
                    border-radius:12px;
                 ">

            <div style="
                font-size:16px;
                font-weight:900;
                margin-top:10px;
                color:#eef7f1;
            ">
                {safe_title}
            </div>

            <div style="
                font-size:12px;
                color:#9eb5a7;
                line-height:1.5;
                margin-top:5px;
            ">
                {safe_desc}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 취향 일치 판별
# =========================================================

def matches_preferences(row):

    age = st.session_state.age_group
    group = st.session_state.group_size
    duration = st.session_state.travel_duration
    theme = st.session_state.travel_theme
    food = st.session_state.food_type

    if age != "전체":
        if age not in row["나이대별_추천"]:
            return False

    if group != "전체":
        if group not in row["인원수별_추천"]:
            return False

    if duration != "전체":
        if duration not in row["추천기간"]:
            return False

    if theme != "전체":
        if theme not in row["여행테마"]:
            return False

    if food != "전체":

        food_map = {

            "한식": [
                "곤드레밥",
                "산채정식",
                "소바",
                "어죽",
                "마늘정식",
                "산채비빔밥",
                "닭백숙",
                "꽃게",
                "장어구이",
                "오징어",
            ],

            "해산물": [
                "꽃게",
                "장어구이",
                "오징어",
            ],

            "향토음식": [
                "곤드레밥",
                "산채정식",
                "소바",
                "어죽",
                "마늘정식",
                "산채비빔밥",
                "닭백숙",
            ],

            "간식·특산물": [
                "곤드레",
                "산수유",
                "의령망개떡",
                "단양마늘",
                "고추·산나물",
                "청송사과",
                "해산물",
                "유자",
                "오징어·호박엿",
            ],
        }

        allowed_foods = food_map.get(
            food,
            [],
        )

        if not any(
            item in str(row["대표음식"])
            or item in str(row["특산품"])
            for item in allowed_foods
        ):
            return False

    return True


# =========================================================
# 사이드바
# =========================================================

with st.sidebar:

    st.markdown(
        "### 🧭 나만의 로컬 여행 찾기"
    )


    # -----------------------------------------------------
    # 지역 행사 홍보
    # -----------------------------------------------------

    events = [

        {
            "title": "정선 아리랑제",
            "region": "강원특별자치도 정선군",
            "date": "2026.09.26 ~ 2026.09.30",
        },

        {
            "title": "단양 로컬 풍경전",
            "region": "충청북도 단양군",
            "date": "2026.09.25 ~ 2026.10.05",
        },

        {
            "title": "구례 가을 로컬마켓",
            "region": "전라남도 구례군",
            "date": "2026.09.27 ~ 2026.10.04",
        },

        {
            "title": "청송 가을 산책길",
            "region": "경상북도 청송군",
            "date": "2026.09.26 ~ 2026.10.11",
        },
    ]


    slides_html = ""


    for i, event in enumerate(events):

        display = (
            "block"
            if i == 0
            else "none"
        )

        slides_html += f"""
        <div class="event-slide"
             style="
                display:{display};
                background:#20342a;
                border:1px solid #355343;
                border-radius:14px;
                padding:15px;
                height:165px;
                box-sizing:border-box;
             ">

            <div style="
                font-size:12px;
                color:#9fe0b6;
                font-weight:800;
            ">
                📢 LOCAL EVENT
            </div>

            <div style="
                font-size:19px;
                font-weight:900;
                color:#ffffff;
                margin-top:8px;
            ">
                {html.escape(event["title"])}
            </div>

            <div style="
                font-size:12px;
                color:#b2c8ba;
                margin-top:8px;
            ">
                📍 {html.escape(event["region"])}
            </div>

            <div style="
                font-size:12px;
                color:#dcebe1;
                margin-top:5px;
            ">
                📅 {html.escape(event["date"])}
            </div>

        </div>
        """


    components.html(
        f"""
        <html>
        <head>
        <style>
        body {{
            margin:0;
            background:transparent;
            font-family:Arial,sans-serif;
        }}
        </style>
        </head>

        <body>

            <div id="event-container">
                {slides_html}
            </div>

            <script>

            let current = 0;

            const slides =
                document.querySelectorAll(".event-slide");

            function showNextSlide() {{

                if (slides.length === 0) {{
                    return;
                }}

                slides[current].style.display = "none";

                current =
                    (current + 1) % slides.length;

                slides[current].style.display =
                    "block";
            }}

            setInterval(
                showNextSlide,
                3000
            );

            </script>

        </body>
        </html>
        """,
        height=195,
    )


    st.divider()


    # -----------------------------------------------------
    # 여행 취향
    # -----------------------------------------------------

    age_options = [
        "전체",
        "10대",
        "20대",
        "30~40대",
        "50대 이상",
    ]

    age_group = st.selectbox(
        "👤 선호 나이대",
        age_options,
        index=age_options.index(
            st.session_state.age_group
        ),
    )

    st.session_state.age_group = age_group


    group_options = [
        "전체",
        "1인",
        "2인",
        "3인",
        "4인 이상",
    ]

    group_size = st.selectbox(
        "👥 여행 인원",
        group_options,
        index=group_options.index(
            st.session_state.group_size
        ),
    )

    st.session_state.group_size = group_size


    duration_options = [
        "전체",
        "당일치기",
        "1박 2일",
        "2박 3일",
        "3박 이상",
    ]

    travel_duration = st.selectbox(
        "🕐 여행 기간",
        duration_options,
        index=duration_options.index(
            st.session_state.travel_duration
        ),
    )

    st.session_state.travel_duration = travel_duration


    theme_options = [
        "전체",
        "액티비티",
        "역사·문화",
        "맛집·미식",
        "축제·행사",
        "사진 명소",
        "가족 여행",
        "자연·힐링",
    ]

    travel_theme = st.selectbox(
        "🎨 여행 테마",
        theme_options,
        index=theme_options.index(
            st.session_state.travel_theme
        ),
    )

    st.session_state.travel_theme = travel_theme


    food_options = [
        "전체",
        "한식",
        "해산물",
        "향토음식",
        "간식·특산물",
    ]

    food_type = st.selectbox(
        "🍴 선호 음식",
        food_options,
        index=food_options.index(
            st.session_state.food_type
        ),
    )

    st.session_state.food_type = food_type


    keyword = st.text_input(
        "🔎 지역·음식·관광지 검색",
        value=st.session_state.keyword,
        placeholder="예: 정선, 곤드레, 산, 시장",
    )

    st.session_state.keyword = keyword


    st.divider()


    # -----------------------------------------------------
    # 지도 표시
    # -----------------------------------------------------

    st.markdown(
        "### 🗺️ 지도 표시"
    )


    show_regions = st.checkbox(
        "📍 추천 지역",
        value=True,
    )

    show_food = st.checkbox(
        "🍴 음식점",
        value=True,
    )

    show_tour = st.checkbox(
        "🏞️ 관광지",
        value=True,
    )

    show_events = st.checkbox(
        "🎉 지역 행사",
        value=True,
    )

    show_specialty = st.checkbox(
        "🎁 특산품",
        value=True,
    )


    st.divider()


    if st.button(
        "🔄 선택 초기화",
        use_container_width=True,
    ):

        for key, value in defaults.items():
            st.session_state[key] = value

        st.rerun()


# =========================================================
# 검색 필터
# =========================================================

filtered_df = df.copy()


if keyword.strip():

    q = keyword.strip().lower()

    mask = (
        filtered_df["지역"].str.lower().str.contains(
            q,
            na=False,
        )
        |
        filtered_df["대표음식"].str.lower().str.contains(
            q,
            na=False,
        )
        |
        filtered_df["음식점"].str.lower().str.contains(
            q,
            na=False,
        )
        |
        filtered_df["관광지"].str.lower().str.contains(
            q,
            na=False,
        )
        |
        filtered_df["지역행사"].str.lower().str.contains(
            q,
            na=False,
        )
        |
        filtered_df["특산품"].str.lower().str.contains(
            q,
            na=False,
        )
        |
        filtered_df["소개"].str.lower().str.contains(
            q,
            na=False,
        )
    )

    filtered_df = filtered_df[mask]


# =========================================================
# 여행 기간 필터
# =========================================================

if st.session_state.travel_duration != "전체":

    filtered_df = filtered_df[
        filtered_df["추천기간"].apply(
            lambda x:
                st.session_state.travel_duration in x
        )
    ]


# =========================================================
# 여행 테마 필터
# =========================================================

if st.session_state.travel_theme != "전체":

    filtered_df = filtered_df[
        filtered_df["여행테마"].apply(
            lambda x:
                st.session_state.travel_theme in x
        )
    ]


# =========================================================
# 음식 필터
# =========================================================

if st.session_state.food_type != "전체":

    food_filter_map = {

        "한식": [
            "곤드레밥",
            "산채정식",
            "소바",
            "어죽",
            "마늘정식",
            "산채비빔밥",
            "닭백숙",
            "꽃게",
            "장어구이",
            "오징어",
        ],

        "해산물": [
            "꽃게",
            "장어구이",
            "오징어",
        ],

        "향토음식": [
            "곤드레밥",
            "산채정식",
            "소바",
            "어죽",
            "마늘정식",
            "산채비빔밥",
            "닭백숙",
        ],

        "간식·특산물": [
            "곤드레",
            "산수유",
            "의령망개떡",
            "단양마늘",
            "고추·산나물",
            "청송사과",
            "해산물",
            "유자",
            "오징어·호박엿",
        ],
    }


    allowed = food_filter_map[
        st.session_state.food_type
    ]


    filtered_df = filtered_df[
        filtered_df.apply(
            lambda r:
                any(
                    item in str(r["대표음식"])
                    or item in str(r["특산품"])
                    for item in allowed
                ),
            axis=1,
        )
    ]


# =========================================================
# 취향 일치 지역
# =========================================================

preference_df = filtered_df[
    filtered_df.apply(
        matches_preferences,
        axis=1,
    )
].copy()


# =========================================================
# 정렬
# =========================================================

filtered_df = filtered_df.sort_values(
    "추천점수",
    ascending=False,
)


preference_df = preference_df.sort_values(
    "추천점수",
    ascending=False,
)


# =========================================================
# 상단
# =========================================================

st.markdown(
    "## 🚗 로컬 쉼표"
)

st.caption(
    "숨은 지역의 먹거리·볼거리·특산품을 찾아 나만의 여행을 만들어보세요."
)


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "여행 인원",
        st.session_state.group_size,
    )


with m2:

    st.metric(
        "선호 나이대",
        st.session_state.age_group,
    )


with m3:

    st.metric(
        "선택 여행 기간",
        st.session_state.travel_duration,
    )


with m4:

    st.metric(
        "선택 여행 테마",
        st.session_state.travel_theme,
    )


st.write("")


# =========================================================
# 취향 일치 결과
# =========================================================

if len(preference_df) == 0:

    st.warning(
        "현재 선택한 여행 취향과 정확히 일치하는 지역이 없습니다. "
        "현재 검색 결과 중 가장 잘 맞는 지역을 추천합니다."
    )

else:

    st.success(
        f"🎯 선택한 여행 취향과 일치하는 지역 "
        f"{len(preference_df)}곳을 찾았습니다."
    )


# =========================================================
# 지역 선택
# =========================================================

if len(filtered_df) > 0:

    selected_region = st.session_state.get(
        "selected_region",
        filtered_df["지역"].iloc[0],
    )


    if selected_region not in filtered_df["지역"].tolist():

        selected_region = filtered_df[
            "지역"
        ].iloc[0]


    st.session_state.selected_region = (
        selected_region
    )


    selected_rows = filtered_df[
        filtered_df["지역"] == selected_region
    ]


    if len(selected_rows) > 0:

        row = selected_rows.iloc[0]

    else:

        row = filtered_df.iloc[0]

else:

    selected_region = ""

    st.session_state.selected_region = ""

    row = None


# =========================================================
# 맞춤 여행 코스 계산
# =========================================================

if row is not None:

    duration_days = {

        "당일치기": 1,
        "1박 2일": 2,
        "2박 3일": 3,
        "3박 이상": 4,
    }


    selected_duration = (
        st.session_state.travel_duration
    )


    if selected_duration == "전체":

        selected_duration = (
            row["추천기간"][0]
        )


    days = duration_days.get(
        selected_duration,
        1,
    )


    theme = st.session_state.travel_theme

    group = st.session_state.group_size

    age = st.session_state.age_group


    # -----------------------------------------------------
    # 테마별 활동
    # -----------------------------------------------------

    if theme == "액티비티":

        first_activity = (
            f"{row['관광지']} 중심 체험 및 "
            "가벼운 액티비티"
        )

        second_activity = (
            f"{row['관광지']} 주요 포인트 둘러보기"
        )


    elif theme == "역사·문화":

        first_activity = (
            f"{row['지역']}의 역사·문화 명소 탐방"
        )

        second_activity = (
            f"{row['지역행사']}와 지역 문화 알아보기"
        )


    elif theme == "맛집·미식":

        first_activity = (
            f"{row['지역']} 로컬시장 및 지역 먹거리 탐방"
        )

        second_activity = (
            f"{row['대표음식']} 맛집 중심 미식 여행"
        )


    elif theme == "축제·행사":

        first_activity = (
            f"{row['지역행사']} 관련 장소 탐방"
        )

        second_activity = (
            "지역 행사 및 로컬 프로그램 즐기기"
        )


    elif theme == "사진 명소":

        first_activity = (
            f"{row['관광지']} 사진 명소 탐방"
        )

        second_activity = (
            "노을·전망·지역 풍경 중심 촬영"
        )


    elif theme == "가족 여행":

        first_activity = (
            f"{row['관광지']} 가족 체험"
        )

        second_activity = (
            f"{row['지역']} 주변 편안한 산책"
        )


    else:

        first_activity = (
            f"{row['관광지']} 대표 명소 탐방"
        )

        second_activity = (
            f"{row['지역']}의 로컬 명소 둘러보기"
        )


    # -----------------------------------------------------
    # 여행 인원 팁
    # -----------------------------------------------------

    group_tip = {

        "1인":
            "혼자 이동하기 편하도록 주요 명소와 자유시간 중심으로 구성했습니다.",

        "2인":
            "사진 명소와 여유로운 식사, 산책 시간을 중심으로 구성했습니다.",

        "3인":
            "관광·식사·휴식의 균형을 고려한 코스입니다.",

        "4인 이상":
            "이동 부담을 줄이고 가족·단체 체험을 고려한 코스입니다.",

        "전체":
            "다양한 여행객이 이용할 수 있도록 관광·식사·휴식을 균형 있게 구성했습니다.",
    }.get(
        group,
        "기본 여행 코스로 구성했습니다.",
    )


    # -----------------------------------------------------
    # 나이대 팁
    # -----------------------------------------------------

    age_tip = {

        "10대":
            "체험·사진·활동적인 관광지를 중심으로 구성했습니다.",

        "20대":
            "감성 명소·맛집·사진과 활동적인 여행지를 중심으로 구성했습니다.",

        "30~40대":
            "관광·식사·휴식이 균형 잡힌 구성으로 만들었습니다.",

        "50대 이상":
            "무리 없는 이동과 자연·문화 중심의 여행을 고려했습니다.",

        "전체":
            "일반적인 관광·식사·휴식 중심의 기본 여행 코스입니다.",
    }.get(
        age,
        "일반적인 여행 코스로 구성했습니다.",
    )


    # -----------------------------------------------------
    # 일정 생성
    # -----------------------------------------------------

    daily_plan = []


    for day in range(
        1,
        days + 1,
    ):

        if day == 1:

            daily_plan.append(
                {
                    "day": day,

                    "morning":
                        f"09:30 · {first_activity}",

                    "lunch":
                        f"12:30 · {row['음식점']} / {row['대표음식']}",

                    "afternoon":
                        f"14:00 · {second_activity}",

                    "evening":
                        f"17:30 · {row['지역']} 로컬 거리 또는 시장 산책",
                }
            )


        elif day == days:

            daily_plan.append(
                {
                    "day": day,

                    "morning":
                        f"09:30 · {row['특산품']} 알아보기 및 기념품 구입",

                    "lunch":
                        f"12:00 · {row['대표음식']} 중심의 지역 식사",

                    "afternoon":
                        f"14:00 · {row['관광지']} 중 방문하지 못한 장소 탐방",

                    "evening":
                        "16:30 · 여행 정리 및 귀가",
                }
            )


        else:

            daily_plan.append(
                {
                    "day": day,

                    "morning":
                        f"09:30 · {row['관광지']} 주변 산책 및 자유 일정",

                    "lunch":
                        f"12:30 · {row['음식점']} 또는 인근 로컬 식당",

                    "afternoon":
                        f"14:00 · {row['지역행사']} 또는 지역 특색 체험",

                    "evening":
                        f"17:30 · {row['특산품']} 쇼핑 및 휴식",
                }
            )


# =========================================================
# 지도 + 맞춤 여행 코스
# =========================================================

if row is not None:

    map_col, course_col = st.columns(
        [1, 1],
        gap="medium",
    )


    # =====================================================
    # 왼쪽 : 지도
    # =====================================================

    with map_col:

        st.markdown(
            "### 🗺️ 숨은 지역 지도"
        )

        st.caption(
            "선택한 여행 취향과 일치하는 지역을 지도에서 확인해 보세요."
        )


        map_regions = preference_df.copy()


        if (
            st.session_state.age_group == "전체"
            and st.session_state.group_size == "전체"
            and st.session_state.travel_duration == "전체"
            and st.session_state.travel_theme == "전체"
            and st.session_state.food_type == "전체"
        ):

            map_regions = filtered_df.copy()


        if len(map_regions) > 0:

            center_lat = map_regions["위도"].mean()

            center_lon = map_regions["경도"].mean()

        else:

            center_lat = 36.2

            center_lon = 127.8


        fmap = folium.Map(
            location=[
                center_lat,
                center_lon,
            ],
            zoom_start=7,
            control_scale=True,
            tiles=None,
        )


        folium.TileLayer(
            tiles="OpenStreetMap",
            name="OpenStreetMap",
            control=True,
        ).add_to(fmap)


        folium.TileLayer(
            tiles="https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png",
            attr="VWorld",
            name="VWorld",
            control=True,
        ).add_to(fmap)


        Fullscreen(
            position="topright",
            title="전체화면",
            title_cancel="전체화면 종료",
            force_separate_button=True,
        ).add_to(fmap)


        bounds = []


        # -------------------------------------------------
        # 지역 마커
        # -------------------------------------------------

        if show_regions:

            for _, r in map_regions.iterrows():

                bounds.append(
                    [
                        r["위도"],
                        r["경도"],
                    ]
                )


                is_selected = (
                    r["지역"] == selected_region
                )


                popup_html = f"""
                <div style="
                    width:230px;
                    font-family:Arial;
                ">

                    <h4 style="
                        margin-bottom:6px;
                    ">
                        📍 {html.escape(str(r["지역"]))}
                    </h4>

                    <b>추천점수</b>
                    {r["추천점수"]}점
                    <br>

                    <b>대표음식</b>
                    {html.escape(str(r["대표음식"]))}
                    <br>

                    <b>관광지</b>
                    {html.escape(str(r["관광지"]))}
                    <br>

                    <b>특산품</b>
                    {html.escape(str(r["특산품"]))}

                </div>
                """


                folium.Marker(
                    location=[
                        r["위도"],
                        r["경도"],
                    ],

                    tooltip=f"📍 {r['지역']}",

                    popup=folium.Popup(
                        popup_html,
                        max_width=280,
                    ),

                    icon=folium.Icon(
                        color=(
                            "red"
                            if is_selected
                            else "green"
                        ),
                        icon="map-marker",
                        prefix="fa",
                    ),
                ).add_to(fmap)


        # -------------------------------------------------
        # 음식점
        # -------------------------------------------------

        if len(map_regions) > 0:

            if show_food:

                for _, r in map_regions.iterrows():

                    folium.Marker(
                        location=[
                            r["위도"] + 0.025,
                            r["경도"] + 0.025,
                        ],

                        tooltip=f"🍴 {r['음식점']}",

                        popup=f"""
                        <b>🍴 음식점</b><br>
                        {html.escape(str(r["음식점"]))}<br>
                        대표음식: {html.escape(str(r["대표음식"]))}
                        """,

                        icon=folium.Icon(
                            color="orange",
                            icon="cutlery",
                            prefix="fa",
                        ),
                    ).add_to(fmap)


            # -------------------------------------------------
            # 관광지
            # -------------------------------------------------

            if show_tour:

                for _, r in map_regions.iterrows():

                    folium.Marker(
                        location=[
                            r["위도"] - 0.025,
                            r["경도"] + 0.025,
                        ],

                        tooltip=f"🏞️ {r['관광지']}",

                        popup=f"""
                        <b>🏞️ 관광지</b><br>
                        {html.escape(str(r["관광지"]))}
                        """,

                        icon=folium.Icon(
                            color="blue",
                            icon="camera",
                            prefix="fa",
                        ),
                    ).add_to(fmap)


            # -------------------------------------------------
            # 행사
            # -------------------------------------------------

            if show_events:

                for _, r in map_regions.iterrows():

                    folium.Marker(
                        location=[
                            r["위도"] + 0.025,
                            r["경도"] - 0.025,
                        ],

                        tooltip=f"🎉 {r['지역행사']}",

                        popup=f"""
                        <b>🎉 지역 행사</b><br>
                        {html.escape(str(r["지역행사"]))}
                        """,

                        icon=folium.Icon(
                            color="purple",
                            icon="calendar",
                            prefix="fa",
                        ),
                    ).add_to(fmap)


            # -------------------------------------------------
            # 특산품
            # -------------------------------------------------

            if show_specialty:

                for _, r in map_regions.iterrows():

                    folium.Marker(
                        location=[
                            r["위도"] - 0.025,
                            r["경도"] - 0.025,
                        ],

                        tooltip=f"🎁 {r['특산품']}",

                        popup=f"""
                        <b>🎁 특산품</b><br>
                        {html.escape(str(r["특산품"]))}
                        """,

                        icon=folium.Icon(
                            color="cadetblue",
                            icon="gift",
                            prefix="fa",
                        ),
                    ).add_to(fmap)


        # -------------------------------------------------
        # 지도 자동 확대
        # -------------------------------------------------

        if len(bounds) >= 2:

            fmap.fit_bounds(
                bounds,
                padding=(35, 35),
                max_zoom=10,
            )

        elif len(bounds) == 1:

            fmap.location = bounds[0]
            fmap.zoom_start = 10

        else:

            fmap.location = [
                36.2,
                127.8,
            ]

            fmap.zoom_start = 7


        folium.LayerControl(
            collapsed=False
        ).add_to(fmap)


        st_folium(
            fmap,
            width=None,
            height=600,
            returned_objects=[],
        )


    # =====================================================
    # 오른쪽 : 맞춤 여행 코스
    # =====================================================

    with course_col:

        st.markdown(
            "### 🧭 맞춤 여행 코스 만들기"
        )

        st.caption(
            f"{row['지역']} · 선택한 여행 조건을 기준으로 구성된 추천 코스"
        )


        # -------------------------------------------------
        # 추천 점수 / 여행 기간
        # -------------------------------------------------

        tag1, tag2 = st.columns(2)


        with tag1:

            st.metric(
                "로컬 추천점수",
                f"{row['추천점수']}점",
            )


        with tag2:

            st.metric(
                "추천 여행기간",
                f"{days}일",
            )


        st.write("")


        # -------------------------------------------------
        # 지역 특징
        # -------------------------------------------------

        st.markdown(
            f"📍 {row['관광유형']}  ·  "
            f"🗺️ {row['랜드마크유형']}  ·  "
            f"🍴 {row['대표음식']}  ·  "
            f"🎁 {row['특산품']}"
        )


        st.divider()

                # =====================================================
        # 교통수단 & 예상 소요시간
        # =====================================================

        st.markdown("#### 🚗 교통수단 & 예상 소요시간")

        transport_col1, transport_col2 = st.columns(2)

        with transport_col1:
            st.markdown(
                """
                <div class="section-card">
                    <div style="font-size:22px; margin-bottom:8px;">🚗</div>
                    <div style="font-size:17px; font-weight:700;">
                        자가용
                    </div>
                    <div style="font-size:14px; opacity:0.75; margin-top:5px;">
                        주요 관광지까지 약 10~30분
                    </div>
                    <div style="font-size:13px; opacity:0.6; margin-top:4px;">
                        지역 내 이동이 편리해요
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with transport_col2:
            st.markdown(
                """
                <div class="section-card">
                    <div style="font-size:22px; margin-bottom:8px;">🚌</div>
                    <div style="font-size:17px; font-weight:700;">
                        대중교통
                    </div>
                    <div style="font-size:14px; opacity:0.75; margin-top:5px;">
                        주요 관광지까지 약 20~60분
                    </div>
                    <div style="font-size:13px; opacity:0.6; margin-top:4px;">
                        버스 중심으로 이동할 수 있어요
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        transport_col3, transport_col4 = st.columns(2)

        with transport_col3:
            st.markdown(
                """
                <div class="section-card">
                    <div style="font-size:22px; margin-bottom:8px;">🚕</div>
                    <div style="font-size:17px; font-weight:700;">
                        택시
                    </div>
                    <div style="font-size:14px; opacity:0.75; margin-top:5px;">
                        관광지 간 약 10~25분
                    </div>
                    <div style="font-size:13px; opacity:0.6; margin-top:4px;">
                        짧은 거리 이동에 적합해요
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with transport_col4:
            st.markdown(
                """
                <div class="section-card">
                    <div style="font-size:22px; margin-bottom:8px;">🚶</div>
                    <div style="font-size:17px; font-weight:700;">
                        도보
                    </div>
                    <div style="font-size:14px; opacity:0.75; margin-top:5px;">
                        관광지 주변 약 5~20분
                    </div>
                    <div style="font-size:13px; opacity:0.6; margin-top:4px;">
                        가까운 명소를 천천히 둘러봐요
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        # -------------------------------------------------
        # 추천 일정
        # -------------------------------------------------

        st.markdown(
            "### 📅 추천 일정"
        )


        for plan in daily_plan:

            morning_time, morning_text = (
                split_schedule_item(
                    plan["morning"]
                )
            )

            lunch_time, lunch_text = (
                split_schedule_item(
                    plan["lunch"]
                )
            )

            afternoon_time, afternoon_text = (
                split_schedule_item(
                    plan["afternoon"]
                )
            )

            evening_time, evening_text = (
                split_schedule_item(
                    plan["evening"]
                )
            )


            if plan["day"] == 1:

                summary = (
                    "대표 관광지 · 로컬 맛집"
                )

            elif plan["day"] == days:

                summary = (
                    "특산품 · 여행 마무리"
                )

            else:

                summary = (
                    "자유 산책 · 지역 체험"
                )


            with st.expander(
                f"📅 {plan['day']}일 차  ·  {summary}",
                expanded=(plan["day"] == 1),
            ):

                schedule_col1, schedule_col2 = (
                    st.columns(2)
                )


                with schedule_col1:

                    st.markdown(
                        f"""
                        **🌅 오전**

                        <span class="schedule-time">
                        {html.escape(morning_time)}
                        </span>

                        <div class="schedule-text">
                        {html.escape(morning_text)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    st.write("")


                    st.markdown(
                        f"""
                        **🍴 점심**

                        <span class="schedule-time">
                        {html.escape(lunch_time)}
                        </span>

                        <div class="schedule-text">
                        {html.escape(lunch_text)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                with schedule_col2:

                    st.markdown(
                        f"""
                        **🏞️ 오후**

                        <span class="schedule-time">
                        {html.escape(afternoon_time)}
                        </span>

                        <div class="schedule-text">
                        {html.escape(afternoon_text)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                    st.write("")


                    st.markdown(
                        f"""
                        **🌙 저녁**

                        <span class="schedule-time">
                        {html.escape(evening_time)}
                        </span>

                        <div class="schedule-text">
                        {html.escape(evening_time)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


        st.caption(
            "※ 현재 코스는 플랫폼의 예시 데이터 기반 추천 일정입니다. "
            "실제 운영시간 및 행사 일정은 방문 전 확인해주세요."
        )


# =========================================================
# 길찾기
# =========================================================

if row is not None:

    st.markdown(
        "### 🚗 여행지 길찾기"
    )


    query = urllib.parse.quote(
        f"{row['지역']} {row['관광지']}"
    )


    nav1, nav2 = st.columns(2)


    with nav1:

        st.link_button(
            "🗺️ 네이버 지도에서 길찾기",
            f"https://map.naver.com/p/search/{query}",
            use_container_width=True,
        )


    with nav2:

        st.link_button(
            "📍 카카오맵에서 검색",
            f"https://map.kakao.com/?q={query}",
            use_container_width=True,
        )


# =========================================================
# 지금 취향에 맞는 추천 지역
# =========================================================

st.markdown(
    "## 📍 지금 취향에 맞는 추천 지역"
)

st.caption(
    "선택한 여행 취향과 지역 정보를 종합하여 가장 잘 맞는 지역을 추천합니다."
)


# =========================================================
# 추천 지역 선정
# =========================================================

if len(preference_df) > 0:

    recommended_region = (
        preference_df
        .sort_values(
            "추천점수",
            ascending=False,
        )
        .iloc[0]
    )

    exact_match = True


elif len(filtered_df) > 0:

    recommended_region = (
        filtered_df
        .sort_values(
            "추천점수",
            ascending=False,
        )
        .iloc[0]
    )

    exact_match = False


else:

    recommended_region = None

    exact_match = False


# =========================================================
# 추천 지역
# =========================================================

if recommended_region is not None:

    region_name = str(
        recommended_region["지역"]
    )

    food = str(
        recommended_region["대표음식"]
    )

    restaurant = str(
        recommended_region["음식점"]
    )

    tourist = str(
        recommended_region["관광지"]
    )

    specialty = str(
        recommended_region["특산품"]
    )

    travel_type = str(
        recommended_region["관광유형"]
    )

    landmark_type = str(
        recommended_region["랜드마크유형"]
    )

    duration = str(
        recommended_region["추천기간"]
    )


    region_images = IMAGE_DATA.get(
        region_name,
        {}
    )

    region_image = region_images.get(
        "여행지"
    )


    if exact_match:

        st.success(
            f"🎯 **{region_name}**이(가) "
            "현재 선택한 여행 취향과 잘 맞습니다."
        )

    else:

        st.info(
            f"💡 현재 조건에서 가장 잘 맞는 지역으로 "
            f"**{region_name}**을(를) 추천합니다."
        )


    # =====================================================
    # 추천 지역 배너
    # =====================================================

    with st.container(border=True):

        # -------------------------------------------------
        # 지역 사진
        # -------------------------------------------------

        if region_image:

            st.image(
                region_image,
                use_container_width=True,
            )


        # -------------------------------------------------
        # 지역 이름
        # -------------------------------------------------

        st.markdown(
            "### ✨ 가장 잘 맞는 추천 지역"
        )

        st.markdown(
            f"# 📍 {region_name}"
        )


        st.divider()


        # =================================================
        # 왜 이 지역을 추천했을까?
        # =================================================

        st.markdown(
            "### 💡 왜 이 지역을 추천했을까?"
        )

        st.caption(
            "여행 취향과 지역 특징을 바탕으로 핵심 정보만 정리했습니다."
        )


        reason_col1, reason_col2 = st.columns(
            2,
            gap="medium",
        )


        with reason_col1:

            with st.container(border=True):

                st.markdown(
                    "#### 🧭 여행 취향"
                )

                if theme != "전체":

                    st.markdown(
                        f"**{theme}** 여행에 잘 어울려요."
                    )

                else:

                    st.markdown(
                        f"**{travel_type}** 중심의 "
                        "여행을 즐기기 좋아요."
                    )

                st.caption(
                    f"추천 기간 · {duration}"
                )


        with reason_col2:

            with st.container(border=True):

                st.markdown(
                    "#### 🍴 대표 먹거리"
                )

                st.markdown(
                    f"**{food}**"
                )

                st.caption(
                    f"추천 음식점 · {restaurant}"
                )


        reason_col3, reason_col4 = st.columns(
            2,
            gap="medium",
        )


        with reason_col3:

            with st.container(border=True):

                st.markdown(
                    "#### 🏞️ 대표 볼거리"
                )

                st.markdown(
                    f"**{tourist}**"
                )

                st.caption(
                    f"{landmark_type} · {travel_type}"
                )


        with reason_col4:

            with st.container(border=True):

                st.markdown(
                    "#### 🎁 로컬 포인트"
                )

                st.markdown(
                    f"**{specialty}**"
                )

                st.caption(
                    "지역 대표 특산품"
                )


        st.info(
            f"📌 **{region_name}**에서 "
            f"**{food}**을(를) 맛보고 "
            f"**{tourist}**을(를) 둘러보며 "
            f"**{specialty}**까지 경험해 보세요."
        )


else:

    with st.container(border=True):

        st.markdown(
            "### 🔎 검색 결과가 없습니다."
        )

        st.caption(
            "사이드바의 검색어나 여행 조건을 변경해 주세요."
        )


# =========================================================
# 상세 지역 정보
# =========================================================

if row is not None:

    st.markdown(
        "## 📚 상세 지역 정보"
    )

    st.caption(
        "추천 지역의 여행 정보를 한눈에 확인해 보세요."
    )


    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🏞️ 관광지",
            "🍴 먹거리",
            "🎉 지역 행사",
            "🎁 특산품",
        ]
    )


    # -----------------------------------------------------
    # 관광지
    # -----------------------------------------------------

    with tab1:

        with st.container(border=True):

            st.markdown(
                "### 🏞️ 추천 관광지"
            )

            st.markdown(
                f"## {str(row['관광지'])}"
            )

            st.divider()


            info_col1, info_col2 = st.columns(2)


            with info_col1:

                st.markdown(
                    "#### 📍 관광 유형"
                )

                st.write(
                    str(row["관광유형"])
                )


            with info_col2:

                st.markdown(
                    "#### 🗺️ 랜드마크 유형"
                )

                st.write(
                    str(row["랜드마크유형"])
                )


            st.info(
                "지역의 대표적인 관광 명소를 중심으로 "
                "여행 코스를 구성할 수 있습니다."
            )


            # 관광지 이미지

            image_url = IMAGE_DATA.get(
                row["지역"],
                {}
            ).get(
                "여행지"
            )

            if image_url:

                st.image(
                    image_url,
                    use_container_width=True,
                )


    # -----------------------------------------------------
    # 먹거리
    # -----------------------------------------------------

    with tab2:

        with st.container(border=True):

            st.markdown(
                "### 🍴 지역 대표 먹거리"
            )

            st.markdown(
                f"## {str(row['대표음식'])}"
            )

            st.divider()


            st.markdown(
                "#### 🍽️ 추천 음식점"
            )

            st.write(
                str(row["음식점"])
            )


            image_url = IMAGE_DATA.get(
                row["지역"],
                {}
            ).get(
                "먹거리"
            )

            if image_url:

                st.image(
                    image_url,
                    use_container_width=True,
                )


            st.info(
                "해당 지역의 대표 음식을 중심으로 "
                "로컬 맛집을 탐색해 보세요."
            )


    # -----------------------------------------------------
    # 지역 행사
    # -----------------------------------------------------

    with tab3:

        with st.container(border=True):

            st.markdown(
                "### 🎉 지역 행사"
            )

            st.markdown(
                f"## {str(row['지역행사'])}"
            )

            st.divider()


            st.markdown(
                "#### 📅 추천 여행 기간"
            )

            st.write(
                str(row["추천기간"])
            )


            st.info(
                "지역 행사와 주변 관광지를 함께 둘러보면 "
                "더 풍성한 여행을 즐길 수 있습니다."
            )


    # -----------------------------------------------------
    # 특산품
    # -----------------------------------------------------

    with tab4:

        with st.container(border=True):

            st.markdown(
                "### 🎁 지역 특산품"
            )

            st.markdown(
                f"## {str(row['특산품'])}"
            )

            st.divider()


            st.markdown(
                "#### 📍 지역 특색"
            )

            st.write(
                str(row["소개"])
            )


            image_url = IMAGE_DATA.get(
                row["지역"],
                {}
            ).get(
                "구경거리"
            )

            if image_url:

                st.image(
                    image_url,
                    use_container_width=True,
                )


            st.info(
                "지역의 특산품과 먹거리를 통해 "
                "해당 지역만의 로컬 문화를 경험해 보세요."
            )


# =========================================================
# 지역 소개
# =========================================================

if row is not None:

    st.markdown(
        "### 💬 지역 소개"
    )

    st.info(
        row["소개"]
    )


# =========================================================
# 푸터
# =========================================================

st.divider()


st.caption(
    "🚗 로컬 쉼표 · SGIS 기반 숨은 지역 발견 플랫폼"
)


st.caption(
    "※ 본 서비스의 지역·관광·음식 데이터는 플랫폼 시연을 위한 예시 데이터이며, "
    "실제 방문 전 운영시간·행사 일정·교통정보를 확인해주세요."
)
