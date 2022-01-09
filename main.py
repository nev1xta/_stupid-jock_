import pygame
from ball import Ball
from random import randint


pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)
f = pygame.font.SysFont('arial', 30)

W, H = 1000, 650
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('STUPID JOCK')

telega = pygame.image.load('images/jock.png').convert_alpha()
bg = pygame.image.load("images/red_bg.png")
t_rect = telega.get_rect(centerx=W//2, bottom=H-5)


clock = pygame.time.Clock()
FPS = 60
game_score = 0

eats_data = ({'path': 'egg.png', 'score': 100},
              {'path': 'meat.png', 'score': 150},
              {'path': 'soup.png', 'score': 200})

eats_surf = [pygame.image.load('images/'+data['path']).convert_alpha() for data in eats_data]

eats = pygame.sprite.Group()


def createBall(group):
    indx = randint(0, len(eats_surf)-1)
    x = randint(165, 650-20)
    speed = randint(1, 4)

    return Ball(x, speed, eats_surf[indx], eats_data[indx]['score'], group)


createBall(eats)
speed = 10

def collideeats():
    global game_score
    for ball in eats:
        if t_rect.collidepoint(ball.rect.center):
            game_score += ball.score
            ball.kill()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createBall(eats)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        t_rect.x -= speed
        if t_rect.x < 150:
            t_rect.x = 150
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        t_rect.x += speed
        if t_rect.x > 650-t_rect.width:
            t_rect.x = 650-t_rect.width

    sc.blit(bg, (0, 0))
    eats.draw(sc)
    sc_text = f.render(str(game_score), 1, (94, 138, 14))
    sc.blit(sc_text, (20, 10))
    sc.blit(telega, t_rect)
    pygame.display.update()

    clock.tick(FPS)

    eats.update(H)
    collideeats()
#ааааааааа