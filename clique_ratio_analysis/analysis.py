import networkx as nx
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')

def perform_clique_ratio_analysis(contributors_list):
    # Create a graph
    G = nx.Graph()

    # Flatten the list of contributors and remove duplicates
    all_contributors = set([contributor for sublist in contributors_list for contributor in sublist])

    # Add nodes for each contributor
    G.add_nodes_from(all_contributors)

    # Add edges between contributors who are associated with each other
    for contributors in contributors_list:
        for i in range(len(contributors)):
            for j in range(i + 1, len(contributors)):
                G.add_edge(contributors[i], contributors[j])

    # Find all cliques in the graph
    cliques = list(nx.find_cliques(G))

    # Calculate the number of cliques
    num_cliques = len(cliques)

    # Calculate the total number of possible connections
    total_possible_connections = len(all_contributors) * (len(all_contributors) - 1) / 2

    # Calculate the clique ratio
    clique_ratio = num_cliques / total_possible_connections if total_possible_connections > 0 else 0

    # Generate and save the graph visualization
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    image_path = os.path.join(static_dir, 'clique_ratio_analysis.png')
    plt.savefig(image_path)
    plt.close()

    return clique_ratio, '/static/clique_ratio_analysis.png'