import streamlit as st
#from st_on_hover_tabs import on_hover_tabs

sidebar_logo = 'assets/170.png'
main_body_logo = 'assets/logo3.png'
main_body_logo2 = 'assets/new.png'
old_web = 'https://www.marketcenter.cz/cs/'

st.set_page_config( page_title = "MC Concordia Equity Fund",
                    page_icon='assets/favicon.ico',
                    layout="wide",
                    )


#st.markdown('<style>' + open('assets/style.css').read() + '</style>', unsafe_allow_html=True)


#st.markdown("""
#    <script>
#     document.addEventListener("DOMContentLoaded", function() {
#        const toggleButton = document.querySelector("button[data-testid='stBaseButton-headerNoPadding']");
#        const sidebar = document.querySelector("section[data-testid='stSidebar']");
#
#        // Toggle between collapsed and expanded states when the button is clicked
#        toggleButton.addEventListener('click', function() {
#            if (sidebar.classList.contains("collapsed")) {
#                sidebar.classList.remove("collapsed");
#                toggleButton.classList.remove("collapsed");  // Also update the button state
#            } else {
#                sidebar.classList.add("collapsed");
#                toggleButton.classList.add("collapsed");
#            }
#        });
#    });
#    </script>
#""", unsafe_allow_html=True)


st.logo(main_body_logo2, size='large', #link=old_web
        )


st.sidebar.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True) # ak chcem divider za Tools ikonami v sidebare


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


home_page= st.Page("public/home.py", title="Home", icon=":material/home:", default=True)
portfolio_page = st.Page("public/portfolio.py", title="Portfolio", icon=":material/finance_mode:")
#login_page = st.Page("public/login.py", title="Log in", icon=":material/lock_person:")

#update_web_page = st.Page("admin/update-web.py", title="Update", icon=":material/deployed_code_update:")
#graphs_page = st.Page("admin/graphs.py", title="Graphs", icon=":material/query_stats:")
#earn_div_page = st.Page("admin/earn-div.py", title="E&D Dates", icon=":material/calendar_clock:")
#web_comments_page = st.Page("admin/web-comments.py", title='Customers', icon=":material/mail:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [home_page, portfolio_page],
            #"Tools": [login_page, update_web_page, graphs_page, earn_div_page, web_comments_page],
        }
    )
else:
    pg = st.navigation({
            "Account": [home_page, portfolio_page],
            #"Tools": [login_page],
        })



pg.run()


#print("🏠, 📈, 🔐, 🔔, 📊, 📆") #check material icon tu: https://fonts.google.com/icons