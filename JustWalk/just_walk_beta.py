import pygame
import csv
import time
import random
from finding import button_v2

pygame.mixer.init()
pygame.font.init()
pygame.font.init()
win_x = 800
win_y = 500
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Just Walk v2.0(under development)")
jump_song = pygame.mixer.Sound("Data/sound/jump.wav")
row = 10
col = 150
gravity = 0.75
vel_y = 0
start_t2 = time.time()
photo = pygame.image.load("Data/img/shooting_and_working.png").convert_alpha()
motion = pygame.image.load("Data/img/walking_frames.png").convert_alpha()
font = pygame.font.SysFont("Georgia", 40)
animation_list = []
animation_step = [5, 5, 8, 7, 5, 5]
# 0 fire left 1 fire right
# action 2(walking to left),3(walking to right),
# 4(stand by left),5(stand by right)
# 6 dead face to left
# 7 dead face to right
frame = 0
action = 5
step = 0
cool_down = 0.07
start_time = time.time()
frame_size = 40
frame_size1 = 33
move_left = False
move_right = False
size = win_y // row
world_data = []
temp = []
rect_data = []
scale = 1.3
# back_ground section
back_list = []
kill_count = 0
font1 = pygame.font.SysFont("Georgia", 20)
background = pygame.image.load("Data/Background/sky_cloud.png").convert_alpha()
mountain = pygame.image.load("Data/Background/mountain.png").convert_alpha()
forest = pygame.image.load('Data/Background/pine1.png').convert_alpha()
forest1 = pygame.image.load('Data/Background/pine2.png').convert_alpha()
start_img = pygame.image.load("Data/main_menu/R.png").convert_alpha()
start_button = button_v2(win_x // 2 - (320 / 2), win_y // 2 - (170 / 2), 320, 100, start_img, "white")
bg = background.get_rect()
for x in range(6):
    rect = pygame.Rect(bg.x + (bg.width * x) - bg.width, bg.y, bg.width, bg.height)
    temp.append(rect)
back_list.append(temp)
temp = []
for x in range(6):
    rect = pygame.Rect(bg.x + (bg.width * x), bg.y + 30, bg.width, bg.height)
    temp.append(rect)
back_list.append(temp)

temp = []
for x in range(6):
    rect = pygame.Rect(bg.x + (bg.width * x), bg.y + 50, bg.width, bg.height)
    temp.append(rect)
back_list.append(temp)

temp = []
for x in range(6):
    rect = pygame.Rect(bg.x + (bg.width * x), bg.y + 100, bg.width, bg.height)
    temp.append(rect)
back_list.append(temp)

img_list = []
deco_list = []
player_health = pygame.Rect(10, 10, 200, 30)
back_health = pygame.Rect(10, 10, 200, 30)
test = pygame.Rect(0, 0, size, win_y)
test2 = pygame.Rect(-(-148 * size) - 800, 0, size, win_y)

# bot
bot = pygame.Rect(size * 15, 0, 50, 50)
for x in range(21):
    img = pygame.image.load(f"Data/tile/{x}.png").convert_alpha()
    img_set = pygame.transform.scale(img, (size, size))
    img_list.append(img_set)
for x in range(col):
    r = [-1] * col
    world_data.append(r)

jump_limit = 0
jump = False
scroll = 0
vic = False
run = True
fire_right = False
fire_left = False

# player
player = pygame.Rect(100, 0, size, size)
bullet_range = pygame.Rect(player.x, player.y, 168, 9)
# bot
bot_action = 0  # 0 rest_right , 1 go right, 2 go left,3 rest_left, 4 attack to right 5 attack to left
# 6 dead face to right 7 dead face to left
bot_f = 0
temp_bot = []
bot_frame = []
bot_list = []
count = 0
# initialize bots
for x in range(5):
    rect = pygame.Rect(random.randint(size, size * 100), -100, size, size)
    a = 0  # action
    botx = 0
    boty = 0
    alive = True
    t = [rect, a, botx, boty, alive]  # bot
    count += 1
    bot_list.append(t)

for x in range(1, 8):
    img = pygame.image.load(f"Data/zombie_animatiion/idle/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (size * scale, size * scale))
    img.set_colorkey("white")
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []
for x in range(1, 8):
    img = pygame.image.load(f"Data/zombie_animatiion/walk/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (size * scale, size * scale))
    img.set_colorkey("white")
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []
for x in bot_frame[1]:
    img = pygame.transform.flip(x, True, False)
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []
for x in bot_frame[0]:
    img = pygame.transform.flip(x, True, False)
    temp_bot.append(img)
bot_frame.append(temp_bot)

temp_bot = []
for x in range(1, 8):
    img = pygame.image.load(f"Data/zombie_animatiion/attack/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (size * scale, size * scale))
    img.set_colorkey("white")
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []
for x in bot_frame[4]:
    img = pygame.transform.flip(x, True, False)
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []
for x in range(1, 8):
    img = pygame.image.load(f"Data/zombie_animatiion/dead/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (size * scale, size * scale))
    img.set_colorkey("white")
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []
for x in bot_frame[6]:
    img = pygame.transform.flip(x, True, False)
    temp_bot.append(img)
bot_frame.append(temp_bot)
temp_bot = []


def animation_engine(screen_width, screen_height, sheet, frame, scale):
    screen = pygame.Surface((screen_width, screen_height))
    screen.fill("green")
    screen.blit(sheet, (0, 0), (screen_width * frame, 0, screen_width, screen_height))
    screen = pygame.transform.scale(screen, (screen_width * scale + 1, screen_height * scale - 8.4))
    screen.set_colorkey("white")
    return screen


for index, animation in enumerate(animation_step):
    temp_list = []
    if index > 1:
        step = 0
        photo = motion
        frame_size = 25
        if index == 3:
            step = 8
        if index == 4:
            step = 15
        if index == 5:
            step = 20

    for x in range(animation):
        temp_list.append(animation_engine(frame_size, frame_size1, photo, step, 2))
        step += 1
    animation_list.append(temp_list)

temp = []
for x in range(1, 9):
    img = pygame.image.load(f"Data/player_death/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (img.width * 2, img.height * 2))
    img.set_colorkey("white")
    temp.append(img)
animation_list.append(temp)
temp = []
for x in animation_list[6]:
    x = pygame.transform.flip(x, True, False)
    temp.append(x)
animation_list.append(temp)


def game_phy(r):
    global jump, vel_y, jump_limit
    dy = 0
    dx = 0
    if move_right and r.x <= win_x - r.width:
        dx = 4
    if action == 1 or action == 3:
        bullet_range.topleft = r.topright
    if move_left and r.x >= 0:
        dx = -4
    if action == 0 or action == 2:
        bullet_range.topright = r.topleft
    if jump:
        vel_y = -15
        jump_song.play()
        jump = False
        # gravity
    vel_y += gravity
    # if bot.x != r.x  and bot.x - r.width> r.x:
    # dx_bot = -3
    # elif bot.x != r.x  and bot.x + r.width< r.x:
    # dx_bot = 3
    # limit is not necressary
    if vel_y > 10:
        vel_y = 10
    dy += vel_y

    for x in rect_data:
        if x[1].colliderect(r.x + dx + scroll, r.y, r.width, r.height):
            dx = 0
            print("!")
        if x[1].colliderect(r.x + scroll, r.y + dy, r.width, r.height):
            # under the block (jumping)
            if vel_y < 0:
                vel_y = 0
                dy = x[1].bottom - r.top

            # normal land collision
            elif vel_y >= 0:
                vel_y = 0
                dy = x[1].top - r.bottom

        if x[1].colliderect(r.x, r.bottom, r.width, r.height):
            jump_limit = 0

    r.y += dy
    r.x += dx + scroll
    bullet_range.y = player.y + 20

# test.x = -((-148 * size) + 800)
def basic_ai(data):
    # dx_bot = 0
    # dy_bot = 0
    global bot_f, roar, kill_count

    for bot in data:
        # dy_bot += 5
        # gravity

        if bot[-1] == True:
            bot[3] += 5

            if bot[3] >= 20:
                bot[3] = 5
            if player.x + 50 <= bot[0].x and bot[0].x - 300 <= player.x:
                bot[1] = 2
                bot[2] = -2
            elif bot[0].x + 300 >= player.x and player.x - 50 >= bot[0].x:
                bot[1] = 1
                bot[2] = 2
            if bot[0].x - 300 >= player.x and bot[1] == 2:
                bot[1] = 3
                bot[2] = 0
            if bot[0].x + 300 <= player.x and bot[1] == 1:
                bot[1] = 0
                bot[2] = 0
            # attack
            if bot[1] == 1 and bot[0].colliderect(player):
                bot[1] = 4
                bot[2] = 0

            if bot[1] == 2 and bot[0].colliderect(player):
                bot[1] = 5
                bot[2] = 0
            if bot[0].colliderect(player):
                player_health.width -= 0.1
            # get killed
            if bullet_range.colliderect(bot[0]) and bot[-1] == True:
                if fire_left and bot[0].x < player.x:
                    bot_f = 0

                    bot[-1] = False
                if fire_right and bot[0].x > player.x:
                    bot_f = 0
                    bot[-1] = False
            if bot[0].y > win_y + 70:
                bot[-1] = False
            for tile in rect_data:
                if tile[1].colliderect(bot[0].x, bot[0].y + bot[3], size, size):
                    bot[3] = 0
                if tile[1].colliderect(bot[0].x + bot[2], bot[0].y, size, size):
                    bot[2] = 0
                    bot[3] -= 10
            bot[0].x += scroll + bot[2]
            bot[0].y += bot[3]
        # get killed animation and respawn nearby
        if bot[-1] == False:

            if bot[1] == 1:  # can't write with (or). I don't know why. weakest of python I guest?
                bot[1] = 6
            elif bot[1] == 5:
                bot[1] = 6
            if bot[1] == 2:
                bot[1] = 7
            elif bot[1] == 4:
                bot[1] = 7
            if bot[1] >= 6:
                if bot_f >= 6:
                    bot[1] = 0
                    bot[2] = 0
                    bot[0].x = random.randint(size * 6, bot[0].x + size * 30)
                    bot[0].y = -bot[0].height * 3
                    bot[-1] = True
                    kill_count += 1
            bot[0].x = bot[0].x + scroll


count = 0


# pre set back_ground
def draw():
    # pygame.draw.rect(win,"green",player)
    global scroll, background, back_list, count
    # pygame.draw.rect(win,"red",test)
    # pygame.draw.rect(win,"red",test2)
    # if rect_data[-1][1].x + size * 14 >= 0 and deco_list[-1][1].x + size * 13 >= 0:

    # if move_right and player.x >= win_x // 2 + (size*2):
    # scroll = -5

    # print(test.x)
    # elif move_left and player.x <= win_x //2 - (size * 3):
    # scroll = 5

    # else:
    # scroll = 0

    # win.blit(background,(background.width * x + test.x,0))
    # win.blit(mountain,(background.width * x + test.x,0))
    # win.blit(forest,(background.width * x + test.x,0))
    # win.blit(forest1,(background.width * x + test.x,0))

    if test.x >= (-148 * size) + 800 and move_right and player.x >= win_x // 2:
        scroll = -4

    elif test2.x <= (-(-147 * size) - 800) and move_left and player.x <= win_x // 2:
        scroll = 4

        # print(test2.x,(-(-146 * size) - 800))

    else:
        scroll = 0

    for room, x in enumerate(back_list):
        for y in x:

            if room == 0:
                y.x += scroll * 0.5
                win.blit(background, y)
            elif room == 1:
                y.x += scroll * 0.5
                win.blit(mountain, y)
            elif room == 2:
                y.x += scroll * 0.5
                win.blit(forest, y)
            elif room == 3:
                y.x += scroll
                win.blit(forest1, y)

    test.x += scroll
    test2.x += scroll
    for x in rect_data:
        x[1].x += scroll

        win.blit(x[0], x[1])

    for x in deco_list:
        x[1].x += scroll
        win.blit(x[0], x[1])
    pygame.draw.rect(win, "red", back_health,
                     0,
                     10,
                     10,
                     10,
                     10)
    pygame.draw.rect(win, "green", player_health,
                     0,
                     10,
                     10,
                     10,
                     10)
    # pygame.draw.line(win,"blue",(player.x - size * 3 ,player.y ),(player.x + size * 4,player.y))

    # pygame.draw.rect(win,"blue",bullet_range)
    for x in bot_list:
        # pygame.draw.line(win,"red",(x[0].x,x[0].y),(player.x,player.y))
        win.blit(bot_frame[x[1]][bot_f], (x[0].x, x[0].y - 7, x[0].width, x[0].height))
    if action >= 6:
        win.blit(animation_list[action][frame], (player.x, player.y - 14, player.width, player.height))
    if action < 6:
        win.blit(animation_list[action][frame], player)


def world(data):
    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            if tile >= 0 and tile < 9:
                rect = pygame.Rect((x * size) + scroll, y * size, size, size)
                data = (img_list[tile], rect)
                rect_data.append(data)
            if tile >= 8:
                rect = pygame.Rect((x * size) + scroll, y * size, size, size)
                data = (img_list[tile], rect)
                deco_list.append(data)


def draw_grib_and_tile():
    for x in range(row):
        pygame.draw.line(win, "red", (0, x * size), (win_x, x * size))

    for x in range(col):
        pygame.draw.line(win, "red", (x * size, 0), (x * size, win_y))


player.y = - player.height * 2
with open(f"Data/level/level1byme.csv", newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for x, ro in enumerate(reader):
        for y, tie in enumerate(ro):
            world_data[x][y] = int(tie)
one_time = True
restart = False
clock = pygame.Clock()
temp = world_data
world(world_data)
game_over = " "
bot_cool_down = 0.1
s = time.time()
start = False
bg_sound = pygame.mixer.Sound("Data/sound/pixel-run-206007.mp3")
bg_sound.set_volume(0.033)
bg_sound.play(-1)
gun_shoot = pygame.mixer.Sound("Data/sound/single-pistol-gunshot-32-101873 (mp3cut.net).mp3")
gun_shoot.set_volume(0.01)

while run:
    clock.tick(60)
    if not start :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw()
    if start :

        end_time = time.time()
        e = time.time()

        if player.y >= win_y or player_health.width == 0:
            scroll = 0
            move_left = False
            move_right = False
            fire_left = False
            fire_right = False
            game_over = "              You die \n [press (x) to continue]"

            if player_health.width == 0:
                if action == 0 or action == 3 or action == 5:
                    action = 7
                elif action == 1 or action == 2 or action == 4:
                    action = 6
                cool_down = 0.1
                if frame == 7:
                    cool_down = 100
                    vic = True

        key = pygame.key.get_pressed()
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                run = False
            if eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_e and not vic and not fire_right and not move_right and not move_left and not jump:
                    fire_left = True
                    action = 0
                    frame = 0
                    gun_shoot.play(-2)

                if eve.key == pygame.K_r and not vic and not fire_left and not move_right and not move_left and not jump:
                    fire_right = True
                    action = 1
                    frame = 0
                    gun_shoot.play(-1)

                if eve.key == pygame.K_UP and jump_limit == 0 and not vic and not fire_left and not fire_right:
                    jump = True
                    jump_limit += 1
                if eve.key == pygame.K_LEFT and not move_right and not vic and not fire_left and not fire_right:
                    move_left = True
                    action = 2
                if eve.key == pygame.K_RIGHT and not move_left and not vic and not fire_left and not fire_right:
                    move_right = True
                    action = 3
                if eve.key == pygame.K_x and vic == True:
                    vic = False
                    restart = True

            if eve.type == pygame.KEYUP and not vic:
                if eve.key == pygame.K_LEFT:
                    move_left = False
                    action = 4
                    gun_shoot.stop()
                if eve.key == pygame.K_RIGHT:
                    move_right = False
                    action = 5
                    gun_shoot.stop()
                if eve.key == pygame.K_e:
                    fire_left = False
                    action = 4
                    gun_shoot.stop()
                if eve.key == pygame.K_r:
                    fire_right = False
                    action = 5
                    gun_shoot.stop()

        if restart:

            one_time = True
            rect_data.clear()
            deco_list.clear()
            bot_list.clear()
            world(temp)
            cool_down = 0.07
            test = pygame.Rect(0, 0, size, win_y)
            test2 = pygame.Rect(-(-148 * size) - 800, 0, size, win_y)
            action = 5
            player.x = 0
            player.y = -size * 2
            kill_count = 0

            if one_time:

                for x in range(3):
                    rect = pygame.Rect(random.randint(size, size * 100), -100, size, size)
                    a = 0  # action
                    # face_to = False#False = left/True = right/
                    botx = 0
                    boty = 0
                    alive = True
                    t = [rect, a, botx, boty, alive]  # bot
                    count += 1
                    bot_list.append(t)
                for x in back_list:
                    for c, y in enumerate(x):
                        y.x = bg.width * c

                one_time = False
            player_health.width += 5
            if player_health.width >= 200:
                restart = False
        if end_time - start_time >= cool_down:
            frame += 1
            start_time = end_time
        if e - s >= bot_cool_down:
            bot_f += 1
            s = e
        if frame >= len(animation_list[action]):
            frame = 0

        if bot_f >= len(bot_frame[0]):  # bug later fix or not
            bot_f = 0

        win.fill("black")

        # draw_grib_and_tile()

        if not vic:
            game_over = " "
            game_phy(player)
            basic_ai(bot_list)

        draw()
        win.blit(font.render(f"{game_over}", False, "red").convert_alpha(), (180, 100))
        win.blit(font1.render(f" Killed point : {kill_count}", True, "white").convert_alpha(), (win_x - 160, 10))
    else :
        if start_button.draw(win):
            start = True
        else :
            start = False

    pygame.display.update()
