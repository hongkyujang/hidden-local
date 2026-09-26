import urllib.parse

import pandas as pd
import streamlit as st
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
# 세션 상태 기본값
# =========================================================

defaults = {
    "age_group": "전체",
    "group_size": "전체",
    "travel_duration": "전체",
    "travel_theme": "전체",
    "food_type": "전체",
    "sort_type": "점수순",
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

section[data-testid="stSidebar"] {
    background: #17251f;
}

section[data-testid="stSidebar"] > div {
    background: #17251f;
}

h1, h2, h3, h4, h5, h6 {
    color: #f4f7f5 !important;
}

p, span, label, div {
    color: inherit;
}

.top-logo {
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 2px;
}

.top-subtitle {
    color: #aebdb6;
    font-size: 15px;
    margin-bottom: 22px;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 12px;
}

.metric-card {
    background: #18251f;
    border: 1px solid #2a3932;
    border-radius: 16px;
    padding: 18px;
    min-height: 105px;
}

.metric-title {
    color: #aebdb6;
    font-size: 13px;
    margin-bottom: 7px;
}

.metric-value {
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
}

.map-course-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 15px;
}

.course-box {
    background: #18251f;
    border: 1px solid #2a3932;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.course-day {
    font-size: 19px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 12px;
}

.course-item {
    background: #111a16;
    border-radius: 12px;
    padding: 13px;
    margin-bottom: 8px;
    border: 1px solid #26352e;
}

.score-box {
    background: #1c2c25;
    border: 1px solid #385447;
    border-radius: 15px;
    padding: 16px;
    text-align: center;
}

.score-number {
    font-size: 30px;
    font-weight: 900;
    color: #ffffff;
}

.score-label {
    color: #aebdb6;
    font-size: 13px;
}

.photo-card {
    background: #18251f;
    border: 1px solid #2a3932;
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
}

.photo-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 10px;
}

.info-card {
    background: #18251f;
    border: 1px solid #2a3932;
    border-radius: 15px;
    padding: 16px;
    margin-bottom: 12px;
}

.small-text {
    color: #aebdb6;
    font-size: 13px;
}

.stButton > button {
    border-radius: 10px;
}

.stLinkButton > a {
    border-radius: 10px;
}

div[data-testid="stMetric"] {
    background: #18251f;
    border: 1px solid #2a3932;
    border-radius: 14px;
    padding: 12px;
}

div[data-testid="stExpander"] {
    background: #18251f;
    border: 1px solid #2a3932;
    border-radius: 14px;
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
            "소개": "지리산의 자연과 지역 음식, 전통문화가 어우러진 로컬 여행지입니다.",
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
            "소개": "잘 알려지지 않은 역사문화 콘텐츠와 지역 먹거리를 함께 즐길 수 있습니다.",
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
            "소개": "자연 속 체험과 산악 관광을 즐기기 좋은 지역입니다.",
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
            "소개": "강과 산을 활용한 액티비티와 지역 먹거리를 함께 즐길 수 있습니다.",
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
            "여행테마": ["사진 명소", "맛집·미식", "자연·힐링"],
            "나이대별_추천": ["20대", "30~40대", "50대 이상"],
            "인원수별_추천": ["1인", "2인", "3인", "4인 이상"],
            "소개": "관광객이 비교적 적고 자연과 밤하늘을 조용하게 즐길 수 있는 지역입니다.",
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
            "소개": "산과 폭포, 지역 특산물을 중심으로 여유로운 여행을 즐길 수 있습니다.",
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
            "소개": "서해 바다와 지역 먹거리를 함께 즐길 수 있는 로컬 여행지입니다.",
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
            "소개": "우주와 바다, 지역 먹거리를 동시에 경험할 수 있는 독특한 여행지입니다.",
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
            "소개": "섬 특유의 자연경관과 지역 먹거리를 경험할 수 있는 특별한 여행지입니다.",
        },
    ]

    return pd.DataFrame(data)


df = load_data()


# =========================================================
# 추천 점수 계산
# =========================================================

def calculate_hidden_score(row):

    hidden_score = 100 - row["관광인지도"]

    population_score = min(
        abs(row["인구변화율"]) * 5,
        20
    )

    return round(
        hidden_score * 0.4
        + population_score * 0.1
        + row["음식점수"] * 0.25
        + row["지역특색"] * 0.25,
        1
    )


