 Implementation Documentation

 1. Program Structure and Execution Flow

`Chess.py` is a single-file Python application built with Pygame for rendering, input handling, and the main game loop. It also uses Python's `pathlib` module to handle file paths across different operating systems.

 Startup

During initialization, the program:

- Initializes Pygame and creates an `1100 × 900` window.
- Sets the window caption and initializes the frame clock.
- Establishes base directories relative to the script's location using `BASE_DIR`.
- Loads the background, move marker, and chess piece images.

 State Setup

The game initializes its board and supporting state variables, including:

- `board` — the current arrangement of pieces.
- `LegalMoves` — the available destinations for the selected piece.
- `marker_rects` — rectangles used to represent move markers.
- `SelectedPiece` — the position of the currently selected piece.
- `turn` — the color of the player whose turn it is (`"W"` or `"B"`).

 Main Loop

The main loop runs at a target rate of 60 frames per second using `clock.tick(60)`.

During each iteration, the program processes window and mouse events, updates the game state when necessary, draws the board and pieces, and refreshes the display.

 2. Major Functions and Variables

 Global State Variables

| Variable | Purpose |
|---|---|
| `board` | An 8×8 list of lists representing the board. Each occupied square contains a piece identifier, while empty squares contain an empty string (`""`). |
| `turn` | Tracks the active player's turn using `"W"` for White and `"B"` for Black. |
| `SelectedPiece` | A tuple `(row, col)` identifying the selected piece's board position. |
| `LegalMoves` | A list of coordinate tuples `(row, col)` representing the destinations currently available to the selected piece. |
| `marker_rects` | Stores rectangles associated with move markers for rendering or interaction. |

 Utility Functions

`get_cell(row, col)`

Safely retrieves the contents of a board square. Returns `None` when the requested coordinates are outside the board's boundaries.

`get_color(row, col)`

Determines a piece's color from its identifier. Black pieces contain `"1"` in their names, while White pieces do not.

`is_enemy(color, cell)`

Determines whether a piece belongs to the opposing player based on the given color and the piece identifier.

 Movement and Validation Functions

`Legal_moves(board, row, col)`

Routes a selected piece to the appropriate movement calculator based on its type.

The individual movement functions include:

- `PawnLegalMoves`
- `KnightLegalMoves`
- `BishopLegalMoves`
- `Rooklegalmoves`
- `QueenLegalMoves`
- `kinglegalmoves`

These functions calculate movement destinations according to each piece's movement rules and the current board state.

`checkdetection(king_row, king_col, origin)`

Checks whether a given square is attacked by an opposing piece. Its detection logic examines sliding pieces, knights, and pawns, and includes adjacent enemy king detection.

The optional `origin` argument allows the function to account for the square a king is moving away from when evaluating a potential destination.

`MakeMove(SelectedPiece, col, row, LegalMoves)`

Updates the board when a selected piece makes a valid move. It moves the piece to its destination, clears its previous square, and returns a dictionary containing information about the moved and captured pieces.

 Rendering Functions

`generateBoard(x, y, board_coordinates)`

Draws the chessboard, including its squares and grid outlines. Returns a list of coordinate tuples representing board positions.

`place_pieces(...)`

Loads and displays the piece images at their corresponding board positions. It also returns a list of `pygame.Rect` objects associated with the rendered pieces for click detection.

 3. Board Representation and Piece Identification

 Board Matrix

The board is represented as an 8×8 list of lists. Each inner list corresponds to a row, and each element represents a square.

Squares contain either a piece identifier or an empty string:

- `""` — an empty square.
- `"rook"` — a White rook.
- `"pawn1"` — a Black pawn.

Board positions use zero-based indexing, with row and column values ranging from `0` to `7`.

 Piece Naming Convention

Piece colors are encoded directly into their string identifiers.

White pieces have no numeric suffix:

`rook`, `knight`, `bishop`, `queen`, `king`, `pawn`

Black pieces have a `"1"` suffix:

`rook1`, `knight1`, `bishop1`, `queen1`, `king1`, `pawn1`

This naming convention is used by the color-detection and enemy-detection functions to distinguish between the two sides.

 4. Movement, Validation, and Captures

 Sliding Pieces

Rooks, bishops, and queens calculate their movement by iterating through directional offsets.

Their movement logic checks successive squares along each direction until it reaches the board boundary or encounters an occupied square. Friendly pieces block movement, while opposing pieces may be included as capture destinations.

 Knights and Kings

Knights use predefined coordinate offsets to determine their possible destinations. Their movement is not blocked by intervening pieces.

Kings examine adjacent squares, excluding positions outside the board and squares occupied by friendly pieces. The king movement logic also calls `checkdetection()` to evaluate whether a destination is attacked.

 Pawns

Pawn movement logic accounts for forward movement, initial double-square advances, and diagonal captures. Movement direction depends on the pawn's color.

 Move Execution

When a player selects a highlighted destination, `MakeMove()` updates the board state. The previous square is cleared, the moved piece occupies its destination, and any captured piece is removed from the board.

The active move list is then reset, and control passes to the opposing player.

Note: The implementation of complete legal-move validation, including all situations in which a move could leave a king in check, remains a work in progress.

 5. Rendering, Input Handling, and Turns

 Rendering Flow

The game redraws its visual elements during each iteration of the main loop.

The rendering process includes:

1. Drawing the background image.
2. Drawing the board surface and grid using `generateBoard()`.
3. Displaying the pieces using `place_pieces()`.
4. Drawing move markers for the currently selected piece when available.
5. Updating the display.

Move markers use semi-transparent images to distinguish available destinations from ordinary board squares.

 Mouse Input

The program listens for `pygame.MOUSEBUTTONDOWN` events to process player interactions.

Mouse coordinates are translated into board positions using the board's screen offset and square dimensions. For example, the column is calculated using an expression of the form:

`(event.pos[0] - x) // 75`

The resulting board coordinates are used to determine which square the player clicked.

 Turn Enforcement

The game tracks the active player through the `turn` variable.

Piece selection is restricted to pieces belonging to the current player. The piece's color is compared with the active turn before the selection is accepted.

After a successful move, the turn changes from White to Black or from Black to White.

 6. Current Implementation Status

The project contains the core components of a graphical chess game, including board rendering, piece representation, turn tracking, movement calculators, move markers, and preliminary king-safety checks.

However, a complete implementation of chess rules requires additional validation and testing. Areas still being developed include comprehensive legal-move enforcement, checkmate and stalemate detection, and special moves such as castling and en passant.

