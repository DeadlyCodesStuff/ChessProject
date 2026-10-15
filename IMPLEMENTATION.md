 Implementation Documentation

 Program Structure and Execution Flow

`Chess.py` is structured as a Pygame-driven application, using Python's `pathlib` for file path handling and a modular framework for chess movement and rule validation.

1. **Initialization:** Initializes Pygame, creates an \(1100 \times 900\) window, resolves image directory paths, and preloads graphical assets into memory.
2. **State Setup:** Establishes global data structures, including the game board matrix (`board`), initial board configuration (`start_board`), active player (`turn`), legal moves (`LegalMoves`), and current game state (`state`).
3. **Main Event Loop:** Runs at 60 FPS using `clock.tick(60)`. Processes input events with boundary checks, handles piece movement, evaluates check and end-game conditions, and updates the display.

 Major Functions and Variables

 Global State Variables

- `board`: An \(8 \times 8\) list of lists containing piece identifier strings. Empty strings (`""`) represent unoccupied squares.
- `start_board`: A copy of the initial board configuration used to reset the game.
- `turn`: A string identifying the active player (`"W"` for White or `"B"` for Black).
- `state`: Tracks the current game state, such as `"neutral"`, `"checkmate"`, or `"stalemate"`.

 Key Functions

- `KingPOS(turn)`: Locates and returns the grid coordinates `(row, col)` of the specified player's king.
- `LeavesKingInCheck(turn, start, end)`: Temporarily simulates a move to determine whether it would leave the active player's king in check.
- `checkdetection(king_row, king_col, origin)`: Checks whether a king's position is under attack by examining sliding pieces, knights, and pawns.
- `WinCheck(turn)`: Evaluates the active player's available legal moves and determines whether the game has reached checkmate or stalemate.
- `Legal_moves(row, col)`: Routes the selected piece to its corresponding movement calculator and filters out moves that violate king safety.
- `MakeMove(...)`: Updates the board when a valid move is executed.
 Implementation Documentation

 Program Structure and Execution Flow

`Chess.py` is structured as a Pygame-driven application, using Python's `pathlib` for file path handling and a modular framework for chess movement and rule validation.

1. **Initialization:** Initializes Pygame, creates an \(1100 \times 900\) window, resolves image directory paths, and preloads graphical assets into memory.
2. **State Setup:** Establishes global data structures, including the game board matrix (`board`), initial board configuration (`start_board`), active player (`turn`), legal moves (`LegalMoves`), and current game state (`state`).
3. **Main Event Loop:** Runs at 60 FPS using `clock.tick(60)`. Processes input events with boundary checks, handles piece movement, evaluates check and end-game conditions, and updates the display.

 Major Functions and Variables

 Global State Variables

- `board`: An \(8 \times 8\) list of lists containing piece identifier strings. Empty strings (`""`) represent unoccupied squares.
- `start_board`: A copy of the initial board configuration used to reset the game.
- `turn`: A string identifying the active player (`"W"` for White or `"B"` for Black).
- `state`: Tracks the current game state, such as `"neutral"`, `"checkmate"`, or `"stalemate"`.

 Key Functions

- `KingPOS(turn)`: Locates and returns the grid coordinates `(row, col)` of the specified player's king.
- `LeavesKingInCheck(turn, start, end)`: Temporarily simulates a move to determine whether it would leave the active player's king in check.
- `checkdetection(king_row, king_col, origin)`: Checks whether a king's position is under attack by examining sliding pieces, knights, and pawns.
- `WinCheck(turn)`: Evaluates the active player's available legal moves and determines whether the game has reached checkmate or stalemate.
- `Legal_moves(row, col)`: Routes the selected piece to its corresponding movement calculator and filters out moves that violate king safety.
- `MakeMove(...)`: Updates the board when a valid move is executed.

