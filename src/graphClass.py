class Graph:
    def __init__(self, graph_dict=None, action_costs=None):
      '''
      graph_dict is { src: { dst: action } }
      action_costs is { action: cost }
      '''
      self.origin = graph_dict
      self.graph_dict = dict()
      self.make_graph(graph_dict, action_costs)

    def make_graph(self, graph_dict, action_costs):
        """Make the graph into {src: {dst: cost}}"""
        for src in list(graph_dict.keys()): 
            for (dst, action) in graph_dict[src].items(): # B is reachable from A through action
                self.connect(src, dst, action_costs[action])

    def connect(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graph_dict.setdefault(A, {})[B] = distance 

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        return [k for k in self.graph_dict.keys()]
