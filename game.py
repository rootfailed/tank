# -*- coding = utf-8 -*-
# @Author : 杨航


# 导入所需模块
import pygame
import sys

import settings
from map import map

# 使用pygame前必须初始化
pygame.init()
pygame.mixer.init()
# 设置主窗口，本质上是个Surface对象
screen = pygame.display.set_mode((416, 416))
screen_rect = screen.get_rect()
# 设置窗口的标题，即游戏名称
pygame.display.set_caption('坦克大战')
icon = pygame.transform.rotate(pygame.image.load('.\\image\\tank_1.png'), -90)
pygame.display.set_icon(icon)
# 导入音乐素材
music_bgm = pygame.mixer.Sound('.\\music\\bgm.wav')
music_bgm.set_volume(0.2)
music_pause = pygame.mixer.Sound('.\\music\\pause.wav')
music_self_dead = pygame.mixer.Sound('.\\music\\self_dead.wav')
music_shoot = pygame.mixer.Sound('.\\music\\shoot.wav')
music_shoot_iron = pygame.mixer.Sound('.\\music\\shoot_iron.wav')
music_shoot_iron.set_volume(0.4)
music_shoot_brick = pygame.mixer.Sound('.\\music\\shoot_brick.wav')
music_shoot_brick.set_volume(0.5)
music_shoot_on = pygame.mixer.Sound('.\\music\\shoot_on.wav')
music_start = pygame.mixer.Sound('.\\music\\start.wav')
music_upgrade = pygame.mixer.Sound('.\\music\\upgrade.wav')

# 初始化自家坦克
selftank = pygame.sprite.Sprite()
selftank.image = pygame.transform.scale(pygame.image.load('.\\image\\tank_1.png'), (26, 26))
selftank.rect = selftank.image.get_rect()
selftank.rect.midbottom = (160, 416)
Direct = 'UP'
moving = False

# 初始化子弹
bullets_up = pygame.sprite.Group()
bullets_down = pygame.sprite.Group()
bullets_left = pygame.sprite.Group()
bullets_right = pygame.sprite.Group()
bullets = [bullets_up, bullets_down, bullets_left, bullets_right]

# 墙壁
bricks = pygame.sprite.Group()
irons = pygame.sprite.Group()
grasses = pygame.sprite.Group()
rivers = pygame.sprite.Group()
roads = pygame.sprite.Group()

for y in range(26):
    for x in range(26):
        piece = pygame.sprite.Sprite()
        piece.rect = pygame.Rect(16 * y, 16 * x, 16, 16)
        if map[x][y] == 1:
            piece.image = pygame.transform.scale(pygame.image.load('.\\image\\brick.png'), (16, 16))
            bricks.add(piece)
        elif map[x][y] == 2:
            piece.image = pygame.transform.scale(pygame.image.load('.\\image\\iron.png'), (16, 16))
            irons.add(piece)
        elif map[x][y] == 3:
            piece.image = pygame.transform.scale(pygame.image.load('.\\image\\grass.png'), (16, 16))
            grasses.add(piece)
        elif map[x][y] == 4:
            piece.image = pygame.transform.scale(pygame.image.load('.\\image\\river.png'), (16, 16))
            rivers.add(piece)
        elif map[x][y] == 5:
            piece.image = pygame.transform.scale(pygame.image.load('.\\image\\road.png'), (16, 16))
            roads.add(piece)


