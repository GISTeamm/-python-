import sys
import time
import pygame
from pygame.locals import *
import Model_Class_Packs


class House(object):
    SIZE = 30  # 每个小方格大小
    BLOCK_HEIGHT = 25  # 游戏区高度
    BLOCK_WIDTH = 10  # 游戏区宽度
    BORDER_WIDTH = 4  # 游戏区边框宽度
    BORDER_COLOR = (40, 40, 200)  # 游戏区边框颜色
    SCREEN_WIDTH = SIZE * (BLOCK_WIDTH + 5)  # 游戏屏幕的宽
    SCREEN_HEIGHT = SIZE * BLOCK_HEIGHT  # 游戏屏幕的高
    BG_COLOR = (40, 40, 60)  # 背景色
    BLOCK_COLOR = (20, 128, 200)  #
    BLACK = (0, 0, 0)
    RED = (200, 30, 30)  # GAME OVER 的字体颜色

    cur_block = None  # 当前下落方块
    next_block = None  # 下一个方块
    cur_pos_x, cur_pos_y = 0, 0

    game_area = None  # 整个游戏区域
    game_over = True
    start = False  # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0  # 得分
    orispeed = 0.5  # 原始速度
    speed = orispeed  # 当前速度
    pause = False  # 暂停
    last_drop_time = None  # 上次下落时间
    last_press_time = None  # 上次按键时间

    myblocks=Model_Class_Packs.Block()

    def judge(self,pos_x, pos_y, block):
        for _i in range(block.start_pos.Y, block.end_pos.Y + 1):
            if pos_y + block.end_pos.Y >= self.BLOCK_HEIGHT:
                return False
            for _j in range(block.start_pos.X, block.end_pos.X + 1):
                if pos_y + _i >= 0 and block.template[_i][_j] != '.' and self.game_area[pos_y + _i][pos_x + _j] != '.':
                    return False
        return True

    def dock(self):
        for _i in range(self.cur_block.start_pos.Y, self.cur_block.end_pos.Y + 1):
            for _j in range(self.cur_block.start_pos.X, self.cur_block.end_pos.X + 1):
                if self.cur_block.template[_i][_j] != '.':
                    self.game_area[self.cur_pos_y + _i][self.cur_pos_x + _j] = '0'
        if self.cur_pos_y + self.cur_block.start_pos.Y <= 0:
            game_over = True
        else:
            # 计算消除
            remove_idxs = []
            for _i in range(self.cur_block.start_pos.Y, self.cur_block.end_pos.Y + 1):
                if all(_x == '0' for _x in self.game_area[self.cur_pos_y + _i]):
                    remove_idxs.append(self.cur_pos_y + _i)
            if remove_idxs:
                # 计算得分
                remove_count = len(remove_idxs)
                if remove_count == 1:
                    self.score += 100
                elif remove_count == 2:
                    self.score += 300
                elif remove_count == 3:
                    self.score += 700
                elif remove_count == 4:
                    self.score += 1500
                speed = self.orispeed - 0.03 * (self.score // 10000)
                # 消除
                _i = _j = remove_idxs[-1]
                while _i >= 0:
                    while _j in remove_idxs:
                        _j -= 1
                    if _j < 0:
                        self.game_area[_i] = ['.'] * self.BLOCK_WIDTH
                    else:
                        self.game_area[_i] = self.game_area[_j]
                    _i -= 1
                    _j -= 1
            self.cur_block = self.next_block
            self.next_block = self.myblocks.get_block()
            self.cur_pos_x, self.cur_pos_y = (self.BLOCK_WIDTH - self.cur_block.end_pos.X - 1) // 2, -1 - self.cur_block.end_pos.Y


class TerisInterface(object):
    myhouse = House()
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_WIDTH, SIZE, BORDER_WIDTH):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')

        self.font1 = pygame.font.SysFont('SimHei', 24)  # 黑体24
        self.font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
        self.font_pos_x = BLOCK_WIDTH * SIZE + BORDER_WIDTH + 10  # 右侧信息显示区域字体位置的X坐标
        self.gameover_size = self.font2.size('GAME OVER')
        self.font1_height = int(self.font1.size('得分')[1])



        #主循环开始
        while True:
            for self.event in pygame.event.get():
                if self.event.type == QUIT:
                    self.gameExit()
                elif self.event.type == KEYDOWN:
                    if self.event.key == K_RETURN:
                        self.gameReturn()
                    elif self.event.key == K_SPACE:
                        self.gameSuspend()
                    elif self.event.key in (K_w, K_UP):
                        self.rotate()

            if self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_LEFT:
                    self.moveBrickLeft()
                if self.event.key == pygame.K_RIGHT:
                    self.moveBrickRight()
                if self.event.key == pygame.K_DOWN:
                    self.moveBrickDown()

    def gameReturn(self):
        if self.myhouse.game_over:
            self.myhouse.start = True
            self.myhouse.game_over = False
            self.myhouse.score = 0
            self.myhouse.last_drop_time = time.time()
            self.myhouse.last_press_time = time.time()
            self.myhouse.game_area = [['.'] * self.myhouse.BLOCK_WIDTH for _ in range(self.myhouse.BLOCK_HEIGHT)]
            self.myhouse.cur_block = self.myhouse.myblocks.get_block()
            self.myhouse.next_block = self.myhouse.myblocks.get_block()
            self.myhouse.cur_pos_x,self.myhouse.cur_pos_y = (self.myhouse.BLOCK_WIDTH - self.myhouse.cur_block.end_pos.X - 1) // 2, -1 - self.myhouse.cur_block.end_pos.Y

    def gameStart(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_WIDTH, SIZE, BORDER_WIDTH):
        self.__init__(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_WIDTH, SIZE, BORDER_WIDTH)

    def gameSuspend(self):
        if not self.myhouse.game_over:
            self.pause = not self.pause

    def gameExit(self):
        sys.exit()

    def moveBrickLeft(self):
        if not self.myhouse.game_over and not self.myhouse.pause:
            if time.time() - self.myhouse.last_press_time > 0.1:
                last_press_time = time.time()
                if self.myhouse.cur_pos_x > - self.myhouse.cur_block.start_pos.X:
                    if self.myhouse.judge(self.myhouse.cur_pos_x - 1, self.myhouse.cur_pos_y, self.myhouse.cur_block):
                        self.myhouse.cur_pos_x -= 1

    def moveBrickRight(self):
            if not self.myhouse.game_over and not self.pause:
                if time.time() - self.myhouse.last_press_time > 0.1:
                    self.myhouse.last_press_time = time.time()
                    # 不能移除右边框
                    if self.myhouse.cur_pos_x + self.myhouse.cur_block.end_pos.X + 1 < self.myhouse.BLOCK_WIDTH:
                        if self.myhouse.judge(self.myhouse.cur_pos_x + 1, self.myhouse.cur_pos_y, self.myhouse.cur_block):
                            self.myhouse.cur_pos_x += 1

    def moveBrickDown(self):
        if not self.myhouse.game_over and not self.myhouse.pause:
            if time.time() - self.myhouse.last_press_time > 0.1:
                self.myhouse.last_press_time = time.time()
                if not self.myhouse.judge(self.myhouse.cur_pos_x, self.myhouse.cur_pos_y + 1, self.myhouse.cur_block):
                    self.myhouse.dock()
                else:
                    self.myhouse.last_drop_time = time.time()
                    self.myhouse.cur_pos_y += 1


    def rotate(self):
        if 0 <= self.myhouse.cur_pos_x <= self.myhouse.BLOCK_WIDTH - len(self.myhouse.cur_block.template[0]):
            _next_block = self.myhouse.myblocks.get_next_block(self.myhouse.cur_block)
            if self.myhouse.judge(self.myhouse.cur_pos_x, self.myhouse.cur_pos_y, _next_block):
                self.myhouse.cur_block = _next_block

    def editBrick(self):
        pass

    def pattern(self):
        pass