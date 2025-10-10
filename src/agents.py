# for the Assignment3

from src.PS_agentPrograms import *
from src.task1.BoatProblemSolvingAgent import BoatProblemSolvingAgent
from src.task2.MazeProblemSolvingAgent import MazeProblemSolvingAgent


def ProblemSolvingBoatAgentBFS(initState, BoatGraph, goalState):
    return BoatProblemSolvingAgent(initState, BoatGraph, goalState, BestFirstSearchAgentProgram())


def ProblemSolvingMazeAgentBFS(initState, MazeGraph, goalStates, endState):
    return MazeProblemSolvingAgent(initState, MazeGraph, goalStates, endState, BestFirstSearchAgentProgram())