 Python Pygame Chess

A small, local two-player chess game built with Python and Pygame.

 Overview

This project is a graphical chess game where two players can face off on the same machine. Players can select pieces and move them around using functional chess logic.

When a piece is selected, visual markers highlight its legal moves while accounting for king safety. The game also tracks active turns and detects end-game states.

 Implemented Features

- **Graphical Board:** Renders an \(8 \times 8\) grid with alternating square colors and a custom background.
- **Piece Sprites:** Loads individual image files for all standard chess pieces for both sides.
- **Turn Tracking:** Switches active control between White and Black after every successful move.
- **Movement Logic and Validation:** Calculates legal moves for all pieces and prevents moves that leave the moving side's king in check.
- **Special Moves:** Supports castling and en passant, including castling rights, attacked-square checks, and en passant king-safety validation.
- **Pawn Promotion:** Lets a pawn reaching the final rank promote to a queen, rook, bishop, or knight.
- **Move History:** Displays algebraic move notation, including captures, disambiguation, promotion, check, checkmate, and castling.
- **Move Markers:** Displays visual indicators on valid destination squares when a piece is selected.
- **Checkmate and Stalemate Detection:** Evaluates the board state at the start of each turn to detect checkmate, stalemate, or ongoing play.


 Controls and Instructions

- **Select a Piece:** Left-click one of your pieces when it is your turn.
- **View Legal Moves:** Available destination squares are highlighted with move markers.
- **Make a Move:** Click a highlighted destination square to move. Castling and en passant appear among legal moves when available.
- **Promote a Pawn:** Choose a queen, rook, bishop, or knight from the promotion menu when a pawn reaches the final rank.
- **Restart:** Press **R** after checkmate or stalemate to reset the board.

 Prerequisites

- Python 3.x
- Pygame

 Installation and Launch

1. Ensure Python 3.x and Pygame are installed on your system.
2. Clone or download the repository.
3. Ensure the `images/` directory and its contents remain in the correct locations.
4. Open a terminal in the project directory and run:

   ```bash
   python Chess.py
   ```

 Repository Structure

```text
├── Chess.py
└── images/
    ├── bg.jpg
    ├── Movemarkers/
    │   └── movemarker.png
    └── Pieces/
        ├── rook.png
        ├── rook1.png
        ├── bishop.png
        ├── bishop1.png
        ├── knight.png
        ├── knight1.png
        ├── queen.png
        ├── queen1.png
        ├── king.png
        ├── king1.png
        ├── pawn.png
        └── pawn1.png
```

 Current Limitations and Unfinished Features

- **Game Modes:** The game currently supports local two-player play only; there is no computer opponent or network play.
- **Draw Rules:** Threefold repetition and the 50-move rule are automatic draws. The 50-move counter tracks half-moves and resets after a pawn move or capture. Insufficient-material draws are not implemented.
