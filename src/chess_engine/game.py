from src.chess_engine.chess_pieces import (
    Bishop,
    ChessPiece,
    King,
    Knight,
    Pawn,
    Pos,
    Queen,
    Rook,
    Side,
)


def initialize_game():
    board = [[ChessPiece(Side.NEUTRAL, Pos(i, j)) for j in range(8)] for i in range(8)]

    for i in range(8):
        board[1][i] = Pawn(Side.WHITE, Pos(1, i))
        board[6][i] = Pawn(Side.BLACK, Pos(6, i))

    board[0][0] = Rook(Side.WHITE, Pos(0, 0))
    board[0][7] = Rook(Side.WHITE, Pos(0, 7))
    board[7][0] = Rook(Side.BLACK, Pos(7, 0))
    board[7][7] = Rook(Side.BLACK, Pos(7, 7))

    board[0][1] = Knight(Side.WHITE, Pos(0, 1))
    board[0][6] = Knight(Side.WHITE, Pos(0, 6))
    board[7][1] = Knight(Side.BLACK, Pos(7, 1))
    board[7][6] = Knight(Side.BLACK, Pos(7, 6))

    board[0][2] = Bishop(Side.WHITE, Pos(0, 2))
    board[0][5] = Bishop(Side.WHITE, Pos(0, 5))
    board[7][2] = Bishop(Side.BLACK, Pos(7, 2))
    board[7][5] = Bishop(Side.BLACK, Pos(7, 5))

    board[0][3] = Queen(Side.WHITE, Pos(0, 3))
    board[0][4] = King(Side.WHITE, Pos(0, 4))
    board[7][3] = Queen(Side.BLACK, Pos(7, 3))
    board[7][4] = King(Side.BLACK, Pos(7, 4))

    return board
