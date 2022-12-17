import streamlit as st
import pandas as pd
import gspread as gs
from google.oauth2 import service_account
import numpy as np


cred = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(
    cred,
    scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ],
)


def connect_main():
    client = gs.authorize(credentials)
    main_sheet = client.open("SWIFT_NOTES")
    return main_sheet


def pull_data(spread, sheetname, filename):
    worksheet = spread.worksheet(sheetname)
    records = worksheet.get_all_records(
        expected_headers=["title", "body", "publisher", "link", "date_created", "note_type"]
    )
    df = pd.DataFrame(records).loc[
        :, ["title", "body", "publisher", "link", "date_created", "note_type"]
    ]
    df.replace("", np.nan, inplace=True)
    df.dropna(axis=0, inplace=True)
    df.to_csv(f"assets/{filename}/data/{filename}.csv", index=False)
    return df

# def update_data(spread, sheetname, filename):