import random
import time


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action


class MaxNAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        self.num_players = state.get_player_count()
        self.my_index = state.get_on_move_chr().get_index()
        self.max_depth = max_depth

        best_score = -float('inf')
        best_action = None

        for action in state.get_legal_actions():
            next_state = state.generate_successor_state(action)
            next_player = next_state.get_on_move_chr()
            score_list = self.max_n(next_state, self.max_depth - 1, next_player)
            if score_list[self.my_index] > best_score or best_action is None:
                best_score = score_list[self.my_index]
                best_action = action

        return best_action

    def max_n(self, state, depth, current_player):
        if depth == 0 or state.is_terminal():
            return state.get_score_list()

        best_score_list = [-float('inf')] * self.num_players
        for action in state.get_legal_actions():
            next_state = state.generate_successor_state(action)
            next_player = next_state.get_on_move_chr()
            child_score_list = self.max_n(next_state, depth - 1, next_player)

            i = current_player.get_index()
            if child_score_list[i] > best_score_list[i]:
                best_score_list = child_score_list

        return best_score_list


class MiniMaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        self.player = state.get_on_move_chr()
        self.max_depth = max_depth

        best_score = float('-inf')
        best_action = None
        for action in state.get_legal_actions():
            next_state = state.generate_successor_state(action)
            eval_score = self.minimax(next_state, self.max_depth - 1, False)
            if eval_score > best_score or best_action is None:
                best_score = eval_score
                best_action = action

        return best_action

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.is_terminal():
            return state.get_score(self.player)

        if maximizing_player:
            max_eval = float('-inf')
            for action in state.get_legal_actions():
                eval_score = self.minimax(state.generate_successor_state(action), depth - 1, False)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for action in state.get_legal_actions():
                eval_score = self.minimax(state.generate_successor_state(action), depth - 1, True)
                min_eval = min(min_eval, eval_score)
            return min_eval


class MinimaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        self.player = state.get_on_move_chr()
        self.max_depth = max_depth

        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')

        for action in state.get_legal_actions():
            next_state = state.generate_successor_state(action)
            eval_score = self.minimax_alpha_beta(next_state, self.max_depth - 1, False, alpha, beta)
            if eval_score > best_score or best_action is None:
                best_score = eval_score
                best_action = action
            alpha = max(alpha, eval_score)

        return best_action

    def minimax_alpha_beta(self, state, depth, maximizing_player, alpha, beta):
        if depth == 0 or state.is_terminal():
            return state.get_score(self.player)

        if maximizing_player:
            max_eval = float('-inf')
            for action in state.get_legal_actions():
                eval_score = self.minimax_alpha_beta(state.generate_successor_state(action), depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if alpha >= beta:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in state.get_legal_actions():
                eval_score = self.minimax_alpha_beta(state.generate_successor_state(action), depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if alpha >= beta:
                    break
            return min_eval
