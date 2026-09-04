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
    page_title="숨은 로컬 발견 - Dark Mode",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# HTML 렌더링 helper
# =========================================================

def render_html(content, sidebar=False):
    """HTML 앞쪽의 들여쓰기를 자동 제거하여 렌더링"""
    dedented_content = textwrap.dedent(content)
    if sidebar:
        st.sidebar.markdown(dedented_content, unsafe_allow_html=True)
    else:
        st.markdown(dedented_content, unsafe_allow_html=True)


# =========================================================
# 다크 모드 CSS (Dark Mode Custom Styling)
# =========================================================

render_html("""
<style>

/* 전체 배경 및 기본 폰트 색상 */
html,
body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: #0e1117 !important;
    color: #e0e6ed !important;
}

[data-testid="stHeader"] {
    background-color: #0e1117 !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 30px !important;
    padding-bottom: 50px !important;
}

/* 사이드바 다크 스타일 */
section[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d !important;
}

section[data-testid="stSidebar"] > div {
    background-color: #161b22 !important;
}

/* 메인 타이틀 카드 */
.main-title-card {
    background: #161b22;
    padding: 32px 38px;
    border-radius: 22px;
    border: 1px solid #30363d;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.4);
    margin-bottom: 25px;
}

.main-title-small {
    font-size: 15px;
    color: #58a6ff;
    font-weight: 700;
    margin-bottom: 8px;
}

.main-title {
    font-size: 42px;
    font-weight: 850;
    color: #f0f6fc;
    letter-spacing: -2px;
    margin-bottom: 8px;
}

.main-subtitle {
    font-size: 16px;
    color: #8b949e;
}

/* 섹션 제목 */
.section-title {
    color: #f0f6fc;
    font-size: 24px;
    font-weight: 850;
    margin-top: 30px;
    margin-bottom: 16px;
}

/* 통계 카드 */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.3);
    min-height: 120px;
}

.metric-title {
    color: #8b949e;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}

.metric-value {
    color: #58a6ff;
    font-size: 30px;
    font-weight: 850;
}

.metric-sub {
    color: #6e7681;
    font-size: 12px;
    margin-top: 5px;
}

/* 지역 카드 */
.region-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.3);
}

.region-name {
    color: #f0f6fc;
    font-size: 25px;
    font-weight: 850;
}

.region-score {
    color: #3fb950;
    font-size: 32px;
    font-weight: 850;
}

.small-label {
    color: #8b949e;
    font-size: 13px;
    font-weight: 700;
}

/* 점수 바 */
.score-bar {
    height: 9px;
    background: #21262d;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 7px;
    margin-bottom: 10px;
}

.score-fill {
    height: 100%;
    background: #238636;
    border-radius: 10px;
}

/* 카드 상세 박스 (다크 테마) */
.food-box {
    background: #1c2128;
    border: 1px solid #343b45;
    border-radius: 16px;
    padding: 20px;
    color: #adbac7;
}

.tour-box {
    background: #1c2128;
    border: 1px solid #343b45;
    border-radius: 16px;
    padding: 20px;
    color: #adbac7;
}

.special-box {
    background: #1c2128;
    border: 1px solid #343b45;
    border-radius: 16px;
    padding: 20px;
    color: #adbac7;
}

/* 리뷰 */
.review-box {
    background: #161b22;
    border-left: 4px solid #238636;
    border-radius: 10px;
    padding: 15px 18px;
    margin-bottom: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    color: #adbac7;
}

/* 지도 iframe 코너 라운딩 */
iframe {
    border-radius: 16px !important;
}

</style>
""")


# =========================================================
# 로컬 이미지 / 온라인 폴백 이미지 설정
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


