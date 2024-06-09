import matplotlib.pyplot as plt
import networkx as nx
import json
from io import BytesIO
import base64
import matplotlib.cm as cm
import colorsys

def get_text_color(node_color):
    r, g, b, _ = node_color  # Convert RGBA to RGB
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # Convert RGB to HLS (Hue, Lightness, Saturation)
    return 'white' if l < 0.5 else 'black'  # If lightness is below 0.5, use white text, otherwise use black text

def draw_graph(state, genes_in):
    G = nx.DiGraph()  # This creates a directed graph object using NetworkX
    
    # Handle if state is a single value
    G.add_node(0, label=f'{0}: {state:.2f}', value=state)
    
    # Add edges
    for gene in genes_in:
        a, b, transfer_mode, magnitude = gene  # Unpack the individual values from gene
        G.add_edge(a, b, weight=magnitude, transfer_mode=transfer_mode, value=magnitude)
    
    # Get node and edge values for color mapping
    node_values = [data.get('value', 0) for _, data in G.nodes(data=True)]
    edge_values = [data.get('value', 0) for _, _, data in G.edges(data=True)]
    
    # Debugging: print node and edge values
    print("Node values:", node_values)
    print("Edge values:", edge_values)
    
    # Normalize the values
    norm = plt.Normalize(min(node_values + edge_values), max(node_values + edge_values))
    
    # Create color maps
    node_cmap = cm.ScalarMappable(norm=norm, cmap=cm.plasma)
    edge_cmap = cm.ScalarMappable(norm=norm, cmap=cm.plasma)
    
    # Draw the graph
    pos = nx.spring_layout(G)  # You can use other layouts as well
    plt.figure(figsize=(12, 8))
    
    # Draw nodes with heat map colors
    node_colors = [node_cmap.to_rgba(data.get('value', 0)) for _, data in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=node_colors)
    
    # Draw edges with heat map colors
    edge_colors = [edge_cmap.to_rgba(data.get('value', 0)) for _, _, data in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='->', arrowsize=40)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Draw node labels with dynamic text color
    labels = nx.get_node_attributes(G, 'label')
    for node, label in labels.items():
        x, y = pos[node]
        node_color = node_colors[node]
        font_color = get_text_color(node_color)
        plt.text(x, y, label, fontsize=8, ha='center', va='center', color=font_color)
    
    # Save the image to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def load_state_and_genes(filename='state_genes.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
    print(data)  # Add this line to inspect the loaded data
    return data['states_in'], data['genes_in']

if __name__ == "__main__":
    states_in, genes_in = load_state_and_genes()
    image_base64 = draw_graph(states_in, genes_in)
    print(image_base64)
