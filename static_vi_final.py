import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data
import json
import urllib.request
import geopandas as gpd
import urllib.request
import numpy as np

# read csv files
MassShootings = pd.read_csv("datasets/MassShootingsComplete_FIPS.csv")
df_shootings = MassShootings
df_GunViolence_csv = pd.read_csv("datasets/GunViolenceCompleteData.csv")

#define 
global_height = 400
global_width = 500


def chart_Q1(k:int) -> alt.Chart:
    df_GunViolence = pd.read_csv("datasets/GunViolenceCompleteData.csv")


    df_GunViolence = df_GunViolence_csv

    # agrupar per state
    df_GunViolence = df_GunViolence.groupby(['State', 'Year', 'Population'])[['Shootings']].sum().reset_index()
    df_GunViolence['Ratio State'] = df_GunViolence['Shootings'] / df_GunViolence['Population'] * 1000000 # ratio entre shootings i population

    # mean ratio for years
    df_GunViolence = df_GunViolence.groupby('State')['Ratio State'].mean().reset_index()

    # mean ratio for years
    df_GunViolence = df_GunViolence.groupby('State')['Ratio State'].mean().reset_index()

    elections_republican = {'Alabama': 4, 'Alaska': 4, 'Arizona': 3, 'Arkansas': 4, 'California': 0, 'Colorado': 0, 'Connecticut': 0, 'Delaware': 0, 'District of Columbia': 0, 'Florida': 3, 'Georgia': 3, 'Hawaii': 0, 'Idaho': 4, 'Illinois': 0, 'Indiana': 4, 'Iowa': 3, 'Kansas': 4, 'Kentucky': 4, 'Louisiana': 4, 'Maine': 0, 'Maryland': 0, 'Massachusetts': 0, 'Michigan': 2, 'Minnesota': 0, 'Mississippi': 4, 'Missouri': 4, 'Montana': 4, 'Nebraska': 4, 'Nevada': 1, 'New Hampshire': 0, 'New Jersey': 0, 'New Mexico': 0, 'New York': 0, 'North Carolina': 4, 'North Dakota': 4, 'Ohio': 3, 'Oklahoma': 4, 'Oregon': 0, 'Pennsylvania': 2, 'Rhode Island': 0, 'South Carolina': 4, 'South Dakota': 4, 'Tennessee': 4, 'Texas': 4, 'Utah': 4, 'Vermont': 0, 'Virginia': 0, 'Washington': 0, 'West Virginia': 4, 'Wisconsin': 2, 'Wyoming': 4}

    mapping = {
        4: 'Republicans won the last 4',
        3: 'Republicans won 3',
        2: 'Republicans won 2, Democrats won 2',
        1: 'Democrats won 3',
        0: 'Democrats won the last 4'

    }
    for state in elections_republican.keys():
        elections_republican[state] = mapping[elections_republican[state]]


    df_GunViolence['Republican Vote'] = df_GunViolence['State'].map(elections_republican)


    k = 10

    top_k_states = df_GunViolence.nlargest(k, 'Ratio State')
    RED = '#f5b7b1'
    SEMIRED = '#fadbd8'
    BLUE = '#aed6f1'

    chart_state = alt.Chart(top_k_states).mark_bar().encode(
        alt.X('Ratio State:Q'),
        alt.Y('State:N', sort='-x'),
        alt.Color('Republican Vote:O', 
                scale=alt.Scale(domain=['Democrats won the last 4', 'Republicans won 3', 'Republicans won the last 4'], range=[BLUE, SEMIRED, RED]),
                title='Majoritary Vote (last 4 elections)',
                legend = alt.Legend(orient='bottom-right',
                                    strokeColor='gray',
                                    legendX=130, legendY=-100,
                                    fillColor='#EEEEEE',
                                    padding=10,
                                    cornerRadius=10,
                                    titleAnchor='middle')
        )
    ).properties(title = f'Top {k} States by Mass shootings per 1M Inhabitants',
                 height = 420,
                 width = 500).configure_legend(
    orient='right',  # La llegenda a la dreta
    padding=10,      # Espai addicional
    titleFontSize=14,
    labelFontSize=14
    ).configure_title(
        fontSize=16,
        anchor='middle'
    )


    return chart_state