def show_local_or_web_image(filename, fallback_url, caption=None):
    """로컬 assets 디렉토리에 파일이 없으면 고화질 온라인 대체 이미지를 사용"""
    path = os.path.join(ASSET_DIR, filename)

    if os.path.isfile(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.image(fallback_url, caption=f"{caption} (웹 이미지 예시)", use_container_width=True)


# =========================================================
# 지역 데이터 (온라인 대체 이미지 URL 포함)
# =========================================================

region_data = [
    {
        "지역": "강원도 정선군",
        "위도": 37.3806,
        "경도": 128.6608,
        "인구": 35000,
        "인구변화율": -2.8,
        "음식점수": 90,
        "관광인지도": 46,
        "지역특색": 90,
        "대표음식": "곤드레밥",
        "음식설명": "정선의 대표 산나물인 곤드레를 이용한 향토 음식입니다.",
        "음식점": "정선 곤드레마을",
        "음식점설명": "정선 지역의 곤드레밥과 다양한 산채요리를 맛볼 수 있는 로컬 식당입니다.",
        "관광지": "민둥산",
        "관광지설명": "가을 억새 풍경으로 유명한 정선의 대표적인 산악 관광지입니다.",
        "지역행사": "정선 5일장",
        "행사설명": "정선 지역의 전통시장 문화와 로컬 먹거리를 경험할 수 있습니다.",
        "특산품": "곤드레",
        "특산품설명": "정선을 대표하는 산나물로 다양한 향토 음식에 활용됩니다.",
        "음식사진": "jeongseon_food.jpg",
        "관광사진": "jeongseon_tour.jpg",
        "특산품사진": "jeongseon_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "곤드레밥이 생각보다 훨씬 맛있었습니다.",
            "관광객이 너무 많지 않아서 여유롭게 여행하기 좋았습니다.",
            "정선 5일장과 같이 방문하면 볼거리가 많습니다."
        ]
    },
    {
        "지역": "충청북도 단양군",
        "위도": 36.9845,
        "경도": 128.3657,
        "인구": 28000,
        "인구변화율": -1.7,
        "음식점수": 85,
        "관광인지도": 52,
        "지역특색": 88,
        "대표음식": "마늘떡갈비",
        "음식설명": "단양의 대표 특산물인 마늘을 활용한 지역 음식입니다.",
        "음식점": "단양 마늘골목",
        "음식점설명": "단양 마늘을 활용한 다양한 향토음식을 맛볼 수 있는 지역 먹거리 공간입니다.",
        "관광지": "도담삼봉",
        "관광지설명": "남한강 위에 솟아 있는 세 개의 봉우리로 단양의 대표 관광지입니다.",
        "지역행사": "단양 마늘축제",
        "행사설명": "단양 마늘을 중심으로 지역 음식과 농특산물을 체험할 수 있는 행사입니다.",
        "특산품": "단양마늘",
        "특산품설명": "단양 지역의 대표적인 농특산물로 향이 강하고 품질이 좋은 것으로 알려져 있습니다.",
        "음식사진": "danyang_food.jpg",
        "관광사진": "danyang_tour.jpg",
        "특산품사진": "danyang_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "마늘을 좋아한다면 음식 때문에라도 방문할 만합니다.",
            "도담삼봉 주변 풍경이 정말 좋았습니다.",
            "조용하게 하루 여행하기 좋은 곳입니다."
        ]
    },
    {
        "지역": "전라남도 구례군",
        "위도": 35.2025,
        "경도": 127.4628,
        "인구": 25000,
        "인구변화율": -2.2,
        "음식점수": 88,
        "관광인지도": 41,
        "지역특색": 94,
        "대표음식": "산채비빔밥",
        "음식설명": "지리산 주변에서 생산되는 다양한 산나물을 활용한 구례의 향토 음식입니다.",
        "음식점": "구례 산채마을",
        "음식점설명": "지리산 산나물을 활용한 다양한 향토음식을 맛볼 수 있는 로컬 음식점입니다.",
        "관광지": "지리산 노고단",
        "관광지설명": "지리산의 대표적인 능선 관광지로 아름다운 산악 풍경을 자랑합니다.",
        "지역행사": "구례 산수유축제",
        "행사설명": "봄철 산수유꽃과 지역 문화를 함께 즐길 수 있는 대표 지역축제입니다.",
        "특산품": "산수유",
        "특산품설명": "구례를 대표하는 특산물로 산수유 관련 제품이 다양하게 생산됩니다.",
        "음식사진": "gurye_food.jpg",
        "관광사진": "gurye_tour.jpg",
        "특산품사진": "gurye_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "산채비빔밥이 담백하고 건강한 느낌이었습니다.",
            "산수유 시즌에 방문하면 정말 예쁠 것 같습니다.",
            "사람이 많지 않아 자연을 즐기기 좋았습니다."
        ]
    },
    {
        "지역": "경상북도 영덕군",
        "위도": 36.4150,
        "경도": 129.3650,
        "인구": 34000,
        "인구변화율": -2.0,
        "음식점수": 91,
        "관광인지도": 48,
        "지역특색": 87,
        "대표음식": "대게",
        "음식설명": "영덕을 대표하는 해산물로 지역의 대표적인 먹거리입니다.",
        "음식점": "영덕 대게거리",
        "음식점설명": "영덕 대게를 중심으로 다양한 해산물 요리를 맛볼 수 있는 음식거리입니다.",
        "관광지": "해맞이공원",
        "관광지설명": "동해의 아름다운 일출을 감상할 수 있는 대표적인 해안 관광지입니다.",
        "지역행사": "영덕 대게축제",
        "행사설명": "영덕대게와 지역 수산문화를 경험할 수 있는 대표적인 지역축제입니다.",
        "특산품": "영덕대게",
        "특산품설명": "영덕을 대표하는 수산물로 지역 경제와 관광을 함께 이끌고 있습니다.",
        "음식사진": "yeongdeok_food.jpg",
        "관광사진": "yeongdeok_tour.jpg",
        "특산품사진": "yeongdeok_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1559737679-d65e94b59f77?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "대게가 정말 신선했습니다.",
            "바다를 보면서 식사할 수 있어서 좋았습니다.",
            "해안도로 드라이브 코스로도 추천합니다."
        ]
    },
    {
        "지역": "전라북도 무주군",
        "위도": 36.0072,
        "경도": 127.6607,
        "인구": 24000,
        "인구변화율": -2.5,
        "음식점수": 82,
        "관광인지도": 39,
        "지역특색": 92,
        "대표음식": "어죽",
        "음식설명": "민물고기를 활용해 끓여낸 무주의 대표적인 향토 음식입니다.",
        "음식점": "무주 어죽마을",
        "음식점설명": "무주 지역 전통 방식의 어죽과 향토음식을 맛볼 수 있습니다.",
        "관광지": "덕유산",
        "관광지설명": "사계절 아름다운 풍경을 가지고 있는 대표적인 산악 관광지입니다.",
        "지역행사": "무주 반딧불축제",
        "행사설명": "반딧불이를 주제로 자연환경과 지역문화를 체험할 수 있는 축제입니다.",
        "특산품": "머루",
        "특산품설명": "무주의 청정 자연환경에서 생산되는 대표적인 농특산물입니다.",
        "음식사진": "muju_food.jpg",
        "관광사진": "muju_tour.jpg",
        "특산품사진": "muju_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "어죽이 생각보다 담백하고 맛있었습니다.",
            "덕유산 풍경이 정말 아름다웠습니다.",
            "자연 속에서 쉬고 싶을 때 좋은 지역입니다."
        ]
    },
    {
        "지역": "충청남도 서천군",
        "위도": 36.0803,
        "경도": 126.6917,
        "인구": 47000,
        "인구변화율": -1.3,
        "음식점수": 84,
        "관광인지도": 44,
        "지역특색": 86,
        "대표음식": "서천김",
        "음식설명": "서천의 바다 환경에서 생산되는 대표적인 지역 먹거리입니다.",
        "음식점": "서천 바다밥상",
        "음식점설명": "서천에서 생산되는 해산물을 활용한 지역 음식점입니다.",
        "관광지": "국립생태원",
        "관광지설명": "다양한 생태환경과 동식물을 체험할 수 있는 대표 관광시설입니다.",
        "지역행사": "서천 한산모시축제",
        "행사설명": "한산모시와 지역 전통문화를 체험할 수 있는 대표 지역축제입니다.",
        "특산품": "한산모시",
        "특산품설명": "서천 한산 지역을 대표하는 전통 섬유 특산품입니다.",
        "음식사진": "seocheon_food.jpg",
        "관광사진": "seocheon_tour.jpg",
        "특산품사진": "seocheon_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1606851094655-b2593a9af63f?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1528458909336-e7a0adfac1d5?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "바다 음식이 신선해서 좋았습니다.",
            "국립생태원이 생각보다 볼거리가 많았습니다.",
            "가족 단위 여행지로 괜찮은 것 같습니다."
        ]
    },
    {
        "지역": "경상남도 의령군",
        "위도": 35.3222,
        "경도": 128.2617,
        "인구": 26000,
        "인구변화율": -2.7,
        "음식점수": 86,
        "관광인지도": 36,
        "지역특색": 91,
        "대표음식": "의령소바",
        "음식설명": "의령을 대표하는 향토 음식으로 담백한 육수와 메밀면이 특징입니다.",
        "음식점": "의령 소바거리",
        "음식점설명": "의령의 전통 소바를 맛볼 수 있는 지역 음식점들이 모여 있는 공간입니다.",
        "관광지": "자굴산",
        "관광지설명": "의령의 자연경관을 감상할 수 있는 대표적인 산악 관광지입니다.",
        "지역행사": "의령 홍의장군축제",
        "행사설명": "의령의 역사와 지역문화를 체험할 수 있는 대표적인 지역행사입니다.",
        "특산품": "망개떡",
        "특산품설명": "망개잎으로 감싸 만든 의령의 대표적인 전통 떡입니다.",
        "음식사진": "uiryeong_food.jpg",
        "관광사진": "uiryeong_tour.jpg",
        "특산품사진": "uiryeong_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "의령소바가 깔끔하고 맛있었습니다.",
            "관광객이 많지 않아 한적하게 여행할 수 있었습니다.",
            "지역 음식 때문에 다시 방문하고 싶습니다."
        ]
    },
    {
        "지역": "강원도 삼척시",
        "위도": 37.4499,
        "경도": 129.1658,
        "인구": 62000,
        "인구변화율": -1.9,
        "음식점수": 89,
        "관광인지도": 50,
        "지역특색": 89,
        "대표음식": "곰치국",
        "음식설명": "동해안에서 잡히는 곰치를 이용한 삼척의 대표적인 향토 음식입니다.",
        "음식점": "삼척 바다밥상",
        "음식점설명": "삼척의 다양한 해산물과 지역 음식을 맛볼 수 있는 로컬 음식점입니다.",
        "관광지": "장호항",
        "관광지설명": "맑은 바다와 아름다운 해안 풍경으로 유명한 삼척의 대표 관광지입니다.",
        "지역행사": "삼척 장미축제",
        "행사설명": "지역의 아름다운 장미와 다양한 문화행사를 함께 즐길 수 있는 축제입니다.",
        "특산품": "삼척 장뇌삼",
        "특산품설명": "삼척의 청정 자연환경에서 재배되는 지역 특산 농산물입니다.",
        "음식사진": "samcheok_food.jpg",
        "관광사진": "samcheok_tour.jpg",
        "특산품사진": "samcheok_specialty.jpg",
        "음식_web": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=800&q=80",
        "관광_web": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "특산품_web": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80",
        "리뷰": [
            "곰치국이 시원하고 해장하기 좋았습니다.",
            "장호항 바다가 정말 예뻤습니다.",
            "유명 관광지보다 조용한 곳을 찾는다면 추천합니다."
        ]
    }
]


