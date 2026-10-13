import pygame
from pathlib import Path

pygame.init()

# todo
# king checks
# legal move funneling

#board start
board = [
    ["rook1","knight1","bishop1","queen1","king1","bishop1","knight1","rook1"],
    ["pawn1","pawn1","pawn1","pawn1","pawn1","pawn1","pawn1","pawn1"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"],
    ["rook","knight","bishop","queen","king","bishop","knight","rook"],
]
knight_offsets = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]   
rook_offsets = [(1,0), (-1,0), (0,1), (0,-1)]
Bishop_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
queen_offsets = [
    (0, 1), (0, -1),   #bum
    (1, 0), (-1, 0),   # bum
    (1, 1), (1, -1),   #bum
    (-1, 1), (-1, -1)  # bum
]   




screen = pygame.display.set_mode((1100, 900))
pygame.display.set_caption('bot makes chess')
clock = pygame.time.Clock()

BASE_DIR = Path(__file__).resolve().parent

# Image directories
IMAGE_DIR = BASE_DIR / "images"
PIECES_DIR = IMAGE_DIR / "Pieces"
MOVEMARKER_DIR = IMAGE_DIR / "Movemarkers"

# Background
img = pygame.image.load(str(IMAGE_DIR / "bg.jpg")).convert()
img = pygame.transform.smoothscale(img, screen.get_size())

# Move marker
MoveMarker = pygame.image.load(
    str(MOVEMARKER_DIR / "movemarker.png")
).convert_alpha()
MoveMarker = pygame.transform.scale_by(MoveMarker, 0.1)

# Black pieces
rook1 = pygame.image.load(str(PIECES_DIR / "rook1.png")).convert_alpha()
BBishop = pygame.image.load(str(PIECES_DIR / "bishop1.png")).convert_alpha()
BKnight = pygame.image.load(str(PIECES_DIR / "knight1.png")).convert_alpha()
BQueen = pygame.image.load(str(PIECES_DIR / "queen1.png")).convert_alpha()
BKing = pygame.image.load(str(PIECES_DIR / "king1.png")).convert_alpha()
Bpawn = pygame.image.load(str(PIECES_DIR / "pawn1.png")).convert_alpha()

# White pieces
WRook = pygame.image.load(str(PIECES_DIR / "rook.png")).convert_alpha()
WBishop = pygame.image.load(str(PIECES_DIR / "bishop.png")).convert_alpha()
WKnight = pygame.image.load(str(PIECES_DIR / "knight.png")).convert_alpha()
Wqueen = pygame.image.load(str(PIECES_DIR / "queen.png")).convert_alpha()
WKing = pygame.image.load(str(PIECES_DIR / "king.png")).convert_alpha()
Wpawn = pygame.image.load(str(PIECES_DIR / "pawn.png")).convert_alpha()


#board
board_surface = pygame.Surface((600,600))
board_surface.fill('blue')

#board-squares
square1 = pygame.Surface((75,75))
square1.fill(pygame.Color('#d28b48'))
square2 = pygame.Surface((75,75))
square2.fill(pygame.Color('#ffcd9f'))


x = 90
y = 100
board_coordinates = []

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
    piece = board[row][col]
    r,c = row,col
    # print("checking moves")
    if "1" in piece:
        if get_cell(r+1,c+1) != "" and "1" not in get_cell(r+1,c+1):
            MoveMarkers.append((r+1,c+1))
        if get_cell(r+1,c-1) != "" and "1" not in get_cell(r+1,c+1):
            MoveMarkers.append((r+1,c-1))
        # print("black pawn")
        if row == starting_rows[1]:
            # print("starting row")
            if get_cell(r+1,c) == "":
                # print("first square empty")
                if get_cell(r+2,c)=="":
                #    print('second square empty')
                   MoveMarkers += [(r+2, c), (r+1, c)]   
                MoveMarkers.append((r+1,c))
        elif get_cell(r+1,c)=="":
            MoveMarkers.append((r+1,c))
    else:
        if get_cell(r-1,c+1) != "" and "1" in get_cell(r-1,c+1):
            MoveMarkers.append((r-1,c+1))
        if get_cell(r-1,c-1) != "" and "1" in get_cell(r-1,c-1):
            MoveMarkers.append((r-1,c-1))
        if row == starting_rows[0]: #print("starting row")
            if get_cell(r-1,c) == "": #print("first square empty")
                if get_cell(r-2,c)=="": #print("second square empty")
                    MoveMarkers += [(r-2, c), (r-1, c)]   
                MoveMarkers.append((r-1,c))
        elif get_cell(r-1,c)=="":
            MoveMarkers.append((r-1,c))
    return MoveMarkers
            



