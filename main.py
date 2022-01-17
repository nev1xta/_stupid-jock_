import pygame
from ball import Ball
from random import randint

pygame.init()
lvl = 0
pygame.time.set_timer(pygame.USEREVENT, 1000)
second = 0
blindness_stopin = 60
drop_ball = False
drop_ball2 = False
timer = 30

W, H = 1000, 650
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('STUPID JOCK')

f = open('progress.txt', 'r', encoding='utf-8')
progress = f.read().split()
f.close()

menu_bg = pygame.image.load('images/menu_bg.png')
menu_bg = pygame.transform.scale(menu_bg, (1000, 650))

jock = pygame.image.load('images/jock.png').convert_alpha()
hand = pygame.image.load('images/hand.png')
telega = jock
red_bg = pygame.image.load("images/red_bg.png")
blue_bg = pygame.image.load("images/blue_bg.png")
bg = red_bg
t_rect = telega.get_rect(centerx=W // 2, bottom=H)

clock = pygame.time.Clock()
FPS = 60
calories_score = 0
power_score = 0
health = 3
health_img = pygame.image.load('images/heart.png')

eating = [pygame.image.load('images/jock.png'), pygame.image.load('images/jock2.png'),
          pygame.image.load('images/jock3.png'), pygame.image.load('images/jock4.png'),
          pygame.image.load('images/jock5.png'), pygame.image.load('images/jock4.png'),
          pygame.image.load('images/jock3.png'), pygame.image.load('images/jock2.png'),
          pygame.image.load('images/jock1.png'), pygame.image.load('images/jock.png')]
animCount = 0
eating_start = False

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


class Button:
    def __init__(self, width, height, inactive_color, active_color, font_size=30):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.font_size = font_size

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(sc, self.active_color, (x, y, self.width, self.height))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if action is not None:
                        action()
        else:
            pygame.draw.rect(sc, self.inactive_color, (x, y, self.width, self.height))
        print_text(message, x + 10, y + 10, font_size=self.font_size, font_color=(0, 0, 0))


def show_menu():
    global menu_bg, bg, timer, health, calories_score, power_score, second, telega
    show = True

    start_btn = Button(400, 100, (25, 130, 10), (20, 100, 10), font_size=75)
    quit_btn = Button(335, 100, (25, 130, 10), (20, 100, 10), font_size=75)
    health = 3
    calories_score = 0
    power_score = 0
    telega = hand
    for i in eats:
        i.kill()
    for i in training_facils:
        i.kill()
    bg = red_bg
    timer = 30
    second = 0

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        sc.blit(menu_bg, ((0, 0), (1000, 650)))
        start_btn.draw(x=300, y=200, message='start game', action=level_selection)
        quit_btn.draw(x=333, y=350, message='exit game', action=quit)
        pygame.display.update()


def level_selection():
    global menu_bg
    show_level = True

    level1_btn = Button(175, 75, (25, 130, 10), (20, 100, 10), font_size=50)
    level2_btn = Button(175, 75, (25, 130, 10), (20, 100, 10), font_size=50)
    level3_btn = Button(175, 75, (25, 130, 10), (20, 100, 10), font_size=50)
    quit_btn = Button(115, 75, (25, 130, 10), (20, 100, 10), font_size=50)

    while show_level:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        sc.blit(menu_bg, ((0, 0), (1000, 650)))
        level1_btn.draw(x=412, y=100, message='level1', action=start_level1)
        level2_btn.draw(x=412, y=200, message='level2', action=start_level2)
        level3_btn.draw(x=412, y=300, message='level3', action=start_level3)
        quit_btn.draw(x=442, y=400, message='back', action=show_menu)
        pygame.display.update()


def start_level1():
    global lvl, telega
    telega = jock
    lvl = 1
    start_game()


def start_level2():
    global lvl, progress, telega
    telega = jock
    if int(progress[0]) == 1:
        lvl = 2
        start_game()


def start_level3():
    global lvl, progress, telega
    telega = jock
    if int(progress[1]) == 1:
        lvl = 3
        start_game()


def createEat(group):
    indx = randint(0, len(eats_surf) - 1)
    x = randint(165, 650 - 20)
    speed = randint(1, 4)

    return Ball(x, speed, eats_surf[indx], eats_data[indx]['score'], group)


def createTraining_facil(group):
    indx = randint(0, len(training_facil_surf) - 1)
    x = randint(165, 650 - 20)
    speed = randint(1, 4)

    return Ball(x, speed, training_facil_surf[indx], training_facil_data[indx]['score'], group)


createEat(eats)
speed = 10


def collideeats():
    global calories_score, health, eating_start
    for ball in eats:
        if t_rect.collidepoint(ball.rect.center):
            if bg == red_bg:
                calories_score += ball.score
                eating_start = True
            else:
                if not check_health():
                    print('game over')
            ball.kill()


def collideTraining_facils():
    global calories_score, health, power_score, bg, red_bg, blue_bg
    for ball in training_facils:
        if t_rect.collidepoint(ball.rect.center):
            if bg == blue_bg:
                calories_score -= 50
                power_score += ball.score
            else:
                if not check_health():
                    print('game over')
            ball.kill()


def print_text(mesage, x, y, font_color=(94, 138, 14), font_type='Fonts/Samson.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(mesage, True, font_color)
    sc.blit(text, (x, y))


def game_over(bool):
    global health, calories_score, eats, training_facils, power_score, bg, red_bg, timer, second, telega
    if bool:
        Pause()
    else:
        Pause()
        health = 3
        calories_score = 0
        power_score = 0
        telega = jock
        for i in eats:
            i.kill()
        for i in training_facils:
            i.kill()
        bg = red_bg
        timer = 30
        second = 0


pause = False


def Pause():
    global pause
    pause = True
    while pause:
        keep_playing_btn = Button(140, 50, (25, 130, 10), (20, 100, 10), font_size=30)
        keep_playing_btn.draw(x=320, y=200, message='continue', action=stop_pause)

        exit_to_menu_btn = Button(185, 50, (25, 130, 10), (20, 100, 10), font_size=30)
        exit_to_menu_btn.draw(x=300, y=275, message='exit to menu', action=show_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
        clock.tick(20)


def Win():
    global health, calories_score, power_score, bg, timer, lvl, progress, second, telega
    win = True
    if lvl == 1:
        progress[0] = '1'
        f = open('progress.txt', 'w', encoding='utf-8')
        f.write('\n'.join(progress))
        f.close()
    elif lvl == 2:
        progress[1] = '1'
        f = open('progress.txt', 'w', encoding='utf-8')
        f.write('\n'.join(progress))
        f.close()
    health = 3
    calories_score = 0
    power_score = 0
    telega = jock
    for i in eats:
        i.kill()
    for i in training_facils:
        i.kill()
    bg = red_bg
    timer = 30
    second = 0
    while win:
        print_text(mesage='you won', x=320, y=150)
        if lvl < 3:
            next_lvl_btn = Button(140, 50, (25, 130, 10), (20, 100, 10), font_size=30)
            next_lvl_btn.draw(x=320, y=200, message='next lvl', action=next_lvl)

        exit_to_menu_btn = Button(185, 50, (25, 130, 10), (20, 100, 10), font_size=30)
        exit_to_menu_btn.draw(x=300, y=275, message='exit to menu', action=show_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
        clock.tick(20)


def next_lvl():
    global lvl, progress, telega
    telega = jock
    if lvl == 1:
        if int(progress[0]) == 1:
            lvl += 1
            start_game()
    elif lvl == 2:
        if int(progress[1]) == 1:
            lvl += 1
            start_game()


def stop_pause():
    global pause
    pause = False


def show_health():
    global health
    x = 680
    show = 0
    while health != show:
        sc.blit(health_img, (x, 600))
        x += 45
        show += 1


def check_health():
    global health
    health -= 1
    if health == 0:
        game_over(bool=False)
        return False
    return True


def start_game():
    global second, timer, drop_ball, drop_ball2, bg, blindness_stopin,\
        animCount, eating, eating_start, lvl, telega, jock
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                second += 1
                timer -= 1
                drop_ball = True
                drop_ball2 = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            t_rect.x -= speed
            if t_rect.x < 150:
                t_rect.x = 150

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            t_rect.x += speed
            if t_rect.x > 650 - t_rect.width:
                t_rect.x = 650 - t_rect.width

        if keys[pygame.K_ESCAPE]:
            game_over(True)

        if second % 2 == 0 and drop_ball and bg == red_bg:
            createEat(eats)
            drop_ball = False

        elif second % 2 == 0 and drop_ball and bg == blue_bg:
            createTraining_facil(training_facils)
            drop_ball = False

        if second % 4 == 0 and drop_ball2 and bg == blue_bg:
            createEat(eats)
            drop_ball2 = False

        elif second % 4 == 0 and drop_ball2 and bg == red_bg:
            createTraining_facil(training_facils)
            drop_ball2 = False

        if second % 30 == 0 and second > 0 and bg == red_bg:
            blindness_stopin -= 1
            print(blindness_stopin)
            if blindness_stopin == 7:
                bg = blue_bg
                telega = hand
                blindness_stopin = 60
                timer = 30
                second = 0
        elif second % 30 == 0 and second > 0 and bg == blue_bg:
            blindness_stopin -= 1
            print(blindness_stopin)
            if blindness_stopin == 7:
                bg = red_bg
                telega = jock
                blindness_stopin = 60
                timer = 30
                second = 0
        if calories_score < 0:
            game_over(bool=False)

        sc.blit(bg, (0, 0))
        eats.draw(sc)
        training_facils.draw(sc)
        print_text(str(timer), 370, 15)
        print_text(str(calories_score), 685, 170)
        print_text(str(power_score), 685, 290)
        if animCount + 1 >= 60:
            animCount = 0
            eating_start = False
        if not eating_start:
            sc.blit(telega, t_rect)
        elif eating_start:
            sc.blit(eating[animCount // 6], t_rect)
            animCount += 1
        print_text(mesage='level' + str(lvl), x=160, y=15)
        print_text(mesage='power:', x=670, y=230, font_size=50, font_color=(0, 0, 0))
        print_text(mesage='kcal:', x=670, y=105, font_size=50, font_color=(0, 0, 0))
        print_text(mesage='SCORE', x=660, y=15, font_size=75, font_color=(0, 0, 0))
        print_text(mesage='mission', x=670, y=360, font_size=50, font_color=(0, 0, 0))
        if lvl == 1:
            print_text(mesage='kcal-2500', x=670, y=410, font_size=30)
        if lvl == 2:
            print_text(mesage='power-2500', x=670, y=410, font_size=30)
        if lvl == 3:
            print_text(mesage='kcal-1000', x=670, y=410, font_size=30)
            print_text(mesage='power-2500', x=670, y=440, font_size=30)

        show_health()
        pygame.display.update()
        clock.tick(FPS)
        eats.update(H)
        training_facils.update(H)
        collideeats()
        collideTraining_facils()

        if lvl == 1 and calories_score >= 2500:
            Win()
        elif lvl == 2 and power_score >= 2500:
            Win()
        elif lvl == 3 and calories_score >= 1000 and power_score >= 2500:
            Win()


show_menu()
start_game()