df["추천점수"] = df.apply(
    calculate_hidden_score,
    axis=1
)


# =========================================================
# 취향 일치 여부
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
                "의령망개떡",
                "곤드레",
                "산수유",
                "단양마늘",
                "고추·산나물",
                "청송사과",
                "해산물",
                "유자",
                "오징어·호박엿",
            ],
        }

        allowed_foods = food_map.get(food, [])

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
        """
        <div class="top-logo">🚗 로컬 쉼표</div>
        <div class="top-subtitle">
        잘 알려지지 않은 지역의 특별한 여행을 발견하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 여행 취향")

    age_options = [
        "전체",
        "10대",
        "20대",
        "30~40대",
        "50대 이상",
    ]

    group_options = [
        "전체",
        "1인",
        "2인",
        "3인",
        "4인 이상",
    ]

    duration_options = [
        "전체",
        "당일치기",
        "1박 2일",
        "2박 3일",
        "3박 이상",
    ]

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

    food_options = [
        "전체",
        "한식",
        "해산물",
        "향토음식",
        "간식·특산물",
    ]

    sort_options = [
        "점수순",
        "인구순",
        "음식점수순",
        "지역특색순",
    ]

    st.session_state.age_group = st.selectbox(
        "👤 선호 나이대",
        age_options,
        index=age_options.index(st.session_state.age_group),
    )

    st.session_state.group_size = st.selectbox(
        "👥 여행 인원",
        group_options,
        index=group_options.index(st.session_state.group_size),
    )

    st.session_state.travel_duration = st.selectbox(
        "📅 여행 기간",
        duration_options,
        index=duration_options.index(
            st.session_state.travel_duration
        ),
    )

    st.session_state.travel_theme = st.selectbox(
        "🎨 여행 테마",
        theme_options,
        index=theme_options.index(
            st.session_state.travel_theme
        ),
    )

    st.session_state.food_type = st.selectbox(
        "🍴 선호 음식",
        food_options,
        index=food_options.index(
            st.session_state.food_type
        ),
    )

    st.session_state.sort_type = st.selectbox(
        "↕️ 정렬",
        sort_options,
        index=sort_options.index(
            st.session_state.sort_type
        ),
    )

    st.session_state.keyword = st.text_input(
        "🔎 지역 검색",
        value=st.session_state.keyword,
        placeholder="예: 정선, 산, 맛집",
    )

    st.markdown("---")

    st.markdown("### 🗺️ 지도 표시")

    show_regions = st.checkbox(
        "📍 추천 지역",
        value=True,
    )

    show_food = st.checkbox(
        "🍴 음식점",
        value=False,
    )

    show_tour = st.checkbox(
        "🏞️ 관광지",
        value=False,
    )

    show_event = st.checkbox(
        "🎉 지역 행사",
        value=False,
    )

    show_specialty = st.checkbox(
        "🎁 특산품",
        value=False,
    )

    st.markdown("---")

    if st.button(
        "🔄 필터 초기화",
        use_container_width=True,
    ):

        for key, value in defaults.items():
            st.session_state[key] = value

        st.rerun()


# =========================================================
# 필터링
# =========================================================

filtered_df = df.copy()


keyword = st.session_state.keyword.strip()

if keyword:

    mask = (
        filtered_df["지역"].str.contains(
            keyword,
            case=False,
            na=False
        )
        | filtered_df["대표음식"].str.contains(
            keyword,
            case=False,
            na=False
        )
        | filtered_df["음식점"].str.contains(
            keyword,
            case=False,
            na=False
        )
        | filtered_df["관광지"].str.contains(
            keyword,
            case=False,
            na=False
        )
        | filtered_df["지역행사"].str.contains(
            keyword,
            case=False,
            na=False
        )
        | filtered_df["특산품"].str.contains(
            keyword,
            case=False,
            na=False
        )
        | filtered_df["소개"].str.contains(
            keyword,
            case=False,
            na=False
        )
    )

    filtered_df = filtered_df[mask]


if st.session_state.travel_duration != "전체":

    filtered_df = filtered_df[
        filtered_df["추천기간"].apply(
            lambda x:
            st.session_state.travel_duration in x
        )
    ]


if st.session_state.travel_theme != "전체":

    filtered_df = filtered_df[
        filtered_df["여행테마"].apply(
            lambda x:
            st.session_state.travel_theme in x
        )
    ]


# =========================================================
# 선호 조건 일치 지역
# =========================================================

preference_df = filtered_df[
    filtered_df.apply(
        matches_preferences,
        axis=1
    )
].copy()


# =========================================================
# 정렬
# =========================================================

if st.session_state.sort_type == "점수순":

    filtered_df = filtered_df.sort_values(
        "추천점수",
        ascending=False
    )

elif st.session_state.sort_type == "인구순":

    filtered_df = filtered_df.sort_values(
        "인구",
        ascending=False
    )

elif st.session_state.sort_type == "음식점수순":

    filtered_df = filtered_df.sort_values(
        "음식점수",
        ascending=False
    )

elif st.session_state.sort_type == "지역특색순":

    filtered_df = filtered_df.sort_values(
        "지역특색",
        ascending=False
    )


# =========================================================
# 상단 제목
# =========================================================

st.markdown(
    """
    <div class="top-logo">🚗 로컬 쉼표</div>
    <div class="top-subtitle">
        데이터로 발견하는 새로운 국내 로컬 여행
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 상단 선택 정보
# =========================================================

metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">여행 인원</div>
            <div class="metric-value">
                {st.session_state.group_size}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with metric2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">선호 나이대</div>
            <div class="metric-value">
                {st.session_state.age_group}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with metric3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">선택 여행 기간</div>
            <div class="metric-value">
                {st.session_state.travel_duration}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with metric4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">선택 여행 테마</div>
            <div class="metric-value">
                {st.session_state.travel_theme}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 지역 선택
# =========================================================

if len(filtered_df) > 0:

    region_list = filtered_df["지역"].tolist()

    if st.session_state.selected_region not in region_list:
        st.session_state.selected_region = region_list[0]

    selected_region = st.selectbox(
        "📍 여행 지역 선택",
        region_list,
        index=region_list.index(
            st.session_state.selected_region
        ),
    )

    st.session_state.selected_region = selected_region

    row = filtered_df[
        filtered_df["지역"] == selected_region
    ].iloc[0]

else:

    row = None

    st.warning(
        "현재 선택한 조건에 맞는 지역이 없습니다."
    )


# =========================================================
# 추천 지역 - 가장 추천하는 지역 1곳
# =========================================================

if len(preference_df) > 0:

    st.markdown(
        "### 📍 지금 취향에 맞는 추천 지역"
    )

    st.caption(
        "선택한 여행 취향을 기준으로 가장 높은 추천점수를 받은 지역입니다."
    )

    best_region = preference_df.sort_values(
        "추천점수",
        ascending=False
    ).iloc[0]

    recommend_col1, recommend_col2 = st.columns(
        [1, 2]
    )

    with recommend_col1:

        st.metric(
            "🏆 로컬 추천점수",
            f"{best_region['추천점수']}점"
        )

    with recommend_col2:

        st.markdown(
            f"## 📍 {best_region['지역']}"
        )

        st.write(
            f"**🍴 대표 음식:** "
            f"{best_region['대표음식']}"
        )

        st.write(
            f"**🏞️ 주요 관광지:** "
            f"{best_region['관광지']}"
        )

        st.write(
            f"**🎁 특산품:** "
            f"{best_region['특산품']}"
        )

        st.write(
            f"**🎨 여행 유형:** "
            f"{best_region['관광유형']}"
        )

else:

    st.markdown(
        "### 📍 지금 취향에 맞는 추천 지역"
    )

    st.info(
        "현재 선택한 여행 취향에 맞는 추천 지역이 없습니다. "
        "사이드바의 조건을 조금 완화해보세요."
    )


# =========================================================
# 지도 + 맞춤 여행 코스
#
# ※ 기존의
# 「숨은 지역 지도 + 맞춤 여행 코스」
# 제목 배너를 삭제하고 바로 두 영역을 표시
# =========================================================

map_col, course_col = st.columns(
    [1, 1],
    gap="medium"
)


# =========================================================
# 지도
# =========================================================