def get_county_data_Q2() -> pd.DataFrame:
    counties_geojson_url = data.us_10m.url
    gdf_counties = gpd.read_file(counties_geojson_url, layer='counties')

    gdf_counties['centroid'] = gdf_counties.geometry.centroid
    gdf_counties['Longitude'] = gdf_counties['centroid'].x
    gdf_counties['Latitude'] = gdf_counties['centroid'].y

    df_coords = gdf_counties[['id', 'Longitude', 'Latitude']].rename(columns={'id': 'FIPS'})
    df_coords['FIPS'] = df_coords['FIPS'].astype(str)

    df_counties = pd.read_csv('datasets/GunViolenceCompleteData.csv')
    df_counties.head()
    df_counties.loc[df_counties['FIPS'] == 11000, 'FIPS'] = 11001

    # aggregate by year and state and county
    df_counties = df_counties.groupby(['FIPS', 'State', 'County', 'Year', 'Population'])[['Shootings']].sum().reset_index()

    df_counties['Ratio County'] = df_counties['Shootings'] / df_counties['Population'] * 1000000 # ratio entre shootings i population
    df_counties = df_counties.groupby(['FIPS', 'County'])['Ratio County'].mean().reset_index()


    df_counties['FIPS'] = df_counties['FIPS'].astype(str)

    df_combined = pd.merge(
        df_counties, df_coords, how='left', left_on='FIPS', right_on='FIPS'
    )
    df_combined['Log Ratio County'] = df_combined['Ratio County'].apply(lambda x: np.log(x + 1))

    df_combined = df_combined[(df_combined['County'] != 'Portsmouth city') & (df_combined['County'] != 'Petersburg city') & (df_combined['County'] != 'Manassas city') & (df_combined['County'] != 'Manassas city')]

    return df_combined[df_combined['Ratio County'] > 0]


def get_state_data_Q2() -> pd.DataFrame:
    url = data.us_10m.url
    
    with urllib.request.urlopen(url) as response:
        us_10m = json.load(response)

    df_GunViolence = df_GunViolence_csv

    df_GunViolence['State Code'] = df_GunViolence_csv['FIPS'].apply(lambda x: str(x)[:2])

    # fips data was not well formatted, manually fix it
    df_GunViolence.loc[df_GunViolence['State'] == 'Alabama', 'State Code'] = '01'
    df_GunViolence.loc[df_GunViolence['State'] == 'Alaska', 'State Code'] = '02'
    df_GunViolence.loc[df_GunViolence['State'] == 'Arizona', 'State Code'] = '04'
    df_GunViolence.loc[df_GunViolence['State'] == 'Arkansas', 'State Code'] = '05'
    df_GunViolence.loc[df_GunViolence['State'] == 'California', 'State Code'] = '06'
    df_GunViolence.loc[df_GunViolence['State'] == 'Colorado', 'State Code'] = '08'


    df_GunViolence = df_GunViolence.groupby(['State Code', 'State', 'Population', 'Year'])[['Shootings']].sum().reset_index()
    df_GunViolence['Ratio State'] = df_GunViolence['Shootings'] / df_GunViolence['Population'] * 1000000
    df_GunViolence = df_GunViolence.groupby(['State', 'State Code'])['Ratio State'].mean().reset_index()

    df_GunViolence['State Code'] = df_GunViolence['State Code'].astype(int)
    df_GunViolence['Log Ratio State'] = df_GunViolence['Ratio State'].apply(lambda x: np.log(x + 1))
    df_GunViolence['Colors'] = df_GunViolence['Ratio State']
    df_GunViolence.loc[df_GunViolence['State'] == 'District of Columbia', 'Colors'] = 5
    return df_GunViolence


