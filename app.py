import os
import html
import urllib.parse

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium


# =========================================================
# 페이지 설정
# =========================================================
st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        font-size: 27px;
        font-weight: 800;
        margin-top: 8px;
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

    [data-testid="stSidebar"] .stSlider, [data-testid="stSidebar"] .stSelectbox,
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
        height: 185px;
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
            "나이대별_추천": {"10대": "시장 체험과 전망대 방문", "20대": "감성 사진 명소와 로컬 맛집", "30~40대": "자연 산책과 가족 체험", "50대 이상": "전통시장과 여유로운 힐링"},
            "인원수별_추천": {"1인 (혼행)": "시장과 전망대 중심", "2인 (커플/친구)": "사진 명소와 맛집 중심", "3인": "체험과 식사 중심", "4인 이상 (가족)": "시장·자연·체험 코스"},
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
            "나이대별_추천": {"10대": "꽃 명소와 산책", "20대": "감성 카페와 사진 명소", "30~40대": "둘레길과 가족 여행", "50대 이상": "사찰과 자연 힐링"},
            "인원수별_추천": {"1인 (혼행)": "둘레길과 사찰", "2인 (커플/친구)": "꽃 명소와 카페", "3인": "자연 산책과 식사", "4인 이상 (가족)": "사찰과 완만한 산책로"},
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
            "나이대별_추천": {"10대": "역사 체험", "20대": "전통 간식과 사진 명소", "30~40대": "가족 역사 여행", "50대 이상": "향토음식과 문화유적"},
            "인원수별_추천": {"1인 (혼행)": "문화유적 탐방", "2인 (커플/친구)": "전통음식과 강변 산책", "3인": "역사·먹거리 코스", "4인 이상 (가족)": "체험형 역사 여행"},
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
            "나이대별_추천": {"10대": "반디랜드 체험", "20대": "덕유산과 액티비티", "30~40대": "가족 자연 여행", "50대 이상": "산채음식과 힐링"},
            "인원수별_추천": {"1인 (혼행)": "산책과 자연 감상", "2인 (커플/친구)": "산과 사진 명소", "3인": "체험과 식사", "4인 이상 (가족)": "반디랜드와 자연 코스"},
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
            "나이대별_추천": {"10대": "전망대와 액티비티", "20대": "스카이워크와 사진 명소", "30~40대": "가족 체험과 맛집", "50대 이상": "강변 풍경과 마늘요리"},
            "인원수별_추천": {"1인 (혼행)": "강변과 전망대", "2인 (커플/친구)": "사진 명소와 액티비티", "3인": "관광·맛집 코스", "4인 이상 (가족)": "전망대와 완만한 관광 코스"},
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
            "나이대별_추천": {"10대": "생태 체험", "20대": "산나물 맛집과 자연", "30~40대": "생태·가족 여행", "50대 이상": "산나물과 산책"},
            "인원수별_추천": {"1인 (혼행)": "생태와 산책", "2인 (커플/친구)": "자연과 맛집", "3인": "생태 체험", "4인 이상 (가족)": "자연·먹거리 코스"},
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
            "나이대별_추천": {"10대": "폭포와 사진 명소", "20대": "트레킹과 사과 디저트", "30~40대": "자연과 가족 여행", "50대 이상": "산책과 향토음식"},
            "인원수별_추천": {"1인 (혼행)": "주왕산 산책", "2인 (커플/친구)": "폭포와 사진", "3인": "자연·맛집 코스", "4인 이상 (가족)": "완만한 산책과 체험"},
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
            "나이대별_추천": {"10대": "해변과 사진 명소", "20대": "노을과 해산물", "30~40대": "가족 해변 여행", "50대 이상": "해안 산책과 미식"},
            "인원수별_추천": {"1인 (혼행)": "해변 산책", "2인 (커플/친구)": "노을과 해산물", "3인": "해변·맛집 코스", "4인 이상 (가족)": "해변과 체험"},
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
            "나이대별_추천": {"10대": "우주 체험", "20대": "해안 사진 명소", "30~40대": "우주·가족 여행", "50대 이상": "해산물과 해안 풍경"},
            "인원수별_추천": {"1인 (혼행)": "전망대와 해안", "2인 (커플/친구)": "해안 드라이브", "3인": "우주 체험과 식사", "4인 이상 (가족)": "우주센터와 가족 코스"},
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
            "나이대별_추천": {"10대": "전망대와 섬 체험", "20대": "트레킹과 사진", "30~40대": "섬 자연 여행", "50대 이상": "해산물과 여유로운 관광"},
            "인원수별_추천": {"1인 (혼행)": "전망대와 항구", "2인 (커플/친구)": "해안 풍경", "3인": "트레킹과 미식", "4인 이상 (가족)": "섬 관광과 체험"},
            "소개": "독특한 섬 지형과 해산물, 해안 풍경이 특징입니다.",
        },
    ]


