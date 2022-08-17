import pygame, os, sys, time
import pygame.mixer

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

end_room = pygame.image.load('assets\\hospital\\end room.jpg').convert()
foreground = pygame.image.load('assets\\hospital\\end room foreground.png').convert_alpha()

uhoh_frame = 1
uhoh_time = 0

"""
{
    "Game_Data": [
        {
        "money": 1105,
        "organs_bought": ["stomach", "liver"],

        "stomach_gave": true,
        "floor_kideny": true,
        "liver_gave": true,
        "started_game": true,

        "tv_start_time": -1,
        "golf_level": 5,

        "key": false
        }
    ]
}
"""

def set_uhoh():
    global uhoh
    uhoh = pygame.image.load(f'assets\\animations\\uhoh\\{str(uhoh_frame)}.png')
    uhoh.set_colorkey((255, 255, 255))
    #uhoh = pygame.transform.scale(uhoh, (328 x 247))

set_uhoh()

patient_frame = 1
patient_time = 0

def set_patient():
    global patient
    patient = pygame.image.load(f'assets\\people\\patient 3\\patient_3_{str(patient_frame)}.png')
    #patient = pygame.transform.scale(patient, (WIDTH, HEIGHT))

set_patient()


button_frame = 1
button_time = 0

def set_button():
    global button
    button = pygame.image.load(f'assets\\animations\\final button\\final_button_{str(button_frame)}.png')
    #uhoh = pygame.transform.scale(uhoh, (328 x 247))

set_button()

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255
fps_wait = 0

end_room = pygame.transform.scale(end_room, (WIDTH, HEIGHT))
foreground = pygame.transform.scale(foreground, (WIDTH, HEIGHT))

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32)
esc_text_render = HighVoltage_Rough_Font.render('Press ESC to leave patients room', True, (0, 0, 0))

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

sfx_mixer = pygame.mixer.Channel(4)

blip = pygame.mixer.Sound('sounds/blip.wav')

sfx_mixer.set_volume(0.7)

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

show_button = False
roll_credits = False
button_time = True
played_blip = False
uhoh_true = False

button_apear_time = 0
credit_time = 0

final_button_rect = pygame.Rect(WIDTH / 2 - button.get_width() / 2, HEIGHT / 2 - button.get_height() / 2, 356, 154)

# 656 x 494 -> 328 x 247

while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if final_button_rect.collidepoint(pygame.mouse.get_pos()):

        if event.type == pygame.MOUSEBUTTONUP:
            uhoh_true = True
            show_button = False
            button_time = False

    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    win.fill((255,255,255))
    
    win.blit(end_room, (0, 0))
    
    # pygame.draw.rect(win, (230, 40, 40), tv_rect)

    button_apear_time += 1 * dt

    patient_time += 2 * dt

    if patient_time > 0.1:
        if patient_frame < 3:
            patient_time = 0
            patient_frame += 1

            set_patient()
        else:
            patient_frame = 0

    win.blit(patient, (200, 60))
    win.blit(foreground, (0, 0))

    if uhoh_true:
        uhoh_time += 2 * dt

        if uhoh_time > 0.2 and uhoh_frame < 82:
            uhoh_time = 0
            uhoh_frame += 1

            set_uhoh()

        win.blit(uhoh, (WIDTH // 10, 5))
    
    if show_button:
        button_time += 1 * dt

        if button_time > 0.5:
            button_time = 0

            if button_frame == 1:
                button_frame = 0
            else:
                button_frame += 1

            set_button()
            

    if button_apear_time > 2:
        if button_time:
            if not played_blip:
                sfx_mixer.play(blip)
                played_blip = True
            show_button = True

    if show_button:
        win.blit(button, (WIDTH / 2 - button.get_width() / 2, HEIGHT / 2 - button.get_height() / 2))

    #pygame.draw.rect(win, (255, 0, 0), final_button_rect, 2)

    if fade_alpha >= 1 and not roll_credits:
        fade_alpha -= 300 * dt

    if uhoh_frame >= 82:
        roll_credits = True
        fade_alpha = 255

        credit_time += 1 * dt

        if credit_time >= 3:
            save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')
            pygame.quit()
            import scripts.states.menu


    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)
    
    pygame.display.flip()
