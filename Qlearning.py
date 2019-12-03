import random

possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
LEARNING_RATE = 0.2
GAMMA = 0
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
                    Qtable[(i, j)][action] = 1000
                else:
                    Qtable[(i, j)][action] = -0.04
    return Qtable


def get_valid_actions(state, Qtable):
    valid_actions = list(filter(lambda x: Qtable[state][x] is not None, Qtable[state].keys()))
    return valid_actions


def get_max_key(state, Qtable):
    pass


game_table = [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
obstacles = []
endpoints = [(2, 2)]
table = create_qtable(game_table, obstacles, endpoints)



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
        return reward, state, end_game
    else:
        reward = table[state][action]
    if matrix[new_state[0]][new_state[1]] == 1000:
        end_game = True
    return reward, new_state, end_game


all_states = possible_states(game_table)


def train():
    for _ in range(EPISODES):
        end_of_game = False
        current_state = random.choice(all_states)
        reward = 0
        while not end_of_game:
            valid = get_valid_actions(current_state, table)
            max_reward_actions = max_value_actions(current_state, table)
            max_reward_action = tuple()
            max_reward_action = random.choice(max_reward_actions)
            if random.random() < EPSILON:
                max_reward_action = random.choice(valid)
            reward, current_state, end_of_game = take_action(game_table, current_state, max_reward_action)
            if end_of_game:
                table[current_state][max_reward_action] = reward
            else:
                optimal_future_value = 0
                discounted_optimal_future_value = GAMMA * optimal_future_value
                learned_value = reward + discounted_optimal_future_value
                table[current_state][max_reward_action] = (1 - LEARNING_RATE) * table[current_state][max_reward_action] + LEARNING_RATE * learned_value


train()
print(table)