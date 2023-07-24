
import pygame as pg
import threading
import time
import numpy as np

class Gthread(threading.Thread):

    HEIGHT = 20
    WIDTH = 20

    flush_speed = 0.01
    land = None
    screen = None
    unit = 6

    def __init__(self, land, screen, height, width, unit):
        super(Gthread, self).__init__()

        self.land = land
        self.screen = screen
        self.HEIGHT = height
        self.WIDTH = width
        self.unit = unit

        self.__flag = threading.Event()
        self.__flag.set()

        self.__running = threading.Event()
        self.__running.set()

    # 图片刷新的操作
    def run(self):

        while True:
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

            # result = np.zeros((self.HEIGHT, self.WIDTH))
            re = {}
            # 搜索
            for i in range(self.HEIGHT):
                for j in range(self.WIDTH):
                    # result[i][j] = self.search_surround((i, j))
                    re[(i, j)] = self.search_surround((i, j))
                    # land[i][j] = search_surround((i, j))
            # 执行
            # self.land = result
            for k, u in re.items():
                self.land[k[0]][k[1]] = u

            self.display()
            time.sleep(self.flush_speed) # 自动更新天数的更新速度，更新速度可以自选  默认一个基础时间，然后X2 X4

    # 刷新屏幕
    def display(self):
        self.screen.fill((100,100,100))

        rect = pg.Rect(0, 0, self.HEIGHT*self.unit, self.WIDTH*self.unit)
        pg.draw.rect(self.screen, (0, 0, 0), rect)









        for i in range(len(self.land)):
            for j in range(len(self.land[i])):  
                if self.land[i][j] == 1:        
                    pg.draw.rect(self.screen, (255, 255, 255), 
                        (i*self.unit,j*self.unit, self.unit, self.unit), 2)
        pg.display.update()
    
    # 检测输入坐标周围的8个区域，返回该坐标的生或死
    # 1. 每个细胞的状态由该细胞及周围八个细胞上一次的状态所决定；
    # 2. 如果一个细胞周围有3个细胞为生，则该细胞为生；
    # 3. 如果一个细胞周围有2个细胞为生，则该细胞的生死状态保持不变；
    # 4. 在其它情况下，该细胞为死；
    # 遍历累加 
    def search_surround(self, p):
        # 判断周围区域累加和
        add = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if p[0] + i < 0 or p[0] + i >= self.HEIGHT:
                    continue
                if p[1] + j < 0 or p[1] + j >= self.WIDTH:
                    continue
                if i == j and i == 0:
                    continue
                add += self.land[p[0] + i][p[1] + j]
        # print(add)
        # 根据细胞本身状态返回不同的结果 生1 死0
        if add == 3: # (1)
            return 1
        elif add == 2: # (2)
            return self.land[p[0]][p[1]]
        
        # print("出错")
        return 0
    
    def set_life(self, p):
        self.land[p[0]][p[1]] = 1

    # 控制器，根据不同的输入值进行相应的操作
    def control(self, param):
        pass

    def pause(self):
        self.__flag.clear()   # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()    # 将线程从暂停状态恢复, 如果已经暂停的话
        self.__running.clear()    # 设置为False  
