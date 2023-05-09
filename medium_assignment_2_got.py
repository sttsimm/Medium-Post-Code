# -*- coding: utf-8 -*-
"""Medium Assignment 2 GOT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-pcOiL8vUB-3f_nhf2PEBgcgwcJ4Zt1M
"""

import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

url = "https://www.anapioficeandfire.com/api"

#This function retrieves character data such as culture, # of seasons, and name.
def get_character_data(character_url):
    response = requests.get(character_url)
    data = response.json()
    return {"Character": data["name"], "Seasons": len(data["tvSeries"]), "Culture": data["culture"]}

# Retrieve data for limited number of characters with names and culture only
#This will give me a nice sized array of charactars and ensure data is not missing
characters = []
for i in range(1, 214):
    response = requests.get(f"{url}/characters?page={i}&pageSize=50")
    response_json = response.json()
    if not response_json:
       break
    for character in response_json:
        if character.get("name") and character.get("culture"):
            characters.append(character)

#printing characters array
characters

# Filtering out characters who were in less than three seasons 
# adding them to a new array
character_data = []
for char in characters:
    if len(char["tvSeries"]) >= 3:
        character_data.append(get_character_data(char["url"]))

#create df
df = pd.DataFrame(character_data)

#printing df to make sure it looks right
df

# Create a new graph
G = nx.Graph()

# Preparing nodes for each character, size of node is based on number of seasons character was in
node_sizes = df["Seasons"] * 100
for i, row in df.iterrows():
    G.add_node(row["Character"], size=node_sizes[i])

# Define colors for each culture to differentiate nodes
colors = {
    "Westeros": "navy",
    "Valyrian": "red",
    "Northmen": "brown",
    "Ironborn": "gray",
    "Rivermen": "blue",  
    "Westerman": "orange",
    "Valemen": "gold",
    "Westerlands": "yellow",
    "Reach": "green",
    "Crannogmen": "olive",
    "Asshai": "indigo",
    "Andal": "khaki",
    "Tyroshi": "coral",
    "Free Folk": "tan",
    "Free folk": "tan",  #had to add freefolk twice, i think there is a slight error in the API
    "Naathi": "lavender",
    "Lysene": "magenta"
}

# Add edges between characters from the same culture using nested for loop
for culture, group in df.groupby("Culture"):
    for x, row1 in group.iterrows():
        for y, row2 in group.iterrows():
          #comparing indices of each row
            if x < y:  # only adding edges once per pair of nodes
                G.add_edge(row1["Character"], row2["Character"], color=colors[culture])

# set k equal to 2 
p = nx.spring_layout(G, k=2, iterations=20)

# Draw nodes and edges
edge_colors = []
for u, v in G.edges():
    edge_colors.append(G[u][v]["color"])
    
node_colors = []
for n in G.nodes():
    culture = df.loc[df["Character"]==n, "Culture"].iloc[0]
    node_colors.append(colors[culture])

nx.draw_networkx_edges(G, p, edge_color=edge_colors, alpha=0.5)
nx.draw_networkx_nodes(G, p, node_size=node_sizes, node_color=node_colors, alpha=0.8)
nx.draw_networkx_labels(G, p, font_size=6.5, font_family="sans-serif")

# Display the graph
plt.axis("off")
plt.show()