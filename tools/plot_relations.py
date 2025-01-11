import os
from matplotlib import pyplot as plt
from scipy.io import mmread
import networkx as nx

# Set the file path (ensure the path is correct)
file_path = '../fb_graph/matname.mtx'

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist!")

# Read the Matrix Market file and convert it into a sparse matrix
sparse_matrix = mmread(file_path)

# Convert the sparse matrix into a NetworkX graph
graph = nx.from_scipy_sparse_matrix(sparse_matrix)

# Print basic graph information
print(f"Number of nodes: {graph.number_of_nodes()}")
print(f"Number of edges: {graph.number_of_edges()}")

# Plotting the graph
plt.figure(figsize=(8, 6))

# Generate layout for nodes
pos = nx.spring_layout(graph, iterations=50)

# Draw the graph
nx.draw(graph, pos,
        node_size=10,
        node_color="lightblue",
        with_labels=False,
        edge_color="gray")

# Show the plot
plt.show()
