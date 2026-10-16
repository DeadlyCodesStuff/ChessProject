
import pygame
from pathlib import Path


pygame.init()

screen = pygame.display.set_mode((1100, 900))
pygame.display.set_caption("bot makes chess")
clock = pygame.time.Clock()


BASE_DIR = Path(__file__).resolve().parent

IMAGE_DIR = BASE_DIR / "images"
PIECES_DIR = IMAGE_DIR / "Pieces"
MOVEMARKER_DIR = IMAGE_DIR / "Movemarkers"

Square_size = 75
DEBUG = False
ispromoting = False
pawn_pos = ()


board = [
    ["rook1", "knight1", "bishop1", "queen1", "king1", "bishop1", "knight1", "rook1"],
    ["pawn1", "pawn1", "pawn1", "pawn1", "pawn1", "pawn1", "pawn1", "pawn1"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
]



piece_names = [
    "pawn", "rook", "knight", "bishop", "queen", "king",
    "pawn1", "rook1", "knight1", "bishop1", "queen1", "king1",
]

piece_surfaces = {}

for name in piece_names:
    path = PIECES_DIR / f"{name}.png"
    piece_surfaces[name] = pygame.image.load(
        str(path)
    ).convert_alpha()

piece_images = {
    name: pygame.transform.scale(
        image,
        (int(Square_size * 0.8), int(Square_size * 0.8))
    )
    for name, image in piece_surfaces.items()
}

promotion_images = {
    name: pygame.transform.scale(
        piece_surfaces[name],
        (Square_size * 0.8, Square_size *0.8)
    )
    for name in [
        "queen", "rook", "bishop", "knight",
        "queen1", "rook1", "bishop1", "knight1"
    ]
}



rook1 = piece_surfaces["rook1"]
BBishop = piece_surfaces["bishop1"]
BKnight = piece_surfaces["knight1"]
BQueen = piece_surfaces["queen1"]
BKing = piece_surfaces["king1"]
Bpawn = piece_surfaces["pawn1"]

WRook = piece_surfaces["rook"]
WBishop = piece_surfaces["bishop"]
WKnight = piece_surfaces["knight"]
Wqueen = piece_surfaces["queen"]
WKing = piece_surfaces["king"]
Wpawn = piece_surfaces["pawn"]



knight_offsets = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1)
]

rook_offsets = [
    (1, 0), (-1, 0), (0, 1), (0, -1)
]

Bishop_offsets = [
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]

queen_offsets = [
    (0, 1), (0, -1),
    (1, 0), (-1, 0),
    (1, 1), (1, -1),
    (-1, 1), (-1, -1)
]



def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


img = pygame.image.load(
    str(IMAGE_DIR / "bg.jpg")
).convert()

img = pygame.transform.smoothscale(
    img, screen.get_size()
)

MoveMarker = pygame.image.load(
    str(MOVEMARKER_DIR / "movemarker.png")
).convert_alpha()

MoveMarker = pygame.transform.scale_by(
    MoveMarker, 0.1
)


board_surface = pygame.Surface((600, 600))
board_surface.fill("blue")

square1 = pygame.Surface((Square_size, Square_size))
square1.fill(pygame.Color("#d28b48"))

square2 = pygame.Surface((Square_size, Square_size))
square2.fill(pygame.Color("#ffcd9f"))


font = pygame.font.SysFont("Arial", 36)
text_surface = font.render(
    "Press R to restart",
    True,
    (255, 255, 255)
)


x = 90
y = 100
board_coordinates = []


def KingPOS(turn):
    row_counter = 0
    col_counter = 0

    for row in board:
        for col in row:
            if col != "":
                if turn == "B" and col == "king1":
                    return (row_counter, col_counter)
                elif turn == "W" and col == "king":
                    return (row_counter, col_counter)

            col_counter += 1
        row_counter += 1
        col_counter = 0

    return None

def LeavesKingInCheck(turn, start, end):
    r, c = start
    nr, nc = end

    piece = board[r][c]
    captured = board[nr][nc]

    board[nr][nc] = piece
    board[r][c] = ""

    x,y = KingPOS(turn)
    in_check = checkdetection(x, y, None)

    board[r][c] = piece
    board[nr][nc] = captured

    return in_check



def get_cell(row, col):
    if row < 0 or col < 0 or row >= 8 or col >= 8:
        return None
    return board[row][col] 
 
