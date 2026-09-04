import os
import html
import textwrap

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# =========================================================
# 1. 페이지 설정
# =========================================================

st.set_page_config(
    page_title="숨은 로컬 발견 - Dark Mode",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. HTML Helper & Custom CSS (Dark Theme)
# =========================================================

def render_html(content):
    st.markdown(textwrap.dedent(content), unsafe_allow_html=True)

def render_sidebar_html(content):
    st.sidebar.markdown(textwrap.dedent(content), unsafe_allow_html=True)

render_html("""
<style>
/* 다크 모드 배경 지정 */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
    background-color: #0b0f19 !important;
    color: #f1f5f9 !important;
}

[data-testid="stHeader"] {
    background-color: #0b0f19 !important;
}

.block-container {
    max-width: 1400px !important;
    padding-top: 20px !important;
    padding-bottom: 50px !important;
}

/* 사이드바 스타일 */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1f2937;
}

/* 상단 헤더 */
.header-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0 20px 0;
}
.header-title {
    font-size: 28px;
    font-weight: 850;
    color: #f8fafc;
}
.header-sub {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 4px;
}

/* 상단 4개 지표 카드 */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.metric-box {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.metric-icon {
    font-size: 28px;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.metric-val {
    font-size: 24px;
    font-weight: 850;
    color: #f8fafc;
}
.metric-lbl {
    font-size: 13px;
    color: #94a3b8;
}

/* 섹션 타이틀 */
.section-head {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
    margin: 28px 0 16px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* 메인 상세 정보 뷰 */
.detail-main-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
}

.hero-badge {
    background: #ef4444;
    color: white;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}

/* 카테고리 썸네일 카드 */
.sub-card {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    overflow: hidden;
    height: 100%;
}
.sub-card-body {
    padding: 14px;
}
.sub-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 6px;
}
.sub-card-desc {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.4;
}

/* 맛집/장소 카드 */
.place-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 16px;
    height: 100%;
}
.place-title {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
    margin: 8px 0 4px 0;
}
.place-star {
    color: #f59e0b;
    font-size: 13px;
    font-weight: 700;
}
.place-address {
    font-size: 12px;
    color: #64748b;
    margin-top: 4px;
}

/* 방문객 리뷰 카드 */
.review-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 16px;
    height: 100%;
}
.review-user {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}
.review-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #3b82f6;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: white;
}
.review-text {
    font-size: 13px;
    color: #cbd5e1;
    line-height: 1.5;
    margin-bottom: 12px;
}

/* 하단 TOP 5 카드 */
.top5-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.top5-rank {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #3b82f6;
    color: white;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

/* 탭 커스텀 */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid #334155;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
    padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom-color: #38bdf8 !important;
}

/* 지도 범례 */
.legend-bar {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 10px;
    font-size: 12px;
    color: #94a3b8;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
}
.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}
</style>
""")


# =========================================================
# 3. 데이터 세트 (문자열 파이썬 오류 수정 완료)
# =========================================================

region_data = [
    {
        "지역": "강원도 정선군",
        "점수": 88.7,
        "위도": 37.3806,
        "경도": 128.6608,
        "인구": "34,419명",
        "면적": "1,220.6㎢",
        "음식점수": "46개",
        "관광지수": "91개",
        "설명": "아리랑의 고장 정선은 아름다운 자연경관과 전통문화, 그리고 건강한 먹거리가 가득한 보석 같은 지역입니다.",
        "대표음식": "곤드레밥",
        "대표음식_설명": "정선의 대표 향토 음식으로, 건강에 좋은 곤드레나물을 넣어 지은 밥입니다.",
        "주요특산품": "곤드레",
        "주요특산품_설명": "해발 700m 고산지대에서 자란 향긋한 곤드레나물입니다.",
        "대표축제": "정선 아리랑제",
        "대표축제_설명": "정선 아리랑을 주제로 한 전통 문화 축제입니다.",
        "맛집목록": [
            {"이름": "정선곤드레본가", "평점": "4.6", "리뷰": "(156)", "특징": "곤드레밥 전문점", "주소": "정선읍 5일장길 31"},
            {"이름": "함백산식당", "평점": "4.4", "리뷰": "(98)", "특징": "산채정식, 더덕구이", "주소": "고한읍 고한로 123"},
            {"이름": "정선아리랑시장 맛집", "평점": "4.3", "리뷰": "(87)", "특징": "다양한 전통시장 먹거리", "주소": "정선읍 봉양리 322"}
        ],
        "리뷰목록": [
            {"이름": "여행좋아", "날짜": "2026.05.12", "평점": 5, "내용": "자연경관이 정말 아름답고 음식도 건강하고 맛있어요! 곤드레밥 꼭 드셔보세요."},
            {"이름": "산책러버", "날짜": "2026.04.28", "평점": 4, "내용": "아리랑시장 구경도 재미있고 5일장도 꼭 가보세요. 지역분들도 친절해요!"},
            {"이름": "맛집탐방가", "날짜": "2026.04.15", "평점": 5, "내용": "정선은 조용하고 깨끗해서 힐링하기 좋아요. 지방은 힐링 100%입니다."},
            {"이름": "캠핑가는부자", "날짜": "2026.03.10", "평점": 4, "내용": "민둥산 억새밭은 가을에 꼭 가보세요. 풍경이 정말 장관입니다."}
        ]
    },
    {
        "지역": "전라남도 구례군",
        "점수": 87.3,
        "위도": 35.2025,
        "경도": 127.4628,
        "인구": "25,110명",
        "면적": "429.8㎢",
        "음식점수": "38개",
        "관광지수": "75개",
        "설명": "지리산과 섬진강이 품은 청정 지역으로, 산수유와 고즈넉한 사찰이 어우러진 휴식의 공간입니다.",
        "대표음식": "산채비빔밥",
        "대표음식_설명": "지리산의 기운을 담은 각종 제철 산나물로 풍성하게 비벼낸 건강식입니다.",
        "주요특산품": "산수유",
        "주요특산품_설명": "붉은 빛깔과 새콤한 맛이 특징인 구례의 대표 특산 자원입니다.",
        "대표축제": "구례 산수유꽃축제",
        "대표축제_설명": "봄을 가장 먼저 알리는 노란 산수유꽃의 향연입니다.",
        "맛집목록": [
            {"이름": "지리산산채식당", "평점": "4.7", "리뷰": "(210)", "특징": "산채정식 및 재첩국", "주소": "구례읍 봉성로 45"},
            {"이름": "구례화엄사맛집", "평점": "4.5", "리뷰": "(134)", "특징": "버섯전골", "주소": "마산면 화엄사로 280"}
        ],
        "리뷰목록": [
            {"이름": "지리산지기", "날짜": "2026.05.01", "평점": 5, "내용": "공기가 너무 맑고 산채비빔밥 나물 향이 살아있습니다."}
        ]
    },
    {
        "지역": "경상남도 의령군",
        "점수": 86.1,
        "위도": 35.3217,
        "경도": 128.2614,
        "인구": "26,300명",
        "면적": "482.9㎢",
        "음식점수": "32개",
        "관광지수": "62개",
        "설명": "의병의 호국 정신과 남강의 수려한 지형, 특색 있는 로컬 음식을 간직한 숨은 보석입니다.",
        "대표음식": "의령소바",
        "대표음식_설명": "메밀면과 진한 육수, 장조림 고명이 조화를 이루는 의령 특유의 별미입니다.",
        "주요특산품": "망개떡",
        "주요특산품_설명": "망개잎으로 감싸 은은한 향이 배어있는 쫄깃한 전통 찹쌀떡입니다.",
        "대표축제": "의령 리치리치페스티벌",
        "대표축제_설명": "솥바위 전설을 바탕으로 한 부자 기원 유익 축제입니다.",
        "맛집목록": [
            {"이름": "의령소바 본점", "평점": "4.8", "리뷰": "(540)", "특징": "전통 온소바/비빔소바", "주소": "의령읍 의병로 18길"}
        ],
        "리뷰목록": [
            {"이름": "소바매니아", "날짜": "2026.04.18", "평점": 5, "내용": "소바 국물이 진국이고 망개떡은 기념품으로 사가기 딱 좋습니다."}
        ]
    },
    {
        "지역": "전라북도 무주군",
        "점수": 84.9,
        "위도": 36.0072,
        "경도": 127.6607,
        "인구": "23,500명",
        "면적": "631.8㎢",
        "음식점수": "41개",
        "관광지수": "83개",
        "설명": "덕유산의 장엄한 산세와 깨끗한 금강 상류가 만들어낸 청정 생태 관광지입니다.",
        "대표음식": "무주 어죽",
        "대표음식_설명": "금강의 민물고기와 수제비를 얼큰하게 끓여낸 영양 만점 향토 음식입니다.",
        "주요특산품": "머루와인",
        "주요특산품_설명": "덕유산 고랭지 머루로 발효시켜 만든 풍미 깊은 지역 와인입니다.",
        "대표축제": "무주 반딧불축제",
        "대표축제_설명": "천연기념물 반딧불이를 직접 관찰하는 친환경 생태 축제입니다.",
        "맛집목록": [
            {"이름": "금강어죽", "평점": "4.6", "리뷰": "(180)", "특징": "빠가사리 어죽", "주소": "무주읍 반딧로 102"}
        ],
        "리뷰목록": [
            {"이름": "반딧불이", "날짜": "2026.03.22", "평점": 5, "내용": "덕유산 등산 후 먹는 어죽 맛은 잊을 수가 없네요."}
        ]
    },
    {
        "지역": "충청북도 단양군",
        "점수": 84.2,
        "위도": 36.9845,
        "경도": 128.3657,
        "인구": "27,800명",
        "면적": "781.0㎢",
        "음식점수": "52개",
        "관광지수": "95개",
        "설명": "단양팔경의 장관과 패러글라이딩, 마늘 풍미 요리가 가득한 활력 넘치는 지역입니다.",
        "대표음식": "마늘떡갈비",
        "대표음식_설명": "알싸한 단양 마늘과 두툼한 육즙이 만나 완성된 명품 떡갈비입니다.",
        "주요특산품": "단양 마늘",
        "주요특산품_설명": "단단한 육질과 우수한 저장성을 자랑하는 명품 마늘입니다.",
        "대표축제": "단양 온달문화축제",
        "대표축제_설명": "온달장군과 평강공주의 설화를 배경으로 펼쳐지는 역사 문화 축제입니다.",
        "맛집목록": [
            {"이름": "단양마늘석갈비", "평점": "4.5", "리뷰": "(320)", "특징": "마늘떡갈비 정식", "주소": "단양읍 중앙로 45"}
        ],
        "리뷰목록": [
            {"이름": "skywalker", "날짜": "2026.02.14", "평점": 5, "내용": "도담삼봉 뷰도 대박이고 마늘떡갈비도 짭조름하니 너무 맛있었습니다."}
        ]
    }
]

df = pd.DataFrame(region_data)


# =========================================================
# 4. 사이드바 (필터 컨트롤)
# =========================================================

render_sidebar_html("""
<div style="font-size:18px; font-weight:800; color:#f8fafc; margin-bottom:15px; display:flex; align-items:center; gap:8px;">
    🔍 지역 탐색 필터
</div>
""")

min_score = st.sidebar.slider("최소 숨은 지역 점수", 0, 100, 60)
food_type = st.sidebar.selectbox("선호 음식 타입", ["전체", "한식/향토음식", "면류/소바", "해산물/어죽"])

st.sidebar.markdown("<div style='margin-top:15px; font-weight:700; color:#94a3b8; font-size:13px;'>지도 표시 옵션</div>", unsafe_allow_html=True)
chk_pin = st.sidebar.checkbox("추천 지역 핀", value=True)
chk_food = st.sidebar.checkbox("음식점", value=True)
chk_tour = st.sidebar.checkbox("관광지", value=True)
chk_fest = st.sidebar.checkbox("축제/행사", value=True)
chk_prod = st.sidebar.checkbox("특산품", value=False)

st.sidebar.markdown("<div style='margin-top:15px; font-weight:700; color:#94a3b8; font-size:13px;'>정렬 기준</div>", unsafe_allow_html=True)
sort_order = st.sidebar.selectbox("", ["숨은 지역 점수 순", "관광지 수 순", "음식점 수 순"])

st.sidebar.markdown("<div style='margin-top:15px; font-weight:700; color:#94a3b8; font-size:13px;'>키워드 검색</div>", unsafe_allow_html=True)
search_kw = st.sidebar.text_input("", placeholder="지역명 또는 키워드 입력")
st.sidebar.button("검색", use_container_width=True)
st.sidebar.button("🔄 필터 초기화", use_container_width=True)


# =========================================================
# 5. 메인 레이아웃 Header & Metric Cards
# =========================================================

render_html("""
<div class="header-card">
    <div>
        <div class="header-title">📍 숨은 로컬 발견</div>
        <div class="header-sub">데이터로 발견하는 대한민국의 숨은 지역과 로컬 경험</div>
    </div>
    <div>
        <span style="background:#1e293b; border:1px solid #334155; padding:6px 14px; border-radius:20px; font-size:13px; color:#ef4444; font-weight:700;">
            ❤️ 찜한 지역 <b style="color:white;">0</b>
        </span>
    </div>
</div>
""")

# 4개 지표 카드
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_html(f"""
    <div class="metric-box">
        <div class="metric-icon" style="background:rgba(16, 185, 129, 0.15); color:#10b981;">★</div>
        <div>
            <div class="metric-lbl">추천 지역 수</div>
            <div class="metric-val">{len(df)}곳</div>
        </div>
    </div>
    """)
with col2:
    render_html(f"""
    <div class="metric-box">
        <div class="metric-icon" style="background:rgba(56, 189, 248, 0.15); color:#38bdf8;">📊</div>
        <div>
            <div class="metric-lbl">평균 숨은 점수</div>
            <div class="metric-val">{df['점수'].mean():.1f}점</div>
        </div>
    </div>
    """)
with col3:
    render_html(f"""
    <div class="metric-box">
        <div class="metric-icon" style="background:rgba(168, 85, 247, 0.15); color:#a855f7;">💬</div>
        <div>
            <div class="metric-lbl">리뷰 수</div>
            <div class="metric-val">237개</div>
        </div>
    </div>
    """)
with col4:
    render_html(f"""
    <div class="metric-box">
        <div class="metric-icon" style="background:rgba(245, 158, 11, 0.15); color:#f59e0b;">🎁</div>
        <div>
            <div class="metric-lbl">특산품</div>
            <div class="metric-val">32개</div>
        </div>
    </div>
    """)


# =========================================================
# 6. 추천 지역 지도 Section (Folium 타일 URL 직접 지정하여 오류 완벽 해결)
# =========================================================

render_html("""
<div class="section-head">
    <span>🗺️ 추천 지역 지도</span>
</div>
""")

m = folium.Map(
    location=[36.3, 127.8],
    zoom_start=7,
    tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    control_scale=False
)

for _, r in df.iterrows():
    popup_text = f"""
    <div style="width:200px; font-family:sans-serif; color:#1e293b;">
        <h4 style="margin:0 0 5px 0; color:#0f172a;">📍 {r['지역']}</h4>
        <b style="color:#ef4444;">숨은 점수: {r['점수']}점</b><br>
        <span style="font-size:12px;">대표음식: {r['대표음식']}</span>
    </div>
    """
    folium.Marker(
        location=[r["위도"], r["경도"]],
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=f"{r['지역']} ({r['점수']}점)",
        icon=folium.Icon(color="red" if r["점수"] > 87 else "blue", icon="star", prefix="fa")
    ).add_to(m)

st_folium(m, width=None, height=420, returned_objects=[])

# 지도 하단 범례
render_html("""
<div class="legend-bar">
    <div class="legend-item"><div class="legend-dot" style="background:#ef4444;"></div> 숨은 점수 90점 이상</div>
    <div class="legend-item"><div class="legend-dot" style="background:#f97316;"></div> 80~90점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#10b981;"></div> 70~80점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#3b82f6;"></div> 60~70점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#64748b;"></div> 60점 이하</div>
</div>
""")


# =========================================================
# 7. 지역 상세 정보 Section (메인 선택 뷰)
# =========================================================

render_html("""
<div class="section-head">
    <span>📍 지역 상세 정보</span>
    <button style="background:#1e293b; border:1px solid #334155; color:#94a3b8; padding:5px 12px; border-radius:8px; font-size:12px; cursor:pointer;">목록으로 돌아가기</button>
</div>
""")

# 선택된 메인 지역 (기본값: 정선군)
selected_name = st.selectbox("상세 조회 지역", df["지역"].tolist(), label_visibility="collapsed")
target = df[df["지역"] == selected_name].iloc[0]

# 히어로 비주얼 + 3열 썸네일 카드
col_hero, col_sub1, col_sub2, col_sub3 = st.columns([1.5, 1, 1, 1], gap="medium")

with col_hero:
    render_html(f"""
    <div class="sub-card" style="padding:20px; height:100%; display:flex; flex-direction:column; justify-between; background:linear-gradient(180deg, #1e293b, #0f172a);">
        <div>
            <span class="hero-badge">숨은 점수 {target['점수']}점</span>
            <h2 style="margin:12px 0 6px 0; font-size:24px; color:#f8fafc;">{html.escape(target['지역'])}</h2>
            <p style="font-size:13px; color:#cbd5e1; line-height:1.5;">{html.escape(target['설명'])}</p>
        </div>
        <div style="display:flex; gap:15px; margin-top:20px; border-top:1px solid #334155; padding-top:15px; font-size:12px; color:#94a3b8;">
            <div>👨‍👩‍👧‍👦 인구<br><b style="color:white; font-size:14px;">{target['인구']}</b></div>
            <div>📐 면적<br><b style="color:white; font-size:14px;">{target['면적']}</b></div>
            <div>🍽️ 음식점<br><b style="color:white; font-size:14px;">{target['음식점수']}</b></div>
            <div>🏔️ 관광지<br><b style="color:white; font-size:14px;">{target['관광지수']}</b></div>
        </div>
    </div>
    """)

with col_sub1:
    render_html(f"""
    <div class="sub-card">
        <div style="background:#334155; height:130px; display:flex; align-items:center; justify-content:center; font-size:40px;">🍚</div>
        <div class="sub-card-body">
            <div style="font-size:11px; color:#38bdf8; font-weight:700;">대표 음식</div>
            <div class="sub-card-title">{html.escape(target['대표음식'])}</div>
            <div class="sub-card-desc">{html.escape(target['대표음식_설명'])}</div>
        </div>
    </div>
    """)

with col_sub2:
    render_html(f"""
    <div class="sub-card">
        <div style="background:#1e3a8a; height:130px; display:flex; align-items:center; justify-content:center; font-size:40px;">🌿</div>
        <div class="sub-card-body">
            <div style="font-size:11px; color:#10b981; font-weight:700;">주요 특산품</div>
            <div class="sub-card-title">{html.escape(target['주요특산품'])}</div>
            <div class="sub-card-desc">{html.escape(target['주요특산품_설명'])}</div>
        </div>
    </div>
    """)

with col_sub3:
    render_html(f"""
    <div class="sub-card">
        <div style="background:#581c87; height:130px; display:flex; align-items:center; justify-content:center; font-size:40px;">🎉</div>
        <div class="sub-card-body">
            <div style="font-size:11px; color:#a855f7; font-weight:700;">대표 축제</div>
            <div class="sub-card-title">{html.escape(target['대표축제'])}</div>
            <div class="sub-card-desc">{html.escape(target['대표축제_설명'])}</div>
        </div>
    </div>
    """)


# =========================================================
# 8. 카테고리 탭 & 맛집 카드 갤러리
# =========================================================

tab_food, tab_tour, tab_fest, tab_prod, tab_rev = st.tabs([
    "🍽️ 음식&맛집", "🏛️ 관광지", "🎉 축제&행사", "🎁 특산품", f"💬 리뷰 ({len(target['리뷰목록'])})"
])

with tab_food:
    render_html("<div style='margin:15px 0 10px 0; font-weight:700; color:#f8fafc;'>추천 맛집</div>")
    
    place_cols = st.columns(3)
    for idx, place in enumerate(target["맛집목록"]):
        with place_cols[idx % 3]:
            render_html(f"""
            <div class="place-card">
                <div style="background:#0f172a; height:120px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:36px; border:1px solid #334155;">
                    🍲
                </div>
                <div class="place-title">{html.escape(place['이름'])}</div>
                <div class="place-star">★ {place['평점']} <span style="color:#64748b; font-weight:normal;">{place['리뷰']}</span></div>
                <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">{html.escape(place['특징'])}</div>
                <div class="place-address">📍 {html.escape(place['주소'])}</div>
            </div>
            """)

with tab_tour:
    st.info("해당 지역의 인접 주요 명소 및 자연 지형 정보가 제공됩니다.")

with tab_fest:
    st.info("지역 대표 연간 축제 및 문화 행사 정보입니다.")

with tab_prod:
    st.info("로컬 직거래 및 온라인 구매 가능한 특산품 목록입니다.")

with tab_rev:
    st.info("실제 방문객들의 검증된 로컬 후기입니다.")


# =========================================================
# 9. 실제 방문객 리뷰 Card Grid
# =========================================================

render_html("""
<div class="section-head">
    <span>실제 방문객 리뷰</span>
    <span style="font-size:13px; color:#38bdf8; cursor:pointer;">전체 리뷰 보기 ></span>
</div>
""")

rev_cols = st.columns(4)
for idx, rev in enumerate(target["리뷰목록"]):
    with rev_cols[idx % 4]:
        stars = "★" * rev["평점"]
        render_html(f"""
        <div class="review-card">
            <div class="review-user">
                <div class="review-avatar">{rev['이름'][0]}</div>
                <div>
                    <div style="font-size:13px; font-weight:700; color:#f8fafc;">{html.escape(rev['이름'])}</div>
                    <div style="font-size:11px; color:#64748b;">{rev['날짜']}</div>
                </div>
            </div>
            <div style="color:#f59e0b; font-size:12px; margin-bottom:6px;">{stars}</div>
            <div class="review-text">"{html.escape(rev['내용'])}"</div>
        </div>
        """)


# =========================================================
# 10. 추천 지역 TOP 5 랭킹
# =========================================================

render_html("""
<div class="section-head">
    <span>🏆 추천 지역 TOP 5</span>
</div>
""")

top5_df = df.sort_values("점수", ascending=False).head(5)
top_cols = st.columns(5)

for idx, (_, r) in enumerate(top5_df.iterrows()):
    with top_cols[idx]:
        render_html(f"""
        <div class="top5-card">
            <div class="top5-rank">{idx+1}</div>
            <div>
                <div style="font-size:14px; font-weight:800; color:#f8fafc;">{r['지역']}</div>
                <div style="font-size:12px; color:#ef4444; font-weight:700;">{r['점수']}점</div>
            </div>
        </div>
        """)
