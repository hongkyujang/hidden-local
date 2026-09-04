
import html
import re
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
    initial_sidebar_state="expanded",
)

# =========================================================
# 화면 디자인
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Noto Sans KR", "Malgun Gothic", sans-serif;
}

.stApp {
    background: #f7f8fa;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e9edf2;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(135deg, #ffffff 0%, #f5f8ff 100%);
    border: 1px solid #e7ebf2;
    border-radius: 22px;
    padding: 26px 30px;
    margin-bottom: 18px;
}

.hero h1 {
    margin: 0;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.8px;
}

.hero p {
    color: #667085;
    margin: 7px 0 0 0;
    font-size: 15px;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e8ecf2;
    border-radius: 18px;
    padding: 18px 20px;
    min-height: 112px;
    box-shadow: 0 3px 15px rgba(30, 41, 59, 0.04);
}

.metric-label {
    color: #667085;
    font-size: 13px;
    margin-bottom: 7px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
}

.metric-sub {
    color: #98a2b3;
    font-size: 12px;
    margin-top: 4px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    margin: 28px 0 12px 0;
    letter-spacing: -0.7px;
}

.region-card {
    background: #ffffff;
    border: 1px solid #e7ebf2;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(30, 41, 59, 0.05);
}

.score-badge {
    display: inline-block;
    background: #fff0f1;
    color: #e53935;
    border-radius: 999px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 800;
}

.info-chip {
    display: inline-block;
    background: #f2f4f7;
    color: #475467;
    border-radius: 999px;
    padding: 5px 9px;
    margin: 2px 3px 2px 0;
    font-size: 11px;
}

.reason-box {
    background: #f8fafc;
    border: 1px solid #e7ebf2;
    border-radius: 15px;
    padding: 16px;
    line-height: 1.8;
}

.review-card {
    background: #ffffff;
    border: 1px solid #e8ecf2;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 10px;
}

.review-name {
    font-weight: 700;
    font-size: 14px;
}

.review-date {
    color: #98a2b3;
    font-size: 11px;
}

.review-text {
    color: #475467;
    line-height: 1.7;
    margin-top: 8px;
}

.photo-caption {
    color: #98a2b3;
    font-size: 10px;
    margin-top: 3px;
}

.top-card {
    background: #ffffff;
    border: 1px solid #e7ebf2;
    border-radius: 16px;
    padding: 15px;
    min-height: 105px;
}

.top-rank {
    font-size: 25px;
    font-weight: 800;
}

.top-region {
    font-weight: 700;
    font-size: 14px;
}

.top-score {
    color: #e53935;
    font-weight: 800;
    font-size: 18px;
}

.small-muted {
    color: #98a2b3;
    font-size: 11px;
}

.footer-note {
    background: #ffffff;
    border: 1px solid #e7ebf2;
    border-radius: 15px;
    padding: 15px;
    color: #667085;
    font-size: 12px;
    line-height: 1.7;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #d9dee7;
    font-weight: 600;
}

div[data-baseweb="select"] > div {
    border-radius: 10px;
}

