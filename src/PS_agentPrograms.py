#How do we decide which node from the frontier to expand next?
from src.nodeClass import Node
from queue import PriorityQueue


def A_StarSearchAgentProgram(f=None):

    def program(problem):
        node = Node(problem.initial)

        # Ensure goals are always a list
        goals = problem.goal if isinstance(problem.goal, list) else [problem.goal]

        # Helper heuristic: min distance to any goal
        def heuristic(state):
            return min(f(state, g) for g in goals)

        frontier = PriorityQueue()
        h = node.path_cost + round(heuristic(node.state), 3)
        frontier.put((h, node))
        reached = {node.state: node}

        expanded_count = 0  # Track number of expanded nodes

        while not frontier.empty():
            print('Queue:', [tuple(map(int, x[1].state)) for x in frontier.queue])
            node = frontier.get()[1]
            state_int = tuple(map(int, node.state))
            print(f"Extracted: {state_int} with f = {h}")
            expanded_count += 1

            if node.state in goals:
                print(f"We have found our goal: {node.state}")
                print(f"Total nodes expanded: {expanded_count}")
                return node

            for child in node.expand(problem):
                if child.state not in reached or child.path_cost < reached[child.state].path_cost:
                    h = child.path_cost + round(heuristic(child.state), 3)
                    frontier.put((h, child))
                    reached[child.state] = child
                    print(f"Child added to frontier: {child.state}")
        
        print(f"Total nodes expanded: {expanded_count}")
        return None

    return program


def IDA_SearchAgentProgram(f=None):

    def program(problem):

        class StackNode:
            """Represents a node in the DFS stack with path cost."""
            def __init__(self, node, g):
                self.node = node
                self.g = g  # path cost

        root = Node(problem.initial)
        goals = problem.goal if isinstance(problem.goal, list) else [problem.goal]

        # Helper heuristic: min distance to any goal
        def heuristic(state):
            return min(f(state, g) for g in goals)

        threshold = heuristic(root.state)
        expanded_count = 0

        while True:
            stack = [StackNode(root, root.path_cost)]
            min_threshold = float('inf')
            reached = {root.state: root.path_cost}

            print(f"New IDA* iteration with threshold: {threshold}")

            while stack:
                current = stack.pop()
                node = current.node
                g = current.g
                f_val = g + heuristic(node.state)
                expanded_count += 1

                state_int = tuple(map(int, node.state))
                print(f"Popped: {state_int} with f = {f_val}")

                if f_val > threshold:
                    if f_val < min_threshold:
                        min_threshold = f_val
                    continue

                if node.state in goals:
                    print(f"We have found our goal: {node.state}")
                    print(f"Total nodes expanded: {expanded_count}")
                    return node

                for child in reversed(node.expand(problem)):
                    g_child = child.path_cost
                    if child.state not in reached or g_child < reached[child.state]:
                        stack.append(StackNode(child, g_child))
                        reached[child.state] = g_child
                        print(f"Child added to stack: {child.state} with g={g_child}")

            if min_threshold == float('inf'):
                print(f"No solution found. Total nodes expanded: {expanded_count}")
                return None  # No solution
            threshold = min_threshold  # Increase threshold for next iteration
            print(f"Threshold updated to: {threshold}")

    return program