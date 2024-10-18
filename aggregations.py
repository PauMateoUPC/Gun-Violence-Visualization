import pandas as pd

# com computem ratio?

# avg(ratios) per anys


# state, population, year


# input: MassShootingsComplete.csv
PATH_COMPLETE_SHOOTINGS = 'datasets/MassShootingsComplete.csv'

'''
Q1 (barchart)
county, state, ratio, year
fem agregacio avg groupby year
'''


def get_county_ratio():
    df = pd.read_csv(PATH_COMPLETE_SHOOTINGS)
    

'''
Q2 (choropleth)
county, state, ratio, year
'''

'''
Q3 (scatterplot)
idees pel notebook:
- eix x: school
- eix y: mass shootings
- color: year
- point: state in year
county, state, mass shootings, school, year
'''

'''
Q4 (linechart)
county, state, mass shootings, year
'''


