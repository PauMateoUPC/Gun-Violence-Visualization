import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data


# read csv files
MassShootings = pd.read_csv("datasets/MassShootingsComplete_FIPS.csv")
df_shootings = MassShootings
ShoolIncidents = pd.read_csv("datasets/SchoolIncidents_FIPS.csv")
df_GunViolence_csv = pd.read_csv("datasets/GunViolenceCompleteData.csv")

#define 
global_height = 400
global_width = 500


def chart_Q1(k:int) -> alt.Chart:
    df_GunViolence = pd.read_csv("datasets/GunViolenceCompleteData.csv")


    df_GunViolence = (
        df_GunViolence.groupby(['FIPS', 'County', 'State', 'Year'])
        .agg({
            'Population': 'first',  # Tomar el primer valor disponible de Population
            'Shootings': 'sum'      # Sumar los valores de Shootings
        })
        .reset_index()
    )
    # agrupar per state
    df_GunViolence = df_GunViolence.groupby(['State', 'Year'])[['Shootings', 'Population']].sum().reset_index()
    df_GunViolence['Ratio State'] = df_GunViolence['Shootings'] / df_GunViolence['Population'] * 1000000 # ratio entre shootings i population

    # mean ratio for years
    df_GunViolence = df_GunViolence.groupby('State')['Ratio State'].mean().reset_index()


    elections_republican = {'Alabama': 4, 'Alaska': 4, 'Arizona': 3, 'Arkansas': 4, 'California': 0, 'Colorado': 0, 'Connecticut': 0, 'Delaware': 0, 'District of Columbia': 0, 'Florida': 3, 'Georgia': 3, 'Hawaii': 0, 'Idaho': 4, 'Illinois': 0, 'Indiana': 4, 'Iowa': 3, 'Kansas': 4, 'Kentucky': 4, 'Louisiana': 4, 'Maine': 0, 'Maryland': 0, 'Massachusetts': 0, 'Michigan': 2, 'Minnesota': 0, 'Mississippi': 4, 'Missouri': 4, 'Montana': 4, 'Nebraska': 4, 'Nevada': 1, 'New Hampshire': 0, 'New Jersey': 0, 'New Mexico': 0, 'New York': 0, 'North Carolina': 4, 'North Dakota': 4, 'Ohio': 3, 'Oklahoma': 4, 'Oregon': 0, 'Pennsylvania': 2, 'Rhode Island': 0, 'South Carolina': 4, 'South Dakota': 4, 'Tennessee': 4, 'Texas': 4, 'Utah': 4, 'Vermont': 0, 'Virginia': 0, 'Washington': 0, 'West Virginia': 4, 'Wisconsin': 2, 'Wyoming': 4}
    mapping = {
        4: 'Republicans won the last 4 elections',
        3: 'Republicans won 3 of the last 4 elections',
        2: 'Republicans won 2 and Democrats won 2 of the last 4 elections',
        1: 'Democrats won 3 of the last 4 elections',
        0: 'Democrats won the last 4 elections'
    }

    for state in elections_republican.keys():
        elections_republican[state] = mapping[elections_republican[state]]


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

    chart_state = alt.Chart(top_k_states).mark_bar().encode(
        alt.X('Ratio State:Q'),
        alt.Y('State:N', sort='-x'),
        alt.Color('Republican Vote:O', 
                scale=alt.Scale(domain=['Democrats won the last 4', 'Democrats won 3', 'Rep won 2, Dem won 2', 'Republicans won 3', 'Republicans won the last 4'],
                                range=['#0000FF', '#ADD8E6', '#800080', '#FF6666', '#FF0000']),
                title='Majoritary Vote (last 4 elections)',
                legend = alt.Legend(orient='bottom-right')
        )
    ).properties(title = f'Top {k} States by Mass shootings per inhabitant',
                 height = 415,
                 width = 500).configure_legend(
    orient='right',  # La llegenda a la dreta
    padding=10,      # Espai addicional
    titleFontSize=14,
    labelFontSize=14
    )


    return chart_state


