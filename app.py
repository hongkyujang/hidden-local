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
# HTML 렌더링 helper
# =========================================================

def render_html(content):
    """메인 영역 HTML 렌더링"""
    st.markdown(
        textwrap.dedent(content),
        unsafe_allow_html=True
    )


def render_sidebar_html(content):
    """사이드바 영역 HTML 렌더링"""
    st.sidebar.markdown(
        textwrap.dedent(content),
        unsafe_allow_html=True
    )


# =========================================================
# 다크 모드 CSS
# =========================================================

render_html("""
<style>

/* 전체 다크 모드 배경 및 글자색 */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
    background-color: #0f172a !important;
    color: #f8fafc !important;
}

[data-testid="stHeader"] {
    background-color: #0f172a !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 30px !important;
    padding-bottom: 50px !important;
}

/* 사이드바 다크 스타일 */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] > div {
    background-color: #111827 !important;
}

/* 메인 제목 카드 */
.main-title-card {
    background: #1e293b;
    padding: 32px 38px;
    border-radius: 22px;
    border: 1px solid #334155;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.4);
    margin-bottom: 25px;
}

.main-title-small {
    font-size: 15px;
    color: #34d399;
    font-weight: 700;
    margin-bottom: 8px;
}

.main-title {
    font-size: 42px;
    font-weight: 850;
    color: #f8fafc;
    letter-spacing: -2px;
    margin-bottom: 8px;
}

.main-subtitle {
    font-size: 16px;
    color: #94a3b8;
}

/* 섹션 제목 */
.section-title {
    color: #f8fafc;
    font-size: 24px;
    font-weight: 850;
    margin-top: 30px;
    margin-bottom: 16px;
}

/* 통계 카드 */
.metric-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.3);
    min-height: 120px;
}

.metric-title {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}

.metric-value {
    color: #38bdf8;
    font-size: 30px;
    font-weight: 850;
}

.metric-sub {
    color: #64748b;
    font-size: 12px;
    margin-top: 5px;
}

/* 지역 카드 */
.region-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.3);
}

.region-name {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 850;
}

.region-score {
    color: #34d399;
    font-size: 32px;
    font-weight: 850;
}

.small-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 700;
}

/* 게이지 바 */
.score-bar {
    height: 9px;
    background: #334155;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 7px;
    margin-bottom: 10px;
}

.score-fill {
    height: 100%;
    background: #10b981;
    border-radius: 10px;
}

/* 로컬 정보 박스 */
.food-box {
    background: #172554;
    border: 1px solid #1e40af;
    border-radius: 16px;
    padding: 20px;
    color: #e0f2fe;
}

.tour-box {
    background: #064e3b;
    border: 1px solid #065f46;
    border-radius: 16px;
    padding: 20px;
    color: #ecfdf5;
}

.special-box {
    background: #4c1d95;
    border: 1px solid #5b21b6;
    border-radius: 16px;
    padding: 20px;
    color: #f3e8ff;
}

/* 리뷰 박스 */
.review-box {
    background: #1e293b;
    border-left: 4px solid #10b981;
    border-radius: 10px;
    padding: 15px 18px;
    margin-bottom: 10px;
    color: #cbd5e1;
}

/* 탭 UI 다크 스타일 커스텀 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: #1e293b;
    color: #94a3b8;
    border-radius: 10px;
    padding: 8px 18px;
}

.stTabs [aria-selected="true"] {
    background: #10b981 !important;
    color: #ffffff !important;
}

iframe {
    border-radius: 16px !important;
}

button {
    border-radius: 10px !important;
}

</style>
""")


# =========================================================
# 로컬 이미지 및 다크 대체 UI 설정
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


def get_image_path(filename):
    return os.path.join(ASSET_DIR, filename)


