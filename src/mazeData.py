import numpy as np
import math
import random

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


def makeMaze(n):
  size = (n,n)
  prob_asteroid = 0.25 # resulting array will have 20% of ones (asteroids)
  prop_enemy = 0.1 # Enemy is represented by a 2
  prob_0 = 1 - prob_asteroid - prop_enemy # probability of nothing being in a cell
  arrMaze=np.random.choice([0, 1, 2], size=size, p=[prob_0, prob_asteroid, prop_enemy])
  return arrMaze


def defineMazeActions(arr):
  n=arr.shape[0]
  mazeAvailableActions={}
  for i in range(n):
    for j in range(n):
      if i==0 and j==0:
        mazeAvailableActions.setdefault((i,j),[RIGHT,DOWN])
      elif i==0 and j==n-1:
        mazeAvailableActions.setdefault((i,j),[LEFT,DOWN])  
      elif i==n-1 and j==0:
        mazeAvailableActions.setdefault((i,j),[UP,RIGHT])
      elif i==n-1 and j==n-1:
        mazeAvailableActions.setdefault((i,j),[])
      elif i==0:
        mazeAvailableActions.setdefault((i,j),[LEFT,RIGHT,DOWN])
      elif i==n-1:
        mazeAvailableActions.setdefault((i,j),[LEFT,UP,RIGHT])
      elif j==0:
        mazeAvailableActions.setdefault((i,j),[UP,RIGHT,DOWN])
      elif j==n-1:
        mazeAvailableActions.setdefault((i,j),[LEFT,UP,DOWN])
      else:
        mazeAvailableActions.setdefault((i,j),[LEFT,UP,RIGHT,DOWN])
  return mazeAvailableActions


def defineMazeAvailableActions(arr):
  # Arr is maze
  n=arr.shape[0]
  mazeAvailableActions={}
  for i in range(n):
    for j in range(n):
      if i==0 and j==0:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[RIGHT,DOWN])
          if arr[i+1,j]==1:
            mazeAvailableActions[i,j].remove(DOWN)
          if arr[i,j+1]==1:
            mazeAvailableActions[i,j].remove(RIGHT)
      elif i==0 and j==n-1:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[LEFT,DOWN])
          if arr[i+1,j]==1:
            mazeAvailableActions[i,j].remove(DOWN)
          if arr[i,j-1]==1:
            mazeAvailableActions[i,j].remove(LEFT)
      elif i==n-1 and j==0:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[UP,RIGHT])
          if arr[i-1,j]==1:
            mazeAvailableActions[i,j].remove(UP)
          if arr[i,j+1]==1:
            mazeAvailableActions[i,j].remove(RIGHT)
          
      elif i==n-1 and j==n-1:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[LEFT,UP])
          if arr[i-1,j]==1:
            mazeAvailableActions[i,j].remove(LEFT)
          if arr[i,j-1]==1:
            mazeAvailableActions[i,j].remove(UP)
      elif i==0:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[LEFT,RIGHT,DOWN])
          if arr[i,j-1]==1:
            mazeAvailableActions[i,j].remove(LEFT)
          if arr[i,j+1]==1:
            mazeAvailableActions[i,j].remove(RIGHT)
          if arr[i+1,j]==1:
            mazeAvailableActions[i,j].remove(DOWN)
      elif i==n-1:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[LEFT,UP,RIGHT])
          if arr[i,j-1]==1:
            mazeAvailableActions[i,j].remove(LEFT)
          if arr[i,j+1]==1:
            mazeAvailableActions[i,j].remove(RIGHT)
          if arr[i-1,j]==1:
            mazeAvailableActions[i,j].remove(UP) 
      elif j==0:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[UP,RIGHT,DOWN])
          if arr[i-1,j]==1:
            mazeAvailableActions[i,j].remove(UP) 
          if arr[i+1,j]==1:
            mazeAvailableActions[i,j].remove(DOWN)
          if arr[i,j+1]==1:
            mazeAvailableActions[i,j].remove(RIGHT)
      elif j==n-1:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[LEFT,UP,DOWN])
          if arr[i,j-1]==1:
            mazeAvailableActions[i,j].remove(LEFT)
          if arr[i-1,j]==1:
            mazeAvailableActions[i,j].remove(UP) 
          if arr[i+1,j]==1:
            mazeAvailableActions[i,j].remove(DOWN)
      else:
        if arr[i,j]==1:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[LEFT,UP,RIGHT,DOWN])
          if arr[i-1,j]==1:
            mazeAvailableActions[i,j].remove(UP) 
          if arr[i+1,j]==1:
            mazeAvailableActions[i,j].remove(DOWN)
          if arr[i,j+1]==1:
            mazeAvailableActions[i,j].remove(RIGHT)
          if arr[i,j-1]==1:
            mazeAvailableActions[i,j].remove(LEFT)
        
  return mazeAvailableActions

def makeMazeTransformationModel(mazeActs):
    mazeStateSpace={}
    for key in mazeActs:
      for action in mazeActs[key]:
        if action==LEFT:
          x=key[0]
          y=key[1]-1
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
        elif action==UP:
          x=key[0]-1
          y=key[1]
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
        elif action==RIGHT:
          x=key[0]
          y=key[1]+1
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
        elif action==DOWN:
          x=key[0]+1
          y=key[1]
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
      if len(mazeActs[key])==0:
        mazeStateSpace.setdefault(key,{})

    return mazeStateSpace

def mazeStatesRandomLocations(n):
  x = []
  y = []
  keyList=[]
  for i in range(n):
    for j in range(n):
      keyList.append((i,j))

  #print(keyList)
  for _ in range(len(keyList)):
    x.append(random.randint(0, n+1))
    y.append(random.randint(0, n+1))
  zipped = zip(x, y)
  return dict(zip(keyList, zipped))


def mazeStatesLocations(keyList): 
  # Creates node coordinates to separate them in pyvis network
  x = []
  y = []
  
  for elem in keyList:
    x.append(elem[1]*150)
    y.append(elem[0]*150)
 
  zipped = zip(x, y)
  return dict(zip(keyList, zipped))



def intTupleTostr(t):
  return "-".join(str(item) for item in t)




