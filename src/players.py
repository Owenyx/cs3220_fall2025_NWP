import random

def smart_player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    # O: Remember - the seach returns val, move so here we extract move
    return lambda game, state: search_algorithm(game, state)[1]


def random_player(game, state):
    """A game player who  uses random choice to do a next move"""
    return random.choice(list(game.actions(state)))


def human_player(game, state):
    actions = list(game.actions(state))

    act = None
    while act not in actions:
        actsString = ', '.join(map(str, actions))
        act = int(input(f'Count by {actsString} ?'))

    return act