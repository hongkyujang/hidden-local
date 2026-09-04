import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from urllib.parse import quote

# -------------------------------------------------
# 기본 설정
# -------------------------------------------------
st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# CSS
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Noto Sans KR", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 34px 38px;
    border-radius: 24px;
    background: linear-gradient(135deg, #f7f9fc 0%, #eef5ff 100%);
    border: 1px solid #e5eaf2;
    margin-bottom: 24px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.25;
    margin: 0 0 10px 0;
}

.hero-sub {
    font-size: 17px;
    color: #64748b;
    line-height: 1.7;
    margin: 0;
}

.card {
    background: white;
    border: 1px solid #e8edf3;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    margin: 28px 0 14px 0;
}

.small {
    color: #64748b;
    font-size: 14px;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #eef4ff;
    color: #3159a6;
    font-size: 13px;
    font-weight: 700;
    margin-right: 5px;
}

.review {
    padding: 15px 0;
    border-bottom: 1px solid #edf0f4;
}

.review:last-child {
    border-bottom: none;
}

.stButton button {
    border-radius: 10px;
    font-weight: 700;
}

[data-testid="stMetric"] {
    background: #fff;
    border: 1px solid #e8edf3;
    border-radius: 16px;
    padding: 12px;
}

img {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 이미지 URL
# Wikimedia 파일명은 quote()로 안전하게 인코딩
# -------------------------------------------------
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

# -------------------------------------------------
# 데이터
# 실제 서비스에서는 SGIS + 관광/지역 API로 교체
# -------------------------------------------------
regions = [
    {
        "지역":"강원도 정선군", "키":"정선", "위도":37.3806, "경도":128.6608,
        "인구":36500, "인구변화율":-2.1, "음식점수":82, "관광인지도":43, "지역특색":91,
        "대표음식":"곤드레밥", "음식유형":"한식",
        "관광지":"민둥산", "관광유형":"자연·힐링", "랜드마크유형":"산",
        "특산품":"정선 곤드레", "지역행사":"정선아리랑제",
        "음식설명":"정선의 대표 산나물인 곤드레를 활용한 향토 음식입니다.",
        "관광설명":"가을 억새 풍경으로 특히 유명한 정선의 대표 산입니다.",
        "특산설명":"정선 지역의 대표적인 산나물 특산품입니다.",
        "행사설명":"정선의 전통문화와 아리랑을 즐길 수 있는 지역 축제입니다.",
        "사진":IMAGE["정선"], "음식사진":IMAGE["산채비빔밥"],
        "음식점":"정선 향토음식점", "리뷰":[
            ("방문객 A",5,"산과 음식 모두 조용히 즐기기 좋았어요.","2026.08"),
            ("방문객 B",4,"곤드레 음식이 생각보다 담백하고 맛있었습니다.","2026.07")
        ]
    },
    {
        "지역":"충청북도 단양군", "키":"단양", "위도":36.9845, "경도":128.3656,
        "인구":27500, "인구변화율":-1.4, "음식점수":86, "관광인지도":59, "지역특색":88,
        "대표음식":"마늘정식", "음식유형":"한식",
        "관광지":"도담삼봉", "관광유형":"자연·힐링", "랜드마크유형":"강·호수",
        "특산품":"단양 마늘", "지역행사":"단양 온달문화축제",
        "음식설명":"단양 마늘을 활용한 다양한 향토 요리를 맛볼 수 있습니다.",
        "관광설명":"남한강 위에 솟은 세 봉우리로 단양의 대표 경관입니다.",
        "특산설명":"단양의 대표 농특산물로 향과 저장성이 좋은 것으로 알려져 있습니다.",
        "행사설명":"온달 설화를 소재로 한 지역 문화 행사입니다.",
        "사진":IMAGE["단양"], "음식사진":IMAGE["산채비빔밥"],
        "음식점":"단양 마늘향토음식점", "리뷰":[
            ("방문객 C",5,"도담삼봉 풍경이 정말 좋았습니다.","2026.08"),
            ("방문객 D",4,"마늘 음식이 다양해서 좋았어요.","2026.06")
        ]
    },
    {
        "지역":"전라남도 구례군", "키":"구례", "위도":35.2025, "경도":127.4627,
        "인구":24500, "인구변화율":-1.8, "음식점수":84, "관광인지도":46, "지역특색":94,
        "대표음식":"산채정식", "음식유형":"한식",
        "관광지":"지리산", "관광유형":"자연·힐링", "랜드마크유형":"산",
        "특산품":"구례 산수유", "지역행사":"구례 산수유꽃축제",
        "음식설명":"지리산 주변의 다양한 산나물을 활용한 향토 음식입니다.",
        "관광설명":"구례를 대표하는 자연 관광지로 다양한 탐방 코스가 있습니다.",
        "특산설명":"구례를 대표하는 봄철 특산물입니다.",
        "행사설명":"산수유꽃이 피는 시기에 열리는 대표적인 지역 축제입니다.",
        "사진":IMAGE["구례"], "음식사진":IMAGE["산채비빔밥"],
        "음식점":"구례 산채향토음식점", "리뷰":[
            ("방문객 E",5,"봄에 다시 가고 싶은 곳입니다.","2026.04"),
            ("방문객 F",4,"자연 속에서 쉬기 좋았어요.","2026.03")
        ]
    },
    {
        "지역":"경상북도 영덕군", "키":"영덕", "위도":36.4150, "경도":129.3650,
        "인구":33500, "인구변화율":-2.0, "음식점수":90, "관광인지도":55, "지역특색":90,
        "대표음식":"영덕대게", "음식유형":"해산물",
        "관광지":"해맞이공원", "관광유형":"바다·해안", "랜드마크유형":"바다",
        "특산품":"영덕대게", "지역행사":"영덕대게축제",
        "음식설명":"영덕을 대표하는 해산물 음식입니다.",
        "관광설명":"동해안의 일출과 해안 경관을 감상하기 좋은 곳입니다.",
        "특산설명":"영덕을 대표하는 수산 특산품입니다.",
        "행사설명":"대게를 주제로 지역의 음식과 문화를 체험할 수 있는 행사입니다.",
        "사진":IMAGE["영덕"], "음식사진":IMAGE["영덕"],
        "음식점":"영덕 대게 향토음식점", "리뷰":[
            ("방문객 G",5,"바다 풍경과 음식 조합이 좋았습니다.","2026.08"),
            ("방문객 H",4,"해산물 좋아하면 추천합니다.","2026.05")
        ]
    },
    {
        "지역":"전라북도 무주군", "키":"무주", "위도":36.0060, "경도":127.6600,
        "인구":24000, "인구변화율":-2.2, "음식점수":80, "관광인지도":48, "지역특색":92,
        "대표음식":"어죽", "음식유형":"한식",
        "관광지":"덕유산", "관광유형":"자연·힐링", "랜드마크유형":"산",
        "특산품":"머루와인", "지역행사":"무주 반딧불축제",
        "음식설명":"민물고기와 채소 등을 활용한 무주의 향토 음식입니다.",
        "관광설명":"사계절 자연경관과 산행을 즐길 수 있는 대표 명산입니다.",
        "특산설명":"무주의 대표적인 지역 특산품 가운데 하나입니다.",
        "행사설명":"반딧불이를 소재로 자연과 생태를 체험하는 지역 행사입니다.",
        "사진":IMAGE["무주"], "음식사진":IMAGE["산채비빔밥"],
        "음식점":"무주 향토음식점", "리뷰":[
            ("방문객 I",5,"자연 풍경이 정말 좋았습니다.","2026.07"),
            ("방문객 J",4,"조용한 여행지로 만족스러웠어요.","2026.06")
        ]
    },
    {
        "지역":"충청남도 서천군", "키":"서천", "위도":36.0800, "경도":126.6900,
        "인구":49000, "인구변화율":-1.0, "음식점수":79, "관광인지도":39, "지역특색":87,
        "대표음식":"주꾸미 요리", "음식유형":"해산물",
        "관광지":"신성리 갈대밭", "관광유형":"자연·힐링", "랜드마크유형":"강·호수",
        "특산품":"서천 김", "지역행사":"서천 동백꽃 주꾸미축제",
        "음식설명":"서천 앞바다에서 나는 수산물을 활용한 지역 음식입니다.",
        "관광설명":"금강 주변의 넓은 갈대 풍경을 볼 수 있는 명소입니다.",
        "특산설명":"서천의 대표 수산 가공 특산품입니다.",
        "행사설명":"봄철 주꾸미와 동백꽃을 함께 즐길 수 있는 지역 축제입니다.",
        "사진":IMAGE["서천"], "음식사진":IMAGE["영덕"],
        "음식점":"서천 해산물 향토음식점", "리뷰":[
            ("방문객 K",4,"한적하게 여행하기 좋았습니다.","2026.05"),
            ("방문객 L",5,"지역 음식이 인상적이었어요.","2026.04")
        ]
    },
    {
        "지역":"경상남도 의령군", "키":"의령", "위도":35.3222, "경도":128.2617,
        "인구":26000, "인구변화율":-1.7, "음식점수":83, "관광인지도":37, "지역특색":93,
        "대표음식":"망개떡", "음식유형":"전통음식",
        "관광지":"정암루", "관광유형":"역사·문화", "랜드마크유형":"문화재",
        "특산품":"의령 망개떡", "지역행사":"의령 홍의장군축제",
        "음식설명":"의령을 대표하는 전통 떡입니다.",
        "관광설명":"남강과 주변 풍경을 바라볼 수 있는 의령의 대표 누각입니다.",
        "특산설명":"의령을 대표하는 전통 먹거리입니다.",
        "행사설명":"의령의 역사와 문화를 체험하는 지역 축제입니다.",
        "사진":IMAGE["의령"], "음식사진":IMAGE["산채비빔밥"],
        "음식점":"의령 향토음식점", "리뷰":[
            ("방문객 M",5,"조용하고 역사적인 분위기가 좋았습니다.","2026.06"),
            ("방문객 N",4,"망개떡이 독특했어요.","2026.05")
        ]
    },
    {
        "지역":"강원도 삼척시", "키":"삼척", "위도":37.4400, "경도":129.1650,
        "인구":62000, "인구변화율":-1.3, "음식점수":85, "관광인지도":52, "지역특색":89,
        "대표음식":"곰치국", "음식유형":"해산물",
        "관광지":"장호항", "관광유형":"바다·해안", "랜드마크유형":"바다",
        "특산품":"삼척 미역", "지역행사":"삼척 장미축제",
        "음식설명":"삼척의 대표적인 해산물 향토 음식입니다.",
        "관광설명":"맑은 바다와 해안 풍경으로 유명한 삼척의 명소입니다.",
        "특산설명":"동해안 지역의 대표적인 해조류 특산품입니다.",
        "행사설명":"지역의 꽃과 문화를 함께 즐길 수 있는 행사입니다.",
        "사진":IMAGE["삼척"], "음식사진":IMAGE["영덕"],
        "음식점":"삼척 해산물 향토음식점", "리뷰":[
            ("방문객 O",5,"바다 색깔이 정말 예뻤어요.","2026.08"),
            ("방문객 P",4,"여유롭게 둘러보기 좋았습니다.","2026.07")
        ]
    },
]

df = pd.DataFrame(regions)

# -------------------------------------------------
# 점수
# -------------------------------------------------
def hidden_score(row):
    hidden = 100 - row["관광인지도"]
    pop = min(abs(row["인구변화율"]) * 5, 20)
    food = row["음식점수"] * 0.25
    local = row["지역특색"] * 0.25
    return round(hidden * 0.4 + pop * 0.1 + food + local, 1)

df["숨은지역점수"] = df.apply(hidden_score, axis=1)

# -------------------------------------------------
# 사이드바
# -------------------------------------------------
st.sidebar.title("🔎 지역 탐색 설정")
st.sidebar.caption("나에게 맞는 숨은 지역을 찾아보세요.")

min_score = st.sidebar.slider(
    "최소 숨은지역 점수",
    min_value=0,
    max_value=100,
    value=55,
    step=5,
)

food_options = ["전체"] + sorted(df["음식유형"].unique().tolist())
tour_options = ["전체"] + sorted(df["관광유형"].unique().tolist())
landmark_options = ["전체"] + sorted(df["랜드마크유형"].unique().tolist())

food_choice = st.sidebar.selectbox("🍴 선호 음식", food_options)
tour_choice = st.sidebar.selectbox("🏞️ 선호 관광 유형", tour_options)
landmark_choice = st.sidebar.selectbox("📍 선호 랜드마크", landmark_options)

st.sidebar.markdown("---")
st.sidebar.subheader("🗺️ 지도 표시")

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

# 개인화 점수
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

# -------------------------------------------------
# 헤더
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">📍 아직 발견되지 않은 대한민국</div>
    <p class="hero-sub">
        SGIS 지역 데이터를 활용해 관광 인지도가 상대적으로 낮지만<br>
        지역의 음식·관광·문화적 매력이 높은 곳을 찾아드립니다.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("분석 지역", f"{len(df)}곳")
c2.metric("추천 지역", f"{len(filtered)}곳")
c3.metric("평균 숨은지역 점수", f"{df['숨은지역점수'].mean():.1f}")
c4.metric("최고 추천 점수", f"{filtered['개인추천점수'].max():.1f}" if len(filtered) else "-")

# -------------------------------------------------
# 지도
# -------------------------------------------------
st.markdown('<div class="section-title">🗺️ 숨은 지역 지도</div>', unsafe_allow_html=True)
st.caption("지도에서 📍 지역 마커를 클릭하면 아래 상세 정보가 해당 지역으로 바뀝니다.")

if len(filtered) == 0:
    st.warning("현재 설정에 맞는 지역이 없습니다. 왼쪽 조건을 조금 낮춰보세요.")
else:
    center_lat = filtered["위도"].mean()
    center_lon = filtered["경도"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        control_scale=True,
        tiles="CartoDB positron",
    )

    # UTF-8을 명시한 팝업
    def popup_html(row):
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: "Malgun Gothic", "Noto Sans KR", sans-serif;
                    width: 260px;
                    margin: 0;
                    padding: 8px;
                    word-break: keep-all;
                }}
                h3 {{ margin: 4px 0 8px; }}
                p {{ margin: 5px 0; line-height: 1.5; }}
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

    for _, row in filtered.iterrows():
        if show_region:
            folium.Marker(
                location=[row["위도"], row["경도"]],
                tooltip=f"📍 {row['지역']} · {row['개인추천점수']}점",
                popup=folium.Popup(popup_html(row), max_width=330),
                icon=folium.Icon(color="red", icon="map-marker", prefix="fa"),
            ).add_to(m)

        # 실제 위치가 아닌 '지역 대표 위치 주변'의 예시 마커임을 명확히 함
        offsets = {
            "food": (0.018, 0.018),
            "tour": (-0.018, 0.018),
            "event": (0.018, -0.018),
            "special": (-0.018, -0.018),
        }

        if show_food:
            folium.Marker(
                location=[row["위도"] + offsets["food"][0], row["경도"] + offsets["food"][1]],
                tooltip=f"🍴 {row['대표음식']}",
                popup=folium.Popup(f"<meta charset='utf-8'><b>🍴 대표 음식</b><br>{row['대표음식']}<br>{row['음식설명']}", max_width=300),
                icon=folium.Icon(color="orange", icon="cutlery", prefix="fa"),
            ).add_to(m)

        if show_tour:
            folium.Marker(
                location=[row["위도"] + offsets["tour"][0], row["경도"] + offsets["tour"][1]],
                tooltip=f"🏞️ {row['관광지']}",
                popup=folium.Popup(f"<meta charset='utf-8'><b>🏞️ 관광지</b><br>{row['관광지']}<br>{row['관광설명']}", max_width=300),
                icon=folium.Icon(color="green", icon="camera", prefix="fa"),
            ).add_to(m)

        if show_event:
            folium.Marker(
                location=[row["위도"] + offsets["event"][0], row["경도"] + offsets["event"][1]],
                tooltip=f"🎉 {row['지역행사']}",
                popup=folium.Popup(f"<meta charset='utf-8'><b>🎉 지역 행사</b><br>{row['지역행사']}<br>{row['행사설명']}", max_width=300),
                icon=folium.Icon(color="purple", icon="calendar", prefix="fa"),
            ).add_to(m)

        if show_special:
            folium.Marker(
                location=[row["위도"] + offsets["special"][0], row["경도"] + offsets["special"][1]],
                tooltip=f"🎁 {row['특산품']}",
                popup=folium.Popup(f"<meta charset='utf-8'><b>🎁 특산품</b><br>{row['특산품']}<br>{row['특산설명']}", max_width=300),
                icon=folium.Icon(color="blue", icon="gift", prefix="fa"),
            ).add_to(m)

    map_result = st_folium(
        m,
        width=1200,
        height=650,
        returned_objects=["last_object_clicked_tooltip"],
        key="local_map",
    )

    # 클릭한 지역 저장
    clicked = map_result.get("last_object_clicked_tooltip")
    if clicked and clicked.startswith("📍 "):
        clicked_name = clicked.split(" · ")[0].replace("📍 ", "").strip()
        if clicked_name in df["지역"].tolist():
            st.session_state["selected_region"] = clicked_name

