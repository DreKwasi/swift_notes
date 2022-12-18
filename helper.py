import streamlit as st
import datetime as dt
import pandas as pd
from google_sheet import connect_main, pull_data
import os


def parse_posts(df, select):
    st.subheader(select)
    grouped_dict = {}

    df = df[df["note_type"] == select]

    if not df.empty:
        date_ranges = list(df["date_created"].unique())
        date_ranges.sort(reverse=True)
        for date in date_ranges:
            grouped_dict[date] = df[df["date_created"] == date]

        for key in grouped_dict.keys():
            format_date = dt.datetime.strptime(key, "%Y-%m-%d")

            df = grouped_dict[key]
            for _, row in df.iterrows():
                st.write(f"##### **:blue[{row['title']}]**")
                expander = st.expander("View Summary")
                expander.markdown(
                    f"""{row['body']} 
                                \n [Access Full Resource]({row['link']})
                                \n **:violet[Published By _{row['publisher']}_]** 
                                \n Date Uploaded: {format_date.strftime("%d-%B-%Y")}"""
                )
    else:
        st.info("Coming Soon! Toggle the Dropdown Menu On the Sidebar for More Subjects")


def full_setup(page_header, filename, table_name):
    # Page settings
    st.set_page_config(page_title="Swift Notes", page_icon="book", layout="wide")

    st.header(page_header)


    st.sidebar.header("Toggle Options")
    select = st.sidebar.selectbox(
        "Select A Subject",
        options=["Free Courses", "Articles", "Research Papers"],
        help="Click the Dropdown to choose a subject",
    )
    path = f"assets/{filename}/data/{filename}.csv"
    if os.path.exists(path):
        with st.spinner("Loading Posts"):
            df = pd.read_csv(path)
            parse_posts(df=df, select=select)

    else:
        with st.spinner("Connecting to The Post Database"):
            spread = connect_main()
            try:
                df = pull_data(spread, table_name, filename)
                parse_posts(df=df, select=select)
            except KeyError:
                st.subheader("Keep In Touch")
                st.info("Resources will be Uploaded Soon")

    st.sidebar.markdown(
        """
    ### Made with ❤️ by:
    - [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
    Would Love to Hear Your Feedback and Contributions"""
    )


if "__name__" == "__main__":
    full_setup()
