import pandas as pd
import os
import datetime as dt
import streamlit as st


st.experimental_memo
def get_data():
    csv_files = os.listdir("assets")
    matX = []
    for file in csv_files:
        df = pd.read_csv(f"assets/{file}")
        matX.append(df)

    df = pd.concat(matX, ignore_index=True)
    df.date_created = list(map(lambda x: dt.datetime.strftime(x, "%d-%B-%Y"), pd.to_datetime(df.date_created)))
    return df

def groupby(df, resource, category):

    df = df[df["note_type"] == resource] if resource != "All" else df

    gdf = df.groupby(
        by=["date_created", "category"]
    ).agg(count_note_type=pd.NamedAgg("note_type", "count"))

    gdf.reset_index(inplace=True)
    final_df = gdf[gdf["category"] == category] if category != "All" else gdf
    return final_df

if __name__ == '__main__':
    get_data()

