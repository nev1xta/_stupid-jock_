import pygame
from ball import Ball
from random import randint

pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 1000)
second = 0
blindness_stopin = 60
drop_ball = False

W, H = 1000, 650
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('STUPID JOCK')


telega = pygame.image.load('images/jock.png').convert_alpha()
red_bg = pygame.image.load("images/red_bg.png")
blue_bg = pygame.image.load("images/blue_bg.png")
bg = red_bg
t_rect = telega.get_rect(centerx=W//2, bottom=H-5)



clock = pygame.time.Clock()
FPS = 60
calories_score = 0
power_score = 0
health = 3
health_img = pygame.image.load('images/heart.png')

eats_data = ({'path': 'egg.png', 'score': 100},
              {'path': 'meat.png', 'score': 150},
              {'path': 'soup.png', 'score': 200})
eats_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in eats_data]
eats = pygame.sprite.Group()


training_facil_data = ({'path': 'expander.png', 'score': 100},
              {'path': 'dumbbell.png', 'score': 150},
              {'path': 'weight.png', 'score': 200})
training_facil_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in training_facil_data]
training_facils = pygame.sprite.Group()


def createEat(group):
    indx = randint(0, len(eats_surf)-1)
    x = randint(165, 650-20)

    speed = randint(1, 4)

    return Ball(x, speed, eats_surf[indx], eats_data[indx]['score'], group)


def createTraining_facil(group):
    indx = randint(0, len(training_facil_surf)-1)
    x = randint(165, 650-20)

    speed = randint(1, 4)

    return Ball(x, speed, training_facil_surf[indx], training_facil_data[indx]['score'], group)


createEat(eats)
speed = 10


def collideeats():
    global calories_score, health
    for ball in eats:
        if t_rect.collidepoint(ball.rect.center):

            calories_score += ball.score
            ball.kill()
            if not check_health():
                print('game over')


def collideTraining_facils():
    global calories_score, health, power_score
    for ball in training_facils:
        if t_rect.collidepoint(ball.rect.center):

            calories_score -= 50
            power_score += ball.score
            ball.kill()
            if not check_health():
                print('game over')


def print_text(mesage, x, y, font_color=(94, 138, 14), font_type='Fonts/Samson.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(mesage, True, font_color)
    sc.blit(text, (x, y))


def game_over(bool):
    global health, calories_score, eats, training_facils, power_score
    if bool:
        pause()
    else:
        pause()
        health = 3
        calories_score = 0
        power_score = 0
        for i in eats:
            i.kill()
        for i in training_facils:
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
            second += 1
            drop_ball = True

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

    if second % 2 == 0 and drop_ball and bg == red_bg:
        createEat(eats)
        drop_ball = False

    elif second % 2 == 0 and drop_ball and bg == blue_bg:
        createTraining_facil(training_facils)
        drop_ball = False

    if second % 30 == 0 and second > 0 and bg == red_bg:
        blindness_stopin -= 1
        if blindness_stopin == 0:
            bg = blue_bg
            blindness_stopin = 60
    elif second % 30 == 0 and second > 0 and bg == blue_bg:
        blindness_stopin -= 1
        if blindness_stopin == 0:
            bg = red_bg
            blindness_stopin = 60

    sc.blit(bg, (0, 0))
    eats.draw(sc)
    training_facils.draw(sc)
    print_text(str(calories_score), 20, 10)
    print_text(str(power_score), 100, 10)
    sc.blit(telega, t_rect)
    show_health()
    pygame.display.update()

    clock.tick(FPS)

    eats.update(H)
    training_facils.update(H)
    collideeats()
    collideTraining_facils()