# =========================================================
# DataFrame & 점수 계산
# =========================================================

df = pd.DataFrame(region_data)

def calculate_hidden_score(row):
    score = (
        (100 - row["관광인지도"]) * 0.35
        + row["음식점수"] * 0.30
        + row["지역특색"] * 0.35
    )
    return round(score, 1)

df["숨은지역점수"] = df.apply(calculate_hidden_score, axis=1)


# =========================================================
# 메인 제목 (다크)
# =========================================================

render_html("""
<div class="main-title-card">
    <div class="main-title-small">📍 LOCAL DISCOVERY</div>
    <div class="main-title">숨은 로컬 발견</div>
    <div class="main-subtitle">데이터로 발견하는 대한민국의 숨은 지역과 로컬 경험 (다크 모드)</div>
</div>
""")


# =========================================================
# 사이드바 (다크 모드)
# =========================================================

render_html("""
<div style="font-size:22px; font-weight:850; color:#f0f6fc; margin-bottom:5px;">
    🔍 검색 & 옵션
</div>
<div style="font-size:13px; color:#8b949e; margin-bottom:20px;">
    다크 테마에서 탐색 조건을 설정하세요
</div>
""", sidebar=True)

# 1. 키워드 검색
search_query = st.sidebar.text_input("🔍 키워드 검색", placeholder="지역, 음식, 관광지, 특산품")

