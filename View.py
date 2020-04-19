import sys
import time
import pygame
from pygame.locals import *


SIZE = 30  # 每个小方格大小
BLOCK_HEIGHT = 25  # 游戏区高度
BLOCK_WIDTH = 10   # 游戏区宽度
BORDER_WIDTH = 4   # 游戏区边框宽度
BORDER_COLOR = (40, 40, 200)  # 游戏区边框颜色
SCREEN_WIDTH = SIZE * (BLOCK_WIDTH + 5)  # 游戏屏幕的宽
SCREEN_HEIGHT = SIZE * BLOCK_HEIGHT      # 游戏屏幕的高
BG_COLOR = (40, 40, 60)  # 背景色
BLOCK_COLOR = (20, 128, 200)  #
BLACK = (0, 0, 0)
RED = (200, 30, 30)      # GAME OVER 的字体颜色


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
   imgText = font.render(text, True, fcolor)
   screen.blit(imgText, (x, y))

class CView:   #只是完成了可视化层、未完成UI交互层，需要在前面设计交互
  
  # 画背景
    def _draw_background(self,screen):
      # 填充背景色
      screen.fill(BG_COLOR)
      # 画游戏区域分隔线
      pygame.draw.line(screen, BORDER_COLOR,
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, 0),
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, SCREEN_HEIGHT), BORDER_WIDTH)

    # 画网格线
    def _draw_gridlines(self,screen):
      # 画网格线 竖线
      for x in range(BLOCK_WIDTH):
          pygame.draw.line(screen, BLACK, (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
      # 画网格线 横线
      for y in range(BLOCK_HEIGHT):
           pygame.draw.line(screen, BLACK, (0, y * SIZE), (BLOCK_WIDTH * SIZE, y * SIZE), 1)


    def _draw_gameon(self,screen):
     _draw_background(screen)
   #将原设计中的菜单选项转化为pygame里的UI交互
    def _draw_UIInterface(self,screen):
         # 填充背景色
        start_ck = pygame.Surface(screen.get_size())    #   充当开始界面的画布

        start_ck = start_ck.convert()

        start_ck.fill(BG_COLOR)  # 蓝色画布1（开始界面用的）

        # 加载各个素材图片 并且赋予变量名
        i1 = pygame.image.load("./images/s1.png")
        i1.convert()
        i11 = pygame.image.load("./images/s2.png")
        i11.convert()

        i2 = pygame.image.load("./images/n2.png")
        i2.convert()
        i21 = pygame.image.load("./images/n1.png")
        i21.convert()

        i3 = pygame.image.load('./images/m2.png')
        i3.convert()
        i31 = pygame.image.load('./images/m1.png')
        i31.convert()
        #  以下为选择开始界面鼠标检测结构。
        n1 = True
        while n1:
          #clock.tick(30)
          buttons = pygame.mouse.get_pressed()
          x1, y1 = pygame.mouse.get_pos()
          if x1 >= 100 and x1 <= 500 and y1 >= 100 and y1 <=150:
            start_ck.blit(i11, (100, 100))
            if buttons[0]:
               n1 = False

          elif x1 >= 100 and x1 <= 500 and y1 >= 200 and y1 <=250:
             start_ck.blit(i21, (100, 200))
             if buttons[0]:
               pygame.quit()
               exit()

          elif x1 >= 100 and x1 <= 500 and y1 >= 300 and y1 <=350:
             start_ck.blit(i31, (100, 300))
          else:
             start_ck.blit(i1, (100, 100))
             start_ck.blit(i2, (100, 200))
             start_ck.blit(i3, (100, 300))


          screen.blit(start_ck,(0,0))
          pygame.display.update()

        # 下面是监听退出动作

         # 监听事件
          for event in pygame.event.get():

            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
              print("游戏退出...")

               # quit 卸载所有的模块
              pygame.quit()

               # exit() 直接终止当前正在执行的程序
              exit()
        screen.blit(screen,(0,0))
        pygame.display.update()
        #  以下可以写第一关的代码了
        n2 = True
        while n2:
         #clock.tick(30)

         _draw_background(self,screen)
         _draw_gridlines(self,screen)
        


         for event in pygame.event.get():

        # 判断事件类型是否是退出事件
           if event.type == pygame.QUIT:
              print("游戏退出...")

              # quit 卸载所有的模块
              pygame.quit()

            # exit() 直接终止当前正在执行的程序
              exit()

