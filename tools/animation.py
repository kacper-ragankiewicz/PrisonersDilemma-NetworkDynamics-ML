from tqdm import tqdm  # For progress tracking
import axelrod as axl
import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

STRATEGY_COLORS = {
    "Cooperator": "blue",
    "Defector": "red",
    "TitForTat": "green",
    "Random": "purple"
}


def load_graph_with_names(file_path, max_edges=None):
    """
    Load a graph from a MatrixMarket coordinate pattern file and assign player names.

    Args:
        file_path (str): Path to the .mtx file.
        max_edges (int, optional): Maximum number of edges to load. If None, load all edges.
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

    # If max_edges is specified, limit the number of edges
    if max_edges is not None:
        edges = edges[:max_edges]

    # Create a graph and label nodes with "Player X"
    G = nx.Graph()
    G.add_edges_from(edges)
    for node in G.nodes():
        G.nodes[node]['name'] = f"Player {node}"
        G.nodes[node]['score'] = 0  # Initialize scores
    return G


def assign_strategies(graph, strategies):
    """
    Assign a random strategy to each node in the graph.
    """
    for node in graph.nodes():
        graph.nodes[node]['strategy'] = random.choice(strategies)


def play_game_round(graph, round_num):
    """
    Play a single round of the Iterated Prisoner's Dilemma on each edge of the graph.
    """
    game = axl.Game()  # Define the game scoring

    for u, v in graph.edges():
        strategy_u = graph.nodes[u]['strategy']
        strategy_v = graph.nodes[v]['strategy']

        # Play one match with only one round
        match = axl.Match([strategy_u(), strategy_v()], turns=round_num + 1)
        actions = match.play()

        # Extract scores for the current round
        score_u, score_v = game.score(actions[round_num])

        # Update scores incrementally
        graph.nodes[u]['score'] += score_u
        graph.nodes[v]['score'] += score_v


def update(frame, graph, pos, ax):
    """
    Update function for animation frames.
    """
    ax.clear()
    ax.axis("off")

    # Play one round of the game
    play_game_round(graph, frame)

    # Get node attributes
    scores = nx.get_node_attributes(graph, 'score')
    strategies = nx.get_node_attributes(graph, 'strategy')

    # Draw edges
    nx.draw_networkx_edges(graph, pos, ax=ax)

    # Draw nodes with colors based on strategies
    node_colors = [STRATEGY_COLORS[strategies[node].__name__]
                   for node in graph.nodes()]
    nx.draw_networkx_nodes(
        graph, pos, ax=ax, node_color=node_colors, node_size=500)

    # Add labels for scores
    labels = {node: f"{graph.nodes[node]['name']}\n{scores[node]}" for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8, ax=ax)

    # Title for the frame
    ax.set_title(f"Round {frame + 1}")


def animate_graph(graph, total_rounds=10, interval=1000, output_file="graph_animation.gif"):
    """
    Animate the graph, showing nodes' strategies and scores over rounds.
    """
    pos = nx.spring_layout(graph)  # Position nodes using a spring layout
    fig, ax = plt.subplots(figsize=(10, 8))
    ani = animation.FuncAnimation(
        fig, update, frames=total_rounds, fargs=(graph, pos, ax), interval=interval)

    # Save the animation as a GIF
    ani.save(output_file, writer="pillow", fps=1)
    plt.close(fig)
    print(f"Animation saved to {output_file}")


def main():
    # Load the graph
    file_path = "fb_graph/matname.mtx"  # Replace with your file's path
    max_edges = 100  # Specify the number of edges to process
    graph = load_graph_with_names(file_path, max_edges=max_edges)

    # Define strategies
    strategies = [axl.Cooperator, axl.Defector, axl.TitForTat, axl.Random]

    # Assign strategies to nodes
    assign_strategies(graph, strategies)

    # Animate the graph over 10 rounds
    animate_graph(graph, total_rounds=10, interval=1000,
                  output_file="graph_animation.gif")


if __name__ == "__main__":
    main()