def get_color(row,col):
    piece = board[row][col]
    if "1" in piece:
        Color = "B"
    else:
        Color ="W" 
    return Color

def is_enemy(color,cell):
    is_black_piece = "1" in cell

    if color == "B":
        return not is_black_piece
    else:
        return is_black_piece

def PawnLegalMoves(MoveMarkers,row,col):
    starting_rows = [6,1]
    piece = get_cell(row,col)
    r,c = row,col
    King_Position = KingPOS(turn)
    # print("checking moves")
    if piece is not None:
        if "1" in piece:  # Black pawn
            # Diagonal captures
            target = get_cell(r + 1, c + 1)
            if target is not None and target != "" and "1" not in target:
                if not LeavesKingInCheck(turn,(row,col),(r+1,c+1)):
                    MoveMarkers.append((r + 1, c + 1))

            target = get_cell(r + 1, c - 1)
            if target is not None and target != "" and "1" not in target:
                if not LeavesKingInCheck(turn,(row,col),(r+1,c-1)):
                    MoveMarkers.append((r + 1, c - 1))

            # Forward movement
            if row == starting_rows[1]:
                if get_cell(r + 1, c) == "":
                    if get_cell(r + 2, c) == "":
                        if not LeavesKingInCheck(turn,(row,col),(r+2,c)):
                            MoveMarkers.append((r + 2, c))
                    if not LeavesKingInCheck(turn,(row,col),(r+1,c)):
                        MoveMarkers.append((r + 1, c))
            elif get_cell(r + 1, c) == "":
                if not LeavesKingInCheck(turn,(row,col),(r+1,c)):
                    MoveMarkers.append((r + 1, c))

        else:  # White pawn
            # Diagonal captures
            target = get_cell(r - 1, c + 1)
            if target is not None and target != "" and "1" in target:
                if not LeavesKingInCheck(turn,(row,col),(r-1,c+1)):
                    MoveMarkers.append((r - 1, c + 1))

            target = get_cell(r - 1, c - 1)
            if target is not None and target != "" and "1" in target:
                if not LeavesKingInCheck(turn,(row,col),(r-1,c-1)):
                    MoveMarkers.append((r - 1, c - 1))

            # Forward movement
            if row == starting_rows[0]:
                if get_cell(r - 1, c) == "":
                    if get_cell(r - 2, c) == "":
                        if not LeavesKingInCheck(turn,(row,col),(r-2,c)):
                            MoveMarkers.append((r - 2, c))
                    if not LeavesKingInCheck(turn,(row,col),(r-1,c)):
                        MoveMarkers.append((r - 1, c))
            elif get_cell(r - 1, c) == "":
                if not LeavesKingInCheck(turn,(row,col),(r-1,c)):
                    MoveMarkers.append((r - 1, c))
    return MoveMarkers


def KnightLegalMoves(MoveMarkers,row,col,knight_offsets):
    Color = get_color(row,col)

    for dr, dc in knight_offsets:
        cell = get_cell(row + dr, col + dc)
        if cell is None:
            continue
        if cell == '':
            if not LeavesKingInCheck(turn,(row,col),(row+dr,col+dc)):
                MoveMarkers.append((row + dr, col + dc))
        elif cell is not None and "king" not in cell:
            is_black_target = "1" in cell
            if (Color == "B" and not is_black_target) or (Color == "W" and is_black_target):
                if not LeavesKingInCheck(turn,(row,col),(row+dr,col+dc)):
                    MoveMarkers.append((row + dr, col + dc))
    return MoveMarkers   
 
            
def BishopLegalMoves(MoveMarkers, row, col, bishop_offsets):

    Color = get_color(row,col)
    for dr, dc in bishop_offsets:
        r, c = row + dr, col + dc          
        while 0 <= r < 8 and 0 <= c < 8:
            cell = get_cell(r,c)
            if cell == "":
                if not LeavesKingInCheck(turn,(row,col),(r,c)):
                    MoveMarkers.append((r, c))
            elif cell is not None and "king" not in cell:
                is_black_target = "1" in cell
                if (Color == "B" and not is_black_target) or (Color == "W" and is_black_target):
                    MoveMarkers.append((r, c ))
                break
            else:
                break
            r += dr
            c += dc
    return MoveMarkers

