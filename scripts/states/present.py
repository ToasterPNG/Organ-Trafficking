import pygame, json, os, sys, time

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

background_frame = 0
background_time = 0

present_y_velocity = 0
present_y = -200

stop = False

present_opened = pygame.image.load(f'assets\\present\\present\\open_0.png').convert_alpha()

def set_background(frame):
    global background
    background = pygame.image.load(f'assets\\present\\background\\background_{str(frame)}.png').convert_alpha()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

set_background(background_frame)

present_frame = 0
present_time = 0

def set_present(frame):
    global present
    present = pygame.image.load(f'assets\\present\\present\\idle_{str(frame)}.png').convert_alpha()
    #present = pygame.transform.scale(present, (WIDTH, HEIGHT))

set_present(present_frame)


confetti_frame = 0
confetti_time = 0

def set_confetti(frame):
    global confetti
    confetti = pygame.image.load(f'assets\\present\\confeti\\confetti_{str(frame)}.png').convert_alpha()
    #present = pygame.transform.scale(present, (WIDTH, HEIGHT))

set_confetti(confetti_frame)


fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255
confetti_wait_time = 0
wait_time = 0

sfx_mixer = pygame.mixer.Channel(4)
yipee_mixer = pygame.mixer.Channel(5)

present_drop = pygame.mixer.Sound('sounds/present_drop.mp3')
yipee = pygame.mixer.Sound('sounds/yipee.mp3')

sfx_mixer.set_volume(0.7)
yipee.set_volume(0.3)

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

present_rect = pygame.Rect(300, present_y + 50, 150, 250)

played_present_drop = False
start_waiting = False
start_fade = False

confetti_wait = False
play_confetti = False
opened = False

save(floor_kideny_=True,stomach_gave_=True)

while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not fade_alpha >= 1:
                    # start_fade = True
                    pass

        if present_rect.collidepoint(pygame.mouse.get_pos()):

            if event.type == pygame.MOUSEBUTTONUP and played_present_drop and not opened:
                yipee_mixer.play(yipee)
                
                present = present_opened
                confetti_wait = True
                opened = True
                
    present_time += 1 * dt

    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)

    if not opened:
        if present_time >= 0.5:
            if present_frame <= 0:
                present_time = 0
                
                present_frame += 1

                set_present(present_frame)
            else:
                present_frame = -1

    if background_time >= 0.5:
        if background_frame <= 0:
            background_time = 0
            
            background_frame += 1

            set_background(background_frame)
        else:
            background_frame = -1

    if play_confetti:
        confetti_time += 1 * dt
        
        if confetti_time >= 0.05:
            if confetti_frame <= 10:
                confetti_time = 0
                
                confetti_frame += 1

                set_confetti(confetti_frame)
            else:
                play_confetti = False
                start_waiting = True
                confetti_frame = -1

    if confetti_wait:
        confetti_wait_time += 1 * dt

        if confetti_wait_time >= 1:
            if not play_confetti:
                play_confetti = True

    if start_waiting:
        wait_time += 1 * dt

        if wait_time >= 2:
            start_fade = True
    
    win.fill((255,255,255))
    
    present_y += present_y_velocity

    if present_y_velocity <= 13 and present_y <= 130:
        present_y_velocity += 0.1

    if present_y >= 130:
        present_y_velocity = 0

        if played_present_drop == False:
            sfx_mixer.play(present_drop)
            played_present_drop = True
        

    present_rect = pygame.Rect(310, present_y + 50, 180, 200)
    
    win.blit(background, (0, 0))
    win.blit(present, (250, present_y))

    if play_confetti:
        #win.blit(confetti, (0, 0))
        pass # no confetti :(

    #pygame.draw.rect(win, (200, 40, 40), present_rect)
    

    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            pygame.quit()
            os.system('python scripts\states\patient_room.py') # fixxx latr

    # win.blit(esc_text_render, (220, 20))

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)
    
    pygame.display.flip()