def KnightLegalMoves(MoveMarkers,row,col,knight_offsets):
    Color = get_color(row,col)


    for dr, dc in knight_offsets:
        cell = get_cell(row + dr, col + dc)
        if cell is None:
            continue
        if cell == '':
            MoveMarkers.append((row + dr, col + dc))
        elif cell is not None and "king" not in cell:
            is_black_target = "1" in cell
            if (Color == "B" and not is_black_target) or (Color == "W" and is_black_target):
                MoveMarkers.append((row + dr, col + dc))
    return MoveMarkers   
 
            
def BishopLegalMoves(MoveMarkers, row, col, bishop_offsets):

    Color = get_color(row,col)
    for dr, dc in bishop_offsets:
        r, c = row + dr, col + dc          
        while 0 <= r < 8 and 0 <= c < 8:
            cell = get_cell(r,c)
            if cell == "":
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
                Movemarkers.append((r,c))
            elif "king" not in cell:
                is_black_target = "1" in cell
                if (Color == "B" and not is_black_target) or (Color == "W" and is_black_target):
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
            print(f"  ({r},{c}) -> off board, skip")
            continue

        cell = get_cell(r, c)

        if cell is None or cell == "":
            in_check = checkdetection(r, c, origin=(row, col))
            if in_check:
                print(f"  ({r},{c}) -> empty, but king would be in check, skip")
            else:
                print(f"  ({r},{c}) -> empty, safe, MARK")
                Movemarkers.append((r, c))

        else:
            is_black_target = "1" in cell
            is_enemy_target = (Color == "B" and not is_black_target) or (Color == "W" and is_black_target)
            if not is_enemy_target:
                print(f"  ({r},{c}) -> own piece ({cell}), skip")
            else:
                in_check = checkdetection(r, c, origin=(row, col))
                if in_check:
                    print(f"  ({r},{c}) -> enemy piece ({cell}), but capture would leave king in check, soo skip")
                else:
                    print(f"  ({r},{c}) -> enemy piece ({cell}), safe capture, marking square")
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
                print(f"Found piece {cell} at ({r},{c}), enemy={is_enemy(Color, cell)}")
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
        
    print(f"Checking ({king_row},{king_col}), Color={Color}")
    return False


def place_pieces(board_coordinates, PIECES_DIR, board):
    #given the board position determine what piece should be there
    piece_rect_list = []
    # piece_surfaces = []
    for row in range(8):
         for col in range(8):
            piece_pos = board_coordinates[row * 8 + col]
            if board[row][col]:
                piece_path = PIECES_DIR / f"{board[row][col]}.png"
                piece = pygame.transform.scale_by(
                    pygame.image.load(str(piece_path)).convert_alpha(),
                    1.2
                )
                piece_rect_list.append(piece.get_rect(topleft = ((piece_pos[0] + 37) - (piece.get_width()/2), (piece_pos[1] + 37) - (piece.get_height()/2))))
                screen.blit(piece, ((piece_pos[0] + 37) - (piece.get_width()/2) , (piece_pos[1] + 37) - (piece.get_height()/2)))
    return piece_rect_list

def Legal_moves(board,row,col):
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
            print("queen")
            return QueenLegalMoves(MoveMarkers,row,col,queen_offsets)


def generateBoard(x,y,board_coordinates):
    board_coordinates = []
    for row in range(8):
        for col in range(8):
            if (row + col)%2 == 0:
                color = square1 
            else: color = square2
            screen.blit(color, ((x, y)))
            board_coordinates.append((x,y))


            pygame.draw.rect(screen, (0, 0, 0), (x, y, 75, 75), 1)
            x+=75    
        y+=75
        x=90
    return board_coordinates


board_coordinates = generateBoard(x,y,board_coordinates)
LegalMoves = []
marker_rects = []
SelectedPiece = ()
turn = "W"


while True:
    # mouse_pos = pygame.event.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            col = (event.pos[0] - x)//75
            row = (event.pos[1] - y)//75
           
            if "1" in board[row][col]:
                color = "B"
            else:
                color = "W"
            hit = False
            for idx,marker in enumerate(marker_rects):
                if marker.collidepoint(event.pos):
                    print(f"you clicked marker {idx}")
                    hit = True
                    MakeMove(SelectedPiece,col,row,LegalMoves)
                    LegalMoves = []
                    if turn == "W": turn = "B"
                    else: turn = "W"
                    break
            if not hit:
                for piece_rect in piece_rect_list:
                    if piece_rect.collidepoint(event.pos):
                        if turn == color:
                            # print(f"click: {event.pos} → grid: ({row}, {col})")
                            LegalMoves = Legal_moves(board,row,col)
                            # print(f"Knight at ({row},{col}) → moves: {LegalMoves}")   
                            SelectedPiece = (row,col)
                            break

            
    #render
    screen.blit(img, (0,0))
    screen.blit(board_surface, (90,100))
    generateBoard(x,y,board_coordinates) 
    piece_rect_list = place_pieces(board_coordinates,PIECES_DIR,board)


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