# 2. 지역 선택
selected_region = st.sidebar.selectbox("지역 선택", ["전체"] + df["지역"].tolist())

# 3. 다크 지도 지원을 포함한 스타일 선택
map_style = st.sidebar.radio(
    "🗺️ 지도 스타일",
    ["다크 테마 지도", "한국 기본 지도", "위성 영상 지도", "OpenStreetMap"],
    index=0
)

# 4. 점수 슬라이더
min_score = st.sidebar.slider("최소 숨은지역 점수", 0, 100, 70)
food_min = st.sidebar.slider("최소 음식 점수", 0, 100, 80)


# =========================================================
# 데이터 필터링
# =========================================================

filtered_df = df[(df["숨은지역점수"] >= min_score) & (df["음식점수"] >= food_min)].copy()

if selected_region != "전체":
    filtered_df = filtered_df[filtered_df["지역"] == selected_region]

if search_query.strip():
    q = search_query.strip().lower()
    filtered_df = filtered_df[
        filtered_df["지역"].str.lower().str.contains(q) |
        filtered_df["대표음식"].str.lower().str.contains(q) |
        filtered_df["관광지"].str.lower().str.contains(q) |
        filtered_df["특산품"].str.lower().str.contains(q)
    ]


# =========================================================
# 상단 통계
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_html(f"""
    <div class="metric-card">
        <div class="metric-title">📍 발견 지역</div>
        <div class="metric-value">{len(filtered_df)}</div>
        <div class="metric-sub">현재 조건에 맞는 지역</div>
    </div>
    """)

