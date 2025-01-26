from tqdm import tqdm  # For progress tracking
import axelrod as axl
import networkx as nx
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

STRATEGY_COLORS = {
    "Cooperator": "blue",
    "Defector": "red",
    "TitForTat": "green",
    "Random": "purple"
}


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


def get_connected_component(graph, player_id):
    """
    Find the connected component for the specified player in the graph.
    
    Args:
        graph (networkx.Graph): The full graph.
        player_id (int): The ID of the player.

    Returns:
        networkx.Graph: Subgraph containing all nodes connected to the specified player.
    """
    if player_id not in graph:
        raise ValueError(f"Player {player_id} is not in the graph.")

    # Get all nodes in the connected component
    connected_nodes = nx.node_connected_component(graph, player_id)

    # Create and return the subgraph
    return graph.subgraph(connected_nodes)


def update(frame, graph, pos, ax, subgraph):
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

    # Draw edges in the subgraph
    nx.draw_networkx_edges(subgraph, pos, ax=ax)

    # Draw nodes in the subgraph with colors based on strategies
    node_colors = [STRATEGY_COLORS[strategies[node].__name__]
                   for node in subgraph.nodes()]
    nx.draw_networkx_nodes(
        subgraph, pos, ax=ax, node_color=node_colors, node_size=500)

    # Add labels for scores in the subgraph
    labels = {node: f"{graph.nodes[node]['name']}\n{scores[node]}" for node in subgraph.nodes()}
    nx.draw_networkx_labels(subgraph, pos, labels=labels, font_size=8, ax=ax)

    # Title for the frame
    ax.set_title(f"Round {frame + 1}")


def animate_subgraph(graph, player_id, total_rounds=10, interval=1000, output_file="connected_component_animation.gif"):
    """
    Animate the connected component for a specific player.
    """
    # Get the connected component for the specified player
    subgraph = get_connected_component(graph, player_id)

    # Use a spring layout for consistent visualization
    pos = nx.spring_layout(subgraph)

    # Create the animation
    fig, ax = plt.subplots(figsize=(10, 8))
    ani = animation.FuncAnimation(
        fig, update, frames=total_rounds, fargs=(graph, pos, ax, subgraph), interval=interval)

    # Save the animation as a GIF
    ani.save(output_file, writer="pillow", fps=1)
    plt.close(fig)
    print(f"Animation for Player {player_id} saved to {output_file}")


def main():
    # Load the graph
    file_path = "fb_graph/matname.mtx"  # Replace with your file's path
    graph = load_graph_with_names(file_path)

    # Define strategies
    strategies = [axl.Cooperator, axl.Defector, axl.TitForTat, axl.Random]

    # Assign strategies to nodes
    assign_strategies(graph, strategies)

    # Animate the connected component for a specific player (e.g., Player 224)
    animate_subgraph(graph, player_id=2, total_rounds=10,
                     interval=10, output_file="connected_component_animation.gif")


if __name__ == "__main__":
    main()
