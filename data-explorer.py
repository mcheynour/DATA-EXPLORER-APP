# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:39:13 2026

@author: mchey
"""

import streamlit as st
import pandas as pd
import plotly.express as px


#Page setup
st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

st.title("DATA EXPLORER APP 📊 ")
st.markdown("Upload a CSV file to automatically explore and visualize your data.")

#Data uploading (.CSV file)
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    sep = st.radio("Separator", [",", ";", "|"], horizontal=True)
    data = pd.read_csv(uploaded_file, sep=sep)

    st.success(f"File loaded : {data.shape[0]} rows × {data.shape[1]} columns")

#Data preview
    st.subheader("Data Preview :")
    st.dataframe(data.head(10), use_container_width=True)

#KPIs introduction
    st.subheader("Some Insights :")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", data.shape[0])
    col2.metric("Columns", data.shape[1])
    col3.metric("Missing values", data.isnull().sum().sum())
    col4.metric("Duplicates", data.duplicated().sum())

#Statistics introduction
    st.subheader("Descriptive Statistics : ")
    if st.checkbox("Show statistics"):
        st.dataframe(data.describe(), use_container_width=True)

#Missing values (NANs)
    if st.checkbox("Show missing values by column"):
        missing = data.isnull().sum().reset_index()
        missing.columns = ["Column", "Missing values"]
        missing = missing[missing["Missing values"] > 0]
        if missing.empty:
            st.info("No missing values found !")
        else:
            st.dataframe(missing, use_container_width=True)

#Data visualisation (chart type selected) 
    st.subheader("Data Visualisation : ")
    col_left, col_right = st.columns(2)

    with col_left:
        column = st.selectbox("Select a column", data.columns)
        chart_type = st.selectbox("Chart type", ["Bar", "Histogram", "Pie", "Box"])

    with col_right:
        if chart_type == "Bar":
            vc = data[column].value_counts().reset_index()
            vc.columns = ["value", "count"]
            fig = px.bar(vc, x="value", y="count", title=f"Bar chart – {column}")
        elif chart_type == "Histogram":
            fig = px.histogram(data, x=column, title=f"Histogram – {column}")
        elif chart_type == "Pie":
            fig = px.pie(data, names=column, title=f"Pie chart – {column}")
        elif chart_type == "Box":
            fig = px.box(data, y=column, title=f"Box plot – {column}")
        st.plotly_chart(fig, use_container_width=True)

#Data downloading (.CSV file)
    st.subheader("Downloading : ")
    st.download_button(
        label="Download cleaned data",
        data=data.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to get started.")