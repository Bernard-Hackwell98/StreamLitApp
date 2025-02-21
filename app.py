#imports
import streamlit as st
import pandas as pd
import os
#convert files to bytes so that they are more easier to work with
from io import BytesIO 

# Setting up the App
st.set_page_config(page_title="The Cleaner",layout="wide")
st.title("The Cleaner")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file extension {file_ext}")
            continue

        #Display Information about the file
        st.write(f"** File Name: **{file.name}")
        st.write(f"** File Size: **{file.size/1024}")

        #Show 5 rows of our data framer
        st.write("Preview the head of the data frame")
        st.dataframe(df.head())

        #Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"The Cleaner is cleaning data for file {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")
            

            with col2:
                if st.button(f"Filling missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been filled")
        

        # Choose specific columns to keep or convert
        st.subheader("Select Column to convert")
        columns = st.multiselect(f"Choose Columns for {file.name}",df.columns, default=df.columns)
        df = df[columns]

        # Create some Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Convert a file CSV <-> Excel
        st.subheader("Convert File")
        conversion_type = st.radio(f"Convert {file.name}",["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):

            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")  # Fix typo from ".xlxs"
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Move to the beginning of the buffer


            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name = file_name,
                mime = mime_type
            )
st.success("All files processed")