import pygame, json, os, sys, time, random

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

trampoline = pygame.image.load(f'assets\\skely\\trampoline.png').convert_alpha()
skeleton_normal = pygame.image.load(f'assets\\skely\\skeleton_normal.png').convert_alpha()
skeleton_yipee = pygame.image.load(f'assets\\skely\\skeleton_yipee.png').convert_alpha()

money_grab = pygame.image.load(f'assets\\skely\\money.png').convert_alpha()

skeleton = skeleton_normal

poster_time = 0
poster_frame = 0

def set_poster(frame):
    global poster
    poster = pygame.image.load(f'assets\\skely\\background\\background_{str(frame)}.png').convert()
    poster = pygame.transform.scale(poster, (WIDTH, HEIGHT))

set_poster(poster_frame)

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
DK_Closet_Skeleton_Font = pygame.font.Font('fonts/DK Closet Skeleton.otf', 64)

esc_text_render = DK_Closet_Skeleton_Font.render('Press ESC to leave skely game', True, (0, 0, 0))


track_mixer = pygame.mixer.Channel(4)
sfx_mixer = pygame.mixer.Channel(5)

skely_song = pygame.mixer.Sound('sounds/skely.mp3')
money_sfx = pygame.mixer.Sound('sounds/money.mp3')

track_mixer.set_volume(0.4)
sfx_mixer.set_volume(0.6)

sk_x, sk_y = 200, 100
x_velocity, y_velocity = 0, 0

gravity = 0.03

door_rect = pygame.Rect(550, 30, 90, 420)
trampoline_rect = pygame.Rect(50, 300, 130, 20)
skeleton_rect = pygame.Rect(sk_x, sk_y, 60, 100)

wall_right = pygame.Rect(795, -900, 50, 4800)
wall_left = pygame.Rect(-40, -90, 50, 4800)

die_rect = pygame.Rect(-2900, 600, 5200, 1600)

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

start_fade = False

moneys = {"1":(200, 300)}
money_rects = []

money_rects.append(pygame.Rect(200, 300, 70, 50))

money_add = 0
money = money

ammount = 1

def reload_money_counter():
    global money_text_render
    money_text_render = DK_Closet_Skeleton_Font.render(str(money) + '€', True, (0, 0, 0))

reload_money_counter()

rand_x_y = None

while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    skeleton = skeleton_yipee

    mx, my = pygame.mouse.get_pos()
    trampoline_rect = pygame.Rect(mx - 50, 425, 130, 10)
    skeleton_rect = pygame.Rect(sk_x, sk_y, 60, 100)

    if not track_mixer.get_busy():
        track_mixer.play(skely_song)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save(money_=money)
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not fade_alpha >= 1:
                    save(money_=money)
                    start_fade = True
        if event.type == pygame.MOUSEBUTTONUP:
            for rect in money_rects:
                # pygame.draw.rect(win, (230, 50, 50,), rect)

                #if pygame.Rect.colliderect(skeleton_rect, rect):
                #    money_rects.remove(rect)
                #    sfx_mixer.play(money_sfx)
                #     money += 10

                if rect.collidepoint(pygame.mouse.get_pos()):
                     money_rects.remove(rect)
                     sfx_mixer.play(money_sfx)
                     money += random.randint(3, 11)
                     reload_money_counter()


    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    poster_time += 1 * dt

    if poster_time >= 0.5:
        if poster_frame <= 0:
            poster_time = 0
            
            poster_frame += 1

            set_poster(poster_frame)
        else:
            poster_frame = -1

    if y_velocity <= 0.35:
        y_velocity += gravity * 20 * dt
    else:
        y_velocity += gravity * 5 * dt # counter velocity ._.


    if x_velocity >= 1.5 or x_velocity <= -1.5:
        sk_x += x_velocity * 150 * dt
    else:
        sk_x += x_velocity * 50 * dt

        
    sk_y += y_velocity * 2000 * dt        # gravity B)

    if pygame.Rect.colliderect(skeleton_rect, trampoline_rect):
        skeleton = skeleton_normal
        y_velocity -= gravity * 240 * dt
        x_velocity += 1 * dt

    if pygame.Rect.colliderect(skeleton_rect, wall_right):
        x_velocity -= 20 * dt

    elif pygame.Rect.colliderect(skeleton_rect, wall_left):
        x_velocity += 20 * dt


    if pygame.Rect.colliderect(skeleton_rect, die_rect):
        save(money_=money)
        start_fade = True
        
    win.fill((255,255,255))
    
    win.blit(poster, (0, 0))
    win.blit(trampoline, (mx - 50, 400))

    win.blit(skeleton, (sk_x, sk_y))

    # win.blit(money_grab, (200, 300))

    money_add += 1 * dt

    if money_add >= 1:
        money_add = 0
        ammount += 1

        rand_x_y = (random.randint(20, 700), random.randint(20, 400))

        moneys[str(ammount)] = (rand_x_y[0], rand_x_y[1])

        money_rects.append(pygame.Rect(rand_x_y[0], rand_x_y[1], 70, 50))

    for key in moneys:
        if pygame.Rect(moneys[key][0], moneys[key][1], 70, 50) in money_rects:
            win.blit(money_grab, moneys[key])
    """
    for rect in money_rects:
        # pygame.draw.rect(win, (230, 50, 50,), rect)

        #if pygame.Rect.colliderect(skeleton_rect, rect):
        #    money_rects.remove(rect)
        #    sfx_mixer.play(money_sfx)
        #     money += 10

        if rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                 money_rects.remove(rect)
                 sfx_mixer.play(money_sfx)
                 money += random.randint(3, 11)
                 reload_money_counter()
    """


    # pygame.draw.rect(win, (250, 40, 40), wall_right)
    # pygame.draw.rect(win, (250, 40, 40), wall_left)

    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            pygame.quit()
            os.system('python scripts\\states\\patient_room.py') # fixxx latr

    # win.blit(esc_text_render, (220, 20))
    win.blit(money_text_render, (70, 50))

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)
    
    pygame.display.flip()
