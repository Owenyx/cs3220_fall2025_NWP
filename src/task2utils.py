given = {
  (1, 2): [1],
  (1, 8): [6],
  (2, 1): [3],
  (2, 3): [9],
  (2, 7): [1],
  (2, 9): [5],
  (3, 2): [8],
  (3, 4): [3],
  (3, 6): [5],
  (3, 8): [7],
  (4, 3): [2],
  (4, 5): [7],
  (4, 7): [8],
  (5, 4): [6],
  (5, 6): [8],
  (6, 3): [8],
  (6, 5): [9],
  (6, 7): [2],
  (7, 2): [2],
  (7, 4): [4],
  (7, 6): [1],
  (7, 8): [9],
  (8, 1): [9],
  (8, 3): [4],
  (8, 7): [6],
  (8, 9): [1],
  (9, 2): [3],
  (9, 8): [8],
}

allVals = [1, 2, 3, 4, 5, 6, 7, 8, 9]

asteriskCells = [(2, 5), (3, 3), (3, 7), (5, 2), (5, 5), (5, 8), (7, 3), (7, 7), (8, 5)]


def sameRow(key):
    row, col = key
    return [(row, j) for j in range(1, 10) if j != col]

def sameCol(key):
    row, col = key
    return [(i, col) for i in range(1, 10) if i != row]

def sameHouse(key):
    row, col = key
    neighbors = []
    houseRow = (row + 2) // 3 # e.g. Cells 1, 2, 3 (+2) -> 3, 4, 5 (//3) -> 1, 1, 1
    houseCol = (col + 2) // 3
    for i in range(3 * (houseRow - 1) + 1, 3 * houseRow + 1):
      for j in range(3 * (houseCol - 1) + 1, 3 * houseCol + 1):
        if i != row or j != col:
           neighbors.append((i, j))
    
    return neighbors
    
def asteriskNeighbours(key):
   if key in asteriskCells:
      return [cell for cell in asteriskCells if cell != key]
   else:
      return []
   
