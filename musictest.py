# -*- coding = utf-8 -*-
# @Author : 杨航
import pygame
import sys

pygame.init()
pygame.mixer.init()
music_1 = pygame.mixer.Sound('.\\music\\bgm.wav')
music_2 = pygame.mixer.Sound('.\\music\\start.wav')

music_1.play(-1)
print('ssss')
music_2.play()

while True:
    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()
