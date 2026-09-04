/* =========================================================
   Streamlit 전체 배경
   ========================================================= */

/* 브라우저 전체 */
html, body {
    background-color: #f7f8fa !important;
}

/* Streamlit 앱 전체 */
.stApp {
    background-color: #f7f8fa !important;
}

/* 실제 메인 화면 */
[data-testid="stAppViewContainer"] {
    background-color: #f7f8fa !important;
}

/* 메인 영역 */
[data-testid="stAppViewContainer"] > section {
    background-color: #f7f8fa !important;
}

/* 콘텐츠 영역 */
[data-testid="stMain"] {
    background-color: #f7f8fa !important;
}

/* Streamlit header */
[data-testid="stHeader"] {
    background-color: #f7f8fa !important;
}

/* 메인 콘텐츠 폭 */
.block-container {
    max-width: 1450px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e9edf2;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] .block-container {
    background-color: #ffffff !important;
    padding-top: 2rem;
}
