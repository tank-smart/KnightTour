import pygame
# import random
# 数字标示宽度（左边及上边）
Num_Mark_Width = 50
# 数字标示字体大小
NUMBER_MARK_SIZE = 36
# 格子宽度（包含框宽度）
CELL_WIDTH = 0
# 浅色格子颜色
LIGHT_COLOR = pygame.Color("white")
# 深色格子颜色
DARK_COLOR = pygame.Color("black")
# 背景色
BG_COLOR = pygame.Color("black")
# 边框色
BORDER_COLOR = pygame.Color("pink")
# 边框宽度
BORDER_WIDTH = 4
# 棋盘大小
BOARD_SIZE = 0
CELL_COUNT = BOARD_SIZE * BOARD_SIZE
# 棋盘尺寸
SQUARE_SIZE = 0


# 设置棋盘
def draw_blank_chess_board(screen: pygame.Surface, board_size):
    global BOARD_SIZE, SQUARE_SIZE, CELL_WIDTH
    BOARD_SIZE = board_size
    SQUARE_SIZE = max(min(screen.get_size()) - Num_Mark_Width - BORDER_WIDTH * 2, 0)
    CELL_WIDTH = SQUARE_SIZE // board_size
    # 画格子
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = Num_Mark_Width + BORDER_WIDTH + col * CELL_WIDTH
            y = Num_Mark_Width + BORDER_WIDTH + row * CELL_WIDTH
            if (row + col) % 2 == 0:
                color = LIGHT_COLOR  # 浅色格子
            else:
                color = DARK_COLOR  # 深色格子
            pygame.draw.rect(screen, color, 
                             pygame.Rect(x, y, CELL_WIDTH, CELL_WIDTH))
    # 画框
    border_rect = pygame.Rect(Num_Mark_Width, Num_Mark_Width,
                              SQUARE_SIZE + BORDER_WIDTH * 2,
                              SQUARE_SIZE + BORDER_WIDTH * 2)
    pygame.draw.rect(screen, BORDER_COLOR, border_rect, BORDER_WIDTH)
    # 标行列号
    # 设置字体和字号
    font = pygame.font.Font(None, NUMBER_MARK_SIZE)
    for t in range(BOARD_SIZE):
        # 创建文本对象
        text = font.render(str(t + 1), True, LIGHT_COLOR)
        # 获取文本对象的矩形
        text_rect = text.get_rect()
        # 行号
        # 设置文本对象的位置
        text_rect.center = (Num_Mark_Width // 2, 
                            Num_Mark_Width + CELL_WIDTH // 2 + t * CELL_WIDTH)
        # 将文本对象绘制到屏幕上
        screen.blit(text, text_rect)
        # 列号
        # 设置文本对象的位置
        text_rect.center = (Num_Mark_Width + CELL_WIDTH // 2 + t * CELL_WIDTH,
                            Num_Mark_Width // 2)
        # 将文本对象绘制到屏幕上
        screen.blit(text, text_rect)
    return


# 向棋盘格子写入数据，当str2write为None时，则清空格子
def write_str2cell(screen: pygame.Surface, row: int,  col: int,
                   str2write: str = None):
    if (row + col) % 2 == 0:
        color = DARK_COLOR  # 深色格子
    else:
        color = LIGHT_COLOR # 浅色格子
    # 填入数字
    col = col - 1
    row = row - 1
    font = pygame.font.Font(None, NUMBER_MARK_SIZE)
    if str2write is not None:
        # 写入文字
        # 创建文本对象
        text = font.render(str2write, True, color)
        # 获取文本对象的矩形
        text_rect = text.get_rect()
        # 设置文本对象的位置
        text_rect.center = (Num_Mark_Width + BORDER_WIDTH + CELL_WIDTH // 2 + col * CELL_WIDTH,
                            Num_Mark_Width + BORDER_WIDTH + CELL_WIDTH // 2 + row * CELL_WIDTH)
        # 将文本对象绘制到屏幕上
        screen.blit(text, text_rect)
    return

def draw_step_list(screen: pygame.Surface, step_list):
    draw_blank_chess_board(screen, BOARD_SIZE)
    if len(step_list) > 0:
        i = 0
        while i < len(step_list):
            write_str2cell(screen, step_list[i][0],
                           step_list[i][1],
                           str(i) if i > 0 else "K")
            i = i + 1
    return
