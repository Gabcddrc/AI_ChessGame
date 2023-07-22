from chess_engine.movements import make_move, make_move_ai
from chess_engine.game import initialize_game, print_board
from chess_engine.chess_pieces import Side
from llm_interface.gpt import prompt

if __name__ == '__main__':
    board = initialize_game()
    board_str = print_board(board)

    print("Which side you want to play?  White or Black")
    user_side_str = input()
    while user_side_str != "White" and user_side_str != "Black":
        print("Invalid input. Pick White or Black")
        user_side_str = input()

    ai_side = Side.WHITE
    ai_side_str = "White"
    user_side = Side.BLACK

    if user_side_str == "White":
        ai_side = Side.BLACK
        user_side = Side.WHITE
        end = not make_move(user_side, board)
        board_str = print_board(board)


    while True:
        end = not make_move_ai(ai_side, board, board_str, prompt)
        board_str = print_board(board)
        if end:
            print(f"Check Mate! {ai_side_str} Wins")
            break

        end = not make_move(user_side, board)
        board_str = print_board(board)
        if end:
            print(f"Check Mate! {user_side_str} Wins")
            break
