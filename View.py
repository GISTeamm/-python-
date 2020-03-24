import sys
import time
import pygame
from pygame.locals import *
import blocks

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


    # 画已经落下的方块
    def _draw_game_area(self,screen, game_area):
      if game_area:
         for i, row in enumerate(game_area):
                for j, cell in enumerate(row):
                   if cell != '.':
                       pygame.draw.rect(screen, BLOCK_COLOR, (j * SIZE, i * SIZE, SIZE, SIZE), 0)


    # 画单个方块
    def _draw_block(self,screen, block, offset_x, offset_y, pos_x, pos_y):
      if block:
         for i in range(block.start_pos.Y, block.end_pos.Y + 1):
                for j in range(block.start_pos.X, block.end_pos.X + 1):
                   if block.template[i][j] != '.':
                      pygame.draw.rect(screen, BLOCK_COLOR,
                                      (offset_x + (pos_x + j) * SIZE, offset_y + (pos_y + i) * SIZE, SIZE, SIZE), 0)


    # 画得分等信息
    def _draw_info(self,screen, font, pos_x, font_height, score):
     print_text(screen, font, pos_x, 10, f'得分: ')
     print_text(screen, font, pos_x, 10 + font_height + 6, f'{score}')
     print_text(screen, font, pos_x, 20 + (font_height + 6) * 2, f'速度: ')
     print_text(screen, font, pos_x, 20 + (font_height + 6) * 3, f'{score // 10000}')
     print_text(screen,font,pos_x,30+(font_height+6)*4,f'消除总行数：')
     print_text(screen,font,pos_x,30+(font_height+6)*5,f'{score/100}')
     print_text(screen, font, pos_x,50 + (font_height + 6) * 6, f'下一个：')
