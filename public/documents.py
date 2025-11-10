import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.header('Důležité dokumenty (ke stažení)')
st.markdown(' ')
st.markdown(' ')
col_pdfs = st.columns([1, 3])
with col_pdfs[0]:
    option = st.selectbox(
            "How would you like to be contacted?",
            ("Summary", "Key Info"),
        )
    if option == 'Summary':
        pdf = 'data/Summary.pdf'
        zoom = 0.8
    elif option == 'Key Info':
        pdf = 'data/Key_information_mccef.pdf'
        zoom = 1.15
    with open(pdf, "rb") as f:
        pdf_bytes = f.read()

    # Create a download button
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name= pdf.split('/')[-1],
        mime="application/pdf"
    )
with col_pdfs[1]:
    with st.container(border=True):    
        pdf_viewer(
            pdf,
            width=800,
            height=500,
            zoom_level=zoom,                    # 120% zoom
            viewer_align="center",             # Center alignment
            show_page_separator=True           # Show separators between pages
        )
