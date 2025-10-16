from src.PS_agentPrograms import *
from src.mazeProblemSolvingAgentSMARTClass import MazeProblemSolvingAgentSMART
from src.task.SatelliteAgent import SatelliteAgent

def ProblemSolvingMazeAgentBFS(initState,mazeWorldGraph,goalState):
    return MazeProblemSolvingAgentSMART(initState,mazeWorldGraph,goalState,BestFirstSearchAgentProgram())

def ProblemSolvingSatelliteAgentBFS(initState,mazeWorldGraph,goalState):
    return SatelliteAgent(initState,mazeWorldGraph,goalState,BestFirstSearchAgentProgram('''Path cost fn?'''))

def ProblemSolvingSatelliteAgentIDS(initState,mazeWorldGraph,goalState):
    return SatelliteAgent(initState,mazeWorldGraph,goalState,IDSSearchAgentProgram())