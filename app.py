import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="숨은 로컬 발견",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. 커스텀 CSS (다크 모드 및 스타일 반영)
# =========================================================
st.markdown("""
<style>
/* 글로벌 다크 배경 및 기본 폰트 설정 */
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #121212 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #e0e0e0 !important;
}

/* 상단 패딩 확보 및 반응형 너비 설정 */
.main .block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
}

/* 사이드바 다크 스타일링 */
section[data-testid="stSidebar"] {
    background-color: #1e1e1e !important;
    border-right: 1px solid #2d2d2d !important;
}

/* 메인 타이틀 헤더 */
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}
.header-title-box {
    display: flex;
    align-items: center;
    gap: 10px;
}
.header-icon {
    font-size: 28px;
    color: #ff6b6b;
}
.header-title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.3 !important;
    margin: 0;
}
.header-subtitle {
    font-size: 14px;
    color: #a0a0a0;
    margin-top: 4px;
}
.fav-btn {
    background-color: #2b2b2b;
    border: 1px solid #3d3d3d;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 13px;
    color: #ff6b6b;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}

/* 대시보드 지표 카드 */
.metric-card {
    background: #1e1e1e;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #2d2d2d;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.metric-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.metric-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}
.metric-label {
    font-size: 12px;
    color: #a0a0a0;
    font-weight: 600;
}
.metric-value {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
}
.metric-sub {
    font-size: 11px;
    color: #707070;
    margin-top: 2px;
}

/* 지도 범례 */
.legend-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-top: 10px;
    margin-bottom: 15px;
    font-size: 12px;
    color: #b0b0b0;
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

/* 상세 정보 섹션 */
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* 메인 지역 정보 카드 */
.main-region-card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #2d2d2d;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    height: 100%;
    position: relative;
}
.main-region-img {
    width: 100%;
    height: 160px;
    object-fit: cover;
}
.badge-score {
    position: absolute;
    top: 12px;
    right: 12px;
    background: #ff6b6b;
    color: white;
    font-weight: 700;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 20px;
}
.main-region-body {
    padding: 16px;
}
.main-region-desc {
    font-size: 13px;
    color: #cccccc;
    line-height: 1.5;
    margin-bottom: 15px;
}
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    border-top: 1px solid #2d2d2d;
    padding-top: 12px;
    text-align: center;
}
.stat-item-label {
    font-size: 11px;
    color: #a0a0a0;
}
.stat-item-val {
    font-size: 12px;
    font-weight: 700;
    color: #ffffff;
}

/* 서브 아이템 카드 */
.sub-info-card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #2d2d2d;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    height: 100%;
}
.sub-info-title {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
}
.sub-info-img {
    width: 100%;
    height: 110px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 10px;
}
.sub-info-name {
    font-size: 15px;
    font-weight: 700;
    color: #ffffff;
}
.sub-info-desc {
    font-size: 12px;
    color: #a0a0a0;
    line-height: 1.4;
    margin-top: 4px;
    margin-bottom: 12px;
}

/* 신규 추천 스타일 카드 */
.rec-card {
    background: #1e1e1e;
    border-radius: 10px;
    border: 1px solid #2d2d2d;
    padding: 12px;
    margin-bottom: 8px;
}
.rec-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 6px;
}
.tag-age { background-color: #2b3a4a; color: #4dabf7; }
.tag-group { background-color: #3b2b4a; color: #da77f2; }

/* 추천 맛집 카드 */
.place-card {
    background: #1e1e1e;
    border-radius: 10px;
    border: 1px solid #2d2d2d;
    padding: 12px;
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: 10px;
}
.place-img {
    width: 80px;
    height: 80px;
    border-radius: 8px;
    object-fit: cover;
}
.place-name {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
}
.place-star {
    font-size: 12px;
    color: #fcc419;
    font-weight: 700;
    margin: 2px 0;
}
.place-addr {
    font-size: 11px;
    color: #a0a0a0;
}

/* 길찾기 커스텀 버튼 스타일 */
.navi-btn-container {
    display: flex;
    gap: 8px;
    margin-top: 8px;
}
.navi-btn-naver {
    flex: 1;
    background-color: #03C75A;
    color: white !important;
    text-align: center;
    padding: 6px 0;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-decoration: none;
}
.navi-btn-kakao {
    flex: 1;
    background-color: #FEE500;
    color: #191919 !important;
    text-align: center;
    padding: 6px 0;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. 데이터 로드
# =========================================================
@st.cache_data
def load_data():
    return [
        {
            "id": 1, "지역": "강원도 정선군", "위도": 37.3806, "경도": 128.6608, "점수": 88.7,
            "인구": "34,419명", "면적": "1,444.00㎢", "음식점수": "46개", "관광지수": "91개",
            "소개": "아리랑의 고향 정선은 아름다운 자연경관과 전통문화, 그리고 건강한 먹거리가 가득한 보석 같은 지역입니다.",
            "대표음식": "곤드레밥", "대표음식_설명": "정선의 대표 향토 음식으로, 건강에 좋은 곤드레나물을 넣어 지은 밥.",
            "대표음식_img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80",
            "특산품": "곤드레", "특산품_설명": "해발 700m 고산지대에서 자란 향긋한 곤드레.",
            "특산품_img": "https://images.unsplash.com/photo-1518843875459-f738682238a6?auto=format&fit=crop&w=600&q=80",
            "축제": "정선 아리랑제", "축제_설명": "정선아리랑을 주제로 한 전통 문화 축제.",
            "축제_img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1000&q=80",
            "나이대별_추천": {
                "20대": {"장소": "병방치 짚와이어 & 스카이워크", "설명": "절벽 위에서 익스트림 액티비티를 즐기고 인스타 인생샷 남기기!"},
                "30-40대": {"장소": "정선 아리랑시장 & 레일바이크", "설명": "가족과 함께 시골 장터 체상 구경 후 풍경길 레일바이크 타기"},
                "50대이상": {"장소": "가리왕산 케이블카 & 힐링숲", "설명": "편안하게 정선의 웅장한 산세를 관람하고 소나무 숲길 산책하기"}
            },
            "인원수별_추천": {
                "1인 (혼행)": {"장소": "아우라지 둘레길 Walk", "설명": "강물을 따라 잔잔한 음악을 들으며 아늑하게 거닐 수 있는 산책로"},
                "2인 (커플)": {"장소": "화암동굴 동굴 탐험", "설명": "신비로운 금광 역사와 대형 종유석을 만나는 이색 데이트 코스"},
                "4인이상 (가족)": {"장소": "정선 레일바이크 체험", "설명": "남녀노소 누구나 같이 페달을 밝으며 정선의 사계절 풍경을 만끽"}
            },
            "맛집목록": [
                {"이름": "정선곤드레본가", "평점": "★ 4.6 (126)", "주소": "정선읍 5일장길 31", "img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=300&q=80"},
                {"이름": "함백산식당", "평점": "★ 4.4 (98)", "주소": "고한읍 고한로 123", "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=300&q=80"},
                {"이름": "정선아리랑시장 맛집", "평점": "★ 4.3 (87)", "주소": "정선읍 봉양3길 322", "img": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 2, "지역": "전라남도 구례군", "위도": 35.2025, "경도": 127.4628, "점수": 87.3,
            "인구": "24,800명", "면적": "429.80㎢", "음식점수": "38개", "관광지수": "75개",
            "소개": "지리산 자락 청정 자연 속에서 산수유와 산채 요리를 만나볼 수 있는 구례입니다.",
            "대표음식": "산채정식", "대표음식_설명": "지리산에서 채취한 다양한 나물과 정갈한 반찬으로 차려낸 한상.",
            "대표음식_img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
            "특산품": "산수유", "특산품_설명": "봄을 알리는 붉은 보석, 영양 가득한 구례 산수유.",
            "특산품_img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=600&q=80",
            "축제": "구례 산수유꽃축제", "축제_설명": "노란 산수유 꽃물결을 감상하는 대표 봄축제.",
            "축제_img": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
            "나이대별_추천": {
                "20대": {"장소": "지리산 치즈랜드", "설명": "넓은 초원과 호수를 배경으로 유럽 감성 스냅 사진 촬영하기"},
                "30-40대": {"장소": "쌍산재 한옥 다도 체험", "설명": "윤스테이 촬영지로 유명한 고풍스러운 한옥에서 다도 힐링하기"},
                "50대이상": {"장소": "화엄사 & 천은사 템플스테이", "설명": "천년 고찰의 호젓함 속에서 단경과 산사 둘레길 걸어보기"}
            },
            "인원수별_추천": {
                "1인 (혼행)": {"장소": "천은사 수홍루 소나무길", "설명": "고요함 속에서 자기만의 시간을 갖는 호수 둘레길 산책"},
                "2인 (커플)": {"장소": "쌍산재 비밀정원", "설명": "고즈넉한 한옥 정원을 거닐며 나누는 깊은 대화와 차 한 잔"},
                "4인이상 (가족)": {"장소": "산수유마을 산책로", "설명": "가족 모두 부담 없이 걸으며 붉은 수유열매와 노란 꽃 감상"}
            },
            "맛집목록": [
                {"이름": "지리산산채식당", "평점": "★ 4.8 (210)", "주소": "구례군 마산면 88", "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 3, "지역": "경상남도 의령군", "위도": 35.3222, "경도": 128.2617, "점수": 86.1,
            "인구": "26,100명", "면적": "482.90㎢", "음식점수": "32개", "관광지수": "58개",
            "소개": "소바와 의령망개떡이 유명하며 맑은 남강이 흐르는 정겨운 로컬 도시입니다.",
            "대표음식": "의령소바", "대표음식_설명": "진한 메밀향과 메밀면의 쫄깃함이 일품인 대표 별미.",
            "대표음식_img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=600&q=80",
            "특산품": "망개떡", "특산품_설명": "청망개잎으로 감싸 향긋함이 더해진 찹쌀떡.",
            "특산품_img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80",
            "축제": "의령 의병제전", "축제_설명": "임진왜란 의병들의 숭고한 호국정신을 기리는 축제.",
            "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1000&q=80",
            "나이대별_추천": {
                "20대": {"장소": "의령 구름다리 & 출렁다리", "설명": "아찔한 인공 스카이워크 구름다리 위에서 스릴 만점 포토타임"},
                "30-40대": {"장소": "솥바위 부자 기운 체험", "설명": "삼성/LG 창업주 기운이 흐르는 솥바위에서 부자 기원 사진 찍기"},
                "50대이상": {"장소": "한우산 드라이브 길", "설명": "차를 타고 편안하게 올라 탁 트인 산세와 억새 군락 관람"}
            },
            "인원수별_추천": {
                "1인 (혼행)": {"장소": "의령 전통시장 탐방", "설명": "전통 소바 맛집 혼밥 후 갓 만든 쫄깃한 망개떡 맛보기"},
                "2인 (커플)": {"장소": "충익사 한적한 백화원", "설명": "남강 변을 따라 호젓하게 거니는 고요한 데이트 산책길"},
                "4인이상 (가족)": {"장소": "자굴산 치유의 숲", "설명": "아이들과 함께하는 숲속 놀이터와 온 가족 힐링 산림욕"}
            },
            "맛집목록": [
                {"이름": "의령소바 본점", "평점": "★ 4.5 (320)", "주소": "의령읍 의병로 18", "img": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 4, "지역": "전라북도 무주군", "위도": 35.9861, "경도": 127.6606, "점수": 84.9,
            "인구": "23,500명", "면적": "631.80㎢", "음식점수": "41개", "관광지수": "82개",
            "소개": "덕유산의 웅장함과 청정 반딧불이가 숨쉬는 힐링 여행지입니다.",
            "대표음식": "어죽", "대표음식_설명": "금강 상류의 민물고기로 푹 끓여낸 얼큰하고 담백한 별미.",
            "대표음식_img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
            "특산품": "머루와인", "특산품_설명": "덕유산 자락에서 재배된 산머루로 만든 깊은 풍미의 와인.",
            "특산품_img": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=600&q=80",
            "축제": "무주 반딧불축제", "축제_설명": "천연기념물 반딧불이와 함께하는 생태 환경 축제.",
            "축제_img": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1000&q=80",
            "나이대별_추천": {
                "20대": {"장소": "머루와인 동굴 & 테이스팅", "설명": "시원한 와인 동굴에서 머루와인 시음하고 인생 사진 완성"},
                "30-40대": {"장소": "덕유산 곤돌라 & 향적봉", "설명": "어린아이도 부담 없이 곤돌라 타고 올라가는 정상의 비경"},
                "50대이상": {"장소": "구천동 33경 계곡길", "설명": "맑은 계곡물 소리와 피톤치드 가득한 단풍 명소 걷기"}
            },
            "인원수별_추천": {
                "1인 (혼행)": {"장소": "반디길 생태 탐방로", "설명": "자연을 보존한 숲길을 따라 혼자 느긋하게 걸어보는 사색"},
                "2인 (커플)": {"장소": "머루와인동굴 족욕 체험", "설명": "와인 족욕으로 피로를 풀고 로맨틱한 와인 한 잔 기분 내기"},
                "4인이상 (가족)": {"장소": "반딧불이 생태공원", "설명": "어린이 생태 교육과 신비로운 반딧불이 관찰 체험"}
            },
            "맛집목록": [
                {"이름": "금강식당 어죽", "평점": "★ 4.7 (180)", "주소": "무주읍 단산리 12", "img": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=300&q=80"}
            ]
        },
        {
            "id": 5, "지역": "충청북도 단양군", "위도": 36.9845, "경도": 128.3657, "점수": 84.2,
            "인구": "28,105명", "면적": "780.10㎢", "음식점수": "52개", "관광지수": "88개",
            "소개": "단양팔경의 수려한 자연경관과 마늘 특산 요리가 어우러진 휴양 도시입니다.",
            "대표음식": "마늘떡갈비", "대표음식_설명": "단양 특산물인 육쪽마늘을 더해 깊은 풍미를 자랑하는 떡갈비.",
            "대표음식_img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80",
            "특산품": "단양 마늘", "특산품_설명": "단단하고 향이 강해 전국 최고의 품질을 자랑하는 마늘.",
            "특산품_img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80",
            "축제": "단양 마늘축제", "축제_설명": "단양 마늘과 로컬 먹거리를 만끽하는 여름 축제.",
            "축제_img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=600&q=80",
            "메인이미지": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
            "나이대별_추천": {
                "20대": {"장소": "패러글라이딩 & 카페산", "설명": "하늘을 나는 패러글라이딩 후 산정상 카페에서 뷰 즐기기"},
                "30-40대": {"장소": "만천하스카이워크 & 알파인코스터", "설명": "남한강이 내려다보이는 전망대와 짜릿한 슬라이드 체험"},
                "50대이상": {"장소": "도담삼봉 유람선 탐방", "설명": "단양팔경의 으뜸 도담삼봉을 유람선 타고 편안하게 감상"}
            },
            "인원수별_추천": {
                "1인 (혼행)": {"장소": "단양 잔도길 산책", "설명": "절벽에 붙은 암벽 길을 혼자 유유자적 걸으며 느끼는 남한강의 운치"},
                "2인 (커플)": {"장소": "수양개빛터널 야경 데이트", "설명": "화려한 LED 조명 예술과 환상적인 빛으로 둘러싸인 정원"},
                "4인이상 (가족)": {"장소": "고수동굴 동굴 탐험", "설명": "천연기념물 고수동굴 속 신비로운 신비의 석순과 종유석 관람"}
            },
            "맛집목록": [
                {"이름": "단양마늘원조집", "평점": "★ 4.7 (150)", "주소": "단양읍 중앙로 15", "img": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=300&q=80"}
            ]
        }
    ]

data = load_data()
df = pd.DataFrame(data)

# 세션 상태 설정
if "selected_region_id" not in st.session_state:
    st.session_state.selected_region_id = 1

# =========================================================
# 4. 사이드바 (필터 컨트롤)
# =========================================================
with st.sidebar:
    st.markdown("<h4 style='font-weight:700; color:#ffffff;'>🔍 지역 탐색 필터</h4>", unsafe_allow_html=True)
    
    score_slider = st.slider("최소 숨은 지역 점수", 0, 100, 60)
    food_type = st.selectbox("선호 음식 타입", ["전체", "향토음식", "해산물", "산채요리", "육류"])
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>지도 표시 옵션</p>", unsafe_allow_html=True)
    chk_pin = st.checkbox("추천 지역 핀", value=True)
    chk_food = st.checkbox("음식점", value=True)
    chk_tour = st.checkbox("관광지", value=True)
    chk_fest = st.checkbox("축제/행사", value=True)
    chk_prod = st.checkbox("특산품", value=True)
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>정렬 기준</p>", unsafe_allow_html=True)
    sort_order = st.selectbox("", ["숨은 지역 점수 순", "인구 적은 순", "관광지 많은 순"], label_visibility="collapsed")
    
    st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0; margin-top:15px; margin-bottom:5px;'>키워드 검색</p>", unsafe_allow_html=True)
    keyword = st.text_input("", placeholder="지역명 또는 키워드 입력", label_visibility="collapsed")
    
    st.button("검색", use_container_width=True, type="primary")
    
    if st.button("🔄 필터 초기화", use_container_width=True):
        st.session_state.selected_region_id = 1
        st.rerun()

# =========================================================
# 5. 헤더 타이틀 및 상단 카드
# =========================================================
st.markdown("""
<div class="main-header">
    <div>
        <div class="header-title-box">
            <span class="header-icon">🚗</span>
            <h1 class="header-title">SGIS(통계지리정보서비스)를 활용한 숨은 지역 발견</h1>
        </div>
        <div class="header-subtitle">SGIS(통계지리정보서비스)로 발견하는 대한민국의 숨은 지역과 로컬 경험</div>
    </div>
    <div class="fav-btn">♥ 찜한 지역 0</div>
</div>
""", unsafe_allow_html=True)

# 지표 계산
filtered_df = df[df["점수"] >= score_slider]
if keyword:
    filtered_df = filtered_df[filtered_df["지역"].str.contains(keyword) | filtered_df["소개"].str.contains(keyword)]

avg_score = filtered_df["점수"].mean() if not filtered_df.empty else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#1b382b; color:#2b8a3e;">★</div>
            <div>
                <div class="metric-label">추천 지역 수</div>
                <div class="metric-value">{len(filtered_df)}곳</div>
                <div class="metric-sub">조건에 맞는 지역</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#182c4d; color:#339af0;">📈</div>
            <div>
                <div class="metric-label">평균 숨은 점수</div>
                <div class="metric-value">{avg_score:.1f}점</div>
                <div class="metric-sub">상위 30% 지역</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#2b2353; color:#91a7ff;">💬</div>
            <div>
                <div class="metric-label">리뷰 수</div>
                <div class="metric-value">237개</div>
                <div class="metric-sub">실제 방문객 리뷰</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-left">
            <div class="metric-icon" style="background:#423213; color:#fcc419;">🎁</div>
            <div>
                <div class="metric-label">혜택/쿠폰</div>
                <div class="metric-value">12개</div>
                <div class="metric-sub">로컬 제휴 할인</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 6. Folium 지도 영역
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

# 지도 중심 구하기
selected_item = df[df["id"] == st.session_state.selected_region_id].iloc[0]
map_center = [selected_item["위도"], selected_item["경도"]]

m = folium.Map(location=map_center, zoom_start=8, tiles="CartoDB dark_matter")

for _, row in filtered_df.iterrows():
    is_selected = (row["id"] == st.session_state.selected_region_id)
    marker_color = "red" if is_selected else "blue"
    
    popup_text = f"<b>{row['지역']}</b><br>점수: {row['점수']}점"
    
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=popup_text,
        tooltip=row["지역"],
        icon=folium.Icon(color=marker_color, icon="info-sign")
    ).add_to(m)

# 범례
st.markdown("""
<div class="legend-container">
    <div class="legend-item"><div class="legend-dot" style="background:#ff6b6b;"></div> 선택된 지역</div>
    <div class="legend-item"><div class="legend-dot" style="background:#339af0;"></div> 추천 지역</div>
</div>
""", unsafe_allow_html=True)

map_data = st_folium(m, width="100%", height=400)

# =========================================================
# 7. 지역 빠른 선택 버튼 (Quick Selector)
# =========================================================
st.markdown("<p style='font-size:13px; font-weight:700; color:#a0a0a0;'>빠른 지역 선택</p>", unsafe_allow_html=True)
cols = st.columns(len(filtered_df))
for idx, (_, row) in enumerate(filtered_df.iterrows()):
    btn_type = "primary" if row["id"] == st.session_state.selected_region_id else "secondary"
    if cols[idx].button(row["지역"], key=f"region_btn_{row['id']}", type=btn_type, use_container_width=True):
        st.session_state.selected_region_id = row["id"]
        st.rerun()

# =========================================================
# 8. 선택된 지역 상세 정보
# =========================================================
st.markdown(f"<div class='section-title'>📍 {selected_item['지역']} 상세 정보</div>", unsafe_allow_html=True)

col_main, col_sub1, col_sub2, col_sub3 = st.columns([1.2, 1, 1, 1])

# 메인 지역 카드
with col_main:
    st.markdown(f"""
    <div class="main-region-card">
        <img src="{selected_item['메인이미지']}" class="main-region-img" />
        <div class="badge-score">점수 {selected_item['점수']}점</div>
        <div class="main-region-body">
            <h3 style="margin:0 0 8px 0; color:#fff; font-size:18px;">{selected_item['지역']}</h3>
            <div class="main-region-desc">{selected_item['소개']}</div>
            <div class="stat-grid">
                <div>
                    <div class="stat-item-label">인구</div>
                    <div class="stat-item-val">{selected_item['인구']}</div>
                </div>
                <div>
                    <div class="stat-item-label">면적</div>
                    <div class="stat-item-val">{selected_item['면적']}</div>
                </div>
                <div>
                    <div class="stat-item-label">음식점</div>
                    <div class="stat-item-val">{selected_item['음식점수']}</div>
                </div>
                <div>
                    <div class="stat-item-label">관광지</div>
                    <div class="stat-item-val">{selected_item['관광지수']}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 대표 음식
with col_sub1:
    st.markdown(f"""
    <div class="sub-info-card">
        <div class="sub-info-title">🍲 대표 음식</div>
        <img src="{selected_item['대표음식_img']}" class="sub-info-img" />
        <div class="sub-info-name">{selected_item['대표음식']}</div>
        <div class="sub-info-desc">{selected_item['대표음식_설명']}</div>
    </div>
    """, unsafe_allow_html=True)

# 특산품
with col_sub2:
    st.markdown(f"""
    <div class="sub-info-card">
        <div class="sub-info-title">🎁 특산품</div>
        <img src="{selected_item['특산품_img']}" class="sub-info-img" />
        <div class="sub-info-name">{selected_item['특산품']}</div>
        <div class="sub-info-desc">{selected_item['특산품_설명']}</div>
    </div>
    """, unsafe_allow_html=True)

# 축제
with col_sub3:
    st.markdown(f"""
    <div class="sub-info-card">
        <div class="sub-info-title">🎉 대표 축제</div>
        <img src="{selected_item['축제_img']}" class="sub-info-img" />
        <div class="sub-info-name">{selected_item['축제']}</div>
        <div class="sub-info-desc">{selected_item['축제_설명']}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 9. 맞춤 추천 코스 (연령대별 / 인원수별) & 맛집 목록
# =========================================================
st.markdown("<div class='section-title'>🎯 맞춤 추천 코스 & 로컬 맛집</div>", unsafe_allow_html=True)

col_rec1, col_rec2, col_food = st.columns([1, 1, 1.2])

with col_rec1:
    st.markdown("<h4 style='font-size:15px; font-weight:700; color:#fff;'>👤 연령대별 추천</h4>", unsafe_allow_html=True)
    for age, info in selected_item["나이대별_추천"].items():
        st.markdown(f"""
        <div class="rec-card">
            <span class="rec-tag tag-age">{age}</span>
            <div style="font-weight:700; color:#fff; font-size:13px;">{info['장소']}</div>
            <div style="color:#a0a0a0; font-size:11px; margin-top:3px;">{info['설명']}</div>
        </div>
        """, unsafe_allow_html=True)

with col_rec2:
    st.markdown("<h4 style='font-size:15px; font-weight:700; color:#fff;'>👥 동반 인원수별 추천</h4>", unsafe_allow_html=True)
    for group, info in selected_item["인원수별_추천"].items():
        st.markdown(f"""
        <div class="rec-card">
            <span class="rec-tag tag-group">{group}</span>
            <div style="font-weight:700; color:#fff; font-size:13px;">{info['장소']}</div>
            <div style="color:#a0a0a0; font-size:11px; margin-top:3px;">{info['설명']}</div>
        </div>
        """, unsafe_allow_html=True)

with col_food:
    st.markdown("<h4 style='font-size:15px; font-weight:700; color:#fff;'>🍽️ 추천 맛집</h4>", unsafe_allow_html=True)
    for store in selected_item["맛집목록"]:
        query_str = urllib.parse.quote(f"{selected_item['지역']} {store['이름']}")
        naver_url = f"https://map.naver.com/v5/search/{query_str}"
        kakao_url = f"https://map.kakao.com/?q={query_str}"
        
        st.markdown(f"""
        <div class="place-card">
            <img src="{store['img']}" class="place-img" />
            <div style="flex:1;">
                <div class="place-name">{store['이름']}</div>
                <div class="place-star">{store['평점']}</div>
                <div class="place-addr">{store['주소']}</div>
                <div class="navi-btn-container">
                    <a href="{naver_url}" target="_blank" class="navi-btn-naver">네이버 지도</a>
                    <a href="{kakao_url}" target="_blank" class="navi-btn-kakao">카카오 맵</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
