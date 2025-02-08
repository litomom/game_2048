import random

def print_board(board):
    """打印当前游戏板"""
    for row in board:
        print('|', end='')
        for num in row:
            print(f' {num} |' if num != 0 else '   |', end='')
        print('\n' + '-' * 21)

def init_board():
    """初始化游戏板"""
    board = [[0 for _ in range(4)] for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    """在随机位置添加新数字（2或4）"""
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4

def move_left(row):
    """向左移动一行"""
    new_row = []
    for num in row:
        if num != 0:
            new_row.append(num)
    while len(new_row) < 4:
        new_row.append(0)
    # 合并相邻相同数字
    for i in range(3):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0
            add_new_tile_flag = True
    # 移动零到行末
    new_row = [num for num in new_row if num != 0] + [0] * new_row.count(0)
    return new_row

def move_right(row):
    """向右移动一行"""
    return move_left(row[::-1])[::-1]

def move_up(board):
    """向上移动"""
    return [move_left(col) for col in zip(*board)]

def move_down(board):
    """向下移动"""
    return [move_right(col) for col in zip(*board)]

def transpose(board):
    """转置矩阵"""
    return [list(row) for row in zip(*board)]

def is_game_over(board):
    """判断游戏是否结束"""
    # 检查是否有空位或相邻相同数字
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
    return True

def main():
    board = init_board()
    while True:
        print_board(board)
        if is_game_over(board):
            print("游戏结束！")
            break
        move = input("请输入方向（↑、↓、←、→）：")
        if move not in ['↑', '↓', '←', '→']:
            print("无效的输入，请重新输入！")
            continue
        old_board = [row.copy() for row in board]
        if move == '←':
            board = [move_left(row) for row in board]
        elif move == '→':
            board = [move_right(row) for row in board]
        elif move == '↑':
            board = transpose([move_left(col) for col in zip(*board)])
        elif move == '↓':
            board = transpose([move_right(col) for col in zip(*board)])
        # 检查是否有移动发生
        if board != old_board:
            add_new_tile(board)
        else:
            print("无法移动，请重新输入方向！")

if __name__ == "__main__":
    main()