from src.PS_agentPrograms import *
from src.mazeProblemSolvingAgentSMARTClass import MazeProblemSolvingAgentSMART

def ProblemSolvingMazeAgentBFS(initState,mazeWorldGraph,goalState):
    return MazeProblemSolvingAgentSMART(initState,mazeWorldGraph,goalState,BestFirstSearchAgentProgram())

def ProblemSolvingSatelliteAgentBFS(initState,mazeWorldGraph,goalState):
    return MazeProblemSolvingAgentSMART(initState,mazeWorldGraph,goalState,BestFirstSearchAgentProgram())