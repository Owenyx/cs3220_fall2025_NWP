# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.CSPclass import CSPBasic
from src.algorithms import AC3
from src.utils import different_values_constraint
from src.task2utils import sameCol, sameRow, sameHouse, asteriskNeighbours, given, allVals, asteriskCells
import ast


nodeColors={
    "empty":"white",
    "filled": "yellow"
}



def main():
    tab1, tab2, tab3, tab4 = st.tabs(["Initial Grid", "Initial Graph of constraints", "Pruned Grid", 'Pruned Graph of constraints'])
    
    sudokuNeighbors,sudokuDomains,sudokuConstraints=getSudokuData()        
    SudokuCSP=CSPBasic(variables=sudokuNeighbors.keys(),neighbors=sudokuNeighbors, domains=sudokuDomains, constraints=sudokuConstraints)

    AC3(SudokuCSP, display=False)


    with tab1: # Pre-AC3 grid
        buildGrid(SudokuCSP, False)

    with tab2: # Pre-AC3 Constraint graph
        st.header("CSP: Sudoku Scheduling Problem - Pre-AC3")
        buildGraph(SudokuCSP, False)
        
    with tab3: # Post-AC3
        st.success("AC-3 applied")
        buildGrid(SudokuCSP, True)

    with tab4: # Post-AC3 grid
        st.success("AC-3 applied")
        buildGraph(SudokuCSP, True)
        
        
def getSudokuData():
    neighbors = {}

    for i in range(1, 10):
        for j in range(1, 10):
            key = (i, j)
            neighbors[key] = set(sameCol(key) + sameRow(key) + sameHouse(key) + asteriskNeighbours(key))

    domains = {}

    for i in range(1, 10):
        for j in range(1, 10):
            key = (i, j)
            domains[key] = allVals

    # Set Pre-filled values
    for key in given:
        domains[key] = given[key]


    # Convert it all to strings for pyvis :/
    sudokuNeighbors = {}
    for key in neighbors:
        sudokuNeighbors[str(key)] = list(map(str, neighbors[key]))

    sudokuDomains = {}
    for key in domains:
        sudokuDomains[str(key)] = domains[key] # domain values are numbers

    sudokuConstraints = different_values_constraint
    return sudokuNeighbors,sudokuDomains,sudokuConstraints


def buildGrid(SudokuCSP, ac3):
    # Define the number of rows you want
    size = 9
    # Define the number of columns per row
    vars=list(SudokuCSP.variables)
    print(vars)
    
    
    
    j=0
    
    for i in range(size):
        # Create a set of columns for each row
        cols = st.columns(size)

        st.divider()
        
        # Place elements within each column of the current row
        for col_index, col in enumerate(cols):
            with col:
                st.write(vars[j])
                if ac3:
                    st.write(str(list(SudokuCSP.curr_domains[vars[j]])))
                else:
                    st.write(str(list(SudokuCSP.domains[vars[j]])))
            j+=1

        
def buildGraph(SudokuCSP, ac3=False):
    netSudoku= Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
                ) 
    
    nodeColorsDict={}
    nodeTitlesDict={}
    nodeLabelsDict={}
    nodes=list(SudokuCSP.variables)

    for node in nodes:
        if len(SudokuCSP.domains[node])==1:
            nodeColorsDict.setdefault(node,nodeColors["filled"])
            if ac3:
                nodeTitlesDict.setdefault(node,str(SudokuCSP.curr_domains[node][0]))
            else:
                nodeTitlesDict.setdefault(node,str(SudokuCSP.domains[node][0]))
            nodeLabelsDict.setdefault(node,str(SudokuCSP.domains[node][0]))           
        else:
            nodeColorsDict.setdefault(node,nodeColors["empty"])
            if ac3:
                string_list = [str(i) for i in SudokuCSP.curr_domains[node]]
               
            else:
                string_list = [str(i) for i in SudokuCSP.domains[node]]
            nodeTitlesDict.setdefault(node, ",".join(string_list) )
                
            nodeLabelsDict.setdefault(node,"")      


    x_coords = {}
    y_coords = {}


    for node in nodes:
        row, col = ast.literal_eval(node)
        x_coords[node] = row * 50
        y_coords[node] = col * 50

           
    # initialize graph
    g = nx.Graph()
    
    
    # add the nodes
    for node in nodes:
        g.add_node(node, size=10, title=nodeTitlesDict[node], label=nodeLabelsDict[node], x=x_coords[node],y=y_coords[node])

    # Add edges
    for nodeFrom in SudokuCSP.neighbors.keys():
        for nodeTo in SudokuCSP.neighbors[nodeFrom]:  
            if ast.literal_eval(nodeFrom) in asteriskCells and ast.literal_eval(nodeTo) in asteriskCells:
                g.add_edge(nodeFrom,nodeTo, color="violet")
            elif nodeFrom[1]==nodeTo[1]: # row const-s
                g.add_edge(nodeFrom,nodeTo, color="red")
            elif nodeFrom[4]==nodeTo[4]: # col const-s
                g.add_edge(nodeFrom,nodeTo, color="blue")
            else:
                g.add_edge(nodeFrom,nodeTo, color="green") # diag con-s

    # generate the graph
    netSudoku.from_nx(g)

    netSudoku.toggle_physics(False)
    
    netSudoku.save_graph(f'L6_Task2.html')
    HtmlFile = open(f'L6_Task2.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    
if __name__ == '__main__':
    main()