def QueenLegalMoves(Movemarkers,row,col,Queen_offsets):
    Color = get_color(row,col)
    for dr,dc in Queen_offsets:
        r,c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            cell = get_cell(r,c)
            if cell == "":
                if not LeavesKingInCheck(turn,(row,col),(r,c)):
                    Movemarkers.append((r,c))
            elif "king" not in cell:
                is_black_target = "1" in cell
                if (Color == "B" and not is_black_target) or (Color == "W" and is_black_target):
                    if not LeavesKingInCheck(turn,(row,col),(r,c)):
                        Movemarkers.append((r, c ))
                break
            else:
                break
            r += dr
            c += dc
    return Movemarkers
            

def Rooklegalmoves(Movemarkers,row,col,rook_offsets):

    Color = get_color(row,col)

    for dr,dc in rook_offsets:
        r,c = row + dr,col + dc
        while 0 <= r <= 8 and 0 <= c <=8:
            cell = get_cell(r,c) 
            if cell == "":
                if not LeavesKingInCheck(turn,(row,col),(r,c)):
                    Movemarkers.append((r,c))
            elif cell is not None and "king" not in cell:
                is_black_target = "1" in cell
                if (Color == "B" and not is_black_target) or (Color == "W" and is_black_target):
                    Movemarkers.append((r, c ))
                break
            else:
                break
            r += dr
            c += dc
    return Movemarkers

def kinglegalmoves(Movemarkers, row, col):
    kingsquares = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

    piece = board[row][col]
    if "1" in piece:
        Color = "B"
    else:
        Color = "W"

    for dr, dc in kingsquares:
        r, c = row + dr, col + dc
        if not (0 <= r < 8 and 0 <= c < 8):
            debug(f"  ({r},{c}) -> off board, skip")
            continue
        cell = get_cell(r, c)
        if cell is None or cell == "":
            in_check = checkdetection(r, c, origin=(row, col))
            if in_check:
                debug(f"  ({r},{c}) -> empty, but king would be in check, skip")
            else:
                debug(f"  ({r},{c}) -> empty, safe, MARK")
                Movemarkers.append((r, c))
        else:
            is_black_target = "1" in cell
            is_enemy_target = (Color == "B" and not is_black_target) or (Color == "W" and is_black_target)
            if not is_enemy_target:
                debug(f"  ({r},{c}) -> own piece ({cell}), skip")
            else:
                in_check = checkdetection(r, c, origin=(row, col))
                if in_check:
                    debug(f"  ({r},{c}) -> enemy piece ({cell}), but capture would leave king in check, soo skip")
                else:
                    debug(f"  ({r},{c}) -> enemy piece ({cell}), safe capture, marking square")
                    Movemarkers.append((r, c))

    return Movemarkers   

def MakeMove(SelectedPiece,col,row,LegalMoves):
    if not SelectedPiece:
        print("No piece selected")
        return[]

    r,c = SelectedPiece

    if (row, col) not in LegalMoves:
        print("Illegal Move")
        return []
    piece = board[r][c]
    captured = board[row][col]
    board[row][col] = piece
    board[r][c] = ""
    return {"moved": piece, "captured": captured}

def checkdetection(king_row, king_col, origin=None):
    # Color = get_color(king_row, king_col)
    if origin is not None:
        Color = get_color(origin[0], origin[1])
    else:
        Color = get_color(king_row, king_col)
        
    directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

    # Sliding pieces (rook, bishop, queen) + adjacent king
    for dr, dc in directions:
        r, c = king_row + dr, king_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if (r, c) == origin:
                r += dr
                c += dc
                continue
            cell = get_cell(r, c)
            if cell is not None and cell != "":
                debug(f"Found piece {cell} at ({r},{c}), enemy={is_enemy(Color, cell)}")
                if is_enemy(Color, cell):
                    if (dr == 0 or dc == 0) and ("rook" in cell or "queen" in cell):
                        return True
                    if (dr != 0 and dc != 0) and ("bishop" in cell or "queen" in cell):
                        return True
                    if abs(dr) <= 1 and abs(dc) <= 1 and "king" in cell:
                        return True
                break
            r += dr
            c += dc

    # Knights
    for dr, dc in [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]:
        r, c = king_row + dr, king_col + dc
        if (r, c) == origin:
            continue
        cell = get_cell(r, c)
        if cell is not None and cell != "" and is_enemy(Color, cell) and "knight" in cell:
            return True

   # Pawns
    pawn_row = king_row + (-1 if Color == "W" else 1)

    for dc in (-1, 1):
        r, c = pawn_row, king_col + dc

        if not (0 <= r < 8 and 0 <= c < 8):
            continue

        if (r, c) == origin:
            continue

        cell = get_cell(r, c)

        if cell and is_enemy(Color, cell) and "pawn" in cell:
            return True
        
    # print(f"Checking ({king_row},{king_col}), Color={Color}")
    return False


