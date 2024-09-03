from src.chess_engine.chess_pieces import ChessPiece, Side


class colour:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    BLACK = "\033[30m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def render_board(board: list[list[ChessPiece]]) -> str:
    board_str = "\n" + (
        "\n".join(
            [
                str(8 - id) + " " + " | ".join([render_piece(piece) for piece in row])
                for id, row in enumerate(reversed(board))
            ]
        )
        + "\n  A   B   C   D   E   F   G   H"
    )
    return board_str


def render_piece(piece: ChessPiece) -> str:
    piece_colour = (
        colour.CYAN
        if piece.side == Side.WHITE
        else colour.PURPLE
        if piece.side == Side.BLACK
        else colour.WHITE
    )
    return f"{piece_colour}{piece.string_representation()}{colour.END}"
