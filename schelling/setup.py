import geopandas as gpd
import pandas as pd
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scipy.spatial import KDTree
import networkx as nx

g = nx.Graph()

def label_race(row):
    racelist = row['race']
    if(len(set(racelist)) == 1):
        return racelist[0]
    else:
        return 9
    

print("Reading Map Geometry")
geofr = gpd.read_file("tl_2017_51_tabblock10.zip")
geofr[['COUNTYFP10', 'TRACTCE10', 'BLOCKCE10', 'GEOID10']] = geofr[['COUNTYFP10', 'TRACTCE10', 'BLOCKCE10', 'GEOID10']].apply(pd.to_numeric)
geofr = geofr[geofr['COUNTYFP10'] == 760]
geofr = geofr.drop(['STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'NAME10', 'BLOCKCE10', 'MTFCC10', 'UR10', 'UACE10', 'UATYPE', 'FUNCSTAT10', 'ALAND10', 'AWATER10', 'INTPTLAT10', 'INTPTLON10'], axis = 1)
geofr = geofr.reset_index(drop=True)
geofr['GEOID10'] = geofr['GEOID10'].astype(np.int64)
geofr = geofr.to_crs(epsg = 2925)
geofr.to_pickle('geofr.pkl') 
print(geofr.info())

print("Reading Household Data")
housefr = pd.read_csv("household.csv", usecols = ['admin2','admin3', 'hid', 'hh_income', 'residence_longitude', 'residence_latitude'])
housefr = housefr[housefr['admin2'] == 760]
housefr = housefr.drop(['admin2', 'admin3'], axis = 1)
print(housefr.info())

print("Reading Person Data")
personfr = pd.read_csv("person.csv", usecols = ['hid', 'race'])
print(personfr.info())

print("Merging Tables")
print("Merging Race")

raceser = personfr.groupby('hid')['race'].apply(list)
synthfr = pd.merge(housefr, raceser, how  = 'left', left_on = 'hid', right_on = 'hid')
synthfr['hh_race'] = synthfr.apply(lambda row: label_race(row), axis=1)
print("Converting Geometry")
synthfr = gpd.GeoDataFrame(synthfr, geometry = gpd.points_from_xy(synthfr['residence_longitude'], synthfr['residence_latitude'])) 
synthfr = synthfr.set_crs(epsg = 4269)
synthfr = synthfr.to_crs(epsg = 2925)
synthfr['lid'] = range(0, len(synthfr))
synthfr[['lid','geometry']] = synthfr[['lid','geometry']].sample(frac = 1).values

print("Finding Neighbors")

tree = KDTree(list(zip(synthfr.geometry.x, synthfr.geometry.y)))

pairs = tree.query_pairs(500)
synthfr['neighbors'] = np.empty((len(synthfr), 0)).tolist()

g = nx.Graph()
for index, row in synthfr.iterrows():
    g.add_node(row['lid'], hid = row['hid'], race = row['hh_race'], income = row['hh_income'], geometry = row['geometry'])

lid = synthfr.columns.get_loc("lid")
nb = synthfr.columns.get_loc("neighbors")
for (i, j) in pairs:
    g.add_edge(synthfr.iloc[i, lid], synthfr.iloc[j, lid])
    synthfr.iloc[i, nb].append(synthfr.iloc[j, lid])
    synthfr.iloc[j, nb].append(synthfr.iloc[i, lid])
synthfr = synthfr.drop(['residence_longitude', 'residence_latitude', 'race'], axis = 1)

print(synthfr.info())
synthfr.to_pickle('synthfr.pkl')
nx.write_gpickle(g,'graph.pkl')
