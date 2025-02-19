import streamlit as st
import pandas as pd
import plotly.express as px
import os
from io import BytesIO

# 🎨 Page Configuration
st.set_page_config(page_title="😁 Data Sweeper", layout="wide")

# 🌙 Theme Toggle (Light/Dark Mode)
light_mode = st.toggle("☀️ Light Mode")

# 🖌 Apply Theme Styling
theme_style = """
    <style>
        body, .stApp { background-color: WHITE_BG; color: TEXT_COLOR !important; }
        h1, h2, h3, h4, h5, h6, p, label, span { color: TEXT_COLOR !important; }
        .stDataFrame, .stTextInput, .stButton, .stRadio, .stCheckbox, .stSelectbox, .stDownloadButton { 
            color: TEXT_COLOR !important; 
        }
        .css-1cpxqw2, .css-1d391kg { color: TEXT_COLOR !important; } /* Fix for file uploader & sidebar */
    </style>
"""

if light_mode:
    theme_style = theme_style.replace("WHITE_BG", "white").replace("TEXT_COLOR", "black")
else:
    theme_style = theme_style.replace("WHITE_BG", "#121212").replace("TEXT_COLOR", "white")

st.markdown(theme_style, unsafe_allow_html=True)

# 🎯 Main UI
st.title("😁 Data Sweeper")
st.write("Upload a CSV or Excel file, clean the data, visualize it, and download it in your preferred format!")

# 📂 File Upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file:", type=["csv", "xlsx"])

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

    # 📖 Load Data
    df = None
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a CSV or Excel file.")
        st.stop()

    # 📜 File Info
    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**File Size:** {uploaded_file.size/1024:.2f} KB")

    # 🔍 Data Preview
    st.subheader("📊 Data Preview")
    st.dataframe(df)

    # 🎨 Pie Chart Visualization
    st.subheader("📊 Pie Chart")

    # 🏷 Get Categorical Columns for Pie Chart
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
    
    if categorical_cols:
        selected_col = st.selectbox("Select a column for the pie chart:", categorical_cols)

        # 📊 Prepare Data for Pie Chart
        pie_data = df[selected_col].value_counts().reset_index()
        pie_data.columns = ["Category", "Count"]

        # 🎨 Create Pie Chart
        fig = px.pie(pie_data, names="Category", values="Count", title=f"Distribution of {selected_col}")

        # 📈 Display Pie Chart
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No categorical columns found for visualization.")

    # 🛠 Data Cleaning Options
    st.subheader("🛠 Data Cleaning")

    if st.checkbox("Remove Duplicates"):
        df.drop_duplicates(inplace=True)
        st.write("✅ Removed duplicate rows!")

    if st.checkbox("Fill Missing Values"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        st.write("✅ Filled missing values with column averages!")

    # 🔄 Updated Data Preview
    st.subheader("🔍 Cleaned Data Preview")
    st.dataframe(df)

    # 📂 File Conversion Options
    st.subheader("📂 Convert & Download")
    convert_to = st.radio("Convert file to:", ["CSV", "Excel"])

    if st.button("Convert & Download"):
        buffer = BytesIO()
        new_filename = uploaded_file.name.replace(file_ext, f".{convert_to.lower()}")

        # 📌 Convert Data
        if convert_to == "CSV":
            df.to_csv(buffer, index=False)
            mime_type = "text/csv"
        elif convert_to == "Excel":
            df.to_excel(buffer, index=False)
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        buffer.seek(0)

        # 🔽 Download File
        st.download_button("Download File", data=buffer, file_name=new_filename, mime=mime_type)

st.success("✅ All tasks completed! 🎉")