# =========================================================
# 이미지 URL 생성
# =========================================================
def photo_url(query):
    # Unsplash Source 기반 검색형 이미지 URL
    encoded = urllib.parse.quote(query)
    return f"https://source.unsplash.com/900x600/?{encoded}"


def photo_card(title, image_query, description):
    url = photo_url(image_query)
    st.markdown(
        f"""
        <div class="photo-card">
            <img src="{url}" alt="{html.escape(title)}">
            <div class="photo-card-content">
                <div class="photo-card-title">{html.escape(title)}</div>
                <div class="photo-card-desc">{html.escape(description)}</div>
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
    return " ".join(f'<span class="tag">{html.escape(str(item))}</span>' for item in items)


df = pd.DataFrame(load_data())
df["숨은지역점수"] = df.apply(calculate_hidden_score, axis=1)

# 지역별 사진 URL
# 실제 서비스에서는 저작권을 확인한 뒤 공식 관광 사이트 또는 직접 보유한 사진을 사용하는 것을 권장합니다.
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
        "먹거리": "https://images.unsplash.com/photo-154 seafood?w=1200".replace(" seafood", ""),
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

def render_image_card(title, image_url, description):
    st.markdown(
        f"""
        <div style="background:#1b2b24;border:1px solid #355143;border-radius:18px;
                    overflow:hidden;height:100%;margin-bottom:12px;">
            <img src="{image_url}" style="width:100%;height:210px;object-fit:cover;"
                 onerror="this.style.display='none';">
            <div style="padding:15px;">
                <h4 style="margin:0 0 8px;color:#ffffff;">{title}</h4>
                <p style="margin:0;color:#b8cdbf;font-size:14px;">{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 세션 상태 / 초기화
# =========================================================
defaults = {
    "age_group": "전체",
    "group_size": "전체",
    "travel_duration": "전체",
    "travel_theme": "전체",
    "min_score": 60,
    "food_type": "전체",
    "sort_type": "점수순",
    "keyword": "",
    "selected_region": "정선군",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 사이드바
# =========================================================
with st.sidebar:
    st.markdown('<div class="filter-heading">🧭 나만의 로컬 여행 찾기</div>', unsafe_allow_html=True)
    st.caption("여행 취향을 선택하면 추천 지역과 코스가 달라집니다.")

    st.slider(
        "최소 추천 점수",
        min_value=0,
        max_value=100,
        value=st.session_state.min_score,
        key="min_score",
    )

    st.selectbox(
        "선호 나이대",
        ["전체", "10대", "20대", "30~40대", "50대 이상"],
        key="age_group",
    )

    st.selectbox(
        "여행 인원",
        ["전체", "1인 (혼행)", "2인 (커플/친구)", "3인", "4인 이상 (가족)"],
        key="group_size",
    )

    st.selectbox(
        "여행 기간",
        ["전체", "당일치기", "1박 2일", "2박 3일", "3박 이상"],
        key="travel_duration",
    )

    st.selectbox(
        "여행 테마",
        ["전체", "자연·힐링", "액티비티", "역사·문화", "맛집·미식", "축제·행사", "사진 명소", "가족 여행"],
        key="travel_theme",
    )

    st.selectbox(
        "선호 음식",
        ["전체", "한식", "해산물", "산채음식", "향토음식", "간식·디저트"],
        key="food_type",
    )

    st.selectbox(
        "정렬 기준",
        ["점수순", "인구 적은 순", "음식 점수순", "지역 특색순"],
        key="sort_type",
    )

    st.text_input("지역·음식·관광지 검색", key="keyword")

    st.markdown("### 지도 표시 항목")
    show_regions = st.checkbox("추천 지역", True)
    show_food = st.checkbox("음식점", True)
    show_tour = st.checkbox("관광지", True)
    show_events = st.checkbox("지역 행사", True)
    show_specialties = st.checkbox("특산품", True)

    if st.button("🔄 필터 초기화", use_container_width=True):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.rerun()


# =========================================================
# 필터 적용
# =========================================================
filtered_df = df[df["숨은지역점수"] >= st.session_state.min_score].copy()

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

if st.session_state.food_type != "전체":
    food_keywords = {
        "한식": ["밥", "국", "정식", "비빔", "떡", "백숙"],
        "해산물": ["해산물", "오징어", "꽃게", "장어", "홍합", "재첩"],
        "산채음식": ["산채", "곤드레", "산나물"],
        "향토음식": ["향토", "마늘", "고추", "사과"],
        "간식·디저트": ["떡", "유자", "사과"],
    }
    keys = food_keywords[st.session_state.food_type]
    filtered_df = filtered_df[
        filtered_df["대표음식"].apply(lambda x: any(k in str(x) for k in keys))
    ]

if st.session_state.travel_duration != "전체":
    filtered_df = filtered_df[
        filtered_df["추천기간"].apply(lambda x: st.session_state.travel_duration in x)
    ]

if st.session_state.travel_theme != "전체":
    filtered_df = filtered_df[
        filtered_df["여행테마"].apply(lambda x: st.session_state.travel_theme in x)
    ]

if st.session_state.sort_type == "점수순":
    filtered_df = filtered_df.sort_values("숨은지역점수", ascending=False)
elif st.session_state.sort_type == "인구 적은 순":
    filtered_df = filtered_df.sort_values("인구", ascending=True)
elif st.session_state.sort_type == "음식 점수순":
    filtered_df = filtered_df.sort_values("음식점수", ascending=False)
else:
    filtered_df = filtered_df.sort_values("지역특색", ascending=False)


# =========================================================
# 상단 제목
# =========================================================
st.markdown(
    """
    <div class="main-title">
        <h1>🚗우리끼리 맵</h1>
        <p>지도로 찾는 숨은 보물! SGIS 기반 맞춤형 여행 코스 추천</p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">검색 지역 수</div><div class="metric-value">{len(filtered_df)}곳</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    avg_score = round(filtered_df["숨은지역점수"].mean(), 1) if len(filtered_df) else 0
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">평균 추천 점수</div><div class="metric-value">{avg_score}점</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">선택 여행 기간</div><div class="metric-value">{html.escape(st.session_state.travel_duration)}</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">선택 여행 테마</div><div class="metric-value">{html.escape(st.session_state.travel_theme)}</div></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# 지도
# =========================================================
st.markdown("## 🗺️ 숨은 지역 지도")

map_center = [36.2, 127.8]
m = folium.Map(
    location=map_center,
    zoom_start=7,
    tiles=None,
    control_scale=True,
)

folium.TileLayer(
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    name="일반 지도",
    attr="© OpenStreetMap",
).add_to(m)

folium.TileLayer(
    tiles="https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png",
    name="VWorld 일반",
    attr="VWorld",
    overlay=False,
).add_to(m)

for _, row in filtered_df.iterrows():
    popup_html = f"""
    <div style="width:240px">
        <h4>{html.escape(row['지역'])}</h4>
        <b>추천 점수: {row['숨은지역점수']}점</b><br>
        대표 음식: {html.escape(row['대표음식'])}<br>
        관광지: {html.escape(row['관광지'])}
    </div>
    """
    if show_regions:
        folium.Marker(
            [row["위도"], row["경도"]],
            tooltip=f"{row['지역']} · {row['숨은지역점수']}점",
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="green", icon="map-marker"),
        ).add_to(m)

    if show_food:
        folium.Marker(
            [row["위도"] + 0.018, row["경도"] + 0.012],
            tooltip=f"🍴 {row['음식점']}",
            popup=row["음식점"],
            icon=folium.Icon(color="orange", icon="cutlery"),
        ).add_to(m)

    if show_tour:
        folium.Marker(
            [row["위도"] - 0.018, row["경도"] - 0.012],
            tooltip=f"🏞️ {row['관광지']}",
            popup=row["관광지"],
            icon=folium.Icon(color="blue", icon="camera"),
        ).add_to(m)

    if show_events:
        folium.Marker(
            [row["위도"] + 0.012, row["경도"] - 0.018],
            tooltip=f"🎉 {row['지역행사']}",
            popup=row["지역행사"],
            icon=folium.Icon(color="purple", icon="star"),
        ).add_to(m)

    if show_specialties:
        folium.Marker(
            [row["위도"] - 0.012, row["경도"] + 0.018],
            tooltip=f"🎁 {row['특산품']}",
            popup=row["특산품"],
            icon=folium.Icon(color="red", icon="shopping-basket"),
        ).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, use_container_width=True, height=520, returned_objects=[])


# =========================================================
# 지역 선택
# =========================================================
st.markdown("## 🔎 추천 지역")

if filtered_df.empty:
    st.warning("현재 조건에 맞는 지역이 없습니다. 필터를 조금 완화해 보세요.")
    st.stop()

region_names = filtered_df["지역"].tolist()
if st.session_state.selected_region not in region_names:
    st.session_state.selected_region = region_names[0]

selected_region = st.selectbox(
    "상세 정보를 볼 지역",
    region_names,
    index=region_names.index(st.session_state.selected_region),
    key="region_selector",
)
st.session_state.selected_region = selected_region

row = filtered_df[filtered_df["지역"] == selected_region].iloc[0]


# =========================================================
# 여행지·구경거리·먹거리 사진
# =========================================================
st.markdown("## 📸 이 지역의 볼거리와 먹거리")

photo1, photo2, photo3 = st.columns(3)

with photo1:
    photo_card(
        "추천 여행지",
        f"{row['지역']} 자연 관광지 한국 여행",
        row["관광지"],
    )

with photo2:
    photo_card(
        "구경거리",
        f"{row['지역']} 지역 행사 전통 문화 풍경",
        row["지역행사"],
    )

with photo3:
    photo_card(
        "로컬 먹거리",
        f"{row['대표음식']} 한국 음식",
        f"{row['대표음식']} · {row['음식점']}",
    )


# =========================================================
# 상세 정보
# =========================================================
st.markdown(
    f"""
    <div class="section-card">
        <div class="small-muted">선택한 지역</div>
        <h2>{html.escape(row['지역'])}</h2>
        <div class="score">{row['숨은지역점수']}점</div>
        <p>{html.escape(row['소개'])}</p>
        {make_tags(row['여행테마'])}
        {make_tags(row['추천기간'])}
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("음식 점수", f"{row['음식점수']}점")
c2.metric("지역 특색", f"{row['지역특색']}점")
c3.metric("관광 인지도", f"{row['관광인지도']}점")
c4.metric("인구", f"{row['인구']:,}명")

st.markdown("### 🎯 맞춤 추천")

recommendation_parts = []
if st.session_state.age_group != "전체":
    age = st.session_state.age_group
    if age == "10대":
        age = "10대"
    recommendation_parts.append(
        f"**나이대 추천:** {row['나이대별_추천'].get(age, '체험·관광 중심의 기본 추천')}"
    )

if st.session_state.group_size != "전체":
    group = st.session_state.group_size
    if group == "3인":
        group_text = row["인원수별_추천"].get("3인", "3인 맞춤 체험과 식사 코스")
    else:
        group_text = row["인원수별_추천"].get(group, "기본 추천 코스")
    recommendation_parts.append(f"**인원별 추천:** {group_text}")

if st.session_state.travel_duration != "전체":
    recommendation_parts.append(
        f"**여행 기간:** {st.session_state.travel_duration}에 적합한 지역"
    )

if st.session_state.travel_theme != "전체":
    recommendation_parts.append(
        f"**여행 테마:** {st.session_state.travel_theme} 중심 추천"
    )

if recommendation_parts:
    for item in recommendation_parts:
        st.markdown(f"- {item}")
else:
    st.info("사이드바에서 나이대, 인원, 기간, 테마를 선택하면 맞춤 추천이 표시됩니다.")



# =========================================================
# 여행지·구경거리·먹거리 사진
# =========================================================
st.markdown("## 📸 지역 사진 미리보기")
region_images = IMAGE_DATA.get(row["지역"], {})

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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🍴 음식", "🏞️ 관광지", "🎉 지역 행사", "🎁 특산품", "💬 로컬 리뷰"]
)

with tab1:
    st.markdown(f"### 대표 음식")
    st.write(row["대표음식"])
    st.markdown(f"**추천 음식점:** {row['음식점']}")
    st.caption("방문 전 영업시간과 실제 운영 여부를 확인하세요.")

with tab2:
    st.markdown("### 추천 관광지")
    st.write(row["관광지"])
    st.markdown("**관광 유형**")
    st.markdown(make_tags(row["관광유형"]), unsafe_allow_html=True)
    st.markdown("**랜드마크 유형**")
    st.markdown(make_tags(row["랜드마크유형"]), unsafe_allow_html=True)

with tab3:
    st.markdown("### 지역 행사")
    st.write(row["지역행사"])
    st.caption("축제 일정은 개최 기관의 공식 공지를 확인하세요.")

with tab4:
    st.markdown("### 지역 특산품")
    st.write(row["특산품"])

with tab5:
    st.markdown("### 로컬 리뷰 예시")
    reviews = [
        f"{row['지역']}의 자연 풍경이 인상적이었어요.",
        f"{row['대표음식']}을 먹어 보니 지역 특색이 잘 느껴졌습니다.",
        "유명 관광지보다 여유롭게 여행하기 좋았습니다.",
    ]
    for review in reviews:
        st.markdown(f"- 💬 {review}")


# =========================================================
# 맞춤 여행 코스 생성기
# =========================================================
st.markdown("---")
st.markdown("## 🧭 맞춤 여행 코스 만들기")
st.write("선택한 지역과 여행 조건을 바탕으로 추천 여행 코스를 자동으로 구성합니다.")

duration_days = {
    "당일치기": 1,
    "1박 2일": 2,
    "2박 3일": 3,
    "3박 이상": 4,
}

selected_duration = st.session_state.travel_duration
if selected_duration == "전체":
    selected_duration = row["추천기간"][0]

days = duration_days.get(selected_duration, 1)

# 선택 조건에 맞는 코스 구성 요소
theme = st.session_state.travel_theme
group = st.session_state.group_size
age = st.session_state.age_group

course_title = f"{row['지역']} {selected_duration} 추천 코스"

if theme == "액티비티":
    first_activity = "대표 관광지에서 체험·전망 활동"
    second_activity = "주변 산책 또는 자연 체험"
elif theme == "역사·문화":
    first_activity = "지역 문화·역사 명소 탐방"
    second_activity = "전통시장 또는 지역 문화 공간 방문"
elif theme == "맛집·미식":
    first_activity = f"{row['음식점']}에서 대표 음식 즐기기"
    second_activity = f"{row['대표음식']} 관련 로컬 먹거리 탐방"
elif theme == "축제·행사":
    first_activity = f"{row['지역행사']} 관련 장소 방문"
    second_activity = "지역 행사장 주변 산책 및 체험"
elif theme == "사진 명소":
    first_activity = f"{row['관광지']}에서 사진 촬영"
    second_activity = "노을·전망·자연 풍경 감상"
elif theme == "가족 여행":
    first_activity = "가족 단위로 이동하기 좋은 관광지 방문"
    second_activity = "무리 없는 산책과 지역 먹거리 체험"
else:
    first_activity = f"{row['관광지']} 방문"
    second_activity = "주변 자연 경관과 로컬 공간 탐방"

if group == "1인 (혼행)":
    group_tip = "혼자 이동하기 편하도록 주요 명소 중심으로 구성"
elif group == "2인 (커플/친구)":
    group_tip = "사진 명소와 여유로운 식사 시간을 포함"
elif group == "3인":
    group_tip = "관광·식사·휴식의 균형을 고려"
elif group == "4인 이상 (가족)":
    group_tip = "이동 부담을 줄이고 가족 체험 중심으로 구성"
else:
    group_tip = "다양한 여행객이 이용할 수 있는 기본 코스"

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

st.markdown(
    f"""
    <div class="section-card">
        <h3>📌 {html.escape(course_title)}</h3>
        <p><b>여행 인원 조건:</b> {html.escape(group)}</p>
        <p><b>여행자 특성:</b> {html.escape(age_tip)}</p>
        <p><b>코스 구성:</b> {html.escape(group_tip)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 하루 단위 기본 일정
daily_plan = []
for day in range(1, days + 1):
    if day == 1:
        daily_plan.append({
            "day": day,
            "morning": f"09:30 · {first_activity}",
            "lunch": f"12:30 · {row['음식점']} / {row['대표음식']}",
            "afternoon": f"14:00 · {second_activity}",
            "evening": f"17:30 · {row['지역']} 로컬 거리 또는 시장 산책",
        })
    elif day == days:
        daily_plan.append({
            "day": day,
            "morning": f"09:30 · {row['특산품']} 알아보기 및 기념품 구입",
            "lunch": f"12:00 · {row['대표음식']} 중심의 지역 식사",
            "afternoon": f"14:00 · {row['관광지']} 중 방문하지 못한 장소 탐방",
            "evening": "16:30 · 여행 정리 및 귀가",
        })
    else:
        daily_plan.append({
            "day": day,
            "morning": f"09:30 · {row['관광지']} 주변 산책 및 자유 일정",
            "lunch": f"12:30 · {row['음식점']} 또는 인근 로컬 식당",
            "afternoon": f"14:00 · {row['지역행사']} 또는 지역 특색 체험",
            "evening": f"17:30 · {row['특산품']} 쇼핑 및 휴식",
        })

for plan in daily_plan:
    with st.expander(f"📅 {plan['day']}일 차 일정", expanded=(plan["day"] == 1)):
        st.markdown(f"- **오전:** {plan['morning']}")
        st.markdown(f"- **점심:** {plan['lunch']}")
        st.markdown(f"- **오후:** {plan['afternoon']}")
        st.markdown(f"- **저녁:** {plan['evening']}")

st.info(
    "위 코스는 플랫폼의 예시 데이터로 생성된 추천 일정입니다. "
    "실제 이동시간, 영업시간, 기상 상황과 행사 개최 여부를 방문 전에 확인하세요."
)

# =========================================================
# 길찾기 링크
# =========================================================
query = urllib.parse.quote(f"{row['지역']} {row['관광지']}")
st.markdown("### 🚗 길찾기")
st.link_button(
    "네이버 지도에서 길찾기",
    f"https://map.naver.com/p/search/{query}",
)
st.link_button(
    "카카오맵에서 검색",
    f"https://map.kakao.com/?q={query}",
)

st.caption("※ 본 서비스는 지역 탐색을 위한 예시 데이터 기반 프로토타입입니다.")
