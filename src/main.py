from chess_engine.game import *

if __name__ == '__main__':
    board = initialize_game()
    print_board(board)

    while True:
        make_move(Side.WHITE, board)
        make_move(Side.BLACK, board)
