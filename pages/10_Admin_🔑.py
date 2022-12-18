import streamlit as st
from google_sheet import connect_main, update_data, pull_data
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Swift Notes",
    page_icon="📚",
    layout="wide",
    menu_items={
        "About": "### Get Quick Access To Relevant Information",
    },
)
st.header("Admin Dashboard  🔑")

def sheet_names(sheet):
    sheet = str(sheet)
    return sheet[sheet.find("'") + 1 : sheet.rfind("'")]

filenames = {
    "Python": "python",
    "Self Development": "self_dev",
    "SQL": "sql",
    "Excel": "excel",
    "Google Sheet": "google_sheet",
    "Research": "research",
    "Data Analysis": "data_analysis",
    "Web Development": "web_dev",
    "Statistics": "stats"
}

# User Authentication
login_credentials = dict(st.secrets["login_cred"])
cookie = dict(st.secrets["cookie"])

authenticator = stauth.Authenticate(
    login_credentials, cookie["name"], cookie["key"], cookie["expiry_days"]
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter a admin username and password")

if authentication_status == True:
    st.header("Data Entry Form")
    with st.spinner("Loading Database..."):
        main_sheet = connect_main()
        sheets = main_sheet.worksheets()
        sheets = list(map(sheet_names, sheets))

    placeholder = st.empty()
    
    with placeholder.form("Update Reading Repository"):
        table_name = st.selectbox("Please Enter Table Name", options=sheets)
        info_type = st.selectbox(
            "Select Information Type", options=("Free Courses", "Articles", "Research")
        )
        title = st.text_input("Title")
        body = st.text_area("Body (Summary)")
        publisher = st.text_input("Publisher")
        link = st.text_input("Link")
        date = st.date_input("Upload Date")
        submit = st.form_submit_button("Submit")

    values_dict = {
        "table_name": table_name,
        "info_type": info_type,
        "title": title,
        "body": body,
        "publisher": publisher,
        "link": link,
        "date": date.strftime("%Y-%m-%d"),
    }
    if submit:
        with st.spinner("Updating Database"):
            update_data(main_sheet, table_name, values_dict)
            pull_data(main_sheet, table_name, filenames[table_name])
            st.success("Database updated")
            placeholder.empty()
            st.button("Add More Entries")
