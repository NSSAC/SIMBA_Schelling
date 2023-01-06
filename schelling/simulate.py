import geopandas as gpd
import pandas as pd
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scipy.spatial import KDTree
import networkx as nx
import random
import copy

print("Reading Graph")
g = nx.read_gpickle('graph.pkl')

def get_average_income(node):
    node_income = g.nodes[node]["income"]
    neighbor_income = []
    for neighbor in g.neighbors(node):
        neighbor_income.append(g.nodes[neighbor]["income"])
    income = (sum(neighbor_income) / len(neighbor_income)) if len(neighbor_income) != 0 else node_income
    g.nodes[node]["average_income"] = income
    return income

def get_race_ratio(node, race):
    neighbor_race = []
    neighbor_race.append(g.nodes[node]["race"])
    for neighbor in g.neighbors(node):
        neighbor_race.append(g.nodes[neighbor]["race"])
    return (neighbor_race.count(race) / len(neighbor_race)) if len(neighbor_race) != 0 else 1

for i in range(5):
    print("Determining Satisfaction")
    for node in g.nodes():
        #node_income = g.nodes[node]["income"]
        node_race = g.nodes[node]["race"]
        average_income = get_average_income(node)
        ratio = get_race_ratio(node, node_race)
        if(ratio >= 0.3):
            g.nodes[node]["happy"] = True
        else:
            g.nodes[node]["happy"] = False

    print("Moving")
    temp_g = g.copy()
    movers = [n for n, h in temp_g.nodes(data=True) if h['happy'] == False]
    vacant_nodes = copy.deepcopy(movers)
    for mover in movers:
        random.shuffle(vacant_nodes)
        mover_hid = g.nodes[mover]["hid"]
        mover_race = g.nodes[mover]["race"]
        mover_income = g.nodes[mover]["income"]
        mover_geo = g.nodes[mover]["geometry"]

        race_pref = [n for n in vacant_nodes if get_race_ratio(n, mover_race) >= 0.3]
        income_pref = [n for n in race_pref if (g.nodes[n]["average_income"] - 5000 < mover_income < g.nodes[n]["average_income"] + 10000)]

        if(len(income_pref) != 0):
            valid_node = income_pref[0]
        elif(len(race_pref) != 0):
            valid_node = race_pref[0]
        else:
            if(temp_g.nodes[mover]['happy'] == True):
                valid_node = vacant_nodes[0]
            else:
                valid_node = mover

        temp_g.nodes[valid_node]["hid"] = mover_hid
        temp_g.nodes[valid_node]["race"] = mover_race
        temp_g.nodes[valid_node]["income"] = mover_income
        temp_g.nodes[valid_node]["geometry"] = mover_geo
        temp_g.nodes[valid_node]["happy"] = True

        vacant_nodes.remove(valid_node)
        print("Remaining:", len(vacant_nodes))

    g = temp_g
    nx.write_gpickle(g, "iterations/iter%d.pkl" %i)
