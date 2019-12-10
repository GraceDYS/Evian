import pygame
import random
import math
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((480, 852))

clock = pygame.time.Clock()

score = 0
font_color = (0, 0, 0)
font = pygame.font.SysFont("arial", 40)


class Sprite:

    def __init__(self, screen, image_path, x, y, w, h):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def display(self):
        self.screen.blit(self.image, self.rect)

bg1 = Sprite(screen, "bg.png", 0, 0, 480, 852)
bg2 = Sprite(screen, "bg.png", 0, -852, 480, 852)
hero = Sprite(screen, "hero.png", 200, 600, 100,  124)

bg_li = [bg1, bg2]
bullet_li = []
enemy_li = []
timer = 0

#移动图片的函数
def moving_background(bg_li):
    bg_li[0].rect.y += 5
    bg_li[1].rect.y += 5

    if bg_li[0].rect.y > 852:
        bg_li[0].rect.y = -852
    if bg_li[1].rect.y > 852:
        bg_li[1].rect.y = -852

    bg_li[0].display()
    bg_li[1].display()

#控制退出游戏
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == KEYDOWN:
            if event.key == K_a:
                hero.rect.x -= 30
            elif event.key == K_d:
                hero.rect.x += 30

    moving_background(bg_li)
    hero.display()
    if timer - math.floor(timer) <= 1 / 30:
        bullet_obj = Sprite(screen, "bullet.png", hero.rect.x + 39, \
                            hero.rect.y - 30, 22, 22)
        bullet_li.append(bullet_obj)


    for bullet in bullet_li:
        bullet.rect.y -= 5
        bullet.display()
        if bullet.rect.y < -22:
            bullet_li.remove(bullet)

    if timer - math.floor(timer) <= 1 / 30:
        enemy_obj = Sprite(screen, "enemy.png", \
                           random.random() * 430, -39, 51, 39)
        enemy_li.append(enemy_obj)

    for enemy in enemy_li:
        enemy.rect.y += 3
        enemy.display()
        if enemy.rect.y > 800:
            enemy_li.remove(enemy)

    for bullet in bullet_li:
        for enemy in enemy_li:
            if bullet.rect.colliderect(enemy.rect):
                bullet_li.remove(bullet)
                enemy_li.remove(enemy)
                score += 10

    textScore = font.render("Score: " + str(score), True, font_color)
    screen.blit(textScore, (0, 0))

    timer += 1 / 30
    clock.tick(30)
    pygame.display.update()
