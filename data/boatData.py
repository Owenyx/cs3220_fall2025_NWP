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

boat_data=dict(
    LLLL=dict(LLBL=lc, LBLL=lg, BLLL=lw),
    LLBL=dict(LLLL=uc),
    LLRL=dict(LBRL=lg, BLRL=lw),
    LBLL=dict(LLLL=ug, LBLR=br),
    LBLR=dict(LRLR=ug, LBLL=bl),
    LBRL=dict(LLRL=lg, LBRR=br),
    LBRR=dict(LRRR=ug, LBRL=bl),
    LRLL=dict(LRLR=br, LRBL=lc, BRLL=lw),
    LRLR=dict(LBLR=lg, LRLL=bl),
    LRBL=dict(LRLL=uc, LRBR=br),
    LRBR=dict(LRRR=uc, LRBL=bl),
    LRRR=dict(LRBR=lc, LBRR=lg),
    
    BLLL=dict(LLLL=uw),
    BLRL=dict(LLRL=uw, BLRR=br),
    BLRR=dict(RLRR=uw, BLRL=bl),
    BRLL=dict(LRLL=uw, BRLR=br),
    BRLR=dict(RRLR=uw, BRLL=bl),
    BRRR=dict(RRRR=uw),

    RLLL=dict(RLBL=lc, RBLL=lg),
    RLBL=dict(RLBR=br, RLLL=uc),
    RLBR=dict(RLBL=bl, RLRR=uc),
    RLRL=dict(RLRR=br, RBRL=lg),
    RLRR=dict(RLRL=bl, RLBR=lc, BLRR=lw),
    RBLL=dict(RBLR=br, RLLL=ug),
    RBLR=dict(RBLL=bl, RRLR=ug),
    RBRL=dict(RBRR=br, RLRL=ug),
    RBRR=dict(RBRL=bl, RRRR=ug),
    RRLR=dict(RBLR=lg, BRLR=lw),
    RRBR=dict(RRRR=uc),
    RRRR=dict(RRBR=lc, RBRR=lg, BRRR=lw),
)