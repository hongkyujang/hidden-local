import os
import html
import textwrap
import math

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
# 2. Helper 함수
# =========================================================

def render_html(content, sidebar=False):
    """HTML 들여쓰기 자동 정리 후 렌더링"""
    dedented = textwrap.dedent(content)
    if sidebar:
        st.sidebar.markdown(dedented, unsafe_allow_html=True)
    else:
        st.markdown(dedented, unsafe_allow_html=True)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def estimate_travel_time(distance_km):
    if distance_km == 0:
        return "0분"
    travel_hours = (distance_km * 1.25) / 70
    total_minutes = int(travel_hours * 60)
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if hours > 0:
        return f"약 {hours}시간 {minutes}분"
    return f"약 {minutes}분"


# =========================================================
# 3. 완벽 다크 모드 Custom CSS (상단 여백 & 제목 짤림 수정)
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

/* 상단 패딩 증가로 제목 짤림 해결 */
.block-container {
    max-width: 1400px !important;
    padding-top: 65px !important;
    padding-bottom: 60px !important;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d !important;
}

/* 헤더 타이틀 보정 */
.header-title-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-top: 5px;
}
.header-title {
    font-size: 32px;
    font-weight: 850;
    color: #f0f6fc;
    line-height: 1.3 !important;
}
.header-subtitle {
    font-size: 14px;
    color: #8b949e;
    margin-top: 4px;
}

/* 상단 지표 카드 */
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
    font-size: 24px;
    width: 46px;
    height: 46px;
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
    font-size: 20px;
    font-weight: 800;
    color: #f0f6fc;
}

/* 다크 카드 */
.dark-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 20px;
    height: 100%;
}

/* 길찾기 정보 박스 */
.route-box {
    background: #1c2128;
    border: 1px solid #388bfd;
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
}

/* 버튼 스타일 */
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

/* 탭 커스텀 */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid #30363d;
}
.stTabs [data-baseweb="tab"] {
    height: 45px;
    background-color: transparent;
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
# 4. 주요 지역 데이터
# =========================================================

START_LOCATIONS = {
    "서울특별시 (강남)": (37.4979, 127.0276),
    "서울특별시 (종로)": (37.5729, 126.9793),
    "경기도 수원시": (37.2636, 127.0286),
    "인천광역시": (37.4563, 126.7052),
    "대전광역시": (36.3504, 127.3845),
    "대구광역시": (35.8714, 128.6014),
    "부산광역시": (35.1796, 129.0756),
    "광주광역시": (35.1595, 126.8526),
    "울산광역시": (35.5384, 129.3114)
}

region_data = [
    {
        "지역": "강원도 정선군",
        "위도": 37.3806,
        "경도": 128.6608,
        "인구": "34,419명",
        "면적": "1,220.6㎢",
        "음식점수": 89,
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
            {"이름": "함백산식당", "평점": "★ 4.4 (98)", "설명": "산채정식, 더덕구이", "주소": "고한읍 고한로 123", "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=80"}
        ]
    },
    {
        "지역": "충청북도 단양군",
        "위도": 36.9845,
        "경도": 128.3657,
        "인구": "28,105명",
        "면적": "780.1㎢",
        "음식점수": 85,
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

if "selected_region" not in st.session_state:
    st.session_state.selected_region = df.iloc[0]["지역"]


# =========================================================
# 5. 사이드바
# =========================================================

with st.sidebar:
    st.markdown("<h3 style='color:#f0f6fc; margin-bottom:15px;'>🚗 길찾기 (내 위치 설정)</h3>", unsafe_allow_html=True)
    
    start_point_name = st.selectbox("내 출발 위치 선택", list(START_LOCATIONS.keys()))
    start_lat, start_lon = START_LOCATIONS[start_point_name]

    st.markdown("---")
    st.markdown("<h3 style='color:#f0f6fc; margin-bottom:15px;'>🔍 지역 탐색 필터</h3>", unsafe_allow_html=True)
    score_filter = st.slider("최소 숨은 지역 점수", 0, 100, 60)
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#8b949e; margin-top:15px;'>지도 표시 옵션</p>", unsafe_allow_html=True)
    chk_recommend = st.checkbox("추천 지역 핀", value=True)
    chk_restaurant = st.checkbox("음식점", value=True)
    chk_tour = st.checkbox("관광지", value=True)
    
    if st.button("🔄 필터 및 위치 초기화", use_container_width=True):
        st.session_state.selected_region = df.iloc[0]["지역"]


# =========================================================
# 6. 헤더 및 지표 카드
# =========================================================

render_html("""
<div class="header-title-container">
    <div>
        <div class="header-title">📍 숨은 로컬 발견</div>
        <div class="header-subtitle">대한민국 구석구석 숨은 로컬 여행지와 내 위치 기반 길찾기</div>
    </div>
</div>
""")

c1, c2, c3, c4 = st.columns(4)

selected_data = df[df["지역"] == st.session_state.selected_region].iloc[0]

dist_km = calculate_distance(start_lat, start_lon, selected_data["위도"], selected_data["경도"])
time_str = estimate_travel_time(dist_km)

with c1:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon" style="color:#2ea043;">★</div>
        <div>
            <div class="stat-label">추천 지역 수</div>
            <div class="stat-value">{len(df)}곳</div>
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
        </div>
    </div>
    """)

with c3:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon" style="color:#f85149;">📍</div>
        <div>
            <div class="stat-label">선택 지역까지 거리</div>
            <div class="stat-value">{dist_km:.1f} km</div>
        </div>
    </div>
    """)

with c4:
    render_html(f"""
    <div class="stat-card">
        <div class="stat-icon" style="color:#d29922;">🚘</div>
        <div>
            <div class="stat-label">예상 소요 시간</div>
            <div class="stat-value">{time_str}</div>
        </div>
    </div>
    """)


# =========================================================
# 7. 네이버 지도 느낌의 한반도 지도 & 길찾기 라인
# =========================================================

st.markdown("<h3 style='color:#f0f6fc; margin-top:35px; margin-bottom:15px;'>🗺️ 한반도 로컬 지도 및 길찾기</h3>", unsafe_allow_html=True)

m = folium.Map(
    location=[36.0, 127.8],
    zoom_start=7,
    tiles="https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png",
    attr="VWorld Base Map",
    max_bounds=True,
    min_lat=33.0, max_lat=38.8,
    min_lon=124.0, max_lon=132.0
)

folium.Marker(
    location=[start_lat, start_lon],
    popup=f"<b>출발지: {start_point_name}</b>",
    tooltip=f"출발지: {start_point_name}",
    icon=folium.Icon(color="blue", icon="home")
).add_to(m)

for _, row in df.iterrows():
    is_selected = row["지역"] == st.session_state.selected_region
    
    if is_selected:
        folium.PolyLine(
            locations=[[start_lat, start_lon], [row["위도"], row["경도"]]],
            color="#388bfd",
            weight=4,
            opacity=0.8,
            dash_array="8, 8"
        ).add_to(m)
    
    pin_color = "red" if is_selected else "green"
    
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=f"<b>{row['지역']}</b><br>숨은점수: {row['숨은지역점수']}점",
        tooltip=f"{row['지역']} ({row['숨은지역점수']}점)",
        icon=folium.Icon(color=pin_color, icon="star" if is_selected else "info-sign")
    ).add_to(m)

