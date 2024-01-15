import ChessBoard
import sys
import pygame
from datetime import datetime
import multiprocessing
import numpy as np

# 骑士跳动规则定义
KNIGHT_JUNMP_RULE = ([-1, 2], [-2, 1], [-2, -1], [-1, -2],
                     [1, -2], [2, -1], [2, 1], [1, 2])

# 骑士跳动，position初始位置int数组（row,col)，direction跳动方向
# direction取1 ~ 8，从0度角开始为1，逆时针旋转
# 跳动成功返回新位置，跳动失败返回None

def knight_jump(position, direction, board_size):
    new_position = [0, 0]
    new_position[0] = position[0] + KNIGHT_JUNMP_RULE[direction - 1][0]
    new_position[1] = position[1] + KNIGHT_JUNMP_RULE[direction - 1][1]
    if new_position[0] < 1 or new_position[0] > board_size:
        new_position = None
    else:
        if new_position[1] < 1 or new_position[1] > board_size:
            new_position = None
    return new_position

def knight_tour_around(start_row, start_col, board_size,
                         result_list):
    # 记录开始时间
    start_time = datetime.now()
    # 棋盘矩阵（是否已走过）
    chess_matrix = \
        [[False for i in range(board_size)] for i in range(board_size)]
    # 棋盘矩阵（每个Cell尝试次数）
    cell_tried_count = \
        [[0 for i in range(board_size)] for i in range(board_size)]
    # 初始化步骤数组
    # 由二维数组组成[步骤总数，3]
    # 前两位表示跳跃后的位置（row, col)，第三位表示跳到此位置所采用的跳跃方向（1~8），0表示第一个启动位置
    # -1表示空
    # 每找到一个合适的跳跃步骤后，在对应步骤的数组位置写入结果，
    # 找不到清空当前数组位置的数据（设为-1）    
    # 将共享内存中的一维数组转换为二维数组
    step_list = np.frombuffer(result_list.get_obj(), dtype="int32").reshape(board_size * board_size, 3)
    step_list[0] = [start_row, start_col, 0]
    chess_matrix[start_row - 1][start_col - 1] = True
    position = [start_row, start_col]
    direction = 0
    setp_count = 0
    max_step_count = 0
    current_step = 0
    cell_count = board_size * board_size
    # 标示启动CELL
    while current_step < cell_count - 1 and current_step >= 0:
        new_direction = direction + 1
        if new_direction <= 8:
            new_position = knight_jump(position, new_direction, board_size)
            setp_count = setp_count + 1
            # 判断是否可找到下一个可跳跃的位置
            if new_position is not None:
                # 判断所找到的位置是否曾经到过
                if not chess_matrix[new_position[0] - 1][new_position[1] - 1]:
                    # 找到了下一个位置，设置标记、并进栈
                    current_step = current_step + 1
                    step_list[current_step] = [new_position[0], new_position[1], new_direction]
                    chess_matrix[new_position[0] - 1][new_position[1] - 1] = \
                        True
                    cell_tried_count[new_position[0] - 1][new_position[1] - 1] \
                        = cell_tried_count[new_position[0] - 1][new_position[1] - 1] + 1
                    position = new_position.copy()
                    direction = 0
                else:
                    direction = new_direction
            else:
                direction = new_direction
        else:
            if current_step > max_step_count:
                max_step_count = current_step
            # 所有方向均失败，出栈
            chess_matrix[step_list[current_step][0] - 1][step_list[current_step][1] - 1] = False
            # print("Go back:" + str(last_step) + "." +
            #         "Stack length = " + str(len(step_list)))
            direction = step_list[current_step][2]
            step_list[current_step] = [-1, -1, -1]
            current_step = current_step - 1
            if current_step >= 0:
                # 如果step_list中还有step（未退回到起始位置）
                # 则从step_list中最后一个位置继续尝试
                # 否则，step_list被清空，while循环终止
                position = [step_list[current_step][0], step_list[current_step][1]] 
    if current_step > 0:
        print("Try to jump %i steps. Successed to find the answer!" % setp_count)
        print(step_list)
    else:
        print("Try to jump %i steps. But failed to find the answer!" % setp_count)
        print("Max step count = %i." % max_step_count + 1)
    print("Take Time:" + str(datetime.now() - start_time))
    return


def main():
    start_row = 1
    strat_col = 1
    board_size = 6
    # 设置屏幕
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 512 + 50 + 8, 512 + 50 + 8  # 设置窗口大小
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Chess Board")  # 设置窗口标题
    ChessBoard.draw_blank_chess_board(screen, board_size)
    pygame.display.flip()  # 更新窗口显示
    # 启动计算进程
    # 创建共享内存
    shared_arr = multiprocessing.Array('i', board_size * board_size * 3)
    for i in range(0, len(shared_arr)):
        shared_arr[i] = -1
    step_list = np.frombuffer(shared_arr.get_obj(), dtype='int32').reshape(board_size * board_size, 3)
    step_list_for_print = []
    tour_process = multiprocessing.Process(target=knight_tour_around,
                                             args=(start_row, strat_col,
                                                   board_size, shared_arr))
    tour_process.start()
    # 循环显示过程结果
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        step_list_for_print = step_list.copy()
        # step_list_for_print = np.frombuffer(step_list_for_print.get_obj(), dtype='int32').reshape(3, board_size * board_size)
        screen.fill(pygame.Color("black"))
        for i in range(len(step_list_for_print)):
                if step_list_for_print[i][0] != -1:
                    for t in range(i + 1, len(step_list_for_print)):
                        if step_list_for_print[i][0] == step_list_for_print[t][0] and\
                            step_list_for_print[i][1] == step_list_for_print[t][1]:
                            print("Error in Setp List! %i" % i )
                            print(step_list_for_print)
        ChessBoard.draw_step_list(screen, step_list_for_print)  # 绘制棋盘
        pygame.display.flip()  # 更新窗口显示


if __name__ == '__main__':
    main()
