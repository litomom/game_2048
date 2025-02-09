import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# 定义屏幕大小和格子大小
WIDTH, HEIGHT = 400, 400
TILE_SIZE = 100
GRID_SIZE = 4

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# 初始化字体
font = pygame.font.SysFont("comicsans", 40)

# 初始化游戏板
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def add_random_tile():
    empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4

def draw_board():
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            color = COLORS.get(value, WHITE)
            pygame.draw.rect(screen, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

def move_left():
    new_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        row = [x for x in board[i] if x != 0]
        new_row = []
        while row:
            if len(row) >= 2 and row[0] == row[1]:
                new_row.append(row[0] * 2)
                row = row[2:]
            else:
                new_row.append(row[0])
                row = row[1:]
        new_row += [0] * (GRID_SIZE - len(new_row))
        new_board[i] = new_row
    return new_board

def move_right():
    new_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        row = [x for x in board[i] if x != 0]
        new_row = []
        while row:
            if len(row) >= 2 and row[-1] == row[-2]:
                new_row.append(row[-1] * 2)
                row = row[:-2]
            else:
                new_row.append(row[-1])
                row = row[:-1]
        new_row = [0] * (GRID_SIZE - len(new_row)) + new_row[::-1]
        new_board[i] = new_row
    return new_board

def move_up():
    new_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for j in range(GRID_SIZE):
        column = [board[i][j] for i in range(GRID_SIZE) if board[i][j] != 0]
        new_column = []
        while column:
            if len(column) >= 2 and column[0] == column[1]:
                new_column.append(column[0] * 2)
                column = column[2:]
            else:
                new_column.append(column[0])
                column = column[1:]
        new_column += [0] * (GRID_SIZE - len(new_column))
        for i in range(GRID_SIZE):
            new_board[i][j] = new_column[i]
    return new_board

def move_down():
    new_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for j in range(GRID_SIZE):
        column = [board[i][j] for i in range(GRID_SIZE) if board[i][j] != 0]
        new_column = []
        while column:
            if len(column) >= 2 and column[-1] == column[-2]:
                new_column.append(column[-1] * 2)
                column = column[:-2]
            else:
                new_column.append(column[-1])
                column = column[:-1]
        new_column = [0] * (GRID_SIZE - len(new_column)) + new_column[::-1]
        for i in range(GRID_SIZE):
            new_board[i][j] = new_column[i]
    return new_board

def check_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return False
            if i < GRID_SIZE - 1 and board[i][j] == board[i + 1][j]:
                return False
            if j < GRID_SIZE - 1 and board[i][j] == board[i][j + 1]:
                return False
    return True

def main():
    global board
    add_random_tile()
    add_random_tile()
    running = True
    while running:
        draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                new_board = None
                if event.key == pygame.K_LEFT:
                    new_board = move_left()
                elif event.key == pygame.K_RIGHT:
                    new_board = move_right()
                elif event.key == pygame.K_UP:
                    new_board = move_up()
                elif event.key == pygame.K_DOWN:
                    new_board = move_down()
                if new_board and new_board != board:
                    board = new_board
                    add_random_tile()
                    if check_game_over():
                        print("Game Over!")
                        running = False

    pygame.quit()

if __name__ == "__main__":
    main()