st_folium(m, use_container_width=True, height=480, returned_objects=[])


# =========================================================
# 8. 지역 상세 정보 및 내 위치 길찾기 정보
# =========================================================

col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h3 style='color:#f0f6fc;'>📍 지역 상세 정보</h3>", unsafe_allow_html=True)
with col_head2:
    selected_r_name = st.selectbox(
        "목적지 선택", 
        df["지역"].tolist(), 
        index=df["지역"].tolist().index(st.session_state.selected_region)
    )
    st.session_state.selected_region = selected_r_name

render_html(f"""
<div class="route-box">
    <span style="color:#58a6ff; font-weight:800; font-size:15px;">🛣️ Real-Time 길찾기 경로 안내</span><br>
    <div style="margin-top:6px; font-size:13px; color:#c9d1d9;">
        <b>[{start_point_name}]</b> ➔ <b>[{selected_data['지역']}]</b> 까지 
        직선/도로 추정 거리 <b style="color:#3fb950;">{dist_km:.1f} km</b> | 
        차량 기준 소요 시간 <b style="color:#d29922;">{time_str}</b>
    </div>
</div>
<div style="height:15px;"></div>
""")

mc1, mc2, mc3 = st.columns([1.2, 1, 1], gap="medium")

with mc1:
    render_html(f"""
    <div class="dark-card">
        <img src="{selected_data['메인이미지']}" style="width:100%; height:150px; object-fit:cover; border-radius:12px; margin-bottom:12px;">
        <p style="font-size:13px; color:#8b949e; line-height:1.5;">{selected_data['지역소개']}</p>
        <div style="margin-top:10px; font-size:12px; color:#8b949e;">
            <span>👥 인구: <b style="color:#f0f6fc;">{selected_data['인구']}</b></span> | 
            <span>📐 면적: <b style="color:#f0f6fc;">{selected_data['면적']}</b></span>
        </div>
    </div>
    """)

with mc2:
    render_html(f"""
    <div class="dark-card">
        <div style="font-size:12px; color:#8b949e; font-weight:700;">대표 음식</div>
        <img src="{selected_data['대표음식_img']}" style="width:100%; height:120px; object-fit:cover; border-radius:10px; margin:8px 0;">
        <div style="font-size:16px; font-weight:800; color:#f0f6fc;">{selected_data['대표음식']}</div>
        <p style="font-size:12px; color:#8b949e; margin-top:4px;">{selected_data['대표음식_설명']}</p>
    </div>
    """)

with mc3:
    render_html(f"""
    <div class="dark-card">
        <div style="font-size:12px; color:#8b949e; font-weight:700;">주요 축제</div>
        <img src="{selected_data['축제_img']}" style="width:100%; height:120px; object-fit:cover; border-radius:10px; margin:8px 0;">
        <div style="font-size:16px; font-weight:800; color:#f0f6fc;">{selected_data['축제']}</div>
        <p style="font-size:12px; color:#8b949e; margin-top:4px;">{selected_data['축제_설명']}</p>
    </div>
    """)


# =========================================================
# 9. 추천 맛집 탭 & 리뷰
# =========================================================

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
tab_food, tab_rev = st.tabs(["🍚 추천 맛집", "💬 실시간 리뷰"])

with tab_food:
    res_cols = st.columns(2)
    for idx, item in enumerate(selected_data["맛집목록"]):
        with res_cols[idx % 2]:
            render_html(f"""
            <div class="dark-card" style="display:flex; gap:15px; align-items:center;">
                <img src="{item['img']}" style="width:100px; height:80px; object-fit:cover; border-radius:10px;">
                <div>
                    <div style="font-size:15px; font-weight:800; color:#f0f6fc;">{item['이름']}</div>
                    <div style="font-size:12px; color:#d29922;">{item['평점']} - {item['설명']}</div>
                    <div style="font-size:11px; color:#6e7681; margin-top:4px;">📍 {item['주소']}</div>
                </div>
            </div>
            """)

with tab_rev:
    st.markdown("<p style='color:#8b949e;'>사용자 실시간 방문 후기 및 평점입니다.</p>", unsafe_allow_html=True)
