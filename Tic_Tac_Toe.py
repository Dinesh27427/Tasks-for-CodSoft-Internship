import sys
import pygame
import numpy as np

pygame.init()

# colors
White = (255, 255, 255)
Gray = (180, 180, 180)
Red = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)

# proportions & sizes
Width = 400
Height = 400
Line_width = 6
Board_Rows = 3
Board_Cols = 3
Square_size = Width // Board_Cols
Circle_Radius = Square_size // 3
Circle_Width = 16
Cross_Width = 26


screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(Black)


board = np.zeros((Board_Rows, Board_Cols), dtype=int)

def draw_lines(color=White):
    for x in range(1, Board_Rows):
        pygame.draw.line(screen, color, (0, Square_size * x), (Width, Square_size * x), Line_width)
        pygame.draw.line(screen, color, (Square_size * x, 0), (Square_size * x, Height), Line_width)

def draw_figuers(color=White):  
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            cx = col * Square_size + Square_size // 2
            cy = row * Square_size + Square_size // 2
            if board[row][col] == 1:
                
                pygame.draw.circle(screen, color, (cx, cy), Circle_Radius, Circle_Width)
            elif board[row][col] == 2:
                
                x1, y1 = col * Square_size + Square_size // 4, row * Square_size + Square_size // 4
                x2, y2 = col * Square_size + 3 * Square_size // 4, row * Square_size + 3 * Square_size // 4
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), Cross_Width)
                pygame.draw.line(screen, color, (x1, y2), (x2, y1), Cross_Width)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=None):
    
    if check_board is None:
        check_board = board
    return not (check_board == 0).any()

def check_win(player, check_board=None):
    if check_board is None:
        check_board = board

    # columns
    for col in range(Board_Cols):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    # rows
    for row in range(Board_Rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    # diagonals
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(Board_Rows):
            for col in range(Board_Cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score
    else:
        
        best_score = 1000
        for row in range(Board_Rows):
            for col in range(Board_Cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(Black)
    draw_lines()
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            restart_game()
            game_over = False
            player = 1

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            
            col = event.pos[0] // Square_size
            row = event.pos[1] // Square_size

            if available_square(row, col):
                mark_square(row, col, player)
                if check_win(player):
                    game_over = True

                
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        
                        player = player % 2 + 1

                if not game_over and is_board_full():
                    game_over = True

    if not game_over:
        draw_figuers()
    else:
        if check_win(1):
            draw_figuers(Green)
            draw_lines(Green)
        elif check_win(2):
            draw_figuers(Red)
            draw_lines(Red)
        else:
            draw_figuers(Gray)
            draw_lines(Gray)

    pygame.display.update()