with col2:
    avg_score = filtered_df["숨은지역점수"].mean() if len(filtered_df) > 0 else 0
    render_html(f"""
    <div class="metric-card">
        <div class="metric-title">✨ 평균 숨은지역 점수</div>
        <div class="metric-value">{avg_score:.1f}</div>
        <div class="metric-sub">지역 발견 가능성</div>
    </div>
    """)

with col3:
    avg_food = filtered_df["음식점수"].mean() if len(filtered_df) > 0 else 0
    render_html(f"""
    <div class="metric-card">
        <div class="metric-title">🍚 평균 음식 점수</div>
        <div class="metric-value">{avg_food:.1f}</div>
        <div class="metric-sub">로컬 음식 매력도</div>
    </div>
    """)

with col4:
    avg_awareness = filtered_df["관광인지도"].mean() if len(filtered_df) > 0 else 0
    render_html(f"""
    <div class="metric-card">
        <div class="metric-title">👀 평균 관광 인지도</div>
        <div class="metric-value">{avg_awareness:.1f}</div>
        <div class="metric-sub">낮을수록 숨은 지역</div>
    </div>
    """)


# =========================================================
# 지도 (다크 타일 연동 & 한반도 영역 제약)
# =========================================================

render_html("""
<div class="section-title">🗺️ 대한민국 숨은 지역 지도</div>
""")

if map_style == "다크 테마 지도":
    tiles_url = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
    attr = "CartoDB dark_all"
elif map_style == "한국 기본 지도":
    tiles_url = "https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png"
    attr = "VWorld Base"
elif map_style == "위성 영상 지도":
    tiles_url = "https://xdworld.vworld.kr/2d/Satellite/service/{z}/{x}/{y}.jpeg"
    attr = "VWorld Satellite"
else:
    tiles_url = "OpenStreetMap"
    attr = "OpenStreetMap"

