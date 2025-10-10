# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.graphClass import Graph
from data.mazeData import maze_data, maze_action_costs, treasure_states, node_coords
from src.agents import ProblemSolvingMazeAgentBFS
from src.task2.MazeEnvironment import MazeEnvironment
import random


def drawBtn(e,a,c,s):
    option= [e,a,c,s]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    st.header("Solving Maze ...")
    e,a,c,s= opt[0],opt[1],opt[2],opt[3]
    if not st.session_state["clicked"]:
        st.session_state["env"]=e
        st.session_state["agent"]=a
        st.session_state["nodeColors"]=c    
        st.session_state["nodeShapes"]=s
    
    if e.is_agent_alive(a):
        e.step()
        st.success(" Agent now at : {}.".format(a.state))
        st.info("Current Agent performance {}:".format(a.performance))
        c[a.state]="orange"
        st.info("State of the Environment:")
        buildGraph(e.status, c, s) 
    else:
        if a.state==a.goal:
            st.success(" Agent now at the goal state: {}.".format(a.state))
        else:
            st.error("Agent in location {} and it is dead.".format(a.state))
        
    st.session_state["clicked"] = True
        
    
        
def buildGraph(graphData, nodeColorsDict, nodeShapesDict):
    net = Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%") 
    nodes=graphData.nodes()
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    for node in nodes:
        x, y = node_coords[node]
        g.add_node(node, color=nodeColorsDict[node], shape=nodeShapesDict[node], x=x, y=y, fixed=True)

    # add the edges
    edges=[]
    for node_source in graphData.nodes():
        for node_target, dist in graphData.get(node_source).items():
            if set((node_source,node_target)) not in edges:
                edges.append(set((node_source,node_target)))                
    g.add_edges_from(edges)
    
    # generate the graph
    net.from_nx(g)
    
    net.save_graph('L3_mazeGraph.html')
    HtmlFile = open(f'L3_mazeGraph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 800,width=1000)
    
    
def makeDefaultColors(dictData):
    nodeColors=dict.fromkeys(dictData.keys(), "gray")
    return nodeColors


def makeDefaultShapes(dictData):
    nodeShapes=dict.fromkeys(dictData.keys(), "circle")
    return nodeShapes


def main():
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
        
    if "env" not in st.session_state:
        st.session_state["env"]=None
        
    if "agent" not in st.session_state:
        st.session_state["agent"]=None
        
    if "nodeColors" not in st.session_state:
        st.session_state["nodeColors"]=None

    if "nodeShapes" not in st.session_state:
        st.session_state["nodeShapes"]=None
        
    if not st.session_state["clicked"]:
        # Set header title
        st.header("The wolf, goat, and the cabbage problem")
        st.header("_Initial Env._", divider=True)
        
        maze_graph = Graph(maze_data, maze_action_costs)
        nodeColors=makeDefaultColors(maze_graph.graph_dict)
        nodeShapes=makeDefaultShapes(maze_graph.graph_dict)
        
        init_state="N1"
        # Choose 4 random treasure states as possible goals
        goals = random.choices(treasure_states, k=4)
        end_state="N26"
        
        env=MazeEnvironment(maze_graph)
        bfsMazeAgent=ProblemSolvingMazeAgentBFS(init_state, maze_graph, goals, end_state)        
                      
        env.add_thing(bfsMazeAgent)

        st.header("State of the Environment", divider="red")
        nodeColors[init_state]="red"
        nodeColors[end_state]="green"
        
        # Set up custom colors and shapes for treasures
        # Pile of gold
        nodeColors[goals[0]] = "gold"
        nodeShapes[goals[0]] = "triangle"
        # Diamond
        nodeColors[goals[1]] = "teal"
        nodeShapes[goals[1]] = "diamond"
        # Flyer for 100 free pizzas
        nodeColors[goals[2]] = "beige"
        nodeShapes[goals[2]] = "box"
        # 20 Extra points on exam
        nodeColors[goals[3]] = "LimeGreen"
        nodeShapes[goals[3]] = "star"
            
        buildGraph(maze_graph, nodeColors, nodeShapes) 
        st.info(f"The Agent in: {bfsMazeAgent.state} with performance {bfsMazeAgent.performance}.")
        st.info(f"The Agent goal is: {bfsMazeAgent.goal} .")
                
        drawBtn(env, bfsMazeAgent, nodeColors, nodeShapes)
    
            
        
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"],st.session_state["agent"], st.session_state["nodeColors"], st.session_state["nodeShapes"])


if __name__ == '__main__':
    main()