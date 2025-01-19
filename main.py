import axelrod as axl
import networkx as nx
import matplotlib.pyplot as plt
from scipy.io import mmread
import numpy as np
import pandas as pd

mtx_file = "fb_graph/matname.mtx"
sparse_matrix = mmread(mtx_file)
graph = nx.Graph(sparse_matrix)

strategies = [
    axl.Cooperator(),
    axl.Defector(),
    axl.TitForTat(),
    axl.Grudger(),
    axl.Random(),
    axl.ZDExtortion(),
    axl.Capri(),
    axl.Appeaser()
]

players = []
for node in graph.nodes:
    players.append(np.random.choice(strategies))

# turns is ther number of iterations between each pair
spatial_tournament = axl.Tournament(
    players, edges=graph.edges, turns=1, repetitions=1)
results = spatial_tournament.play(filename="test.csv")

df = pd.read_csv("test.csv")
