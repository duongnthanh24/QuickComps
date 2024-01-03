from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import re

response = """SELECT Name, Country, Description, Primary_Industry, Detailed_Description, Detailed_Product, Revenue, EBITDA FROM df WHERE Primary_Industry = 'Brewers' AND Country = 'China' OR Detailed_Description LIKE '%coffee%' OR Detailed_Product LIKE '%coffee%'"""
response
country_pattern = r"Country\s*=\s*'([^']+)'" 
country_matches = re.findall(country_pattern, response)
industry_pattern = r"Primary_Industry\s*=\s*'([^']+)'" 
industry_matches = re.findall(industry_pattern, response)

description_pattern = r"Detailed_Description\s+LIKE\s+'([^']*)'" 
de_inter = re.findall(description_pattern, response)
description_matches = [item.replace('%', '') for item in de_inter]

df = pd.read_csv('table_g.csv',encoding = "ISO-8859-1")
#df['Detailed_Description'].fillna("Not Available")
sql_select_list = []
for i in df.columns:
    if i in response:
        sql_select_list.append(i)


df = df.copy()

modification_container = st.container()

with modification_container:
    to_filter_columns = st.multiselect("Filter dataframe on", df.columns,sql_select_list)
    to_filter_columns
    for column in to_filter_columns:
        left, right = st.columns((1, 20))
        # Treat columns with < 10 unique values as categorical
        if column == "Country":
            user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                country_matches,
            )
            coun = df[df[column].isin(user_cat_input)]
        elif column == "Primary_Industry":
            i_user_cat_input = right.multiselect(
                f"Values for {column}",
                df[column].unique(),
                industry_matches,
            )
            ind = df[df[column].isin(i_user_cat_input)]
            
        elif column == "Detailed_Description":
            user_cat_input = right.multiselect(
                f"Values for {column}",
                description_matches,
                description_matches,
            )
            #description_matches[0]
            #a = df[df[column].str.contains(description_matches[0])] 
            des = df.dropna()[df.dropna()[column].str.contains(description_matches[0])]
        elif is_numeric_dtype(df[column]):
            _min = float(df[column].min())
            _max = float(df[column].max())
            step = (_max - _min) / 100
            user_num_input = right.slider(
                f"Values for {column}",
                min_value=_min,
                max_value=_max,
                value=(_min, _max),
                step=step,
            )
            num = df[df[column].between(*user_num_input)]
    df = pd.merge(coun, ind, how="inner")

df
#st.dataframe(filter_dataframe(df))

#to_filter_columns = st.multiselect("Filter dataframe on", df.columns,sql_select_list)