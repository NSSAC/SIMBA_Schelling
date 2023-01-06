import numpy as np 
import pandas as pd 
import geopandas as gpd
import networkx as nx
import glob
import imageio
import matplotlib.pyplot as plt

geofr = pd.read_pickle('geofr.pkl')

def plot():
    print("Plotting")
    filenames = glob.glob("*iterations/*.pkl")
    filenames.sort()
    images = []
    i = 0
    for filename in filenames:
        g = nx.read_gpickle(filename)
        synthfr = pd.DataFrame.from_dict(dict(g.nodes(data=True)), orient='index')
        synthfr = gpd.GeoDataFrame(synthfr, geometry = synthfr['geometry'])
        base = geofr.plot(edgecolor = 'black', zorder = 0, color = 'lightgray')
        synthfr.plot(ax = base, column = 'race', marker = 'o', markersize = 1, zorder = 10, cmap = 'Set1' , legend = True)
        plt.title("t = %d"%i)
        plt.savefig("imgs/time%d.jpg" %i, dpi = 1000)
        i += 1

def create_gif():
    filenames = glob.glob("*imgs/*.jpg")
    filenames.sort()
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('imgs/full.gif', images, duration = 2)

plot()
create_gif()


