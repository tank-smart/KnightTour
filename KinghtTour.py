import ChessBoard
import turtle
from datetime import datetime


def knight_tour_around(draw_pen: turtle.Pen, start_row, start_col, board_size):
    # 记录开始时间
    start_time = datetime.now()
    # 棋盘矩阵（是否已走过）
    chess_matrix = [[False for i in range(board_size)] for i in range(board_size)]
    # 棋盘矩阵（每个Cell尝试次数）
    cell_tried_count = [[0 for i in range(board_size)] for i in range(board_size)]
    # 初始化步骤堆栈
    # 每找到一个合适的跳跃步骤后入栈，找不到则出栈
    # 堆栈中每一项用一个数组表示
    # 前两位表示跳跃后的位置（row, col)
    # 第三位表示跳到此位置所采用的跳跃方向（1~8），0表示第一个启动位置
    step_list = []
    step_list.append([[start_row, start_col], 0])
    chess_matrix[start_row - 1][start_col - 1] = True
    position = [start_row, start_col]
    direction = 0
    setp_count = 0
    max_step_count = 0
    cell_count = board_size * board_size
    # 标示启动CELL
    ChessBoard.write_str2cell(draw_pen, start_row, start_col, "K")
    while len(step_list) < cell_count and len(step_list) > 0:
        new_direction = direction + 1
        if new_direction <= 8:
            new_position = ChessBoard.knight_jump(position, new_direction)
            setp_count = setp_count + 1
            # 判断是否可找到下一个可跳跃的位置
            if new_position is not None:
                # print("Knight try to jump:" + str(new_position) + " " + str(new_direction))
                # 判断所找到的位置是否曾经到过
                if chess_matrix[new_position[0] - 1][new_position[1] - 1] is False:
                    # 找到了下一个位置，设置标记、并进栈
                    step_list.append([new_position, new_direction])
                    chess_matrix[new_position[0] - 1][new_position[1] - 1] = True
                    cell_tried_count[new_position[0] - 1][new_position[1] - 1] = cell_tried_count[new_position[0] - 1][new_position[1] - 1] + 1
                    # 画入棋盘对应CELL
                    # ChessBoard.write_str2cell(draw_pen, new_position[0],
                    #                new_position[1],
                    #                str(cell_tried_count[new_position[0] - 1][new_position[1] - 1]))
                    ChessBoard.write_str2cell(draw_pen, new_position[0],
                                    new_position[1],
                                    str(len(step_list) - 1))
                    # print(position)
                    # print("Knight jumped to :" + str(new_position) + " " + str(new_direction))                    
                    position = new_position.copy()
                    direction = 0
                else:
                    # print("Cell was jumped:" + str(new_position) + " " + str(new_direction))
                    direction = new_direction
            else:
                direction = new_direction
        else:
            if len(step_list) > max_step_count:
                max_step_count = len(step_list)
            # 所有方向均失败，出栈
            last_step = step_list.pop()
            chess_matrix[last_step[0][0] - 1][last_step[0][1] - 1] = False
            ChessBoard.write_str2cell(draw_pen, last_step[0][0], last_step[0][1], None)
            # print("Go back:" + str(last_step) + "." + 
            #         "Stack length = " + str(len(step_list)))
            direction = last_step[1]
            if len(step_list) > 0:
                # 如果step_list中还有step（未退回到起始位置）
                # 则从step_list中最后一个位置继续尝试
                # 否则，step_list被清空，while循环终止
                position = step_list[-1][0].copy()
    if len(step_list) > 0:
        print("Try to jump %i steps. Successed to find the answer!" % setp_count)
        print(step_list)
        ChessBoard.write_2_cell = True
        i = 0
        while i < cell_count:
            ChessBoard.write_str2cell(draw_pen, step_list[i][0][0],
                            step_list[i][0][1],
                            str(i) if i > 0 else "K")
            i = i + 1
                     
    else:
        print("Try to jump %i steps. But failed to find the answer!" % setp_count)
        print("Max step count = %i." % max_step_count)
    print("Take Time:" + str(datetime.now() - start_time))
    return


def main():
    board_size = 6
    t = turtle.Pen()
    ChessBoard.draw_blank_chess_board(t, board_size)
    knight_tour_around(t, 1, 1, board_size)

    turtle.done()
    turtle.exitonclick()
    turtle.mainloop()


if __name__ == '__main__':
    main()