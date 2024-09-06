import pygame
import chess
import chess.svg
import cairosvg
import io
from chess_ollama import get_ollama_move, get_ollama_commentary

# Initialize Pygame
pygame.init()

# Constants
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
TEXT_PANE_WIDTH = 300
WIDTH, HEIGHT = BOARD_WIDTH + TEXT_PANE_WIDTH, BOARD_HEIGHT
BOARD_SIZE = 560
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_SIZE = int(SQUARE_SIZE * 0.85)  # Slightly smaller than the square
BOARD_OFFSET = (BOARD_WIDTH - BOARD_SIZE) // 2  # Center the board

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
TEXT_BG = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess vs Ollama")

# Load chess pieces images
def load_piece_images():
    pieces = {}
    for color in ['w', 'b']:
        for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
            symbol = piece.upper() if color == 'w' else piece
            svg_string = chess.svg.piece(chess.Piece.from_symbol(symbol))
            png_bytes = cairosvg.svg2png(bytestring=svg_string.encode('utf-8'), scale=2, output_width=PIECE_SIZE, output_height=PIECE_SIZE)
            pieces[symbol] = pygame.image.load(io.BytesIO(png_bytes))
    return pieces

piece_images = load_piece_images()

def draw_board(board):
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, (BOARD_OFFSET + col * SQUARE_SIZE, BOARD_OFFSET + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            piece_image = piece_images[piece.symbol()]
            x = BOARD_OFFSET + col * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
            y = BOARD_OFFSET + row * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
            screen.blit(piece_image, (x, y))

def get_square_from_mouse(pos):
    x, y = pos
    col = (x - BOARD_OFFSET) // SQUARE_SIZE
    row = 7 - ((y - BOARD_OFFSET) // SQUARE_SIZE)
    if 0 <= col < 8 and 0 <= row < 8:
        return chess.square(col, row)
    return None

def draw_text_pane(commentary):
    pygame.draw.rect(screen, TEXT_BG, (BOARD_WIDTH, 0, TEXT_PANE_WIDTH, HEIGHT))
    font = pygame.font.Font(None, 24)
    words = commentary.split()
    lines = []
    current_line = []
    for word in words:
        if font.size(' '.join(current_line + [word]))[0] <= TEXT_PANE_WIDTH - 20:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    
    y = 20
    for line in lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (BOARD_WIDTH + 10, y))
        y += 30

def play_chess_gui():
    board = chess.Board()
    selected_square = None
    game_over = False
    commentary = "Welcome to Chess vs Ollama! I'm ready to play. Make your move!"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not game_over and board.turn == chess.WHITE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    square = get_square_from_mouse(pos)

                    if square is not None:
                        if selected_square is None:
                            selected_square = square
                        else:
                            move = chess.Move(selected_square, square)
                            if move in board.legal_moves:
                                board.push(move)
                                commentary = get_ollama_commentary(board)
                                selected_square = None
                            else:
                                selected_square = square

        screen.fill(WHITE)
        draw_board(board)
        if selected_square is not None:
            col = chess.square_file(selected_square)
            row = 7 - chess.square_rank(selected_square)
            pygame.draw.rect(screen, HIGHLIGHT, (BOARD_OFFSET + col * SQUARE_SIZE, BOARD_OFFSET + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

        draw_text_pane(commentary)
        pygame.display.flip()

        if not game_over and board.turn == chess.BLACK:
            move = get_ollama_move(board)
            board.push(move)
            commentary = get_ollama_commentary(board)

        if board.is_game_over():
            game_over = True
            font = pygame.font.Font(None, 36)
            if board.is_checkmate():
                text = font.render("Checkmate!", True, BLACK)
            elif board.is_stalemate():
                text = font.render("Stalemate!", True, BLACK)
            elif board.is_insufficient_material():
                text = font.render("Draw (Insufficient material)", True, BLACK)
            elif board.is_seventyfive_moves():
                text = font.render("Draw (75-move rule)", True, BLACK)
            elif board.is_fivefold_repetition():
                text = font.render("Draw (Fivefold repetition)", True, BLACK)
            else:
                text = font.render("Game Over!", True, BLACK)
            
            text_rect = text.get_rect(center=(BOARD_WIDTH // 2, HEIGHT - 30))
            screen.blit(text, text_rect)
            pygame.display.flip()

if __name__ == "__main__":
    play_chess_gui()