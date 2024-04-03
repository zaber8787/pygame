import pygame


FPS = 60
HEIGHT = 600
WIDTH = 500
WHITE = (255, 255, 255)

# 遊戲初始化 & 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("first game")

# 物件Sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_RIGHT] or key[pygame.K_d]):
            self.rect.x += 2
        if (key[pygame.K_LEFT] or key[pygame.K_a]):
            self.rect.x -= 2
        if (key[pygame.K_UP] or key[pygame.K_w]):
            self.rect.y -= 2
        if (key[pygame.K_DOWN] or key[pygame.K_s]):
            self.rect.y += 2
        if (self.rect.left > WIDTH):
            self.rect.right = 0
        if (self.rect.top > WIDTH):
            self.rect.bottom = 0
        if (self.rect.right < 0):
            self.rect.left = WIDTH
        if (self.rect.bottom < 0):
            self.rect.top = WIDTH


all_sprite = pygame.sprite.Group()
player = Player()
all_sprite.add(player)


# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 遊戲更新

    all_sprite.update()

    # 畫面顯示
    screen.fill(WHITE)
    all_sprite.draw(screen)
    pygame.display.update()
pygame.quit()
