import numpy as np
import math
import random
from collections import deque


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

# Actions dictionary
actions_dict = {
    LEFT: 'left',
    UP: 'up',
    RIGHT: 'right',
    DOWN: 'down',
}

def makeMaze(n, ghosts=True, max_attempts=100):
    '''
    Legend:
    0 → wall
    1 → empty
    2 → food
    3 → ghost
    4 → init
    5 → goal
    6 → init + food
    7 → goal + food
    '''
    for attempt in range(max_attempts):
        size = (n, n)
        proba_0 = 0.2   # 20% walls (0)
        proba_food = 0.1  # 10% food (2)
        arrMaze = np.random.choice(
            [0, 1, 2], 
            size=size, 
            p=[proba_0, 1 - proba_0 - proba_food, proba_food]
        )

        # --- Place init ---
        valid_positions = list(zip(*np.where(arrMaze != 0)))
        np.random.shuffle(valid_positions)
        init = valid_positions.pop()
        if arrMaze[init] == 2:
            arrMaze[init] = 6
        else:
            arrMaze[init] = 4

        # --- Place goal ---
        goal = valid_positions.pop()
        if arrMaze[goal] == 2:
            arrMaze[goal] = 7
        else:
            arrMaze[goal] = 5

        # --- Place ghosts ---
        if ghosts:
            ghost_positions = []
            while len(ghost_positions) < 5 and valid_positions:
                pos = valid_positions.pop()
                if arrMaze[pos] in [1, 2]:
                    arrMaze[pos] = 3
                    ghost_positions.append(pos)

        # --- Collect food positions ---
        food_positions = list(zip(*np.where(np.isin(arrMaze, [2, 6, 7]))))

        # --- BFS to check reachability ---
        reachable = set()
        queue = deque([init])
        visited = set([init])

        while queue:
            x, y = queue.popleft()
            reachable.add((x, y))
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < n and 0 <= ny < n and arrMaze[nx, ny] != 0:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        # Check if all food and goal are reachable
        if all(pos in reachable for pos in food_positions + [goal]):
            return arrMaze, init, goal, food_positions
        # else: retry

    raise RuntimeError("Failed to generate a fully reachable maze after {} attempts".format(max_attempts))


# Global variables to hold the figure, axes, and agent patch
_draw_maze_state = {
    'fig': None,
    'ax': None,
    'agent_patch': None,
    'heatmap': None
}

from IPython.display import display, clear_output

def draw_maze(maze, agentState=(-1, -1)):
    global _draw_maze_state
    ai, aj = agentState

    base_colors = [
        'black',    # 0 - wall
        'white',    # 1 - empty
        'orange',   # 2 - food
        'red',      # 3 - ghost
        'green',    # 4 - init
        'pink',     # 5 - goal
        'olive',    # 6 - init + food
        'violet'    # 7 - goal + food
    ]
    cmap = ListedColormap(base_colors)
    bounds = np.arange(-0.5, 8.5, 1)
    norm = BoundaryNorm(bounds, cmap.N)

    if _draw_maze_state['fig'] is None:
        # First call: create figure and axes
        fig, ax = plt.subplots()
        heatmap = sns.heatmap(
            maze,
            cmap=cmap,
            norm=norm,
            cbar=False,
            square=True,
            linewidths=0.5,
            linecolor='black',
            ax=ax
        )
        agent_patch = None
        if ai >= 0 and aj >= 0:
            agent_patch = patches.Rectangle(
                (aj, ai), 1, 1,
                fill=False,
                edgecolor='cyan',
                lw=2
            )
            ax.add_patch(agent_patch)
        _draw_maze_state.update({
            'fig': fig,
            'ax': ax,
            'agent_patch': agent_patch,
            'heatmap': heatmap
        })
        plt.show()
    else:
        # Subsequent calls: update heatmap data
        fig = _draw_maze_state['fig']
        ax = _draw_maze_state['ax']

        ax.clear()
        sns.heatmap(
            maze,
            cmap=cmap,
            norm=norm,
            cbar=False,
            square=True,
            linewidths=0.5,
            linecolor='black',
            ax=ax
        )
        # Update agent position
        if ai >= 0 and aj >= 0:
            agent_patch = patches.Rectangle(
                (aj, ai), 1, 1,
                fill=False,
                edgecolor='cyan',
                lw=2
            )
            ax.add_patch(agent_patch)
            _draw_maze_state['agent_patch'] = agent_patch

        clear_output(wait=True)
        display(fig)



