import streamlit as st
from google_sheet import connect_main
import streamlit_authenticator as stauth


# Page settings
st.set_page_config(page_title="Swift Notes", page_icon="📚", layout="wide")

st.header("Home 🏡")


st.sidebar.header("Welcome Stranger")

# About the CSGH Project
with st.expander("About this App"):
    st.markdown(
        """
        This App is a simple online repository for resources pertaining to 
        Self-Development, Research, Technology (Python, Excel, SQL, etc).
        
        This list will continue to grow when more interesting subject areas are discovered
                """
    )


# How to use the app
with st.expander("How to use the app"):
    st.markdown(
        """
    - Use the Navigation Bar on Your top left to peruse any topic of interest.(Toggle the Dropdown to Reveal More)
    - Within each area you can find various subsets of resources such as articles, pdfs and even FREE online courses.
    - Click on the Expander Per Group, Read the Summary for any of the listed topics and click the link to be directed to the Page
    """
    )


# Made by section - footer in the sidebar
st.sidebar.markdown(
    """
### Made with ❤️ by:
- [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
Would Love to Hear Your Feedback and Contributions"""
)
