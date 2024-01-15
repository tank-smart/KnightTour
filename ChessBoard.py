import turtle
# import random
# 线宽
LINE_WIDTH = 1
# 格子宽度（包含框宽度）
CELL_WIDTH = 60
# 颜色
BOARD_COLOR = "white"
# 背景色
BG_COLOR = "black"
# 是否在棋盘中填入数字
write_2_cell = False
# 棋盘大小
BOARD_SIZE = 8
CELL_COUNT = BOARD_SIZE * BOARD_SIZE


# 画格子
def draw_cell(draw_pen: turtle.Pen, fill_color: bool):
    t = draw_pen.position()
    h = draw_pen.heading()
    c = draw_pen.fillcolor()
    d = draw_pen.isdown()
    if fill_color is True:
        draw_pen.fillcolor(BOARD_COLOR)
    else:
        draw_pen.fillcolor(BG_COLOR)
    draw_pen.up()
    draw_pen.goto(t[0] - CELL_WIDTH/2, t[1] + CELL_WIDTH / 2)
    draw_pen.setheading(0)
    draw_pen.down()

    draw_pen.begin_fill()
    for _ in range(4):
        draw_pen.forward(CELL_WIDTH)
        draw_pen.right(90)
    draw_pen.end_fill()
    draw_pen.up()
    draw_pen.setposition(t)
    draw_pen.setheading(h)
    draw_pen.fillcolor(c)
    if d:
        draw_pen.down()
        
                
# 设置棋盘
def draw_blank_chess_board(draw_pen: turtle.Pen, board_size):
    global BOARD_SIZE
    BOARD_SIZE = board_size
    turtle.bgcolor(BG_COLOR)
    draw_pen.speed(0)
    draw_pen.pencolor(BOARD_COLOR)
    draw_pen.fillcolor(BOARD_COLOR)
    draw_pen.pensize(LINE_WIDTH)
    draw_pen.hideturtle()
    board_long = BOARD_SIZE * CELL_WIDTH
    start_x = -1 * board_long / 2
    start_y = board_long / 2
    # 画棋框
    draw_pen.up()
    draw_pen.setposition(start_x - LINE_WIDTH, start_y + LINE_WIDTH)
    draw_pen.down()
    for _ in range(4):
        draw_pen.forward(board_long + LINE_WIDTH * 2)
        draw_pen.right(90)
    
    # 画格子
    start_x = start_x + CELL_WIDTH / 2
    start_y = start_y - CELL_WIDTH / 2
    fill_color = False
    draw_pen.up()
    turtle.tracer(0)
    for x in range(BOARD_SIZE):
        draw_pen.setposition(start_x, start_y - CELL_WIDTH * x)
        for y in range(BOARD_SIZE):
            if (x + y) % 2 == 0:
                # 如果x+y是偶数，则格子是涂色格
                fill_color = True 
            else:
                fill_color = False
            # if y != 0:
            #     fill_color = not fill_color
            draw_cell(draw_pen, fill_color)
            draw_pen.forward(CELL_WIDTH)
    draw_pen.down()
    turtle.update()
    # turtle.tracer(1)
    # 标行列号
    for t in range(BOARD_SIZE):
        # 行号
        draw_pen.up()
        # draw_pen.goto(start_x - CELL_WIDTH, 
        #               start_y - (CELL_WIDTH + LINE_WIDTH) * t + CELL_WIDTH)
        draw_pen.goto(start_x - CELL_WIDTH, start_y - CELL_WIDTH * t - 15)
        draw_pen.down()
        # draw_pen.dot(3, "red")
        draw_pen.write(t + 1,
                       font=('Times New Roman', 20, 'bold'),
                       align="center")
        # 列号
        draw_pen.up()
        draw_pen.goto(start_x + CELL_WIDTH * t, start_y + CELL_WIDTH - 15)
        draw_pen.down()
        draw_pen.write(t + 1,
                       font=('Times New Roman', 20, 'bold'),
                       align="center")
    turtle.update()
    return


# 向棋盘格子写入数据，当str2write为None时，则清空格子
def write_str2cell(draw_pen: turtle.Pen, row: int,  col: int,
                   str2write: str = None):
    if write_2_cell:
        fill_color = False
        if (col + row) % 2 == 0:
            # 如果x+y是偶数，则格子是涂色格
            fill_color = True 
        board_long = BOARD_SIZE * CELL_WIDTH
        start_x = -1 * board_long / 2 + CELL_WIDTH / 2
        start_y = board_long / 2 - CELL_WIDTH / 2
        
        # 填入数字
        col = col - 1
        row = row - 1
        
        # 清空格内文字
        draw_pen.up()
        draw_pen.setposition(start_x + col * CELL_WIDTH,
                            start_y - CELL_WIDTH * row)
        draw_pen.down()
        draw_cell(draw_pen, fill_color)
        if str2write is not None:
            # 写入文字
            draw_pen.up()
            draw_pen.setposition(start_x + col * CELL_WIDTH,
                                start_y - CELL_WIDTH * row - 15)
            draw_pen.down()
            if fill_color is True:
                draw_pen.pencolor(BG_COLOR)
            else:
                draw_pen.pencolor(BOARD_COLOR)
            draw_pen.write(str2write,
                        font=('Times New Roman', 20, 'bold'),
                        align="center")
            draw_pen.color = BOARD_COLOR
    turtle.update()
    return


# 骑士跳动规则定义
KNIGHT_JUNMP_RULE = ([-1, 2], [-2, 1], [-2, -1], [-1, -2],
                     [1, -2], [2, -1], [2, 1], [1, 2])

# 骑士跳动，position初始位置int数组（row,col)，direction跳动方向
# direction取1 ~ 8，从0度角开始为1，逆时针旋转
# 跳动成功返回新位置，跳动失败返回None


def knight_jump(position, direction):
    new_position = [0, 0]
    new_position[0] = position[0] + KNIGHT_JUNMP_RULE[direction - 1][0]
    new_position[1] = position[1] + KNIGHT_JUNMP_RULE[direction - 1][1]
    if new_position[0] < 1 or new_position[0] > BOARD_SIZE:
        new_position = None
    else:
        if new_position[1] < 1 or new_position[1] > BOARD_SIZE:
            new_position = None
    return new_position
