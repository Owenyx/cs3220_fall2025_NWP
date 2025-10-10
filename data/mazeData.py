# Shorthand
a = 'Advance'
l = 'Left'
r = 'Right'


maze_data = dict(
    N1={a: 'N2'},
    N2={a: 'N3', l: 'N6'},
    N3={},
    N4={},
    N5={a: 'N4', r: 'N9'},
    N6={l: 'N5', r: 'N7'},
    N7={a: 'N8', l: 'N12'},
    N8={},
    N9={r: 'N10', a: 'N13'},
    N10={},
    N11={},
    N12={l: 'N11', a: 'N15'},
    N13={r: 'N14', a: 'N16'},
    N14={a: 'N24'},
    N15={l: 'N14', a: 'N19'},
    N16={r: 'N17', a: 'N20'},
    N17={l: 'N23'},
    N18={r: 'N25'},
    N19={l: 'N18', a: 'N21'},
    N20={},
    N21={},
    N22={},
    N23={l: 'N22', r: 'N24'},
    N24={a: 'N25'},
    N25={a: 'N26'},
    N26={},
)

maze_action_costs = {
    a: 1,
    r: 1,
    l: 1,
}

# States that are not dead ends or start or end states
treasure_states = [
  'N2',
  'N5',
  'N6',
  'N7',
  'N9',
  'N12',
  'N13',
  'N14',
  'N15',
  'N16',
  'N17',
  'N18',
  'N19',
  'N23',
  'N24',
  'N25',
]