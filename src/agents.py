# for the Assignment3

from src.PS_agentPrograms import *
from src.vacuumProblemSolvingAgentSMARTClass import VacuumProblemSolvingAgentSMART
#from vacuumProblemSolvingAgentShowClass import VacuumProblemSolvingAgentDraw
from src.navProblemSolvingAgentClass import navProblemSolvingAgent
from src.task1.BoatProblemSolvingAgent import BoatProblemSolvingAgent
from src.task2.MazeProblemSolvingAgent import MazeProblemSolvingAgent


def ProblemSolvingVacuumAgentBFS(initState,vacuumWorldGraph,goalState):
    return VacuumProblemSolvingAgentSMART(initState,vacuumWorldGraph,goalState,BestFirstSearchAgentProgram())

 
def ProblemSolvingNavAgentBFS(initState,WorldGraph,goalState):
    return navProblemSolvingAgent(initState,WorldGraph,goalState,BestFirstSearchAgentProgram())


def ProblemSolvingBoatAgentBFS(initState, BoatGraph, goalState):
    return BoatProblemSolvingAgent(initState, BoatGraph, goalState, BestFirstSearchAgentProgram())


def ProblemSolvingMazeAgentBFS(initState, MazeGraph, goalStates, endState):
    return MazeProblemSolvingAgent(initState, MazeGraph, goalStates, endState, BestFirstSearchAgentProgram())

# def ProblemSolvingVacuumAgentBFSwithShow(initState,vacuumWorldGraph,goalState):
#     return VacuumProblemSolvingAgentDraw(initState,vacuumWorldGraph,goalState,BestFirstSearchAgentProgramForShow())