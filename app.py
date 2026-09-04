import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide"
)

st.title("📍 숨은 로컬 발견")
st.subheader("SGIS 지역 데이터를 활용한 숨은 지역 & 로컬 음식 추천 플랫폼")

st.markdown(
    """
    **잘 알려지지 않은 지역을 데이터로 발견하고,
    그 지역만의 음식과 로컬 콘텐츠를 추천합니다.**
    """
)

# --------------------------------------------------
# 샘플 지역 데이터
# 실제 서비스에서는 SGIS API 데이터로 교체
# --------------------------------------------------

data = {
    "지역": [
        "강원도 정선군",
        "충청북도 단양군",
        "전라남도 구례군",
        "경상북도 영덕군",
        "전라북도 무주군",
        "충청남도 서천군",
        "경상남도 의령군",
        "강원도 삼척시"
    ],

    "위도": [
        37.3806,
        36.9846,
        35.2025,
        36.4150,
        36.0068,
        36.0800,
        35.3920,
        37.4499
    ],

    "경도": [
        128.6608,
        128.3656,
        127.4620,
        129.3650,
        127.6600,
        126.6900,
        128.2620,
        129.1650
    ],

    "인구": [
        35000,
        27000,
        25000,
        34000,
        24000,
        47000,
        13000,
        62000
    ],

    "인구변화율": [
        -2.8,
        -1.9,
        -3.1,
        -2.2,
        -3.5,
        -1.7,
        -4.2,
        -1.5
    ],

    "음식점수": [
        87,
        83,
        91,
        85,
        89,
        82,
        94,
        80
    ],

    "관광인지도": [
        48,
        52,
        35,
        38,
        32,
        30,
        22,
        55
    ],

    "지역특색": [
        90,
        86,
        95,
        88,
        91,
        84,
        96,
        81
    ],

    "대표음식": [
        "곤드레밥",
        "마늘순대",
        "산수유 음식",
        "대게",
        "어죽",
        "꽃게요리",
        "소고기국밥",
        "곰치국"
    ]
}

df = pd.DataFrame(data)

# --------------------------------------------------
# 숨은 지역 점수 계산
# --------------------------------------------------

def calculate_hidden_score(row):

    # 인지도가 낮을수록 높은 점수
    hidden_score = 100 - row["관광인지도"]

    # 인구 감소 지역 가산점
    population_score = min(abs(row["인구변화율"]) * 5, 20)

    # 음식과 지역 특색
    food_score = row["음식점수"] * 0.25
    local_score = row["지역특색"] * 0.25

    score = (
        hidden_score * 0.4
        + population_score * 0.1
        + food_score
        + local_score
    )

    return round(score, 1)


df["숨은지역점수"] = df.apply(calculate_hidden_score, axis=1)

# --------------------------------------------------
# 사이드바
# --------------------------------------------------

st.sidebar.header("🔎 지역 탐색 조건")

min_score = st.sidebar.slider(
    "최소 숨은 지역 점수",
    min_value=0,
    max_value=100,
    value=60
)

food_preference = st.sidebar.selectbox(
    "선호 음식",
    [
        "전체",
        "밥",
        "국밥",
        "해산물",
        "향토음식"
    ]
)

# --------------------------------------------------
# 필터
# --------------------------------------------------

filtered_df = df[
    df["숨은지역점수"] >= min_score
].copy()

# 음식 검색
if food_preference != "전체":

    keyword_map = {
        "밥": ["밥", "어죽"],
        "국밥": ["국밥"],
        "해산물": ["대게", "꽃게", "곰치"],
        "향토음식": ["곤드레", "마늘", "산수유", "어죽"]
    }

    keywords = keyword_map[food_preference]

    filtered_df = filtered_df[
        filtered_df["대표음식"].apply(
            lambda x: any(k in x for k in keywords)
        )
    ]

# --------------------------------------------------
# TOP 추천
# --------------------------------------------------

st.header("🏆 숨은 로컬 추천 TOP 5")

top5 = filtered_df.sort_values(
    "숨은지역점수",
    ascending=False
).head(5)

for i, (_, row) in enumerate(top5.iterrows(), start=1):

    with st.container():

        col1, col2, col3 = st.columns([1, 4, 2])

        with col1:
            st.markdown(f"## {i}")

        with col2:

            st.markdown(
                f"### 📍 {row['지역']}"
            )

            st.write(
                f"🍴 대표 음식 : **{row['대표음식']}**"
            )

            st.write(
                f"👥 인구 : {row['인구']:,}명"
            )

        with col3:

            st.metric(
                "숨은 지역 점수",
                f"{row['숨은지역점수']}점"
            )

# --------------------------------------------------
# 지도
# --------------------------------------------------

st.header("🗺️ 숨은 로컬 지도")

m = folium.Map(
    location=[36.5, 127.8],
    zoom_start=7
)

for _, row in filtered_df.iterrows():

    popup_text = f"""
    <b>{row['지역']}</b><br>
    숨은 지역 점수: {row['숨은지역점수']}점<br>
    대표 음식: {row['대표음식']}<br>
    지역 특색: {row['지역특색']}점
    """

    folium.Marker(
        location=[
            row["위도"],
            row["경도"]
        ],
        popup=folium.Popup(
            popup_text,
            max_width=300
        ),
        tooltip=f"{row['지역']} ({row['숨은지역점수']}점)"
    ).add_to(m)

st_folium(
    m,
    width=1200,
    height=600
)

# --------------------------------------------------
# 지역 상세 분석
# --------------------------------------------------

st.header("📊 지역 상세 분석")

if len(filtered_df) > 0:

    selected_region = st.selectbox(
        "분석할 지역을 선택하세요",
        filtered_df["지역"].tolist()
    )

    selected = filtered_df[
        filtered_df["지역"] == selected_region
    ].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "숨은 지역 점수",
            f"{selected['숨은지역점수']}점"
        )

    with col2:
        st.metric(
            "지역 특색",
            f"{selected['지역특색']}점"
        )

    with col3:
        st.metric(
            "음식 특색",
            f"{selected['음식점수']}점"
        )

    with col4:
        st.metric(
            "관광 인지도",
            f"{selected['관광인지도']}점"
        )

    st.markdown("### 🍴 이 지역의 로컬 음식")

    st.info(
        f"**{selected['대표음식']}**\n\n"
        f"{selected_region}의 대표적인 로컬 음식으로 "
        f"추천합니다."
    )

    st.markdown("### 💡 왜 이 지역을 추천하나요?")

    st.write(
        f"""
        **{selected_region}**은 관광 인지도가 상대적으로 낮으면서
        지역 특색과 음식 특색이 높은 지역입니다.

        - 관광 인지도 : {selected['관광인지도']}점
        - 지역 특색 : {selected['지역특색']}점
        - 음식 특색 : {selected['음식점수']}점
        - 인구 변화율 : {selected['인구변화율']}%
        
        따라서 일반적인 유명 관광지보다
        **숨겨진 로컬 경험을 원하는 사용자에게 적합한 지역**으로
        판단됩니다.
        """

    )

else:

    st.warning(
        "현재 조건에 맞는 지역이 없습니다."
    )

# --------------------------------------------------
# 데이터 테이블
# --------------------------------------------------

with st.expander("📋 지역 데이터 확인"):

    st.dataframe(
        filtered_df[
            [
                "지역",
                "인구",
                "인구변화율",
                "음식점수",
                "관광인지도",
                "지역특색",
                "숨은지역점수",
                "대표음식"
            ]
        ],
        use_container_width=True
    )