def chart_Q2() -> alt.Chart:
    
    df_combined = get_county_data_Q2()
    df_GunViolence = get_state_data_Q2()
    states = alt.topo_feature(data.us_10m.url, feature='states')

    map_chart = alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('Colors:Q', scale=alt.Scale(scheme='oranges'), title='Ratio State'),
        tooltip=[
                alt.Tooltip('State:N', title='Name'),
                alt.Tooltip('Colors:Q', title='Ratio State')
        ]).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_GunViolence, 'State Code', ['Colors', 'State'])  # Unir per estat
    ).project(
        type='albersUsa'
    ).properties(
        width=800, height=500,
        title="Ratio per State in the USA"
    )

    points_chart = alt.Chart(df_combined).mark_circle().encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        size=alt.Size('Ratio County:Q', scale=alt.Scale(range=[15, 80]), title='Ratio County'),
        color = alt.condition(
        alt.datum['State'] == 'District of Columbia',
        alt.value('red'),
        alt.value('black')
    ),
        tooltip=[
            alt.Tooltip('County:N', title='County'),
            alt.Tooltip('Ratio County:Q', title='Shootings')
        ]
    )

    final_chart = alt.layer(
        map_chart,
        points_chart
    ).resolve_scale(
        color='independent'
    ).properties(
    width=800, height=global_height,
    title="Shootings per 1M Inhabitants per State and County"
    ).configure_title(
            fontSize=16,
            anchor='middle'
    )

    return final_chart


def chart_Q3() -> alt.Chart:
    # Agrupar per estat i comptar el nombre total de tirotejos per estat
    df_GunViolence = df_GunViolence_csv.fillna(0)

    df_GunViolence = df_GunViolence[df_GunViolence['Year'] == 2023]
    df_GunViolence = df_GunViolence.groupby(['State'])[['Shootings', 'School Incidents', 'Population']].agg({
        'Shootings': 'sum',
        'School Incidents': 'sum',
        'Population': 'sum'
    }).reset_index()

    df_GunViolence['Ratio Shootings'] = df_GunViolence['Shootings']*1000000 / df_GunViolence['Population']
    df_GunViolence['Ratio School Incidents'] = df_GunViolence['School Incidents'] *1000000/ df_GunViolence['Population']


    scatter_plot = alt.Chart(df_GunViolence).mark_circle(size=100).encode(
        y=alt.Y('Ratio Shootings:Q', title='Ratio of Shootings per 1M inhabitants'),
        x=alt.X('Ratio School Incidents:Q', title='Ratio of School Incidents per 1M inhabitants'),
            color=alt.condition(
            alt.datum['Ratio Shootings'] > 3,  # Condició per al color
            alt.value('grey'),  # Color si es compleix la condició
            alt.value('black')  # Color si no es compleix la condició
        ),
        tooltip=['State', 'Shootings', 'School Incidents', 'Population'] 
    ).properties(
        width=800,
        height=515,
        title="Shootings vs School Incidents per 1M inhabitants by State (2023)"
    )

    ##### scatter plot to compute the regression line without outliers
    scatterplot_without_outliers = alt.Chart(df_GunViolence[df_GunViolence['Ratio Shootings'] < 3]).mark_circle(size=100).encode(
        y=alt.Y('Ratio Shootings:Q', title=''),
        x=alt.X('Ratio School Incidents:Q', title=''),
        tooltip=['State', 'Shootings', 'School Incidents', 'Population'] 
    ).properties(
        width=800,
        height=515,
        title="Ratio of Shootings per Population by State"
    )


    df_GunViolence['Label'] = df_GunViolence.apply(
        lambda x: x['State'] if (x['Ratio Shootings'] >= 3 or x['Ratio School Incidents']>=100)  else '', axis=1
    )


    # Etiquetes per a la resta dels estats a baix a l'esquerra
    text_labels_others = alt.Chart(df_GunViolence[(df_GunViolence['Label'] != '') & (df_GunViolence['State'] != 'South Carolina')]).mark_text(
        align='right',  # Alineació a la dreta
        dx=-7,  # Desplaçament cap a l'esquerra
        dy=14,  # Desplaçament cap avall
        size=14  # Mida del text augmentada
    ).encode(
        y=alt.Y('Ratio Shootings:Q'),
        x=alt.X('Ratio School Incidents:Q'),
        text='State'
    )


    # Crear una línia de regressió
    regression_line = scatterplot_without_outliers.transform_regression(
        'Ratio School Incidents', 'Ratio Shootings'
    ).mark_line(color='red')

    # Combinar el diagrama de dispersió i la línia de regressió
    final_chart = alt.layer(scatter_plot,
                            text_labels_others,
                            regression_line).configure_title(
        fontSize=16,
        anchor='middle'
    )

    return final_chart


