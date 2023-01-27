import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import networkx as nx
import random
import copy

class environment:
    def __init__(self):
        self.i = 0
        self.graph = nx.Graph()
        self.df = pd.DataFrame
        self.PATH = '../schelling'
        #self.reset()

    # take in previous state
    def step(self, prevState, mode=0):
        def get_average_income(node):
            node_income = self.graph.nodes[node]["income"]
            neighbor_income = []
            for neighbor in self.graph.neighbors(node):
                neighbor_income.append(self.graph.nodes[neighbor]["income"])
            income = (
                (sum(neighbor_income) / len(neighbor_income))
                if len(neighbor_income) != 0
                else node_income
            )
            self.graph.nodes[node]["average_income"] = income
            return income

        def get_race_ratio(node, race):
            neighbor_race = []
            neighbor_race.append(self.graph.nodes[node]["race"])
            for neighbor in self.graph.neighbors(node):
                neighbor_race.append(self.graph.nodes[neighbor]["race"])
            return (
                (neighbor_race.count(race) / len(neighbor_race))
                if len(neighbor_race) != 0
                else 1
            )

        self.i += 1
        node_attr = prevState.to_dict(orient="index")

        nx.set_node_attributes(self.graph, node_attr)

        if mode == 0:
            print("Determining Satisfaction")
            for node in self.graph.nodes():
                # node_income = g.nodes[node]["income"]
                node_race = self.graph.nodes[node]["race"]
                average_income = get_average_income(node)
                ratio = get_race_ratio(node, node_race)
                if ratio >= 0.3:
                    self.graph.nodes[node]["happy"] = True
                else:
                    self.graph.nodes[node]["happy"] = False

            self.df = pd.DataFrame.from_dict(
                dict(self.graph.nodes(data=True)), orient="index"
            )

            #self.df = self.df["happy"] == True
            self.df['lid'] = self.df.index
            self.df = self.df[['hid','lid', 'happy']]

        elif mode == 1:
            print("Moving")
            temp_graph = self.graph.copy()
            movers = [n for n, h in temp_graph.nodes(data=True) if h["happy"] == False]
            vacant_nodes = copy.deepcopy(movers)

            for mover in movers:
                random.shuffle(vacant_nodes)
                mover_hid = self.graph.nodes[mover]["hid"]
                mover_race = self.graph.nodes[mover]["race"]
                mover_income = self.graph.nodes[mover]["income"]
                mover_geo = self.graph.nodes[mover]["geometry"]

                race_pref = [
                    n for n in vacant_nodes if get_race_ratio(n, mover_race) >= 0.3
                ]
                income_pref = [
                    n
                    for n in race_pref
                    if (
                        self.graph.nodes[n]["average_income"] - 5000
                        < mover_income
                        < self.graph.nodes[n]["average_income"] + 10000
                    )
                ]

                if len(income_pref) != 0:
                    valid_node = income_pref[0]
                elif len(race_pref) != 0:
                    valid_node = race_pref[0]
                else:
                    if temp_graph.nodes[mover]["happy"] == True:
                        valid_node = vacant_nodes[0]
                    else:
                        valid_node = mover

                temp_graph.nodes[valid_node]["hid"] = mover_hid
                temp_graph.nodes[valid_node]["race"] = mover_race
                temp_graph.nodes[valid_node]["income"] = mover_income
                temp_graph.nodes[valid_node]["geometry"] = mover_geo
                temp_graph.nodes[valid_node]["happy"] = True

                vacant_nodes.remove(valid_node)
                # print("Remaining:", len(vacant_nodes))

                self.graph = temp_graph
                self.df = pd.DataFrame.from_dict(
                    dict(self.graph.nodes(data=True)), orient="index"
                )
                
                self.df['lid'] = self.df.index
                self.df = self.df[['hid','lid', 'happy']]

        self.i += 1
        return self.df

    def reset(self, shuffle=False):
        self.graph = nx.Graph()
        self.i = 0

        def label_race(row):
            racelist = row["race"]
            if len(set(racelist)) == 1:
                return racelist[0]
            else:
                return 9

        print("Reading Map Geometry")
        geofr = gpd.read_file("{}/tl_2017_51_tabblock10.zip".format(self.PATH))
        geofr[["COUNTYFP10", "TRACTCE10", "BLOCKCE10", "GEOID10"]] = geofr[
            ["COUNTYFP10", "TRACTCE10", "BLOCKCE10", "GEOID10"]
        ].apply(pd.to_numeric)
        geofr = geofr[geofr["COUNTYFP10"] == 760]
        #geofr = geofr[geofr["TRACTCE10"].between(10000, 10500)]
        geofr = geofr.drop(
            [
                "STATEFP10",
                "COUNTYFP10",
                "TRACTCE10",
                "NAME10",
                "BLOCKCE10",
                "MTFCC10",
                "UR10",
                "UACE10",
                "UATYPE",
                "FUNCSTAT10",
                "ALAND10",
                "AWATER10",
                "INTPTLAT10",
                "INTPTLON10",
            ],
            axis=1,
        )
        geofr = geofr.reset_index(drop=True)
        geofr["GEOID10"] = geofr["GEOID10"].astype(np.int64)
        geofr = geofr.to_crs(epsg=2925)
        geofr.to_pickle("geofr.pkl")
        print(geofr.info())

        print("Reading Household Data")
        housefr = pd.read_csv(
            "{}/household.csv".format(self.PATH),
            usecols=[
                "admin2",
                "admin3",
                "hid",
                "hh_income",
                "residence_longitude",
                "residence_latitude",
            ],
        )
        housefr = housefr[housefr["admin2"] == 760]
        housefr = housefr[housefr["admin3"].between(10000, 10500)]
        housefr = housefr.drop(["admin2", "admin3"], axis=1)
        print(housefr.info())

        print("Reading Person Data")
        personfr = pd.read_csv("{}/person.csv".format(self.PATH), usecols=["hid", "race"])
        print(personfr.info())

        print("Merging Tables")
        print("Merging Race")

        raceser = personfr.groupby("hid")["race"].apply(list)
        synthfr = pd.merge(housefr, raceser, how="left", left_on="hid", right_on="hid")
        synthfr["hh_race"] = synthfr.apply(lambda row: label_race(row), axis=1)
        print("Converting Geometry")
        synthfr = gpd.GeoDataFrame(synthfr, geometry = gpd.points_from_xy(synthfr["residence_longitude"], synthfr["residence_latitude"]))

        synthfr = synthfr.set_crs(epsg=4269)
        synthfr = synthfr.to_crs(epsg=2925)
        synthfr["lid"] = range(0, len(synthfr))
        if shuffle:
            synthfr[["lid", "geometry"]] = (
                synthfr[["lid", "geometry"]].sample(frac=1).values
            )

        print("Finding Neighbors")
        tree = KDTree(list(zip(synthfr.geometry.x, synthfr.geometry.y)))

        pairs = tree.query_pairs(500)
        synthfr["neighbors"] = np.empty((len(synthfr), 0)).tolist()
    
        for index, row in synthfr.iterrows():
            self.graph.add_node(
                row["lid"],
                hid=row["hid"],
                race=row["hh_race"],
                income=row["hh_income"],
                #geometry=row["geometry"],
            )

        lid = synthfr.columns.get_loc("lid")
        nb = synthfr.columns.get_loc("neighbors")
        for (i, j) in pairs:
            self.graph.add_edge(synthfr.iloc[i, lid], synthfr.iloc[j, lid])
            synthfr.iloc[i, nb].append(synthfr.iloc[j, lid])
            synthfr.iloc[j, nb].append(synthfr.iloc[i, lid])
        synthfr = synthfr.drop(
            ["residence_longitude", "residence_latitude", "race"], axis=1
        )

        print(synthfr.info())
    
        self.df = pd.DataFrame.from_dict(
            dict(self.graph.nodes(data=True)), orient="index"
        )
        return self.df

if __name__ == '__main__':
    env = environment()
    last = env.reset()
    print(out)
    for i in range(2):
        print(last)
        last = env.step(last)


    
