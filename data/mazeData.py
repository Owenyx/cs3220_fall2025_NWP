# Shorthand
a = 'Advance'
l = 'Left'
r = 'Right'


maze_data=dict(
    N1 =dict(N2=a),
    N2 =dict(N3=a, N6=l),
    N3 =dict(),
    N4 =dict(),
    N5 =dict(N4=a, N9=r),
    N6 =dict(N5=l, N7=r),
    N7 =dict(N8=a, N12=l),
    N8 =dict(),
    N9 =dict(N10=r, N13=a),
    N10=dict(),
    N11=dict(),
    N12=dict(N11=l, N15=a),
    N13=dict(N14=r, N16=a),
    N14=dict(N24=a),
    N15=dict(N14=l, N19=a),
    N16=dict(N17=r, N20=a),
    N17=dict(N23=l),
    N18=dict(N25=r),
    N19=dict(N18=l, N21=a),
    N20=dict(),
    N21=dict(),
    N22=dict(),
    N23=dict(N22=l, N24=r),
    N24=dict(N25=a),
    N25=dict(N26=a),
    N26=dict(),
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