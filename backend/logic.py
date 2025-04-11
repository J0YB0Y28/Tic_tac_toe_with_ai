import random
import time
import math

ROWS = 6
COLS = 7

class ConnectFour:
    def __init__(self, mode='pvp', player1='Player 1', player2='Player 2', difficulty='hard'):
        self.board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        self.mode = mode
        self.difficulty = difficulty
        self.p1_name = player1
        self.p2_name = player2 if mode == 'pvp' else 'Computer'
        self.current_player = self.p1_name
        self.symbols = {self.p1_name: 'X', self.p2_name: 'O'}
        self.winner = None
        self.game_over = False
        self.winning_cells = []
        self.move_times = {self.p1_name: [], self.p2_name: []}
        self.last_move_time = time.time()

    def get_state(self):
        return {
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner,
            'game_over': self.game_over,
            'move_times': self.get_total_times(),
            'symbols': self.symbols,
            'winning_cells': self.winning_cells
        }

    def make_move(self, col):
        if self.game_over:
            return 'Game already over'

        if not isinstance(col, int) or not (0 <= col < COLS):
            return 'Invalid column'

        row = self.get_available_row(col)
        if row is None:
            return 'Column full'

        symbol = self.symbols[self.current_player]
        self.board[row][col] = symbol

        now = time.time()
        self.move_times[self.current_player].append(now - self.last_move_time)
        self.last_move_time = now

        if self.check_win(row, col, symbol):
            self.winner = self.current_player
            self.game_over = True
        elif self.is_full():
            self.game_over = True
        else:
            self.switch_player()

        return 'Move accepted'

    def check_win(self, row, col, symbol):
        self.winning_cells = self.get_winning_cells(row, col, symbol)
        return bool(self.winning_cells)

    def get_winning_cells(self, row, col, symbol):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            cells = [(row, col)]
            for dir in [1, -1]:
                r, c = row, col
                for _ in range(3):
                    r += dy * dir
                    c += dx * dir
                    if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == symbol:
                        cells.append((r, c))
                    else:
                        break
            if len(cells) >= 4:
                return cells
        return []

    def ai_move(self):
        if self.current_player != self.p2_name:
            return 'Not AI turn'

        if self.difficulty == 'easy':
            available_cols = [c for c in range(COLS) if self.get_available_row(c) is not None]
            return self.make_move(random.choice(available_cols)) if available_cols else 'No valid moves'

        elif self.difficulty == 'medium':
            ai_symbol = self.symbols[self.p2_name]
            player_symbol = self.symbols[self.p1_name]
            for col in range(COLS):
                row = self.get_available_row(col)
                if row is not None:
                    copy = [r.copy() for r in self.board]
                    copy[row][col] = ai_symbol
                    if self.check_win_on_board(copy, row, col, ai_symbol):
                        return self.make_move(col)
            for col in range(COLS):
                row = self.get_available_row(col)
                if row is not None:
                    copy = [r.copy() for r in self.board]
                    copy[row][col] = player_symbol
                    if self.check_win_on_board(copy, row, col, player_symbol):
                        return self.make_move(col)
            center = COLS // 2
            if self.get_available_row(center) is not None:
                return self.make_move(center)
            available_cols = [c for c in range(COLS) if self.get_available_row(c) is not None]
            return self.make_move(random.choice(available_cols)) if available_cols else 'No valid moves'

        else:
            _, best_col = self.minimax(self.board, 4, -math.inf, math.inf, True)
            if best_col is not None and self.get_available_row(best_col) is not None:
                return self.make_move(best_col)
            available_cols = [c for c in range(COLS) if self.get_available_row(c) is not None]
            return self.make_move(random.choice(available_cols)) if available_cols else 'No valid moves'

    def get_available_row(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == ' ':
                return row
        return None

    def get_valid_locations(self, board):
        return [c for c in range(COLS) if board[0][c] == ' ']

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def score_position(self, board, piece):
        score = 0
        center_array = [board[i][COLS // 2] for i in range(ROWS)]
        score += center_array.count(piece) * 3

        for row in range(ROWS):
            row_array = board[row]
            for col in range(COLS - 3):
                window = row_array[col:col + 4]
                score += self.evaluate_window(window, piece)

        for col in range(COLS):
            col_array = [board[row][col] for row in range(ROWS)]
            for row in range(ROWS - 3):
                window = col_array[row:row + 4]
                score += self.evaluate_window(window, piece)

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for row in range(3, ROWS):
            for col in range(COLS - 3):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.symbols[self.p1_name] if piece == self.symbols[self.p2_name] else self.symbols[self.p2_name]

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(' ') == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(' ') == 1:
            score -= 4

        return score

    def is_terminal_node(self, board):
        return self.check_winner_on_board(board, self.symbols[self.p1_name]) or \
               self.check_winner_on_board(board, self.symbols[self.p2_name]) or \
               len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        ai_piece = self.symbols[self.p2_name]
        player_piece = self.symbols[self.p1_name]

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner_on_board(board, ai_piece):
                    return (1000000, None)
                elif self.check_winner_on_board(board, player_piece):
                    return (-1000000, None)
                else:
                    return (0, None)
            else:
                return (self.score_position(board, ai_piece), None)

        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row_for_board(board, col)
                if row is not None:
                    temp_board = [r.copy() for r in board]
                    self.drop_piece(temp_board, row, col, ai_piece)
                    new_score, _ = self.minimax(temp_board, depth - 1, alpha, beta, False)
                    if new_score > value:
                        value = new_score
                        best_col = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value, best_col

        else:
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_available_row_for_board(board, col)
                if row is not None:
                    temp_board = [r.copy() for r in board]
                    self.drop_piece(temp_board, row, col, player_piece)
                    new_score, _ = self.minimax(temp_board, depth - 1, alpha, beta, True)
                    if new_score < value:
                        value = new_score
                        best_col = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value, best_col

    def get_available_row_for_board(self, board, col):
        for row in reversed(range(ROWS)):
            if board[row][col] == ' ':
                return row
        return None

    def switch_player(self):
        self.current_player = self.p2_name if self.current_player == self.p1_name else self.p1_name

    def is_full(self):
        return all(self.board[0][c] != ' ' for c in range(COLS))

    def get_total_times(self):
        return {
            self.p1_name: round(sum(self.move_times[self.p1_name]), 2),
            self.p2_name: round(sum(self.move_times[self.p2_name]), 2)
        }

    def check_win(self, row, col, symbol):
        return self.check_win_on_board(self.board, row, col, symbol)

    def check_win_on_board(self, board, row, col, symbol):
        def count(dx, dy):
            r, c = row + dy, col + dx
            count = 0
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                count += 1
                r += dy
                c += dx
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if 1 + count(dx, dy) + count(-dx, -dy) >= 4:
                return True
        return False

    def check_winner_on_board(self, board, symbol):
        for col in range(COLS):
            row = self.get_available_row_for_board(board, col)
            if row is not None and self.check_win_on_board(board, row, col, symbol):
                return True
        return False