def place_pieces(board_coordinates, board):
    #given the board position determine what piece should be there
    piece_rect_list = []
    # piece_surfaces = []
    for row in range(8):
         for col in range(8):
            piece_pos = board_coordinates[row * 8 + col]
            cell = get_cell(row,col)
            if cell is not None and cell != "":
                # piece_path = PIECES_DIR / f"{board[row][col]}.png"
                piece = piece_images[board[row][col]]
                piece_rect_list.append(piece.get_rect(topleft = ((piece_pos[0] + 37) - (piece.get_width()/2), (piece_pos[1] + 37) - (piece.get_height()/2))))
                screen.blit(piece, ((piece_pos[0] + 37) - (piece.get_width()/2) , (piece_pos[1] + 37) - (piece.get_height()/2)))
    return piece_rect_list


def restart_game():
    global board, turn, state, SelectedPiece, LegalMoves, marker_rects

    board = [
        ["rook1", "knight1", "bishop1", "queen1", "king1", "bishop1", "knight1", "rook1"],
        ["pawn1"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["pawn"] * 8,
        ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    ]

    turn = "W"
    state = "neutral"
    SelectedPiece = None
    LegalMoves = []
    marker_rects = []

def Legal_moves(row,col):
    MoveMarkers = []

    if board[row][col]:
        Selectedpiece = board[row][col]
        #pawns
        if Selectedpiece == 'pawn' or Selectedpiece == "pawn1":
             return PawnLegalMoves(MoveMarkers,row,col)

        if Selectedpiece == "knight" or Selectedpiece == "knight1":
            return KnightLegalMoves(MoveMarkers,row,col,knight_offsets)
        
        if Selectedpiece == "bishop" or Selectedpiece == "bishop1":
            return BishopLegalMoves(MoveMarkers, row,col,Bishop_offsets)
        
        if Selectedpiece == "rook" or Selectedpiece == "rook1":
            return Rooklegalmoves(MoveMarkers,row,col,rook_offsets)
        
        if Selectedpiece == "king" or Selectedpiece == "king1":
            return kinglegalmoves(MoveMarkers,row,col)
    
        if Selectedpiece == "queen" or Selectedpiece == "queen1":
            return QueenLegalMoves(MoveMarkers,row,col,queen_offsets)
    else:
        return MoveMarkers

def generateBoard(x,y,board_coordinates):
    board_coordinates = []
    for row in range(8):
        for col in range(8):
            if (row + col)%2 == 0:
                color = square1 
            else: color = square2
            screen.blit(color, ((x, y)))
            board_coordinates.append((x,y))


            pygame.draw.rect(screen, (0, 0, 0), (x, y, Square_size, Square_size), 1)
            x+=75    
        y+=75
        x=90
    return board_coordinates

def WinCheck(turn):
    # print(f'turn {turn}')
    moves = 0
    row_counter = 0
    state = "neutral"

    for row in board:
        debug(row)
        col_counter = 0

        for i in row:
            if i != "":
                if turn == "W":
                    if "1" not in i:
                        if "king" in i:
                            king_pos = (row_counter,col_counter)

                        legal = Legal_moves(row_counter, col_counter)
                        moves += len(legal)
                        debug(f"found {len(legal)} for {i}")
                else:
                    if "1" in i:
                        if "king" in i:
                            king_pos = (row_counter,col_counter)
                        legal = Legal_moves(row_counter, col_counter)
                        moves += len(legal)
                        debug(f"found {len(legal)} for {i}")

            col_counter += 1
        row_counter += 1
    if moves == 0:
       if checkdetection(king_pos[0],king_pos[1],None): state = "checkmate"
       else: state = "stalemate"
    return state

def PromotionCheck(row, col):
    cell = get_cell(row, col)

    if not cell or "pawn" not in cell:
        return False

    if cell.endswith("1"): 
        return row == 7

    return row == 0
                
            

def promoting(row, col):
    promotion_pieces = ["queen", "rook", "bishop", "knight"]
    promotion_rects = []

    cell = get_cell(row, col)
    if cell is None or cell == "":
        return promotion_rects

    is_black = "1" in cell
    suffix = "1" if is_black else ""

    piece_x, piece_y = board_coordinates[row * 8 + col]

    for i, piece in enumerate(promotion_pieces):
        option_x = piece_x
        option_y = piece_y + (-i * Square_size if is_black else i * Square_size)

        square_rect = pygame.Rect(
            option_x, option_y, Square_size, Square_size
        )
        promotion_rects.append(square_rect)

        pygame.draw.rect(screen, pygame.Color("#808080"), square_rect)

        image = promotion_images[f"{piece}{suffix}"]
        image_rect = image.get_rect(center=square_rect.center)
        screen.blit(image, image_rect)

    return promotion_rects

def PromotePawn(row, col, piece):
    global board, ispromoting, promotion_rects,state,turn

    cell = get_cell(row, col)
    debug(f"PromotePawn called. Turn before: {turn}")

    if cell is None or "pawn" not in cell:
        return

    suffix = "1" if "1" in cell else ""

    board[row][col] = f"{piece}{suffix}"

    ispromoting = False
    promotion_rects = []

    if turn == "W": 
        turn = "B"
    else: turn = "W"

    debug(f"Turn after switch: {turn}")

    state = WinCheck(turn)


    


board_coordinates = generateBoard(x,y,board_coordinates)
LegalMoves = []
marker_rects = []
SelectedPiece = ()
turn = "W"
state = WinCheck(turn)



while True:
    # mouse_pos = pygame.event.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if state in ("checkmate", "stalemate") and event.key == pygame.K_r:
                restart_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
                col = (event.pos[0] - x)//Square_size
                row = (event.pos[1] - y)//Square_size

                if ispromoting:
                    promotion_pieces = ["queen", "rook", "bishop", "knight"]
                    debug("promoting")
                    for i, rect in enumerate(promotion_rects):
                        debug(f"Option: {promotion_pieces[i]}, rect: {rect}")
                        if rect.collidepoint(event.pos):
                            debug(f"Selected promotion: {promotion_pieces[i]}")
                            PromotePawn(
                                promotion_row,
                                promotion_col,
                                promotion_pieces[i]
                            )
                            break
                    continue

                elif state == "neutral":
                    if 0 <= row < 8 and 0 <= col < 8:
                        piece = get_cell(row,col)
                        if piece != None:
                            if "1" in piece:
                                color = "B"
                            else:
                                color = "W"

                            hit = False

                            for idx,marker in enumerate(marker_rects):
                                if marker.collidepoint(event.pos):
                                    debug(f"you clicked marker {idx}")
                                    hit = True
                                    MakeMove(SelectedPiece,col,row,LegalMoves)

                                    ispromoting = PromotionCheck(row,col)

                                    if ispromoting:
                                        promotion_row = row
                                        promotion_col = col
                                        promotion_rects = promoting(promotion_row, promotion_col)
                                        promotion_pieces = ["queen", "rook", "bishop", "knight"]
                                    else:
                                        if turn == "W":
                                            turn = "B"
                                        else:
                                            turn = "W"
                                        state = WinCheck(turn)

                                    LegalMoves = []
                                    break

                                    
                            if not hit:
                                for piece_rect in piece_rect_list:
                                    if piece_rect.collidepoint(event.pos):
                                        if turn == color:
                                            debug(f"click: {event.pos} → grid: ({row}, {col})")
                                            LegalMoves = Legal_moves(row,col)
                                            debug(f"Knight at ({row},{col}) → moves: {LegalMoves}")   
                                            SelectedPiece = (row,col)
                                            break

                
        
    #render
    screen.blit(img, (0,0))
    screen.blit(board_surface, (90,100))
    generateBoard(x,y,board_coordinates) 
    piece_rect_list = place_pieces(board_coordinates,board)


    if ispromoting:
        promotion_rects = promoting(promotion_row,promotion_col)


    if state == "checkmate" or state == "stalemate":
        screen.blit(text_surface, (50, 50)) 
    else:
        marker_rects = []
        if LegalMoves:
            #  print(LegalMoves)
            for r,c in LegalMoves: 
                pos = board_coordinates[r * 8 + c]
                center = (pos[0] + 37, pos[1] + 37)
                marker_rect = MoveMarker.get_rect(center=center)
                screen.blit(MoveMarker, marker_rect)
                marker_rects.append(marker_rect)

    # pygame.display.flip()
    pygame.display.update()
    clock.tick(60)