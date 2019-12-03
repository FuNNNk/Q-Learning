import random
import pandas as pd

possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
LEARNING_RATE = 1
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


def get_max_key(state, Qtable):
    pass


game_table = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
obstacles = [(1, 1)]
endpoints = [(2, 2)]
table = create_qtable(game_table, obstacles, endpoints)

for _ in range(EPISODES):
    end_of_game = False
    while not end_of_game:
        current_state = game_table[0][0]
        valid = get_valid_actions(current_state, table)
        max_reward_action = max(valid)

        if random.random() < EPSILON:
            max_reward_action = random.random(valid)
        reward = table[max_reward_action]

        if end_of_game:
            table[max_reward_action, current_state] = reward

        else:
            optimal_future_value = max(valid)
            discounted_optimal_future_value = GAMMA * optimal_future_value
            learned_value = reward + discounted_optimal_future_value
            table[max_reward_action, current_state] = (1 - LEARNING_RATE) * table[current_state][
                max_reward_action] + LEARNING_RATE * learned_value