def chart_Q4() -> alt.HConcatChart:
    MassShootings['Incident Date'] = pd.to_datetime(MassShootings['Incident Date'])
    MassShootings['Year'] = MassShootings['Incident Date'].dt.year
    MassShootings['Month'] = MassShootings['Incident Date'].dt.month
    monthly_shootings = MassShootings[MassShootings['Year'] > 2014].groupby(['Year', 'Month']).size().reset_index(name='Total Shootings')
    monthly_avg = monthly_shootings.groupby('Month')['Total Shootings'].mean().reset_index()
    
    df_GunViolence = pd.read_csv('datasets/GunViolenceCompleteData.csv')
    df_GunViolence = df_GunViolence.groupby('Year')["Shootings"].sum().reset_index()
    df_GunViolence = df_GunViolence[df_GunViolence['Year'] < 2024]
    df_GunViolence['Year'] = pd.to_datetime(df_GunViolence['Year'], format='%Y')

    RED = '#f5b7b1'
    BLUE = '#aed6f1' 

    D = alt.Scale(domain=(250,700))
    w = 450

    chart_ms = alt.Chart(df_GunViolence).mark_line(
        color='black',
        point=alt.OverlayMarkDef(filled=True, fill="black"),
        strokeWidth=2.5
    ).encode(
        x=alt.X('Year:T', timeUnit='year', title='Year'),
        y=alt.Y('Shootings:Q', title='Total Shootings', scale=D)
    ).properties(
        title={
            "text": ['Total Shootings per Year'],
            "fontSize": 16,
        },
        width=w,
        height=global_height
    )

    #we keep this just for the legend
    gov = pd.DataFrame({
        'government':['Republican', 'Democratic']
    })

    chart_gov = alt.Chart(gov).mark_area().encode(
        x=alt.X('Year:T', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('y1:Q', title='Total Shootings', scale=D,axis=None),
        y2='y2:Q',
        color=alt.Color('government', legend=alt.Legend(
            orient='top-left', 
            legendX=130, legendY=-100,  # Ajusta la posició de la llegenda
            strokeColor='gray',
            fillColor='#EEEEEE',
            padding=10,
            cornerRadius=10,
            titleAnchor='middle'  # Centra el títol dins de la llegenda
        ), scale=alt.Scale(domain=['Democratic', 'Republican'], range=[BLUE, RED]))
    )


    df_dem1 = pd.DataFrame({
        'x1': 2014,
        'x2': 2017,
        'y1': [250]*2, 
        'y2': [700]*2,
        'government': ['Democratic']*2
    })
    df_dem1['x1'] = pd.to_datetime(df_dem1['x1'], format ='%Y')
    df_dem1['x2'] = pd.to_datetime(df_dem1['x2'], format ='%Y')


    df_rep = pd.DataFrame({
        'x1': 2017,
        'x2': 2021,
        'y1': [250]*2, 
        'y2': [700]*2,
        'government': ['Republican']*2
    })
    df_rep['x1'] = pd.to_datetime(df_rep['x1'], format ='%Y')
    df_rep['x2'] = pd.to_datetime(df_rep['x2'], format ='%Y')

    df_dem2 = pd.DataFrame({
        'x1': 2021,
        'x2': 2023,
        'y1': [250]*2, 
        'y2': [700]*2,
        'government': ['Democratic']*2
    })
    df_dem2['x1'] = pd.to_datetime(df_dem2['x1'], format ='%Y')
    df_dem2['x2'] = pd.to_datetime(df_dem2['x2'], format ='%Y')

    # Rectangles for government background
    dem1 = alt.Chart(df_dem1).mark_rect(color=BLUE, opacity=1).encode(
        x=alt.X('x1:T', title='Year'),  # No title for X axis here
        x2='x2:T',
        y=alt.Y('y1:Q', scale=D, axis=None),  # No Y axis for background
        y2=alt.Y2('y2:Q'),
        tooltip=alt.value(None)
    )

    rep = alt.Chart(df_rep).mark_rect(color=RED, opacity=1).encode(
        x=alt.X('x1:T', title='Year'),
        x2='x2:T',
        y=alt.Y('y1:Q', scale=D, axis=None),
        y2=alt.Y2('y2:Q'),
        tooltip=alt.value(None)
    )

    dem2 = alt.Chart(df_dem2).mark_rect(color=BLUE, opacity=1).encode(
        x=alt.X('x1:T', title='Year'),
        x2='x2:T',
        y=alt.Y('y1:Q', scale=D, axis=None),
        y2=alt.Y2('y2:Q'),
        tooltip=alt.value(None)
    )

    # Manual gridlines
    y_values = pd.DataFrame({'y': [y for y in range(250, 701, 50)]})
    lines = alt.Chart(y_values).mark_rule(color='gray', size=0.8, opacity=0.5).encode(
        y=alt.Y('y:Q', scale=D, title='Year', axis=None),
        tooltip=alt.value(None)
    )


    line2 = pd.DataFrame({
        'x': [2019,2019],  # Coordenada fixa per la línia vertical
        'y': [294, 390],  # Rang de les coordenades en l'eix Y
    })

    line2['x'] = pd.to_datetime(line2['x'],  format='%Y')

    # Crear el gràfic amb Altair
    chart_line2 = alt.Chart(line2).mark_line(strokeWidth=1, color='black').encode(
        x=alt.X('x:T', timeUnit='year',title='Year'),  # Fixem la coordenada X
        y=alt.Y('y:Q', axis=None,scale=D),
        tooltip=alt.value(None)
    )

    text2 = pd.DataFrame({
        'x': [2019],
        'y': [280],
        'text': ["GVA reaches 7000+ sources"]
    })
    text2['x'] = pd.to_datetime(text2['x'], format = "%Y")

    chart_text2 = alt.Chart(text2).mark_text().encode(
        text="text",
        x = alt.X('x:T', timeUnit='year',title='Year'),
        y = alt.Y("y:Q", axis=None,scale=D)
    )

    # Combine layers with shared y-scale
    chart_with_background = alt.layer(
        dem1,       # Background rectangles
        dem2,
        rep,
        lines,     # Gridlines
        chart_ms,   # Main line chart
        chart_gov,
        chart_text2,
        chart_line2
    ).properties(
        width=w,
        height=400
    ).resolve_scale(
        y='independent'  # Enforce shared y-scale for all layers
    )


    # Afegir els noms dels mesos en anglès
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg['Month Name'] = [months[m-1] for m in monthly_avg['Month']]

    # Crear el heatmap en format vertical
    heatmap = alt.Chart(monthly_avg).mark_rect().encode(
        y=alt.Y('Month Name:N', sort=months, title=None),  # Canviar a l'eix Y
        color=alt.Color('Total Shootings:Q',
                        scale=alt.Scale(scheme='lightorange'),legend=None),
        tooltip=alt.value(None)
    ).properties(
        width=40,
        height=global_height,
        title={
            "text":['Monthly average of','shootings ditribution'],
            "dy": 0,
            "fontSize": 16
            }
    )

    text = alt.Chart(monthly_avg).mark_text(
        baseline='middle',
        color='black'
    ).encode(
        y=alt.Y('Month Name:N', sort=months),
        text=alt.Text('Total Shootings:Q', format='.1f'),
        tooltip=alt.value(None)
    )


    heatmap_month_distribution = (heatmap + text)

    combined_chart = alt.hconcat(
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

    return combined_chart





q1 = chart_Q1(13)

q2 = chart_Q2()

q3 = chart_Q3()

q4 = chart_Q4()

st.set_page_config(
    page_title="Gun Violence in the USA",layout="wide"
)

st.markdown("<h1 style='text-align: center; color: black;'>Gun Violence in the USA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>"+
            "Laia Mogas & Pau Mateo"+
            "</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>"+
            ""+
            "</p>", unsafe_allow_html=True)
col1, col2 = st.columns(2)




col1.altair_chart(q1,use_container_width=True)
col1.altair_chart(q3,use_container_width=True)
col2.altair_chart(q2, use_container_width=True)
col2.altair_chart(q4, use_container_width=True)

