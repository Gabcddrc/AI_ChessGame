import copy
from chess_engine.chess_pieces import ChessPiece, Side, Move, Pos

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

def print_moves(moves):
    n = len(moves)
    for i in range(n):
        p, curr, next = moves[i]
        print(f'{i} : {curr.string_representation()} -> {next.string_representation()}', end = "    ")

def handle_en_passant(curr, to, board):
    if to.move == Move.ENPASSANT:
        board[curr.x][to.y] =\
            ChessPiece(Side.NEUTRAL, Pos(curr.x, to.y))

    if abs(to.x - curr.x) == 2:
        board[to.x][to.y].en_passant_possible = True
    else:
        board[to.x][to.y].en_passant_possible = False

def perform_move(move, board):
    _, curr, to = move
    board[curr.x][curr.y].pos = to
    board[curr.x][curr.y], board[to.x][to.y] =\
        ChessPiece(Side.NEUTRAL, Pos(curr.x, curr.y)), board[curr.x][curr.y]

    if board[to.x][to.y].string_representation == "P":
        handle_en_passant(curr, to, board)
        
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
    count  = 0
    side_str = "White Side" if side == Side.WHITE else "Black Side"

    move_index = "not selected"
    while True:
        if count > 0:
            print("\n invalid input, please select a move:")
        else:
            print(f"\n ({side_str}) Pick your move:")
        move_index = input()
        if move_index.isdigit():
            perform_move(moves[int(move_index)], board)
            print_moves(moves)
            break
        count += 1
    
    return True

