from chess_engine.chess_pieces import ChessPiece, Side, Pos, Pawn, Rook, Knight, Bishop, \
                         Queen, King, Move


def initialize_game():
    board = [[ChessPiece(Side.NEUTRAL, Pos(i ,j))
              for j in range(8)] for i in range(8)]

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

def get_avaliable_moves(side: Side, board):
    moves = []

    for i in range(8):
        for j in range(8):
            if board[i][j].side == side:
                new_moves = board[i][j].get_new_possible_pos(board)
                for move in new_moves:
                    moves.append([board[i][j].string_representation(),
                                  board[i][j].pos,
                                  move])
    return moves

def print_board(board):
    print(("\n".join(
        [str(8-id)+" " + " | ".join([piece.string_representation_colour() for piece in row])
            for id, row in enumerate(reversed(board))]) + '\n  a   b   c   d   e   f   g   h'))

def print_moves(moves):
    n = len(moves)
    for i in range(n):
        p, curr, next = moves[i]
        print(f'{i} : {curr.string_representation()} -> {next.string_representation()}', end = "    ")

def handle_pawn(curr, to, board):
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

    if isinstance(board[to.x][to.y] , Pawn):
        handle_pawn(curr, to, board)

    print(f'{curr.string_representation()} -> {to.string_representation()}')

def make_move(side, board):
    moves = get_avaliable_moves(side, board)
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
            break
        count += 1
        print_moves(moves)

    print_board(board)
