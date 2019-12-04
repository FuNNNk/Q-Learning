import random

possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
LEARNING_RATE = 0.2
GAMMA = 0.2
EPSILON = 0.1
EPISODES = 2000


def create_qtable(matrix, obstacles, endpoints):
    Qtable = dict()
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            Qtable[(i, j)] = dict()
            for action in possible_moves:
                next_state = (i + action[0], j + action[1])
                if next_state[0] < 0 or next_state[1] < 0 or next_state[0] >= len(matrix) or next_state[1] >= len(
                        matrix):
                    Qtable[(i, j)][action] = -1000
                elif next_state in obstacles:
                    Qtable[(i, j)][action] = -1000
                elif next_state in endpoints:
                    Qtable[(i, j)][action] = 10
                else:
                    Qtable[(i, j)][action] = 0
    return Qtable


def get_valid_actions(state, Qtable):
    valid_actions = list(filter(lambda x: Qtable[state][x] is not None, Qtable[state].keys()))
    return valid_actions


def create_matrix(lines, columns, endpoints, obstacles):
    matrix = list()
    for i in range(lines):
        matrix.append(list())
        for j in range(columns):
            if (i, j) in endpoints:
                matrix[i].append(10)
            elif (i, j) in obstacles:
                matrix[i].append(-1000)
            else:
                matrix[i].append(0)
    return matrix


def possible_states(matrix):
    states = list()
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != -1:
                states.append((i, j))
    return states


def max_value_actions(state, qtable):
    possible_actions = get_valid_actions(state, qtable)
    if len(possible_actions) == 0:
        return 0, 0
    max_value = qtable[state][possible_actions[0]]
    for value in qtable[state].values():
        if value is not None:
            if value > max_value:
                max_value = value
    max_value_act = list()
    for action in possible_actions:
        if qtable[state][action] == max_value:
            max_value_act.append(action)
    return max_value_act


def take_action(matrix, state, action):
    end_game = False
    new_state = (state[0] + action[0], state[1] + action[1])
    if new_state[0] < 0 or new_state[1] < 0 or new_state[0] >= len(matrix) or new_state[1] >= len(matrix):
        reward = -1000
        end_game = True
        return reward, new_state, end_game
    else:
        reward = matrix[new_state[0]][new_state[1]]
    if matrix[new_state[0]][new_state[1]] == 10:
        end_game = True
    return reward, new_state, end_game


def train(game_table, table):
    for _ in range(500):
        end_of_game = False
        current_state = random.choice(possible_states(game_table))
        next_state = current_state
        reward = 0
        while not end_of_game:
            current_state = next_state
            valid = get_valid_actions(current_state, table)
            max_reward_actions = max_value_actions(current_state, table)
            max_reward_action = random.choice(max_reward_actions)
            if random.random() < EPSILON:
                max_reward_action = random.choice(valid)
            reward, next_state, end_of_game = take_action(game_table, current_state, max_reward_action)
            if end_of_game:
                table[current_state][max_reward_action] = reward
            else:
                optimal_future_value = table[next_state][random.choice(max_value_actions(next_state, table))]
                discounted_optimal_future_value = GAMMA * optimal_future_value
                learned_value = reward + discounted_optimal_future_value
                table[current_state][max_reward_action] = (1 - LEARNING_RATE) * table[current_state][
                    max_reward_action] + LEARNING_RATE * learned_value


def test(game_table, table):
    end_game = False
    path = list()
    current_state = (0, 0)
    next_state = current_state
    while not end_game:
        current_state = next_state
        valid = get_valid_actions(current_state, table)
        max_reward_actions = max_value_actions(current_state, table)
        max_reward_action = random.choice(max_reward_actions)
        reward, next_state, end_game = take_action(game_table, current_state, max_reward_action)
        print(next_state)
        path.append(next_state)


def create_matrix_table_and_train(lines, columns, endpoints, obstacles):
    matrix = create_matrix(lines, columns, endpoints, obstacles)
    table = create_qtable(matrix, obstacles, endpoints)
    train(matrix, table)
    test(matrix, table)


create_matrix_table_and_train(4, 4, [(3, 3)], [(1, 2), (1, 1), (1, 0)])
