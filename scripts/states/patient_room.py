import pygame, json, os, sys, time

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

patient_room = pygame.image.load('assets\\hospital\\patient room.jpg').convert()
kideny = pygame.image.load('assets\\organs\\kideny.png').convert_alpha()

kideny = pygame.transform.scale(kideny, (30, 40))

kideny_on_floor = pygame.image.load('assets\\organs\\kideny_on_floor.png').convert_alpha()
kideny_on_floor = pygame.transform.scale(kideny_on_floor, (80, 60))

sparkle_frame = 0
sparkle_time = 0

def set_sparkle(frame):
    global sparkle
    sparkle = pygame.image.load(f'assets\\animations\\sparkle\\sparkle_{str(frame)}.png').convert_alpha()
    # sparkle = pygame.transform.scale(sparkle, (140, 160))

set_sparkle(sparkle_frame)


poster_frame = 0
poster_time = 0

def set_poster(frame):
    global poster
    poster = pygame.image.load(f'assets\\animations\\poster\\poster_{str(frame)}.png').convert_alpha()
    poster = pygame.transform.scale(poster, (140, 160))

set_poster(poster_frame)

golf_bubble_frame = 0
golf_bubble_time = 0

def set_golf_bubble(frame):
    global golf_bubble
    golf_bubble = pygame.image.load(f'assets\\animations\\golf bubble\\golf_bubble_{str(frame)}.png').convert_alpha()
    golf_bubble = pygame.transform.scale(golf_bubble, (185, 120))

set_golf_bubble(golf_bubble_frame)

patient_frame = 0
patient_time = 0

def set_patient(frame):
    global patient
    patient = pygame.image.load(f'assets\\people\\patient\\patient_{str(frame)}.png').convert()
    patient = pygame.transform.scale(patient, (140, 110))
    patient.set_colorkey((255, 255, 255))

set_patient(patient_frame)

organ_bubble_frame = 0
organ_bubble_time = 0

def set_organ_bubble(frame):
    global organ_bubble
    organ_bubble = pygame.image.load(f'assets\\animations\\bubble organ\\bubble_{str(frame)}.png').convert_alpha()
    organ_bubble = pygame.transform.scale(organ_bubble, (110, 90))

set_organ_bubble(organ_bubble_frame)

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255

patient_room = pygame.transform.scale(patient_room, (WIDTH, HEIGHT))

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32)
esc_text_render = HighVoltage_Rough_Font.render('Press ESC to leave patients room', True, (0, 0, 0))

sfx_mixer = pygame.mixer.Channel(4)
sparkle_mixer = pygame.mixer.Channel(5)
organ_mixer = pygame.mixer.Channel(6)

dim_angry_chattering = pygame.mixer.Sound('sounds/angry_chattering.mp3')
sparkle_sfx = pygame.mixer.Sound('sounds/sparkle.mp3')
no_organ = pygame.mixer.Sound('sounds/no_organ.mp3')
tv = pygame.mixer.music.load('sounds/tv.mp3')

sfx_mixer.set_volume(0.7)
organ_mixer.set_volume(0.7)

pygame.mixer.music.set_volume(0.1)

poster_rect = pygame.Rect(130, 180, 60, 70)
patient_rect = patient.get_rect(topleft= (350, 250))

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

start_fade = False
show_sparkles = False
change_to_game = False
change_to_present = False

hover_over_patient = False

while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not fade_alpha >= 1:
                    start_fade = True

        elif poster_rect.collidepoint(pygame.mouse.get_pos()):
            show_sparkles = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                start_fade = True
                change_to_game = True
        else:
            show_sparkles = False
        if patient_rect.collidepoint(pygame.mouse.get_pos()):
            hover_over_patient = True

            if event.type == pygame.MOUSEBUTTONUP:

                if stomach_gave == False and "stomach" in organs_bought:
                    stomach_gave = True
                    save(stomach_gave_=True)
                    change_to_present = True
                    start_fade = True
                else:
                    if stomach_gave == False:
                        organ_mixer.play(no_organ)
        else:
            hover_over_patient = False
                
    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    if stomach_gave == False:
        if not sfx_mixer.get_busy():
            sfx_mixer.play(dim_angry_chattering)

    patient_time += 1 * dt

    if patient_time >= 0.5:
        if patient_frame <= 2:
            patient_time = 0
            
            patient_frame += 1

            set_patient(patient_frame)
        else:
            patient_frame = -1

    if floor_kideny == True:
        if not 'liver' in organs_bought:
            golf_bubble_time += 1 * dt

            if golf_bubble_time >= 0.5:
                if golf_bubble_frame <= 0:
                    golf_bubble_time = 0
                    
                    golf_bubble_frame += 1

                    set_golf_bubble(golf_bubble_frame)
                else:
                    golf_bubble_frame = -1
            
    if stomach_gave == False:
        organ_bubble_time += 1 * dt

        if organ_bubble_time >= 0.5:
            if organ_bubble_frame <= 0:
                organ_bubble_time = 0
                
                organ_bubble_frame += 1

                set_organ_bubble(organ_bubble_frame)
            else:
                organ_bubble_frame = -1

    poster_time += 1 * dt

    if poster_time >= 0.2:
        if poster_frame <= 0:
            poster_time = 0
            
            poster_frame += 1

            set_poster(poster_frame)
        else:
            poster_frame = -1

    if show_sparkles:
        sparkle_time += 1 * dt

        if not sparkle_mixer.get_busy():
            sparkle_mixer.play(sparkle_sfx)

        if sparkle_time >= 0.1:
            if sparkle_frame <= 5:
                sparkle_time = 0
                
                sparkle_frame += 1

                set_sparkle(sparkle_frame)
            else:
                sparkle_frame = -1

    if not pygame.mixer.music.get_busy():
        if floor_kideny == True:
            if not 'liver' in organs_bought:
                pygame.mixer.music.play(start=tv_stat_time)
        
    win.fill((255,255,255))
    
    win.blit(patient_room, (0, 0))
    win.blit(patient, (350, 250))

    if floor_kideny == True:
        win.blit(kideny_on_floor, (369, 380))
        if not 'liver' in organs_bought:
            win.blit(golf_bubble, (20, 230))

    win.blit(poster, (90, 140))

    # pygame.draw.rect(win, (230, 50, 50), patient_rect)

    if show_sparkles:
        win.blit(sparkle, (160, 150))

    # pygame.draw.rect(win, (250, 20, 20), poster_rect)

    if hover_over_patient:
        if stomach_gave == False:
            win.blit(organ_bubble, (340, 170))
            win.blit(kideny, (380, 190))

    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            if change_to_present == True:
                 save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                 pygame.quit()
                 os.system('python scripts\states\present.py')
            elif change_to_game == True:
                 save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                 pygame.quit()
                 os.system('python scripts\states\skely.py')
            else:
                save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                pygame.quit()
                os.system('python scripts\states\hallway.py') # fixxx latr

    win.blit(esc_text_render, (220, 20))

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)

    pygame.display.update()
    pygame.display.flip()
