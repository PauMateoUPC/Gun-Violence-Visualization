import streamlit as st
import altair as alt
import pandas as pd

data = pd.DataFrame({'Country': ['Germany', 'France', 'Italy', 'Spain', 'Poland', 'Romania', 'Netherlands', 'Belgium', 'Czech Republic', 'Greece'],
        'Population (Millions)': [83.155, 67.657, 59.236, 47.399, 37.840, 19.202, 17.475, 11.555, 10.702, 10.679]})



chart1 = alt.Chart(data).mark_bar().encode(   #mark_bar -> type of chart ; #encode -> how we want to encode our data
    alt.X('Country:N'),  #nominal variable
    alt.Y('Population (Millions):Q'),  #quantity data
).properties(title = 'Population')


data = pd.DataFrame({'Country': ['Germany', 'France', 'Italy', 'Spain', 'Poland', 'Romania', 'Netherlands', 'Belgium', 'Czech Republic', 'Greece'],
        'Population (Millions)': [83.155, 67.657, 59.236, 47.399, 37.840, 19.202, 17.475, 11.555, 10.702, 10.679]})

chart2 = alt.Chart(data).mark_bar().encode(
    alt.X('Country:N'),
    alt.Y('Population (Millions):Q'),
    alt.Color('Country')   # coding color by country (by dafault it assumes that country is a nominal variable) si posem 'Country:O' (ordinal)
).properties(title = 'Population')

col1, col2 = st.columns(2)

st.title("Gun Violence in the USA")
st.header("prova")

with col1:
    st.altair_chart(chart1, use_container_width=True)

with col2:
    st.altair_chart(chart2, use_container_width=True)