with map_col:

    st.markdown(
        "### 🗺️ 숨은 지역 지도"
    )

    map_regions = preference_df.copy()

    all_preferences = (
        st.session_state.age_group == "전체"
        and st.session_state.group_size == "전체"
        and st.session_state.travel_duration == "전체"
        and st.session_state.travel_theme == "전체"
        and st.session_state.food_type == "전체"
    )

    if all_preferences:
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
            center_lon
        ],
        zoom_start=7,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    Fullscreen(
        position="topright"
    ).add_to(fmap)

    # -----------------------------------------------------
    # 추천 지역 마커
    # -----------------------------------------------------

    bounds = []

    for _, r in map_regions.iterrows():

        lat = r["위도"]
        lon = r["경도"]

        bounds.append(
            [lat, lon]
        )

        if show_regions:

            folium.Marker(
                location=[lat, lon],
                tooltip=f"📍 {r['지역']}",
                popup=folium.Popup(
                    f"""
                    <b>{r['지역']}</b><br>
                    추천점수: {r['추천점수']}점<br>
                    대표음식: {r['대표음식']}<br>
                    관광지: {r['관광지']}
                    """,
                    max_width=300,
                ),
                icon=folium.Icon(
                    icon="map-marker",
                    prefix="fa",
                ),
            ).add_to(fmap)

        # -------------------------------------------------
        # 음식점
        # -------------------------------------------------

        if show_food:

            folium.Marker(
                location=[
                    lat + 0.025,
                    lon + 0.025
                ],
                tooltip=f"🍴 {r['음식점']}",
                popup=folium.Popup(
                    f"""
                    <b>🍴 음식점</b><br>
                    {r['음식점']}<br>
                    대표 음식: {r['대표음식']}
                    """,
                    max_width=300,
                ),
                icon=folium.Icon(
                    color="red",
                    icon="cutlery",
                    prefix="fa",
                ),
            ).add_to(fmap)

        # -------------------------------------------------
        # 관광지
        # -------------------------------------------------

        if show_tour:

            folium.Marker(
                location=[
                    lat - 0.025,
                    lon + 0.025
                ],
                tooltip=f"🏞️ {r['관광지']}",
                popup=folium.Popup(
                    f"""
                    <b>🏞️ 관광지</b><br>
                    {r['관광지']}
                    """,
                    max_width=300,
                ),
                icon=folium.Icon(
                    color="green",
                    icon="camera",
                    prefix="fa",
                ),
            ).add_to(fmap)

        # -------------------------------------------------
        # 지역 행사
        # -------------------------------------------------

        if show_event:

            folium.Marker(
                location=[
                    lat + 0.025,
                    lon - 0.025
                ],
                tooltip=f"🎉 {r['지역행사']}",
                popup=folium.Popup(
                    f"""
                    <b>🎉 지역 행사</b><br>
                    {r['지역행사']}
                    """,
                    max_width=300,
                ),
                icon=folium.Icon(
                    color="purple",
                    icon="star",
                    prefix="fa",
                ),
            ).add_to(fmap)

        # -------------------------------------------------
        # 특산품
        # -----------------------------------------------------

        if show_specialty:

            folium.Marker(
                location=[
                    lat - 0.025,
                    lon - 0.025
                ],
                tooltip=f"🎁 {r['특산품']}",
                popup=folium.Popup(
                    f"""
                    <b>🎁 특산품</b><br>
                    {r['특산품']}
                    """,
                    max_width=300,
                ),
                icon=folium.Icon(
                    color="orange",
                    icon="gift",
                    prefix="fa",
                ),
            ).add_to(fmap)

    # -----------------------------------------------------
    # 지도 자동 확대
    # -----------------------------------------------------

    if len(bounds) >= 2:

        fmap.fit_bounds(
            bounds,
            padding=(35, 35),
        )

    elif len(bounds) == 1:

        fmap.location = bounds[0]
        fmap.zoom_start = 10

    else:

        fmap.location = [
            36.2,
            127.8
        ]

        fmap.zoom_start = 7

    st_folium(
        fmap,
        width=None,
        height=600,
        returned_objects=[],
    )


# =========================================================
# 맞춤 여행 코스
# =========================================================

