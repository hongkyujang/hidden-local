from pathlib import Path

app = r'''import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from urllib.parse import quote

# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. 다크모드에서도 글자가 보이도록 전체 색상 고정
# =========================================================
st.markdown("""
<style>
/* 전체 페이지 */
.stApp {
    background: #f7f8fa !important;
    color: #172033 !important;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 30px;
    padding-bottom: 50px;
}

/* 모든 기본 텍스트 */
html, body, [class*="css"], p, span, label, div {
    font-family: "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
}

/* Streamlit 기본 텍스트 색상 강제 */
.stApp p,
.stApp span,
.stApp label,
.stApp div[data-testid="stMarkdownContainer"],
.stApp div[data-testid="stText"],
.stApp div[data-testid="stCaptionContainer"] {
    color: #172033;
}

/* 제목 */
h1, h2, h3, h4 {
    color: #111827 !important;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #ffffff 0%, #eef5ff 100%);
    border: 1px solid #dce5f0;
    border-radius: 24px;
    padding: 38px 42px;
    margin-bottom: 24px;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
}

.hero-title {
    color: #111827 !important;
    font-size: 40px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 12px;
}

.hero-sub {
    color: #526176 !important;
    font-size: 17px;
    line-height: 1.8;
}

/* Metric 카드 */
div[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e1e7ef !important;
    border-radius: 18px !important;
    padding: 18px !important;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

div[data-testid="stMetricLabel"] p {
    color: #64748b !important;
}

div[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 800 !important;
}

div[data-testid="stMetricDelta"] {
    color: #64748b !important;
}

/* 섹션 */
.section-title {
    color: #111827 !important;
    font-size: 27px;
    font-weight: 800;
    margin-top: 34px;
    margin-bottom: 12px;
}

/* 카드 */
.card {
    background: #ffffff;
    border: 1px solid #e1e7ef;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
}

.card h2, .card h3 {
    color: #111827 !important;
}

.card p {
    color: #526176 !important;
}

/* 배지 */
.badge {
    display: inline-block;
    background: #edf4ff;
    color: #3159a6 !important;
    border-radius: 999px;
    padding: 6px 11px;
    margin-right: 6px;
    font-size: 13px;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] * {
    color: #172033 !important;
}

/* Selectbox / Slider */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #172033 !important;
    border-color: #cbd5e1 !important;
}

div[data-baseweb="select"] span {
    color: #172033 !important;
}

div[data-testid="stSlider"] {
    color: #172033 !important;
}

/* 버튼 */
.stButton > button {
    color: #172033 !important;
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    border-color: #4778c9 !important;
}

/* 탭 */
button[data-baseweb="tab"] {
    color: #526176 !important;
    font-weight: 700 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #1d4ed8 !important;
}

/* 입력창 */
textarea, input {
    color: #172033 !important;
    background: #ffffff !important;
}

/* 리뷰 */
.review {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 15px 5px;
    color: #172033 !important;
}

.review * {
    color: #172033 !important;
}

.small {
    color: #64748b !important;
    font-size: 13px;
}

/* 알림 */
div[data-testid="stAlert"] {
    color: #172033 !important;
}

/* 이미지 */
img {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. 이미지 URL
# =========================================================
def commons(filename):
    return "https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(filename, safe="")

IMAGE = {
    "정선": commons("Mindungsan.jpg"),
    "단양": commons("Korea-Danyang-Dodamsambong 3087-07.JPG"),
    "구례": commons("20221101 지리산.jpg"),
    "영덕": commons("영덕 대게.jpg"),
    "무주": commons("MJ-Deogyusan.jpg"),
    "서천": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?auto=format&fit=crop&w=1200&q=85",
    "의령": commons("정암루 모습.png"),
    "삼척": commons("한국의 나폴리 장호항2.jpg"),
    "산채비빔밥": commons("Sanchae Bibimbap in homemade style.jpg"),
}

# =========================================================
# 4. 지역 데이터
# =========================================================
regions = [
    ["강원도 정선군","정선",37.3806,128.6608,36500,-2.1,82,43,91,
     "곤드레밥","한식","민둥산","자연·힐링","산","정선 곤드레","정선아리랑제",
     "정선의 대표 산나물 음식입니다.","가을 억새 풍경으로 유명한 대표 명소입니다.",
     "정선을 대표하는 산나물 특산품입니다.","정선의 전통문화와 아리랑을 즐기는 축제입니다.",
     IMAGE["정선"],IMAGE["산채비빔밥"],"정선 향토음식점",
     [("방문객 A",5,"산과 음식 모두 조용히 즐기기 좋았어요.","2026.08"),
      ("방문객 B",4,"곤드레 음식이 담백하고 맛있었습니다.","2026.07")]],

    ["충청북도 단양군","단양",36.9845,128.3656,27500,-1.4,86,59,88,
     "마늘정식","한식","도담삼봉","자연·힐링","강·호수","단양 마늘","단양 온달문화축제",
     "단양 마늘을 활용한 향토 음식입니다.","남한강 위에 솟은 세 봉우리로 유명합니다.",
     "단양을 대표하는 농특산물입니다.","온달 설화를 소재로 한 지역 문화 행사입니다.",
     IMAGE["단양"],IMAGE["산채비빔밥"],"단양 마늘향토음식점",
     [("방문객 C",5,"도담삼봉 풍경이 정말 좋았습니다.","2026.08"),
      ("방문객 D",4,"마늘 음식이 다양해서 좋았어요.","2026.06")]],

    ["전라남도 구례군","구례",35.2025,127.4627,24500,-1.8,84,46,94,
     "산채정식","한식","지리산","자연·힐링","산","구례 산수유","구례 산수유꽃축제",
     "지리산 주변의 산나물을 활용한 향토 음식입니다.","구례를 대표하는 자연 관광지입니다.",
     "구례를 대표하는 봄철 특산물입니다.","산수유꽃이 피는 시기에 열리는 축제입니다.",
     IMAGE["구례"],IMAGE["산채비빔밥"],"구례 산채향토음식점",
     [("방문객 E",5,"봄에 다시 가고 싶은 곳입니다.","2026.04"),
      ("방문객 F",4,"자연 속에서 쉬기 좋았어요.","2026.03")]],

    ["경상북도 영덕군","영덕",36.4150,129.3650,33500,-2.0,90,55,90,
     "영덕대게","해산물","해맞이공원","바다·해안","바다","영덕대게","영덕대게축제",
     "영덕을 대표하는 해산물 음식입니다.","동해안 일출과 해안 경관을 감상하기 좋습니다.",
     "영덕을 대표하는 수산 특산품입니다.","대게를 주제로 한 지역 축제입니다.",
     IMAGE["영덕"],IMAGE["영덕"],"영덕 대게 향토음식점",
     [("방문객 G",5,"바다 풍경과 음식 조합이 좋았습니다.","2026.08"),
      ("방문객 H",4,"해산물 좋아하면 추천합니다.","2026.05")]],

    ["전라북도 무주군","무주",36.0060,127.6600,24000,-2.2,80,48,92,
     "어죽","한식","덕유산","자연·힐링","산","머루와인","무주 반딧불축제",
     "민물고기와 채소 등을 활용한 향토 음식입니다.","사계절 자연경관을 즐길 수 있는 명산입니다.",
     "무주의 대표적인 지역 특산품입니다.","반딧불이를 소재로 한 생태 문화 행사입니다.",
     IMAGE["무주"],IMAGE["산채비빔밥"],"무주 향토음식점",
     [("방문객 I",5,"자연 풍경이 정말 좋았습니다.","2026.07"),
      ("방문객 J",4,"조용한 여행지로 만족스러웠어요.","2026.06")]],

    ["충청남도 서천군","서천",36.0800,126.6900,49000,-1.0,79,39,87,
     "주꾸미 요리","해산물","신성리 갈대밭","자연·힐링","강·호수","서천 김","서천 동백꽃 주꾸미축제",
     "서천 앞바다의 수산물을 활용한 지역 음식입니다.","금강 주변의 넓은 갈대 풍경을 볼 수 있습니다.",
     "서천의 대표 수산 가공 특산품입니다.","주꾸미와 동백꽃을 함께 즐기는 지역 축제입니다.",
     IMAGE["서천"],IMAGE["영덕"],"서천 해산물 향토음식점",
     [("방문객 K",4,"한적하게 여행하기 좋았습니다.","2026.05"),
      ("방문객 L",5,"지역 음식이 인상적이었어요.","2026.04")]],

    ["경상남도 의령군","의령",35.3222,128.2617,26000,-1.7,83,37,93,
     "망개떡","전통음식","정암루","역사·문화","문화재","의령 망개떡","의령 홍의장군축제",
     "의령을 대표하는 전통 떡입니다.","남강과 주변 풍경을 볼 수 있는 대표 누각입니다.",
     "의령을 대표하는 전통 먹거리입니다.","의령의 역사와 문화를 체험하는 축제입니다.",
     IMAGE["의령"],IMAGE["산채비빔밥"],"의령 향토음식점",
     [("방문객 M",5,"조용하고 역사적인 분위기가 좋았습니다.","2026.06"),
      ("방문객 N",4,"망개떡이 독특했어요.","2026.05")]],

    ["강원도 삼척시","삼척",37.4400,129.1650,62000,-1.3,85,52,89,
     "곰치국","해산물","장호항","바다·해안","바다","삼척 미역","삼척 장미축제",
     "삼척의 대표적인 해산물 향토 음식입니다.","맑은 바다와 해안 풍경으로 유명합니다.",
     "동해안 지역의 대표 해조류 특산품입니다.","지역의 꽃과 문화를 즐길 수 있는 행사입니다.",
     IMAGE["삼척"],IMAGE["영덕"],"삼척 해산물 향토음식점",
     [("방문객 O",5,"바다 색깔이 정말 예뻤어요.","2026.08"),
      ("방문객 P",4,"여유롭게 둘러보기 좋았습니다.","2026.07")]],
]

columns = [
    "지역","키","위도","경도","인구","인구변화율","음식점수","관광인지도","지역특색",
    "대표음식","음식유형","관광지","관광유형","랜드마크유형","특산품","지역행사",
    "음식설명","관광설명","특산설명","행사설명","사진","음식사진","음식점","리뷰"
]

df = pd.DataFrame(regions, columns=columns)

# =========================================================
# 5. 점수 계산
# =========================================================
def hidden_score(row):
    hidden = 100 - row["관광인지도"]
    population = min(abs(row["인구변화율"]) * 5, 20)
    food = row["음식점수"] * 0.25
    local = row["지역특색"] * 0.25
    return round(hidden * 0.4 + population * 0.1 + food + local, 1)

df["숨은지역점수"] = df.apply(hidden_score, axis=1)

# =========================================================
# 6. 사이드바
# =========================================================
st.sidebar.markdown("## 🔎 지역 탐색")
st.sidebar.caption("내 취향에 맞는 숨은 지역을 찾아보세요.")

min_score = st.sidebar.slider(
    "최소 숨은지역 점수",
    0, 100, 55, 5
)

food_choice = st.sidebar.selectbox(
    "🍴 선호 음식",
    ["전체"] + sorted(df["음식유형"].unique().tolist())
)

tour_choice = st.sidebar.selectbox(
    "🏞️ 선호 관광 유형",
    ["전체"] + sorted(df["관광유형"].unique().tolist())
)

landmark_choice = st.sidebar.selectbox(
    "📍 선호 랜드마크",
    ["전체"] + sorted(df["랜드마크유형"].unique().tolist())
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗺️ 지도 표시")

show_region = st.sidebar.checkbox("📍 추천 지역", True)
show_food = st.sidebar.checkbox("🍴 대표 음식", True)
show_tour = st.sidebar.checkbox("🏞️ 관광지", True)
show_event = st.sidebar.checkbox("🎉 지역 행사", True)
show_special = st.sidebar.checkbox("🎁 특산품", True)

filtered = df[df["숨은지역점수"] >= min_score].copy()

if food_choice != "전체":
    filtered = filtered[filtered["음식유형"] == food_choice]

if tour_choice != "전체":
    filtered = filtered[filtered["관광유형"] == tour_choice]

if landmark_choice != "전체":
    filtered = filtered[filtered["랜드마크유형"] == landmark_choice]

def personal_score(row):
    score = row["숨은지역점수"]
    if food_choice != "전체" and row["음식유형"] == food_choice:
        score += 5
    if tour_choice != "전체" and row["관광유형"] == tour_choice:
        score += 5
    if landmark_choice != "전체" and row["랜드마크유형"] == landmark_choice:
        score += 5
    return round(score, 1)

filtered["개인추천점수"] = filtered.apply(personal_score, axis=1)
filtered = filtered.sort_values("개인추천점수", ascending=False)

# =========================================================
# 7. 홈페이지
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">📍 아직 발견되지 않은 대한민국</div>
    <div class="hero-sub">
        SGIS 지역 데이터를 활용해 관광 인지도가 상대적으로 낮지만<br>
        지역의 음식·관광·문화적 매력이 높은 곳을 찾아드립니다.
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

c1.metric("분석 지역", f"{len(df)}곳")
c2.metric("추천 지역", f"{len(filtered)}곳")
c3.metric("평균 숨은지역 점수", f"{df['숨은지역점수'].mean():.1f}")
c4.metric(
    "최고 추천 점수",
    f"{filtered['개인추천점수'].max():.1f}" if len(filtered) else "-"
)

# =========================================================
# 8. 지도
# =========================================================
st.markdown('<div class="section-title">🗺️ 숨은 지역 지도</div>', unsafe_allow_html=True)
st.caption("📍 빨간 지역 마커를 클릭하면 해당 지역의 상세 정보가 아래에 표시됩니다.")

if len(filtered) == 0:
    st.warning("현재 설정에 맞는 지역이 없습니다. 왼쪽 조건을 조금 낮춰보세요.")
else:
    center = [filtered["위도"].mean(), filtered["경도"].mean()]

    # CartoDB 대신 OpenStreetMap 사용
    # → API KEY REQUIRED 워터마크가 나타나지 않음
    m = folium.Map(
        location=center,
        zoom_start=7,
        tiles="OpenStreetMap",
        control_scale=True,
        width="100%",
        height=650,
    )

    # 한글 팝업
    def popup_html(row):
        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                html, body {{
                    font-family: "Malgun Gothic", "Noto Sans KR", sans-serif;
                    color: #172033;
                    background: #ffffff;
                    margin: 0;
                    padding: 10px;
                }}
                h3 {{
                    color: #111827;
                    margin: 0 0 10px 0;
                    font-size: 18px;
                }}
                p {{
                    color: #374151;
                    margin: 6px 0;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
            <h3>📍 {row["지역"]}</h3>
            <p><b>추천 점수</b> : {row["개인추천점수"]}점</p>
            <p><b>대표 음식</b> : {row["대표음식"]}</p>
            <p><b>관광지</b> : {row["관광지"]}</p>
            <p><b>특산품</b> : {row["특산품"]}</p>
        </body>
        </html>
        """

    # 카테고리 마커 위치는 MVP용 지역 중심 주변 예시 위치
    offsets = {
        "food": (0.018, 0.018),
        "tour": (-0.018, 0.018),
        "event": (0.018, -0.018),
        "special": (-0.018, -0.018),
    }

    for _, row in filtered.iterrows():

        if show_region:
            folium.Marker(
                [row["위도"], row["경도"]],
                tooltip=f"📍 {row['지역']} · {row['개인추천점수']}점",
                popup=folium.Popup(
                    popup_html(row),
                    max_width=330
                ),
                icon=folium.Icon(
                    color="red",
                    icon="map-marker",
                    prefix="fa"
                ),
            ).add_to(m)

        if show_food:
            folium.Marker(
                [
                    row["위도"] + offsets["food"][0],
                    row["경도"] + offsets["food"][1]
                ],
                tooltip=f"🍴 {row['대표음식']}",
                popup=folium.Popup(
                    f"<meta charset='UTF-8'><b>🍴 대표 음식</b><br>{row['대표음식']}<br>{row['음식설명']}",
                    max_width=300
                ),
                icon=folium.Icon(color="orange", icon="cutlery", prefix="fa"),
            ).add_to(m)

        if show_tour:
            folium.Marker(
                [
                    row["위도"] + offsets["tour"][0],
                    row["경도"] + offsets["tour"][1]
                ],
                tooltip=f"🏞️ {row['관광지']}",
                popup=folium.Popup(
                    f"<meta charset='UTF-8'><b>🏞️ 관광지</b><br>{row['관광지']}<br>{row['관광설명']}",
                    max_width=300
                ),
                icon=folium.Icon(color="green", icon="camera", prefix="fa"),
            ).add_to(m)

        if show_event:
            folium.Marker(
                [
                    row["위도"] + offsets["event"][0],
                    row["경도"] + offsets["event"][1]
                ],
                tooltip=f"🎉 {row['지역행사']}",
                popup=folium.Popup(
                    f"<meta charset='UTF-8'><b>🎉 지역 행사</b><br>{row['지역행사']}<br>{row['행사설명']}",
                    max_width=300
                ),
                icon=folium.Icon(color="purple", icon="calendar", prefix="fa"),
            ).add_to(m)

        if show_special:
            folium.Marker(
                [
                    row["위도"] + offsets["special"][0],
                    row["경도"] + offsets["special"][1]
                ],
                tooltip=f"🎁 {row['특산품']}",
                popup=folium.Popup(
                    f"<meta charset='UTF-8'><b>🎁 특산품</b><br>{row['특산품']}<br>{row['특산설명']}",
                    max_width=300
                ),
                icon=folium.Icon(color="blue", icon="gift", prefix="fa"),
            ).add_to(m)

    result = st_folium(
        m,
        width=1200,
        height=650,
        returned_objects=["last_object_clicked_tooltip"],
        key="local_map",
    )

    clicked = result.get("last_object_clicked_tooltip")

    if clicked and clicked.startswith("📍 "):
        clicked_name = clicked.split(" · ")[0].replace("📍 ", "").strip()

        if clicked_name in df["지역"].tolist():
            st.session_state["selected_region"] = clicked_name

# =========================================================
# 9. 선택 지역
# =========================================================
if "selected_region" not in st.session_state:
    if len(filtered):
        st.session_state["selected_region"] = filtered.iloc[0]["지역"]
    else:
        st.session_state["selected_region"] = df.iloc[0]["지역"]

available = filtered["지역"].tolist() if len(filtered) else df["지역"].tolist()

if st.session_state["selected_region"] not in available:
    st.session_state["selected_region"] = available[0]

selected = df[df["지역"] == st.session_state["selected_region"]].iloc[0]

st.markdown('<div class="section-title">✨ 지역 상세</div>', unsafe_allow_html=True)

left, right = st.columns([1.1, 1])

with left:
    st.image(selected["사진"], use_container_width=True)

    st.markdown(
        f"""
        <div class="card">
            <span class="badge">{selected["지역"]}</span>
            <span class="badge">{selected["관광유형"]}</span>
            <span class="badge">{selected["랜드마크유형"]}</span>
            <h2>{selected["관광지"]}</h2>
            <p>{selected["관광설명"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.metric("숨은지역 점수", f"{selected['숨은지역점수']}점")
    st.metric("관광 인지도", f"{selected['관광인지도']}점")
    st.metric("지역 특색", f"{selected['지역특색']}점")

    reasons = []

    if selected["관광인지도"] < 50:
        reasons.append("관광 인지도가 상대적으로 낮습니다.")
    if selected["음식점수"] >= 80:
        reasons.append("지역 음식 경쟁력이 높습니다.")
    if selected["지역특색"] >= 90:
        reasons.append("지역 특색이 강합니다.")

    st.markdown(
        f"""
        <div class="card">
            <b>💡 추천 이유</b>
            <p>{"<br>".join("• " + x for x in reasons)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 10. 상세 탭
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🍴 음식 & 맛집", "🏞️ 관광지", "🎉 축제/행사", "🎁 특산품", "💬 방문객 리뷰"]
)

with tab1:
    a, b = st.columns([1, 1])

    with a:
        st.image(selected["음식사진"], use_container_width=True)

    with b:
        st.markdown(f"### {selected['대표음식']}")
        st.write(selected["음식설명"])
        st.markdown(f"**추천 맛집 영역:** {selected['음식점']}")
        st.caption("※ 현재 맛집명은 MVP 예시입니다. 실제 서비스에서는 검증된 공공데이터/API를 연결하세요.")

with tab2:
    st.markdown(f"### 🏞️ {selected['관광지']}")
    st.write(selected["관광설명"])
    st.write(f"**관광 유형:** {selected['관광유형']}")
    st.write(f"**랜드마크:** {selected['랜드마크유형']}")

with tab3:
    st.markdown(f"### 🎉 {selected['지역행사']}")
    st.write(selected["행사설명"])
    st.info("※ 실제 서비스에서는 공식 지자체/관광 API를 통해 축제 일정과 개최 여부를 확인합니다.")

with tab4:
    st.markdown(f"### 🎁 {selected['특산품']}")
    st.write(selected["특산설명"])

with tab5:
    st.caption("※ 아래 리뷰는 화면 구성 확인을 위한 MVP 예시 데이터입니다.")

    for name, rating, text, date in selected["리뷰"]:
        st.markdown(
            f"""
            <div class="review">
                <b>{name}</b> &nbsp; ⭐ {rating}/5
                <br>{text}
                <br><span class="small">{date}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# 11. 여행 코스
# =========================================================
st.markdown('<div class="section-title">🧭 추천 여행 코스</div>', unsafe_allow_html=True)

course = [
    f"① {selected['관광지']} 방문",
    f"② {selected['대표음식']} 맛보기",
    f"③ {selected['특산품']} 체험/구매",
    f"④ {selected['지역행사']} 일정 확인",
]

cols = st.columns(4)

for col, item in zip(cols, course):
    with col:
        st.markdown(
            f'<div class="card"><b>{item}</b></div>',
            unsafe_allow_html=True
        )

# =========================================================
# 12. TOP 5
# =========================================================
st.markdown('<div class="section-title">🏆 숨은 지역 TOP 5</div>', unsafe_allow_html=True)

for i, (_, row) in enumerate(
    df.sort_values("숨은지역점수", ascending=False).head(5).iterrows(),
    start=1
):
    st.markdown(
        f"""
        <div class="card">
            <b>{i}. {row["지역"]}</b>
            — 숨은지역 점수 <b>{row["숨은지역점수"]}점</b>
            · 대표 음식 {row["대표음식"]}
            · 관광지 {row["관광지"]}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.caption(
    "본 화면은 SGIS 기반 창업 아이디어의 MVP입니다. "
    "현재 지역·점수·리뷰 일부는 시연용 예시이며, "
    "상용 서비스에서는 SGIS OpenAPI와 관광·지역 공공데이터를 연결합니다."
)
'''

Path("/mnt/data/app.py").write_text(app, encoding="utf-8")
Path("/mnt/data/requirements.txt").write_text(
    "streamlit>=1.36\n"
    "pandas>=2.0\n"
    "folium>=0.16\n"
    "streamlit-folium>=0.20\n",
    encoding="utf-8"
)

print("새 app.py 및 requirements.txt 생성 완료")
