import streamlit as st
import altair as alt
import pandas as pd



def chart_Q3() -> alt.Chart:
    # Converteix les dates a un format de data de pandas

    df_shootings = pd.read_csv("datasets/MassShootingsComplete_FIPS.csv")
    df_school_incidents = pd.read_csv("datasets/SchoolIncidents_FIPS.csv")

    df_shootings['Incident Date'] = pd.to_datetime(df_shootings['Incident Date'])
    df_school_incidents['Incident Date'] = pd.to_datetime(df_school_incidents['Incident Date'])

    # Extreu l'any de la data de l'incident per ambdós datasets
    df_shootings['Year'] = df_shootings['Incident Date'].dt.year
    df_school_incidents['Year'] = df_school_incidents['Incident Date'].dt.year

    # Filtra només els anys 2022 i posteriors
    df_shootings = df_shootings[df_shootings['Year'] >= 2022]
    df_school_incidents = df_school_incidents[df_school_incidents['Year'] >= 2022]

    # Calcula el total de tirotejos per estat i any
    total_shootings_per_state_year = df_shootings.groupby(['State', 'Year']).size().reset_index(name='Total Shootings')

    # Calcula el total d'incidents escolars per estat i any
    total_school_incidents_per_state_year = df_school_incidents.groupby(['State', 'Year']).size().reset_index(name='Total School Incidents')

    # Uneix els dos datasets per estat i any
    merged_data = pd.merge(total_shootings_per_state_year, total_school_incidents_per_state_year, on=['State', 'Year'])

    # Crea el scatterplot amb Altair
    scatterplot = alt.Chart(merged_data).mark_circle(size=100).encode(
        x=alt.X('Total Shootings:Q', title='Total Shootings'),
        y=alt.Y('Total School Incidents:Q', title='Total School Incidents'),
        color=alt.Color('Year:O', 
                        title='Year', 
                        scale=alt.Scale(
                            domain=[2022, 2023],  # Anys que tens en les dades
                            range=['#1f77b4', '#ff7f0e']  # Paleta de colors contrastada
                        )
        ),
        tooltip=['State', 'Year', 'Total Shootings', 'Total School Incidents'],  # Afegeix informació de descripció
    ).properties(
        title='Comparison of Total Shootings and School Incidents by State (2022 onwards)',
        width=500,
        height=400
    )

    return scatterplot


def chart_Q4() -> alt.Chart:
    df_shootings = pd.read_csv("datasets/MassShootingsComplete_FIPS.csv")
    gov = {
        'Year': [i for i in range(2014, 2025)],
        'y1': [230]*11,
        'y2': [220]*11,
        'governement': ['Democratic']*3 + ['Republican']*5 + ['Democratic']*3
    }

    # Convert to a DataFrame
    df = pd.DataFrame(gov)

    # Create the Altair bar chart using 'y1' or 'y2' as the Total Shootings value
    chart_gov = alt.Chart(df).mark_area().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('y1:Q', title='Total Shootings', scale=alt.Scale(domain=(200, 710))),
        y2='y2:Q',  # Specify the y2 encoding for the upper boundary of the area
        color=alt.Color('governement', scale=alt.Scale(domain=['Democratic', 'Republican'], range=['#3182bd', '#d7301f']))
    ).properties(
        title='Total Shootings per Year in the USA',
        width=500,
        height=400
    )


    # Converteix la data a un format de data de pandas
    df_shootings['Incident Date'] = pd.to_datetime(df_shootings['Incident Date'])

    # Extreu l'any de la data de l'incident
    df_shootings['Year'] = df_shootings['Incident Date'].dt.year

    # Agrupa per any i compta el nombre de tirotejos
    shootings_per_year = df_shootings.groupby('Year').size().reset_index(name='Total Shootings')

    # Crea el gràfic de línia amb Altair
    chart_ms = alt.Chart(shootings_per_year).mark_line(
        color='#525252',
        point=alt.OverlayMarkDef(filled=True, fill="#525252"),
        strokeWidth=2.5).encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),  # Usa ':O' per especificar que l'eix X és ordinal
        y=alt.Y('Total Shootings:Q', title='Total Shootings').scale(domain=(200,710))
    ).properties(
        title='Total Shootings per Year in the USA',
        width=500,
        height=400
    )


    return chart_gov + chart_ms


q3 = chart_Q3()

q4 = chart_Q4()

st.set_page_config(
    page_title="Gun Violence in the USA",layout="wide"
)

st.markdown("<h1 style='text-align: center; color: black;'>Gun Violence in the USA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>"+
            "bla bla bla"+
            "</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)



col1.altair_chart(q3,use_container_width=True)

col1.altair_chart(q3,use_container_width=True)

col2.altair_chart(q4, use_container_width=True)

col2.altair_chart(q4, use_container_width=True)


