import math

from src.PS_agentPrograms import A_StarSearchAgentProgram, IDA_SearchAgentProgram
from src.task.PacmanAgent import PacmanAgent

def ProblemSolvingPacmanAgentAstarEuclidian(initState,mazeWorldGraph,goalState,foodStates):
    return PacmanAgent(initState,mazeWorldGraph,goalState,foodStates,A_StarSearchAgentProgram(math.dist))

def ProblemSolvingPacmanAgentAstarManhattan(initState,mazeWorldGraph,goalState,foodStates):
    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    return PacmanAgent(initState,mazeWorldGraph,goalState,foodStates,A_StarSearchAgentProgram(manhattan))

def ProblemSolvingPacmanAgentIDA(initState,mazeWorldGraph,goalState,foodStates):
    return PacmanAgent(initState,mazeWorldGraph,goalState,foodStates,IDA_SearchAgentProgram(math.dist))