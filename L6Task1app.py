# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.CSPclass import CSPBasic
from src.algorithms import AC3
from src.utils import different_values_constraint


def main():
    tab1, tab2 = st.tabs(["Initial Domains", "Graph of constraints"])
    
    examNeighbors,examDomains,examConstraints=getExamData()        
    basicExamCSP=CSPBasic(variables=examNeighbors.keys(),neighbors=examNeighbors, domains=examDomains, constraints=examConstraints)

    prunedExamCSP=CSPBasic(variables=examNeighbors.keys(),neighbors=examNeighbors, domains=examDomains, constraints=examConstraints)
    AC3(prunedExamCSP)
            
    
    with tab1: # Pre-AC3
        st.header("CSP: Exam Scheduling Problem - Pre-AC3")
        
        buildGraph(basicExamCSP, False)
        
    with tab2: # Post-AC3
        
          st.success("AC-3 applied. Check new domains")
          buildGraph(prunedExamCSP, True)
        
        
def getExamData():
    examNeighbors = {
      'A': ['B', 'C'],
      'B': ['A', 'C', 'D'],
      'C': ['A', 'B', 'E', 'F'],
      'D': ['B', 'E'],
      'E': ['C', 'D'],
      'F': ['C', 'G'],
      'G': ['F']
    }

    examDomains = {
      'A': ['Mon', 'Tue', 'Wed'],
      'B': ['Tue'],
      'C': ['Mon', 'Tue', 'Wed'],
      'D': ['Mon', 'Tue', 'Wed'],
      'E': ['Mon', 'Tue', 'Wed'],
      'F': ['Wed'],
      'G': ['Mon', 'Tue', 'Wed'],
    }
    
    examConstraints = different_values_constraint
    return examNeighbors,examDomains,examConstraints

        
def buildGraph(ExamCSP, ac3=False):
    netExam= Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
                ) 
    
    nodeTitlesDict={}
    nodeLabelsDict={}
    nodes=list(ExamCSP.variables)

    for node in nodes:
        if ac3:
            string_list = [str(i) for i in ExamCSP.curr_domains[node]]
            
        else:
            string_list = [str(i) for i in ExamCSP.domains[node]]
        nodeTitlesDict.setdefault(node, ",".join(string_list) )
            
        nodeLabelsDict.setdefault(node,"")      
           
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    for node in nodes:
        g.add_node(node, size=10, title=nodeTitlesDict[node], label=nodeLabelsDict[node])

    # Add edges
    for nodeFrom in ExamCSP.neighbors.keys():
        for nodeTo in ExamCSP.neighbors[nodeFrom]:        
            g.add_edge(nodeFrom,nodeTo, color="green")

    # generate the graph
    netExam.from_nx(g)
    
    netExam.save_graph(f'L6_Task1.html')
    HtmlFile = open(f'L6_Task1.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    
if __name__ == '__main__':
    main()