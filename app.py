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
# 2. Helper 함수 (HTML & 이미지 폴백)
# =========================================================

def render_html(content, sidebar=False):
    """HTML 들여쓰기 자동 정리 후 렌더링"""
    dedented = textwrap.dedent(content)
    if sidebar:
        st.sidebar.markdown(dedented, unsafe_allow_html=True)
    else:
        st.markdown(dedented, unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")

def get_img_url(filename, fallback_url):
    """로컬 이미지 파일 존재 여부 확인 후 URL 반환"""
    path = os.path.join(ASSET_DIR, filename)
    if os.path.isfile(path):
        return f"app/static/{filename}" # Streamlit static serving
    return fallback_url


# =========================================================
# 3. 완벽 다크 모드 Custom CSS
# =========================================================

render_html("""
<style>
/* 기본 배경 및 글로벌 폰트 */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], 
[data-testid="stMain"], [data-testid="stMainBlockContainer"] {
    background-color: #0e1117 !important;
    color: #c9d1d9 !important;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

[data-testid="stHeader"] {
    background-color: #0e1117 !important;
}

.block-container {
    max-width: 1400px !important;
    padding-top: 25px !important;
    padding-bottom: 60px !important;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d !important;
}

/* 헤더 타이틀 */
.header-title-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}
.header-title {
    font-size: 32px;
    font-weight: 850;
    color: #f0f6fc;
}
.header-subtitle {
    font-size: 14px;
    color: #8b949e;
    margin-top: 4px;
}

/* 4대 상단 지표 카드 */
.stat-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 15px;
}
.stat-icon {
    font-size: 26px;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: #21262d;
    display: flex;
    align-items: center;
    justify-content: center;
}
.stat-label {
    font-size: 13px;
    color: #8b949e;
    font-weight: 600;
}
.stat-value {
    font-size: 22px;
    font-weight: 800;
    color: #f0f6fc;
}
.stat-sub {
    font-size: 11px;
    color: #6e7681;
}

/* 범례 (Legend) */
.legend-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 12px;
    margin-bottom: 30px;
    font-size: 12px;
    color: #8b949e;
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

/* 카드 UI 다크 커스텀 */
.dark-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 20px;
    height: 100%;
}

/* 버튼 다크 스타일 */
.stButton > button {
    background-color: #238636 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background-color: #2ea043 !important;
}

/* 리뷰 카드 */
.review-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
}
.review-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.review-user {
    font-weight: 700;
    color: #f0f6fc;
    font-size: 14px;
}
.review-date {
    font-size: 12px;
    color: #6e7681;
}
.review-text {
    font-size: 13px;
    color: #c9d1d9;
    line-height: 1.5;
    margin-bottom: 12px;
}

/* 탭 커스텀 */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid #30363d;
}
.stTabs [data-baseweb="tab"] {
    height: 45px;
    background-color: transparent;
    border-radius: 8px 8px 0px 0px;
    color: #8b949e;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background-color: #21262d !important;
    color: #58a6ff !important;
    border-bottom: 2px solid #58a6ff !important;
}

iframe {
    border-radius: 14px !important;
}
</style>
""")


# =========================================================
# 4. 데이터 세팅 (이미지 URL 매핑 포함)
# =========================================================

region_data = [
    {
        "지역": "강원도 정선군",
        "위도": 37.3806,
        "경도": 128.6608,
        "인구": "34,419명",
        "면적": "1,220.6㎢",
        "음식점수": 89,
        "숙박업수": 120,
        "관광인지도": 46,
        "숨은지역점수": 88.7,
        "지역소개": "아리랑의 고향 정선은 아름다운 자연경관과 전통문화, 그리고 건강한 먹거리가 가득한 보석 같은 지역입니다.",
        "대표음식": "곤드레밥",
        "대표음식_설명": "정선의 대표 향토 음식으로, 건강에 좋은 곤드레나물을 넣어 지은 밥입니다.",
        "대표음식_img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80",
        "특산품": "곤드레",
        "특산품_설명": "해발 700m 고산지대에서 자란 청정한 곤드레 나물입니다.",
        "특산품_img": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=600&q=80",
        "축제": "정선 아리랑제",
        "축제_설명": "정선아리랑을 주제로 한 전통 문화 축제입니다.",
        "축제_img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80",
        "메인이미지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1000&q=80",
        "맛집목록": [
            {"이름": "정선곤드레본가", "평점": "★ 4.6 (126)", "설명": "곤드레밥 전문점", "주소": "정선읍 5일장길 31", "img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80"},
            {"이름": "함백산식당", "평점": "★ 4.4 (98)", "설명": "산채정식, 더덕구이", "주소": "고한읍 고한로 123", "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=80"},
            {"이름": "정선아리랑시장 맛집", "평점": "★ 4.5 (87)", "설명": "다양한 전통시장 먹거리", "주소": "정선읍 봉양3길 322", "img": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80"}
        ]
    },
    {
        "지역": "충청북도 단양군",
        "위도": 36.9845,
        "경도": 128.3657,
        "인구": "28,105명",
        "면적": "780.1㎢",
        "음식점수": 85,
        "숙박업수": 95,
        "관광인지도": 52,
        "숨은지역점수": 84.2,
        "지역소개": "단양팔경의 수려한 자연경관과 마늘 특산 요리가 어우러진 휴양 도시입니다.",
        "대표음식": "마늘떡갈비",
        "대표음식_설명": "단양 특산물인 육쪽마늘을 더해 깊은 풍미를 자랑하는 떡갈비입니다.",
        "대표음식_img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80",
        "특산품": "단양 마늘",
        "특산품_설명": "단단하고 향이 강해 전국 최고의 품질을 자랑하는 마늘입니다.",
        "특산품_img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80",
        "축제": "단양 마늘축제",
        "축제_설명": "단양 마늘과 로컬 먹거리를 만끽하는 여름 축제입니다.",
        "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
        "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
        "맛집목록": [
            {"이름": "단양마늘원조집", "평점": "★ 4.7 (150)", "설명": "마늘떡갈비 전문", "주소": "단양읍 중앙로 15", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&q=80"}
        ]
    },
    {
        "지역": "전라남도 구례군",
        "위도": 35.2025,
        "경도": 127.4628,
        "인구": "24,800명",
        "면적": "429.8㎢",
        "음식점수": 88,
        "숙박업수": 80,
        "관광인지도": 41,
        "숨은지역점수": 87.3,
        "지역소개": "지리산 자락 청정 자연 속에서 산수유와 산채 요리를 만나볼 수 있는 구례입니다.",
        "대표음식": "산채비빔밥",
        "대표음식_설명": "지리산의 신선한 나물들이 가득한 구례 고유의 건강 비빔밥입니다.",
        "대표음식_img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
        "특산품": "산수유",
        "특산품_설명": "봄을 알리는 붉은 보석, 구례 산수유 열매입니다.",
        "특산품_img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
        "축제": "구례 산수유꽃축제",
        "축제_설명": "노란 산수유 꽃물결을 감상하는 대표 봄축제입니다.",
        "축제_img": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80",
        "메인이미지": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1000&q=80",
        "맛집목록": [
            {"이름": "지리산산채식당", "평점": "★ 4.8 (210)", "설명": "산채정식 전문", "주소": "구례군 마산면 88", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=400&q=80"}
        ]
    }
]

df = pd.DataFrame(region_data)

# 세션 상태 선택 지역 초기화
if "selected_region" not in st.session_state:
    st.session_state.selected_region = df.iloc[0]["지역"]


# =========================================================
# 5. 사이드바 (지역 탐색 필터)
# =========================================================

with st.sidebar:
    st.markdown("<h3 style='color:#f0f6fc; margin-bottom:15px;'>🔍 지역 탐색 필터</h3>", unsafe_allow_html=True)
    
    score_filter = st.slider("최소 숨은 지역 점수", 0, 100, 60)
    
    food_type = st.selectbox("선호 음식 타입", ["전체", "한식/향토음식", "해산물", "육류"])
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#8b949e; margin-top:20px;'>지도 표시 옵션</p>", unsafe_allow_html=True)
    chk_recommend = st.checkbox("추천 지역 핀", value=True)
    chk_restaurant = st.checkbox("음식점", value=True)
    chk_tour = st.checkbox("관광지", value=True)
    chk_festival = st.checkbox("축제/행사", value=True)
    chk_special = st.checkbox("특산품", value=True)
    
    sort_by = st.selectbox("정렬 기준", ["숨은 지역 점수 순", "인기 순", "음식점수 순"])
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#8b949e; margin-top:20px;'>키워드 검색</p>", unsafe_allow_html=True)
    search_keyword = st.text_input("지역명 또는 키워드 입력", placeholder="예: 정선, 곤드레")
    
    if st.button("검색 실행", use_container_width=True):
        pass
    if st.button("🔄 필터 초기화", use_container_width=True):
        st.session_state.selected_region = df.iloc[0]["지역"]


# =========================================================
# 6. 메인 헤더 & 상단 4대 지표 카드
# =========================================================

render_html("""
<div class="header-title-container">
    <div>
        <div class="header-title">📍 숨은 로컬 발견</div>
        <div class="header-subtitle">데이터로 발견하는 대한민국의 숨은 지역과 로컬 경험</div>
    </div>
    <div style="background:#161b22; border:1px solid #30363d; padding:8px 16px; border-radius:20px; font-size:13px; color:#f0f6fc;">
        ❤️ 찜한 지역 <b style="color:#f85149;">0</b>
    </div>
</div>
""")

c1, c2, c3, c4 = st.columns(4)

with c1:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon" style="color:#2ea043;">★</div>
        <div>
            <div class="stat-label">추천 지역 수</div>
            <div class="stat-value">{len(df)}곳</div>
            <div class="stat-sub">조건에 맞는 지역</div>
        </div>
    </div>
    """)

with c2:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon" style="color:#58a6ff;">📈</div>
        <div>
            <div class="stat-label">평균 숨은 점수</div>
            <div class="stat-value">{df['숨은지역점수'].mean():.1f}점</div>
            <div class="stat-sub">상위 30% 지역</div>
        </div>
    </div>
    """)

with c3:
    render_html("""
    <div class="stat-card">
        <div class="stat-icon" style="color:#a371f7;">💬</div>
        <div>
            <div class="stat-label">리뷰 수</div>
            <div class="stat-value">237개</div>
            <div class="stat-sub">실제 방문객 리뷰</div>
        </div>
    </div>
    """)

with c4:
    render_html("""
    <div class="stat-card">
        <div class="stat-icon" style="color:#d29922;">🎁</div>
        <div>
            <div class="stat-label">특산품</div>
            <div class="stat-value">32개</div>
            <div class="stat-sub">지역 특산품</div>
        </div>
    </div>
    """)


# =========================================================
# 7. 추천 지역 지도 (CartoDB Dark Matter 적용)
# =========================================================

st.markdown("<h3 style='color:#f0f6fc; margin-top:35px; margin-bottom:15px;'>🗺️ 추천 지역 지도</h3>", unsafe_allow_html=True)

# CartoDB Dark Matter 지도 타일
m = folium.Map(
    location=[36.3, 127.8],
    zoom_start=7,
    tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attr="CartoDB Dark Matter"
)

for _, row in df.iterrows():
    popup_html = f"""
    <div style="width:200px; font-family:sans-serif; color:#111;">
        <h4 style="margin:0 0 5px 0; color:#238636;">{row['지역']}</h4>
        <p style="margin:0; font-size:12px;"><b>⭐ 숨은 점수:</b> {row['숨은지역점수']}점</p>
        <p style="margin:0; font-size:12px;"><b>🍚 대표음식:</b> {row['대표음식']}</p>
        <p style="margin:0; font-size:12px;"><b>🏔️ 주요관광:</b> {row['축제']}</p>
    </div>
    """
    
    # 점수별 핀 색상 연동
    pin_color = "green" if row['숨은지역점수'] >= 88 else "orange" if row['숨은지역점수'] >= 85 else "blue"
    
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"{row['지역']} ({row['숨은지역점수']}점)",
        icon=folium.Icon(color=pin_color, icon="info-sign")
    ).add_to(m)

st_folium(m, use_container_width=True, height=450, returned_objects=[])

# 지도 하단 범례
render_html("""
<div class="legend-container">
    <div class="legend-item"><div class="legend-dot" style="background:#238636;"></div> 숨은 점수 90점 이상</div>
    <div class="legend-item"><div class="legend-dot" style="background:#d29922;"></div> 80~90점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#1f6beb;"></div> 70~80점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#8957e5;"></div> 60~70점</div>
    <div class="legend-item"><div class="legend-dot" style="background:#6e7681;"></div> 60점 이하</div>
</div>
""")


# =========================================================
# 8. 지역 상세 정보 (3열 메인 카드 + 탭 구성)
# =========================================================

selected_data = df[df["지역"] == st.session_state.selected_region].iloc[0]

col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown("<h3 style='color:#f0f6fc;'>📍 지역 상세 정보</h3>", unsafe_allow_html=True)
with col_head2:
    selected_r_name = st.selectbox("지역 바로 선택", df["지역"].tolist(), index=df["지역"].tolist().index(st.session_state.selected_region))
    st.session_state.selected_region = selected_r_name

# --- 3개 메인 대표 카드 ---
mc1, mc2, mc3 = st.columns([1.2, 1, 1], gap="medium")

with mc1:
    render_html(f"""
    <div class="dark-card" style="position:relative; overflow:hidden;">
        <div style="position:absolute; top:15px; right:15px; background:#f85149; color:#fff; font-weight:800; font-size:12px; padding:4px 10px; border-radius:12px;">
            숨은 점수 {selected_data['숨은지역점수']}점
        </div>
        <img src="{selected_data['메인이미지']}" style="width:100%; height:160px; object-fit:cover; border-radius:12px; margin-bottom:12px;">
        <p style="font-size:13px; color:#8b949e; line-height:1.5;">{selected_data['지역소개']}</p>
        <div style="display:flex; justify-content:space-between; margin-top:15px; border-top:1px solid #30363d; padding-top:10px; font-size:12px; color:#8b949e;">
            <span>👥 인구: <b style="color:#f0f6fc;">{selected_data['인구']}</b></span>
            <span>📐 면적: <b style="color:#f0f6fc;">{selected_data['면적']}</b></span>
            <span>🍽️ 음식점: <b style="color:#f0f6fc;">{selected_data['음식점수']}개</b></span>
        </div>
    </div>
    """)

with mc2:
    render_html(f"""
    <div class="dark-card">
        <div style="font-size:12px; color:#8b949e; font-weight:700;">대표 음식</div>
        <img src="{selected_data['대표음식_img']}" style="width:100%; height:130px; object-fit:cover; border-radius:10px; margin:8px 0;">
        <div style="font-size:18px; font-weight:800; color:#f0f6fc;">{selected_data['대표음식']}</div>
        <p style="font-size:12px; color:#8b949e; margin-top:4px;">{selected_data['대표음식_설명']}</p>
    </div>
    """)

with mc3:
    render_html(f"""
    <div class="dark-card">
        <div style="font-size:12px; color:#8b949e; font-weight:700;">주요 특산품</div>
        <img src="{selected_data['특산품_img']}" style="width:100%; height:130px; object-fit:cover; border-radius:10px; margin:8px 0;">
        <div style="font-size:18px; font-weight:800; color:#f0f6fc;">{selected_data['특산품']}</div>
        <p style="font-size:12px; color:#8b949e; margin-top:4px;">{selected_data['특산품_설명']}</p>
    </div>
    """)

st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)


# --- 상세 탭 (음식&맛집, 관광지, 축제&행사, 특산품, 리뷰) ---
tab_food, tab_tour, tab_fest, tab_spec, tab_rev = st.tabs(["🍚 음식 & 맛집", "🏔️ 관광지", "🎉 축제 & 행사", "🎁 특산품", "💬 리뷰 (32)"])

with tab_food:
    st.markdown("<h4 style='color:#f0f6fc; margin-bottom:15px;'>추천 맛집</h4>", unsafe_allow_html=True)
    res_cols = st.columns(3)
    for idx, item in enumerate(selected_data["맛집목록"]):
        with res_cols[idx % 3]:
            render_html(f"""
            <div class="dark-card">
                <img src="{item['img']}" style="width:100%; height:120px; object-fit:cover; border-radius:10px;">
                <div style="font-size:16px; font-weight:800; color:#f0f6fc; margin-top:10px;">{item['이름']}</div>
                <div style="font-size:12px; color:#d29922; margin-top:2px;">{item['평점']}</div>
                <div style="font-size:12px; color:#8b949e; margin-top:4px;">{item['설명']}</div>
                <div style="font-size:11px; color:#6e7681; margin-top:2px;">📍 {item['주소']}</div>
            </div>
            """)

with tab_tour:
    st.info(f"{selected_data['지역']}의 아름다운 대표 관광지 리스트를 준비 중입니다.")

with tab_fest:
    render_html(f"""
    <div class="dark-card" style="display:flex; gap:20px; align-items:center;">
        <img src="{selected_data['축제_img']}" style="width:200px; height:120px; object-fit:cover; border-radius:10px;">
        <div>
            <h3 style="color:#f0f6fc; margin:0;">🎉 {selected_data['축제']}</h3>
            <p style="color:#8b949e; font-size:14px; margin-top:8px;">{selected_data['축제_설명']}</p>
        </div>
    </div>
    """)

with tab_spec:
    render_html(f"""
    <div class="dark-card" style="display:flex; gap:20px; align-items:center;">
        <img src="{selected_data['특산품_img']}" style="width:200px; height:120px; object-fit:cover; border-radius:10px;">
        <div>
            <h3 style="color:#f0f6fc; margin:0;">🎁 {selected_data['특산품']}</h3>
            <p style="color:#8b949e; font-size:14px; margin-top:8px;">{selected_data['특산품_설명']}</p>
        </div>
    </div>
    """)

with tab_rev:
    st.markdown("<p style='color:#8b949e;'>사용자 실시간 방문 후기입니다.</p>", unsafe_allow_html=True)


# =========================================================
# 9. 실제 방문객 리뷰 세션
# =========================================================

st.markdown("<h3 style='color:#f0f6fc; margin-top:40px; margin-bottom:15px;'>💬 실제 방문객 리뷰</h3>", unsafe_allow_html=True)

rev_cols = st.columns(4)

reviews = [
    {"user": "여행좋아", "date": "2026.05.12", "text": "자연경관이 정말 아름답고 음식도 건강하고 맛있었어요! 곤드레밥 꼭 드셔보세요.", "stars": "★★★★★"},
    {"user": "산책러버", "date": "2026.04.28", "text": "전통시장 구경도 재미있고 5일장도 꼭 가보세요. 지역분들도 친절해요!", "stars": "★★★★★"},
    {"user": "맛집탐방가", "date": "2026.04.15", "text": "조용하고 깨끗해서 힐링하기 좋아요. 지방은 역시 먹거리가 최고!", "stars": "★★★★☆"},
    {"user": "캠핑가는부자", "date": "2026.03.10", "text": "억새밭은 가을에 꼭 가보세요. 풍경이 정말 장관입니다.", "stars": "★★★★★"}
]

for idx, r in enumerate(reviews):
    with rev_cols[idx]:
        render_html(f"""
        <div class="review-card">
            <div class="review-header">
                <span class="review-user">👤 {r['user']}</span>
                <span class="review-date">{r['date']}</span>
            </div>
            <div style="color:#d29922; font-size:12px; margin-bottom:6px;">{r['stars']}</div>
            <div class="review-text">"{r['text']}"</div>
            <div style="font-size:11px; color:#6e7681; display:flex; gap:10px;">
                <span>👍 좋아요 12</span>
                <span>💬 답글 2</span>
            </div>
        </div>
        """)


# =========================================================
# 10. 추천 지역 TOP 5 카드 세션
# =========================================================

st.markdown("<h3 style='color:#f0f6fc; margin-top:40px; margin-bottom:15px;'>🏆 추천 지역 TOP 5</h3>", unsafe_allow_html=True)

top_cols = st.columns(5)

for rank, (_, row) in enumerate(df.iterrows(), start=1):
    if rank > 5:
        break
    with top_cols[rank - 1]:
        render_html(f"""
        <div class="dark-card" style="padding:12px; text-align:center;">
            <div style="font-size:12px; font-weight:800; color:#58a6ff; margin-bottom:6px;">
                <span style="background:#21262d; padding:2px 8px; border-radius:10px;">{rank}</span> {row['지역']}
            </div>
            <img src="{row['메인이미지']}" style="width:100%; height:90px; object-fit:cover; border-radius:8px;">
            <div style="font-size:12px; font-weight:800; color:#3fb950; margin-top:8px;">
                {row['숨은지역점수']}점
            </div>
            <div style="font-size:11px; color:#8b949e; margin-top:2px;">
                {row['대표음식']}
            </div>
        </div>
        """)
