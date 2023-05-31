from enum import Enum


class Side(Enum):
    WHITE = 0
    BLACK = 1
    NEUTRAL = 2


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ChessPiece:
    def __init__(self, side: Side, pos: Pos):
        self.side = side
        self.pos = pos

    def string_representation(self):
        return "0"

    def validate_continuous_move(self, move, board, new_positions):
        for i in range(1, 8):
            new_pos = Pos(self.pos.x + move[0] * i, self.pos.y + move[1] * i)
            if self.validate_next_pos(new_pos, board):
                new_positions.append(new_pos)
            else:
                break
            if board[new_pos.x][new_pos.y].side != Side.NEUTRAL:
                break

    def validate_move(self, move, board, new_positions):
        new_pos = Pos(self.pos.x + move[0], self.pos.y + move[1])
        if self.validate_next_pos(new_pos, board):
            new_positions.append(new_pos)

    def validate_next_pos(self, pos: Pos, board: list):
        return (
            pos.x > -1
            and pos.x < 8
            and pos.y > -1
            and pos.y < 8
            and board[pos.x][pos.y].side != self.side
        )


class King(ChessPiece):
    def get_new_possible_pos(self, board):
        new_pos = []

        self.validate_move([0, 1], board, new_pos)
        self.validate_move([0, -1], board, new_pos)
        self.validate_move([1, 0], board, new_pos)
        self.validate_move([-1, 0], board, new_pos)
        self.validate_move([1, 1], board, new_pos)
        self.validate_move([-1, -1], board, new_pos)
        self.validate_move([+1, -1], board, new_pos)
        self.validate_move([-1, +1], board, new_pos)

        return new_pos

    def string_representation(self):
        return "K"


class Queen(ChessPiece):
    def get_new_possible_pos(self, board):
        new_pos = []

        self.validate_continuous_move([0, 1], board, new_pos)
        self.validate_continuous_move([0, -1], board, new_pos)
        self.validate_continuous_move([1, 0], board, new_pos)
        self.validate_continuous_move([-1, 0], board, new_pos)
        self.validate_continuous_move([1, 1], board, new_pos)
        self.validate_continuous_move([-1, -1], board, new_pos)
        self.validate_continuous_move([+1, -1], board, new_pos)
        self.validate_continuous_move([-1, +1], board, new_pos)

        return new_pos

    def string_representation(self):
        return "Q"


class Rook(ChessPiece):
    def get_new_posssible_pos(self, board):
        new_pos = []

        self.validate_continuous_move([0, 1], board, new_pos)
        self.validate_continuous_move([0, -1], board, new_pos)

        return new_pos

    def string_representation(self):
        return "R"


class Bishop(ChessPiece):
    def get_new_possible_pos(self, board):
        new_pos = []

        self.validate_continuous_move([1, 1], board, new_pos)
        self.validate_continuous_move([-1, -1], board, new_pos)
        self.validate_continuous_move([+1, -1], board, new_pos)
        self.validate_continuous_move([-1, +1], board, new_pos)

        return new_pos

    def string_representation(self):
        return "R"


class Knight(ChessPiece):
    def get_new_possible_pos(self, board):
        new_pos = []

        self.validate_move([2, 1], board, new_pos)
        self.validate_move([2, -1], board, new_pos)
        self.validate_move([-2, 1], board, new_pos)
        self.validate_move([-2, -1], board, new_pos)
        self.validate_move([1, 2], board, new_pos)
        self.validate_move([-1, 2], board, new_pos)
        self.validate_move([1, -2], board, new_pos)
        self.validate_move([-1, -2], board, new_pos)

        return new_pos


def initialize_game():
    board = [[ChessPiece(Side.NEUTRAL, None)
              for _ in range(8)] for _ in range(8)]
    board[0][0] = Queen(Side.WHITE, Pos(0, 0))
    board[0][1] = King(Side.BLACK, Pos(0, 1))
    print([(pos.x, pos.y) for pos in board[0][0].get_new_possible_pos(board)])
    print_board(board)


def print_board(board):
    print("\n".join(
        ["|".join([piece.string_representation() for piece in row])
            for row in board]))

# TODO: Enpeseant, castling


initialize_game()
