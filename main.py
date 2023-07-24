import pygame as pg
import numpy as np
import time
import sys
import gthread

HEIGHT = 60
WIDTH = 60
UNITWIDTH = 6

land = np.zeros((HEIGHT, WIDTH))


# 检测输入坐标周围的8个区域，返回该坐标的生或死
# 1. 每个细胞的状态由该细胞及周围八个细胞上一次的状态所决定；
# 2. 如果一个细胞周围有3个细胞为生，则该细胞为生；
# 3. 如果一个细胞周围有2个细胞为生，则该细胞的生死状态保持不变；
# 4. 在其它情况下，该细胞为死；
# 遍历累加 
def search_surround(p):
    global land
    # 判断周围区域累加和
    add = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if p[0] + i < 0 or p[0] + i >= HEIGHT:
                continue
            if p[1] + j < 0 or p[1] + j >= WIDTH:
                continue
            if i == j and i == 0:
                continue
            add += land[p[0] + i][p[1] + j]
    # print(add)
    # 根据细胞本身状态返回不同的结果 生1 死0
    if add == 3: # (1)
        return 1
    elif add == 2: # (2)
        return land[p[0]][p[1]]
    
    # print("出错")
    return 0

def display():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if land[i][j] == 1:
                print('*', end=' ')
            else:
                print(' ', end=' ')
        print()

def land_init():
    # 随机
    for i in range(HEIGHT):
        for j in range(WIDTH):
            land[i][j] = int(2*np.random.random())
    





if __name__ == '__main__':
    
    # 初始化
    land_init()
    # 初始化游戏各项数据
    # game_data = game_init()
    pg.init()
    screen = pg.display.set_mode((500, 400)) # 画板对象
    # 根据初始化参数，开启游戏进程
    game_thread = gthread.Gthread(land, screen, HEIGHT, WIDTH, UNITWIDTH)
    game_thread.setDaemon(True) # 设定为守护进程，主进程结束后，子进程自动结束运行
    game_thread.start()
    
    
    pg.display.set_caption("Life game V1.0")

    # display()
    # while True:
    #     result = np.zeros((HEIGHT, WIDTH))
    #     # 搜索
    #     for i in range(HEIGHT):
    #         for j in range(WIDTH):
    #             result[i][j] = search_surround((i, j))
    #             # land[i][j] = search_surround((i, j))
    #     # 执行
    #     land = result

    #     print()
    #     display()
    #     time.sleep(0.2)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game_thread.pause()
                
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                y, x = int((pos[0])/UNITWIDTH), int((pos[1])/UNITWIDTH) # 获取棋子系统坐标
                if x<0 or y<0 or x>=HEIGHT or y>=WIDTH:
                    continue
                game_thread.set_life((y, x))
                game_thread.display()
                game_thread.resume()
            elif event.type == pg.MOUSEMOTION:
                if pg.mouse.get_pressed()[0]==1:
                    pos = pg.mouse.get_pos()
                    y, x = int((pos[0])/UNITWIDTH), int((pos[1])/UNITWIDTH) # 获取棋子系统坐标
                    if x<0 or y<0 or x>=HEIGHT or y>=WIDTH:
                        continue
                    game_thread.set_life((y, x))
                    game_thread.display()


