import copy
from shutil import move
from chess_engine.chess_pieces import Bishop, ChessPiece, Queen, Rook, Knight, Side, Move, Pos

def get_all_moves(side: Side, board : list[list]):
    moves = []

    for i in range(8):
        for j in range(8):
            if board[i][j].side == side:
                new_poses = board[i][j].get_new_possible_pos(board)
                for new_pos in new_poses:
                    move = [board[i][j].string_representation(),
                            board[i][j].pos,
                            new_pos]
                    moves.append(move)

    return moves

def get_valid_moves(side: Side, board: list[list]):
    moves = []

    for move in get_all_moves(side, board):
        if not move_cause_check(move, side, board):
            moves.append(move)

    return moves

def print_moves(moves) -> str:
    n = len(moves)
    moves_string = ""
    for i in range(n):
        p, curr, next = moves[i]
        moves_string += f'{i} : {curr.string_representation()} -> {next.string_representation()}    '
    print(moves_string)
    return moves_string

def handle_en_passant(curr, to, board):
    if to.move == Move.ENPASSANT:
        board[curr.x][to.y] =\
            ChessPiece(Side.NEUTRAL, Pos(curr.x, to.y))

    if abs(to.x - curr.x) == 2:
        board[to.x][to.y].en_passant_possible = True
    else:
        board[to.x][to.y].en_passant_possible = False

def handle_promotion(to : Pos, board: list[list]):
    print("Please indicate the piece you want to promote to")
    piece = input()
    side = board[to.x][to.y].side

    match piece:
        case "Q":
            board[to.x][to.y] = Queen(side, to)
        case "R":
            board[to.x][to.y] = Rook(side, to)
        case "B":
            board[to.x][to.y] = Bishop(side, to)
        case "N":
            board[to.x][to.y] = Knight(side, to)
        case other:
            print(f'Invalid Piece: {other}')
            handle_promotion(to, board)


def perform_move(move, board):
    _, curr, to = move
    board[curr.x][curr.y].pos = to
    board[curr.x][curr.y], board[to.x][to.y] =\
        ChessPiece(Side.NEUTRAL, Pos(curr.x, curr.y)), board[curr.x][curr.y]

    if board[to.x][to.y].string_representation == "P":
        handle_en_passant(curr, to, board)
        if board[to.x][to.y].side == Side.WHITE:
            if to.x == 7:
                handle_promotion(to, board)
        else:
            if to.x == 0:
                handle_promotion(to, board)


    if to.move == Move.CASTLING:
        perform_castling(to, board)

    board[to.x][to.y].moved = True

def print_move(move : list):
    print(f'{move[1].string_representation()} -> {move[2].string_representation()}')

def perform_castling(to, board):
    if to.y == 2:
        board[to.x][0], board[to.x][3] = board[to.x][3], board[to.x][0]
        board[to.x][3].pos = Pos(to.x, 3)
        board[to.x][0].pos = Pos(to.x, 0)
        board[to.x][3].moved = True
    if to.y == 6:
        board[to.x][7], board[to.x][5] = board[to.x][5], board[to.x][7]
        board[to.x][5].pos = Pos(to.x, 5)
        board[to.x][7].pos = Pos(to.x, 7)
        board[to.x][5].moved = True

def move_cause_check(move, side, board):
    board_copy = copy.deepcopy(board)
    opposite_side = Side.WHITE if side == Side.BLACK else Side.BLACK
    perform_move(move, board_copy)

    moves = get_all_moves(opposite_side, board_copy)
    for _, _, next in moves:
        if board_copy[next.x][next.y].string_representation() == "K":
            return True

    return False

def make_move(side, board):
    moves = get_valid_moves(side, board)

    if len(moves) == 0:
        return False

    print_moves(moves)
    side_str = "White Side" if side == Side.WHITE else "Black Side"

    move_index = "not selected"
    while True:
        print(f"\n ({side_str}) Pick your move:")

        move_index = input()
        if move_index.isdigit() and int(move_index) < len(moves):
            perform_move(moves[int(move_index)], board)
            break

        print(f'\n invalid input: {move_index}')

    return True

def make_move_ai(side : Side, board : list[list], board_str:str, messages : list, prompt) -> bool:
    moves = get_valid_moves(side, board)
    if len(moves) == 0:
        return False

    moves_str = board_str + "\n" +print_moves(moves)
    side_str = "White" if side == Side.WHITE else "Black"

    print(f"\n ChatGPT as ({side_str}) making move")
    move_index = prompt(messages, moves_str, side_str)
    perform_move(moves[int(move_index)], board)

    return True
