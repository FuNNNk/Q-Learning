possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def create_qtable(matrix, obstacles, endpoints):
    Qtable = dict()
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            Qtable[(i, j)] = dict()
            for action in possible_moves:
                next_state = (i + action[0], j + action[1])
                if next_state[0] < 0 or next_state[1] < 0 or next_state[1] >= len(matrix) or next_state[1] >= len(
                        matrix):
                    Qtable[(i, j)][action] = None
                elif next_state in obstacles:
                    Qtable[(i, j)][action] = None
                elif next_state in endpoints:
                    Qtable[(i, j)][action] = 1
                else:
                    Qtable[(i, j)][action] = -0.004
    return Qtable


def get_valid_actions(state, Qtable):
    valid_actions = list(filter(lambda x: Qtable[state][x] is not None, Qtable[state].keys()))
    return valid_actions


table = create_qtable([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [(1, 1)], [(2, 2)])
print(table)
print(get_valid_actions((0, 0), table))
