class Graph:
  def __init__(self, graph_dict=None, action_costs=None):
    self.origin=graph_dict # Original data the original format
    self.graph_dict = dict()
    # This changes the backwards data to be normal, where it is {a: {b: cost}}
    # Actions is not stored here
    self.make_graph(graph_dict, action_costs)


  def make_graph(self, graph_dict, action_costs):
    for a in graph_dict.keys():
      for (act, b) in graph_dict[a].items():
        self.connect(a, b, action_costs[act])

      # Create nodes even if no action available
      if len(graph_dict[a].keys()) == 0:
         self.graph_dict[a] = {}

  def connect(self, A, B, distance):
    self.graph_dict.setdefault(A, {})[B] = distance

  def nodes(self):
    return [k for k in self.graph_dict.keys()]

  def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)