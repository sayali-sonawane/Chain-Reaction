import random


def get_argmax_key(dict_value):
    return max(dict_value, key=lambda key: dict_value[key])


def get_arg_key_wtr_agent_type(dict_value, agent_type):
    return agent_type(dict_value, key=lambda key: dict_value[key])


def get_rand_argmax_key(dict_value):
    max_value = max(dict_value.values())

    values = []
    for i in dict_value:
        if dict_value[i] == max_value:
            values.append(i)

    return random.choice(values)


def get_random_move(player, board):
    states = board.get_available_moves(player.color)
    return states[random.randrange(0, len(states))]