img {
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 실제 공개 사진
# Wikimedia Commons의 실제 지역/음식 사진을 사용한다.
# 상업적 사용 전에는 각 사진의 라이선스/출처를 반드시 확인한다.
# =========================================================
def commons(filename):
    return "https://commons.wikimedia.org/wiki/Special:FilePath/" + filename.replace(" ", "_")

IMAGE = {
    "정선_지역": commons("Mindungsan.jpg"),
    "정선_관광": commons("Mindungsan.jpg"),
    "정선_행사": commons("180204 정선 A-POP 콘서트 (2) (cropped).jpg"),
    "정선_특산": commons("Mindungsan.jpg"),

    "단양_지역": commons("Korea-Danyang-Dodamsambong 3087-07.JPG"),
    "단양_관광": commons("Korea-Danyang-Dodamsambong 3087-07.JPG"),
    "단양_행사": commons("Danyanggun Travel Day2 01 (31517164294).jpg"),
    "단양_특산": commons("Korea-Danyang-Dodamsambong 3087-07.JPG"),

    "구례_지역": commons("20221101 지리산.jpg"),
    "구례_관광": commons("20221101 지리산.jpg"),
    "구례_행사": commons("Gurye Sansuyu Flower Festival in Spring - 4402796001.jpg"),
    "구례_특산": commons("Gurye Sansuyu Flower Festival in Spring - 4402796001.jpg"),

    "영덕_지역": commons("영덕 대게.jpg"),
    "영덕_관광": commons("영덕 대게.jpg"),
    "영덕_행사": commons("영덕 대게.jpg"),
    "영덕_특산": commons("영덕 대게.jpg"),

    "무주_지역": commons("MJ-Deogyusan.jpg"),
    "무주_관광": commons("MJ-Deogyusan.jpg"),
    "무주_행사": commons("Firefly Bridge Night.JPG"),
    "무주_특산": commons("MJ-Deogyusan.jpg"),

    "서천_지역": commons("Seocheon-gun.jpg"),
    "서천_관광": commons("Seocheon-gun.jpg"),
    "서천_행사": commons("Seocheon-gun.jpg"),
    "서천_특산": commons("Seocheon-gun.jpg"),

    "의령_지역": commons("정암루 모습.png"),
    "의령_관광": commons("정암루 모습.png"),
    "의령_행사": commons("전통혼례(의령군).JPG"),
    "의령_특산": commons("정암루 모습.png"),

    "삼척_지역": commons("한국의 나폴리 장호항2.jpg"),
    "삼척_관광": commons("한국의 나폴리 장호항2.jpg"),
    "삼척_행사": commons("삼척 삼성헌 고택.jpg"),
    "삼척_특산": commons("삼척 삼성헌 고택.jpg"),

    "산채비빔밥": commons("Sanchae Bibimbap in homemade style.jpg"),
    "영덕대게": commons("영덕 대게.jpg"),
    "덕유산": commons("MJ-Deogyusan.jpg"),
}

# 서천 사진 파일이 Commons에서 다를 수 있으므로 안전한 대체 사진을 지정
IMAGE["서천_지역"] = "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=85"
IMAGE["서천_관광"] = IMAGE["서천_지역"]
IMAGE["서천_행사"] = IMAGE["서천_지역"]
IMAGE["서천_특산"] = IMAGE["서천_지역"]

# =========================================================
# 지역 데이터
# =========================================================
regions = [
    {
        "지역": "강원도 정선군", "시군": "정선군",
        "위도": 37.3806, "경도": 128.6608,
        "인구": 35000, "인구변화율": -2.8,
        "음식점수": 90, "관광인지도": 46, "지역특색": 90,
        "대표음식": "곤드레밥", "음식유형": "향토음식",
        "관광지": "민둥산", "관광유형": "자연관광",
        "랜드마크유형": "산·자연",
        "특산품": "곤드레", "지역행사": "정선아리랑제",
        "음식설명": "정선에서 유명한 곤드레나물을 활용한 향토음식입니다.",
        "관광설명": "정선의 대표적인 산악 관광지로 억새 풍경으로 잘 알려져 있습니다.",
        "특산설명": "정선을 대표하는 산나물 특산품입니다.",
        "행사설명": "정선의 전통문화와 지역색을 체험할 수 있는 대표 지역축제입니다.",
        "지역사진": IMAGE["정선_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["정선_관광"], "특산사진": IMAGE["정선_특산"],
        "행사사진": IMAGE["정선_행사"],
        "음식점": "정선 지역 향토음식점",
        "리뷰": [
            ("여행좋아", 5, "민둥산 풍경이 정말 좋았어요. 곤드레밥도 정선에서 먹으니 더 맛있었습니다.", "2026.08.21"),
            ("정선주민", 5, "관광객이 몰리는 곳 말고 조용한 곳을 찾는다면 정선을 추천합니다.", "2026.08.12"),
            ("산책러", 4, "정선 5일장과 주변 시장을 같이 둘러보는 코스가 좋았습니다.", "2026.07.29"),
        ],
    },
    {
        "지역": "충청북도 단양군", "시군": "단양군",
        "위도": 36.9845, "경도": 128.3657,
        "인구": 28000, "인구변화율": -1.7,
        "음식점수": 85, "관광인지도": 52, "지역특색": 88,
        "대표음식": "마늘떡갈비", "음식유형": "향토음식",
        "관광지": "도담삼봉", "관광유형": "자연관광",
        "랜드마크유형": "강·계곡",
        "특산품": "단양마늘", "지역행사": "단양마늘축제",
        "음식설명": "단양의 대표 특산물인 마늘을 활용한 지역 음식입니다.",
        "관광설명": "남한강 위에 솟은 세 봉우리로 단양을 대표하는 명승지입니다.",
        "특산설명": "단양을 대표하는 지역 농특산물입니다.",
        "행사설명": "단양 마늘을 주제로 지역 먹거리와 문화를 체험하는 축제입니다.",
        "지역사진": IMAGE["단양_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["단양_관광"], "특산사진": IMAGE["단양_특산"],
        "행사사진": IMAGE["단양_행사"],
        "음식점": "단양 지역 마늘음식점",
        "리뷰": [
            ("단양여행자", 5, "도담삼봉은 사진보다 직접 보는 게 훨씬 좋았습니다.", "2026.08.19"),
            ("강따라", 4, "마늘을 활용한 음식이 생각보다 다양해서 먹거리 여행으로 좋았어요.", "2026.08.04"),
        ],
    },
    {
        "지역": "전라남도 구례군", "시군": "구례군",
        "위도": 35.2025, "경도": 127.4628,
        "인구": 25000, "인구변화율": -2.2,
        "음식점수": 88, "관광인지도": 41, "지역특색": 94,
        "대표음식": "산채비빔밥", "음식유형": "향토음식",
        "관광지": "지리산", "관광유형": "자연관광",
        "랜드마크유형": "산·자연",
        "특산품": "산수유", "지역행사": "구례산수유꽃축제",
        "음식설명": "지리산 주변의 다양한 산나물을 활용한 향토음식입니다.",
        "관광설명": "지리산의 자연경관을 즐길 수 있는 구례의 대표 관광자원입니다.",
        "특산설명": "구례를 대표하는 산수유 지역 특산품입니다.",
        "행사설명": "봄철 산수유를 중심으로 지역 문화와 자연을 즐기는 축제입니다.",
        "지역사진": IMAGE["구례_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["구례_관광"], "특산사진": IMAGE["구례_특산"],
        "행사사진": IMAGE["구례_행사"],
        "음식점": "구례 지역 산채음식점",
        "리뷰": [
            ("구례한달살이", 5, "조용한 자연을 좋아한다면 정말 잘 맞는 지역입니다.", "2026.08.20"),
            ("지리산러", 5, "산책하고 산채비빔밥 먹는 하루 코스가 좋았어요.", "2026.08.07"),
        ],
    },
    {
        "지역": "경상북도 영덕군", "시군": "영덕군",
        "위도": 36.4150, "경도": 129.3650,
        "인구": 34000, "인구변화율": -2.0,
        "음식점수": 91, "관광인지도": 48, "지역특색": 87,
        "대표음식": "영덕대게", "음식유형": "해산물",
        "관광지": "해맞이공원", "관광유형": "해양관광",
        "랜드마크유형": "해변·항구",
        "특산품": "영덕대게", "지역행사": "영덕대게축제",
        "음식설명": "영덕을 대표하는 동해안 해산물입니다.",
        "관광설명": "동해의 바다 풍경과 일출을 즐길 수 있는 대표 관광지입니다.",
        "특산설명": "영덕을 대표하는 해산물 특산품입니다.",
        "행사설명": "대게와 지역문화를 체험할 수 있는 대표 지역축제입니다.",
        "지역사진": IMAGE["영덕_지역"], "음식사진": IMAGE["영덕대게"],
        "관광사진": IMAGE["영덕_관광"], "특산사진": IMAGE["영덕_특산"],
        "행사사진": IMAGE["영덕_행사"],
        "음식점": "영덕 대게거리 지역 식당",
        "리뷰": [
            ("바다여행", 5, "바다를 보면서 지역 음식을 즐기고 싶다면 추천합니다.", "2026.08.16"),
            ("대게러버", 4, "대게뿐만 아니라 주변 해산물 음식도 다양했습니다.", "2026.08.01"),
        ],
    },
    {
        "지역": "전라북도 무주군", "시군": "무주군",
        "위도": 36.0072, "경도": 127.6607,
        "인구": 24000, "인구변화율": -2.5,
        "음식점수": 82, "관광인지도": 39, "지역특색": 92,
        "대표음식": "어죽", "음식유형": "향토음식",
        "관광지": "덕유산", "관광유형": "자연관광",
        "랜드마크유형": "산·자연",
        "특산품": "머루", "지역행사": "무주반딧불축제",
        "음식설명": "민물고기를 활용한 무주 지역의 향토음식입니다.",
        "관광설명": "사계절 자연경관이 아름다운 무주의 대표 관광지입니다.",
        "특산설명": "무주 지역에서 생산되는 대표 농특산물입니다.",
        "행사설명": "무주의 자연환경과 반딧불이를 주제로 한 지역축제입니다.",
        "지역사진": IMAGE["무주_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["덕유산"], "특산사진": IMAGE["무주_특산"],
        "행사사진": IMAGE["무주_행사"],
        "음식점": "무주 지역 향토음식점",
        "리뷰": [
            ("무주산책", 5, "산과 자연을 좋아하는 사람에게 잘 맞는 지역입니다.", "2026.08.11"),
        ],
    },
    {
        "지역": "충청남도 서천군", "시군": "서천군",
        "위도": 36.0803, "경도": 126.6917,
        "인구": 47000, "인구변화율": -1.3,
        "음식점수": 84, "관광인지도": 44, "지역특색": 86,
        "대표음식": "서천김", "음식유형": "해산물",
        "관광지": "국립생태원", "관광유형": "생태관광",
        "랜드마크유형": "생태·공원",
        "특산품": "한산모시", "지역행사": "한산모시문화제",
        "음식설명": "서천 지역을 대표하는 수산물 특산품입니다.",
        "관광설명": "다양한 생태환경을 체험할 수 있는 서천의 대표 관광자원입니다.",
        "특산설명": "서천의 전통문화와 연결되는 대표 특산품입니다.",
        "행사설명": "한산모시와 지역 전통문화를 체험할 수 있는 지역 행사입니다.",
        "지역사진": IMAGE["서천_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["서천_관광"], "특산사진": IMAGE["서천_특산"],
        "행사사진": IMAGE["서천_행사"],
        "음식점": "서천 지역 해산물 식당",
        "리뷰": [
            ("서해여행", 4, "바다와 생태 체험을 함께 하고 싶을 때 좋은 지역입니다.", "2026.08.05"),
        ],
    },
    {
        "지역": "경상남도 의령군", "시군": "의령군",
        "위도": 35.3222, "경도": 128.2617,
        "인구": 26000, "인구변화율": -2.7,
        "음식점수": 86, "관광인지도": 36, "지역특색": 91,
        "대표음식": "의령소바", "음식유형": "향토음식",
        "관광지": "정암루", "관광유형": "역사·문화",
        "랜드마크유형": "역사·문화",
        "특산품": "망개떡", "지역행사": "의령홍의장군축제",
        "음식설명": "의령을 대표하는 지역 음식입니다.",
        "관광설명": "의령의 역사와 풍경을 함께 느낄 수 있는 지역 명소입니다.",
        "특산설명": "의령을 대표하는 전통 간식입니다.",
        "행사설명": "의령의 역사와 문화를 체험할 수 있는 지역 행사입니다.",
        "지역사진": IMAGE["의령_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["의령_관광"], "특산사진": IMAGE["의령_특산"],
        "행사사진": IMAGE["의령_행사"],
        "음식점": "의령 지역 소바 전문점",
        "리뷰": [
            ("의령여행", 5, "관광객이 많지 않아 조용하게 여행하기 좋았습니다.", "2026.08.09"),
        ],
    },
    {
        "지역": "강원도 삼척시", "시군": "삼척시",
        "위도": 37.4499, "경도": 129.1658,
        "인구": 62000, "인구변화율": -1.9,
        "음식점수": 89, "관광인지도": 50, "지역특색": 89,
        "대표음식": "곰치국", "음식유형": "해산물",
        "관광지": "장호항", "관광유형": "해양관광",
        "랜드마크유형": "해변·항구",
        "특산품": "삼척 장뇌삼", "지역행사": "삼척 장미축제",
        "음식설명": "삼척의 동해안 지역색을 느낄 수 있는 향토음식입니다.",
        "관광설명": "맑은 바다와 해안 풍경으로 유명한 삼척의 대표 관광지입니다.",
        "특산설명": "삼척 지역의 농특산품입니다.",
        "행사설명": "지역 주민과 방문객이 함께 즐기는 삼척의 대표 행사입니다.",
        "지역사진": IMAGE["삼척_지역"], "음식사진": IMAGE["산채비빔밥"],
        "관광사진": IMAGE["삼척_관광"], "특산사진": IMAGE["삼척_특산"],
        "행사사진": IMAGE["삼척_행사"],
        "음식점": "삼척 지역 해산물 식당",
        "리뷰": [
            ("동해바다", 5, "바다 풍경이 좋고 생각보다 조용한 장소가 많았습니다.", "2026.08.16"),
        ],
    },
]

df = pd.DataFrame(regions)

# =========================================================
# 숨은 지역 점수
# =========================================================
def hidden_score(row):
    hidden = 100 - row["관광인지도"]
    population = min(abs(row["인구변화율"]) * 5, 20)
    food = row["음식점수"] * 0.25
    local = row["지역특색"] * 0.25
    return round(hidden * 0.4 + population * 0.1 + food + local, 1)

df["숨은지역점수"] = df.apply(hidden_score, axis=1)

# =========================================================
# 세션 상태
# =========================================================
if "selected_region" not in st.session_state:
    st.session_state.selected_region = df.sort_values(
        "숨은지역점수", ascending=False
    ).iloc[0]["지역"]

# =========================================================
# 사이드바
# =========================================================
st.sidebar.markdown("## 🔎 지역 탐색 필터")

min_score = st.sidebar.slider(
    "⭐ 최소 숨은 지역 점수",
    0, 100, 60
)

food_filter = st.sidebar.selectbox(
    "🍴 선호 음식",
    ["전체", "밥", "국", "해산물", "향토음식"]
)

tour_filter = st.sidebar.selectbox(
    "🏞️ 선호 관광지",
    ["전체", "자연관광", "해양관광", "역사·문화", "생태관광"]
)

landmark_filter = st.sidebar.selectbox(
    "📍 선호 랜드마크",
    ["전체", "산·자연", "강·계곡", "해변·항구", "생태·공원", "역사·문화"]
)

st.sidebar.divider()
st.sidebar.markdown("### 🗺️ 지도 표시")

show_region = st.sidebar.checkbox("📍 추천 지역 핀", True)
show_food = st.sidebar.checkbox("🍴 음식점", True)
show_tour = st.sidebar.checkbox("🏞️ 관광지", True)
show_event = st.sidebar.checkbox("🎪 축제/행사", True)
show_specialty = st.sidebar.checkbox("🛍️ 특산품", True)

# =========================================================
# 필터링
# =========================================================
filtered = df[df["숨은지역점수"] >= min_score].copy()

if food_filter != "전체":
    if food_filter == "밥":
        filtered = filtered[filtered["대표음식"].str.contains("밥", na=False)]
    elif food_filter == "국":
        filtered = filtered[filtered["대표음식"].str.contains("국", na=False)]
    else:
        filtered = filtered[filtered["음식유형"] == food_filter]

if tour_filter != "전체":
    filtered = filtered[filtered["관광유형"] == tour_filter]

if landmark_filter != "전체":
    filtered = filtered[filtered["랜드마크유형"] == landmark_filter]

# 개인화 점수
def personal_score(row):
    score = row["숨은지역점수"]

    if food_filter != "전체":
        if food_filter == "밥" and "밥" in row["대표음식"]:
            score += 5
        elif food_filter == "국" and "국" in row["대표음식"]:
            score += 5
        elif food_filter == row["음식유형"]:
            score += 5

    if tour_filter != "전체" and row["관광유형"] == tour_filter:
        score += 5

    if landmark_filter != "전체" and row["랜드마크유형"] == landmark_filter:
        score += 5

    return round(score, 1)

if len(filtered) > 0:
    filtered["개인추천점수"] = filtered.apply(personal_score, axis=1)

# =========================================================
# 헤더
# =========================================================
st.markdown("""
<div class="hero">
    <h1>📍 숨은 로컬 발견</h1>
    <p>데이터로 발견하는 대한민국의 숨은 지역과 로컬 경험</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 상단 통계
# =========================================================
c1, c2, c3, c4 = st.columns(4)

avg_score = filtered["개인추천점수"].mean() if len(filtered) else 0
review_count = sum(len(x) for x in filtered["리뷰"]) if len(filtered) else 0

with c1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">📍 추천 지역 수</div>'
        f'<div class="metric-value">{len(filtered)}곳</div>'
        f'<div class="metric-sub">현재 조건에 맞는 지역</div></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">⭐ 평균 추천 점수</div>'
        f'<div class="metric-value">{avg_score:.1f}점</div>'
        f'<div class="metric-sub">개인 취향 반영</div></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">💬 리뷰 수</div>'
        f'<div class="metric-value">{review_count}개</div>'
        f'<div class="metric-sub">MVP 예시 리뷰</div></div>',
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">🇰🇷 서비스 범위</div>'
        f'<div class="metric-value">대한민국</div>'
        f'<div class="metric-sub">전국 지역 확장 구조</div></div>',
        unsafe_allow_html=True
    )

# =========================================================
# 지도
# =========================================================
st.markdown('<div class="section-title">🗺️ 추천 지역 지도</div>', unsafe_allow_html=True)

if len(filtered) == 0:
    st.warning("현재 선택한 조건에 맞는 지역이 없습니다. 필터를 조금 낮춰보세요.")
else:
    m = folium.Map(
        location=[36.2, 127.8],
        zoom_start=7,
        tiles="OpenStreetMap"
    )

    # 한국어가 깨지지 않도록 UTF-8 HTML과 CSS를 명시
    for _, row in filtered.iterrows():
        region = html.escape(str(row["지역"]))
        score = html.escape(str(row["개인추천점수"]))
        food = html.escape(str(row["대표음식"]))
        tour = html.escape(str(row["관광지"]))
        specialty = html.escape(str(row["특산품"]))

        popup = f"""
        <meta charset="utf-8">
        <div style="
            width:245px;
            font-family:'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif;
            color:#222;
            line-height:1.55;
        ">
            <div style="font-size:17px;font-weight:800;margin-bottom:7px;">
                📍 {region}
            </div>
            <div style="font-size:14px;margin-bottom:8px;">
                ⭐ <b>맞춤 추천 점수 {score}점</b>
            </div>
            <hr style="border:0;border-top:1px solid #eee;">
            <div>🍚 <b>대표 음식</b> · {food}</div>
            <div>🏞️ <b>관광지</b> · {tour}</div>
            <div>🛍️ <b>특산품</b> · {specialty}</div>
            <div style="margin-top:10px;color:#667085;font-size:12px;">
                아래 상세 영역에서 음식·관광·행사·리뷰를 확인하세요.
            </div>
        </div>
        """

        if show_region:
            folium.Marker(
                [row["위도"], row["경도"]],
                tooltip=f"📍 {row['지역']} · {row['개인추천점수']}점",
                popup=folium.Popup(
                    popup,
                    max_width=320,
                    parse_html=True
                ),
                icon=folium.Icon(
                    color="red",
                    icon="star",
                    prefix="glyphicon"
                )
            ).add_to(m)

        if show_food:
            folium.Marker(
                [row["위도"] + 0.025, row["경도"] + 0.015],
                tooltip=f"🍴 {row['음식점']}",
                popup=folium.Popup(
                    f"""<meta charset="utf-8"><div style="font-family:'Malgun Gothic','Noto Sans KR',sans-serif;">
                    <b>🍴 {html.escape(row['음식점'])}</b><br><br>
                    {html.escape(row['대표음식'])} · {html.escape(row['음식설명'])}
                    </div>""",
                    max_width=300,
                    parse_html=True
                ),
                icon=folium.Icon(color="orange", icon="cutlery", prefix="glyphicon")
            ).add_to(m)

        if show_tour:
            folium.Marker(
                [row["위도"] - 0.025, row["경도"] + 0.020],
                tooltip=f"🏞️ {row['관광지']}",
                popup=folium.Popup(
                    f"""<meta charset="utf-8"><div style="font-family:'Malgun Gothic','Noto Sans KR',sans-serif;">
                    <b>🏞️ {html.escape(row['관광지'])}</b><br><br>
                    {html.escape(row['관광설명'])}
                    </div>""",
                    max_width=300,
                    parse_html=True
                ),
                icon=folium.Icon(color="green", icon="camera", prefix="glyphicon")
            ).add_to(m)

        if show_event:
            folium.Marker(
                [row["위도"] + 0.015, row["경도"] - 0.025],
                tooltip=f"🎪 {row['지역행사']}",
                popup=folium.Popup(
                    f"""<meta charset="utf-8"><div style="font-family:'Malgun Gothic','Noto Sans KR',sans-serif;">
                    <b>🎪 {html.escape(row['지역행사'])}</b><br><br>
                    {html.escape(row['행사설명'])}
                    </div>""",
                    max_width=300,
                    parse_html=True
                ),
                icon=folium.Icon(color="purple", icon="calendar", prefix="glyphicon")
            ).add_to(m)

        if show_specialty:
            folium.Marker(
                [row["위도"] - 0.015, row["경도"] - 0.025],
                tooltip=f"🛍️ {row['특산품']}",
                popup=folium.Popup(
                    f"""<meta charset="utf-8"><div style="font-family:'Malgun Gothic','Noto Sans KR',sans-serif;">
                    <b>🛍️ {html.escape(row['특산품'])}</b><br><br>
                    {html.escape(row['특산설명'])}
                    </div>""",
                    max_width=300,
                    parse_html=True
                ),
                icon=folium.Icon(color="blue", icon="shopping-bag", prefix="glyphicon")
            ).add_to(m)

    map_result = st_folium(
        m,
        width="100%",
        height=610,
        returned_objects=[
            "last_object_clicked_tooltip",
            "last_object_clicked"
        ],
        key="korea_map"
    )

    # 지역 핀 클릭 시 선택 지역 변경
    clicked_tooltip = map_result.get("last_object_clicked_tooltip") if map_result else None

    if clicked_tooltip and "📍" in clicked_tooltip:
        clicked_name = clicked_tooltip.split("📍", 1)[1].split("·", 1)[0].strip()
        if clicked_name in df["지역"].tolist():
            st.session_state.selected_region = clicked_name

# =========================================================
# 지역 상세
# =========================================================
st.markdown('<div class="section-title">📌 지역 상세 정보</div>', unsafe_allow_html=True)

if len(filtered) == 0:
    st.info("지역 상세 정보가 없습니다.")
else:
    names = filtered["지역"].tolist()

    if st.session_state.selected_region not in names:
        st.session_state.selected_region = names[0]

    selected_name = st.selectbox(
        "지역 핀을 클릭하거나 아래에서 지역을 선택하세요.",
        names,
        index=names.index(st.session_state.selected_region),
        key="region_select"
    )

    st.session_state.selected_region = selected_name

    selected = filtered[filtered["지역"] == selected_name].iloc[0]

    # 기본 정보
    a, b, c = st.columns([1.35, 1.0, 1.0])

    with a:
        st.image(selected["지역사진"], use_container_width=True)
        st.markdown(
            f'<div class="photo-caption">공개 라이선스 사진 / 실제 지역 사진</div>',
            unsafe_allow_html=True
        )

    with b:
        st.markdown(f"### 📍 {selected['지역']}")
        st.markdown(
            f'<span class="score-badge">⭐ 맞춤 추천 {selected["개인추천점수"]}점</span>',
            unsafe_allow_html=True
        )
        st.write("")
        st.metric("숨은 지역 점수", f"{selected['숨은지역점수']}점")
        st.write(f"👥 인구: {selected['인구']:,}명")
        st.write(f"📉 인구 변화율: {selected['인구변화율']}%")
        st.write(f"🌍 관광 인지도: {selected['관광인지도']}점")
        st.write(f"✨ 지역 특색: {selected['지역특색']}점")

    with c:
        st.markdown("### 💡 추천 이유")
        st.markdown(
            f"""
            <div class="reason-box">
            ✓ 관광 인지도가 상대적으로 낮음<br>
            ✓ 지역 특색 점수가 높음<br>
            ✓ <b>{selected['음식유형']}</b> 음식 경험 가능<br>
            ✓ <b>{selected['관광유형']}</b> 관광 취향과 연결<br>
            ✓ <b>{selected['랜드마크유형']}</b> 랜드마크 보유
            </div>
            """,
            unsafe_allow_html=True
        )

    # 탭
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🍴 음식 & 맛집", "🏞️ 관광지", "🎪 축제/행사", "🛍️ 특산품", "💬 방문객 리뷰"]
    )

    with tab1:
        x, y = st.columns([1.05, 1])
        with x:
            st.image(selected["음식사진"], use_container_width=True)
            st.markdown(
                '<div class="photo-caption">실제 음식 관련 공개 사진 예시</div>',
                unsafe_allow_html=True
            )
        with y:
            st.markdown(f"### 🍚 {selected['대표음식']}")
            st.write(selected["음식설명"])
            st.markdown("### 🍴 추천 맛집")
            st.write(f"**{selected['음식점']}**")
            st.caption("실제 운영 매장 데이터는 향후 관광/지역 상권 API로 교체할 수 있습니다.")

    with tab2:
        x, y = st.columns([1.05, 1])
        with x:
            st.image(selected["관광사진"], use_container_width=True)
        with y:
            st.markdown(f"### 🏞️ {selected['관광지']}")
            st.write(selected["관광설명"])
            st.markdown(
                f'<span class="info-chip">{selected["관광유형"]}</span>'
                f'<span class="info-chip">{selected["랜드마크유형"]}</span>',
                unsafe_allow_html=True
            )

    with tab3:
        x, y = st.columns([1.05, 1])
        with x:
            st.image(selected["행사사진"], use_container_width=True)
        with y:
            st.markdown(f"### 🎪 {selected['지역행사']}")
            st.write(selected["행사설명"])
            st.info("실제 서비스에서는 행사 일정·장소·예약 정보를 공공 관광 데이터와 연결할 수 있습니다.")

    with tab4:
        x, y = st.columns([1.05, 1])
        with x:
            st.image(selected["특산사진"], use_container_width=True)
        with y:
            st.markdown(f"### 🛍️ {selected['특산품']}")
            st.write(selected["특산설명"])
            st.info("실제 서비스에서는 지역 생산자·판매처·온라인 구매 정보까지 연결할 수 있습니다.")

    with tab5:
        st.markdown("### 💬 방문객 리뷰")
        st.caption("※ 현재는 화면 검증용 예시 리뷰입니다. 실제 서비스에서는 리뷰 DB/API로 교체해야 합니다.")

        for name, rating, text, date in selected["리뷰"]:
            stars = "⭐" * rating
            st.markdown(
                f"""
                <div class="review-card">
                    <div>
                        <span class="review-name">{html.escape(name)}</span>
                        <span class="review-date"> · {html.escape(date)}</span>
                    </div>
                    <div style="margin-top:5px;">{stars}</div>
                    <div class="review-text">{html.escape(text)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### ✍️ 나도 리뷰 남기기")
        review_rating = st.slider("평점", 1, 5, 5, key="review_rating")
        review_text = st.text_area(
            "방문 후기를 입력하세요.",
            key="review_text",
            placeholder="음식, 관광지, 분위기 등에 대한 솔직한 후기를 남겨주세요."
        )

        if st.button("리뷰 등록", key="review_submit"):
            if review_text.strip():
                st.success("리뷰가 등록되었습니다. (현재 MVP에서는 새로고침하면 사라집니다.)")
            else:
                st.warning("리뷰 내용을 입력해주세요.")

# =========================================================
# 여행 코스
# =========================================================
if len(filtered) > 0:
    st.markdown('<div class="section-title">🧭 추천 로컬 여행 코스</div>', unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)

    course = [
        ("①", "🏞️ 관광", selected["관광지"], selected["관광유형"]),
        ("②", "🍴 음식", selected["대표음식"], selected["음식유형"]),
        ("③", "🎪 행사", selected["지역행사"], "지역문화"),
        ("④", "🛍️ 특산품", selected["특산품"], "로컬 쇼핑"),
    ]

    for col, item in zip([q1, q2, q3, q4], course):
        with col:
            st.markdown(
                f"""
                <div class="top-card">
                    <div style="color:#98a2b3;font-size:12px;">{item[0]} {item[1]}</div>
                    <div style="font-weight:800;margin-top:7px;">{item[2]}</div>
                    <div class="small-muted" style="margin-top:6px;">{item[3]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# TOP 5
# =========================================================
st.markdown('<div class="section-title">🏆 추천 지역 TOP 5</div>', unsafe_allow_html=True)

top5 = df.sort_values("숨은지역점수", ascending=False).head(5)

cols = st.columns(5)

for rank, (_, row) in enumerate(top5.iterrows(), start=1):
    with cols[rank - 1]:
        st.markdown(
            f"""
            <div class="top-card">
                <div class="top-rank">{rank}</div>
                <div class="top-region">{row['지역']}</div>
                <div class="top-score">{row['숨은지역점수']}점</div>
                <div class="small-muted">{row['대표음식']} · {row['관광지']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# 안내
# =========================================================
st.markdown(
    """
    <div class="footer-note" style="margin-top:25px;">
    <b>현재 MVP 안내</b><br>
    • 지도/지역 구조는 한국 지역 중심으로 구성되어 있습니다.<br>
    • 지역 사진 일부는 Wikimedia Commons의 공개 라이선스 사진을 사용합니다.
      실제 배포·상업 이용 전에는 각 이미지의 라이선스와 출처 표시 조건을 확인하세요.<br>
    • 방문객 리뷰는 현재 UI 시연용 예시입니다. 실제 리뷰를 사용하려면 리뷰 제공 서비스의 공식 API/사용자 동의 기반 DB가 필요합니다.<br>
    • 다음 단계에서 SGIS OpenAPI를 연결하면 지역 통계 데이터를 자동으로 가져와 숨은 지역 점수를 계산하도록 바꿀 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True
)