m = folium.Map(
    location=[36.0, 127.8],
    zoom_start=7,
    min_zoom=7,
    max_zoom=13,
    tiles=tiles_url,
    attr=attr,
    control_scale=True,
    no_wrap=True
)

m.fit_bounds([[33.1, 124.5], [38.6, 131.0]])
m.options["maxBounds"] = [[32.5, 123.5], [39.0, 132.0]]
m.options["maxBoundsViscosity"] = 1.0

for _, row in filtered_df.iterrows():
    popup_html = f"""
    <div style="width:230px; font-family:sans-serif; color:#111;">
        <h4 style="margin-bottom:8px; color:#18352c;">📍 {html.escape(row["지역"])}</h4>
        <b>숨은지역 점수</b><br>⭐ {row["숨은지역점수"]}<hr>
        <b>대표 음식</b><br>🍚 {html.escape(row["대표음식"])}<br><br>
        <b>대표 관광지</b><br>🏔️ {html.escape(row["관광지"])}<br><br>
        <b>특산품</b><br>🎁 {html.escape(row["특산품"])}
    </div>
    """

    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f'{row["지역"]} · 숨은지역 {row["숨은지역점수"]}점',
        icon=folium.Icon(color="green", icon="map-marker")
    ).add_to(m)

st_folium(m, use_container_width=True, height=550, returned_objects=[])


# =========================================================
# 지역 탐색
# =========================================================

render_html("""
<div class="section-title">🔎 지역 탐색</div>
""")

if len(filtered_df) == 0:
    st.warning("검색 결과 및 조건에 맞는 지역이 없습니다. 검색어를 바꾸거나 최소 점수를 낮춰보세요.")
else:
    sorted_regions = filtered_df.sort_values("숨은지역점수", ascending=False)

    for _, row in sorted_regions.iterrows():
        render_html(f"""
        <div class="region-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div class="region-name">📍 {html.escape(row["지역"])}</div>
                    <div style="color:#8b949e; margin-top:6px;">
                        대표 음식 · {html.escape(row["대표음식"])}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="small-label">숨은지역 점수</div>
                    <div class="region-score">{row["숨은지역점수"]}</div>
                </div>
            </div>
            <div style="margin-top:18px;">
                <div class="small-label">지역 특색</div>
                <div class="score-bar">
                    <div class="score-fill" style="width:{row["지역특색"]}%"></div>
                </div>
                <div class="small-label">음식 매력도</div>
                <div class="score-bar">
                    <div class="score-fill" style="width:{row["음식점수"]}%"></div>
                </div>
            </div>
        </div>
        """)


# =========================================================
# 상세 지역 (이미지 자동 폴백 렌더링 포함)
# =========================================================

render_html("""
<div class="section-title">🍴 지역 상세 정보</div>
""")

