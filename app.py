import os
import html
import urllib.parse

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
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
    "selected_day": 1,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 스타일
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background: #101916;
        color: #f1f5f3;
    }

    .top-logo {
        font-size: 22px;
        font-weight: 800;
        color: #dceee3;
        margin-top: 5px;
        margin-bottom: 18px;
        text-align: left;
        letter-spacing: -0.5px;
    }

    .top-logo span {
        margin-left: 4px;
    }

    [data-testid="stSidebar"] {
        background: #17251f;
        border-right: 1px solid #30463b;
    }

    [data-testid="stSidebar"] * {
        color: #e8f0eb;
    }

    .main-title {
        padding: 28px 32px;
        border-radius: 24px;
        background: linear-gradient(135deg, #1d3d31, #284f3d);
        border: 1px solid #456b58;
        margin-bottom: 22px;
    }

    .main-title h1 {
        margin: 0;
        color: #ffffff;
        font-size: 38px;
        font-weight: 800;
    }

    .main-title p {
        margin: 10px 0 0;
        color: #c5d9cd;
        font-size: 15px;
        line-height: 1.7;
    }

    .metric-card {
        background: #1b2b24;
        border: 1px solid #355143;
        border-radius: 18px;
        padding: 18px;
        min-height: 112px;
    }

    .metric-label {
        color: #a9c0b2;
        font-size: 13px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        margin-top: 8px;
        word-break: keep-all;
    }

    .section-card {
        background: #18271f;
        border: 1px solid #334e40;
        border-radius: 20px;
        padding: 22px;
        margin: 14px 0;
    }

    .section-card h3 {
        color: #dceee3;
        margin-top: 0;
    }

    .tag {
        display: inline-block;
        background: #294c3b;
        color: #d5eddf;
        border: 1px solid #47745b;
        padding: 5px 10px;
        border-radius: 999px;
        margin: 3px;
        font-size: 12px;
    }

    .score {
        color: #8bd3a8;
        font-size: 32px;
        font-weight: 800;
    }

    .small-muted {
        color: #9eb6a7;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: #1b2b24;
        border: 1px solid #355143;
        border-radius: 16px;
        padding: 12px;
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid #527b62;
    }

    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stTextInput {
        background: #20352a;
        border-radius: 16px;
        padding: 8px 10px;
        margin-bottom: 10px;
    }

    .filter-heading {
        background: linear-gradient(135deg, #315d46, #244434);
        padding: 14px 16px;
        border-radius: 16px;
        color: #ffffff;
        font-weight: 800;
        margin: 8px 0 14px 0;
    }

    .photo-card {
        background: #1b2b24;
        border: 1px solid #355143;
        border-radius: 18px;
        overflow: hidden;
        height: 100%;
    }

    .photo-card img {
        width: 100%;
        height: 210px;
        object-fit: cover;
    }

    .photo-card-content {
        padding: 14px 16px;
    }

    .photo-card-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 800;
    }

    .photo-card-desc {
        color: #b4cbbb;
        font-size: 13px;
        margin-top: 6px;
    }

    /* =========================================================
       지도 + 코스
       ========================================================= */

    .map-course-title {
        color: #dceee3;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .course-box {
        background: #18271f;
        border: 1px solid #334e40;
        border-radius: 20px;
        padding: 20px;
        height: 100%;
    }

    .course-header {
        background: linear-gradient(135deg, #315d46, #244434);
        border-radius: 15px;
        padding: 16px;
        margin-bottom: 15px;
    }

    .course-header-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .course-header-desc {
        color: #c5d9cd;
        font-size: 13px;
    }

    /* =========================================================
       DAY 탭
       ========================================================= */

    .day-guide {
        color: #9eb6a7;
        font-size: 12px;
        margin-top: -5px;
        margin-bottom: 10px;
    }

    .schedule-card {
        background: #20352a;
        border: 1px solid #3a5949;
        border-radius: 14px;
        padding: 13px 14px;
        margin-bottom: 9px;
    }

    .schedule-time {
        color: #8bd3a8;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 3px;
    }

    .schedule-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: 800;
        line-height: 1.4;
    }

    .schedule-desc {
        color: #a9c0b2;
        font-size: 11px;
        margin-top: 4px;
        line-height: 1.45;
    }

    .course-tip {
        background: #1b2b24;
        border: 1px solid #355143;
        border-radius: 12px;
        padding: 10px 12px;
        color: #c5d9cd;
        font-size: 12px;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .nav-button {
        margin-top: 10px;
    }

    /* Streamlit 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: #20352a;
        border: 1px solid #3a5949;
        border-radius: 10px;
        padding: 7px 13px;
        color: #a9c0b2;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: #315d46 !important;
        color: #ffffff !important;
        border-color: #527b62 !important;
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
    return [
        {
            "지역": "강원특별자치도 정선군",
            "위도": 37.3806,
            "경도": 128.6608,
            "인구": 36000,
            "인구변화율": -2.1,
            "음식점수": 91,
            "관광인지도": 38,
            "지역특색": 94,
            "대표음식": "곤드레밥, 콧등치기국수",
            "음식점": "정선 곤드레 전문점",
            "관광지": "병방치 스카이워크, 아리랑시장",
            "지역행사": "정선아리랑제",
            "특산품": "곤드레, 황기",
            "관광유형": ["자연", "체험", "전통시장"],
            "랜드마크유형": ["전망대", "시장", "문화"],
            "추천기간": ["당일치기", "1박 2일", "2박 3일"],
            "여행테마": ["자연·힐링", "맛집·미식", "역사·문화", "사진 명소"],
            "나이대별_추천": {
                "10대": "시장 체험과 전망대 방문",
                "20대": "감성 사진 명소와 로컬 맛집",
                "30~40대": "자연 산책과 가족 체험",
                "50대 이상": "전통시장과 여유로운 힐링",
            },
            "인원수별_추천": {
                "1인 (혼행)": "시장과 전망대 중심",
                "2인 (커플/친구)": "사진 명소와 맛집 중심",
                "3인": "체험과 식사 중심",
                "4인 이상 (가족)": "시장·자연·체험 코스",
            },
            "소개": "산과 시장, 향토음식이 어우러진 로컬 여행지입니다.",
        },
        {
            "지역": "전라남도 구례군",
            "위도": 35.2025,
            "경도": 127.4628,
            "인구": 24000,
            "인구변화율": -1.8,
            "음식점수": 90,
            "관광인지도": 42,
            "지역특색": 96,
            "대표음식": "산채비빔밥, 재첩국",
            "음식점": "구례 산채음식점",
            "관광지": "지리산 둘레길, 화엄사",
            "지역행사": "구례 산수유꽃축제",
            "특산품": "산수유, 매실",
            "관광유형": ["자연", "문화", "트레킹"],
            "랜드마크유형": ["사찰", "둘레길", "꽃 명소"],
            "추천기간": ["당일치기", "1박 2일", "2박 3일"],
            "여행테마": ["자연·힐링", "역사·문화", "사진 명소", "축제·행사"],
            "나이대별_추천": {
                "10대": "꽃 명소와 산책",
                "20대": "감성 카페와 사진 명소",
                "30~40대": "둘레길과 가족 여행",
                "50대 이상": "사찰과 자연 힐링",
            },
            "인원수별_추천": {
                "1인 (혼행)": "둘레길과 사찰",
                "2인 (커플/친구)": "꽃 명소와 카페",
                "3인": "자연 산책과 식사",
                "4인 이상 (가족)": "사찰과 완만한 산책로",
            },
            "소개": "지리산의 자연과 산수유 마을의 정취를 느낄 수 있습니다.",
        },
        {
            "지역": "경상남도 의령군",
            "위도": 35.3222,
            "경도": 128.2617,
            "인구": 26000,
            "인구변화율": -1.2,
            "음식점수": 87,
            "관광인지도": 35,
            "지역특색": 89,
            "대표음식": "망개떡, 소고기국밥",
            "음식점": "의령 향토음식점",
            "관광지": "솥바위, 충익사",
            "지역행사": "의령 홍의장군축제",
            "특산품": "망개떡, 수박",
            "관광유형": ["역사", "문화", "먹거리"],
            "랜드마크유형": ["역사유적", "강변", "전통음식"],
            "추천기간": ["당일치기", "1박 2일"],
            "여행테마": ["맛집·미식", "역사·문화", "축제·행사"],
            "나이대별_추천": {
                "10대": "역사 체험",
                "20대": "전통 간식과 사진 명소",
                "30~40대": "가족 역사 여행",
                "50대 이상": "향토음식과 문화유적",
            },
            "인원수별_추천": {
                "1인 (혼행)": "문화유적 탐방",
                "2인 (커플/친구)": "전통음식과 강변 산책",
                "3인": "역사·먹거리 코스",
                "4인 이상 (가족)": "체험형 역사 여행",
            },
            "소개": "전통 먹거리와 역사 이야기가 살아 있는 지역입니다.",
        },
        {
            "지역": "전북특별자치도 무주군",
            "위도": 36.0071,
            "경도": 127.6608,
            "인구": 23000,
            "인구변화율": -1.9,
            "음식점수": 86,
            "관광인지도": 40,
            "지역특색": 93,
            "대표음식": "어죽, 산채정식",
            "음식점": "무주 산채정식 식당",
            "관광지": "덕유산, 반디랜드",
            "지역행사": "무주 반딧불축제",
            "특산품": "머루, 천마",
            "관광유형": ["자연", "가족", "체험"],
            "랜드마크유형": ["산", "과학관", "축제"],
            "추천기간": ["1박 2일", "2박 3일", "3박 이상"],
            "여행테마": ["자연·힐링", "액티비티", "축제·행사", "가족 여행"],
            "나이대별_추천": {
                "10대": "반디랜드 체험",
                "20대": "덕유산과 액티비티",
                "30~40대": "가족 자연 여행",
                "50대 이상": "산채음식과 힐링",
            },
            "인원수별_추천": {
                "1인 (혼행)": "산책과 자연 감상",
                "2인 (커플/친구)": "산과 사진 명소",
                "3인": "체험과 식사",
                "4인 이상 (가족)": "반디랜드와 자연 코스",
            },
            "소개": "산과 체험시설, 계절 축제를 함께 즐길 수 있습니다.",
        },
        {
            "지역": "충청북도 단양군",
            "위도": 36.9846,
            "경도": 128.3656,
            "인구": 27000,
            "인구변화율": -1.5,
            "음식점수": 88,
            "관광인지도": 48,
            "지역특색": 95,
            "대표음식": "마늘정식, 올갱이국",
            "음식점": "단양 마늘요리 전문점",
            "관광지": "만천하스카이워크, 도담삼봉",
            "지역행사": "단양 온달문화축제",
            "특산품": "단양마늘",
            "관광유형": ["자연", "액티비티", "사진"],
            "랜드마크유형": ["전망대", "강변", "역사"],
            "추천기간": ["당일치기", "1박 2일", "2박 3일"],
            "여행테마": ["액티비티", "자연·힐링", "맛집·미식", "사진 명소"],
            "나이대별_추천": {
                "10대": "전망대와 액티비티",
                "20대": "스카이워크와 사진 명소",
                "30~40대": "가족 체험과 맛집",
                "50대 이상": "강변 풍경과 마늘요리",
            },
            "인원수별_추천": {
                "1인 (혼행)": "강변과 전망대",
                "2인 (커플/친구)": "사진 명소와 액티비티",
                "3인": "관광·맛집 코스",
                "4인 이상 (가족)": "전망대와 완만한 관광 코스",
            },
            "소개": "강과 절벽 풍경, 전망대와 마늘 음식이 특징입니다.",
        },
        {
            "지역": "경상북도 영양군",
            "위도": 36.6668,
            "경도": 129.1124,
            "인구": 16000,
            "인구변화율": -2.5,
            "음식점수": 89,
            "관광인지도": 28,
            "지역특색": 92,
            "대표음식": "산나물비빔밥, 고추전",
            "음식점": "영양 산나물 식당",
            "관광지": "국립생태원, 일월산",
            "지역행사": "영양산나물축제",
            "특산품": "고추, 산나물",
            "관광유형": ["자연", "미식", "생태"],
            "랜드마크유형": ["산", "생태", "축제"],
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["자연·힐링", "맛집·미식", "축제·행사"],
            "나이대별_추천": {
                "10대": "생태 체험",
                "20대": "산나물 맛집과 자연",
                "30~40대": "생태·가족 여행",
                "50대 이상": "산나물과 산책",
            },
            "인원수별_추천": {
                "1인 (혼행)": "생태와 산책",
                "2인 (커플/친구)": "자연과 맛집",
                "3인": "생태 체험",
                "4인 이상 (가족)": "자연·먹거리 코스",
            },
            "소개": "청정 자연과 산나물 음식이 어우러진 지역입니다.",
        },
        {
            "지역": "경상북도 청송군",
            "위도": 36.4363,
            "경도": 129.0571,
            "인구": 24000,
            "인구변화율": -1.7,
            "음식점수": 88,
            "관광인지도": 34,
            "지역특색": 94,
            "대표음식": "닭백숙, 사과요리",
            "음식점": "청송 닭백숙 전문점",
            "관광지": "주왕산, 용연폭포",
            "지역행사": "청송사과축제",
            "특산품": "청송사과",
            "관광유형": ["자연", "트레킹", "미식"],
            "랜드마크유형": ["폭포", "산", "축제"],
            "추천기간": ["1박 2일", "2박 3일"],
            "여행테마": ["자연·힐링", "맛집·미식", "사진 명소", "축제·행사"],
            "나이대별_추천": {
                "10대": "폭포와 사진 명소",
                "20대": "트레킹과 사과 디저트",
                "30~40대": "자연과 가족 여행",
                "50대 이상": "산책과 향토음식",
            },
            "인원수별_추천": {
                "1인 (혼행)": "주왕산 산책",
                "2인 (커플/친구)": "폭포와 사진",
                "3인": "자연·맛집 코스",
                "4인 이상 (가족)": "완만한 산책과 체험",
            },
            "소개": "주왕산의 절경과 사과 특산품이 유명합니다.",
        },
        {
            "지역": "충청남도 태안군",
            "위도": 36.7456,
            "경도": 126.2980,
            "인구": 61000,
            "인구변화율": -0.8,
            "음식점수": 90,
            "관광인지도": 52,
            "지역특색": 91,
            "대표음식": "꽃게탕, 해산물",
            "음식점": "태안 해산물 식당",
            "관광지": "꽃지해수욕장, 신두리 해안사구",
            "지역행사": "태안 튤립축제",
            "특산품": "꽃게, 해산물",
            "관광유형": ["바다", "자연", "사진"],
            "랜드마크유형": ["해변", "사구", "꽃 명소"],
            "추천기간": ["당일치기", "1박 2일", "2박 3일"],
            "여행테마": ["자연·힐링", "맛집·미식", "사진 명소", "가족 여행"],
            "나이대별_추천": {
                "10대": "해변과 사진 명소",
                "20대": "노을과 해산물",
                "30~40대": "가족 해변 여행",
                "50대 이상": "해안 산책과 미식",
            },
            "인원수별_추천": {
                "1인 (혼행)": "해변 산책",
                "2인 (커플/친구)": "노을과 해산물",
                "3인": "해변·맛집 코스",
                "4인 이상 (가족)": "해변과 체험",
            },
            "소개": "해변, 노을, 해산물을 함께 즐길 수 있는 서해안 지역입니다.",
        },
        {
            "지역": "전라남도 고흥군",
            "위도": 34.6112,
            "경도": 127.2851,
            "인구": 62000,
            "인구변화율": -1.6,
            "음식점수": 89,
            "관광인지도": 31,
            "지역특색": 93,
            "대표음식": "장어구이, 유자음식",
            "음식점": "고흥 장어구이 식당",
            "관광지": "나로우주센터, 우주발사전망대",
            "지역행사": "고흥 유자축제",
            "특산품": "유자, 김",
            "관광유형": ["과학", "바다", "미식"],
            "랜드마크유형": ["전망대", "우주", "해안"],
            "추천기간": ["1박 2일", "2박 3일", "3박 이상"],
            "여행테마": ["액티비티", "맛집·미식", "사진 명소", "가족 여행"],
            "나이대별_추천": {
                "10대": "우주 체험",
                "20대": "해안 사진 명소",
                "30~40대": "우주·가족 여행",
                "50대 이상": "해산물과 해안 풍경",
            },
            "인원수별_추천": {
                "1인 (혼행)": "전망대와 해안",
                "2인 (커플/친구)": "해안 드라이브",
                "3인": "우주 체험과 식사",
                "4인 이상 (가족)": "우주센터와 가족 코스",
            },
            "소개": "우주과학과 해안 풍경, 유자 먹거리가 공존합니다.",
        },
        {
            "지역": "경상북도 울릉군",
            "위도": 37.4845,
            "경도": 130.9057,
            "인구": 9000,
            "인구변화율": -2.8,
            "음식점수": 92,
            "관광인지도": 45,
            "지역특색": 98,
            "대표음식": "홍합밥, 오징어",
            "음식점": "울릉도 해산물 식당",
            "관광지": "독도전망대, 성인봉",
            "지역행사": "울릉도 오징어축제",
            "특산품": "오징어, 명이나물",
            "관광유형": ["섬", "자연", "트레킹"],
            "랜드마크유형": ["전망대", "산", "항구"],
            "추천기간": ["2박 3일", "3박 이상"],
            "여행테마": ["자연·힐링", "액티비티", "맛집·미식", "사진 명소"],
            "나이대별_추천": {
                "10대": "전망대와 섬 체험",
                "20대": "트레킹과 사진",
                "30~40대": "섬 자연 여행",
                "50대 이상": "해산물과 여유로운 관광",
            },
            "인원수별_추천": {
                "1인 (혼행)": "전망대와 항구",
                "2인 (커플/친구)": "해안 풍경",
                "3인": "트레킹과 미식",
                "4인 이상 (가족)": "섬 관광과 체험",
            },
            "소개": "독특한 섬 지형과 해산물, 해안 풍경이 특징입니다.",
        },
    ]


# =========================================================
# 지역 이미지
# =========================================================
IMAGE_DATA = {
    "강원특별자치도 정선군": {
        "여행지": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1200",
    },
    "전라남도 구례군": {
        "여행지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1200",
    },
    "경상남도 의령군": {
        "여행지": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1200",
    },
    "전북특별자치도 무주군": {
        "여행지": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200",
    },
    "충청북도 단양군": {
        "여행지": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1200",
    },
    "경상북도 영양군": {
        "여행지": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1200",
    },
    "경상북도 청송군": {
        "여행지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1200",
    },
    "충청남도 태안군": {
        "여행지": "https://images.unsplash.com/photo-1507524275556-7e4f7b3f0f7f?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200",
    },
    "전라남도 고흥군": {
        "여행지": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1547592180-85f173990554?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1200",
    },
    "경상북도 울릉군": {
        "여행지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200",
        "먹거리": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200",
        "구경거리": "https://images.unsplash.com/photo-1507524275556-7e4f7b3f0f7f?w=1200",
    },
}


# =========================================================
# 이미지 카드
# =========================================================
def render_image_card(title, image_url, description):
    safe_title = html.escape(str(title))
    safe_desc = html.escape(str(description))
    safe_url = html.escape(str(image_url))

    st.markdown(
        f"""
        <div class="photo-card">
            <img src="{safe_url}"
                 alt="{safe_title}"
                 onerror="this.style.display='none';">
            <div class="photo-card-content">
                <div class="photo-card-title">{safe_title}</div>
                <div class="photo-card-desc">{safe_desc}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 점수 계산
# =========================================================
def calculate_hidden_score(row):
    hidden_score = 100 - row["관광인지도"]
    population_score = min(abs(row["인구변화율"]) * 5, 20)

    return round(
        hidden_score * 0.4
        + population_score * 0.1
        + row["음식점수"] * 0.25
        + row["지역특색"] * 0.25,
        1,
    )


def make_tags(items):
    return " ".join(
        f'<span class="tag">{html.escape(str(item))}</span>'
        for item in items
    )


# =========================================================
# 데이터 생성
# =========================================================
df = pd.DataFrame(load_data())
df["숨은지역점수"] = df.apply(calculate_hidden_score, axis=1)


# =========================================================
# 사이드바
# =========================================================
with st.sidebar:

    st.markdown(
        '<div class="filter-heading">🧭 나만의 로컬 여행 찾기</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # 로컬 행사 광고
    # =====================================================

    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">

            <style>

                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    font-family:
                        Arial,
                        "Noto Sans KR",
                        sans-serif;
                }

                .ad-container {
                    width: 100%;
                    height: 190px;
                    position: relative;
                    overflow: hidden;
                    border-radius: 16px;
                }

                .ad-slide {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    left: 0;
                    top: 0;

                    opacity: 0;

                    transition:
                        opacity 0.6s ease,
                        transform 0.6s ease;

                    transform: translateX(20px);
                }

                .ad-slide.active {
                    opacity: 1;
                    transform: translateX(0);
                }

                .ad-card {
                    width: 100%;
                    height: 100%;

                    padding: 17px;

                    border-radius: 16px;

                    background:
                        linear-gradient(
                            135deg,
                            #315d46,
                            #1d3328
                        );

                    border: 1px solid #426851;

                    display: flex;
                    flex-direction: column;
                    justify-content: center;

                    box-shadow:
                        0 6px 18px rgba(0,0,0,0.18);
                }

                .ad-badge {
                    display: inline-block;

                    width: fit-content;

                    padding: 4px 8px;

                    margin-bottom: 7px;

                    border-radius: 20px;

                    background:
                        rgba(255,255,255,0.12);

                    color: #b9dfc8;

                    font-size: 10px;
                    font-weight: 700;
                }

                .ad-title {
                    color: #ffffff;

                    font-size: 16px;
                    font-weight: 800;

                    line-height: 1.3;

                    margin-bottom: 5px;
                }

                .ad-region {
                    color: #b9dfc8;

                    font-size: 11px;
                    font-weight: 700;

                    margin-bottom: 5px;
                }

                .ad-date {
                    color: #ffffff;

                    font-size: 11px;
                    font-weight: 700;

                    margin-bottom: 6px;
                }

                .ad-description {
                    color: #c4d4cb;

                    font-size: 10px;

                    line-height: 1.45;
                }

                .ad-dots {
                    position: absolute;

                    left: 0;
                    right: 0;
                    bottom: 8px;

                    text-align: center;

                    z-index: 20;
                }

                .dot {
                    display: inline-block;

                    width: 5px;
                    height: 5px;

                    margin: 0 3px;

                    border-radius: 50%;

                    background: #789786;
                }

                .dot.active {
                    width: 16px;

                    border-radius: 10px;

                    background: #dceee3;
                }

            </style>
        </head>

        <body>

            <div class="ad-container">

                <div class="ad-slide active">

                    <div class="ad-card">

                        <div class="ad-badge">
                            지금 떠나기 좋은 행사
                        </div>

                        <div class="ad-title">
                            정선 아리랑제
                        </div>

                        <div class="ad-region">
                            강원특별자치도 정선군
                        </div>

                        <div class="ad-date">
                            2026.09.26 ~ 2026.09.30
                        </div>

                        <div class="ad-description">
                            정선의 전통문화와 아리랑을 만나보세요.
                        </div>

                    </div>

                </div>


                <div class="ad-slide">

                    <div class="ad-card">

                        <div class="ad-badge">
                            가을 로컬 여행
                        </div>

                        <div class="ad-title">
                            단양 로컬 풍경전
                        </div>

                        <div class="ad-region">
                            충청북도 단양군
                        </div>

                        <div class="ad-date">
                            2026.09.25 ~ 2026.10.05
                        </div>

                        <div class="ad-description">
                            단양의 숨은 풍경과 가을 여행지를 만나보세요.
                        </div>

                    </div>

                </div>


                <div class="ad-slide">

                    <div class="ad-card">

                        <div class="ad-badge">
                            로컬 미식 여행
                        </div>

                        <div class="ad-title">
                            구례 가을 로컬마켓
                        </div>

                        <div class="ad-region">
                            전라남도 구례군
                        </div>

                        <div class="ad-date">
                            2026.09.27 ~ 2026.10.04
                        </div>

                        <div class="ad-description">
                            구례의 특산품과 지역 먹거리를 만나보세요.
                        </div>

                    </div>

                </div>


                <div class="ad-slide">

                    <div class="ad-card">

                        <div class="ad-badge">
                            가을 여행 추천
                        </div>

                        <div class="ad-title">
                            청송 가을 산책길
                        </div>

                        <div class="ad-region">
                            경상북도 청송군
                        </div>

                        <div class="ad-date">
                            2026.09.26 ~ 2026.10.11
                        </div>

                        <div class="ad-description">
                            청송의 자연과 가을 풍경을 천천히 즐겨보세요.
                        </div>

                    </div>

                </div>


                <div class="ad-dots">

                    <span class="dot active"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>

                </div>

            </div>


            <script>

                const slides =
                    document.querySelectorAll(".ad-slide");

                const dots =
                    document.querySelectorAll(".dot");

                let currentIndex = 0;


                function showNextSlide() {

                    slides[currentIndex]
                        .classList.remove("active");

                    dots[currentIndex]
                        .classList.remove("active");


                    currentIndex =
                        (currentIndex + 1)
                        % slides.length;


                    slides[currentIndex]
                        .classList.add("active");

                    dots[currentIndex]
                        .classList.add("active");
                }


                setInterval(
                    showNextSlide,
                    3000
                );

            </script>

        </body>
        </html>
        """,
        height=195,
        scrolling=False,
    )


    st.caption(
        "여행 취향을 선택하면 추천 지역과 코스가 달라집니다."
    )


    # =====================================================
    # 필터
    # =====================================================

    st.selectbox(
        "선호 나이대",
        [
            "전체",
            "10대",
            "20대",
            "30~40대",
            "50대 이상"
        ],
        key="age_group",
    )

    st.selectbox(
        "여행 인원",
        [
            "전체",
            "1인 (혼행)",
            "2인 (커플/친구)",
            "3인",
            "4인 이상 (가족)"
        ],
        key="group_size",
    )

    st.selectbox(
        "여행 기간",
        [
            "전체",
            "당일치기",
            "1박 2일",
            "2박 3일",
            "3박 이상"
        ],
        key="travel_duration",
    )

    st.selectbox(
        "여행 테마",
        [
            "전체",
            "자연·힐링",
            "액티비티",
            "역사·문화",
            "맛집·미식",
            "축제·행사",
            "사진 명소",
            "가족 여행"
        ],
        key="travel_theme",
    )

    st.selectbox(
        "선호 음식",
        [
            "전체",
            "한식",
            "해산물",
            "산채음식",
            "향토음식",
            "간식·디저트"
        ],
        key="food_type",
    )

    st.selectbox(
        "정렬 기준",
        [
            "점수순",
            "인구 적은 순",
            "음식 점수순",
            "지역 특색순"
        ],
        key="sort_type",
    )

    st.text_input(
        "지역·음식·관광지 검색",
        key="keyword"
    )

    st.markdown("### 지도 표시 항목")

    show_regions = st.checkbox(
        "추천 지역",
        True
    )

    show_food = st.checkbox(
        "음식점",
        True
    )

    show_tour = st.checkbox(
        "관광지",
        True
    )

    show_events = st.checkbox(
        "지역 행사",
        True
    )

    show_specialties = st.checkbox(
        "특산품",
        True
    )

    if st.button(
        "🔄 필터 초기화",
        use_container_width=True
    ):

        for key, value in defaults.items():
            st.session_state[key] = value

        st.rerun()


# =========================================================
# 필터 적용
# =========================================================
filtered_df = df.copy()


# =========================================================
# 키워드 검색
# =========================================================
if st.session_state.keyword.strip():

    keyword = st.session_state.keyword.strip().lower()

    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: keyword in " ".join(
                [
                    str(row["지역"]),
                    str(row["대표음식"]),
                    str(row["음식점"]),
                    str(row["관광지"]),
                    str(row["지역행사"]),
                    str(row["특산품"]),
                    str(row["소개"]),
                ]
            ).lower(),
            axis=1,
        )
    ]


# =========================================================
# 음식 필터
# =========================================================
if st.session_state.food_type != "전체":

    food_keywords = {
        "한식": [
            "밥",
            "국",
            "정식",
            "비빔",
            "떡",
            "백숙"
        ],
        "해산물": [
            "해산물",
            "오징어",
            "꽃게",
            "장어",
            "홍합",
            "재첩",
        ],
        "산채음식": [
            "산채",
            "곤드레",
            "산나물",
        ],
        "향토음식": [
            "향토",
            "마늘",
            "고추",
            "사과",
        ],
        "간식·디저트": [
            "떡",
            "유자",
            "사과",
        ],
    }

    keys = food_keywords[st.session_state.food_type]

    filtered_df = filtered_df[
        filtered_df["대표음식"].apply(
            lambda x: any(
                k in str(x)
                for k in keys
            )
        )
    ]


# =========================================================
# 여행 기간 필터
# =========================================================
if st.session_state.travel_duration != "전체":

    filtered_df = filtered_df[
        filtered_df["추천기간"].apply(
            lambda x: st.session_state.travel_duration in x
        )
    ]


# =========================================================
# 여행 테마 필터
# =========================================================
if st.session_state.travel_theme != "전체":

    filtered_df = filtered_df[
        filtered_df["여행테마"].apply(
            lambda x: st.session_state.travel_theme in x
        )
    ]


# =========================================================
# 정렬
# =========================================================
if st.session_state.sort_type == "점수순":

    filtered_df = filtered_df.sort_values(
        "숨은지역점수",
        ascending=False,
    )

elif st.session_state.sort_type == "인구 적은 순":

    filtered_df = filtered_df.sort_values(
        "인구",
        ascending=True,
    )

elif st.session_state.sort_type == "음식 점수순":

    filtered_df = filtered_df.sort_values(
        "음식점수",
        ascending=False,
    )

else:

    filtered_df = filtered_df.sort_values(
        "지역특색",
        ascending=False,
    )


# =========================================================
# 상단 로고
# =========================================================
st.markdown(
    """
    <div class="top-logo">
        🚗 <span>로컬 쉼표</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 상단 선택 정보
# =========================================================
m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">여행 인원</div>
            <div class="metric-value">
                {html.escape(st.session_state.group_size)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">선호 나이대</div>
            <div class="metric-value">
                {html.escape(st.session_state.age_group)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">선택 여행 기간</div>
            <div class="metric-value">
                {html.escape(st.session_state.travel_duration)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">선택 여행 테마</div>
            <div class="metric-value">
                {html.escape(st.session_state.travel_theme)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 필터 결과가 없을 경우
# =========================================================
if filtered_df.empty:

    st.warning(
        "현재 조건에 맞는 지역이 없습니다. "
        "필터를 조금 완화해 보세요."
    )

    st.stop()


# =========================================================
# 지역 선택
# =========================================================
region_names = filtered_df["지역"].tolist()

if st.session_state.selected_region not in region_names:

    st.session_state.selected_region = region_names[0]


selected_region = st.selectbox(
    "🔎 상세 정보를 볼 지역",
    region_names,
    index=region_names.index(
        st.session_state.selected_region
    ),
    key="region_selector",
)

st.session_state.selected_region = selected_region

row = filtered_df[
    filtered_df["지역"] == selected_region
].iloc[0]


# =========================================================
# 맞춤 코스 데이터 계산
# =========================================================
duration_days = {
    "당일치기": 1,
    "1박 2일": 2,
    "2박 3일": 3,
    "3박 이상": 4,
}

selected_duration = st.session_state.travel_duration

if selected_duration == "전체":
    selected_duration = row["추천기간"][0]

days = duration_days.get(
    selected_duration,
    1,
)

theme = st.session_state.travel_theme
group = st.session_state.group_size
age = st.session_state.age_group


# =========================================================
# DAY 선택값 보정
# =========================================================
if st.session_state.selected_day > days:
    st.session_state.selected_day = 1


# =========================================================
# 코스 내용
# =========================================================
if theme == "액티비티":

    first_activity = "대표 관광지에서 체험·전망 활동"
    second_activity = "주변 산책 또는 자연 체험"

elif theme == "역사·문화":

    first_activity = "지역 문화·역사 명소 탐방"
    second_activity = "전통시장 또는 지역 문화 공간 방문"

elif theme == "맛집·미식":

    first_activity = (
        f"{row['음식점']}에서 대표 음식 즐기기"
    )
    second_activity = (
        f"{row['대표음식']} 관련 로컬 먹거리 탐방"
    )

elif theme == "축제·행사":

    first_activity = (
        f"{row['지역행사']} 관련 장소 방문"
    )
    second_activity = "지역 행사장 주변 산책 및 체험"

elif theme == "사진 명소":

    first_activity = (
        f"{row['관광지']}에서 사진 촬영"
    )
    second_activity = "노을·전망·자연 풍경 감상"

elif theme == "가족 여행":

    first_activity = "가족 단위로 이동하기 좋은 관광지 방문"
    second_activity = "무리 없는 산책과 지역 먹거리 체험"

else:

    first_activity = f"{row['관광지']} 방문"
    second_activity = "주변 자연 경관과 로컬 공간 탐방"


# =========================================================
# 인원별 팁
# =========================================================
if group == "1인 (혼행)":

    group_tip = "혼자 이동하기 편하도록 주요 명소 중심"

elif group == "2인 (커플/친구)":

    group_tip = "사진 명소와 여유로운 식사 중심"

elif group == "3인":

    group_tip = "관광·식사·휴식의 균형 중심"

elif group == "4인 이상 (가족)":

    group_tip = "이동 부담을 줄이고 가족 체험 중심"

else:

    group_tip = "다양한 여행객이 이용할 수 있는 기본 코스"


# =========================================================
# 나이대별 팁
# =========================================================
if age == "10대":

    age_tip = "체험·사진·활동 중심"

elif age == "20대":

    age_tip = "감성 명소·맛집·활동 중심"

elif age == "30~40대":

    age_tip = "관광·식사·휴식이 균형 잡힌 구성"

elif age == "50대 이상":

    age_tip = "무리 없는 이동과 자연·문화 중심"

else:

    age_tip = "일반적인 관광·식사·휴식 중심"


# =========================================================
# 하루 일정 생성
# =========================================================
daily_plan = []

for day in range(1, days + 1):

    if day == 1:

        daily_plan.append(
            {
                "day": day,
                "morning_time": "09:30",
                "morning_title": first_activity,
                "morning_desc": "여행지의 대표적인 로컬 명소부터 가볍게 시작",

                "lunch_time": "12:30",
                "lunch_title": f"{row['음식점']} / {row['대표음식']}",
                "lunch_desc": "지역 대표 먹거리로 점심 식사",

                "afternoon_time": "14:00",
                "afternoon_title": second_activity,
                "afternoon_desc": "지역의 자연·문화·볼거리 탐방",

                "evening_time": "17:30",
                "evening_title": f"{row['지역']} 로컬 거리 또는 시장 산책",
                "evening_desc": "여유롭게 주변을 둘러보며 하루 마무리",
            }
        )

    elif day == days:

        daily_plan.append(
            {
                "day": day,
                "morning_time": "09:30",
                "morning_title": f"{row['특산품']} 알아보기 및 기념품 구입",
                "morning_desc": "지역 특산품을 둘러보며 마지막 여행 준비",

                "lunch_time": "12:00",
                "lunch_title": f"{row['대표음식']} 중심의 지역 식사",
                "lunch_desc": "여행 마지막 로컬 음식 즐기기",

                "afternoon_time": "14:00",
                "afternoon_title": f"{row['관광지']} 중 남은 장소 탐방",
                "afternoon_desc": "시간에 맞춰 원하는 장소를 선택해 방문",

                "evening_time": "16:30",
                "evening_title": "여행 정리 및 귀가",
                "evening_desc": "여행 기록을 남기고 귀가",
            }
        )

    else:

        daily_plan.append(
            {
                "day": day,
                "morning_time": "09:30",
                "morning_title": f"{row['관광지']} 주변 산책 및 자유 일정",
                "morning_desc": "관광지 주변을 여유롭게 둘러보기",

                "lunch_time": "12:30",
                "lunch_title": f"{row['음식점']} 또는 인근 로컬 식당",
                "lunch_desc": "지역 음식으로 든든하게 식사",

                "afternoon_time": "14:00",
                "afternoon_title": f"{row['지역행사']} 또는 지역 특색 체험",
                "afternoon_desc": "지역만의 분위기를 경험하는 시간",

                "evening_time": "17:30",
                "evening_title": f"{row['특산품']} 쇼핑 및 휴식",
                "evening_desc": "지역 특산품을 둘러보고 휴식",
            }
        )


# =========================================================
# 지도 + 맞춤 여행 코스
# =========================================================
st.markdown(
    '<div class="map-course-title">🗺️ 숨은 지역 지도 &nbsp; + &nbsp; 🧭 맞춤 여행 코스</div>',
    unsafe_allow_html=True,
)

map_col, course_col = st.columns(
    [1, 1],
    gap="medium",
)


# =========================================================
# 지도
# =========================================================

with map_col:

    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🗺️ 숨은 지역 지도</div>
            <div class="section-desc">
                대한민국 곳곳의 숨은 지역과 여행 정보를 한눈에 확인해보세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 대한민국 전체 영역
    korea_bounds = [
        [33.0, 124.5],   # 남서쪽
        [38.7, 132.0],   # 북동쪽
    ]

    # 대한민국 중심
    m = folium.Map(
        location=[36.3, 127.8],
        zoom_start=7,
        min_zoom=6,
        max_zoom=11,
        min_lat=32.5,
        max_lat=39.5,
        min_lon=124.0,
        max_lon=132.5,
        max_bounds=True,
        control_scale=True,
        tiles="OpenStreetMap",
    )

    # 대한민국 전체가 처음부터 보이도록 설정
    m.fit_bounds(
        korea_bounds,
        padding=(10, 10)
    )

    # -----------------------------------------------------
    # 지도 타일
    # -----------------------------------------------------

    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        name="OpenStreetMap",
        attr="© OpenStreetMap contributors",
        control=True,
    ).add_to(m)

    # -----------------------------------------------------
    # 추천 지역
    # -----------------------------------------------------

    if show_recommended:
        for _, r in filtered_df.iterrows():

            popup_html = f"""
            <div style="
                width:220px;
                font-family:Arial, sans-serif;
                padding:5px;
            ">
                <h4 style="margin-bottom:8px;">
                    📍 {html.escape(str(r['지역']))}
                </h4>

                <p style="margin:4px 0;">
                    ⭐ 추천점수 : <b>{r['추천점수']}</b>
                </p>

                <p style="margin:4px 0;">
                    🍴 대표음식 : {html.escape(str(r['대표음식']))}
                </p>

                <p style="margin:4px 0;">
                    🏞️ 관광지 : {html.escape(str(r['관광지']))}
                </p>
            </div>
            """

            folium.Marker(
                location=[r["위도"], r["경도"]],
                popup=folium.Popup(
                    popup_html,
                    max_width=300
                ),
                tooltip=f"📍 {r['지역']}",
                icon=folium.Icon(
                    color="green",
                    icon="map-marker",
                    prefix="fa",
                ),
            ).add_to(m)

    # -----------------------------------------------------
    # 음식점
    # -----------------------------------------------------

    if show_food:

        for _, r in filtered_df.iterrows():

            folium.Marker(
                location=[
                    r["위도"] + 0.015,
                    r["경도"] + 0.015
                ],
                tooltip=f"🍴 {r['음식점']}",
                popup=f"""
                <b>🍴 로컬 음식점</b><br>
                {html.escape(str(r['음식점']))}<br>
                대표음식 : {html.escape(str(r['대표음식']))}
                """,
                icon=folium.Icon(
                    color="orange",
                    icon="cutlery",
                    prefix="fa",
                ),
            ).add_to(m)

    # -----------------------------------------------------
    # 관광지
    # -----------------------------------------------------

    if show_tour:

        for _, r in filtered_df.iterrows():

            folium.Marker(
                location=[
                    r["위도"] - 0.015,
                    r["경도"] - 0.015
                ],
                tooltip=f"🏞️ {r['관광지']}",
                popup=f"""
                <b>🏞️ 관광지</b><br>
                {html.escape(str(r['관광지']))}
                """,
                icon=folium.Icon(
                    color="blue",
                    icon="camera",
                    prefix="fa",
                ),
            ).add_to(m)

    # -----------------------------------------------------
    # 지역 행사
    # -----------------------------------------------------

    if show_event:

        for _, r in filtered_df.iterrows():

            folium.Marker(
                location=[
                    r["위도"] + 0.025,
                    r["경도"] - 0.015
                ],
                tooltip=f"🎉 {r['지역행사']}",
                popup=f"""
                <b>🎉 지역 행사</b><br>
                {html.escape(str(r['지역행사']))}
                """,
                icon=folium.Icon(
                    color="red",
                    icon="calendar",
                    prefix="fa",
                ),
            ).add_to(m)

    # -----------------------------------------------------
    # 특산품
    # -----------------------------------------------------

    if show_specialty:

        for _, r in filtered_df.iterrows():

            folium.Marker(
                location=[
                    r["위도"] - 0.025,
                    r["경도"] + 0.015
                ],
                tooltip=f"🛍️ {r['특산품']}",
                popup=f"""
                <b>🛍️ 지역 특산품</b><br>
                {html.escape(str(r['특산품']))}
                """,
                icon=folium.Icon(
                    color="purple",
                    icon="shopping-bag",
                    prefix="fa",
                ),
            ).add_to(m)

    # -----------------------------------------------------
    # 지도 표시
    # -----------------------------------------------------

    st_folium(
        m,
        width=None,
        height=900,
        returned_objects=[],
        use_container_width=True,
    )

# =========================================================
# 오른쪽 : 맞춤 여행 코스
# =========================================================
with course_col:

    st.subheader("🧭 맞춤 여행 코스 만들기")

    st.caption(
        f"{row['지역']} · 선택한 여행 조건을 기준으로 구성된 추천 코스"
    )

    tag1, tag2 = st.columns(2)

    with tag1:

        st.markdown(
            f"👤 **여행 인원**  \n{group}"
        )

    with tag2:

        st.markdown(
            f"🎂 **선호 나이대**  \n{age}"
        )

    tag3, tag4 = st.columns(2)

    with tag3:

        st.markdown(
            f"📅 **여행 기간**  \n{selected_duration}"
        )

    with tag4:

        st.markdown(
            f"🎯 **여행 테마**  \n{theme}"
        )

    st.divider()

    # =====================================================
    # 맞춤 포인트
    # =====================================================

    st.markdown("**👥 여행자 맞춤 포인트**")

    st.markdown(
        f"""
        <div class="course-tip">
            🎂 <b>나이대</b> · {html.escape(age_tip)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="course-tip">
            👥 <b>여행 인원</b> · {html.escape(group_tip)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📅 추천 일정")

    st.markdown(
        '<div class="day-guide">DAY를 선택하면 해당 날짜의 일정만 표시됩니다.</div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # DAY 탭 생성
    # =====================================================

    day_labels = [
        f"DAY {i}"
        for i in range(1, days + 1)
    ]

    day_tabs = st.tabs(day_labels)

    for index, day_tab in enumerate(day_tabs):

        with day_tab:

            plan = daily_plan[index]

            st.markdown(
                f"""
                <div class="schedule-card">
                    <div class="schedule-time">
                        🌅 {plan['morning_time']} · 오전
                    </div>
                    <div class="schedule-title">
                        {html.escape(plan['morning_title'])}
                    </div>
                    <div class="schedule-desc">
                        {html.escape(plan['morning_desc'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="schedule-card">
                    <div class="schedule-time">
                        🍴 {plan['lunch_time']} · 점심
                    </div>
                    <div class="schedule-title">
                        {html.escape(plan['lunch_title'])}
                    </div>
                    <div class="schedule-desc">
                        {html.escape(plan['lunch_desc'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="schedule-card">
                    <div class="schedule-time">
                        🏞️ {plan['afternoon_time']} · 오후
                    </div>
                    <div class="schedule-title">
                        {html.escape(plan['afternoon_title'])}
                    </div>
                    <div class="schedule-desc">
                        {html.escape(plan['afternoon_desc'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="schedule-card">
                    <div class="schedule-time">
                        🌙 {plan['evening_time']} · 저녁
                    </div>
                    <div class="schedule-title">
                        {html.escape(plan['evening_title'])}
                    </div>
                    <div class="schedule-desc">
                        {html.escape(plan['evening_desc'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "※ 예시 데이터 기반 추천 코스입니다. "
        "실제 이동시간·영업시간·날씨·행사 일정은 방문 전에 확인하세요."
    )


# =========================================================
# 길찾기
# =========================================================
query = urllib.parse.quote(
    f"{row['지역']} {row['관광지']}"
)

st.markdown("### 🚗 길찾기")

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
# 추천 지역
# =========================================================
st.subheader("📍 추천 지역")

st.caption(
    "현재 맞춤 여행 코스로 선택한 지역입니다."
)

with st.container(border=True):

    st.markdown(
        f"## 📍 {row['지역']}"
    )

    st.markdown("---")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown(
            f"""
            **🍚 대표 음식**  
            {row['대표음식']}

            **🎁 지역 특산품**  
            {row['특산품']}

            **🎉 지역 행사**  
            {row['지역행사']}
            """
        )

    with info_col2:

        st.markdown(
            f"""
            **📸 주요 관광지**  
            {row['관광지']}

            **🌿 관광 유형**  
            {row['관광유형']}

            **📅 추천 기간**  
            {row['추천기간']}
            """
        )

    st.markdown("---")

    st.markdown("### 💡 지역 소개")

    st.write(
        row["소개"]
    )

    st.markdown("### 🧭 맞춤 여행 조건")

    condition_col1, condition_col2, condition_col3, condition_col4 = st.columns(4)

    with condition_col1:

        st.info(
            f"👤 **여행 인원**\n\n{group}"
        )

    with condition_col2:

        st.info(
            f"🎂 **선호 나이대**\n\n{age}"
        )

    with condition_col3:

        st.info(
            f"📅 **여행 기간**\n\n{selected_duration}"
        )

    with condition_col4:

        st.info(
            f"🎯 **여행 테마**\n\n{theme}"
        )


# =========================================================
# 맞춤 추천
# =========================================================
st.markdown("### 🎯 맞춤 추천")

recommendation_parts = []


if st.session_state.age_group != "전체":

    age_key = st.session_state.age_group

    recommendation_parts.append(
        f"**나이대 추천:** "
        f"{row['나이대별_추천'].get(
            age_key,
            '체험·관광 중심의 기본 추천'
        )}"
    )


if st.session_state.group_size != "전체":

    group_key = st.session_state.group_size

    group_text = row["인원수별_추천"].get(
        group_key,
        "기본 추천 코스",
    )

    recommendation_parts.append(
        f"**인원별 추천:** {group_text}"
    )


if st.session_state.travel_duration != "전체":

    recommendation_parts.append(
        f"**여행 기간:** "
        f"{st.session_state.travel_duration}에 적합한 지역"
    )


if st.session_state.travel_theme != "전체":

    recommendation_parts.append(
        f"**여행 테마:** "
        f"{st.session_state.travel_theme} 중심 추천"
    )


if recommendation_parts:

    for item in recommendation_parts:

        st.markdown(
            f"- {item}"
        )

else:

    st.info(
        "사이드바에서 나이대, 인원, 기간, 테마를 선택하면 "
        "맞춤 추천이 표시됩니다."
    )


# =========================================================
# 지역 사진
# =========================================================
st.markdown("## 📸 지역 사진 미리보기")

region_images = IMAGE_DATA.get(
    row["지역"],
    {},
)

photo1, photo2, photo3 = st.columns(3)


with photo1:

    render_image_card(
        "🏞️ 여행지",
        region_images.get("여행지", ""),
        row["관광지"],
    )


with photo2:

    render_image_card(
        "👀 구경거리",
        region_images.get("구경거리", ""),
        row["지역행사"],
    )


with photo3:

    render_image_card(
        "🍴 먹거리",
        region_images.get("먹거리", ""),
        f"{row['대표음식']} · {row['음식점']}",
    )


# =========================================================
# 상세 탭
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🍴 음식",
        "🏞️ 관광지",
        "🎉 지역 행사",
        "🎁 특산품",
        "💬 로컬 리뷰",
    ]
)


with tab1:

    st.markdown("### 대표 음식")

    st.write(
        row["대표음식"]
    )

    st.markdown(
        f"**추천 음식점:** {row['음식점']}"
    )

    st.caption(
        "방문 전 영업시간과 실제 운영 여부를 확인하세요."
    )


with tab2:

    st.markdown("### 추천 관광지")

    st.write(
        row["관광지"]
    )

    st.markdown("**관광 유형**")

    st.markdown(
        make_tags(row["관광유형"]),
        unsafe_allow_html=True,
    )

    st.markdown("**랜드마크 유형**")

    st.markdown(
        make_tags(row["랜드마크유형"]),
        unsafe_allow_html=True,
    )


with tab3:

    st.markdown("### 지역 행사")

    st.write(
        row["지역행사"]
    )

    st.caption(
        "축제 일정은 개최 기관의 공식 공지를 확인하세요."
    )


with tab4:

    st.markdown("### 지역 특산품")

    st.write(
        row["특산품"]
    )


with tab5:

    st.markdown("### 로컬 리뷰 예시")

    reviews = [
        f"{row['지역']}의 자연 풍경이 인상적이었어요.",
        f"{row['대표음식']}을 먹어 보니 지역 특색이 잘 느껴졌습니다.",
        "유명 관광지보다 여유롭게 여행하기 좋았습니다.",
    ]

    for review in reviews:

        st.markdown(
            f"- 💬 {review}"
        )


# =========================================================
# 하단 안내
# =========================================================
st.markdown("---")

st.caption(
    "※ 본 서비스는 SGIS 기반 지역 탐색을 보여주기 위한 "
    "예시 데이터 기반 프로토타입입니다."
)
