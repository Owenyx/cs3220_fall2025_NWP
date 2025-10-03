import random

vacuumWorldStates=['Dirty','Clean']
agenLocations=['Left','Right']
agentActions=['Suck','Left','Right']

'''
Hanna couldn't make this work because pyvis does not accept tuples as keys for dictionary, unlike normal Python
'''
# DDL=(vacuumWorldStates[0],vacuumWorldStates[0],agenLocations[0])
# DDR=(vacuumWorldStates[0],vacuumWorldStates[0],agenLocations[1])
# DCL=(vacuumWorldStates[0],vacuumWorldStates[1],agenLocations[0])
# DCR=(vacuumWorldStates[0],vacuumWorldStates[1],agenLocations[1])
# CDL=(vacuumWorldStates[1],vacuumWorldStates[0],agenLocations[0])
# CDR=(vacuumWorldStates[1],vacuumWorldStates[0],agenLocations[1])
# CCL=(vacuumWorldStates[1],vacuumWorldStates[1],agenLocations[0])
# CCR=(vacuumWorldStates[1],vacuumWorldStates[1],agenLocations[1])

# Hence, we convert to strings to use a dict keys in pyvis
DDL=''.join(map(lambda x: x[0],(vacuumWorldStates[0],vacuumWorldStates[0],agenLocations[0])))
DDR=''.join(map(lambda x: x[0],(vacuumWorldStates[0],vacuumWorldStates[0],agenLocations[1])))
DCL=''.join(map(lambda x: x[0],(vacuumWorldStates[0],vacuumWorldStates[1],agenLocations[0])))
DCR=''.join(map(lambda x: x[0],(vacuumWorldStates[0],vacuumWorldStates[1],agenLocations[1])))
CDL=''.join(map(lambda x: x[0],(vacuumWorldStates[1],vacuumWorldStates[0],agenLocations[0])))
CDR=''.join(map(lambda x: x[0],(vacuumWorldStates[1],vacuumWorldStates[0],agenLocations[1])))
CCL=''.join(map(lambda x: x[0],(vacuumWorldStates[1],vacuumWorldStates[1],agenLocations[0])))
CCR=''.join(map(lambda x: x[0],(vacuumWorldStates[1],vacuumWorldStates[1],agenLocations[1])))

# THIS IS DIFFERENT THAN CITY DICT
# Here, she uses the actions (edges) as keys instead of the destination
# This is because dict keys must be unique, and some actions lead the the same state
# so using state as keys would lead to duplicate keys
vacuumWorld = (dict(
    DDL=dict(Suck=CDL, Left=DDL, Right=DDR),
    DDR=dict(Suck=DCR, Left=DDL, Right=DDR),
    DCL=dict(Suck=CCL, Left=DCL, Right=DCR),
    DCR=dict(Suck=DCR, Left=DCL, Right=DCR),
    CDL=dict(Suck=CDL, Left=CDL, Right=CDR),
    CDR=dict(Suck=CCR, Left=CDL, Right=CDR),
    CCL=dict(Suck=CCL, Left=CCL, Right=CCR),
    CCR=dict(Suck=CCR, Left=CCL, Right=CCR)
))

# vacuumWorldDict={
#   DDL:
#     {
#       DDL:agentActions[1],
#       DDR:agentActions[2],
#       CDL:agentActions[0]
#     },
#   DDR:
#     {
#       DDL:agentActions[1],
#       DDR:agentActions[2],
#       DCL:agentActions[0]
#     },
#   DCL:
#     {
#       DCL:agentActions[1],
#       DCR:agentActions[2],
#       CCL:agentActions[0]
#     },
#   DCR:
#     {
#       DCL:agentActions[1],
#       DCR:agentActions[2],
#       DCR:agentActions[0]
#     },
#   CDL:
#     {
#       CDL:agentActions[1],
#       CDR:agentActions[2],
#       CDL:agentActions[0]
#     },
#   CDR:
#     {
#       CDL:agentActions[1],
#       CDR:agentActions[2],
#       CCR:agentActions[0]
#     },
#   CCL:
#     {
#       CCL:agentActions[1],
#       CCR:agentActions[2],
#       CCL:agentActions[0]
#     },
#   CCR:
#     {
#       CCL:agentActions[1],
#       CCR:agentActions[2],
#       CCR:agentActions[0]
#     }  
    
    
# }


#results=[dict(Suck=CDL,Left=DDL, Right=DDR),dict(Suck=DCR, Left=DDL, Right=DDR),dict(Suck=CCL, Left=DCL, Right=DCR),dict(Suck=DCR, Left=DCL, Right=DCR),dict(Suck=CDL, Left=CDL, Right=CDR),dict(Suck=CCR, Left=CDL, Right=CDR),dict(Suck=CCL, Left=CCL, Right=CCR),dict(Suck=CCR, Left=CCL, Right=CCR)]

#d1 = {}
keyList = [DDL,DDR,DCL,DCR,CDL,CDR,CCL,CCR]


# def makeData():
#   d1 = {}
#   for i in range(len(keyList)):
#     d1[keyList[i]]=results[i]
#   return d1



def vacuumStatesLocations():
  x = []
  y = []
  n=len(keyList)
  for _ in range(n):
    x.append(random.randint(0, n+1)+100)
    y.append(random.randint(0, n+1)+100)
  zipped = zip(x, y)
  return dict(zip(keyList, zipped))



def getAction(dict):
  edge_weights = {(k, v2) : k2 for k, v in dict.items() for k2, v2 in v.items()}#actions
  return edge_weights
