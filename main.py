import pygame
from ball import Ball
from random import randint

pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 2000)

W, H = 1000, 650
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('STUPID JOCK')


telega = pygame.image.load('images/jock.png').convert_alpha()
bg = pygame.image.load("images/red_bg.png")
t_rect = telega.get_rect(centerx=W//2, bottom=H-5)



clock = pygame.time.Clock()
FPS = 60
game_score = 0
health = 3
health_img = pygame.image.load('images/heart.png')

eats_data = ({'path': 'egg.png', 'score': 100},
              {'path': 'meat.png', 'score': 150},
              {'path': 'soup.png', 'score': 200})


eats_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in eats_data]

eats = pygame.sprite.Group()


def createBall(group):
    indx = randint(0, len(eats_surf)-1)
    x = randint(165, 650-20)

    speed = randint(1, 4)

    return Ball(x, speed, eats_surf[indx], eats_data[indx]['score'], group)


createBall(eats)
speed = 10


def collideeats():
    global game_score, health
    for ball in eats:
        if t_rect.collidepoint(ball.rect.center):

            game_score += ball.score
            ball.kill()
            if not check_health():
                print('game over')


def print_text(mesage, x, y, font_color=(94, 138, 14), font_type='Fonts/Samson.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(mesage, True, font_color)
    sc.blit(text, (x, y))


def game_over(bool):
    global health, game_score, eats
    if bool:
        pause()
    else:
        pause()
        health = 3
        game_score = 0
        for i in eats:
            i.kill()


def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        print_text('Press ENTER to play', 300, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pause = False

        pygame.display.update()
        clock.tick(20)


def show_health():
    global health
    x = 20
    show = 0
    while health != show:
        sc.blit(health_img, (x, 40))
        x += 45
        show += 1


def check_health():
    global health
    health -= 1
    if health == 0:
        game_over(bool=False)
        return False
    return True


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
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        t_rect.x += speed
        if t_rect.x > 650-t_rect.width:
            t_rect.x = 650-t_rect.width
    if keys[pygame.K_ESCAPE]:
        game_over(True)

    sc.blit(bg, (0, 0))
    eats.draw(sc)
    print_text(str(game_score), 20, 10)
    sc.blit(telega, t_rect)
    show_health()
    pygame.display.update()

    clock.tick(FPS)

    eats.update(H)
    collideeats()

