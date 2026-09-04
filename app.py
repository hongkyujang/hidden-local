
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide"
)


# =========================================================
# 전체 화면 디자인
# =========================================================

st.markdown("""
<style>

    /* 전체 배경 */
    .stApp {
        background: #f4f7f6;
    }

    /* 메인 영역 */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* 제목 */
    h1 {
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2, h3 {
        font-weight: 700;
    }

    /* Metric 카드 */
    div[data-testid="stMetric"] {
        background: white;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #e8eceb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    /* 버튼 */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# 제목
# =========================================================

st.title("📍 숨은 로컬 발견")

st.caption(
    "데이터로 발견하는 대한민국의 숨은 지역과 로컬 경험"
)


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
        "음식설명":
            "정선의 대표적인 향토음식으로 곤드레나물을 활용한 건강한 한식",

        "음식점": "정선 곤드레마을",
        "음식점설명":
            "곤드레밥과 정선 지역 향토음식을 즐길 수 있는 로컬 식당",

        "관광지": "민둥산",
        "관광지설명":
            "가을 억새와 아름다운 산 풍경을 즐길 수 있는 정선의 대표 관광지",

        "지역행사": "정선 5일장",
        "행사설명":
            "정선의 전통시장과 지역 먹거리를 경험할 수 있는 대표적인 지역 행사",

        "특산품": "곤드레",
        "특산품설명":
            "정선을 대표하는 산나물 특산품",

        "지역사진":
            "https://images.unsplash.com/photo-1500534623283-312aade485b7",

        "음식사진":
            "https://images.unsplash.com/photo-1547592180-85f173990554",

        "관광사진":
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470",

        "특산품사진":
            "https://images.unsplash.com/photo-1547592180-85f173990554",

        "리뷰": [
            {
                "작성자": "정선 주민",
                "평점": 5,
                "내용":
                    "관광객들이 많이 찾는 곳보다 조용한 동네를 좋아한다면 추천하고 싶어요.",
                "날짜": "2026.08.15"
            },
            {
                "작성자": "정선 거주 3년",
                "평점": 4,
                "내용":
                    "곤드레 음식이 생각보다 다양하고 지역 분위기도 여유롭습니다.",
                "날짜": "2026.08.02"
            },
            {
                "작성자": "지역 상인",
                "평점": 5,
                "내용":
                    "정선 5일장에 오면 지역 분위기를 제대로 느낄 수 있습니다.",
                "날짜": "2026.07.21"
            }
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
        "음식설명":
            "단양의 대표 특산물인 마늘을 활용한 지역 음식",

        "음식점": "단양 마늘골목",
        "음식점설명":
            "마늘을 활용한 다양한 지역 음식을 맛볼 수 있는 로컬 식당가",

        "관광지": "도담삼봉",
        "관광지설명":
            "남한강에 솟아 있는 세 개의 봉우리로 유명한 단양의 대표 관광지",

        "지역행사": "단양 마늘축제",
        "행사설명":
            "단양 마늘을 주제로 다양한 체험과 먹거리를 즐길 수 있는 지역 행사",

        "특산품": "단양마늘",
        "특산품설명":
            "단양의 대표적인 지역 특산물",

        "지역사진":
            "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",

        "음식사진":
            "https://images.unsplash.com/photo-1547592180-85f173990554",

        "관광사진":
            "https://images.unsplash.com/photo-1500534623283-312aade485b7",

        "특산품사진":
            "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f",

        "리뷰": [
            {
                "작성자": "단양 주민",
                "평점": 5,
                "내용":
                    "유명 관광지뿐만 아니라 주변에 작은 식당과 볼거리가 많습니다.",
                "날짜": "2026.08.18"
            },
            {
                "작성자": "단양 거주 5년",
                "평점": 4,
                "내용":
                    "마늘을 활용한 음식이 생각보다 많아서 먹거리 여행으로도 좋아요.",
                "날짜": "2026.07.29"
            }
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
        "음식설명":
            "지리산 주변의 다양한 산나물을 활용한 향토음식",

        "음식점": "구례 산채마을",
        "음식점설명":
            "지리산 산나물을 활용한 다양한 향토음식을 맛볼 수 있는 곳",

        "관광지": "지리산 노고단",
        "관광지설명":
            "지리산의 아름다운 자연경관을 감상할 수 있는 대표 명소",

        "지역행사": "구례 산수유축제",
        "행사설명":
            "봄철 산수유를 중심으로 지역 문화와 먹거리를 즐기는 행사",

        "특산품": "산수유",
        "특산품설명":
            "구례를 대표하는 지역 특산품",

        "지역사진":
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b",

        "음식사진":
            "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",

        "관광사진":
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",

        "특산품사진":
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352",

        "리뷰": [
            {
                "작성자": "구례 주민",
                "평점": 5,
                "내용":
                    "조용한 자연을 좋아하는 사람에게 정말 잘 맞는 지역이라고 생각합니다.",
                "날짜": "2026.08.20"
            },
            {
                "작성자": "구례 거주 2년",
                "평점": 5,
                "내용":
                    "산나물 음식이 정말 다양하고 지역 분위기가 편안합니다.",
                "날짜": "2026.08.01"
            }
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
        "음식설명":
            "동해안 영덕을 대표하는 해산물",

        "음식점": "영덕 대게거리",
        "음식점설명":
            "영덕의 대표적인 해산물 요리를 즐길 수 있는 음식 거리",

        "관광지": "해맞이공원",
        "관광지설명":
            "동해의 바다 풍경과 일출을 감상하기 좋은 관광지",

        "지역행사": "영덕 대게축제",
        "행사설명":
            "영덕 대게와 지역 문화를 체험할 수 있는 대표 지역 행사",

        "특산품": "영덕대게",
        "특산품설명":
            "영덕을 대표하는 해산물 특산품",

        "지역사진":
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",

        "음식사진":
            "https://images.unsplash.com/photo-1544943910-4c1dc44aab44",

        "관광사진":
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",

        "특산품사진":
            "https://images.unsplash.com/photo-1559339352-11d035aa65de",

        "리뷰": [
            {
                "작성자": "영덕 주민",
                "평점": 5,
                "내용":
                    "바다를 좋아한다면 한적하게 여행하기 좋은 지역입니다.",
                "날짜": "2026.08.14"
            },
            {
                "작성자": "영덕 거주 4년",
                "평점": 4,
                "내용":
                    "대게뿐만 아니라 주변 해산물 음식도 생각보다 다양합니다.",
                "날짜": "2026.07.30"
            }
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
        "음식설명":
            "민물고기를 활용한 무주 지역의 향토음식",

        "음식점": "무주 어죽마을",
        "음식점설명":
            "지역 주민들이 즐겨 찾는 향토음식점",

        "관광지": "덕유산",
        "관광지설명":
            "사계절 아름다운 자연환경을 가진 무주의 대표 관광지",

        "지역행사": "무주 반딧불축제",
        "행사설명":
            "지역 자연환경과 반딧불이를 주제로 한 대표적인 지역 축제",

        "특산품": "머루",
        "특산품설명":
            "무주 지역에서 생산되는 대표 농특산물",

        "지역사진":
            "https://images.unsplash.com/photo-1464278533981-50106e6176b1",

        "음식사진":
            "https://images.unsplash.com/photo-1547592180-85f173990554",

        "관광사진":
            "https://images.unsplash.com/photo-1464278533981-50106e6176b1",

        "특산품사진":
            "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea",

        "리뷰": [
            {
                "작성자": "무주 주민",
                "평점": 5,
                "내용":
                    "산과 자연을 좋아한다면 정말 추천합니다.",
                "날짜": "2026.08.11"
            }
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
        "음식설명":
            "서천 지역의 대표적인 수산물 특산품",

        "음식점": "서천 바다밥상",
        "음식점설명":
            "서천 지역의 해산물과 향토음식을 맛볼 수 있는 곳",

        "관광지": "국립생태원",
        "관광지설명":
            "다양한 생태환경을 체험할 수 있는 서천의 대표 관광지",

        "지역행사": "서천 한산모시축제",
        "행사설명":
            "한산모시와 지역 전통문화를 경험할 수 있는 행사",

        "특산품": "한산모시",
        "특산품설명":
            "서천을 대표하는 전통 특산품",

        "지역사진":
            "https://images.unsplash.com/photo-1500534623283-312aade485b7",

        "음식사진":
            "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",

        "관광사진":
            "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",

        "특산품사진":
            "https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85",

        "리뷰": [
            {
                "작성자": "서천 주민",
                "평점": 4,
                "내용":
                    "조용하게 바다와 자연을 즐기고 싶은 분에게 추천합니다.",
                "날짜": "2026.08.05"
            }
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
        "음식설명":
            "의령을 대표하는 지역 음식",

        "음식점": "의령 소바거리",
        "음식점설명":
            "의령 지역의 대표적인 소바와 향토음식을 맛볼 수 있는 곳",

        "관광지": "자굴산",
        "관광지설명":
            "의령의 자연환경을 감상할 수 있는 대표적인 산",

        "지역행사": "의령 홍의장군축제",
        "행사설명":
            "의령의 역사와 문화를 체험할 수 있는 지역 행사",

        "특산품": "망개떡",
        "특산품설명":
            "의령을 대표하는 전통 간식",

        "지역사진":
            "https://images.unsplash.com/photo-1473448912268-2022ce9509d8",

        "음식사진":
            "https://images.unsplash.com/photo-1552611052-33e04de081de",

        "관광사진":
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e",

        "특산품사진":
            "https://images.unsplash.com/photo-1551024506-0bccd828d307",

        "리뷰": [
            {
                "작성자": "의령 주민",
                "평점": 5,
                "내용":
                    "아직 관광객이 많지 않아서 조용하게 여행하기 좋습니다.",
                "날짜": "2026.08.09"
            }
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
        "음식설명":
            "삼척의 대표적인 동해안 향토음식",

        "음식점": "삼척 바다밥상",
        "음식점설명":
            "동해안 해산물과 지역 음식을 맛볼 수 있는 로컬 식당",

        "관광지": "장호항",
        "관광지설명":
            "맑은 바다와 아름다운 해안 풍경으로 유명한 삼척의 관광지",

        "지역행사": "삼척 장미축제",
        "행사설명":
            "지역 주민과 관광객이 함께 즐기는 삼척의 대표적인 봄 행사",

        "특산품": "삼척 장뇌삼",
        "특산품설명":
            "삼척 지역의 대표적인 농특산품",

        "지역사진":
            "https://images.unsplash.com/photo-1500534623283-312aade485b7",

        "음식사진":
            "https://images.unsplash.com/photo-1547592180-85f173990554",

        "관광사진":
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",

        "특산품사진":
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352",

        "리뷰": [
            {
                "작성자": "삼척 주민",
                "평점": 5,
                "내용":
                    "바다 풍경이 좋고 생각보다 조용한 여행지가 많아요.",
                "날짜": "2026.08.16"
            }
        ]
    }
]


df = pd.DataFrame(region_data)


# =========================================================
# 숨은 지역 점수
# =========================================================

def calculate_hidden_score(row):

    hidden_score = 100 - row["관광인지도"]

    population_score = min(
        abs(row["인구변화율"]) * 5,
        20
    )

    food_score = row["음식점수"] * 0.25

    local_score = row["지역특색"] * 0.25

    score = (
        hidden_score * 0.4
        + population_score * 0.1
        + food_score
        + local_score
    )

    return round(score, 1)


df["숨은지역점수"] = df.apply(
    calculate_hidden_score,
    axis=1
)


# =========================================================
# 사이드바
# =========================================================

st.sidebar.header("🔎 지역 탐색 필터")

min_score = st.sidebar.slider(
    "최소 숨은 지역 점수",
    0,
    100,
    60
)

food_filter = st.sidebar.selectbox(
    "🍴 선호 음식",
    [
        "전체",
        "밥",
        "국",
        "해산물",
        "향토음식"
    ]
)


st.sidebar.subheader("🗺️ 지도 카테고리")

show_region = st.sidebar.checkbox(
    "📍 추천 지역 핀",
    value=True
)

show_food = st.sidebar.checkbox(
    "🍴 음식점 위치",
    value=True
)

show_tour = st.sidebar.checkbox(
    "🏞️ 관광지 위치",
    value=True
)

show_event = st.sidebar.checkbox(
    "🎪 지역행사 위치",
    value=True
)

show_specialty = st.sidebar.checkbox(
    "🛍️ 특산품 위치",
    value=True
)


# =========================================================
# 데이터 필터
# =========================================================

filtered_df = df[
    df["숨은지역점수"] >= min_score
].copy()


if food_filter != "전체":

    keyword_map = {

        "밥": [
            "밥"
        ],

        "국": [
            "국"
        ],

        "해산물": [
            "대게",
            "곰치",
            "김"
        ],

        "향토음식": [
            "곤드레",
            "마늘",
            "산채",
            "어죽",
            "소바",
            "곰치"
        ]
    }

    keywords = keyword_map[food_filter]

    filtered_df = filtered_df[
        filtered_df["대표음식"].apply(
            lambda x:
                any(
                    keyword in x
                    for keyword in keywords
                )
        )
    ]


# =========================================================
# 상단 통계
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📍 추천 지역",
        f"{len(filtered_df)}개"
    )


with col2:

    average_score = (
        filtered_df["숨은지역점수"].mean()
        if len(filtered_df) > 0
        else 0
    )

    st.metric(
        "⭐ 평균 숨은 지역 점수",
        f"{average_score:.1f}"
    )


with col3:

    total_reviews = sum(
        len(row["리뷰"])
        for _, row in filtered_df.iterrows()
    )

    st.metric(
        "💬 주민 리뷰",
        f"{total_reviews}개"
    )


with col4:

    st.metric(
        "🛍️ 발견한 특산품",
        f"{len(filtered_df)}개"
    )


# =========================================================
# 대한민국 지도
# =========================================================

st.subheader("🗺️ 대한민국 추천 지역 지도")


map_data = None
clicked_region = None


if len(filtered_df) == 0:

    st.warning(
        "현재 조건에 맞는 추천 지역이 없습니다."
    )

else:

    # -----------------------------------------------------
    # 지도 생성
    # -----------------------------------------------------

    m = folium.Map(

        # 대한민국 중심
        location=[
            36.2,
            127.8
        ],

        # 초기 확대
        zoom_start=7,

        # 너무 멀리 축소하지 않도록 설정
        min_zoom=7,

        # 지나치게 확대하지 않도록 설정
        max_zoom=12,

        # 오류가 적은 OpenStreetMap 사용
        tiles="OpenStreetMap",

        # 축척 표시
        control_scale=True,

        # 세계지도를 반복해서 보여주지 않음
        no_wrap=True
    )


    # -----------------------------------------------------
    # 대한민국 영역
    # -----------------------------------------------------

    korea_bounds = [
        [33.0, 124.0],
        [39.0, 132.0]
    ]


    # 대한민국 전체가 처음에 보이도록 설정

    m.fit_bounds(
        korea_bounds
    )


    # -----------------------------------------------------
    # 지도 이동 범위 제한
    # -----------------------------------------------------

    m.options["maxBounds"] = [
        [32.0, 123.0],
        [40.5, 134.0]
    ]

    m.options["maxBoundsViscosity"] = 1.0


    # -----------------------------------------------------
    # 추천 지역 핀
    # -----------------------------------------------------

    for _, row in filtered_df.iterrows():

        if show_region:

            popup_html = f"""

            <div style="
                width:230px;
                font-family:Arial;
            ">

                <h4>
                    📍 {row['지역']}
                </h4>

                <hr>

                <b>
                    ⭐ 숨은 지역 점수
                </b>

                <br>

                {row['숨은지역점수']}점

                <br><br>

                <b>
                    🍚 대표 음식
                </b>

                <br>

                {row['대표음식']}

                <br><br>

                <b>
                    🏞️ 대표 관광지
                </b>

                <br>

                {row['관광지']}

                <br><br>

                <b>
                    🛍️ 특산품
                </b>

                <br>

                {row['특산품']}

                <br><br>

                <b>
                    💬 주민 리뷰
                </b>

                <br>

                {len(row['리뷰'])}개

            </div>

            """


            folium.Marker(

                location=[
                    row["위도"],
                    row["경도"]
                ],

                popup=folium.Popup(
                    popup_html,
                    max_width=300
                ),

                tooltip=(
                    f"📍 {row['지역']} "
                    f"({row['숨은지역점수']}점)"
                ),

                icon=folium.Icon(
                    color="red",
                    icon="star"
                )

            ).add_to(m)


        # -------------------------------------------------
        # 음식점 핀
        # -------------------------------------------------

        if show_food:

            folium.Marker(

                location=[
                    row["위도"] + 0.025,
                    row["경도"] + 0.015
                ],

                tooltip=(
                    f"🍴 {row['음식점']}"
                ),

                popup=f"""
                    <b>🍴 음식점</b><br><br>

                    <b>{row['음식점']}</b>

                    <br><br>

                    {row['음식점설명']}
                """,

                icon=folium.Icon(
                    color="orange",
                    icon="cutlery"
                )

            ).add_to(m)


        # -------------------------------------------------
        # 관광지 핀
        # -------------------------------------------------

        if show_tour:

            folium.Marker(

                location=[
                    row["위도"] - 0.025,
                    row["경도"] + 0.020
                ],

                tooltip=(
                    f"🏞️ {row['관광지']}"
                ),

                popup=f"""
                    <b>🏞️ 관광지</b><br><br>

                    <b>{row['관광지']}</b>

                    <br><br>

                    {row['관광지설명']}
                """,

                icon=folium.Icon(
                    color="green",
                    icon="camera"
                )

            ).add_to(m)


        # -------------------------------------------------
        # 지역 행사 핀
        # -------------------------------------------------

        if show_event:

            folium.Marker(

                location=[
                    row["위도"] + 0.015,
                    row["경도"] - 0.025
                ],

                tooltip=(
                    f"🎪 {row['지역행사']}"
                ),

                popup=f"""
                    <b>🎪 지역행사</b><br><br>

                    <b>{row['지역행사']}</b>

                    <br><br>

                    {row['행사설명']}
                """,

                icon=folium.Icon(
                    color="purple",
                    icon="calendar"
                )

            ).add_to(m)


        # -------------------------------------------------
        # 특산품 핀
        # -------------------------------------------------

        if show_specialty:

            folium.Marker(

                location=[
                    row["위도"] - 0.015,
                    row["경도"] - 0.025
                ],

                tooltip=(
                    f"🛍️ {row['특산품']}"
                ),

                popup=f"""
                    <b>🛍️ 특산품</b><br><br>

                    <b>{row['특산품']}</b>

                    <br><br>

                    {row['특산품설명']}
                """,

                icon=folium.Icon(
                    color="blue",
                    icon="shopping-bag"
                )

            ).add_to(m)


    # -----------------------------------------------------
    # 지도 출력
    # -----------------------------------------------------

    map_data = st_folium(

        m,

        width=1200,

        height=600,

        returned_objects=[
            "last_object_clicked"
        ]
    )


# =========================================================
# 지도 클릭 감지
# =========================================================

if map_data:

    clicked = map_data.get(
        "last_object_clicked"
    )


    if clicked:

        clicked_lat = clicked.get(
            "lat"
        )

        clicked_lon = clicked.get(
            "lng"
        )


        if (
            clicked_lat is not None
            and
            clicked_lon is not None
        ):

            temp_df = filtered_df.copy()


            temp_df["거리"] = (

                (
                    temp_df["위도"]
                    - clicked_lat
                ) ** 2

                +

                (
                    temp_df["경도"]
                    - clicked_lon
                ) ** 2

            )


            closest = (
                temp_df
                .sort_values("거리")
                .iloc[0]
            )


            clicked_region = (
                closest["지역"]
            )


# =========================================================
# 지역 상세 정보
# =========================================================

st.subheader(
    "📍 추천 지역 상세 정보"
)


region_names = (
    filtered_df["지역"].tolist()
)


if len(region_names) == 0:

    st.info(
        "필터 조건을 조금 낮춰보세요."
    )

else:

    default_index = 0


    if clicked_region in region_names:

        default_index = (
            region_names.index(
                clicked_region
            )
        )


    selected_region = st.selectbox(

        "지역을 선택하세요",

        region_names,

        index=default_index
    )


    selected = filtered_df[
        filtered_df["지역"]
        == selected_region
    ].iloc[0]


    # =====================================================
    # 지역 기본 정보
    # =====================================================

    info_col1, info_col2, info_col3 = st.columns(
        [1.3, 1, 1]
    )


    with info_col1:

        st.image(
            selected["지역사진"],
            width="stretch"
        )


    with info_col2:

        st.markdown(
            f"## {selected['지역']}"
        )


        st.metric(
            "⭐ 숨은 지역 점수",
            f"{selected['숨은지역점수']}점"
        )


        st.write(
            f"👥 인구: "
            f"{selected['인구']:,}명"
        )


        st.write(
            f"📉 인구 변화율: "
            f"{selected['인구변화율']}%"
        )


        st.write(
            f"🌍 관광 인지도: "
            f"{selected['관광인지도']}점"
        )


        st.write(
            f"✨ 지역 특색: "
            f"{selected['지역특색']}점"
        )


    with info_col3:

        st.markdown(
            "### 💡 왜 추천할까요?"
        )


        st.write(
            f"""
            ✅ 관광 인지도가 상대적으로 낮음

            ✅ 지역 특색 점수가 높음

            ✅ 지역 음식 및 특산품이 존재

            ✅ 지역 주민 리뷰를 확인할 수 있음

            ✅ 숨은 지역 점수
            {selected['숨은지역점수']}점
            """
        )


    # =====================================================
    # 상세 탭
    # =====================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(

        [
            "🍚 음식",
            "🏞️ 관광지",
            "🛍️ 특산품",
            "🎪 지역행사",
            "💬 주민 리뷰"
        ]
    )


    # =====================================================
    # 음식
    # =====================================================

    with tab1:

        st.subheader(
            f"🍚 {selected['대표음식']}"
        )


        food_col1, food_col2 = st.columns(
            [1, 1]
        )


        with food_col1:

            st.image(
                selected["음식사진"],
                width="stretch"
            )


        with food_col2:

            st.markdown(
                f"### {selected['대표음식']}"
            )


            st.write(
                selected["음식설명"]
            )


            st.markdown(
                "### 🍴 추천 음식점"
            )


            st.write(
                f"**{selected['음식점']}**"
            )


            st.write(
                selected["음식점설명"]
            )


    # =====================================================
    # 관광지
    # =====================================================

    with tab2:

        st.subheader(
            f"🏞️ {selected['관광지']}"
        )


        tour_col1, tour_col2 = st.columns(
            [1, 1]
        )


        with tour_col1:

            st.image(
                selected["관광사진"],
                width="stretch"
            )


        with tour_col2:

            st.markdown(
                f"### {selected['관광지']}"
            )


            st.write(
                selected["관광지설명"]
            )


            st.success(
                "📍 추천 지역과 함께 방문해보세요."
            )


    # =====================================================
    # 특산품
    # =====================================================

    with tab3:

        st.subheader(
            f"🛍️ {selected['특산품']}"
        )


        specialty_col1, specialty_col2 = st.columns(
            [1, 1]
        )


        with specialty_col1:

            st.image(
                selected["특산품사진"],
                width="stretch"
            )


        with specialty_col2:

            st.markdown(
                f"### {selected['특산품']}"
            )


            st.write(
                selected["특산품설명"]
            )


            st.info(
                "💡 실제 서비스에서는 "
                "지역 특산품 구매처까지 연결할 수 있습니다."
            )


    # =====================================================
    # 지역 행사
    # =====================================================

    with tab4:

        st.subheader(
            f"🎪 {selected['지역행사']}"
        )


        st.write(
            selected["행사설명"]
        )


        st.success(
            "🎉 실제 서비스에서는 행사 일정과 "
            "예약/참여 정보까지 연결할 수 있습니다."
        )


    # =====================================================
    # 주민 리뷰
    # =====================================================

    with tab5:

        st.subheader(
            "💬 지역 주민 리뷰"
        )


        reviews = selected["리뷰"]


        if len(reviews) == 0:

            st.info(
                "아직 등록된 리뷰가 없습니다."
            )


        else:

            average_rating = (

                sum(
                    review["평점"]
                    for review in reviews
                )

                /

                len(reviews)

            )


            st.metric(
                "⭐ 평균 주민 평점",
                f"{average_rating:.1f} / 5.0"
            )


            st.divider()


            for review in reviews:

                st.markdown(

                    f"""
                    ### {'⭐' * review['평점']}

                    **{review['작성자']}**

                    {review['내용']}

                    📅 {review['날짜']}
                    """
                )


                st.divider()


        # -------------------------------------------------
        # 리뷰 작성
        # -------------------------------------------------

        st.markdown(
            "### ✍️ 리뷰 작성"
        )


        review_rating = st.slider(
            "평점",
            1,
            5,
            5
        )


        review_text = st.text_area(
            "지역에 대한 의견을 남겨주세요."
        )


        if st.button(
            "리뷰 등록하기"
        ):

            if review_text.strip() == "":

                st.warning(
                    "리뷰 내용을 입력해주세요."
                )

            else:

                st.success(
                    "리뷰가 등록되었습니다! "
                    "(현재 MVP에서는 실제 DB에 저장되지 않습니다.)"
                )


    # =====================================================
    # 추천 여행 코스
    # =====================================================

    st.subheader(
        "🧭 추천 로컬 여행 코스"
    )


    course1, course2, course3, course4 = st.columns(
        4
    )


    with course1:

        st.markdown(
            "### ① 🏞️"
        )

        st.write(
            selected["관광지"]
        )

        st.caption(
            "지역 관광지 탐방"
        )


    with course2:

        st.markdown(
            "### ② 🍚"
        )

        st.write(
            selected["대표음식"]
        )

        st.caption(
            "지역 음식 체험"
        )


    with course3:

        st.markdown(
            "### ③ 🎪"
        )

        st.write(
            selected["지역행사"]
        )

        st.caption(
            "지역 행사 체험"
        )


    with course4:

        st.markdown(
            "### ④ 🛍️"
        )

        st.write(
            selected["특산품"]
        )

        st.caption(
            "지역 특산품 구매"
        )


# =========================================================
# 추천 지역 TOP 5
# =========================================================

st.subheader(
    "🏆 추천 지역 TOP 5"
)


top5 = (
    df
    .sort_values(
        "숨은지역점수",
        ascending=False
    )
    .head(5)
)


for rank, (_, row) in enumerate(
    top5.iterrows(),
    start=1
):

    col1, col2, col3, col4 = st.columns(
        [0.5, 2, 1, 2]
    )


    with col1:

        st.markdown(
            f"## {rank}"
        )


    with col2:

        st.markdown(
            f"**{row['지역']}**"
        )


    with col3:

        st.markdown(
            f"⭐ **{row['숨은지역점수']}점**"
        )


    with col4:

        st.write(
            f"🍚 {row['대표음식']} · "
            f"🏞️ {row['관광지']}"
        )


# =========================================================
# 안내
# =========================================================

st.divider()


st.caption(
    "※ 현재 버전은 창업 아이디어 검증을 위한 MVP 예시입니다. "
    "지역 사진, 음식점, 관광지, 행사, 주민 리뷰는 예시 데이터이며 "
    "실제 서비스에서는 SGIS OpenAPI 및 관광·지역 데이터 API와 "
    "데이터베이스를 연결하여 운영할 수 있습니다."
)
```
