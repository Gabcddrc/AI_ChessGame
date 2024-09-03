from src.chess_engine.chess_pieces import Side
from src.chess_engine.game import initialize_game
from src.chess_engine.render import render_board
from src.chess_engine.movements import make_move

if __name__ == "__main__":
    board = initialize_game()
    print(render_board(board))

    while True:
        end = not make_move(Side.WHITE, board)
        print(render_board(board))

        if end:
            print("Check Mate! Black Wins")
            break

        end = not make_move(Side.BLACK, board)
        print(render_board(board))

        if end:
            print("Check Mate! White Wins")
            break
