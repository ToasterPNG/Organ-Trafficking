import pygame, json, os, sys, time, math, random

sys.path.insert(0, os.getcwd())

from scripts.saving import *

pygame.init()


WIDTH = 800
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Organ Trafficking')

clock = pygame.time.Clock()

arrow_background = pygame.image.load(f'assets\\golf\\arrow\\bg.png').convert()
background = pygame.image.load(f'assets\\golf\\background.png').convert()
arrow = pygame.image.load(f'assets\\golf\\arrow\\arrow.png').convert_alpha()

sand_0 = pygame.image.load('assets\\golf\\sand\\sand_1.png').convert()
sand_0.set_colorkey((0, 0, 0))

sand_1 = pygame.image.load('assets\\golf\\sand\\sand_0.png').convert()
sand_1 = pygame.transform.flip(sand_1, True, True)
sand_1.set_colorkey((0, 0, 0))

water_0 = pygame.image.load('assets\\golf\\water\\water_0.png').convert()
water_0.set_colorkey((0, 0, 0))

bar = pygame.image.load(f'assets\\golf\\bar.png').convert()
tutorial_3_text = pygame.image.load(f'assets\\golf\\tutorial_3_text.png').convert_alpha()

vignette = pygame.image.load(f'assets\\golf\\vignette.png').convert_alpha()

vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))
tutorial_3_text = pygame.transform.scale(tutorial_3_text, (170, 150))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
arrow_background = pygame.transform.scale(arrow_background, (WIDTH, HEIGHT))
bar = pygame.transform.scale(bar, (650, 30))
sand_0 = pygame.transform.scale(sand_0, (450, 380))
sand_1 = pygame.transform.scale(sand_1, (450, 580))
water_0 = pygame.transform.scale(water_0, (450, 580))

#sand_0 = pygame.transform.scale(sand_0, (110, 150))
sand_0_mask = pygame.mask.from_surface(sand_0)
sand_1_mask = pygame.mask.from_surface(sand_1)
water_0_mask = pygame.mask.from_surface(water_0)

eye_frame = 0
eye_time = 0

def set_eye_roll(frame):
    global eye
    eye = pygame.image.load(f'assets\\golf\\eye\\eye_roll_0_{str(frame)}.png').convert_alpha()
    eye = pygame.transform.scale(eye, (20, 20))

set_eye_roll(eye_frame)

flag_frame = 0
flag_time = 0

def set_flag(frame):
    global flag
    flag = pygame.image.load(f'assets\\golf\\finish_flag\\finish_flag_{str(frame)}.png').convert_alpha()
    flag = pygame.transform.scale(flag, (60, 110))

set_flag(flag_frame)

fade_screen = pygame.Surface((WIDTH,HEIGHT))
fade_screen.fill((0,0,0))

fade_alpha = 255
shots_left = 1

HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
BadlyStamped_Font = pygame.font.Font('fonts/BadlyStamped.ttf', 32)

def set_shots_text_render():
    global shots_left_text_render
    shots_left_text_render = BadlyStamped_Font.render(f'SHOTS LEFT {str(shots_left)}', True, (0, 0, 0))

set_shots_text_render()

prev_time = time.time()
fade_screen.set_alpha(fade_alpha)

controlling_golf_ball = False
golf_ball_end_vel = False
shoot_golf_ball = False
played_water = True
start_fade = False
next_level = False
bar_shown = True

golf_ball_col = [70, 420]
arrow_rect = pygame.Rect(golf_ball_col[0] - 20, golf_ball_col[1] - 20, 40, 40)
golf_ball_rect = pygame.Rect(golf_ball_col[0] - 20, golf_ball_col[1] - 20, 40, 40)

wall_rect = pygame.Rect(0, 500, 800, 500)
wall_rect_0 = pygame.Rect(0, -500, 800, 500)
wall_rect_1 = pygame.Rect(-800, 0, 800, 500)
wall_rect_2 = pygame.Rect(800, 0, 800, 500)