def chart_Q3() -> alt.Chart:
    df_GunViolence = df_GunViolence_csv.fillna(0)


    df_GunViolence = df_GunViolence[df_GunViolence['Year']==2023]
    df_GunViolence = df_GunViolence.groupby(['State'])[['Shootings', 'School Incidents', 'Population']].agg({
        'Shootings': 'sum',
        'School Incidents': 'sum',
        'Population': 'first'
    }).reset_index()

    df_GunViolence['Ratio Shootings'] = df_GunViolence['Shootings']*1000000 / df_GunViolence['Population']
    df_GunViolence['Ratio School Incidents'] = df_GunViolence['School Incidents'] *1000000/ df_GunViolence['Population']


    scatter_plot = alt.Chart(df_GunViolence).mark_circle(size=100).encode(
        y=alt.Y('Ratio Shootings:Q', title='Ratio of Shootings per Population'),
        x=alt.X('Ratio School Incidents:Q', title='Ratio of School Incidents per Population'),
        tooltip=['State', 'Shootings', 'School Incidents', 'Population'] 
    ).properties(
        width=600,
        height=global_height+115,
        title="Ratio of Shootings per Population by State"
    )

    df_GunViolence['Label'] = df_GunViolence.apply(
        lambda x: x['State'] if (x['Ratio Shootings'] >= 80 or x['Ratio School Incidents']>=100)  else '', axis=1
    )
    # Afegir les etiquetes
    # Ajustar les etiquetes individualment
    # Etiquetes per a "South Carolina" a dalt a l'esquerra
    text_labels_sc = alt.Chart(df_GunViolence[df_GunViolence['State'] == 'South Carolina']).mark_text(
        align='center',  # Alineació a l'esquerra
        dx=-20,  # Desplaçament cap a l'esquerra
        dy=-15,  # Desplaçament cap amunt
        size=14  # Mida del text augmentada
    ).encode(
        y=alt.Y('Ratio Shootings:Q'),
        x=alt.X('Ratio School Incidents:Q'),
        text='State'
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

    # Combinar el gràfic de dispersió amb les etiquetes
    final_plot = scatter_plot + text_labels_sc + text_labels_others

    return final_plot


def chart_Q4() -> alt.HConcatChart:
    MassShootings['Incident Date'] = pd.to_datetime(MassShootings['Incident Date'])
    MassShootings['Year'] = MassShootings['Incident Date'].dt.year
    MassShootings['Month'] = MassShootings['Incident Date'].dt.month
    monthly_shootings = MassShootings[MassShootings['Year']>2014].groupby(['Year', 'Month']).size().reset_index(name='Total Shootings')
    monthly_avg = monthly_shootings.groupby('Month')['Total Shootings'].mean().reset_index()
    df_GunViolence = pd.read_csv('datasets/GunViolenceCompleteData.csv')

    df_GunViolence = df_GunViolence.groupby('Year')["Shootings"].sum().reset_index()
    df_GunViolence = df_GunViolence[df_GunViolence['Year']<2024]
    df_GunViolence['Year'] = pd.to_datetime(df_GunViolence['Year'], format='%Y')

    RED = '#f5b7b1'
    BLUE = '#aed6f1' 

    D = alt.Scale(domain=(1000,10000))

    chart_ms = alt.Chart(df_GunViolence).mark_line(
        color='black',
        point=alt.OverlayMarkDef(filled=True, fill="black"),
        strokeWidth=2.5
    ).encode(
        x=alt.X('Year:T', timeUnit='year', title='Year'),
        y=alt.Y('Shootings:Q', title='Total Shootings', scale=D)
    ).properties(
        title={
            "text": ['Total Shootings per Year in the USA'],
            "fontSize": 16,
        },
        width=500,
        height=global_height
    )

        #we keep this just for the legend
    gov = pd.DataFrame({
        'governement':['Republican', 'Democratic']
    })

    chart_gov = alt.Chart(gov).mark_area().encode(
        x=alt.X('Year:T', title='Year', axis=alt.Axis(labelAngle=0)),
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
        ), scale=alt.Scale(domain=['Democratic', 'Republican'], range=[BLUE, RED]))
    )


    df_dem1 = pd.DataFrame({
        'x1': 2014,
        'x2': 2017,
        'y1': [250]*2, 
        'y2': [700]*2,
        'governement': ['Democratic']*2
    })
    df_dem1['x1'] = pd.to_datetime(df_dem1['x1'], format ='%Y')
    df_dem1['x2'] = pd.to_datetime(df_dem1['x2'], format ='%Y')


    df_rep = pd.DataFrame({
        'x1': 2017,
        'x2': 2021,
        'y1': [250]*2, 
        'y2': [700]*2,
        'governement': ['Republican']*2
    })
    df_rep['x1'] = pd.to_datetime(df_rep['x1'], format ='%Y')
    df_rep['x2'] = pd.to_datetime(df_rep['x2'], format ='%Y')

    df_dem2 = pd.DataFrame({
        'x1': 2021,
        'x2': 2023,
        'y1': [250]*2, 
        'y2': [700]*2,
        'governement': ['Democratic']*2
    })
    df_dem2['x1'] = pd.to_datetime(df_dem2['x1'], format ='%Y')
    df_dem2['x2'] = pd.to_datetime(df_dem2['x2'], format ='%Y')

    # Rectangles for government background
    dem1 = alt.Chart(df_dem1).mark_rect(color=BLUE, opacity=1).encode(
        x=alt.X('x1:T', title=None),  # No title for X axis here
        x2='x2:T',
        y=alt.Y('y1:Q', scale=D, axis=None),  # No Y axis for background
        y2=alt.Y2('y2:Q')
    )

    rep = alt.Chart(df_rep).mark_rect(color=RED, opacity=1).encode(
        x=alt.X('x1:T', title=None),
        x2='x2:T',
        y=alt.Y('y1:Q', scale=D, axis=None),
        y2=alt.Y2('y2:Q')
    )

    dem2 = alt.Chart(df_dem2).mark_rect(color=BLUE, opacity=1).encode(
        x=alt.X('x1:T', title=None),
        x2='x2:T',
        y=alt.Y('y1:Q', scale=D, axis=None),
        y2=alt.Y2('y2:Q')
    )

    # Manual gridlines
    y_values = pd.DataFrame({'y': list(range(250, 701, 50))})
    lines = alt.Chart(y_values).mark_rule(color='gray', size=0.8, opacity=0.5).encode(
        y=alt.Y('y:Q', scale=D, title=None, axis=None)
    )


    # Combine layers with shared y-scale
    chart_with_background = alt.layer(
        dem1,       # Background rectangles
        dem2,
        rep,
        lines,     # Gridlines
        chart_ms,   # Main line chart
        chart_gov
    ).properties(
        width=500,
        height=global_height
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
        tooltip=[
            alt.Tooltip('Month Name:N', title='Month'),
            alt.Tooltip('Total Shootings:Q', title='Average', format='.1f')
        ]
    ).properties(
        width=40,
        height=global_height,
        title={
            "text":['Average month','ditribution'],
            "dy": 0,
            "fontSize": 16
            }
    )

    text = alt.Chart(monthly_avg).mark_text(
        baseline='middle',
        color='black'
    ).encode(
        y=alt.Y('Month Name:N', sort=months),
        text=alt.Text('Total Shootings:Q', format='.1f')
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




# Agrupar per estat i comptar el nombre de tirotejos per estat
df_shootings['StateCode'] = df_shootings['FIPS'].apply(lambda x: str(x)[:2])
df_shootings_grouped = df_shootings.groupby(['StateCode']).size().reset_index(name='Total Shootings')


# Carregar la geometria dels estats dels EUA (mitjançant l'URL de topojson)
states = alt.topo_feature(data.us_10m.url, feature='states')

# Crear el coroplèstic map amb Altair
map_chart = alt.Chart(states).mark_geoshape().encode(
    color=alt.Color('Total Shootings:Q', scale=alt.Scale(scheme='reds'), title='Total Shootings'),
    tooltip=['properties.name:N', 'Total Shootings:Q']  # Mostra el nom de l'estat i el nombre de tirotejos
).transform_lookup(
    lookup='id',  # Identificador dels estats
    from_=alt.LookupData(df_shootings_grouped, 'StateCode', ['Total Shootings'])  # Unir per estat
).project(
    type='albersUsa'
).properties(
    width=800, height=global_height,
    title="Total Shootings per State in the USA"
)


col1.altair_chart(q1,use_container_width=True)
col1.altair_chart(q3,use_container_width=False)
col2.altair_chart(map_chart, use_container_width=True)
col2.altair_chart(q4, use_container_width=False)