# -------------------------------------------------
# 상세 지역
# -------------------------------------------------
if "selected_region" not in st.session_state:
    st.session_state["selected_region"] = filtered.iloc[0]["지역"] if len(filtered) else df.iloc[0]["지역"]

available_names = filtered["지역"].tolist()
if not available_names:
    available_names = df["지역"].tolist()

if st.session_state["selected_region"] not in available_names:
    st.session_state["selected_region"] = available_names[0]

selected = df[df["지역"] == st.session_state["selected_region"]].iloc[0]

st.markdown('<div class="section-title">✨ 지역 상세</div>', unsafe_allow_html=True)

left, right = st.columns([1.05, 1])

with left:
    st.image(selected["사진"], use_container_width=True)
    st.markdown(
        f'<div class="card"><span class="badge">{selected["지역"]}</span>'
        f'<span class="badge">{selected["관광유형"]}</span>'
        f'<span class="badge">{selected["랜드마크유형"]}</span>'
        f'<h2>{selected["관광지"]}</h2>'
        f'<p class="small">{selected["관광설명"]}</p></div>',
        unsafe_allow_html=True,
    )

with right:
    st.metric("숨은지역 점수", f"{selected['숨은지역점수']}점")
    st.metric("관광 인지도", f"{selected['관광인지도']}점")
    st.metric("지역 특색", f"{selected['지역특색']}점")

    reasons = []
    if selected["관광인지도"] < 50:
        reasons.append("관광 인지도가 상대적으로 낮음")
    if selected["음식점수"] >= 80:
        reasons.append("지역 음식 경쟁력이 높음")
    if selected["지역특색"] >= 90:
        reasons.append("지역 특색이 강함")

    st.markdown(
        '<div class="card"><b>💡 추천 이유</b><br>' +
        "<br>".join("• " + x for x in reasons) +
        "</div>",
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# 상세 탭
# -------------------------------------------------
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
        st.caption("※ 현재 이름은 MVP용 예시입니다. 실제 서비스에서는 공공데이터/관광 API 등으로 검증된 사업장 정보를 연결하세요.")

with tab2:
    st.markdown(f"### 🏞️ {selected['관광지']}")
    st.write(selected["관광설명"])
    st.markdown(f"**관광 유형:** {selected['관광유형']}")
    st.markdown(f"**랜드마크 유형:** {selected['랜드마크유형']}")

with tab3:
    st.markdown(f"### 🎉 {selected['지역행사']}")
    st.write(selected["행사설명"])
    st.info("※ 축제 개최 여부와 일정은 실제 서비스에서 공식 지자체/관광 API로 실시간 확인해야 합니다.")

with tab4:
    st.markdown(f"### 🎁 {selected['특산품']}")
    st.write(selected["특산설명"])

with tab5:
    st.caption("아래 리뷰는 화면 구성 확인을 위한 MVP 예시 데이터입니다.")
    for name, rating, text, date in selected["리뷰"]:
        st.markdown(
            f'<div class="review"><b>{name}</b> &nbsp; ⭐ {rating}/5'
            f'<br>{text}<br><span class="small">{date}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### ✍️ 리뷰 작성 UI")
    review_rating = st.slider("별점", 1, 5, 5, key=f"rating_{selected['키']}")
    review_text = st.text_area("방문 후기를 입력해보세요.", key=f"text_{selected['키']}")
    if st.button("리뷰 등록", key=f"submit_{selected['키']}"):
        if review_text.strip():
            st.success("MVP 화면에서는 입력 완료를 표시합니다. 실제 서비스에서는 DB 저장 기능을 연결하면 됩니다.")
        else:
            st.warning("후기를 입력해주세요.")

# -------------------------------------------------
# 추천 코스
# -------------------------------------------------
st.markdown('<div class="section-title">🧭 추천 여행 코스</div>', unsafe_allow_html=True)

course = [
    f"① {selected['관광지']} 방문",
    f"② {selected['대표음식']} 맛보기",
    f"③ {selected['특산품']} 체험/구매",
    f"④ {selected['지역행사']} 일정 확인",
]

cols = st.columns(4)
for col, text in zip(cols, course):
    with col:
        st.markdown(f'<div class="card"><b>{text}</b></div>', unsafe_allow_html=True)

# -------------------------------------------------
# TOP 5
# -------------------------------------------------
st.markdown('<div class="section-title">🏆 숨은 지역 TOP 5</div>', unsafe_allow_html=True)

top5 = df.sort_values("숨은지역점수", ascending=False).head(5)

for i, (_, row) in enumerate(top5.iterrows(), start=1):
    st.markdown(
        f'<div class="card"><b>{i}. {row["지역"]}</b> '
        f'— 숨은지역 점수 <b>{row["숨은지역점수"]}점</b> '
        f'· 대표 음식 {row["대표음식"]} · 관광지 {row["관광지"]}</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "본 화면은 SGIS 기반 창업 아이디어의 MVP 예시입니다. "
    "지역 점수는 서비스 기획을 위한 예시 계산식이며, "
    "실제 상용 서비스에서는 SGIS OpenAPI 및 관광·지역 공공데이터를 연결해야 합니다."
)
