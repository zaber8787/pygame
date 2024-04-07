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
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("first game")


# load image
background_img = pygame.image.load(
    os.path.join('img', 'background.png')).convert()
player_img = pygame.image.load(
    os.path.join('img', 'player.png')).convert()
bullet_img = pygame.image.load(
    os.path.join('img', 'bullet.png')).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(
        os.path.join('img', f'rock{i}.png')).convert())

# load music
bullet_shoot = pygame.mixer.Sound(
    os.path.join('sound', 'shoot.wav'))
expl_sound = [
    pygame.mixer.Sound(
        os.path.join('sound', 'expl0.wav')),
    pygame.mixer.Sound(
        os.path.join('sound', 'expl1.wav'))
]
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
# score board
score = 0
font_name = pygame.font.match_font('arial')


def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surf, text_rect)

# 物件Sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT*3/4)
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
        bullet_shoot.play()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -00)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.radius = self.rect.width * 0.8 / 2
        self.degree = random.randrange(-3, 3)
        self.sum = 0

    def rotate(self):
        self.sum += self.degree
        self.sum %= 360
        self.image = pygame.transform.rotate(self.image_ori, self.sum)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
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
        random.choice(expl_sound).play()
        score += hit.radius
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
    draw_score(screen, str(round(score)), 18, WIDTH * 1/2, 10)
    pygame.display.update()
pygame.quit()
