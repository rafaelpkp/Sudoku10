import pygame
import sys
from Board import Board
from Cell import Cell
from SudokuGenerator import SudokuGenerator

pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)
FONT = pygame.font.SysFont('Arial', 40)
SMALL_FONT = pygame.font.SysFont('Arial', 20)

def draw_start_screen():
    SCREEN.fill(BG_COLOR)
    title_font = pygame.font.SysFont('Arial', 70)
    title = title_font.render("Sudoku", True, LINE_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    SCREEN.blit(title, title_rect)

    easy_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    medium_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    hard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

    pygame.draw.rect(SCREEN, LINE_COLOR, easy_button, 2)
    pygame.draw.rect(SCREEN, LINE_COLOR, medium_button, 2)
    pygame.draw.rect(SCREEN, LINE_COLOR, hard_button, 2)

    easy_text = FONT.render("Easy", True, LINE_COLOR)
    medium_text = FONT.render("Medium", True, LINE_COLOR)
    hard_text = FONT.render("Hard", True, LINE_COLOR)

    SCREEN.blit(easy_text, easy_text.get_rect(center=easy_button.center))
    SCREEN.blit(medium_text, medium_text.get_rect(center=medium_button.center))
    SCREEN.blit(hard_text, hard_text.get_rect(center=hard_button.center))

    pygame.display.flip()

    return easy_button, medium_button, hard_button

def draw_game_screen(board):
    SCREEN.fill(BG_COLOR)
    board.draw()
    # Draw buttons
    reset_button = pygame.Rect(50, HEIGHT - 50, 100, 40)
    restart_button = pygame.Rect(220, HEIGHT - 50, 100, 40)
    exit_button = pygame.Rect(390, HEIGHT - 50, 100, 40)

    pygame.draw.rect(SCREEN, LINE_COLOR, reset_button, 2)
    pygame.draw.rect(SCREEN, LINE_COLOR, restart_button, 2)
    pygame.draw.rect(SCREEN, LINE_COLOR, exit_button, 2)

    reset_text = SMALL_FONT.render("Reset", True, LINE_COLOR)
    restart_text = SMALL_FONT.render("Restart", True, LINE_COLOR)
    exit_text = SMALL_FONT.render("Exit", True, LINE_COLOR)

    SCREEN.blit(reset_text, reset_text.get_rect(center=reset_button.center))
    SCREEN.blit(restart_text, restart_text.get_rect(center=restart_button.center))
    SCREEN.blit(exit_text, exit_text.get_rect(center=exit_button.center))
    
    pygame.display.flip()
    return reset_button, restart_button, exit_button

def draw_end_screen(win):
    SCREEN.fill(BG_COLOR)
    end_font = pygame.font.SysFont('Arial', 70)
    if win:
        end_text = end_font.render("Game Won!", True, (0, 255, 0))
    else:
        end_text = end_font.render("Game Over", True, (255, 0, 0))
    
    end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(end_text, end_rect)
    pygame.display.flip()

def main():
    game_state = "start"
    board = None
    win = False

    while True:
        if game_state == "start":
            easy_button, medium_button, hard_button = draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    difficulty = None
                    if easy_button.collidepoint(pos):
                        difficulty = "easy"
                    elif medium_button.collidepoint(pos):
                        difficulty = "medium"
                    elif hard_button.collidepoint(pos):
                        difficulty = "hard"
                    
                    if difficulty:
                        removed_cells = {"easy": 30, "medium": 40, "hard": 50}[difficulty]
                        sudoku_generator = SudokuGenerator(9, removed_cells)
                        sudoku_generator.fill_values()
                        solution = [row[:] for row in sudoku_generator.get_board()]
                        sudoku_generator.remove_cells()
                        puzzle = sudoku_generator.get_board()
                        
                        board = Board(WIDTH, HEIGHT - 60, SCREEN, difficulty)
                        board.cells = [[Cell(puzzle[i][j], i, j, SCREEN) for j in range(9)] for i in range(9)]
                        board.solution = solution
                        game_state = "game"

        elif game_state == "game":
            reset_button, restart_button, exit_button = draw_game_screen(board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if reset_button.collidepoint(pos):
                        board.reset_to_original()
                    elif restart_button.collidepoint(pos):
                        game_state = "start"
                    elif exit_button.collidepoint(pos):
                        pygame.quit()
                        sys.exit()
                    else:
                        if pos[1] < HEIGHT - 60:
                            row, col = board.click(pos[0], pos[1])
                            if row is not None:
                                board.select(row, col)
                if event.type == pygame.KEYDOWN:
                    if board.selected_cell:
                        row, col = board.selected_cell
                        if board.cells[row][col].editable:
                            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                                board.sketch(int(event.unicode))
                            elif event.key == pygame.K_RETURN:
                                board.place_number(board.cells[row][col].sketched_value)
                                if board.is_full():
                                    if board.check_board():
                                        win = True
                                    else:
                                        win = False
                                    game_state = "end"
                            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                                board.clear()
                        if event.key == pygame.K_UP:
                            board.select(max(0, row - 1), col)
                        elif event.key == pygame.K_DOWN:
                            board.select(min(8, row + 1), col)
                        elif event.key == pygame.K_LEFT:
                            board.select(row, max(0, col - 1))
                        elif event.key == pygame.K_RIGHT:
                            board.select(row, min(8, col + 1))

        elif game_state == "end":
            draw_end_screen(win)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "start"

if __name__ == "__main__":
    main()
