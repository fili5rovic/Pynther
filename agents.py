import random
import math
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


class MinimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        if state.get_num_of_players() != 2:
            raise ValueError("MinimaxAgent supports exactly 2 players")

        max_player_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != max_player_char][0]

        def is_terminal(node, depth_left):
            return node.is_goal_state() or depth_left == 0

        def evaluate(node):
            return node.get_score(max_player_char) - node.get_score(opponent_char)

        def minimax(node, maximizing_player, depth_left):
            if is_terminal(node, depth_left):
                return evaluate(node)

            if maximizing_player:
                best = -math.inf
                for move in node.get_legal_actions():
                    succ = node.generate_successor_state(move)
                    val = minimax(succ, False, depth_left - 1)
                    if val > best:
                        best = val
                return best
            else:
                best = math.inf
                for move in node.get_legal_actions():
                    succ = node.generate_successor_state(move)
                    val = minimax(succ, True, depth_left - 1)
                    if val < best:
                        best = val
                return best

        best_move = None
        best_value = -math.inf
        for move in state.get_legal_actions():
            succ = state.generate_successor_state(move)
            val = minimax(succ, False, max_depth - 1)
            if val > best_value:
                best_value = val
                best_move = move

        return best_move


class MinimaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        if state.get_num_of_players() != 2:
            raise ValueError("MinimaxABAgent supports exactly 2 players")

        agent_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != agent_char][0]

        def is_terminal(node, depth_left):
            return node.is_goal_state() or depth_left == 0

        def evaluate(node):
            return node.get_score(agent_char) - node.get_score(opponent_char)

        def alphabeta(node, maximizing_player, depth_left, alpha, beta):
            if is_terminal(node, depth_left):
                return evaluate(node)

            if maximizing_player:
                value = -math.inf
                for move in node.get_legal_actions():
                    succ = node.generate_successor_state(move)
                    value = max(value, alphabeta(succ, False, depth_left - 1, alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value
            else:
                value = math.inf
                for move in node.get_legal_actions():
                    succ = node.generate_successor_state(move)
                    value = min(value, alphabeta(succ, True, depth_left - 1, alpha, beta))
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
                return value

        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in state.get_legal_actions():
            succ = state.generate_successor_state(move)
            val = alphabeta(succ, False, max_depth - 1, alpha, beta)
            if val > best_value:
                best_value = val
                best_move = move
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

        return best_move


class MaxNAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        num_players = state.get_num_of_players()

        def evaluate_as_tuple(s):
            vals = []
            for i in range(num_players):
                ch = chr(ord('A') + i)
                vals.append(s.get_score(ch))
            return tuple(vals)

        def maxn(node, depth_left):
            if node.is_goal_state() or depth_left == 0:
                return evaluate_as_tuple(node), None

            current_player_ord = node.get_on_move_ord()
            best_vector = None
            best_move = None

            for move in node.get_legal_actions():
                succ = node.generate_successor_state(move)
                vec, _ = maxn(succ, depth_left - 1)
                if best_vector is None or vec[current_player_ord] > best_vector[current_player_ord]:
                    best_vector = vec
                    best_move = move

            return best_vector, best_move

        _, best_move = maxn(state, max_depth)
        return best_move


class NegamaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        if state.get_num_of_players() != 2:
            raise ValueError("NegamaxAgent supports exactly 2 players")

        agent_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != agent_char][0]

        def is_terminal(node, depth_left):
            return node.is_goal_state() or depth_left == 0

        def evaluate(node):
            return node.get_score(agent_char) - node.get_score(opponent_char)

        def negamax(node, depth_left, color):
            if is_terminal(node, depth_left):
                return color * evaluate(node)

            best_value = -math.inf
            for move in node.get_legal_actions():
                succ = node.generate_successor_state(move)
                val = -negamax(succ, depth_left - 1, -color)
                if val > best_value:
                    best_value = val
            return best_value

        best_move = None
        best_value = -math.inf
        for move in state.get_legal_actions():
            succ = state.generate_successor_state(move)
            val = -negamax(succ, max_depth - 1, -1)
            if val > best_value:
                best_value = val
                best_move = move

        return best_move


class NegamaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        if state.get_num_of_players() != 2:
            raise ValueError("NegamaxABAgent supports exactly 2 players")

        agent_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != agent_char][0]

        def is_terminal(node, depth_left):
            return node.is_goal_state() or depth_left == 0

        def evaluate(node):
            return node.get_score(agent_char) - node.get_score(opponent_char)

        def negamax(node, depth_left, alpha, beta, color):
            if is_terminal(node, depth_left):
                return color * evaluate(node)

            best_value = -math.inf
            for move in node.get_legal_actions():
                succ = node.generate_successor_state(move)
                val = -negamax(succ, depth_left - 1, -beta, -alpha, -color)
                if val > best_value:
                    best_value = val
                alpha = max(alpha, val)
                if alpha >= beta:
                    break  # cutoff
            return best_value

        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in state.get_legal_actions():
            succ = state.generate_successor_state(move)
            val = -negamax(succ, max_depth - 1, -beta, -alpha, -1)
            if val > best_value:
                best_value = val
                best_move = move
            alpha = max(alpha, best_value)

        return best_move


class ExpectimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        if state.get_num_of_players() != 2:
            raise ValueError("ExpectimaxAgent supports exactly 2 players")

        agent_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != agent_char][0]

        def is_terminal(node, depth_left):
            return node.is_goal_state() or depth_left == 0

        def evaluate(node):
            return node.get_score(agent_char) - node.get_score(opponent_char)

        def expectimax(node, depth_left, maximizing_player):
            if is_terminal(node, depth_left):
                return evaluate(node)

            actions = node.get_legal_actions()
            if maximizing_player:
                best = -math.inf
                for move in actions:
                    succ = node.generate_successor_state(move)
                    val = expectimax(succ, depth_left - 1, False)
                    if val > best:
                        best = val
                return best
            else:
                total = 0
                for move in actions:
                    succ = node.generate_successor_state(move)
                    total += expectimax(succ, depth_left - 1, True)
                return total / len(actions) if actions else 0

        best_move = None
        best_value = -math.inf
        for move in state.get_legal_actions():
            succ = state.generate_successor_state(move)
            val = expectimax(succ, max_depth - 1, False)
            if val > best_value:
                best_value = val
                best_move = move

        return best_move


class NegascoutAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        if state.get_num_of_players() != 2:
            raise ValueError("NegaScoutAgent supports exactly 2 players")

        agent_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != agent_char][0]

        def is_terminal(node, depth_left):
            return node.is_goal_state() or depth_left == 0

        def evaluate(node):
            return node.get_score(agent_char) - node.get_score(opponent_char)

        def negascout(node, depth_left, alpha, beta, color):
            if is_terminal(node, depth_left):
                return color * evaluate(node)

            b = beta
            best_value = -math.inf
            first_child = True
            for move in node.get_legal_actions():
                succ = node.generate_successor_state(move)
                if first_child:
                    val = -negascout(succ, depth_left - 1, -b, -alpha, -color)
                else:
                    val = -negascout(succ, depth_left - 1, -alpha - 1, -alpha, -color)
                    if val > alpha and val < beta:
                        val = -negascout(succ, depth_left - 1, -b, -alpha, -color)
                if val > best_value:
                    best_value = val
                if best_value > alpha:
                    alpha = best_value
                if alpha >= beta:
                    break
                b = alpha + 1
                first_child = False
            return best_value

        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in state.get_legal_actions():
            succ = state.generate_successor_state(move)
            val = -negascout(succ, max_depth - 1, -beta, -alpha, -1)
            if val > best_value:
                best_value = val
                best_move = move
            if best_value > alpha:
                alpha = best_value

        return best_move


class MinimaxID(Agent):
    def get_chosen_action(self, state, max_depth, time_limit=None):
        agent_char = state.get_on_move_chr()
        players = [chr(ord('A') + i) for i in range(state.get_num_of_players())]
        opponent_char = [p for p in players if p != agent_char][0]

        def is_terminal(node, depth):
            return node.is_goal_state() or depth == 0

        def evaluate(node):
            return node.get_score(agent_char) - node.get_score(opponent_char)

        def minimax(node, depth, maximizing_player):
            if is_terminal(node, depth):
                return evaluate(node)

            actions = node.get_legal_actions()
            if maximizing_player:
                best_val = -math.inf
                for move in actions:
                    succ = node.generate_successor_state(move)
                    val = minimax(succ, depth - 1, False)
                    best_val = max(best_val, val)
                return best_val
            else:
                best_val = math.inf
                for move in actions:
                    succ = node.generate_successor_state(move)
                    val = minimax(succ, depth - 1, True)
                    best_val = min(best_val, val)
                return best_val

        best_move = None
        start_time = time.time()

        for depth in range(1, max_depth + 1):
            if time_limit and (time.time() - start_time) >= time_limit:
                break

            current_best_move = None
            best_value = -math.inf
            for move in state.get_legal_actions():
                succ = state.generate_successor_state(move)
                val = minimax(succ, depth - 1, False)
                if val > best_value:
                    best_value = val
                    current_best_move = move

            best_move = current_best_move

        return best_move
