import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

st.set_page_config(
    page_title="MC Concordia Equity Fund",
    page_icon=str(ASSETS_DIR / "favicon.ico"),
    layout="wide",
)


st.logo(str(ASSETS_DIR / "new.png") #, size="large"
        )



#main_body_logo2 = 'assets/new.png'
#st.set_page_config( page_title = "MC Concordia Equity Fund",
#                    page_icon='assets/favicon.ico',
#                    layout="wide",
#                    )
#st.logo(main_body_logo2, size='large',
#        )

st.sidebar.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

home_page= st.Page("public/home.py", title="Info o Fondu", icon=":material/home:", default=True)
portfolio_page = st.Page("public/portfolio.py", title="Portfolio", icon=":material/finance_mode:")
docs_page = st.Page("public/documents.py", title="Dokumenty", icon=":material/picture_as_pdf:")

pg = st.navigation(
    {
        "Podstránky": [home_page, portfolio_page, docs_page],
    }
)

pg.run()
