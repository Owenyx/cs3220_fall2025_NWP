import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components #to display the HTML code


def data_load():
    return pd.read_csv("data/game-of-thrones-battles.csv")


def data_proc(df):
    # Select relavent columns
    battles_df = df.loc[:,['name','attacker_king','defender_king','attacker_size','defender_size']]

    # Remove rows with missing values (NaN)
    battles_df_cleaned=battles_df.dropna()

    return battles_df_cleaned


def build_nodes(df):
    # Create lists of all attacking and defending kings
    attackers = df.attacker_king.unique()
    defenders = df.defender_king.unique()

    # Define nodes - list of unique king names
    kings = set(list(attackers) + list(defenders))
    return kings


def build_edges(df):
    # Define potential edges
    potential_edges = df.loc[:, ['attacker_king', 'defender_king']].to_numpy().tolist()

    # Define real edges (no repetitions)
    edges = []
    for edge in potential_edges:
        if edge not in edges:
            edges.append(edge)

    # Calculate edge weights
    battle_counts = df.groupby(['attacker_king', 'defender_king']).count()['name']

    # Define edge titles
    battle_names = df.groupby(['attacker_king', 'defender_king'])['name'].aggregate(', '.join)

    # Add weights and titles to each edge
    full_edges = [] # Will contain dicts that have a src, dst, weight, and title

    for edge in edges:
        attacker, defender = edge
        weight = battle_counts.get((attacker, defender))
        title = battle_names.get((attacker, defender))

        full_edges.append({
            'src': attacker,
            'dst': defender,
            'weight': weight,
            'title': title
        })

    # Add edges to network

    # To convert edges to format suitable for network
    def format_edge(full_edge): 
        return {
            "value": int(full_edge["weight"]),
            "title": full_edge["title"],
            "arrows": "to",
            "from": full_edge["src"],
            "to": full_edge["dst"],
        }

    formatted_edges = map(format_edge, full_edges)
    return formatted_edges


def build_graph(nodes, edges):
    # Instantiate Pyvis network
    net5kings = Network(heading="Task1. Building Interactive Network of battles of the War of 5 Kings",
        bgcolor ="#242020",
        font_color = "white",
        height = "1000px",
        width = "100%",
        directed = True, # Since attacks are directed
        cdn_resources = "remote"
    )

    # Add nodes to graph
    net5kings.add_nodes(nodes)

    # Add edges to graph
    for edge in edges:
        net5kings.add_edge(
            edge["from"],
            edge["to"],
            value = edge['value'],
            title = edge['title'],
            arrows = edge['arrows']
        )


def add_node_values(network):
    enemies_map = network.get_adj_list()

    value_map = {} # Maps king name to value

    for king in enemies_map:
        enemies = enemies_map[king]
        value_map[king] = len(enemies) + 1

    for node in network.nodes:
        node['value'] = value_map[node['id']]


def add_node_colors(network):
    color_map={
        0: "blue",
        1: "green",
        2: "orange",
        3: "purple",
        4: "gold",
        5: "red"
    }

    for node in network.nodes:
        node['color'] = color_map[node['value']]


def main():
    # Load data
    raw_df = data_load()

    # Process data
    battles_df_cleaned = data_proc(raw_df)

    nodes = build_nodes(battles_df_cleaned)
    edges = build_edges(battles_df_cleaned)

    net5kings = build_graph(nodes, edges)

    add_node_values(net5kings)
    add_node_colors(net5kings)

    # Display graph
    net5kings.save_graph("Lab1-task1-net5kings.html")
    HtmlFile = open(f'Lab1-task1-net5kings.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)