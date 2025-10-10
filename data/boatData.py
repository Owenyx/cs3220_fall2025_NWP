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