with course_col:

    st.markdown(
        "### 🧭 맞춤 여행 코스"
    )

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

            if len(row["추천기간"]) > 0:
                selected_duration = row["추천기간"][0]
            else:
                selected_duration = "1박 2일"

        days = duration_days.get(
            selected_duration,
            2
        )

        # -------------------------------------------------
        # 테마별 일정
        # -------------------------------------------------

        theme = st.session_state.travel_theme

        if theme == "액티비티":

            activity = "만천하스카이워크 또는 지역 체험"
            evening = "지역 맛집에서 저녁 식사"

        elif theme == "역사·문화":

            activity = "지역 역사문화 명소 탐방"
            evening = "전통시장 및 지역 문화거리 산책"

        elif theme == "맛집·미식":

            activity = "지역 대표 음식 맛집 탐방"
            evening = "로컬시장 먹거리 탐방"

        elif theme == "축제·행사":

            activity = row["지역행사"]
            evening = "지역 행사 및 야간 프로그램 체험"

        elif theme == "사진 명소":

            activity = row["관광지"] + " 사진 명소 탐방"
            evening = "노을·야경 촬영"

        elif theme == "가족 여행":

            activity = "가족과 함께하는 지역 관광"
            evening = "가족 단위 로컬 식당 방문"

        elif theme == "자연·힐링":

            activity = "자연 속 산책 및 힐링"
            evening = "조용한 로컬 맛집에서 저녁 식사"

        else:

            activity = row["관광지"]
            evening = "지역 맛집 및 로컬 거리 탐방"

        # -------------------------------------------------
        # 나이대별 팁
        # -------------------------------------------------

        age = st.session_state.age_group

        if age == "10대":
            age_tip = "체험형 관광과 사진 명소를 중심으로 구성했습니다."

        elif age == "20대":
            age_tip = "사진 명소와 맛집, 체험 콘텐츠를 중심으로 구성했습니다."

        elif age == "30~40대":
            age_tip = "맛집과 자연, 문화 콘텐츠를 균형 있게 구성했습니다."

        elif age == "50대 이상":
            age_tip = "여유로운 자연 관광과 지역 먹거리를 중심으로 구성했습니다."

        else:
            age_tip = "다양한 여행자가 즐길 수 있도록 균형 있게 구성했습니다."

        # -------------------------------------------------
        # 인원별 팁
        # -------------------------------------------------

        group = st.session_state.group_size

        if group == "1인":
            group_tip = "혼자서도 부담 없이 이동할 수 있는 여유로운 코스입니다."

        elif group == "2인":
            group_tip = "2명이 함께 즐기기 좋은 맛집과 관광지를 연결했습니다."

        elif group == "3인":
            group_tip = "소규모 여행에 적합한 관광·먹거리 중심 코스입니다."

        elif group == "4인 이상":
            group_tip = "가족·친구 단위 여행을 고려한 코스입니다."

        else:
            group_tip = "다양한 인원으로 활용할 수 있는 기본 여행 코스입니다."

        st.info(
            f"📅 {selected_duration} · "
            f"👤 {age} · "
            f"👥 {group}"
        )

        st.caption(
            age_tip + " " + group_tip
        )

        # -------------------------------------------------
        # 일정 생성
        # -------------------------------------------------

        for day in range(1, days + 1):

            with st.expander(
                f"DAY {day}  ·  {row['지역']}",
                expanded=(day == 1),
            ):

                morning_col, afternoon_col = st.columns(2)

                with morning_col:

                    st.markdown(
                        "#### 🌅 오전"
                    )

                    if day == 1:

                        st.markdown(
                            f"""
                            <div class="course-item">
                                🚗 지역 도착 및 여행 시작
                            </div>

                            <div class="course-item">
                                🏞️ {row['관광지']}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    elif day == days:

                        st.markdown(
                            f"""
                            <div class="course-item">
                                🌿 {row['관광지']} 주변 산책
                            </div>

                            <div class="course-item">
                                🎁 {row['특산품']} 체험 및 쇼핑
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="course-item">
                                🏞️ {activity}
                            </div>

                            <div class="course-item">
                                🍴 {row['음식점']}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        "#### 🍚 점심"
                    )

                    st.markdown(
                        f"""
                        <div class="course-item">
                            🍴 {row['음식점']}<br>
                            대표 메뉴: {row['대표음식']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with afternoon_col:

                    st.markdown(
                        "#### 🌆 오후"

                    )

                    if day == 1:

                        st.markdown(
                            f"""
                            <div class="course-item">
                                📸 {activity}
                            </div>

                            <div class="course-item">
                                🎁 {row['특산품']} 알아보기
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    elif day == days:

                        st.markdown(
                            f"""
                            <div class="course-item">
                                🎉 {row['지역행사']}
                            </div>

                            <div class="course-item">
                                🚗 여행 마무리 및 귀가
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="course-item">
                                🎉 {row['지역행사']}
                            </div>

                            <div class="course-item">
                                {evening}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        "#### 🌙 저녁"
                    )

                    st.markdown(
                        f"""
                        <div class="course-item">
                            🍴 {row['대표음식']} 중심 로컬 저녁 식사
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# =========================================================
# 선택 지역 기본 정보
# =========================================================

if row is not None:

    st.markdown("---")

    st.markdown(
        f"### 📌 {row['지역']} 여행 정보"
    )

    info1, info2, info3, info4 = st.columns(4)

    with info1:
        st.metric(
            "로컬 추천점수",
            f"{row['추천점수']}점"
        )

    with info2:
        st.metric(
            "지역 음식 점수",
            f"{row['음식점수']}점"
        )

    with info3:
        st.metric(
            "지역 특색",
            f"{row['지역특색']}점"
        )

    with info4:
        st.metric(
            "관광 인지도",
            f"{row['관광인지도']}점"
        )


# =========================================================
# 상세 정보
# =========================================================

if row is not None:

    st.markdown(
        f"### 📋 {row['지역']} 상세 정보"
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

        st.subheader(
            "🏞️ 주요 관광지"
        )

        st.write(
            row["관광지"]
        )

        st.markdown(
            "**🧭 관광 유형**"
        )

        st.write(
            row["관광유형"]
        )

        st.markdown(
            "**📍 랜드마크 유형**"
        )

        st.write(
            row["랜드마크유형"]
        )

        st.divider()

        st.info(
            f"{row['지역']}에서 추천하는 "
            "주요 관광 콘텐츠입니다."
        )

    # -----------------------------------------------------
    # 먹거리
    # -----------------------------------------------------

    with tab2:

        st.subheader(
            "🍴 로컬 먹거리"
        )

        food_col1, food_col2 = st.columns(2)

        with food_col1:

            st.markdown(
                "**🍚 대표 음식**"
            )

            st.write(
                row["대표음식"]
            )

        with food_col2:

            st.markdown(
                "**🏪 추천 음식점**"
            )

            st.write(
                row["음식점"]
            )

        st.divider()

        st.metric(
            "지역 음식 점수",
            f"{row['음식점수']}점"
        )

        st.info(
            f"{row['지역']}의 대표 로컬 먹거리인 "
            f"{row['대표음식']}을 중심으로 "
            "맛집을 탐방해보세요."
        )

    # -----------------------------------------------------
    # 지역 행사
    # -----------------------------------------------------

    with tab3:

        st.subheader(
            "🎉 지역 행사"
        )

        st.markdown(
            f"### {row['지역행사']}"
        )

        st.write(
            f"{row['지역']}에서 경험할 수 있는 "
            "지역 특색형 행사 콘텐츠입니다."
        )

        st.divider()

        st.info(
            "방문 전 실제 행사 개최 여부와 일정, "
            "운영시간을 확인해주세요."
        )

    # -----------------------------------------------------
    # 특산품
    # -----------------------------------------------------

    with tab4:

        st.subheader(
            "🎁 지역 특산품"
        )

        st.markdown(
            f"### {row['특산품']}"
        )

        st.write(
            f"{row['지역']}의 지역 특색을 담은 "
            "대표 특산품입니다."
        )

        st.divider()

        st.info(
            "지역 여행 중 특산품을 직접 체험하거나 "
            "기념품으로 만나볼 수 있습니다."
        )


# =========================================================
# 여행지 이동
# =========================================================

if row is not None:

    st.markdown("---")

    st.markdown(
        "### 🧭 여행지 찾아가기"
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
# 하단 안내
# =========================================================

st.markdown("---")

st.caption(
    "※ 본 서비스의 지역·점수·추천 정보는 플랫폼 시연을 위한 예시 데이터입니다."
)

st.caption(
    "※ 실제 여행 전 관광지 운영시간, 행사 일정 및 교통정보를 확인해주세요."
)
