import pygame, json, os, sys, time, cv2
import pygame.mixer

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

patient_room = pygame.image.load('assets\\hospital\\patient room 2.jpg').convert()
foreground = pygame.image.load('assets\\hospital\\foreground.png').convert_alpha()
present_liver = pygame.image.load('assets\\present\\present_liver.png').convert_alpha()

liver = pygame.image.load('assets\\organs\\liver.png').convert_alpha()
present_liver = pygame.transform.scale(present_liver, (100, 100))
liver = pygame.transform.scale(liver, (50, 70))

golf = cv2.VideoCapture('assets\\videos\\golf.mp4')

success, golf_frame = golf.read()

shape = golf_frame.shape[1::-1]

patient_2_time = 0
patient_2_frame = 0

def set_patient_2(frame):
    global patient_2
    patient_2 = pygame.image.load(f'assets\\people\\patient 2\\patient_2_{str(frame)}.png').convert_alpha()
    patient_2 = pygame.transform.scale(patient_2, (319, 246))

set_patient_2(patient_2_frame)

organ_bubble_time = 0
organ_bubble_frame = 0

def set_organ_bubble(frame):
    global organ_bubble
    organ_bubble = pygame.image.load(f'assets\\animations\\bubble organ\\bubble_{str(frame)}.png').convert_alpha()
    organ_bubble = pygame.transform.scale(organ_bubble, (130, 100))

set_organ_bubble(organ_bubble_frame)

tv_back_panel_time = 0
tv_back_panel_frame = 0

def set_tv_back_panel(frame):
    global tv_back_panel
    tv_back_panel = pygame.image.load(f'assets\\animations\\tv\\back_plate_{str(frame)}.png').convert_alpha()
    tv_back_panel = pygame.transform.scale(tv_back_panel, (130, 100))

set_tv_back_panel(tv_back_panel_frame)

tv_front_panel_time = 0
tv_front_panel_frame = 0

def set_tv_front_panel(frame):
    global tv_front_panel
    tv_front_panel = pygame.image.load(f'assets\\animations\\tv\\front_plate_{str(frame)}.png').convert_alpha()
    tv_front_panel = pygame.transform.scale(tv_front_panel, (130, 100))

set_tv_front_panel(tv_front_panel_frame)

sparkle_frame = 0
sparkle_time = 0

def set_sparkle(frame):
    global sparkle
    sparkle = pygame.image.load(f'assets\\animations\\sparkle\\sparkle_{str(frame)}.png').convert_alpha()
    # sparkle = pygame.transform.scale(sparkle, (140, 160))

set_sparkle(sparkle_frame)

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255
fps_wait = 0

patient_room = pygame.transform.scale(patient_room, (WIDTH, HEIGHT))
foreground = pygame.transform.scale(foreground, (WIDTH, HEIGHT))

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32)
esc_text_render = HighVoltage_Rough_Font.render('Press ESC to leave patients room', True, (0, 0, 0))

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

sfx_mixer = pygame.mixer.Channel(4)
sparkle_mixer = pygame.mixer.Channel(5)

# dim_angry_chattering = pygame.mixer.Sound('sounds/angry_chattering.mp3')
no_organ = pygame.mixer.Sound('sounds/no_organ.mp3')
sparkle_sfx = pygame.mixer.Sound('sounds/sparkle.mp3')
tv = pygame.mixer.music.load('sounds/tv.mp3')

sfx_mixer.set_volume(0.7)
sparkle_mixer.set_volume(0.7)

patient_2_rect = pygame.Rect(385, 194, 259, 116)
tv_rect = pygame.Rect(135, 220, 100, 70)

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

start_fade = False
hovered_over_patient_2 = False
move_to_golf = False
show_sparkels = False
present_2 = False

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

        if patient_2_rect.collidepoint(pygame.mouse.get_pos()):
            if not liver_gave:
                hovered_over_patient_2 = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if not 'liver' in organs_bought:
                        sfx_mixer.play(no_organ)
                    else:
                        start_fade = True
                        present_2 = True
        else:
            hovered_over_patient_2 = False

        if tv_rect.collidepoint(pygame.mouse.get_pos()):
            if not 'liver' in organs_bought:
                show_sparkles = True

                if event.type == pygame.MOUSEBUTTONUP:
                    start_fade = True
                    move_to_golf = True
        else:
            show_sparkles = False
            
    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    patient_2_time += 1 * dt

    if patient_2_time >= 0.5:
        if patient_2_frame <= 0:
            patient_2_time = 0
            
            patient_2_frame += 1

            set_patient_2(patient_2_frame)
        else:
            patient_2_frame = -1

    organ_bubble_time += 1 * dt

    if organ_bubble_time >= 0.5:
        if organ_bubble_frame <= 0:
            organ_bubble_time = 0
            
            organ_bubble_frame += 1

            set_organ_bubble(organ_bubble_frame)
        else:
            organ_bubble_frame = -1

    tv_back_panel_time += 1 * dt

    if tv_back_panel_time >= 0.7:
        if tv_back_panel_frame <= 0:
            tv_back_panel_time = 0
            
            tv_back_panel_frame += 1

            set_tv_back_panel(tv_back_panel_frame)
        else:
            tv_back_panel_frame = -1

    tv_front_panel_time += 1 * dt

    if tv_front_panel_time >= 0.7:
        if tv_front_panel_frame <= 0:
            tv_front_panel_time = 0
            
            tv_front_panel_frame += 1

            set_tv_front_panel(tv_front_panel_frame)
        else:
            tv_front_panel_frame = -1

    if not pygame.mixer.music.get_busy():
        if floor_kideny == True:
            if not 'liver' in organs_bought:
                pygame.mixer.music.play(start=tv_stat_time)
        
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
    
    win.fill((255,255,255))
    
    win.blit(patient_room, (0, 0))
    win.blit(patient_2, (375, 154))
    win.blit(tv_back_panel, (120, 210))

    if show_sparkles:
        win.blit(sparkle, (210, 190))

    fps_wait += 30 * dt

    if fps_wait >= 1:
        success, golf_frame = golf.read()
        fps_wait = 0

    if not 'liver' in organs_bought:
        if type(golf_frame) != type(None):
            current_frame = pygame.image.frombuffer(golf_frame.tobytes(), shape, "BGR")

            current_frame = pygame.transform.scale(current_frame, (50, 48))
            win.blit(current_frame, (175, 240))
        else:
            golf = cv2.VideoCapture('assets\\videos\\golf.mp4')
    else:
        current_frame = pygame.Surface((50, 48))
        current_frame.fill((0, 0, 0))

        win.blit(current_frame, (175, 240))

    
    win.blit(tv_front_panel, (120, 210))

    if liver_gave:
        win.blit(present_liver, (650, 205))

    if hovered_over_patient_2:
        win.blit(organ_bubble, (420, 137))
        win.blit(liver, (460, 147))

    win.blit(foreground, (0, 0))

    # pygame.draw.rect(win, (230, 40, 40), tv_rect)


    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            if present_2:
                pygame.quit()
                os.system('python scripts\states\present_2.py')  
            elif not move_to_golf:
                save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                pygame.quit()
                os.system('python scripts\states\hallway.py') # fixxx latr
            else:
                save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000))
                pygame.quit()
                os.system('python scripts\states\golf.py')

    win.blit(esc_text_render, (220, 20))

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)
    
    pygame.display.flip()
