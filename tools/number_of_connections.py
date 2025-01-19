import networkx as nx


def load_graph_with_names(file_path):
    """
    Load a graph from a MatrixMarket coordinate pattern file and assign player names.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    edges = []
    for line in lines:
        if line.startswith('%'):  # Skip comment lines
            continue
        parts = line.split()
        if len(parts) == 2:  # Ensure it's a valid edge
            node1, node2 = map(int, parts)
            edges.append((node1, node2))

    # Create a graph and label nodes with "Player X"
    G = nx.Graph()
    G.add_edges_from(edges)
    for node in G.nodes():
        G.nodes[node]['name'] = f"Player {node}"
    return G


def count_node_connections(graph, node_id):
    """
    Print the number of connections to a specific node in the graph.
    
    Args:
        graph (networkx.Graph): The graph representing the network.
        node_id (int): The ID of the node to analyze.
    """
    if node_id not in graph:
        print(f"Node {node_id} not found in the graph.")
        return

    # Get the degree (number of connections) of the node
    connections = graph.degree[node_id]
    print(f"Node {node_id} has {connections} connections.")


def main():
    # Load the graph
    file_path = "fb_graph/matname.mtx"  # Replace with your file's path
    graph = load_graph_with_names(file_path)

    # Specify the node ID to analyze
    node_id = 1
    count_node_connections(graph, node_id)


if __name__ == "__main__":
    main()
