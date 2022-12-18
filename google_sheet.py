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
        expected_headers=[
            "title",
            "body",
            "publisher",
            "link",
            "date_created",
            "note_type",
        ]
    )
    df = pd.DataFrame(records).loc[
        :, ["title", "body", "publisher", "link", "date_created", "note_type"]
    ]
    df.replace("", np.nan, inplace=True)
    df.dropna(axis=0, inplace=True)
    df.to_csv(f"assets/{filename}/data/{filename}.csv", index=False)
    return df

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def update_data(spread, table_name, values_dict):
    worksheet = spread.worksheet(table_name)
    last_row = next_available_row(worksheet)

    worksheet.update(
        f"A{last_row}",
        [[
            values_dict["title"],
            values_dict["body"],
            values_dict["publisher"],
            values_dict["link"],
            values_dict["date"],
            values_dict["info_type"],
        ]]
    )
