import pygame, json, os, sys, time

from scripts.shake import *
from scripts.saving import *


pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()
hospital_outside = pygame.image.load('assets\\hospital\\outside.jpg').convert()
hospital_door = pygame.image.load('assets\\door.png').convert_alpha()

flag_pole = pygame.image.load('assets\\flag_pole.png').convert_alpha()


fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

guy_idle_frame = 0
guy_interact_frame = 0

guy_anim = 0
flag_frame = 0

cursor_idle_frame = 0

fade_alpha = 255


def cursor_set(frame):
    global cursor
    cursor = pygame.image.load(f'assets\\cursor\\cursor_{str(frame)}.png').convert_alpha()

def flag_set(frame):
    global flag
    flag = pygame.image.load(f'assets\\animations\\flag\\flag_{str(frame)}.png').convert_alpha()

def guy_set_idle(frame):
    global guy_idle
    guy_idle = pygame.image.load(f'assets\\people\\guy\\idle_{str(frame)}.png').convert()
    guy_idle.set_colorkey((255, 255, 255))
    
def guy_set_interact(frame):
    global guy_interact
    guy_interact = pygame.image.load(f'assets\\people\\guy\\interact_{str(frame)}.png').convert()
    guy_interact.set_colorkey((255, 255, 255))
    
guy_set_idle(guy_idle_frame)
guy_set_interact(guy_interact_frame)
cursor_set(cursor_idle_frame)

flag_set(flag_frame)

hospital_outside = pygame.transform.scale(hospital_outside, (WIDTH, HEIGHT))
hospital_door = pygame.transform.scale(hospital_door, (40, 70))

prev_time = time.time()

guy_idle_time = 0
guy_interact_time = 0

flag_time = 0
between_frame = 0

guy_rect = pygame.Rect(500, 300, 70, 140)
door_rect = pygame.Rect(350, 310, 40, 50)

sfx_mixer = pygame.mixer.Channel(4)

jaket_open = pygame.mixer.Sound('sounds/jaket_open.mp3')

sfx_mixer.set_volume(0.5)
fade_screen.set_alpha(fade_alpha)

start_fade_anim = False
start_fade_door = False

#pygame.mouse.set_visible(False)

save(started_game_=True)

while True:
    dt = time.time() - prev_time
    prev_time = time.time()
    
    win.fill((255,255,255))
    #mx, my = pygame.mouse.get_pos()

    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if guy_rect.collidepoint(pygame.mouse.get_pos()):

            if guy_anim == 0:
                sfx_mixer.play(jaket_open)
            guy_anim = 1

            if event.type == pygame.MOUSEBUTTONUP:
                if guy_interact_frame == 2 and fade_alpha <= 1:
                    start_fade_anim = True

        elif door_rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONUP:
                start_fade_door = True
                start_fade_anim = True
                    
        else:
            guy_anim = 0
            guy_interact_frame = -1

    guy_idle_time += 1 * dt
    guy_interact_time += 1 * dt

    flag_time += 1 * dt

    if guy_anim == 0:
        if guy_idle_time >= 1:
            guy_idle_time = 0
            
            if guy_idle_frame == 0:
                guy_idle_frame = 1
            else:
                guy_idle_frame = 0
                
            guy_set_idle(guy_idle_frame)
    elif guy_anim == 1:
        if guy_interact_time >= 0.1:
            if guy_interact_frame <= 1:

                guy_interact_time = 0
                
                guy_interact_frame += 1
                    
                guy_set_interact(guy_interact_frame)

    if flag_time >= 0.5:
        if flag_frame <= 1:
            flag_time = 0
            
            flag_frame += 1

            flag_set(flag_frame)
        else:
            flag_frame = -1
    
    win.blit(hospital_outside, (0, 0))
    win.blit(hospital_door, (350, 290))

    win.blit(flag_pole, (220, 160))

    win.blit(flag, (220, 160))
    
    
    if guy_anim == 0:
        win.blit(guy_idle, (500, 300))
    elif guy_anim == 1:
        win.blit(guy_interact, (500, 300))
    # pygame.draw.rect(win, (255, 20, 20), door_rect)

    if fade_alpha >= 1 and start_fade_anim == False:
        fade_alpha -= 300 * dt

    if start_fade_anim == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            # pygame.quit()
            if start_fade_door == True:
                import scripts.states.hallway
            else:
                import scripts.states.shop

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)

    win.blit(fade_screen, (0, 0))

    #win.blit(cursor, (mx, my))
    
    clock.tick(144)
    
    pygame.display.flip()
