import streamlit as st
from func.google_sheet import connect_main, pull_data, load_all
import streamlit_authenticator as stauth
import os
import altair as alt
from func.analysis import get_data, groupby
import plotly_express as px

# Page settings
st.set_page_config(page_title="Swift Notes", page_icon="📚", layout="wide")

# Merging all csv files into a single file
df = get_data()


# Main Header
st.header("Dashboard 🏡")

# Refresh button
refresh = st.button("Refresh Dashboard", type="secondary", on_click=load_all)


# Subheader for Summary Stats
st.subheader("Summary Stats for Overall Uploads")

# Columns for spliting headers or metrics
col1, col2, col3 = st.columns(3)

# Column 1 Metric for 
col1.metric("Articles", value=df[df["note_type"] == "Articles"].shape[0])
col2.metric("Free Courses", value=df[df["note_type"] == "Free Courses"].shape[0])
col3.metric("Research Publications", value=df[df["note_type"] == "Research"].shape[0])

st.sidebar.header("Welcome Guest")

top_number = st.sidebar.slider(
    "Select Number of Top Resources To View", min_value=3, max_value=15
)

resources = ["All", "Articles", "Free Courses", "Research"]
sel_resource = st.sidebar.selectbox("Choose Resource", options=resources)

categories = df["category"].unique().tolist()
categories.insert(0, "All")
sel_category = st.sidebar.selectbox(
    "Choose Category",
    options=categories,
)

sorted_df = df.loc[
    :, ["title", "link", "publisher", "date_created", "note_type", "category"]
].sort_values(by="date_created", ascending=True)

sorted_df = (
    sorted_df[sorted_df["note_type"] == sel_resource]
    if sel_resource != "All"
    else sorted_df
)
sorted_df = (
    sorted_df[sorted_df["category"] == sel_category][:5]
    if sel_category != "All"
    else sorted_df[:top_number]
)

st.markdown("###")

st.subheader(
    f"Top {top_number} Recently Uploaded {sel_resource if sel_resource != 'All' else 'Resources'}"
)

for index, row in sorted_df.iterrows():
    st.markdown(
        f"""
                [{row["title"]}]({row["link"]})
                by {row["publisher"]}
                """
    )

st.markdown("###")

st.subheader("Trend View")

gdf = groupby(df, sel_resource, sel_category)
gdf.rename(
    columns={"date_created": "Upload Date", "count_note_type": "Number of Uploads"},
    inplace=True,
)
fig = px.bar(gdf, x="Upload Date", y="Number of Uploads", color='category')

with fig.batch_update():
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(width=1000, height=700,
                    title="Number of Resources Uploaded Against Date of Upload")

st.plotly_chart(fig)


# # About the SwiftNotes Project
# with st.expander("About this App"):
#     st.markdown(
#         """
#         This App is a simple online repository for resources pertaining to
#         Self-Development, Research, Technology (Python, Excel, SQL, etc).

#         This list will continue to grow when more interesting subject areas are discovered
#                 """
#     )


# # How to use the app
# with st.expander("How to use the app"):
#     st.markdown(
#         """
#     - Use the Navigation Bar on Your top left to peruse any topic of interest.(Toggle the Dropdown to Reveal More)
#     - Within each area you can find various subsets of resources such as articles, pdfs and even FREE online courses.
#     - Click on the Expander Per Group, Read the Summary for any of the listed topics and click the link to be directed to the Page
#     """
#     )


# Made by section - footer in the sidebar
st.sidebar.markdown(
    """
### Made with ❤️ by:
- [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
Would Love to Hear Your Feedback and Contributions"""
)
