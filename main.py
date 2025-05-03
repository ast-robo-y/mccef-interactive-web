import streamlit as st

main_body_logo2 = 'assets/new.png'

st.set_page_config( page_title = "MC Concordia Equity Fund",
                    page_icon='assets/favicon.ico',
                    layout="wide",
                    )
st.logo(main_body_logo2, size='large',
        )
st.sidebar.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

home_page= st.Page("public/home.py", title="Home", icon=":material/home:", default=True)
portfolio_page = st.Page("public/portfolio.py", title="Portfolio", icon=":material/finance_mode:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [home_page, portfolio_page],
        }
    )
else:
    pg = st.navigation({
            "Account": [home_page, portfolio_page],
        })

pg.run()
