from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st
import re

response = """SELECT Name, Country, Primary_Industry, ROE FROM df WHERE Primary_Industry = 'Banks' AND Country = 'Indonesia' AND ROE > 5 ORDER BY ROE DESC"""
df = pd.read_csv('table_g.csv',encoding = "ISO-8859-1")
sql_where_list = []
for i in df.columns:
    if i in response[response.find("WHERE"):0]:
        sql_where_list.append(i)

df = df[df["Detailed_Description"].str.contains('coffee chain',case = False, na=False)]
df










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


container = st.container()

def update_df(a):
    return container.multiselect("Filter dataframe on", df.columns,a)

#update_df(sql_select_list)


all = st.checkbox("Select all")
if all:
    sql_select_list.append("COGS")
    z = container.multiselect("Filter dataframe on", df.columns,sql_select_list)
else:
    z = container.multiselect("Filter dataframe on", df.columns,sql_select_list)



sql_select_list.append("PE_Ratio")
#st.dataframe(filter_dataframe(df))

#to_filter_columns = st.multiselect("Filter dataframe on", df.columns,sql_select_list)