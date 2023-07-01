import pandas as pd
import streamlit as st
from src.analyze_marijuana import convert_data, render, filter_data
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Marijuana Arrest In Colombia - Analyze", page_icon="chart_with_upwards_trend")

# Add title and description
st.title("Marijuana Arrest In Colombia")
st.sidebar.header("Discover Our Project.")
st.write(
    """
         Here is our analyze.
         """
)


data = pd.read_csv("data/Marijuana_Arrests.csv")
columns = data.columns
data = filter_data(data, columns)

for column in columns:
    if column == "ARREST_BLOCKX":
        column = column[:-1]
        fig, ax = plt.subplots()
        data = data.loc[:, ['ARREST_BLOCKX', 'ARREST_BLOCKY']]
        data = data[data['ARREST_BLOCKX'] < 600000]
        X = data.values
        plt.xlabel('ARREST_BLOCKX')
        plt.ylabel('ARREST_BLOCKY')

        st.divider()
        st.write(f"### {column} [COORDINATES] Post traitement")
        left, right = st.columns(2)
        p = plt.gcf()
        left.pyplot(fig)
        right.write(
            f'Les blocs démontrent des zones géographiques relatives aux services de polices.')


    if column not in ["CATEGORY", "ADDRESS", "GIS_ID", "CREATOR", "CREATED", "EDITOR", "EDITED", "OBJECTID",
                      "GLOBALID", "OFFENSE_BLOCKX", "OFFENSE_BLOCKY", "ARREST_BLOCKX", "ARREST_BLOCKY"]:
        dataset, data_type = convert_data(
            data[column]
        )  # Convert data to numerical, categorical, text or index

        dataset = dataset.dropna()  # Remove NaN values

        sparsity = 1.0 - len(dataset) / float(
            len(data[column])
        )  # 1 - Size after cleaning / Size before cleaning

        render(dataset, column, sparsity, data_type)
