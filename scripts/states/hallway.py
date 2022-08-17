import pygame, json, os, sys, time

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

hospital_hallway = pygame.image.load('assets\\hospital\\hallway.jpg').convert()
hospital_hallway_door = pygame.image.load('assets\\hallway_door.png').convert_alpha()

bubble_frame = 0
bubble_time = 0

def set_speech_bubble(frame):
    global speech_bubble
    speech_bubble = pygame.image.load(f'assets\\animations\\speech bubble\\bubble_{str(frame)}.png').convert_alpha()
    speech_bubble = pygame.transform.scale(speech_bubble, (200, 200))

set_speech_bubble(bubble_frame)

warning_frame = 0
warning_time = 0

warning_frame_2 = 0
warning_time_2 = 0

def set_warning(frame):
    global warning
    warning = pygame.image.load(f'assets\\ui\\pop_up_unlock_error_{str(frame)}.png').convert_alpha()
    warning = pygame.transform.scale(warning, (200, 150))

def set_warning_2(frame):
    global warning_2
    warning_2 = pygame.image.load(f'assets\\ui\\pop_up_unlock_error_2_{str(frame)}.png').convert_alpha()
    warning_2 = pygame.transform.scale(warning_2, (200, 150))

set_warning(warning_frame)
set_warning_2(warning_frame_2)

golf_bubble_frame = 0
golf_bubble_time = 0

def set_golf_bubble(frame):
    global golf_bubble
    golf_bubble = pygame.image.load(f'assets\\animations\\golf bubble\\golf_bubble_{str(frame)}.png').convert_alpha()
    golf_bubble = pygame.transform.scale(golf_bubble, (155, 100))

set_golf_bubble(golf_bubble_frame)

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255

hospital_hallway = pygame.transform.scale(hospital_hallway, (WIDTH, HEIGHT))
hospital_hallway_door = pygame.transform.scale(hospital_hallway_door, (WIDTH, HEIGHT))

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32)
esc_text_render = HighVoltage_Rough_Font.render('Press ESC to leave hospital', True, (0, 0, 0))

sfx_mixer = pygame.mixer.Channel(4)

tv = pygame.mixer.music.load('sounds/tv.mp3')
dim_angry_chattering = pygame.mixer.Sound('sounds/dim_angry_chattering.mp3')

sfx_mixer.set_volume(0.4)
pygame.mixer.music.set_volume(0.2)

door_rect = pygame.Rect(580, 30, 60, 420)
door_2_rect = pygame.Rect(230, 80, 90, 320)
door_3_rect = pygame.Rect(500, 30, 70, 320)

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

start_fade = False
show_warning = False
show_warning_2 = False
move_next_scene = False
move_to_end_scene = False

fade_warning_time = 255
fade_warning_time_vel = 0

fade_warning_time_2 = 255
fade_warning_time_vel_2 = 0

scene_change = 1

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

        if door_rect.collidepoint(pygame.mouse.get_pos()):

            if event.type == pygame.MOUSEBUTTONUP:
                start_fade = True
                move_next_scene = True

        if door_2_rect.collidepoint(pygame.mouse.get_pos()):

            if event.type == pygame.MOUSEBUTTONUP:
                if stomach_gave == False:
                    show_warning = True
                else:
                    scene_change = 2
                    start_fade = True
                    move_next_scene = True

        if door_3_rect.collidepoint(pygame.mouse.get_pos()):

            if event.type == pygame.MOUSEBUTTONUP:
                if liver_gave:
                    start_fade = True
                    move_next_scene = True
                    move_to_end_scene = True
                else:
                    show_warning_2 = True

    if not pygame.mixer.music.get_busy():
        if floor_kideny == True:
            if not 'liver' in organs_bought:
                pygame.mixer.music.play(start=tv_stat_time)
                
    bubble_time += 1 * dt

    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    if bubble_time >= 0.5:
        if bubble_frame <= 0:
            bubble_time = 0
            
            bubble_frame += 1

            set_speech_bubble(bubble_frame)
        else:
            bubble_frame = -1

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
                
    if show_warning:
        warning_time += 1 * dt

        if warning_time >= 0.5:
            if warning_frame <= 0:
                warning_time = 0
                
                warning_frame += 1

                set_warning(warning_frame)
            else:
                warning_frame = -1

    if show_warning:
        fade_warning_time_vel += 100 * dt
        fade_warning_time -= fade_warning_time_vel * dt

        warning.set_alpha(int(fade_warning_time))


    if show_warning_2:
        warning_time_2 += 1 * dt

        if warning_time_2 >= 0.5:
            if warning_frame_2 <= 0:
                warning_time_2 = 0
                
                warning_frame_2 += 1

                set_warning_2(warning_frame_2)
            else:
                warning_frame_2 = -1

    if show_warning_2:
        fade_warning_time_vel_2 += 100 * dt
        fade_warning_time_2 -= fade_warning_time_vel_2 * dt

        warning_2.set_alpha(int(fade_warning_time_2))

    if fade_warning_time <= 0:
        show_warning = False
        fade_warning_time_vel = 0
        fade_warning_time = 255

    if fade_warning_time_2 <= 0:
        show_warning_2 = False
        fade_warning_time_vel_2 = 0
        fade_warning_time_2= 255
            
    if stomach_gave == False:
        if not sfx_mixer.get_busy():
            sfx_mixer.play(dim_angry_chattering)
    
    win.fill((255,255,255))
    
    win.blit(hospital_hallway, (0, 0))
    win.blit(hospital_hallway_door, (0, 0))

    # pygame.draw.rect(win, (250, 20, 20), door_3_rect)

    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            if not move_next_scene:
                pygame.quit()
                os.system('python main.py') # fixxx latr
            else:
                if move_to_end_scene:
                    save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                    pygame.quit()
                    os.system('python scripts\states\end_room.py')
                elif scene_change == 1:
                    save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                    pygame.quit()
                    os.system('python scripts\states\patient_room.py')
                else:
                    save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                    pygame.quit()
                    os.system('python scripts\states\patient_room_2.py')
                #import scripts.states.patient_room


    win.blit(esc_text_render, (270, 20))

    if stomach_gave == False:
        win.blit(speech_bubble, (370, 70))
    else:
        if not 'liver' in organs_bought:
            win.blit(golf_bubble, (290, 160))

    if show_warning:
        win.blit(warning, (325, 150))

    if show_warning_2:
        win.blit(warning_2, (325, 150))

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)
    
    pygame.display.flip()
