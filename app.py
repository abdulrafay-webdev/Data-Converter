import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Cleaning App" , layout="wide")
st.title("Data Cleaning App")
st.write("This is a simple data cleaning app that allows you to upload a CSV file and perform some basic data cleaning operations on it.")

# taking files 
Upload_files = st.file_uploader("upload your file here in CSV or Excel Format",type=['csv','xlsx'] , accept_multiple_files=True)

if Upload_files:
    for file in Upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower() 

        if file_ext == ".csv": 
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"you uploaded invalid file format {file_ext}")
            continue

        st.write(f"File Name : {file.name}")    
        st.write(f"File Size : {file.size/1024} KB")

        st.header("Data Preview")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean any Data in {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button("Remove Duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")

            with col2:
                if st.button(f"Fill Mising Values of {file.name}"):
                    num_cols = df.select_dtypes(include=['number']).columns
                    df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
                    st.write("Missing Numeric Values Filled")

        st.subheader("Choose Column for keep and comnvert")
        column = st.multiselect(f"select column for {file.name}",df.columns,default=df.columns)
        df = df[column]

        #chart visualization
        st.subheader("Chart Visualization")
        if st.checkbox("show chart"):
            st.line_chart(df.select_dtypes(include=['number']))


        #file conversion
        st.subheader("File Conversion")
        convert_type = st.radio(f"convert {file.name} to ",["csv","xlsx"],key=file.name)
        if st.button(f"convert {file.name} to {convert_type}"):
            buffer = BytesIO()
            if convert_type == "csv":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)    

            #download option
            st.download_button(label=f"click to download {file_name}",
            data=buffer,
            mime=mime_type,
            file_name=file_name)

st.success("Thank you for using this app")
