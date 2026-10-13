# Python Pygame Chess

A small, local two-player chess game built with Python and Pygame.

## Overview

This project is a graphical chess game where two players can face off on the same machine, select pieces, and move them using custom movement logic. When a piece is selected, visual markers show its available destinations, and the game tracks whose turn it is between White and Black.

## Implemented Features

- Graphical Board: Renders an 8×8 grid with alternating square colors and a custom background.
- Piece Sprites: Loads individual image files for all standard chess pieces for both sides.
- Turn Tracking: Switches active control between White and Black after every successful move.
- Movement Logic: Includes custom movement calculator functions for pawns, knights, bishops, rooks, queens, and kings.
- Move Markers: Displays visual indicators on destination squares when a piece is selected.
- Initial Check Detection: Includes preliminary logic for detecting attacks on the king and checking king movement safety.

## Controls and Instructions

- Select a Piece: Left-click one of your pieces when it is your turn.
- View Available Moves: Destination squares are highlighted with move markers.
- Make a Move: Click a highlighted destination to move the piece and pass the turn to the other player.

## Prerequisites

- Python 3.x
- Pygame

## Installation and Launch Instructions

1. Install Python and Pygame.
2. Clone or download the repository, keeping the `images/` directory structure intact.
3. Run the game from your terminal:

   ```bash
   python Chess.py
   ```

## Repository Directory Structure

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

## Planned / In Progress

- King Safety and Legal Move Validation: Complete the logic that prevents moves from leaving the player's king in check, including handling discovered attacks and pinned pieces.
- Checkmate and Stalemate Detection: Determine when a game has ended because a player has no legal moves.
- Complete Check Detection: Improve and test attack detection across different board positions and piece interactions.

## Future Ideas

- Pawn Promotion: Allow pawns reaching the opposite end of the board to promote to another piece.
- Castling and En Passant: Implement the remaining special chess moves.
- Move History: Display a record of moves made during the game.
- Move Timer: Add a chess clock for timed games.
- Move Undo: Allow players to take back a move, potentially for testing and debugging.
- Board State Testing: Create specific board positions to test movement rules, king safety, and other edge cases.
- Chess Notation: Record moves using standard algebraic chess notation.
- Game Restart: Add a convenient way to start a new game without relaunching the application.


