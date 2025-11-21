from collections import defaultdict, Counter


class UniversalDict:
    """A universal dict maps any key to the same value. 
    We use it here as the domains dict for CSPs 
    in which all variables have the same domain.
    >>> d = UniversalDict(list('RGB'))
    >>> d['SA']
    ['R','G','B']
    """

    def __init__(self, value): 
      self.value = value

    def __getitem__(self, key): 
      return self.value

    def __repr__(self): 
      return f'Any from {self.value}'


def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def parse_neighbors(neighbors):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors. The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name. If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    True
    """
    dic = defaultdict(list)
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        #print(A)
        A = A.strip()
        for B in Aneighbors.split():
            dic[A].append(B)
            dic[B].append(A)
    return dic


def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))

def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)


def not_sitting_adjacent_constraint(A, a, B, b):
  """A constraint that restricts two people from sitting next to each other in the dinner problem"""
  # Difference of 1 is adjacent seat
  # Difference of 5 would be seats 1 and 6, which are adjacent
  return abs(a - b) != 1 and abs(a - b) != 5


def dinner_constraint(A, a, B, b):
  """A constraint that encapsulates all rules for the dinner problem"""

  """No two people can sit on the same chair"""
  all_diff = different_values_constraint(A, a, B, b)

  """A & B. B & E. C & B. Each pair cannot sit together"""
  safe_seating = True
  if set([A, B]) in [set(['A', 'B']), set(['B', 'E']), set(['C', 'B'])]:
    safe_seating = not_sitting_adjacent_constraint(A, a, B, b)

  return all_diff and safe_seating


def handle_dinner_fail_message(var, value, assignment):
    # Check that B doesn't sit next to the one's it has constraints with
    if var == "B":
        for other in ("A", "C", "E"):
            if other in assignment:
                diff = abs(value - assignment[other])
                if diff in (1, 5):
                    return f"B cannot sit next to {other}"
                
    if var in ("A", "C", "E"):
        b_val = assignment["B"]
        diff = abs(assignment[var] - b_val)
        if diff in (1, 5):
            return f"{var} cannot sit next to B"
                
    for other, other_val in assignment.items():
        if other != var and other_val == value:
            return f"{var} cannot sit in chair {value} because {other} is there"
    return "Conflicts with constraints"