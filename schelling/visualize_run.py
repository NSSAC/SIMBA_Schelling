import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

geofr = pd.read_pickle("./pickles/geofr.pckl")
synthfr = pd.read_pickle("./pickles/synthfr.pckl")
base = geofr.plot(edgecolor = 'black', zorder = 0, color = 'lightgray')

class Visualizer:
    def generateImage(self, state):
        visfr = pd.merge(state, synthfr[["hid", "hh_race"]], how="left", left_on="hid", right_on="hid")
        visfr = pd.merge(visfr, synthfr[["lid", "geometry"]], how="left", left_on="lid", right_on="lid")
        visfr = gpd.GeoDataFrame(visfr, geometry = visfr['geometry'])
        print(visfr.head())
        visfr.plot(ax = base, column = 'hh_race', marker = 'o', markersize = 1, zorder = 10, cmap = 'Set1' , legend = False)
        plt.savefig("./img/out", dpi = 1000)
        
