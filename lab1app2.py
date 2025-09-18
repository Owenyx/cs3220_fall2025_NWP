from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code
import json
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx


class Dynasty:
    def __init__(self,name):
        self._name=name # House name, for.ex."Martell"
        self.characters=[] # Family members ("Doran Martell","Ellaria Sand","Nymeria Sand",...)


    @property
    def name(self): # getter for the private instance attribute _name
        return self._name
       

    @name.setter
    def name(self, value):
        # Ensure value is a non-empty string
        if value == '' or not isinstance(value, str):
            raise ValueError('House name must be a non-empty string')
        
        self._name = value
      

    def append(self, ch): # To append character to the House (during reading data from JSON-file)
        # Ensure ch is string
        if not isinstance(ch, str):
            raise ValueError('Character name must be a string')
        
        self.characters.append(ch)


    def __iter__(self): # to loop throw the list of characters via IN operator (for ex. for person in house: ....)
        return iter(self.characters)


    def __contains__(self, ch): # to check if the character belongs to the house (for ex., if person in house ...)
        return ch in self.characters


    def __str__(self): # to print like print(house) - > display the house's name
        return f"This is a House of {self._name}!"

    
    def getStrength(self): # return N of family members in this house (int)
        return len(self.characters)
    

class GameOfThronesGraph:
    def __init__(self, corpus):
        # Corpus structure is:
        # {
        #     name: string
        #     characters: string[]
        # }[]

        # Initialization of dictionary that will store all houses. 
        # The keys are House (Dynasty) names, the values are Dynasty objects.
        self.houses = {}
        #Load the house corpus
        for data_item in corpus:
            house_name = data_item['name']

            # Create Dynasty with all corrosponding characters
            house = Dynasty(house_name)
            for ch in data_item['characters']:
                house.append(ch)

            self.houses[house_name] = house


    def __iter__(self): # for the case like the following: for house in GameOfThronesHouses:
        return iter(self.houses.values())
            
    def __contains__(self, h): #Check if h (house's name) is a key in dict houses - the house is in the graph
        return h in self.houses


def data_load():
    file_name = "data/game-of-thrones-characters-groups.json"

    with open(file_name) as f:
        json_data = json.load(f)

    return json_data


def build_houses(json_data):
    corpusData=json_data['groups']
    return GameOfThronesGraph(corpusData)


def build_chart(houses):
    # Create visualisation and legend data for chart
    visualisationData={}
    legendData=[]
    for house in houses:
        visualisationData[house.name]=house.getStrength()
        legendData.append(house.name)

    #Configure x and y values from the dictionary:
    x = list(visualisationData.keys())
    y = list(visualisationData.values())

    #Create the graph = create seaborn barplot
    ax=sns.barplot(x=x,y=y)

    #specify axis labels
    ax.legend(legendData)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1.05, 1))
    ax.set(xlabel='Houses',
        ylabel='Strength (N family members)',
        title='Strength of GameOfThronesHouses')

    # Rotate x axis titles
    plt.xticks(rotation=45)
    

def build_network(houses):
    GameOfThronesNet = Network(
        bgcolor ="#242020",
        font_color = "white",
        height = "1000px",
        width = "100%",
        cdn_resources = "remote")
    
    g = build_nx_graph(houses)
    
    # generate the network graph from the nx graph
    GameOfThronesNet.from_nx(g)

    add_network_node_colors(GameOfThronesNet, houses)

    return GameOfThronesNet


def build_nx_graph(houses):
    g = nx.Graph() # Initialize graph

    add_nodes(g, houses)
    add_edges(g, houses)

    return g
    

def add_nodes(g, houses):
    # Add house nodes
    for house in houses:
        # Skip include since not a family
        if house.name != "Include":
            # add the house's name as a node to the graph g (houses's strength values is used as a node's size)
            g.add_node(house.name, size=house.getStrength())

    # Add character nodes
    for house in houses:
        if house.name!="Include":
            # add each character as a node to the graph g 
            for ch in house:
                g.add_node(ch)


def add_edges(g, houses):
    myEdges=[]

    for house in houses:
        if house.name!="Include":
            for person in house:
                myEdges.append((person, house.name))

    g.add_edges_from(myEdges) # run this code to add edges to our graph g


def add_network_node_colors(network, houses):
    # Generate node colors
    N_houses=0
    colorKeys=[]
    for house in houses:
        if house.name!="Include":
            N_houses+=1
            colorKeys.append(house.name)
    colors = sns.color_palette("husl", N_houses) # N_houses colors

    nodeColors=dict(zip(colorKeys, [tuple(int(c*255) for c in cs) for cs in colors]))

    for node in network.nodes:
        if node["id"] in houses:
            # Convert RGB to hexadecimal string
            node["color"] = '#%02x%02x%02x' % nodeColors[node["id"]]
        else:
            for house in houses: 
                if house.name != "Include": # apply the color of the House to this family member
                    if node["id"] in house:
                        node["color"] = '#%02x%02x%02x' % nodeColors[house.name]


def render(houses, network):
    # Declare state so houses and network can be accessed by pages
    st.session_state["houses"] = houses
    st.session_state["network"] = network

    st.title('Task 2: Infographic of relationships between characters in Game of Thrones')

    tab1, tab2, tab3 = st.tabs([
        "Game of Thrones Houses", 
        "Members of Houses", 
        "Graph for Game of Thrones Houses"
    ])

    with tab1:
        tab_houses(houses)

    with tab2:
        tab_members(houses)

    with tab3:
        tab_graph(network)


def tab_houses(houses): # Page context is passed but not needed
    st.text('Game of Thrones Houses:')

    # House names and strengths
    for house in houses:
        st.markdown(f"- {house}: Strength: {house.getStrength()}")

    # House strength bar chart
    chart, ax = plt.subplots()
    st.pyplot(chart)


def tab_members(houses):
    for house in houses:
        st.text(house)
        st.text("Our members:")
        for person in house:
            st.text(person)
        st.text(f"We have {house.getStrength()} family members!!!")


def tab_graph(network):
    st.title("Lab1. Task2.")
    
    network.save_graph("GameOfThronesNet.html")
    HtmlFile = open(f'GameOfThronesNet.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200, width = 1000)


def main():
    json_data = data_load()

    # Create houses from data
    GameOfThronesHouses = build_houses(json_data)

    build_chart(GameOfThronesHouses)
    
    GameOfThronesNet = build_network(GameOfThronesHouses)

    render(GameOfThronesHouses, GameOfThronesNet)


if __name__ == '__main__':
    main()