golf_ball_surface_rect = pygame.Surface((golf_ball_rect.w // 2, golf_ball_rect.h // 2)).convert_alpha()
glof_ball_mask = None

offset = pygame.math.Vector2(50, 0)
velocity = 0

dxv, dyv = 0, 0
gxv, gyv = 0, 0

ball_speed = 3
shown_ball_speed = 0 # bar speed

sand_pos = (150, 300)
sand_1_pos = (130, -220)
water_pos = (420, 300)

collisions = [False] * 9

simpler_collisions = [False] * 5  # top bottom right left
last_collisions = [False] * 5

angle = 0

golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)

win_rect = pygame.Rect(680, 80, 30, 15)

track_mixer = pygame.mixer.Channel(4)
sfx_mixer = pygame.mixer.Channel(5)

golf_song = pygame.mixer.Sound('sounds/golf.mp3')

water = pygame.mixer.Sound('sounds/water.mp3')

club_0 = pygame.mixer.Sound('sounds/club_0.mp3')
club_1 = pygame.mixer.Sound('sounds/club_1.mp3')
club_2 = pygame.mixer.Sound('sounds/club_2.mp3')

track_mixer.set_volume(0.4)
sfx_mixer.set_volume(0.6)

dont_show_eye = False
restart = False

while True:
    dt = time.time() - prev_time
    prev_time = time.time()

    golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)
    
    overlap_sand_mask = golf_ball_mask.overlap_mask(sand_0_mask, (sand_pos[0] - golf_ball_rect.x, sand_pos[1] - golf_ball_rect.y))
    overlap_1_sand_mask = golf_ball_mask.overlap_mask(sand_1_mask, (sand_1_pos[0] - golf_ball_rect.x, sand_1_pos[1] - golf_ball_rect.y))
    overlap_water_mask = golf_ball_mask.overlap_mask(water_0_mask, (water_pos[0] - golf_ball_rect.x, water_pos[1] - golf_ball_rect.y))

    mx, my = pygame.mouse.get_pos()
    collision = False

    if not track_mixer.get_busy():
        track_mixer.play(golf_song)

    if shots_left == 0 and not shoot_golf_ball and not next_level:
        restart = True
        start_fade = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save(golf_level_=3)
            pygame.quit()
            quit()

        """

        Hold Space To Aim The Golf Ball

        Release Space To Shoot The Golf Ball
        
        """
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not fade_alpha >= 1:
                    save(golf_level_=3)
                    start_fade = True

            if event.key == pygame.K_SPACE and not shoot_golf_ball:
                if not arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    controlling_golf_ball = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and not shoot_golf_ball:
                if not arrow_rect.collidepoint(pygame.mouse.get_pos()) and shots_left > 0:
                    if "rotated_arrow" in locals():
                        dxv, dyv = mx, my
                        gxv, gyv = golf_ball_col[0], golf_ball_col[1]

                        shots_left -= 1; set_shots_text_render()

                        club = random.randint(1, 3)

                        if club == 1:
                            sfx_mixer.play(club_0)
                        if club == 2:
                            sfx_mixer.play(club_1)
                        if club == 3:
                            sfx_mixer.play(club_2)

                            
                        ball_speed = shown_ball_speed
                        
                        controlling_golf_ball = False
                        shoot_golf_ball = True
                    
        if controlling_golf_ball:
            if event.type == pygame.MOUSEMOTION: # Rotate arrow around ball and twords mouse B) (math math math)
                
                dx, dy = mx - arrow_rect.centerx, my - arrow_rect.centery
                angle = math.degrees(math.atan2(dy, dx))
                
                rotated_arrow = pygame.transform.rotozoom(arrow, -angle, 1)
                rotated_offset = offset.rotate(angle)

                arrow_rect = rotated_arrow.get_rect(center=golf_ball_col+rotated_offset)

    if overlap_water_mask.count() > 0:
        if played_water:
            sfx_mixer.play(water)
            played_water = False
            
        restart = True
        dont_show_eye = True
        start_fade = True
    
    golf_ball_rect = pygame.Rect(golf_ball_col[0]-10, golf_ball_col[1]-10,   10*2, 10*2 )

    vignette_alpha = 50 + overlap_sand_mask.count() // 20
    vignette_alpha = 50 + overlap_1_sand_mask.count() // 20

    vignette.set_alpha(vignette_alpha)

    """
    if shoot_golf_ball and ball_speed >= 0:          # math math math math math math math math
                                                     # (move ball to mouse)
        if gxv > dxv:   
            if int(golf_ball_col[0]) > dxv:
                ball_speed -= 0.01
                golf_ball_col[0] += ball_speed*math.cos(math.radians(angle))
        else:
            if int(golf_ball_col[0]) < dxv:
                ball_speed -= 0.01
                golf_ball_col[0] += ball_speed*math.cos(math.radians(angle))


        if gyv > dyv:
            if int(golf_ball_col[1]) > dyv:
                ball_speed -= 0.01
                golf_ball_col[1] += ball_speed*math.sin(math.radians(angle))
        else:
            if int(golf_ball_col[1]) < dyv:
                ball_speed -= 0.01
                golf_ball_col[1] += ball_speed*math.sin(math.radians(angle))
    else:
        ball_speed = 3
        shoot_golf_ball = False
    """

    if golf_ball_rect.colliderect(win_rect):
        dont_show_eye = True
        next_level = True
        start_fade = True

    #print(overlap_sand_mask.count())

    eye_time += 0.6 * dt

    if eye_time >= 0.5:
        if eye_frame <= 0:
            eye_time = 0
            
            eye_frame += 1

            set_eye_roll(eye_frame)
        else:
            eye_frame = -1


    flag_time += 0.4 * dt

    if flag_time >= 0.5:
        if flag_frame <= 0:
            flag_time = 0
            
            flag_frame += 1

            set_flag(flag_frame)
        else:
            flag_frame = -1

            
    if shoot_golf_ball and ball_speed >= 0:          # math math math math math math math math
                                                     # (move ball to mouse)

        ball_speed -= 0.02
        golf_ball_col[0] += ball_speed*math.cos(math.radians(angle))
        golf_ball_col[1] += ball_speed*math.sin(math.radians(angle))
        
    else:
        ball_speed = 3
        shoot_golf_ball = False

    if bar_shown:
        if shown_ball_speed < 8:
            shown_ball_speed += 6 * dt
        else:
            bar_shown = False
    else:
        if shown_ball_speed > 0:
            shown_ball_speed -= 6 * dt
        else:
            bar_shown = True
        
    #print(int(shown_ball_speed))
    #print('DV', dxv, dyv, 'GOLF BALL', int(golf_ball_col[0]), int(golf_ball_col[1]))

    ball_speed -= overlap_sand_mask.count() // 300
    ball_speed -= overlap_1_sand_mask.count() // 300
    
    if golf_ball_rect.colliderect(wall_rect):
        angle = -angle
        golf_ball_col[1] -= ball_speed * 4
        
    if golf_ball_rect.colliderect(wall_rect_0):
        angle = -angle
        golf_ball_col[1] += ball_speed * 4


    if golf_ball_rect.colliderect(wall_rect_1):
        angle = angle // 2
        golf_ball_col[0] += ball_speed * 4

    if golf_ball_rect.colliderect(wall_rect_2):
        angle = angle * 2
        golf_ball_col[0] -= ball_speed * 4

        
    if fade_alpha != 0:
        fade_screen.set_alpha(fade_alpha)
        
    win.fill((255,255,255))
    
    win.blit(background, (0, 0))

    #win.blit(sand_0, (620, 200))
    #win.blit(sand_0_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), (620, 200))

    win.blit(tutorial_3_text, (550, 170))
    
    #pygame.draw.circle(win, (0, 255, 0), golf_ball_col, 10, 0)
    win.blit(sand_0, (150, 300))
    win.blit(sand_1, (sand_1_pos[0], sand_1_pos[1]))
    win.blit(water_0, (water_pos[0], water_pos[1]))
    
    if not dont_show_eye:
        win.blit(eye, (golf_ball_rect.x, golf_ball_rect.y))
        
    win.blit(flag, (660, 0))

    #pygame.draw.rect(win, (0, 0, 255), win_rect, 2)

    #win.blit(golf_ball_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), (golf_ball_rect.x, golf_ball_rect.y))
    #win.blit(overlap_sand_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 0, 0, 255)), (golf_ball_rect.x, golf_ball_rect.y))
    
    #pygame.draw.rect(win, (0, 0, 255), arrow_rect, 2)

    #pygame.draw.rect(win, (250, 0, 0), golf_ball_rect, 2)
    #pygame.draw.rect(win, (210, 30, 30), wall_rect_1)


    if controlling_golf_ball:
        if "rotated_arrow" in locals() and shots_left > 0:
            #win.blit(rotated_arrow, arrow_rect)   # Masked arrow bg effect

            win.blit(rotated_arrow, arrow_rect)
            
    # shown ball speed bar

    win.blit(bar, (70, 440))

    pygame.draw.rect(win, (30, 30, 30), pygame.Rect(70 + shown_ball_speed * 78, 440, 10, 30)) # line
    pygame.draw.rect(win, (0, 0, 0), pygame.Rect(70, 440, 650, 30), 3, 2)
    
    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:
            if next_level and not restart:
                pygame.quit()
                os.system('python scripts\\states\\levels\\level_4.py')    
            elif restart and not next_level:
                pygame.quit()
                os.system('python scripts\\states\\levels\\level_3.py')
            else:
                pygame.quit()
                os.system('python scripts\\states\\levels\\level_3.py')
            
    win.blit(shots_left_text_render, (230, 20))
    win.blit(vignette, (0, 0))

    title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title)
    
    win.blit(fade_screen, (0, 0))
    clock.tick(144)
    
    pygame.display.flip()
