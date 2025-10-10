# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.graphClass import Graph
from data.boatData import boat_data, boat_action_costs
from src.agents import ProblemSolvingBoatAgentBFS
from src.task1.RiverEnvironment import RiverEnvironment


def drawBtn(e,a,c):
    option= [e,a,c]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    st.header("Crossing River ...")
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
    
    net.save_graph('L3_boatGraph.html')
    HtmlFile = open(f'L3_boatGraph.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 800,width=1000)
    
    
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
        
        boat_graph = Graph(boat_data, boat_action_costs)
        nodeColors=makeDefaultColors(boat_graph.graph_dict)
        
        initState="LLLL"
        goalState="RRRR"
        
        env=RiverEnvironment(boat_graph)
        bfsBoatAgent=ProblemSolvingBoatAgentBFS(initState, boat_graph, goalState)        
                      
        env.add_thing(bfsBoatAgent)

        st.header("State of the Environment", divider="red")
        nodeColors[bfsBoatAgent.state]="red"
        nodeColors[bfsBoatAgent.goal]="green"
        buildGraph(boat_graph, nodeColors) 
        st.info(f"The Agent in: {bfsBoatAgent.state} with performance {bfsBoatAgent.performance}.")
        st.info(f"The Agent goal is: {bfsBoatAgent.goal} .")
                
        drawBtn(env, bfsBoatAgent, nodeColors)
    
            
        
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"],st.session_state["agent"], st.session_state["nodeColors"])


if __name__ == '__main__':
    main()