if len(filtered_df) > 0:
    detail_region = st.selectbox("상세 정보를 볼 지역", filtered_df["지역"].tolist())
    selected = filtered_df[filtered_df["지역"] == detail_region].iloc[0]

    render_html(f"""
    <div class="region-card">
        <div class="region-name">📍 {html.escape(selected["지역"])}</div>
        <div style="color:#8b949e; margin-top:7px;">데이터 기반 숨은 지역 탐색 결과</div>
        <div style="display:flex; gap:30px; margin-top:18px;">
            <div>
                <div class="small-label">숨은지역 점수</div>
                <div style="font-size:27px; font-weight:850; color:#3fb950;">
                    {selected["숨은지역점수"]}
                </div>
            </div>
            <div>
                <div class="small-label">음식 점수</div>
                <div style="font-size:27px; font-weight:850; color:#d29922;">
                    {selected["음식점수"]}
                </div>
            </div>
            <div>
                <div class="small-label">지역 특색</div>
                <div style="font-size:27px; font-weight:850; color:#a371f7;">
                    {selected["지역특색"]}
                </div>
            </div>
        </div>
    </div>
    """)

    tab1, tab2, tab3, tab4 = st.tabs(["🍚 로컬 음식", "🏔️ 관광", "🎁 특산품", "💬 리뷰"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            show_local_or_web_image(selected["음식사진"], selected["음식_web"], selected["대표음식"])
        with col2:
            render_html(f"""
            <div class="food-box">
                <div class="small-label">대표 로컬 음식</div>
                <h2 style="color:#f0f6fc; margin-top:6px;">🍚 {html.escape(selected["대표음식"])}</h2>
                <p>{html.escape(selected["음식설명"])}</p>
                <hr style="border-color:#30363d;">
                <div class="small-label">추천 음식점</div>
                <h3 style="color:#f0f6fc;">{html.escape(selected["음식점"])}</h3>
                <p>{html.escape(selected["음식점설명"])}</p>
                <div style="margin-top:20px; font-size:30px; font-weight:850; color:#d29922;">
                    {selected["음식점수"]}점
                </div>
            </div>
            """)

    with tab2:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            show_local_or_web_image(selected["관광사진"], selected["관광_web"], selected["관광지"])
        with col2:
            render_html(f"""
            <div class="tour-box">
                <div class="small-label">추천 관광지</div>
                <h2 style="color:#f0f6fc;">🏔️ {html.escape(selected["관광지"])}</h2>
                <p>{html.escape(selected["관광지설명"])}</p>
                <hr style="border-color:#30363d;">
                <div class="small-label">지역 행사</div>
                <h3 style="color:#f0f6fc;">🎉 {html.escape(selected["지역행사"])}</h3>
                <p>{html.escape(selected["행사설명"])}</p>
                <div style="margin-top:18px; color:#8b949e; font-size:13px;">관광 인지도</div>
                <div class="score-bar">
                    <div class="score-fill" style="width:{selected["관광인지도"]}%"></div>
                </div>
                <b>{selected["관광인지도"]} / 100</b>
            </div>
            """)

    with tab3:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            show_local_or_web_image(selected["특산품사진"], selected["특산품_web"], selected["특산품"])
        with col2:
            render_html(f"""
            <div class="special-box">
                <div class="small-label">지역 특산품</div>
                <h2 style="color:#f0f6fc;">🎁 {html.escape(selected["특산품"])}</h2>
                <p>{html.escape(selected["특산품설명"])}</p>
                <hr style="border-color:#30363d;">
                <div class="small-label">지역 특색 점수</div>
                <div style="font-size:34px; font-weight:850; color:#a371f7; margin-top:5px;">
                    {selected["지역특색"]}점
                </div>
                <div class="score-bar">
                    <div class="score-fill" style="width:{selected["지역특색"]}%"></div>
                </div>
            </div>
            """)

    with tab4:
        render_html(f"""
        <div style="margin-bottom:18px; color:#8b949e;">
            {html.escape(selected["지역"])}에 대한 로컬 여행자들의 간단한 후기입니다.
        </div>
        """)
        for review in selected["리뷰"]:
            render_html(f"""
            <div class="review-box">
                💬 {html.escape(review)}
            </div>
            """)


# =========================================================
# TOP 5
# =========================================================

render_html("""
<div class="section-title">🏆 숨은 지역 TOP 5</div>
""")

top5 = df.sort_values("숨은지역점수", ascending=False).head(5)

for rank, (_, row) in enumerate(top5.iterrows(), start=1):
    col1, col2 = st.columns([0.7, 4])

    with col1:
        render_html(f"""
        <div style="font-size:28px; font-weight:850; color:#58a6ff; padding-top:10px;">
            #{rank}
        </div>
        """)

    with col2:
        render_html(f"""
        <div style="background:#161b22; border:1px solid #30363d; border-radius:14px; padding:15px 18px; margin-bottom:10px;">
            <div style="font-size:20px; font-weight:800; color:#f0f6fc;">
                📍 {html.escape(row["지역"])}
            </div>
            <div style="color:#8b949e; font-size:13px; margin-top:4px;">
                🍚 {html.escape(row["대표음식"])} &nbsp;·&nbsp; 🏔️ {html.escape(row["관광지"])} &nbsp;·&nbsp; ⭐ {row["숨은지역점수"]}점
            </div>
        </div>
        """)
