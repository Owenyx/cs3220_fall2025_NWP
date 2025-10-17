#How do we decide which node from the frontier to expand next?
from src.nodeClass import Node
from queue import PriorityQueue
from src.mazeProblemClass import MazeProblem
from src.nodeClass import Node

nodeColors={
    "start":"red",
    "goal": "green",
    "frontier": "orange",
    "expanded":"pink"
}

def BestFirstSearchAgentProgram(f=None):
  #with BFS we choose a node, n, with minimum value of some evaluation function, f (n).
    
    def program(problem):

      node = Node(problem.initial)
      #node.color=nodeColors["start"]
      #print(node.state)
      frontier = PriorityQueue()
      frontier.put((node.path_cost, node))
      print(f"The {node} is being pushed to frontier ...")
      #node.color=nodeColors["frontier"]
      reached = {problem.initial:node}

      while not frontier.empty():
        node = frontier.get()[1]
        #node.color=nodeColors["expanded"]
        print(f"The {node} is being extracted from frontier ...")

        print(f'Path cost: {node.path_cost}')

        if problem.goal_test(node.state):
          node.color=nodeColors["goal"]
          print(f"We have found our goal:  {node}!")
          return node

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost < reached[child.state].path_cost:
                frontier.put((1,child))
                print(f"The child {child} is being pushed to frontier ...")
                #child.color=nodeColors["frontier"]
                reached.update({child.state:child})
            
        #node.color=nodeColors["expanded"]
      return None

    return program
  

def DLS(problem: MazeProblem, limit):
    return recursiveDLS(Node(problem.initial), problem, limit)
  
def recursiveDLS(node: Node, problem: MazeProblem, limit):
    print(f"Checking node {node.state}")

    has_cutoff = False

    if problem.goal_test(node.state):
        return node
   
    if node.depth >= limit:
        return 'cutoff'
   
    for successor in node.expand(problem):
        result = recursiveDLS(successor, problem, limit)
        if result == 'cutoff':
            has_cutoff = True
    
        elif result != 'failure':
            return result
    
    if has_cutoff:
       return 'cutoff'
    else:
       return 'failure'


def IDSSearchAgentProgram(f=None):
    max_depth=50

    def program(problem):
      for depth in range(max_depth):
        print(f'\nCurrent Depth: {depth}')
        result = DLS(problem, depth)
        if result != 'cutoff':

          if result == 'failure':
            return None  # no solution exists
          else:
            return result  # found solution
            
      return None
            
    return program










def BestFirstSearchAgentProgramForShow(f=None):
  #with BFS we choose a node, n, with minimum value of some evaluation function, f (n).
    
    def program(problem):
      #print(111)
      steps = 0
      allNodeColors = []
      nodeColors = {k : 'white' for k in problem.graph.nodes()}

      node = Node(problem.initial)
      nodeColors[node.state] = "yellow"
      steps += 1
      allNodeColors.append(dict(nodeColors))

      #print(node.state)
      frontier = PriorityQueue()
      frontier.put((1,node))

      nodeColors[node.state] = "orange"
      steps += 1
      allNodeColors.append(dict(nodeColors))



      reached = {problem.initial:node}

      while frontier:
        node = frontier.get()[1]
        nodeColors[node.state] = "red"
        steps += 1
        allNodeColors.append(dict(nodeColors))
        #print(node)

        if problem.goal_test(node.state):
          nodeColors[node.state] = "green"
          steps += 1
          allNodeColors.append(dict(nodeColors))
          return (node,steps,allNodeColors)
          

        #reached.add(node.state)
        for child in node.expand(problem):
            if child.state not in reached or child.path_cost<reached[child.state].path_cost:
                frontier.put((1,child))
                nodeColors[child.state] = "orange"
                steps += 1
                allNodeColors.append(dict(nodeColors))

                reached.update({child.state:child})

        # modify the color of explored nodes to blue
        nodeColors[node.state] = "blue"
        steps += 1
        allNodeColors.append(dict(nodeColors))
            
      return None

    return program