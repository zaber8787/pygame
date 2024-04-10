import pygame
import random
import os

FPS = 60
HEIGHT = 600
WIDTH = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
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
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(
    os.path.join('img', 'bullet.png')).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(
        os.path.join('img', f'rock{i}.png')).convert())
expl_ani = {}
expl_ani['lg'] = []
expl_ani['sm'] = []
expl_ani['player'] = []
for i in range(9):
    expl_img = (pygame.image.load(
        os.path.join('img', f'expl{i}.png')).convert())
    expl_img.set_colorkey(BLACK)
    expl_ani['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_ani['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = (pygame.image.load(
        os.path.join('img', f'player_expl{i}.png')).convert())
    player_expl_img.set_colorkey(BLACK)
    expl_ani['player'].append(player_expl_img)
treasure_img = {}
treasure_img['shield'] = (pygame.image.load(
    os.path.join('img', f'shield.png')).convert())
treasure_img['gun'] = (pygame.image.load(
    os.path.join('img', f'gun.png')).convert())


# load voice
bullet_shoot = pygame.mixer.Sound(
    os.path.join('sound', 'shoot.wav'))
expl_sound = [
    pygame.mixer.Sound(
        os.path.join('sound', 'expl0.wav')),
    pygame.mixer.Sound(
        os.path.join('sound', 'expl1.wav'))
]
die_sound = pygame.mixer.Sound(
    os.path.join('sound', 'rumble.ogg'))
gun_sound = pygame.mixer.Sound(
    os.path.join('sound', 'pow1.wav'))
shield_sound = pygame.mixer.Sound(
    os.path.join('sound', 'pow0.wav'))
pygame.mixer.music.load(os.path.join('sound', 'Sunny.mp3'))
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(-1)
# score board
score = 0
font_name = (os.path.join('NotoSansTC-Bold.ttf'))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surf, text_rect)

# hp


def draw_health(surf, hp, x, y):
    if (hp <= 0):
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_in = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_in)
    pygame.draw.rect(surf, WHITE, outline, 2)

# 物件Sprite


def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '太空生存戰', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '上下左右或WASD操縱飛船，空白鍵發射子彈', 18, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲', 16, WIDTH/2, HEIGHT/4*3)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYUP:
                waiting = False
                return False
    all_sprite = pygame.sprite.Group()
    player = Player()
    all_sprite.add(player)
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    treasures = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT*3/4)
        self.redius = 25
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if (self.gun > 1 and now - self.gun_time > 5000):
            self.gun -= 1
            self.gun_time = now
        if (self.hidden and now - self.hide_time >= 1000):
            self.hidden = False
            self.rect.center = (WIDTH/2, HEIGHT*3/4)
        key = pygame.key.get_pressed()
        if not self.hidden:
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
        if not self.hidden:
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprite.add(bullet)
                bullets.add(bullet)
                bullet_shoot.play()
            else:
                if self.gun == 2:
                    bullet1 = Bullet(self.rect.right, self.rect.centery)
                    all_sprite.add(bullet1)
                    bullets.add(bullet1)
                    bullet_shoot.play()
                    bullet2 = Bullet(self.rect.left, self.rect.centery)
                    all_sprite.add(bullet2)
                    bullets.add(bullet2)
                else:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprite.add(bullet)
                    bullets.add(bullet)
                    bullet_shoot.play()
                    bullet1 = Bullet(self.rect.right, self.rect.centery)
                    all_sprite.add(bullet1)
                    bullets.add(bullet1)
                    bullet_shoot.play()
                    bullet2 = Bullet(self.rect.left, self.rect.centery)
                    all_sprite.add(bullet2)
                    bullets.add(bullet2)

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_ani[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame += 1
            if (self.frame == len(expl_ani[self.size])):
                self.kill()
            else:
                self.image = expl_ani[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Treasure(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = treasure_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if (self.rect.top >= HEIGHT):
            self.kill()


all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
treasures = pygame.sprite.Group()
for i in range(10):
    rock = Rock()
    all_sprite.add(rock)
    rocks.add(rock)

# 遊戲迴圈
show_init = True
running = True
while running:
    if (show_init):
        close = draw_init()
        if close:
            break
        show_init = False
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
    # check if bullet it the rocks
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        if random.random() <= 0.1:
            treasure = Treasure(hit.rect.center)
            all_sprite.add(treasure)
            treasures.add(treasure)
        random.choice(expl_sound).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprite.add(expl)
        score += hit.radius
        rock = Rock()
        all_sprite.add(rock)
        rocks.add(rock)
    # check if player hit the treasure
    hits = pygame.sprite.spritecollide(
        player, treasures, True)
    for hit in hits:
        if (hit.type == 'shield'):
            player.health += 20
            shield_sound.play()
            if (player.health > 100):
                player.health = 100
        elif hit.type == 'gun':
            gun_sound.play()
            player.gunup()
    # check if player it the rocks
    hits = pygame.sprite.spritecollide(
        player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        if (player.health <= 0):
            die = Explosion(player.rect.center, 'player')
            all_sprite.add(die)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
        rock = Rock()
        all_sprite.add(rock)
        rocks.add(rock)
    if (player.lives == 0 and not die.alive()):
        show_init = True

    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprite.draw(screen)
    draw_text(screen, str(round(score)), 18, WIDTH * 1/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH-100, 15)
    pygame.display.update()
pygame.quit()
