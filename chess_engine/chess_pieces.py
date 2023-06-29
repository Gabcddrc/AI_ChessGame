from enum import Enum


class Side(Enum):
    WHITE = 0
    BLACK = 1
    NEUTRAL = 2

class Move(Enum):
    NORMAL = 0
    ENPASSANT = 1


class Pos:
    def __init__(self, x, y, move = Move.NORMAL):
        self.x = x
        self.y = y
        self.move = move
    def string_representation(self):
        return f'{chr(self.y+97)}{self.x+1}'

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
    def get_new_possible_pos(self, board):
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
        return "B"


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

    def string_representation(self):
        return "N"


class Pawn(ChessPiece):
    def __init__(self, side: Side, pos: Pos):
        super().__init__(side, pos)
        self.moved = False
        self.en_passant_possible = False
        self.multiplier = 1 if self.side == Side.WHITE else -1

    def get_new_possible_pos(self, board):
        new_pos = []

        if self.validate_move_pawn([self.multiplier*1, 0], board, new_pos) \
                and not self.moved:
            self.validate_move_pawn([self.multiplier*2, 0], board, new_pos)
        else:
            self.first_move = False

        self.validate_capture([self.multiplier*1, 1], board, new_pos)
        self.validate_capture([self.multiplier*1, -1], board, new_pos)
        self.en_passant(board, new_pos)
        return new_pos

    def validate_move_pawn(self, move, board, new_positions):
        new_pos = Pos(self.pos.x + move[0], self.pos.y + move[1])

        if self.validate_next_pos(new_pos, board) \
                and board[new_pos.x][new_pos.y].side == Side.NEUTRAL:
            new_positions.append(new_pos)
            return True
        return False

    def validate_capture(self, move, board, new_positions):
        new_pos = Pos(self.pos.x + move[0], self.pos.y + move[1])
        if self.validate_next_pos(new_pos, board) \
                and board[new_pos.x][new_pos.y].side != self.side \
                and board[new_pos.x][new_pos.y].side != Side.NEUTRAL:
            new_positions.append(new_pos)

    def en_passant(self, board, new_positions):
        left, right = False, False
        if self.pos.y > 0 \
                and isinstance(board[self.pos.x][self.pos.y-1], Pawn) \
                and board[self.pos.x][self.pos.y-1].en_passant_possible \
                and self.validate_next_pos(
                    Pos(self.pos.x +self.multiplier*1, self.pos.y-1), board) \
                and board[self.pos.x +self.multiplier*1][self.pos.y-1].side \
                == Side.NEUTRAL:
            new_positions.append(Pos(self.pos.x +self.multiplier*1, self.pos.y-1, Move.ENPASSANT))

        if self.pos.y < 7 \
                and isinstance(board[self.pos.x][self.pos.y+1], Pawn) \
                and board[self.pos.x][self.pos.y+1].en_passant_possible \
                and self.validate_next_pos(
                    Pos(self.pos.x+self.multiplier*1, self.pos.y + 1), board) \
                and board[self.pos.x+self.multiplier*1][self.pos.y + 1].side \
                == Side.NEUTRAL:
            new_positions.append(Pos(self.pos.x+self.multiplier*1, self.pos.y + 1, Move.ENPASSANT))


    def string_representation(self):
        return "P"


# TODO:  castling