def defineMazeActions(arr):
  n=arr.shape[0]
  mazeAvailableActions={}
  for i in range(n):
    for j in range(n):
      if i==0 and j==0:
        mazeAvailableActions.setdefault((i,j),[actions_dict[2],actions_dict[3]])
      elif i==0 and j==n-1:
        mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[3]])  
      elif i==n-1 and j==0:
        mazeAvailableActions.setdefault((i,j),[actions_dict[1],actions_dict[2]])
      elif i==n-1 and j==n-1:
        mazeAvailableActions.setdefault((i,j),[])
      elif i==0:
        mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[2],actions_dict[3]])
      elif i==n-1:
        mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1],actions_dict[2]])
      elif j==0:
        mazeAvailableActions.setdefault((i,j),[actions_dict[1],actions_dict[2],actions_dict[3]])
      elif j==n-1:
        mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1],actions_dict[3]])
      else:
        mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1],actions_dict[2],actions_dict[3]])
  return mazeAvailableActions


def defineMazeAvailableActions(arr):
  n=arr.shape[0]
  mazeAvailableActions={}
  for i in range(n):
    for j in range(n):
      if i==0 and j==0:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[2],actions_dict[3]])
          if arr[i+1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[3])
          if arr[i,j+1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[2])
      elif i==0 and j==n-1:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[3]])
          if arr[i+1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[3])
          if arr[i,j-1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[0])
      elif i==n-1 and j==0:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[1],actions_dict[2]])
          if arr[i-1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[1])
          if arr[i,j+1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[2])
          
      elif i==n-1 and j==n-1:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1]])
          if arr[i-1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[1])
          if arr[i,j-1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[0])
      elif i==0:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[2],actions_dict[3]])
          if arr[i,j-1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[0])
          if arr[i,j+1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[2])
          if arr[i+1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[3])
      elif i==n-1:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1],actions_dict[2]])
          if arr[i,j-1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[0])
          if arr[i,j+1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[2])
          if arr[i-1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[1]) 
      elif j==0:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[1],actions_dict[2],actions_dict[3]])
          if arr[i-1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[1]) 
          if arr[i+1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[3])
          if arr[i,j+1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[2])
      elif j==n-1:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1],actions_dict[3]])
          if arr[i,j-1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[0])
          if arr[i-1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[1]) 
          if arr[i+1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[3])
      else:
        if arr[i,j]==0:
          mazeAvailableActions.setdefault((i,j),[])
        else:
          mazeAvailableActions.setdefault((i,j),[actions_dict[0],actions_dict[1],actions_dict[2],actions_dict[3]])
          if arr[i-1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[1]) 
          if arr[i+1,j]==0:
            mazeAvailableActions[i,j].remove(actions_dict[3])
          if arr[i,j+1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[2])
          if arr[i,j-1]==0:
            mazeAvailableActions[i,j].remove(actions_dict[0])
        
  return mazeAvailableActions

def makeMazeTransformationModel(mazeActs):
    mazeStateSpace={}
    for key in mazeActs:
      for action in mazeActs[key]:
        if action=='left':
          x=key[0]
          y=key[1]-1
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
        elif action=='up':
          x=key[0]-1
          y=key[1]
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
        elif action=='right':
          x=key[0]
          y=key[1]+1
          mazeStateSpace.setdefault(key,{})[action]=(x,y)
        elif action=='down':
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
  x = []
  y = []
  
  for elem in keyList:
    x.append(elem[1]*100)
    y.append(elem[0]*100)
 
  zipped = zip(x, y)
  return dict(zip(keyList, zipped))



def intTupleTostr(t):
  return "-".join(str(item) for item in t)




