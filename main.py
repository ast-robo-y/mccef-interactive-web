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

# Temporary test

from PIL import Image
BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "assets" / "new.png"

st.write("Path:", str(logo_path))
st.write("Exists:", logo_path.is_file())
st.write("Size (bytes):", logo_path.stat().st_size if logo_path.is_file() else "Missing")

if logo_path.is_file():
    with open(logo_path, "rb") as f:
        st.write("File signature:", f.read(16).hex())

    try:
        with Image.open(logo_path) as img:
            st.write("Image format:", img.format)
            st.write("Image dimensions:", img.size)
            img.verify()

        st.image(str(logo_path), width=300)
        st.success("Image decoded successfully.")

    except Exception as e:
        st.error(f"Image decoding failed: {e}")



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
