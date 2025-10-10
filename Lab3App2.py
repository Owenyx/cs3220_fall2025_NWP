# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.graphClass import Graph
from data.mazeData import maze_data, maze_action_costs
from src.agents import ProblemSolvingMazeAgentBFS
from src.task2.MazeEnvironment import MazeEnvironment


def drawBtn(e,a,c):
    option= [e,a,c]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    st.header("Solving Maze ...")
    e,a,c= opt[0],opt[1],opt[2]
    if not st.session_state["clicked"]:
        st.session_state["env"]=e
        st.session_state["agent"]=a
        st.session_state["nodeColors"]=c    
    
    if e.is_agent_alive(a):
        e.step()
        st.success(" Agent now at : {}.".format(a.state))
        st.info("Current Agent performance {}:".format(a.performance))
        c[a.state]="orange"
        st.info("State of the Environment:")
        buildGraph(e.status, c) 
    else:
        if a.state==a.goal:
            st.success(" Agent now at the goal state: {}.".format(a.state))
        else:
            st.error("Agent in location {} and it is dead.".format(a.state))
        
    st.session_state["clicked"] = True
        
    
        
def buildGraph(graphData, nodeColorsDict):
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
        g.add_node(node, color=nodeColorsDict[node])

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
    components.html(HtmlFile.read(), height = 1000,width=1000)
    
    
def makeDefaultColors(dictData):
    nodeColors=dict.fromkeys(dictData.keys(), "white")
    return nodeColors


def main():
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
        
    if "env" not in st.session_state:
        st.session_state["env"]=None
        
    if "agent" not in st.session_state:
        st.session_state["agent"]=None
        
    if "nodeColors" not in st.session_state:
        st.session_state["nodeColors"]=None
        
    if not st.session_state["clicked"]:
        # Set header title
        st.header("The wolf, goat, and the cabbage problem")
        st.header("_Initial Env._", divider=True)
        
        maze_graph = Graph(maze_data, maze_action_costs)
        nodeColors=makeDefaultColors(maze_graph.graph_dict)
        
        initState="LLLL"
        goalState="RRRR"
        
        env=MazeEnvironment(maze_graph)
        bfsMazeAgent=ProblemSolvingMazeAgentBFS(initState, maze_graph, goalState)        
                      
        env.add_thing(bfsMazeAgent)

        st.header("State of the Environment", divider="red")
        nodeColors[bfsMazeAgent.state]="red"
        nodeColors[bfsMazeAgent.goal]="green"
        buildGraph(maze_graph, nodeColors) 
        st.info(f"The Agent in: {bfsMazeAgent.state} with performance {bfsMazeAgent.performance}.")
        st.info(f"The Agent goal is: {bfsMazeAgent.goal} .")
                
        drawBtn(env, bfsMazeAgent, nodeColors)
    
            
        
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"],st.session_state["agent"], st.session_state["nodeColors"])


if __name__ == '__main__':
    main()