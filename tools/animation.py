import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Define strategies and colors for visualization
STRATEGY_COLORS = {
    "Cooperator": "blue",
    "Defector": "red",
    "TitForTat": "green",
    "Random": "purple"
}


def create_network_with_scores(file_path):
    """
    Create a graph with players, strategies, and scores.
    """
    # Load the graph
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            if not line.startswith('%'):
                node1, node2 = map(int, line.split()[:2])
                G.add_edge(node1, node2)

    # Assign strategies and scores randomly for demonstration purposes
    for node in G.nodes():
        G.nodes[node]['strategy'] = random.choice(list(STRATEGY_COLORS.keys()))
        G.nodes[node]['score'] = random.randint(
            0, 300)  # Replace with actual scores

    return G


def update(frame, G, pos, ax, nodes):
    """
    Update function for animation frames.
    """
    ax.clear()
    ax.axis("off")
    scores = nx.get_node_attributes(G, 'score')
    strategies = nx.get_node_attributes(G, 'strategy')

    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax)

    # Draw nodes with colors based on strategies
    node_colors = [STRATEGY_COLORS[strategies[node]] for node in G.nodes()]
    nodes = nx.draw_networkx_nodes(
        G, pos, ax=ax, node_color=node_colors, node_size=500)

    # Add labels for scores
    labels = {node: f"{node}\n{scores[node]}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    # Title for the frame
    ax.set_title(f"Frame {frame}")


def animate_graph(G, frames=30, interval=500, output_file="graph_animation.mp4"):
    """
    Create an animation showing node colors by strategy and scores on a graph.
    """
    pos = nx.spring_layout(G)  # Position nodes using a spring layout
    fig, ax = plt.subplots(figsize=(10, 8))
    ani = animation.FuncAnimation(fig, update, frames=frames, fargs=(
        G, pos, ax, None), interval=interval)

    # Save the animation
    ani.save(output_file, writer="ffmpeg", fps=2)
    plt.close(fig)
    print(f"Animation saved to {output_file}")


if __name__ == "__main__":
    # Replace with your actual graph file
    graph_file = "fb_graph/matname_10.mtx"
    G = create_network_with_scores(graph_file)

    # Create the animation
    animate_graph(G, frames=30, interval=500,
                  output_file="graph_animation.mp4")
