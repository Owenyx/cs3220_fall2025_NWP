from src.graphClass import Graph

'''
We only extend this to get rid of the functionality that the Grpah class has to make
the graph symmetrical
'''
class MazeGraph(Graph):
  def __init__(self, graph_dict=None):
    self.graph_dict = graph_dict or {}