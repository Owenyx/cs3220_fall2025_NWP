# Shorthand for actions
bl = 'Boat Left'
br = 'Boat Right'
lw = 'Load Wolf'
uw = 'Unload Wolf'
lg = 'Load Goat'
ug = 'Unload Goat'
lc = 'Load Cabbage'
uc = 'Unload Cabbage'

boat_action_costs = {
    bl: 1,
    br: 1,
    lw: 3,
    uw: 3,
    lg: 3,
    ug: 3,
    lc: 2,
    uc: 2,
}

boat_data = dict(
    LLLL={lc: 'LLBL', lg: 'LBLL', lw: 'BLLL'},
    LLBL={uc: 'LLLL'},
    LLRL={lg: 'LBRL', lw: 'BLRL'},
    LBLL={ug: 'LLLL', br: 'LBLR'},
    LBLR={ug: 'LRLR', bl: 'LBLL'},
    LBRL={lg: 'LLRL', br: 'LBRR'},
    LBRR={ug: 'LRRR', bl: 'LBRL'},
    LRLL={br: 'LRLR', lc: 'LRBL', lw: 'BRLL'},
    LRLR={lg: 'LBLR', bl: 'LRLL'},
    LRBL={uc: 'LRLL', br: 'LRBR'},
    LRBR={uc: 'LRRR', bl: 'LRBL'},
    LRRR={lc: 'LRBR', lg: 'LBRR'},

    BLLL={uw: 'LLLL'},
    BLRL={uw: 'LLRL', br: 'BLRR'},
    BLRR={uw: 'RLRR', bl: 'BLRL'},
    BRLL={uw: 'LRLL', br: 'BRLR'},
    BRLR={uw: 'RRLR', bl: 'BRLL'},
    BRRR={uw: 'RRRR'},

    RLLL={lc: 'RLBL', lg: 'RBLL'},
    RLBL={br: 'RLBR', uc: 'RLLL'},
    RLBR={bl: 'RLBL', uc: 'RLRR'},
    RLRL={br: 'RLRR', lg: 'RBRL'},
    RLRR={bl: 'RLRL', lc: 'RLBR', lw: 'BLRR'},
    RBLL={br: 'RBLR', ug: 'RLLL'},
    RBLR={bl: 'RBLL', ug: 'RRLR'},
    RBRL={br: 'RBRR', ug: 'RLRL'},
    RBRR={bl: 'RBRL', ug: 'RRRR'},
    RRLR={lg: 'RBLR', lw: 'BRLR'},
    RRBR={uc: 'RRRR'},
    RRRR={lc: 'RRBR', lg: 'RBRR', lw: 'BRRR'},
)


node_coords = {
  'LLLL': (-30, -400),
  'BLLL': (-80, -400),
  'LLBL': (20, -400),

  'LBLL': (-30, -350),
  'LBLR': (30, -300),
  'LRLR': (30, -250),
  'LRLL': (-30, -200),

  'BRLL': (-100, -150),
  'BRLR': (-150, -150),
  'RRLR': (-200, -150),
  'RBLR': (-250, -150),
  'RBLL': (-250, -50),
  'RLLL': (-200, -50),
  'RLBL': (-150, -50),
  'RLBR': (-100, -50),

  'LRBL': (100, -150),
  'LRBR': (150, -150),
  'LRRR': (200, -150),
  'LBRR': (250, -150),
  'LBRL': (250, -50),
  'LLRL': (200, -50),
  'BLRL': (150, -50),
  'BLRR': (100, -50),

  'RLRR': (30, 0),
  'RLRL': (-30, 50),
  'RBRL': (-30, 100),
  'RBRR': (30, 150),
  'RRRR': (30, 200),
  'RRBR': (80, 200),
  'BRRR': (-20, 200),
}