import pygame
import random
import os

FPS = 60
HEIGHT = 600
WIDTH = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# 遊戲初始化 & 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("first game")
background_img = pygame.image.load(
    os.path.join('img', 'background.png')).convert()
player_img = pygame.image.load(
    os.path.join('img', 'player.png')).convert()
rock_img = pygame.image.load(
    os.path.join('img', 'rock.png')).convert()
bullet_img = pygame.image.load(
    os.path.join('img', 'bullet.png')).convert()
# 物件Sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.redius = 25

    def update(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_RIGHT] or key[pygame.K_d]):
            self.rect.x += 5
        if (key[pygame.K_LEFT] or key[pygame.K_a]):
            self.rect.x -= 5
        if (key[pygame.K_UP] or key[pygame.K_w]):
            self.rect.y -= 5
        if (key[pygame.K_DOWN] or key[pygame.K_s]):
            self.rect.y += 5
        if (self.rect.right >= WIDTH):
            self.rect.right = WIDTH
        if (self.rect.bottom >= HEIGHT):
            self.rect.bottom = HEIGHT
        if (self.rect.left <= 0):
            self.rect.left = 0
        if (self.rect.top <= 0):
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprite.add(bullet)
        bullets.add(bullet)


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.radius = self.rect.width * 0.8

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top >= HEIGHT or self.rect.left > WIDTH or self.rect.right < 0):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if (self.rect.bottom <= 0):
            self.kill()


all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for i in range(10):
    rock = Rock()
    all_sprite.add(rock)
    rocks.add(rock)

# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # 遊戲更新
    all_sprite.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        rock = Rock()
        all_sprite.add(rock)
        rocks.add(rock)
    hit = pygame.sprite.spritecollide(
        player, rocks, False, pygame.sprite.collide_circle)
    if hit:
        running = False
    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprite.draw(screen)
    pygame.display.update()
pygame.quit()
