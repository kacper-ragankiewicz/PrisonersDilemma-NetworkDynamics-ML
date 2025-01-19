from tqdm import tqdm  # For progress tracking
import axelrod as axl
import networkx as nx
import random
import csv
import pandas as pd

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
        G.nodes[node]['name'] = f"{node}"
        G.nodes[node]['score'] = 0  # Initialize scores
    return G


def assign_strategies(graph, strategies):
    """
    Assign a random strategy to each node in the graph.
    """
    for node in graph.nodes():
        graph.nodes[node]['strategy'] = random.choice(strategies)


def play_games(graph, rounds=100):
    """
    Play the Iterated Prisoner's Dilemma on each edge of the graph.
    """
    game = axl.Game()  # Define the game scoring

    for u, v in tqdm(graph.edges(), desc="Processing edges"):
        strategy_u = graph.nodes[u]['strategy']
        strategy_v = graph.nodes[v]['strategy']

        # Play one match
        match = axl.Match([strategy_u(), strategy_v()], turns=rounds)
        actions = match.play()

        # Compute numerical scores for the match
        scores_u, scores_v = 0, 0
        for action_u, action_v in actions:
            score_u, score_v = game.score((action_u, action_v))
            scores_u += score_u
            scores_v += score_v

        # Update scores in the graph
        graph.nodes[u]['score'] += scores_u
        graph.nodes[v]['score'] += scores_v

        # Store the scores for the edge
        graph.edges[u, v]['scores'] = (scores_u, scores_v)


def find_best_player(graph):
    """
    Find the player with the highest score in the network.
    """
    best_player = max(graph.nodes(data=True), key=lambda x: x[1]['score'])
    return best_player[1]['name'], best_player[1]['score']


def save_results_to_csv(graph, file_name="network_results.csv"):
    """
    Save game results and node scores to a CSV file.
    """
    data = []
    for u, v in graph.edges():
        score1, score2 = graph.edges[u, v]['scores']
        data.append({
            "Player 1": graph.nodes[u]['name'],
            "Player 2": graph.nodes[v]['name'],
            "Score Player 1": score1,
            "Score Player 2": score2
        })

    # Convert to DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Edge results saved to {file_name}")

    # Save player scores
    node_data = [{"Player": graph.nodes[n]['name'],
                  "Total Score": graph.nodes[n]['score']} for n in graph.nodes()]
    df_nodes = pd.DataFrame(node_data)
    df_nodes.to_csv("player_scores.csv", index=False)
    print(f"Player scores saved to player_scores.csv")


def save_detailed_results_to_csv(graph, file_name="detailed_network_results.csv"):
    """
    Save detailed results to a CSV file including node name, score, strategy, and players interacted with.
    """
    data = []
    for node in graph.nodes():
        node_name = graph.nodes[node]['name']
        node_score = graph.nodes[node]['score']
        # Get the strategy name
        node_strategy = graph.nodes[node]['strategy'].__name__
        # Find all players this node interacted with
        connected_players = [graph.nodes[neighbor]['name']
                             for neighbor in graph.neighbors(node)]
        data.append({
            "Node Name": node_name,
            "Total Score": node_score,
            "Strategy": node_strategy,
            "Players Interacted With": ", ".join(connected_players)
        })

    # Convert to DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Detailed results with strategies saved to {file_name}")



def main():
    # Load the graph
    file_path = "fb_graph/matname.mtx"  # Replace with your file's path
    graph = load_graph_with_names(file_path)

    # Define strategies
    strategies = [axl.Cooperator, axl.Defector, axl.TitForTat, axl.Random]

    # Assign strategies to nodes
    assign_strategies(graph, strategies)

    # Play games
    play_games(graph)

    # Find the best player
    best_player, best_score = find_best_player(graph)
    print(f"The best player in the network is {best_player} with a total score of {best_score}.")

    # Save results to CSV
    save_results_to_csv(graph)

    #Save detailed results to CSV
    save_detailed_results_to_csv(graph)


if __name__ == "__main__":
    main()

