import streamlit as st
import altair as alt
import pandas as pd

MassShootings = pd.read_csv("datasets/MassShootingsComplete_FIPS.csv")
ShoolIncidents = pd.read_csv("datasets/SchoolIncidents_FIPS.csv")

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
                            range=['#f1c40f', '#9b59b6']  # Paleta de colors contrastada
                        )
        ),
        tooltip=['State', 'Year', 'Total Shootings', 'Total School Incidents'],  # Afegeix informació de descripció
    ).properties(
        title='Comparison of Total Shootings and School Incidents by State (2022 onwards)',
        width=500,
        height=400
    )

    return scatterplot


def chart_Q4() -> alt.HConcatChart:
    MassShootings['Incident Date'] = pd.to_datetime(MassShootings['Incident Date'])
    MassShootings['Year'] = MassShootings['Incident Date'].dt.year
    MassShootings['Month'] = MassShootings['Incident Date'].dt.month
    monthly_shootings = MassShootings[MassShootings['Year']>2014].groupby(['Year', 'Month']).size().reset_index(name='Total Shootings')
    monthly_avg = monthly_shootings.groupby('Month')['Total Shootings'].mean().reset_index()

    # group by year
    MassShootings_year = MassShootings.groupby('Year').size().reset_index(name='Total Shootings')
    gov = pd.DataFrame({
        'Year': [i for i in range(2014, 2025)],
        'y1': [0]*11, 
        'y2': [0]*11,
        'governement': ['Democratic']*3 + ['Republican']*5 + ['Democratic']*3
    })


    chart_gov = alt.Chart(gov).mark_area().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('y1:Q', title='Total Shootings', scale=alt.Scale(domain=(200, 720))),
        y2='y2:Q',
        color=alt.Color('governement', legend=alt.Legend(
            orient='top-left', 
            legendX=130, legendY=-100,  # Ajusta la posició de la llegenda
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            titleAnchor='middle'  # Centra el títol dins de la llegenda
        ), scale=alt.Scale(domain=['Democratic', 'Republican'], range=['#3182bd', '#d7301f']))
    )
    df_shootings = MassShootings
    # Converteix la data a un format de data de pandas
    df_shootings['Incident Date'] = pd.to_datetime(df_shootings['Incident Date'])

    # Extreu l'any de la data de l'incident
    df_shootings['Year'] = df_shootings['Incident Date'].dt.year

    # Agrupa per any i compta el nombre de tirotejos
    shootings_per_year = df_shootings.groupby('Year').size().reset_index(name='Total Shootings')

    # Crea el gràfic de línia amb Altair
    chart_ms = alt.Chart(shootings_per_year).mark_line(
        color='black',
        point=alt.OverlayMarkDef(filled=True, fill="black"),
        strokeWidth=2.5).encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0,grid=False)),  # Usa ':O' per especificar que l'eix X és ordinal
        y=alt.Y('Total Shootings:Q', title='Total Shootings').scale(domain=(250,710))
    ).properties(
        title='Total Shootings per Year in the USA',
        width=500,
        height=400
    )


    rep = alt.Chart().mark_rect(color=' #ec7063 ', opacity=1).encode(
        x=alt.value(160),
        y=alt.value(0),
        x2=alt.value(341),
        y2=alt.value(400))

    dem1 = alt.Chart().mark_rect(color=' #5dade2  ', opacity=1).encode(
        x=alt.value(0),
        y=alt.value(0),
        x2=alt.value(160.5),
        y2=alt.value(400))

    dem2 = alt.Chart().mark_rect(color=' #5dade2  ', opacity=1).encode(
        x=alt.value(341.2),
        y=alt.value(0),
        x2=alt.value(500),
        y2=alt.value(400))

    # Background rectangles
    background = alt.layer(
        dem1, rep, dem2
    )

    y_values = pd.DataFrame({'y': list(range(0, 701, 50))})

    # Crear les línies utilitzant mark_rule
    lines = alt.Chart(y_values).mark_rule(color='black', size=0.8, opacity=0.5).encode(
        y=alt.Y('y:Q',title=None, axis=None)
    )

    # Line charts layered on top of the background rectangles
    chart_with_background = alt.layer(
        background,
        lines,
        chart_ms,
        chart_gov
    ).properties(
        title='Total Shootings per Year in the USA',
        width=500,
        height=400
    ).resolve_scale(
        y='independent'
    )



    # Crear una configuració per a l'eix
    chart_with_background = chart_with_background.configure_axisX(
        grid=False  # Desactiva les línies de la graella verticals
    ).configure_axisY(
        grid=True,         # Activa les línies de la graella horitzontals
        gridColor='grey', # Defineix el color de les línies horitzontals
        gridWidth=1.1
    )
    
    # Calcular la mitjana de tirotejos per mes
    monthly_avg = monthly_shootings.groupby('Month')['Total Shootings'].mean().reset_index()

    # Afegir els noms dels mesos en anglès
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg['Month Name'] = [months[m-1] for m in monthly_avg['Month']]

    # Crear el heatmap en format vertical
    heatmap = alt.Chart(monthly_avg).mark_rect().encode(
        y=alt.Y('Month Name:N', sort=months, title=None),  # Canviar a l'eix Y
        color=alt.Color('Total Shootings:Q',
                        scale=alt.Scale(scheme='reds'),legend=None),
        tooltip=[
            alt.Tooltip('Month Name:N', title='Month'),
            alt.Tooltip('Total Shootings:Q', title='Average', format='.1f')
        ]
    ).properties(
        width=40,
        height=300,
        title={
            "text":['Average month','ditribution'],
            "dy": -20,
            "fontSize": 16
            }
    )

    text = alt.Chart(monthly_avg).mark_text(
        baseline='middle',
        color='white'
    ).encode(
        y=alt.Y('Month Name:N', sort=months),
        text=alt.Text('Total Shootings:Q', format='.1f')
    )

    # Combinar el heatmap amb el text
    heatmap_month_distribution = (heatmap + text)
    return chart_with_background

    '''combined_chart = alt.hconcat(
        chart_with_background,
        heatmap_month_distribution
    ).resolve_scale(
        color='independent'
    ).configure_axis(
        labelAngle=0,
        labelFontSize=12
    ).configure_title(
        fontSize=14,
        anchor='middle'
    )

    return combined_chart'''


q3 = chart_Q3()

q4 = chart_Q4()

st.set_page_config(
    page_title="Gun Violence in the USA",layout="wide"
)

st.markdown("<h1 style='text-align: center; color: black;'>Gun Violence in the USA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>"+
            "Laia Mogas & Pau Mateo"+
            "</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)



col1.altair_chart(q3,use_container_width=True)

col1.altair_chart(q3,use_container_width=True)

col2.altair_chart(q4, use_container_width=True)

col2.altair_chart(q4, use_container_width=True)


