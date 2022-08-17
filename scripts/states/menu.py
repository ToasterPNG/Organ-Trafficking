
"""
Buttons:

NEW GAME - only shows up if there is no save file
LOAD GAME - only shows up if there is a save file
SETTINGS
EXIT

"""

# make song for main menu laterrr

import pygame, os, sys, time
import pygame.mixer

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()

WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking - MENU')

clock = pygame.time.Clock()

background = pygame.image.load('assets\\ui\\background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
vignette = pygame.image.load('assets\\golf\\vignette.png')
vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))

cursor_idle_frame = 0
cur_button = None

def cursor_set(frame):
    global cursor
    cursor = pygame.image.load(f'assets\\cursor\\cursor_{str(frame)}.png').convert_alpha()
    cursor = pygame.transform.scale(cursor, (int(cursor.get_width() * 1.5), int(cursor.get_height() * 1.5)))

cursor_set(cursor_idle_frame)

vignette.set_alpha(144)

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 64)
Decaying_Felt_Pen = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
title_render = HighVoltage_Rough_Font.render('Organ Trafficking', True, (0, 0, 0))

with open('save.json', 'r') as save_file:
    save_file = save_file.read()

if started_game == False:
    buttons = ['NEW GAME', 'SETTINGS', 'EXIT']
else:
    buttons = ['CONTINUE', 'SETTINGS', 'EXIT']

def load_buttons():
    global buttons, cur_button

    pos = 150 - len(buttons) * 10
    cur_button = None

    for button in buttons:
        color = (0, 0, 0)

        button_render = Decaying_Felt_Pen.render(button, True, (0, 0, 0))

        pos += 65

        button_rect = button_render.get_rect()
        button_rect.x = WIDTH // 2 - Decaying_Felt_Pen.size(button)[0] // 2
        button_rect.y = pos

        #pygame.draw.rect(win, (255, 0, 0), button_rect, 2)

        if button_rect.colliderect(cursor_rect) and cur_button == None:
            color = (230, 230, 230)
            cur_button = button

        button_render = Decaying_Felt_Pen.render(button, True, color)

        win.blit(button_render, (WIDTH // 2 - Decaying_Felt_Pen.size(button)[0] // 2 , pos))

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

sfx_mixer = pygame.mixer.Channel(4)
track_mixer = pygame.mixer.Channel(5)

hospital = pygame.mixer.Sound('sounds/hospital.mp3')

sfx_mixer.set_volume(0.7)
track_mixer.set_volume(0.5)

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    mx, my = pygame.mouse.get_pos()
    pygame.mouse.set_visible(False)

    cursor_rect = cursor.get_rect()
    cursor_rect.x = mx; cursor_rect.y = my
    cursor_rect.w = cursor_rect.w // 2
    cursor_rect.h = cursor_rect.h // 2

    win.fill((255, 255, 255))

    if not track_mixer.get_busy():
        track_mixer.play(hospital)

    print(cur_button)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cur_button == 'EXIT':
                pygame.quit()
                sys.exit()
            elif cur_button == 'NEW GAME' or cur_button == 'CONTINUE':
                pygame.quit()
                os.system('python main.py')
            elif cur_button == 'SETTINGS':
                buttons = ['BACK', 'RESET SAVE']
            elif cur_button == 'BACK':
                if started_game == False:
                    buttons = ['NEW GAME', 'SETTINGS', 'EXIT']
                else:
                    buttons = ['CONTINUE', 'SETTINGS', 'EXIT']
            elif cur_button == 'RESET SAVE':
                save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')
                pygame.quit()
                os.system('python scripts\states\menu.py')
            # save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')

    title ='Organ Trafficking  FPS: ' + str(int(clock.get_fps())) + ' - Menu'

    pygame.display.set_caption(title)

    win.blit(background, (0, 0))
    win.blit(title_render, (200, 60))

    load_buttons()

    win.blit(vignette, (0, 0))

    win.blit(cursor, (mx - 8, my - 15))
    
    clock.tick(144)
    
    pygame.display.flip()
