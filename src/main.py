from chess_engine.movements import make_move
from chess_engine.game import initialize_game, print_board
from chess_engine.chess_pieces import Side

if __name__ == '__main__':
    board = initialize_game()
    print_board(board)

    while True:
        end = not make_move(Side.WHITE, board)
        print_board(board)
        if end:
            print("Check Mate! Black Wins")
            break
        
        end = not make_move(Side.BLACK, board)
        print_board(board)
        if end:
            print("Check Mate! White Wins")
            break