def show_local_image(filename, caption=None, category="관광"):
    """로컬 이미지 출력 (없을 경우 카테고리별 다크 카드 표시)"""
    path = get_image_path(filename)

    if os.path.isfile(path):
        st.image(
            path,
            caption=caption,
            use_container_width=True
        )
    else:
        # 카테고리별 아이콘 & 스타일 지정
        icons = {"음식": "🍚", "관광": "🏔️", "지형": "🌿"}
        icon = icons.get(category, "📷")

        render_html(f"""
        <div style="
            width:100%;
            height:320px;
            background:linear-gradient(135deg, #1e293b, #0f172a);
            border:1px solid #334155;
            border-radius:16px;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            color:#94a3b8;
            font-weight:700;
        ">
            <div>
                <div style="font-size:50px; margin-bottom:12px;">{icon}</div>
                <div style="font-size:18px; color:#f8fafc; margin-bottom:4px;">{html.escape(caption or category)}</div>
                <div style="font-size:12px; color:#64748b;">이미지 준비 중 (assets/{html.escape(filename)})</div>
            </div>
        </div>
        """)


# =========================================================
# 지역 데이터
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
        "특산품": "곤드레 & 산채",
        "특산품설명": "정선을 대표하는 산나물로 다양한 향토 음식에 활용됩니다.",
        "음식사진": "jeongseon_food.jpg",
        "관광사진": "jeongseon_tour.jpg",
        "특산품사진": "jeongseon_specialty.jpg",
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
        "대표음식": "영덕 대게",
        "음식설명": "영덕을 대표하는 해산물로 지역의 대표적인 먹거리입니다.",
        "음식점": "영덕 대게거리",
        "음식점설명": "영덕 대게를 중심으로 다양한 해산물 요리를 맛볼 수 있는 음식거리입니다.",
        "관광지": "해맞이공원 & 영덕 해안선",
        "관광지설명": "동해의 아름다운 일출과 해안 절경을 감상할 수 있는 대표적인 지형/관광지입니다.",
        "지역행사": "영덕 대게축제",
        "행사설명": "영덕대게와 지역 수산문화를 경험할 수 있는 대표적인 지역축제입니다.",
        "특산품": "영덕대게",
        "특산품설명": "영덕을 대표하는 수산물로 지역 경제와 관광을 함께 이끌고 있습니다.",
        "음식사진": "yeongdeok_food.jpg",
        "관광사진": "yeongdeok_tour.jpg",
        "특산품사진": "yeongdeok_specialty.jpg",
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
        "대표음식": "무주 어죽",
        "음식설명": "민물고기를 활용해 끓여낸 무주의 대표적인 향토 음식입니다.",
        "음식점": "무주 어죽마을",
        "음식점설명": "무주 지역 전통 방식의 어죽과 향토음식을 맛볼 수 있습니다.",
        "관광지": "덕유산 국립공원",
        "관광지설명": "사계절 아름다운 산세와 계곡 풍경을 자랑하는 대표적인 지형 관광지입니다.",
        "지역행사": "무주 반딧불축제",
        "행사설명": "반딧불이를 주제로 자연환경과 지역문화를 체험할 수 있는 축제입니다.",
        "특산품": "무주 머루",
        "특산품설명": "무주의 청정 자연환경에서 생산되는 대표적인 농특산물입니다.",
        "음식사진": "muju_food.jpg",
        "관광사진": "muju_tour.jpg",
        "특산품사진": "muju_specialty.jpg",
        "리뷰": [
            "어죽이 생각보다 담백하고 맛있었습니다.",
            "덕유산 풍경이 정말 아름다웠습니다.",
            "자연 속에서 쉬고 싶을 때 좋은 지역입니다."
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
# 메인 제목
# =========================================================

render_html("""
<div class="main-title-card">
    <div class="main-title-small">📍 LOCAL DISCOVERY (DARK MODE)</div>
    <div class="main-title">숨은 로컬 발견</div>
    <div class="main-subtitle">데이터로 발견하는 대한민국의 숨은 지역, 관광지, 음식 및 지형 정보</div>
</div>
""")


# =========================================================
# 사이드바
# =========================================================

render_sidebar_html("""
<div style="font-size:25px; font-weight:850; color:#f8fafc; margin-bottom:5px;">
    📍 숨은 로컬
</div>
<div style="font-size:13px; color:#94a3b8; margin-bottom:25px;">
    지역을 데이터로 탐색해보세요
</div>
""")

selected_region = st.sidebar.selectbox(
    "지역 선택",
    ["전체"] + df["지역"].tolist()
)

min_score = st.sidebar.slider(
    "최소 숨은지역 점수",
    min_value=0,
    max_value=100,
    value=70
)

food_min = st.sidebar.slider(
    "최소 음식 점수",
    min_value=0,
    max_value=100,
    value=80
)


# =========================================================
# 데이터 필터
# =========================================================

filtered_df = df[
    (df["숨은지역점수"] >= min_score) &
    (df["음식점수"] >= food_min)
].copy()

if selected_region != "전체":
    filtered_df = filtered_df[filtered_df["지역"] == selected_region]


# =========================================================
# 상단 통계
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_html(f"""
    <div class="metric-card">
        <div class="metric-title">📍 발견 지역</div>
        <div class="metric-value">{len(filtered_df)}개</div>
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
# 지도 (다크 모드 타일 적용)
# =========================================================

render_html("""
<div class="section-title">🗺️ 숨은 지역 지도</div>
""")

m = folium.Map(
    location=[36.2, 127.8],
    zoom_start=7,
    min_zoom=7,
    max_zoom=12,
    tiles="CartoDB dark_matter",
    control_scale=True,
    no_wrap=True
)

m.fit_bounds([[33.0, 124.0], [38.8, 132.0]])
m.options["maxBounds"] = [[32.0, 123.0], [40.5, 134.0]]
m.options["maxBoundsViscosity"] = 1.0


for _, row in filtered_df.iterrows():
    popup_html = f"""
    <div style="width:230px; font-family:Arial,sans-serif; color:#1e293b;">
        <h4 style="margin-bottom:8px; color:#0f172a;">📍 {html.escape(row["지역"])}</h4>
        <b>숨은지역 점수</b>: ⭐ {row["숨은지역점수"]}<br>
        <hr style="margin:8px 0;">
        <b>대표 음식</b>: 🍚 {html.escape(row["대표음식"])}<br>
        <b>관광/지형</b>: 🏔️ {html.escape(row["관광지"])}<br>
        <b>특산품</b>: 🌿 {html.escape(row["특산품"])}
    </div>
    """

    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f'{row["지역"]} · 숨은지역 {row["숨은지역점수"]}점',
        icon=folium.Icon(color="emerald", icon="map-marker", prefix="fa")
    ).add_to(m)

st_folium(m, width=None, height=550, returned_objects=[])


# =========================================================
# 지역 탐색
# =========================================================

render_html("""
<div class="section-title">🔎 지역 목록</div>
""")

if len(filtered_df) == 0:
    st.warning("현재 필터 조건에 맞는 지역이 없습니다. 최소 점수를 조정해보세요.")
else:
    sorted_regions = filtered_df.sort_values("숨은지역점수", ascending=False)

    for _, row in sorted_regions.iterrows():
        render_html(f"""
        <div class="region-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div class="region-name">📍 {html.escape(row["지역"])}</div>
                    <div style="color:#94a3b8; margin-top:6px;">대표 음식: {html.escape(row["대표음식"])} | 대표 관광/지형: {html.escape(row["관광지"])}</div>
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
# 상세 정보 및 사진 갤러리
# =========================================================

render_html("""
<div class="section-title">🏞️ 지역 상세 정보 및 갤러리</div>
""")

if len(filtered_df) > 0:
    detail_region = st.selectbox("상세 조회를 위한 지역 선택", filtered_df["지역"].tolist())
    selected = filtered_df[filtered_df["지역"] == detail_region].iloc[0]

    render_html(f"""
    <div class="region-card">
        <div class="region-name">📍 {html.escape(selected["지역"])}</div>
        <div style="color:#94a3b8; margin-top:7px;">데이터 기반 상세 로컬 분석 결과</div>
        <div style="display:flex; gap:30px; margin-top:18px;">
            <div>
                <div class="small-label">숨은지역 점수</div>
                <div style="font-size:27px; font-weight:850; color:#34d399;">{selected["숨은지역점수"]}</div>
            </div>
            <div>
                <div class="small-label">음식 점수</div>
                <div style="font-size:27px; font-weight:850; color:#f59e0b;">{selected["음식점수"]}</div>
            </div>
            <div>
                <div class="small-label">지역 특색</div>
                <div style="font-size:27px; font-weight:850; color:#a855f7;">{selected["지역특색"]}</div>
            </div>
        </div>
    </div>
    """)

    tab1, tab2, tab3, tab4 = st.tabs(["🍚 대표 음식", "🏔️ 관광지 & 지형", "🌿 특산품", "💬 로컬 리뷰"])

    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            show_local_image(selected["음식사진"], caption=selected["대표음식"], category="음식")
        with col2:
            render_html(f"""
            <div class="food-box">
                <div class="small-label" style="color:#93c5fd;">대표 로컬 음식</div>
                <h2 style="color:#ffffff; margin-top:6px;">🍚 {html.escape(selected["대표음식"])}</h2>
                <p>{html.escape(selected["음식설명"])}</p>
                <hr style="border-color:#1e40af;">
                <div class="small-label" style="color:#93c5fd;">추천 맛집</div>
                <h3 style="color:#ffffff;">{html.escape(selected["음식점"])}</h3>
                <p>{html.escape(selected["음식점설명"])}</p>
                <div style="margin-top:20px; font-size:30px; font-weight:850; color:#60a5fa;">
                    음식 점수: {selected["음식점수"]}점
                </div>
            </div>
            """)

    with tab2:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            show_local_image(selected["관광사진"], caption=selected["관광지"], category="관광")
        with col2:
            render_html(f"""
            <div class="tour-box">
                <div class="small-label" style="color:#6ee7b7;">추천 관광지 / 지형</div>
                <h2 style="color:#ffffff;">🏔️ {html.escape(selected["관광지"])}</h2>
                <p>{html.escape(selected["관광지설명"])}</p>
                <hr style="border-color:#065f46;">
                <div class="small-label" style="color:#6ee7b7;">지역 대표 행사</div>
                <h3 style="color:#ffffff;">🎉 {html.escape(selected["지역행사"])}</h3>
                <p>{html.escape(selected["행사설명"])}</p>
            </div>
            """)

    with tab3:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            show_local_image(selected["특산품사진"], caption=selected["특산품"], category="지형")
        with col2:
            render_html(f"""
            <div class="special-box">
                <div class="small-label" style="color:#c084fc;">지역 특산품 및 자원</div>
                <h2 style="color:#ffffff;">🌿 {html.escape(selected["특산품"])}</h2>
                <p>{html.escape(selected["특산품설명"])}</p>
                <hr style="border-color:#5b21b6;">
                <div class="small-label" style="color:#c084fc;">지역 특색 점수</div>
                <div style="font-size:34px; font-weight:850; color:#e9d5ff; margin-top:5px;">
                    {selected["지역특색"]}점
                </div>
            </div>
            """)

    with tab4:
        render_html(f"""
        <div style="margin-bottom:18px; color:#94a3b8;">
            {html.escape(selected["지역"])} 방문객들의 실제 리뷰입니다.
        </div>
        """)
        for review in selected["리뷰"]:
            render_html(f"""
            <div class="review-box">💬 {html.escape(review)}</div>
            """)