# 调整绘图方向
def direct(self, directin):
    global Direct
    rect_h = self.get_rect().height
    rect_w = self.get_rect().width
    if directin == Direct:
        return self
    elif directin == 'UP':
        if Direct == 'LEFT':
            self = pygame.transform.rotate(self, -90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'RIGHT':
            self = pygame.transform.rotate(self, 90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'DOWN':
            self = pygame.transform.rotate(self, 180)
        Direct = 'UP'
    elif directin == 'DOWN':
        if Direct == 'LEFT':
            self = pygame.transform.rotate(self, 90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'RIGHT':
            self = pygame.transform.rotate(self, -90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'UP':
            self = pygame.transform.rotate(self, 180)
        Direct = 'DOWN'
    elif directin == 'LEFT':
        if Direct == 'UP':
            self = pygame.transform.rotate(self, 90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'DOWN':
            self = pygame.transform.rotate(self, -90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'RIGHT':
            self = pygame.transform.rotate(self, 180)
        Direct = 'LEFT'
    elif directin == 'RIGHT':
        if Direct == 'UP':
            self = pygame.transform.rotate(self, -90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'DOWN':
            self = pygame.transform.rotate(self, 90)
            self = pygame.transform.scale(self, (rect_h, rect_w))
        if Direct == 'LEFT':
            self = pygame.transform.rotate(self, 180)
        Direct = 'RIGHT'
    return self


music_bgm.play(-1)
music_start.play()
# 主循环
while True:
    # 循环获取事件，监听事件状态
    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 控制坦克
            if event.key == pygame.K_UP:
                selftank.image = direct(selftank.image, 'UP')
                moving = True
            if event.key == pygame.K_DOWN:
                selftank.image = direct(selftank.image, 'DOWN')
                moving = True
            if event.key == pygame.K_LEFT:
                selftank.image = direct(selftank.image, 'LEFT')
                moving = True
            if event.key == pygame.K_RIGHT:
                selftank.image = direct(selftank.image, 'RIGHT')
                moving = True
            # 按空格发射子弹
            if event.key == pygame.K_SPACE and len(bullets_up) + len(bullets_down) + \
                    len(bullets_left) + len(bullets_right) < settings.self_bullet_limit:
                music_shoot.play()
                new_bullet = pygame.sprite.Sprite()
                new_bullet.image = pygame.transform.scale(pygame.image.load('.\\image\\bullet.png'), (5, 8))
                new_bullet.rect = new_bullet.image.get_rect()
                if Direct == 'UP':
                    new_bullet.rect.midbottom = selftank.rect.midtop
                    bullets_up.add(new_bullet)
                if Direct == 'DOWN':
                    new_bullet.image = pygame.transform.rotate(new_bullet.image, 180)
                    new_bullet.rect.midtop = selftank.rect.midbottom
                    bullets_down.add(new_bullet)
                if Direct == 'LEFT':
                    new_bullet.image = pygame.transform.rotate(new_bullet.image, 90)
                    new_bullet.rect = new_bullet.image.get_rect()
                    new_bullet.rect.midright = selftank.rect.midleft
                    bullets_left.add(new_bullet)
                if Direct == 'RIGHT':
                    new_bullet.image = pygame.transform.rotate(new_bullet.image, -90)
                    new_bullet.rect = new_bullet.image.get_rect()
                    new_bullet.rect.midleft = selftank.rect.midright
                    # noinspection PyTypeChecker
                    bullets_right.add(new_bullet)

        # 松开按钮，坦克停止移动
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or pygame.K_DOWN or pygame.K_LEFT or pygame.K_RIGHT:
                moving = False

    # 坦克移动
    if moving:
        if Direct == 'UP' and selftank.rect.top > 0:
            selftank.rect.y -= settings.self_speed
        elif Direct == 'DOWN' and selftank.rect.bottom < screen_rect.bottom:
            selftank.rect.y += settings.self_speed
        elif Direct == 'LEFT' and selftank.rect.left > 0:
            selftank.rect.x -= settings.self_speed
        elif Direct == 'RIGHT' and selftank.rect.right < screen_rect.right:
            selftank.rect.x += settings.self_speed
        # noinspection PyTypeChecker
        if pygame.sprite.spritecollideany(selftank, bricks) \
                or pygame.sprite.spritecollideany(selftank, irons) \
                or pygame.sprite.spritecollideany(selftank, rivers):
            if Direct == 'UP' and selftank.rect.top > 0:
                selftank.rect.y += settings.self_speed
            elif Direct == 'DOWN' and selftank.rect.bottom < screen_rect.bottom:
                selftank.rect.y -= settings.self_speed
            elif Direct == 'LEFT' and selftank.rect.left > 0:
                selftank.rect.x += settings.self_speed
            elif Direct == 'RIGHT' and selftank.rect.right < screen_rect.right:
                selftank.rect.x -= settings.self_speed

    # 绘制图像
    screen.fill(settings.bg_color)

    # 绘制砖块、铁块、河，等下层地图
    bricks.draw(screen)
    irons.draw(screen)
    rivers.draw(screen)
    roads.draw(screen)

    # 绘制坦克
    screen.blit(selftank.image, selftank.rect)

    # 绘制子弹
    if bullets_up is not None:
        for bullet in bullets_up:
            screen.blit(bullet.image, bullet.rect)
            bullet.rect.y -= settings.self_bullet_speed
            if bullet.rect.top < 0:
                bullets_up.remove(bullet)
    if bullets_down is not None:
        for bullet in bullets_down:
            screen.blit(bullet.image, bullet.rect)
            bullet.rect.y += settings.self_bullet_speed
            if bullet.rect.bottom > screen_rect.bottom:
                bullets_down.remove(bullet)
    if bullets_left is not None:
        for bullet in bullets_left:
            screen.blit(bullet.image, bullet.rect)
            bullet.rect.x -= settings.self_bullet_speed
            if bullet.rect.left < 0:
                bullets_left.remove(bullet)
    if bullets_right is not None:
        for bullet in bullets_right:
            screen.blit(bullet.image, bullet.rect)
            bullet.rect.x += settings.self_bullet_speed
            if bullet.rect.right > screen_rect.right:
                bullets_right.remove(bullet)

    # 绘制草等上层地图
    grasses.draw(screen)
    # 判断子弹是否碰撞
    for bullet in bullets:
        if pygame.sprite.groupcollide(bullet, bricks, True, True):
            music_shoot_brick.play()
        if settings.bullet_level < 3:            # 3级子弹特殊效果
            if pygame.sprite.groupcollide(bullet, irons, True, False):
                music_shoot_iron.play()
        else:
            if pygame.sprite.groupcollide(bullet, irons, True, True):
                music_shoot_brick.play()
        pygame.sprite.groupcollide(bullet, grasses, False, False)
        pygame.sprite.groupcollide(bullet, rivers, False, False)

    # 更新屏幕内容
    # print(map)
    pygame.time.delay(10)
    pygame.display.flip()
