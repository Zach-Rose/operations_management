import os
import time
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-interactive plotting
import networkx as nx
import matplotlib.pyplot as plt

def analyze_process(steps):
    B = nx.Graph()
    for step, resources in steps.items():
        for resource in resources:
            B.add_edge(step, resource)

    G = nx.bipartite.weighted_projected_graph(B, steps.keys())
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
    bottlenecks = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)

    output_dir = 'intake_form/static/intake_form'
    os.makedirs(output_dir, exist_ok=True)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='skyblue', edgecolors='black')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_color='red')

    timestamp = int(time.time())
    image_path = os.path.join(output_dir, f'process_diagram_{timestamp}.png')
    plt.savefig(image_path, format='PNG')
    plt.close()

    nodes = [{'id': node, 'label': node} for node in G.nodes()]
    edges = [{'source': u, 'target': v, 'weight': d['weight']} for u, v, d in G.edges(data=True)]

    return bottlenecks, image_path, nodes, edges