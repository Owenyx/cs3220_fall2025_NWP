# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.CSPclass import CSPBasic
from src.algorithms import AC3
from src.utils import different_values_constraint
from src.task2utils import sameCol, sameRow, sameHouse, asteriskNeighbours, given, allVals


def main():
    tab1, tab2 = st.tabs(["Initial Domains", "Graph of constraints"])
    
    sudokuNeighbors,sudokuDomains,sudokuConstraints=getSudokuData()        
    basicSudokuCSP=CSPBasic(variables=sudokuNeighbors.keys(),neighbors=sudokuNeighbors, domains=sudokuDomains, constraints=sudokuConstraints)

    prunedSudokuCSP=CSPBasic(variables=sudokuNeighbors.keys(),neighbors=sudokuNeighbors, domains=sudokuDomains, constraints=sudokuConstraints)
    AC3(prunedSudokuCSP)
            
    
    with tab1: # Pre-AC3
        st.header("CSP: Sudoku Scheduling Problem - Pre-AC3")
        
        buildGraph(basicSudokuCSP, False)
        
    with tab2: # Post-AC3
        
          st.success("AC-3 applied. Check new domains")
          buildGraph(prunedSudokuCSP, True)
        
        
def getSudokuData():
    sudokuNeighbors = {}

    for i in range(1, 10):
        for j in range(1, 10):
            key = (i, j)
            sudokuNeighbors[key] = set(sameCol(key) + sameRow(key) + sameHouse(key) + asteriskNeighbours(key))

    sudokuDomains = {}

    for i in range(1, 10):
        for j in range(1, 10):
            key = (i, j)
            sudokuDomains[key] = allVals

    # Set Pre-filled values
    for key in given:
        sudokuDomains[key] = given[key]

    sudokuDomains
    
    sudokuConstraints = different_values_constraint
    return sudokuNeighbors,sudokuDomains,sudokuConstraints

        
def buildGraph(SudokuCSP, ac3=False):
    netSudoku= Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
                ) 
    
    nodeTitlesDict={}
    nodeLabelsDict={}
    nodes=list(SudokuCSP.variables)

    for node in nodes:
        if ac3:
            string_list = [str(i) for i in SudokuCSP.curr_domains[node]]
            
        else:
            string_list = [str(i) for i in SudokuCSP.domains[node]]
        nodeTitlesDict.setdefault(node, ",".join(string_list) )
            
        nodeLabelsDict.setdefault(node,"")      
           
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    for node in nodes:
        g.add_node(node, size=10, title=nodeTitlesDict[node], label=nodeLabelsDict[node])

    # Add edges
    for nodeFrom in SudokuCSP.neighbors.keys():
        for nodeTo in SudokuCSP.neighbors[nodeFrom]:        
            if nodeFrom[0]==nodeTo[0]: # row const-s
                g.add_edge(nodeFrom,nodeTo, color="red")
            elif nodeFrom[1]==nodeTo[1]: # col const-s
                g.add_edge(nodeFrom,nodeTo, color="blue")
            else:
                g.add_edge(nodeFrom,nodeTo, color="green") # diag con-s

    # generate the graph
    netSudoku.from_nx(g)
    
    netSudoku.save_graph(f'L6_Task2.html')
    HtmlFile = open(f'L6_Task2.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    
if __name__ == '__main__':
    main()