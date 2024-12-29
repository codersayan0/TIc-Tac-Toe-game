import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (28, 170, 156)
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
FONT = pygame.font.SysFont('arial', 40)

# Load custom background image
background_img = pygame.image.load('game.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe with AI')

# Board setup
board = [[None for _ in range(3)] for _ in range(3)]
player_turn = 'X'
game_over = False
winner = None

# Draw grid lines
def draw_grid():
    # Background image
    screen.blit(background_img, (0, 0))

    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

# Draw symbols (X or O)
def draw_symbols():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * 200 + 100), int(row * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + 200 - SPACE), (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)    
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + SPACE), (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_WIDTH)

# Check for a win
def check_win(player):
    # Vertical wins
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    
    # Horizontal wins
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Diagonal wins
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

# Minimax function for AI
def minimax(is_maximizing):
    if check_win('O'):
        return 1
    elif check_win('X'):
        return -1
    elif all(all(cell is not None for cell in row) for row in board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    score = minimax(False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    score = minimax(True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# AI's turn to play
def ai_move():
    best_score = -math.inf
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = 'O'
                score = minimax(False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'

# Display result and buttons
def display_result():
    if winner == 'X':
        text = FONT.render('Player Wins!', True, (255, 0, 0))  # Red color
    elif winner == 'O':
        text = FONT.render('AI Wins!', True, (0, 255, 0))      # Green color
    else:
        text = FONT.render('It\'s a Draw!', True, (0, 0, 255))  # Blue color

    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4))
    
    # Draw buttons
    pygame.draw.rect(screen, (0, 0, 0), (150, 400, 100, 50))
    pygame.draw.rect(screen, (0, 0, 0), (350, 400, 100, 50))

    replay_text = FONT.render('Replay', True, (255, 255, 0))  # Yellow color
    quit_text = FONT.render('Quit', True, (255, 255, 0))      # Yellow color

    screen.blit(replay_text, (160, 410))
    screen.blit(quit_text, (370, 410))


# Handle button click
def handle_buttons(pos):
    x, y = pos
    if 150 <= x <= 250 and 400 <= y <= 450:
        restart_game()
    elif 350 <= x <= 450 and 400 <= y <= 450:
        pygame.quit()
        sys.exit()

# Restart the game
def restart_game():
    global board, player_turn, game_over, winner
    board = [[None for _ in range(3)] for _ in range(3)]
    player_turn = 'X'
    game_over = False
    winner = None

# Main game loop
def game_loop():
    global player_turn, game_over, winner
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]  # x-coordinate of the mouse click
                mouseY = event.pos[1]  # y-coordinate of the mouse click

                clicked_row = mouseY // 200
                clicked_col = mouseX // 200

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player_turn
                    if check_win(player_turn):
                        winner = player_turn
                        game_over = True
                    player_turn = 'O'
                    ai_move()
                    if check_win('O'):
                        winner = 'O'
                        game_over = True
                    player_turn = 'X'

                if all(all(cell is not None for cell in row) for row in board) and winner is None:
                    winner = 'Draw'
                    game_over = True

            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
                handle_buttons(pygame.mouse.get_pos())

        screen.fill(BG_COLOR)
        draw_grid()
        draw_symbols()

        if game_over:
            display_result()

        pygame.display.update()

# Start the game loop
game_loop()

