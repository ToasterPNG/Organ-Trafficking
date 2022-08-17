

"""

COPMILATION DAY: yipee



first day:
----------------

made the architecture or smthn

added:

  --menu
  --map  (no tranzitions)


second day:
----------------

  --map
  --patient-room-1
  --shop
  --hallway


third day:
----------------

  --skely
  --patient-room-2
  --present-1
  --present-2

  --endroom

  --golf_lvl_1
  --golf_lvl_2
  --golf_lvl_3
  --golf_lvl_4
  --golf_lvl_5

  # fixed some weird saving bugs too
  # finished adding all scenes

fourth day:
----------------

  --fixed a couple var referencing bugs
  --fixed some more save data bugs
  
  # mostly just bug fixes

fifth day:
----------------

  --added extra fade screen to menu
  --fixing save bug at end of game

"""

from scripts.shake import *
from scripts.sharpen import *

import scripts.saving

class Scene_Functions():

    def __init__(self):
        pass

    def add_global(self, var, var_name):
        exec(f"self.{var_name} = var")

    def load_buttons(self, buttons, cur_button, cursor_rect, win):

        pos = 150 - len(buttons) * 10
        cur_button = None

        for button in buttons:
            color = (0, 0, 0)

            button_render = self.Decaying_Felt_Pen.render(button, True, (0, 0, 0))

            pos += 65

            button_rect = button_render.get_rect()
            button_rect.x = self.WIDTH // 2 - self.Decaying_Felt_Pen.size(button)[0] // 2
            button_rect.y = pos

            #pygame.draw.rect(win, (255, 0, 0), button_rect, 2)

            if button_rect.colliderect(cursor_rect) and cur_button == None:
                color = (230, 230, 230)
                cur_button = button

            button_render = self.Decaying_Felt_Pen.render(button, True, color)

            win.blit(button_render, (self.WIDTH // 2 - self.Decaying_Felt_Pen.size(button)[0] // 2 , pos))

        return cur_button

    def check_contract_anmation(self, title, show_contract, contract_y_anim, signiture_counter_movement_y, vel_anim_y, win, contract, contract_stomach, frame_signature,
                                signature_delay, money, sfx_mixer, contract_sign, contract_leave_delay, contract_slide_2, stomach_sold_out):
        global signature_animation

        set_sold_out = 'global ' + title + '_sold_out; ' + title + '_sold_out = True'

        if show_contract: # CONTRACT ANIMATION #
            exec(set_sold_out)

            stomach_sold_out = True

            # paper move up anim

            if contract_y_anim > 150 and signiture_counter_movement_y == 0:
                vel_anim_y += 0.4
                contract_y_anim -= vel_anim_y
            else:
                signature_delay += 20

                # signing anim
                if frame_signature < 19 and signature_delay >= 2400:
                    
                    if frame_signature == 0:
                        sfx_mixer.play(contract_sign)
                        sfx_mixer.set_volume(0.9)

                    signature_animation = pygame.image.load(f'assets\\animations\\signature\{frame_signature}.png').convert_alpha()
                    signature_animation = pygame.transform.scale(signature_animation, (100, 50))
                    frame_signature += 1

                if not sfx_mixer.get_busy():
                    sfx_mixer.set_volume(0.5)
        
            win.blit(contract, (self.WIDTH // 2.7, contract_y_anim))
            win.blit(contract_stomach, (self.WIDTH // 2.7, contract_y_anim))


            if frame_signature > 1:
                win.blit(signature_animation, (self.WIDTH // 2.05, contract_y_anim * 2.27 + signiture_counter_movement_y))

            if frame_signature == 19:

                contract_leave_delay += 20

                if contract_y_anim < 550 and contract_leave_delay >= 3400:
                    vel_anim_y -= 1

                    if signiture_counter_movement_y == 0:
                        sfx_mixer.play(contract_slide_2)
                        sfx_mixer.set_volume(0.9)

                    if signiture_counter_movement_y <= 30:
                        signiture_counter_movement_y += 52
                    else:
                        signiture_counter_movement_y += vel_anim_y
                        # show_contract = False

                    if vel_anim_y == -33.199999999999996:
                        show_contract = False
                        
                    contract_y_anim -= vel_anim_y

        if not stomach_sold_out:
            return contract_y_anim, signiture_counter_movement_y, money, vel_anim_y, signature_delay, frame_signature, contract_leave_delay, show_contract, False
        else:
            return contract_y_anim, signiture_counter_movement_y, money, vel_anim_y, signature_delay, frame_signature, contract_leave_delay, show_contract, True
                            
func = Scene_Functions()


class Scene_Manager():

    def __init__(self, func, organs_bought, stomach_gave, floor_kideny, money, organ, level, liver, started):
        self.current_scene = 'menu'
        
        self.organs_bought = organs_bought
        self.stomach_gave = stomach_gave
        self.floor_kideny = floor_kideny

        self.money = money
        self.func = func

        self.organ = organ
        self.golf_level = level

        self.gvliver = liver
        self.started = started

    def update_scene(self, func):
        import scripts.saving
        if self.current_scene == 'menu': # ----------------------MENU----------------------------

            """
            Buttons:

            NEW GAME - only shows up if there is no save file
            LOAD GAME - only shows up if there is a save file
            SETTINGS
            EXIT

            """

            import pygame, os, sys, time
            import pygame.mixer

            sys.path.insert(0, os.getcwd())

            pygame.init()

            WIDTH = 800
            HEIGHT = 500

            win = pygame.display.set_mode((WIDTH,HEIGHT))
            pygame.display.set_caption('Organ Trafficking - MENU')

            clock = pygame.time.Clock()
            stop_fade = False

            background = pygame.image.load('assets\\ui\\background.jpg')
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            vignette = pygame.image.load('assets\\golf\\vignette.png')
            vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))

            fade_time = 0
            start_fade = False

            cursor_idle_frame = 0
            cur_button = None
            
            def cursor_set(frame):
                cursor = pygame.image.load(f'assets\\cursor\\cursor_{str(frame)}.png').convert_alpha()
                cursor = pygame.transform.scale(cursor, (int(cursor.get_width() * 1.5), int(cursor.get_height() * 1.5)))
                return cursor

            cursor = cursor_set(cursor_idle_frame)

            vignette.set_alpha(144)

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            fade_alpha = 255

            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 64)
            Decaying_Felt_Pen = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
            title_render = HighVoltage_Rough_Font.render('Organ Trafficking', True, (0, 0, 0))

            with open('save.json', 'r') as save_file:
                save_file = save_file.read()

            

            if scripts.saving.started_game == False:
                buttons = ['NEW GAME', 'SETTINGS', 'EXIT']
            else:
                buttons = ['CONTINUE', 'SETTINGS', 'EXIT']

            # main

            func.add_global(Decaying_Felt_Pen, "Decaying_Felt_Pen")
            func.add_global(WIDTH, "WIDTH")
            func.add_global(HEIGHT, "HEIGHT")

            cursor_rect = cursor.get_rect()
            
            s = func.load_buttons(buttons, cur_button, cursor_rect, win)

            trk_vol = 0.0 # 0.0 -> 0.5

            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()

            sfx_mixer = pygame.mixer.Channel(4)
            track_mixer = pygame.mixer.Channel(5)

            hospital = pygame.mixer.Sound('sounds/hospital.mp3')

            sfx_mixer.set_volume(0.7)
            track_mixer.set_volume(trk_vol)

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

                fade_screen.set_alpha(fade_alpha)

                win.fill((255, 255, 255))

                if not track_mixer.get_busy():
                    track_mixer.play(hospital)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if cur_button == 'EXIT':
                            pygame.quit()
                            sys.exit()
                        elif cur_button == 'NEW GAME' or cur_button == 'CONTINUE':
                            if stop_fade:
                                start_fade = True
                                
                                #pygame.mixer.quit()
                                #pygame.mouse.set_visible(True)
                                #scene_manager.change_scene('map')
                        elif cur_button == 'SETTINGS':
                            buttons = ['BACK', 'RESET SAVE']
                        elif cur_button == 'BACK':
                            if scripts.saving.started_game == False:
                                buttons = ['NEW GAME', 'SETTINGS', 'EXIT']
                            else:
                                buttons = ['CONTINUE', 'SETTINGS', 'EXIT']
                        elif cur_button == 'RESET SAVE':
                            scripts.saving.save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')
                            pygame.quit()
                            os.system('python main.py') 
                        # scripts.saving.save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')

                title ='Organ Trafficking  FPS: ' + str(int(clock.get_fps())) + ' - Menu'

                fade_time += 50 * dt

                if fade_time > 0.001 and not stop_fade:
                    fade_time = 0
                    if fade_alpha > 1:
                        fade_alpha -= 2
                        trk_vol += 0.0038
                        track_mixer.set_volume(trk_vol)
                    else:
                        stop_fade = True
                        #trk_vol -= 0.002

                print(trk_vol)

                if start_fade:
                    fade_time += 50 * dt

                    if fade_time > 0.001:
                        fade_time = 0
                        if fade_alpha < 255:
                            fade_alpha += 2
                            trk_vol -= 0.002
                            track_mixer.set_volume(trk_vol)
                        else:
                            pygame.mixer.quit()
                            pygame.mouse.set_visible(True)
                            self.change_scene('map')
                            
                pygame.display.set_caption(title)

                win.blit(background, (0, 0))
                win.blit(title_render, (200, 60))

                cur_button = func.load_buttons(buttons, cur_button, cursor_rect, win)

                win.blit(vignette, (0, 0))

                win.blit(cursor, (mx - 8, my - 15))

                win.blit(fade_screen, (0, 0))
                
                clock.tick(144)
                
                pygame.display.flip()

        elif self.current_scene == 'map': # ----------------------MAP----------------------------
            import pygame, json, os, sys, time
            import scripts.saving


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
                cursor = pygame.image.load(f'assets\\cursor\\cursor_{str(frame)}.png').convert_alpha()
                return cursor

            def flag_set(frame):
                flag = pygame.image.load(f'assets\\animations\\flag\\flag_{str(frame)}.png').convert_alpha()
                return flag

            def guy_set_idle(frame):
                guy_idle = pygame.image.load(f'assets\\people\\guy\\idle_{str(frame)}.png').convert()
                guy_idle.set_colorkey((255, 255, 255))
                return guy_idle
                
            def guy_set_interact(frame):
                guy_interact = pygame.image.load(f'assets\\people\\guy\\interact_{str(frame)}.png').convert()
                guy_interact.set_colorkey((255, 255, 255))
                return guy_interact
                
            guy_idle = guy_set_idle(guy_idle_frame)
            guy_interact = guy_set_interact(guy_interact_frame)
            cursor = cursor_set(cursor_idle_frame)

            flag = flag_set(flag_frame)

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

            self.started = True

            scripts.saving.sv_read()
            scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()
                
                win.fill((255,255,255))

                #print(self.money)
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
                            
                        guy_idle = guy_set_idle(guy_idle_frame)
                elif guy_anim == 1:
                    if guy_interact_time >= 0.1:
                        if guy_interact_frame <= 1:

                            guy_interact_time = 0
                            
                            guy_interact_frame += 1
                                
                            guy_interact = guy_set_interact(guy_interact_frame)

                if flag_time >= 0.5:
                    if flag_frame <= 1:
                        flag_time = 0
                        
                        flag_frame += 1

                        flag = flag_set(flag_frame)
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
                            fade_screen.set_alpha(0)
                            
                            pygame.mixer.quit()
                            self.change_scene('hallway')
                        else:
                            self.change_scene('shop')

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)

                win.blit(fade_screen, (0, 0))

                #win.blit(cursor, (mx, my))
                
                clock.tick(144)
                
                pygame.display.flip()
            
        elif self.current_scene == 'hallway': # ----------------------HALLWAY----------------------------
            import pygame, json, os, sys, time
            import scripts.saving

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
                speech_bubble = pygame.image.load(f'assets\\animations\\speech bubble\\bubble_{str(frame)}.png').convert_alpha()
                speech_bubble = pygame.transform.scale(speech_bubble, (200, 200))
                return speech_bubble

            speech_bubble = set_speech_bubble(bubble_frame)

            warning_frame = 0
            warning_time = 0

            warning_frame_2 = 0
            warning_time_2 = 0

            def set_warning(frame):
                warning = pygame.image.load(f'assets\\ui\\pop_up_unlock_error_{str(frame)}.png').convert_alpha()
                warning = pygame.transform.scale(warning, (200, 150))
                return warning

            def set_warning_2(frame):
                warning_2 = pygame.image.load(f'assets\\ui\\pop_up_unlock_error_2_{str(frame)}.png').convert_alpha()
                warning_2 = pygame.transform.scale(warning_2, (200, 150))
                return warning_2

            warning = set_warning(warning_frame)
            warning_2 = set_warning_2(warning_frame_2)

            golf_bubble_frame = 0
            golf_bubble_time = 0

            def set_golf_bubble(frame):
                golf_bubble = pygame.image.load(f'assets\\animations\\golf bubble\\golf_bubble_{str(frame)}.png').convert_alpha()
                golf_bubble = pygame.transform.scale(golf_bubble, (155, 100))
                return golf_bubble

            golf_bubble = set_golf_bubble(golf_bubble_frame)

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

            #sv_read()

            scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
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
                            if scripts.saving.stomach_gave == False:
                                show_warning = True
                            else:
                                scene_change = 2
                                start_fade = True
                                move_next_scene = True

                    if door_3_rect.collidepoint(pygame.mouse.get_pos()):

                        if event.type == pygame.MOUSEBUTTONUP:
                            if self.gvliver:
                                start_fade = True
                                move_next_scene = True
                                move_to_end_scene = True
                            else:
                                show_warning_2 = True

                if not pygame.mixer.music.get_busy():
                    if scripts.saving.floor_kideny == True:
                        if not 'liver' in self.organs_bought:
                            pygame.mixer.music.play(start=scripts.saving.tv_stat_time)
                            
                bubble_time += 1 * dt

                if fade_alpha != 0:
                    fade_screen.set_alpha(fade_alpha)

                if bubble_time >= 0.5:
                    if bubble_frame <= 0:
                        bubble_time = 0
                        
                        bubble_frame += 1

                        speech_bubble = set_speech_bubble(bubble_frame)
                    else:
                        bubble_frame = -1

                if scripts.saving.floor_kideny == True:
                    if not 'liver' in self.organs_bought:
                        golf_bubble_time += 1 * dt

                        if golf_bubble_time >= 0.5:
                            if golf_bubble_frame <= 0:
                                golf_bubble_time = 0
                                
                                golf_bubble_frame += 1

                                golf_bubble = set_golf_bubble(golf_bubble_frame)
                            else:
                                golf_bubble_frame = -1
                            
                if show_warning:
                    warning_time += 1 * dt

                    if warning_time >= 0.5:
                        if warning_frame <= 0:
                            warning_time = 0
                            
                            warning_frame += 1

                            warning = set_warning(warning_frame)
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

                            warning_2 = set_warning_2(warning_frame_2)
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
                        
                if scripts.saving.stomach_gave == False:
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
                            pygame.mixer.quit()
                            self.change_scene('map')
                        else:
                            if move_to_end_scene:
                                scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                                pygame.mixer.quit()
                                self.change_scene('end_room')
                            elif scene_change == 1:
                                scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                                pygame.mixer.quit()
                                self.change_scene('patient_room')
                            else:
                                scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                                pygame.mixer.quit()
                                self.change_scene('patient_room_2')
                            #import scripts.states.patient_room


                win.blit(esc_text_render, (270, 20))

                if scripts.saving.stomach_gave == False:
                    win.blit(speech_bubble, (370, 70))
                else:
                    if not 'liver' in self.organs_bought:
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

        elif self.current_scene == 'shop': # ----------------------SHOP----------------------------
            import pygame, json, os, sys, time

            import scripts.saving

            pygame.init()


            WIDTH = 800
            HEIGHT = 500

            win = pygame.display.set_mode((WIDTH,HEIGHT))
            pygame.display.set_caption('Organ Trafficking')

            clock = pygame.time.Clock()
            crashed = False
            avarage_kosovar = pygame.image.load('assets\\bg.png').convert()
            stomach = pygame.image.load('assets\\organs\\stomach.png').convert_alpha()

            wallet = pygame.image.load('assets\\ui\\wallet.png').convert_alpha()
            sold_out = pygame.image.load('assets\\ui\\sold_out.png').convert_alpha()
            contract = pygame.image.load('assets\\ui\\contract.png').convert_alpha()

            contract_stomach = pygame.image.load('assets\\ui\\contract - stomach.png').convert_alpha()

            avarage_kosovar = pygame.transform.scale(avarage_kosovar, (WIDTH, HEIGHT))
            contract = pygame.transform.scale(contract, (230, 260))
            contract_stomach = pygame.transform.scale(contract_stomach, (230, 260))
            stomach = pygame.transform.scale(stomach, (170, 300))

            sold_out = pygame.transform.scale(sold_out, (270, 200))

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            # Animation Assets

            frame_signature = 0
            signature_animation = pygame.image.load(f'assets\\animations\\signature\{frame_signature}.png').convert_alpha()

            signiture_counter_movement_y = 0
            fade_alpha = 255


            stomach_rect = pygame.Rect(570, 160, 160, 270)
            wallet_rect = pygame.Rect(0, 430, 800, 270)
            hovered_stomach = False
            show_contract = False

            contract_y_anim = 500
            vel_anim_y = 0

            wallet_y = 430
            wallet_alpha = 125

            organs_bought = self.organs_bought


            sfx_mixer = pygame.mixer.Channel(4)

            contract_slide_1 = pygame.mixer.Sound('sounds/contract_slide_1.mp3')
            contract_slide_2 = pygame.mixer.Sound('sounds/contract_slide_2.mp3')
            contract_sign = pygame.mixer.Sound('sounds/contract_sign.mp3')

            failed_purchase = pygame.mixer.Sound('sounds/failed_purchase.mp3')
            wallet_open = pygame.mixer.Sound('sounds/wallet_open.mp3')

            sfx_mixer.set_volume(0.5)

            stomach_sold_out = False
            title = ''

            scripts.saving.sv_read()

            Currenct_Font = pygame.font.Font('fonts/Cash Currency.ttf', 32)
            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32)

            money = scripts.saving.money
            prev_time = time.time()

            """
            {
                "Game_Data": [
                    {
                    "money": 800,
                    "organs_bought": []
                    }
                ]
            }
            """

            esc_text_render = HighVoltage_Rough_Font.render('Press ESC to leave shop', True, (0, 0, 0))

            # LOAD SAVE


            money_currenct_render = Currenct_Font.render(str(money), True, (109, 34, 29))
            money_currenct_render = pygame.transform.rotozoom(money_currenct_render, 5, 1)

            if "stomach" in self.organs_bought:
                stomach_sold_out = True



            def buy_window(title, show_contract, organs_bought):
                #global show_contract, organs_bought

                if not show_contract:
                    sfx_mixer.play(contract_slide_1)
                
                show_contract = True
                organs_bought.append(title)

                return show_contract, organs_bought
                    
            def draw_sold_out(stomach_sold_out, organs_bought):
                if not stomach_sold_out or not'stomach' in organs_bought:
                    win.blit(sold_out, (520, 250))

            def wallet_anim(action, wallet_y, wallet_alpha, money_currenct_render):

                if action == 1:
                    if wallet_y >= 200:
                        wallet_y -= 10
                        wallet_alpha += 11
                        wallet.set_alpha(wallet_alpha)
                        money_currenct_render.set_alpha(wallet_alpha + 30)
                else:
                    if wallet_y <= 430:
                        wallet_y += 10
                        wallet_alpha -= 11
                        wallet.set_alpha(wallet_alpha)
                        money_currenct_render.set_alpha(wallet_alpha + 30)

                return wallet_y, wallet_alpha

            def reload_money_counter(money):
                global money_currenct_render

                money_currenct_render = Currenct_Font.render(str(money), True, (109, 34, 29))
                money_currenct_render = pygame.transform.rotozoom(money_currenct_render, 5, 1)

                money_currenct_render.set_alpha(wallet_alpha + 30)

                return money, money_currenct_render

            wallet.set_alpha(wallet_alpha)
            money_currenct_render.set_alpha(wallet_alpha + 30)

            scripts.saving.save(money_=money, organs_bought_=organs_bought,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
            signature_delay, contract_leave_delay = 0, 0

            fade_screen.set_alpha(fade_alpha)
            start_fade = False

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()
                
                if fade_alpha != 0:
                    fade_screen.set_alpha(fade_alpha)

                clock.tick(144)
                win.fill((255,255,255))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(money_=money, organs_bought_=organs_bought,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                start_fade = True
                                self.money = money
                    if stomach_rect.collidepoint(pygame.mouse.get_pos()) and not show_contract:
                        if not stomach_sold_out or not'stomach' in organs_bought:
                            hovered_stomach = True
                            if event.type == pygame.MOUSEBUTTONUP:
                                if money >= 560:
                                    signature_delay, contract_leave_delay = 0, 0
                                    title = "stomach"
                                    show_contract, organs_bought = buy_window(title, show_contract, organs_bought)
                                    money -= 560
                                    scripts.saving.save(money_=money, organs_bought_=organs_bought,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                                    money, money_currenct_render = reload_money_counter(money)
                                    scripts.saving.sv_read()
                                else:
                                    sfx_mixer.play(failed_purchase)
                    else:
                        hovered_stomach = False

                    if wallet_rect.collidepoint(pygame.mouse.get_pos()) and not show_contract:
                        wallet_args = 1 # wallet move up
                        if wallet_y >= 430:
                            sfx_mixer.play(wallet_open)
                    else:
                        wallet_args = 0 # wallet move down

                win.blit(avarage_kosovar, (0, 0))

                if hovered_stomach and not show_contract:
                    # display_surface.blit(funy, effects.shake.smoothshake((cur_x, Y // 2), 15))
                    win.blit(stomach, shake((570, 170), 4))

                win.blit(sold_out, (180, 240))
                win.blit(sold_out, (340, 290))
                contract_y_anim, signiture_counter_movement_y, money, vel_anim_y, signature_delay, frame_signature, contract_leave_delay, show_contract, stomach_sold_out = func.check_contract_anmation(title, show_contract, contract_y_anim, signiture_counter_movement_y, vel_anim_y, win,
                                                                                                    contract, contract_stomach, frame_signature, signature_delay, money, sfx_mixer, contract_sign, contract_leave_delay, contract_slide_2, stomach_sold_out)
                wallet_y, wallet_alpha = wallet_anim(wallet_args, wallet_y, wallet_alpha, money_currenct_render)
                if stomach_sold_out:
                    win.blit(sold_out, (520, 250))

                print(stomach_sold_out)

                win.blit(wallet, (0, wallet_y))
                win.blit(money_currenct_render, (225, wallet_y + 20))

                win.blit(esc_text_render, (340, 20))

                if fade_alpha >= 1 and start_fade == False:
                    fade_alpha -= 300 * dt

                if start_fade == True:
                    if fade_alpha <= 255:
                        fade_alpha += 300 * dt
                    else:

                        pygame.mixer.quit()
                        self.change_scene('map')
                        #import scripts.states.map

                title_ ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title_)
                
                win.blit(fade_screen, (0, 0))
                        
                pygame.display.update()
                pygame.display.flip()
        elif self.current_scene == 'patient_room': # ----------------------PATIENT_ROOM----------------------------
            import pygame, json, os, sys, time
            import scripts.saving

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
                return sparkle

            sparkle = set_sparkle(sparkle_frame)


            poster_frame = 0
            poster_time = 0

            def set_poster(frame):
                global poster
                poster = pygame.image.load(f'assets\\animations\\poster\\poster_{str(frame)}.png').convert_alpha()
                poster = pygame.transform.scale(poster, (140, 160))
                return poster

            poster = set_poster(poster_frame)

            golf_bubble_frame = 0
            golf_bubble_time = 0

            def set_golf_bubble(frame):
                global golf_bubble
                golf_bubble = pygame.image.load(f'assets\\animations\\golf bubble\\golf_bubble_{str(frame)}.png').convert_alpha()
                golf_bubble = pygame.transform.scale(golf_bubble, (185, 120))
                return golf_bubble

            golf_bubble = set_golf_bubble(golf_bubble_frame)

            patient_frame = 0
            patient_time = 0

            def set_patient(frame):
                global patient
                patient = pygame.image.load(f'assets\\people\\patient\\patient_{str(frame)}.png').convert()
                patient = pygame.transform.scale(patient, (140, 110))
                patient.set_colorkey((255, 255, 255))
                return patient

            patient = set_patient(patient_frame)

            organ_bubble_frame = 0
            organ_bubble_time = 0

            def set_organ_bubble(frame):
                global organ_bubble
                organ_bubble = pygame.image.load(f'assets\\animations\\bubble organ\\bubble_{str(frame)}.png').convert_alpha()
                organ_bubble = pygame.transform.scale(organ_bubble, (110, 90))
                return organ_bubble

            organ_bubble = set_organ_bubble(organ_bubble_frame)

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

            scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000), money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
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

                            if self.stomach_gave == False and "stomach" in self.organs_bought:
                                self.stomach_gave = True
                                scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                                change_to_present = True
                                start_fade = True
                            else:
                                if scripts.saving.stomach_gave == False:
                                    organ_mixer.play(no_organ)
                    else:
                        hover_over_patient = False
                            
                if fade_alpha != 0:
                    fade_screen.set_alpha(fade_alpha)

                if scripts.saving.stomach_gave == False:
                    if not sfx_mixer.get_busy():
                        sfx_mixer.play(dim_angry_chattering)

                patient_time += 1 * dt

                if patient_time >= 0.5:
                    if patient_frame <= 2:
                        patient_time = 0
                        
                        patient_frame += 1

                        patient = set_patient(patient_frame)
                    else:
                        patient_frame = -1

                if self.organ[0] == True:
                    if not 'liver' in self.organs_bought:
                        golf_bubble_time += 1 * dt

                        if golf_bubble_time >= 0.5:
                            if golf_bubble_frame <= 0:
                                golf_bubble_time = 0
                                
                                golf_bubble_frame += 1

                                golf_bubble = set_golf_bubble(golf_bubble_frame)
                            else:
                                golf_bubble_frame = -1
                        
                if self.organ[1] == False:
                    organ_bubble_time += 1 * dt

                    if organ_bubble_time >= 0.5:
                        if organ_bubble_frame <= 0:
                            organ_bubble_time = 0
                            
                            organ_bubble_frame += 1

                            organ_bubble = set_organ_bubble(organ_bubble_frame)
                        else:
                            organ_bubble_frame = -1

                poster_time += 1 * dt

                if poster_time >= 0.2:
                    if poster_frame <= 0:
                        poster_time = 0
                        
                        poster_frame += 1

                        poster = set_poster(poster_frame)
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

                            sparkle = set_sparkle(sparkle_frame)
                        else:
                            sparkle_frame = -1

                if not pygame.mixer.music.get_busy():
                    if self.organ[0]:
                        if not 'liver' in self.organs_bought:
                            pygame.mixer.music.play(start=scripts.saving.tv_stat_time)
                    
                win.fill((255,255,255))
                
                win.blit(patient_room, (0, 0))
                win.blit(patient, (350, 250))

                if self.organ[0]:
                    win.blit(kideny_on_floor, (369, 380))
                    if not 'liver' in self.organs_bought:
                        win.blit(golf_bubble, (20, 230))

                win.blit(poster, (90, 140))

                # pygame.draw.rect(win, (230, 50, 50), patient_rect)

                if show_sparkles:
                    win.blit(sparkle, (160, 150))

                # pygame.draw.rect(win, (250, 20, 20), poster_rect)

                if hover_over_patient:
                    if scripts.saving.stomach_gave == False:
                        win.blit(organ_bubble, (340, 170))
                        win.blit(kideny, (380, 190))

                if fade_alpha >= 1 and start_fade == False:
                    fade_alpha -= 300 * dt

                if start_fade == True:
                    if fade_alpha <= 255:
                        fade_alpha += 300 * dt
                    else:
                        if change_to_present == True:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('present')
                        elif change_to_game == True:
                            fade_screen.set_alpha(0)
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('skely')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('hallway')

                win.blit(esc_text_render, (220, 20))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)

                pygame.display.update()
                pygame.display.flip()
        elif self.current_scene == 'skely': # ----------------------SKELY----------------------------
            import pygame, json, os, sys, time, random

            

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
                poster = pygame.image.load(f'assets\\skely\\background\\background_{str(frame)}.png').convert()
                poster = pygame.transform.scale(poster, (WIDTH, HEIGHT))
                return poster

            poster = set_poster(poster_frame)

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
            money = self.money

            ammount = 1

            scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)

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
                        scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.quit()
                        quit()
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                                self.money = self.money
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
                                self.money += random.randint(3, 11)
                                money = self.money
                                reload_money_counter()

                if fade_alpha != 0:
                    fade_screen.set_alpha(fade_alpha)

                poster_time += 1 * dt

                if poster_time >= 0.5:
                    if poster_frame <= 0:
                        poster_time = 0
                        
                        poster_frame += 1

                        poster = set_poster(poster_frame)
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
                    scripts.saving.save(money_=self.money,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
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
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.mixer.quit()
                        self.change_scene('patient_room')

                # win.blit(esc_text_render, (220, 20))
                win.blit(money_text_render, (70, 50))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'present': # ----------------------PRESENT----------------------------
            import pygame, json, os, sys, time

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
                background = pygame.image.load(f'assets\\present\\background\\background_{str(frame)}.png').convert_alpha()
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                return background

            background = set_background(background_frame)

            present_frame = 0
            present_time = 0

            def set_present(frame):
                present = pygame.image.load(f'assets\\present\\present\\idle_{str(frame)}.png').convert_alpha()
                #present = pygame.transform.scale(present, (WIDTH, HEIGHT))
                return present

            present = set_present(present_frame)


            confetti_frame = 0
            confetti_time = 0

            def set_confetti(frame):
                confetti = pygame.image.load(f'assets\\present\\confeti\\confetti_{str(frame)}.png').convert_alpha()
                #present = pygame.transform.scale(present, (WIDTH, HEIGHT))
                return confetti

            confetti = set_confetti(confetti_frame)


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

            self.organ = (True, True)

            scripts.saving.save(floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,money_=self.money)

            import scripts.saving
            scripts.saving.sv_read()

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,money_=self.money)
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
                background_time += 2 * dt

                if fade_alpha != 0:
                    fade_screen.set_alpha(fade_alpha)

                if not opened:
                    if present_time >= 0.5:
                        if present_frame <= 0:
                            present_time = 0
                            
                            present_frame += 1

                            present = set_present(present_frame)
                        else:
                            present_frame = -1

                if background_time >= 0.5:
                    if background_frame <= 0:
                        background_time = 0
                        
                        background_frame += 1

                        background = set_background(background_frame)
                    else:
                        background_frame = -1

                if play_confetti:
                    confetti_time += 1 * dt
                    
                    if confetti_time >= 0.05:
                        if confetti_frame <= 10:
                            confetti_time = 0
                            
                            confetti_frame += 1

                            confetti = set_confetti(confetti_frame)
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
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.mixer.quit()
                        self.change_scene('patient_room')

                # win.blit(esc_text_render, (220, 20))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'patient_room_2': # ----------------------PATIENT ROOM 2----------------------------
            import pygame, json, os, sys, time, cv2
            import pygame.mixer

            import scripts.saving

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
                patient_2 = pygame.image.load(f'assets\\people\\patient 2\\patient_2_{str(frame)}.png').convert_alpha()
                patient_2 = pygame.transform.scale(patient_2, (319, 246))
                return patient_2

            patient_2 = set_patient_2(patient_2_frame)

            organ_bubble_time = 0
            organ_bubble_frame = 0

            def set_organ_bubble(frame):
                organ_bubble = pygame.image.load(f'assets\\animations\\bubble organ\\bubble_{str(frame)}.png').convert_alpha()
                organ_bubble = pygame.transform.scale(organ_bubble, (130, 100))
                return organ_bubble

            organ_bubble = set_organ_bubble(organ_bubble_frame)

            tv_back_panel_time = 0
            tv_back_panel_frame = 0

            def set_tv_back_panel(frame):
                tv_back_panel = pygame.image.load(f'assets\\animations\\tv\\back_plate_{str(frame)}.png').convert_alpha()
                tv_back_panel = pygame.transform.scale(tv_back_panel, (130, 100))
                return tv_back_panel

            tv_back_panel = set_tv_back_panel(tv_back_panel_frame)

            tv_front_panel_time = 0
            tv_front_panel_frame = 0

            def set_tv_front_panel(frame):
                tv_front_panel = pygame.image.load(f'assets\\animations\\tv\\front_plate_{str(frame)}.png').convert_alpha()
                tv_front_panel = pygame.transform.scale(tv_front_panel, (130, 100))
                return tv_front_panel

            tv_front_panel = set_tv_front_panel(tv_front_panel_frame)

            sparkle_frame = 0
            sparkle_time = 0

            def set_sparkle(frame):
                sparkle = pygame.image.load(f'assets\\animations\\sparkle\\sparkle_{str(frame)}.png').convert_alpha()
                # sparkle = pygame.transform.scale(sparkle, (140, 160))
                return sparkle

            sparkle = set_sparkle(sparkle_frame)

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
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.quit()
                        quit()
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                start_fade = True

                    if patient_2_rect.collidepoint(pygame.mouse.get_pos()):
                        if not self.gvliver:
                            hovered_over_patient_2 = True

                            if event.type == pygame.MOUSEBUTTONUP:
                                if not 'liver' in self.organs_bought:
                                    sfx_mixer.play(no_organ)
                                else:
                                    start_fade = True
                                    present_2 = True
                    else:
                        hovered_over_patient_2 = False

                    if tv_rect.collidepoint(pygame.mouse.get_pos()):
                        if not 'liver' in self.organs_bought:
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

                        patient_2 = set_patient_2(patient_2_frame)
                    else:
                        patient_2_frame = -1

                organ_bubble_time += 1 * dt

                if organ_bubble_time >= 0.5:
                    if organ_bubble_frame <= 0:
                        organ_bubble_time = 0
                        
                        organ_bubble_frame += 1

                        organ_bubble = set_organ_bubble(organ_bubble_frame)
                    else:
                        organ_bubble_frame = -1

                tv_back_panel_time += 1 * dt

                if tv_back_panel_time >= 0.7:
                    if tv_back_panel_frame <= 0:
                        tv_back_panel_time = 0
                        
                        tv_back_panel_frame += 1

                        tv_back_panel = set_tv_back_panel(tv_back_panel_frame)
                    else:
                        tv_back_panel_frame = -1

                tv_front_panel_time += 1 * dt

                if tv_front_panel_time >= 0.7:
                    if tv_front_panel_frame <= 0:
                        tv_front_panel_time = 0
                        
                        tv_front_panel_frame += 1

                        tv_front_panel = set_tv_front_panel(tv_front_panel_frame)
                    else:
                        tv_front_panel_frame = -1

                if not pygame.mixer.music.get_busy():
                    if scripts.saving.floor_kideny == True:
                        if not 'liver' in self.organs_bought:
                            pygame.mixer.music.play(start=scripts.saving.tv_stat_time)
                    
                if show_sparkles:
                    sparkle_time += 1 * dt

                    if not sparkle_mixer.get_busy():
                        sparkle_mixer.play(sparkle_sfx)

                    if sparkle_time >= 0.1:
                        if sparkle_frame <= 5:
                            sparkle_time = 0
                            
                            sparkle_frame += 1

                            sparkle = set_sparkle(sparkle_frame)
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

                if not 'liver' in self.organs_bought:
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

                if self.gvliver:
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
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('present_2')
                        elif not move_to_golf:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('hallway')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene(f'golf_lvl_{self.golf_level}')

                win.blit(esc_text_render, (220, 20))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()



        elif self.current_scene == 'golf_lvl_1': # ----------------------GOLF LEVEL 1----------------------------

            
            """
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf golf
            
            """

            import pygame, json, os, sys, time, math, random
            import scripts.saving

            pygame.init()


            WIDTH = 800
            HEIGHT = 500

            win = pygame.display.set_mode((WIDTH,HEIGHT))
            pygame.display.set_caption('Organ Trafficking')

            clock = pygame.time.Clock()

            arrow_background = pygame.image.load(f'assets\\golf\\arrow\\bg.png').convert()
            background = pygame.image.load(f'assets\\golf\\background.png').convert()
            arrow = pygame.image.load(f'assets\\golf\\arrow\\arrow.png').convert_alpha()

            bar = pygame.image.load(f'assets\\golf\\bar.png').convert()
            tutorial_text = pygame.image.load(f'assets\\golf\\tutorial_text.png').convert_alpha()

            vignette = pygame.image.load(f'assets\\golf\\vignette.png').convert_alpha()

            vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))
            tutorial_text = pygame.transform.scale(tutorial_text, (270, 210))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            arrow_background = pygame.transform.scale(arrow_background, (WIDTH, HEIGHT))
            bar = pygame.transform.scale(bar, (650, 30))


            eye_frame = 0
            eye_time = 0

            def set_eye_roll(frame):
                eye = pygame.image.load(f'assets\\golf\\eye\\eye_roll_0_{str(frame)}.png').convert_alpha()
                eye = pygame.transform.scale(eye, (20, 20))
                return eye

            eye = set_eye_roll(eye_frame)

            flag_frame = 0
            flag_time = 0

            def set_flag(frame):
                flag = pygame.image.load(f'assets\\golf\\finish_flag\\finish_flag_{str(frame)}.png').convert_alpha()
                flag = pygame.transform.scale(flag, (60, 110))
                return flag

            flag = set_flag(flag_frame)

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            fade_alpha = 255
            shots_left = 1

            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
            Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
            BadlyStamped_Font = pygame.font.Font('fonts/BadlyStamped.ttf', 32)

            def set_shots_text_render():
                shots_left_text_render = BadlyStamped_Font.render(f'SHOTS LEFT {str(shots_left)}', True, (0, 0, 0))
                return shots_left_text_render

            shots_left_text_render = set_shots_text_render()

            prev_time = time.time()
            fade_screen.set_alpha(fade_alpha)

            controlling_golf_ball = False
            golf_ball_end_vel = False
            shoot_golf_ball = False
            start_fade = False
            next_level = False
            bar_shown = True

            golf_ball_col = [130, 120]
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

            collisions = [False] * 9

            simpler_collisions = [False] * 5  # top bottom right left
            last_collisions = [False] * 5

            angle = 0

            golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)
            sand_pos = (620, 200)

            win_rect = pygame.Rect(660, 340, 30, 15)

            track_mixer = pygame.mixer.Channel(4)
            sfx_mixer = pygame.mixer.Channel(5)

            golf_song = pygame.mixer.Sound('sounds/golf.mp3')

            club_0 = pygame.mixer.Sound('sounds/club_0.mp3')
            club_1 = pygame.mixer.Sound('sounds/club_1.mp3')
            club_2 = pygame.mixer.Sound('sounds/club_2.mp3')

            track_mixer.set_volume(0.4)
            sfx_mixer.set_volume(0.6)

            restart = False

            self.golf_level = 1

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                mx, my = pygame.mouse.get_pos()
                collision = False

                if not track_mixer.get_busy():
                    track_mixer.play(golf_song)

                if shots_left == 0 and not shoot_golf_ball and not next_level:
                    restart = True
                    start_fade = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                        pygame.quit()
                        quit()

                    """

                    Hold Space To Aim The Golf Ball

                    Release Space To Shoot The Golf Ball
                    
                    """
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
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

                                    shots_left -= 1; shots_left_text_render = set_shots_text_render()

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

                golf_ball_rect = pygame.Rect(golf_ball_col[0]-10, golf_ball_col[1]-10,   10*2, 10*2 )

                vignette.set_alpha(50)

                #golf_song.set_volume(float(0.4 - vignette_alpha // 3))

                #print(float(0.4 - vignette_alpha // 85))

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
                    next_level = True
                    start_fade = True

                #print(overlap_sand_mask.count())

                eye_time += 0.6 * dt

                if eye_time >= 0.5:
                    if eye_frame <= 0:
                        eye_time = 0
                        
                        eye_frame += 1

                        eye = set_eye_roll(eye_frame)
                    else:
                        eye_frame = -1


                flag_time += 0.4 * dt

                if flag_time >= 0.5:
                    if flag_frame <= 0:
                        flag_time = 0
                        
                        flag_frame += 1

                        flag = set_flag(flag_frame)
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

                win.blit(tutorial_text, (160, 200))
                
                #pygame.draw.circle(win, (0, 255, 0), golf_ball_col, 10, 0)
                if not next_level:
                    win.blit(eye, (golf_ball_rect.x, golf_ball_rect.y))
                win.blit(flag, (640, 260))

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
                        if next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_2')
                        if restart and not next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_1')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('patient_room_2')
                        
                win.blit(shots_left_text_render, (230, 20))
                win.blit(vignette, (0, 0))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'golf_lvl_2': # ----------------------GOLF LEVEL 2----------------------------
            import pygame, json, os, sys, time, math, random
            import scripts.saving

            pygame.init()


            WIDTH = 800
            HEIGHT = 500

            win = pygame.display.set_mode((WIDTH,HEIGHT))
            pygame.display.set_caption('Organ Trafficking')

            clock = pygame.time.Clock()

            arrow_background = pygame.image.load(f'assets\\golf\\arrow\\bg.png').convert()
            background = pygame.image.load(f'assets\\golf\\background.png').convert()
            arrow = pygame.image.load(f'assets\\golf\\arrow\\arrow.png').convert_alpha()

            sand_0 = pygame.image.load('assets\\golf\\sand\\sand_0.png').convert()
            sand_0.set_colorkey((0, 0, 0))

            sand_1 = pygame.image.load('assets\\golf\\sand\\sand_1.png').convert()
            sand_1 = pygame.transform.flip(sand_1, True, True)
            sand_1.set_colorkey((0, 0, 0))

            bar = pygame.image.load(f'assets\\golf\\bar.png').convert()
            tutorial_2_text = pygame.image.load(f'assets\\golf\\tutorial_2_text.png').convert_alpha()

            vignette = pygame.image.load(f'assets\\golf\\vignette.png').convert_alpha()

            vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))
            tutorial_2_text = pygame.transform.scale(tutorial_2_text, (170, 210))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            arrow_background = pygame.transform.scale(arrow_background, (WIDTH, HEIGHT))
            bar = pygame.transform.scale(bar, (650, 30))
            sand_0 = pygame.transform.scale(sand_0, (450, 380))
            sand_1 = pygame.transform.scale(sand_1, (450, 580))

            #sand_0 = pygame.transform.scale(sand_0, (110, 150))
            sand_0_mask = pygame.mask.from_surface(sand_0)
            sand_1_mask = pygame.mask.from_surface(sand_1)

            eye_frame = 0
            eye_time = 0

            def set_eye_roll(frame):
                eye = pygame.image.load(f'assets\\golf\\eye\\eye_roll_0_{str(frame)}.png').convert_alpha()
                eye = pygame.transform.scale(eye, (20, 20))
                return eye

            eye = set_eye_roll(eye_frame)

            flag_frame = 0
            flag_time = 0

            def set_flag(frame):
                flag = pygame.image.load(f'assets\\golf\\finish_flag\\finish_flag_{str(frame)}.png').convert_alpha()
                flag = pygame.transform.scale(flag, (60, 110))
                return flag

            flag = set_flag(flag_frame)

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            fade_alpha = 255
            shots_left = 2

            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
            Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
            BadlyStamped_Font = pygame.font.Font('fonts/BadlyStamped.ttf', 32)

            def set_shots_text_render():
                shots_left_text_render = BadlyStamped_Font.render(f'SHOTS LEFT {str(shots_left)}', True, (0, 0, 0))
                return shots_left_text_render

            shots_left_text_render = set_shots_text_render()

            prev_time = time.time()
            fade_screen.set_alpha(fade_alpha)

            controlling_golf_ball = False
            golf_ball_end_vel = False
            shoot_golf_ball = False
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

            sand_pos = (150, 240)
            sand_1_pos = (170, -220)

            collisions = [False] * 9

            simpler_collisions = [False] * 5  # top bottom right left
            last_collisions = [False] * 5

            angle = 0

            golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)

            win_rect = pygame.Rect(680, 430, 30, 15)

            track_mixer = pygame.mixer.Channel(4)
            sfx_mixer = pygame.mixer.Channel(5)

            golf_song = pygame.mixer.Sound('sounds/golf.mp3')

            club_0 = pygame.mixer.Sound('sounds/club_0.mp3')
            club_1 = pygame.mixer.Sound('sounds/club_1.mp3')
            club_2 = pygame.mixer.Sound('sounds/club_2.mp3')

            track_mixer.set_volume(0.4)
            sfx_mixer.set_volume(0.6)

            self.golf_level = 2

            restart = False

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)
                overlap_sand_mask = golf_ball_mask.overlap_mask(sand_0_mask, (sand_pos[0] - golf_ball_rect.x, sand_pos[1] - golf_ball_rect.y))
                overlap_1_sand_mask = golf_ball_mask.overlap_mask(sand_1_mask, (sand_1_pos[0] - golf_ball_rect.x, sand_1_pos[1] - golf_ball_rect.y))

                mx, my = pygame.mouse.get_pos()
                collision = False

                if not track_mixer.get_busy():
                    track_mixer.play(golf_song)

                if shots_left == 0 and not shoot_golf_ball and not next_level:
                    restart = True
                    start_fade = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                        pygame.quit()
                        quit()

                    """

                    Hold Space To Aim The Golf Ball

                    Release Space To Shoot The Golf Ball
                    
                    """
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
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

                                    shots_left -= 1; shots_left_text_render = set_shots_text_render()

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
                    next_level = True
                    start_fade = True

                #print(overlap_sand_mask.count())

                eye_time += 0.6 * dt

                if eye_time >= 0.5:
                    if eye_frame <= 0:
                        eye_time = 0
                        
                        eye_frame += 1

                        eye = set_eye_roll(eye_frame)
                    else:
                        eye_frame = -1


                flag_time += 0.4 * dt

                if flag_time >= 0.5:
                    if flag_frame <= 0:
                        flag_time = 0
                        
                        flag_frame += 1

                        flag = set_flag(flag_frame)
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

                win.blit(tutorial_2_text, (30, 250))
                
                #pygame.draw.circle(win, (0, 255, 0), golf_ball_col, 10, 0)
                win.blit(sand_0, (150, 240))
                win.blit(sand_1, (sand_1_pos[0], sand_1_pos[1]))
                
                if not next_level:
                    win.blit(eye, (golf_ball_rect.x, golf_ball_rect.y))
                win.blit(flag, (660, 350))

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
                        if next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_3') 
                        if restart and not next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_2')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('patient_room_2')
                        
                win.blit(shots_left_text_render, (230, 20))
                win.blit(vignette, (0, 0))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()

        elif self.current_scene == 'golf_lvl_3': # ----------------------GOLF LEVEL 3----------------------------
            import pygame, json, os, sys, time, math, random
            import scripts.saving

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
                eye = pygame.image.load(f'assets\\golf\\eye\\eye_roll_0_{str(frame)}.png').convert_alpha()
                eye = pygame.transform.scale(eye, (20, 20))
                return eye

            eye = set_eye_roll(eye_frame)

            flag_frame = 0
            flag_time = 0

            def set_flag(frame):
                flag = pygame.image.load(f'assets\\golf\\finish_flag\\finish_flag_{str(frame)}.png').convert_alpha()
                flag = pygame.transform.scale(flag, (60, 110))
                return flag

            flag = set_flag(flag_frame)

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            fade_alpha = 255
            shots_left = 1

            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
            Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
            BadlyStamped_Font = pygame.font.Font('fonts/BadlyStamped.ttf', 32)

            def set_shots_text_render():
                shots_left_text_render = BadlyStamped_Font.render(f'SHOTS LEFT {str(shots_left)}', True, (0, 0, 0))
                return shots_left_text_render

            shots_left_text_render = set_shots_text_render()

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

            self.golf_level = 3

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
                        scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                        pygame.quit()
                        quit()

                    """

                    Hold Space To Aim The Golf Ball

                    Release Space To Shoot The Golf Ball
                    
                    """
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
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

                                    shots_left -= 1; shots_left_text_render = set_shots_text_render()

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

                        eye = set_eye_roll(eye_frame)
                    else:
                        eye_frame = -1


                flag_time += 0.4 * dt

                if flag_time >= 0.5:
                    if flag_frame <= 0:
                        flag_time = 0
                        
                        flag_frame += 1

                        flag = set_flag(flag_frame)
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
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_4') 
                        elif restart and not next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_3')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('patient_room_2')
                        
                win.blit(shots_left_text_render, (230, 20))
                win.blit(vignette, (0, 0))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'golf_lvl_4': # ----------------------GOLF LEVEL 4----------------------------
            import pygame, json, os, sys, time, math, random
            import scripts.saving

            pygame.init()


            WIDTH = 800
            HEIGHT = 500

            win = pygame.display.set_mode((WIDTH,HEIGHT))
            pygame.display.set_caption('Organ Trafficking')

            clock = pygame.time.Clock()

            arrow_background = pygame.image.load(f'assets\\golf\\arrow\\bg.png').convert()
            background = pygame.image.load(f'assets\\golf\\background.png').convert()
            arrow = pygame.image.load(f'assets\\golf\\arrow\\arrow.png').convert_alpha()

            sand_1 = pygame.image.load('assets\\golf\\sand\\sand_2.png').convert()
            sand_1.set_colorkey((0, 0, 0))

            water_0 = pygame.image.load('assets\\golf\\water\\water_1.png').convert()
            water_0.set_colorkey((0, 0, 0))

            bar = pygame.image.load(f'assets\\golf\\bar.png').convert()

            vignette = pygame.image.load(f'assets\\golf\\vignette.png').convert_alpha()

            vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            arrow_background = pygame.transform.scale(arrow_background, (WIDTH, HEIGHT))
            bar = pygame.transform.scale(bar, (650, 30))

            #sand_0 = pygame.transform.scale(sand_0, (110, 150))
            sand_1_mask = pygame.mask.from_surface(sand_1)
            water_0_mask = pygame.mask.from_surface(water_0)

            eye_frame = 0
            eye_time = 0

            def set_eye_roll(frame):
                eye = pygame.image.load(f'assets\\golf\\eye\\eye_roll_0_{str(frame)}.png').convert_alpha()
                eye = pygame.transform.scale(eye, (20, 20))
                return eye

            eye = set_eye_roll(eye_frame)

            flag_frame = 0
            flag_time = 0

            def set_flag(frame):
                flag = pygame.image.load(f'assets\\golf\\finish_flag\\finish_flag_{str(frame)}.png').convert_alpha()
                flag = pygame.transform.scale(flag, (60, 110))
                return flag

            flag = set_flag(flag_frame)

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            fade_alpha = 255
            shots_left = 2

            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
            Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
            BadlyStamped_Font = pygame.font.Font('fonts/BadlyStamped.ttf', 32)

            def set_shots_text_render():
                shots_left_text_render = BadlyStamped_Font.render(f'SHOTS LEFT {str(shots_left)}', True, (0, 0, 0))
                return shots_left_text_render

            shots_left_text_render = set_shots_text_render()

            prev_time = time.time()
            fade_screen.set_alpha(fade_alpha)

            controlling_golf_ball = False
            golf_ball_end_vel = False
            shoot_golf_ball = False
            played_water = True
            start_fade = False
            next_level = False
            bar_shown = True

            golf_ball_col = [50, 320]
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

            sand_1_pos = (0, 0)
            water_pos = (0, 0)

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

            self.golf_level = 4

            scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)
                
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
                        scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                        pygame.quit()
                        quit()

                    """

                    Hold Space To Aim The Golf Ball

                    Release Space To Shoot The Golf Ball
                    
                    """
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
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

                                    shots_left -= 1; shots_left_text_render = set_shots_text_render()

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

                vignette_alpha = 50 + overlap_1_sand_mask.count() // 10

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

                        eye = set_eye_roll(eye_frame)
                    else:
                        eye_frame = -1


                flag_time += 0.4 * dt

                if flag_time >= 0.5:
                    if flag_frame <= 0:
                        flag_time = 0
                        
                        flag_frame += 1

                        flag = set_flag(flag_frame)
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

                ball_speed -= overlap_1_sand_mask.count() // 150
                
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
                
                #pygame.draw.circle(win, (0, 255, 0), golf_ball_col, 10, 0)
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
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_5') 
                        elif restart and not next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_4')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('patient_room_2')
                        
                win.blit(shots_left_text_render, (230, 20))
                win.blit(vignette, (0, 0))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'golf_lvl_5': # ----------------------GOLF LEVEL 5----------------------------
            import pygame, json, os, sys, time, math, random
            import scripts.saving

            pygame.init()


            WIDTH = 800
            HEIGHT = 500

            win = pygame.display.set_mode((WIDTH,HEIGHT))
            pygame.display.set_caption('Organ Trafficking')

            clock = pygame.time.Clock()

            arrow_background = pygame.image.load(f'assets\\golf\\arrow\\bg.png').convert()
            background = pygame.image.load(f'assets\\golf\\background.png').convert()
            arrow = pygame.image.load(f'assets\\golf\\arrow\\arrow.png').convert_alpha()
            liver = pygame.image.load(f'assets\\organs\\liver_small.png').convert_alpha()

            bar = pygame.image.load(f'assets\\golf\\bar.png').convert()
            tutorial_3_text = pygame.image.load(f'assets\\golf\\tutorial_3_text.png').convert_alpha()

            vignette = pygame.image.load(f'assets\\golf\\vignette.png').convert_alpha()

            vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))
            tutorial_3_text = pygame.transform.scale(tutorial_3_text, (170, 150))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            arrow_background = pygame.transform.scale(arrow_background, (WIDTH, HEIGHT))
            liver = pygame.transform.scale(liver, (120, 130))
            bar = pygame.transform.scale(bar, (650, 30))

            red_channel = pygame.Surface((WIDTH, HEIGHT))

            eye_frame = 0
            eye_time = 0

            def set_eye_roll(frame):
                eye = pygame.image.load(f'assets\\golf\\eye\\eye_roll_0_{str(frame)}.png').convert_alpha()
                eye = pygame.transform.scale(eye, (20, 20))
                return eye

            eye = set_eye_roll(eye_frame)

            flag_frame = 0
            flag_time = 0

            def set_flag(frame):
                flag = pygame.image.load(f'assets\\golf\\finish_flag\\finish_flag_{str(frame)}.png').convert_alpha()
                flag = pygame.transform.scale(flag, (60, 110))
                return flag

            flag = set_flag(flag_frame)

            fade_screen = pygame.Surface((WIDTH,HEIGHT))
            fade_screen.fill((0,0,0))

            fade_alpha = 255
            shots_left = 1

            HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32) # Decaying Felt Pen.ttf
            Decaying_Felt_Pen_Font = pygame.font.Font('fonts/Decaying Felt Pen.ttf', 32)
            BadlyStamped_Font = pygame.font.Font('fonts/BadlyStamped.ttf', 32)

            def set_shots_text_render():
                shots_left_text_render = BadlyStamped_Font.render('INFINITE SHOTS LEFT', True, (0, 0, 0))
                return shots_left_text_render

            shots_left_text_render = set_shots_text_render()

            prev_time = time.time()
            fade_screen.set_alpha(fade_alpha)

            controlling_golf_ball = False
            golf_ball_end_vel = False
            shoot_golf_ball = False
            played_water = True
            start_fade = False
            next_level = False
            bar_shown = True
            back = False
            STOP = False

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

            back_time = 0

            ball_speed = 3
            shown_ball_speed = 0 # bar speed

            collisions = [False] * 9

            simpler_collisions = [False] * 5  # top bottom right left
            last_collisions = [False] * 5

            angle = 0

            golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)

            win_rect = pygame.Rect(350, 200, 120, 130)

            track_mixer = pygame.mixer.Channel(4)
            sfx_mixer = pygame.mixer.Channel(5)

            golf_song = pygame.mixer.Sound('sounds/uhohohoh.mp3')

            club_0 = pygame.mixer.Sound('sounds/club_0.mp3')
            club_1 = pygame.mixer.Sound('sounds/club_1.mp3')
            club_2 = pygame.mixer.Sound('sounds/club_2.mp3')

            track_mixer.set_volume(0.4)
            sfx_mixer.set_volume(0.6)

            dont_show_eye = False
            restart = False

            self.golf_level = 5

            scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                liver_pos = smoothshake((350, 200), 129, radius=300)
                win_rect = pygame.Rect(liver_pos[0], liver_pos[1], 120, 130)

                golf_ball_mask = pygame.mask.from_surface(golf_ball_surface_rect)
                
                mx, my = pygame.mouse.get_pos()
                collision = False

                if not track_mixer.get_busy():
                    track_mixer.play(golf_song)

                if shots_left == 0 and not shoot_golf_ball and not next_level:
                    restart = True
                    start_fade = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                        pygame.quit()
                        quit()

                    """

                    Hold Space To Aim The Golf Ball

                    Release Space To Shoot The Golf Ball
                    
                    """
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
                                scripts.saving.save(golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                                start_fade = True

                        if event.key == pygame.K_SPACE and not shoot_golf_ball:
                            if not arrow_rect.collidepoint(pygame.mouse.get_pos()):
                                controlling_golf_ball = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE and not shoot_golf_ball:
                            if not arrow_rect.collidepoint(pygame.mouse.get_pos()):
                                if "rotated_arrow" in locals():
                                    dxv, dyv = mx, my
                                    gxv, gyv = golf_ball_col[0], golf_ball_col[1]

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

                golf_ball_rect = pygame.Rect(golf_ball_col[0]-10, golf_ball_col[1]-10,   10*2, 10*2 )

                if golf_ball_rect.colliderect(win_rect):
                    STOP = True
                
                vignette.set_alpha(122)

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

                #print(overlap_sand_mask.count())

                if back:
                    back_time += 1 * dt

                    if back_time > 3:
                        self.organs_bought.append('liver')
                        scripts.saving.save(organs_bought_=self.organs_bought, golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1])
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.mixer.quit()
                        self.change_scene('patient_room_2')

                eye_time += 0.6 * dt

                if eye_time >= 0.5:
                    if eye_frame <= 0:
                        eye_time = 0
                        
                        eye_frame += 1

                        eye = set_eye_roll(eye_frame)
                    else:
                        eye_frame = -1


                flag_time += 0.4 * dt

                if flag_time >= 0.5:
                    if flag_frame <= 0:
                        flag_time = 0
                        
                        flag_frame += 1

                        flag = set_flag(flag_frame)
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
                    
                red_channel.fill((255,255,255))
                
                red_channel.blit(background, (0, 0))

                #win.blit(sand_0, (620, 200))
                #win.blit(sand_0_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), (620, 200))
                
                #pygame.draw.circle(win, (0, 255, 0), golf_ball_col, 10, 0)
                
                if not dont_show_eye:
                    red_channel.blit(eye, (golf_ball_rect.x, golf_ball_rect.y))

                pygame.draw.rect(win, (0, 0, 255), win_rect, 2)

                #win.blit(golf_ball_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), (golf_ball_rect.x, golf_ball_rect.y))
                #win.blit(overlap_sand_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 0, 0, 255)), (golf_ball_rect.x, golf_ball_rect.y))
                
                #pygame.draw.rect(win, (0, 0, 255), arrow_rect, 2)

                #pygame.draw.rect(win, (250, 0, 0), golf_ball_rect, 2)
                #pygame.draw.rect(win, (210, 30, 30), wall_rect_1)


                if controlling_golf_ball:
                    if "rotated_arrow" in locals() and shots_left > 0:
                        #win.blit(rotated_arrow, arrow_rect)   # Masked arrow bg effect

                        red_channel.blit(rotated_arrow, arrow_rect)
                        
                # shown ball speed bar

                red_channel.blit(bar, (70, 440))

                pygame.draw.rect(win, (30, 30, 30), pygame.Rect(70 + shown_ball_speed * 78, 440, 10, 30)) # line
                pygame.draw.rect(win, (0, 0, 0), pygame.Rect(70, 440, 650, 30), 3, 2)
                
                if fade_alpha >= 1 and start_fade == False:
                    fade_alpha -= 100 * dt

                if start_fade == True:
                    if fade_alpha <= 255:
                        fade_alpha += 300 * dt
                    else:
                        if next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_4')  
                        if restart and not next_level:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('golf_lvl_4')
                        else:
                            scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                            pygame.mixer.quit()
                            self.change_scene('patient_room_2')

                if STOP:
                    fade_alpha = 255
                    track_mixer.stop()
                    sfx_mixer.stop()

                    back = True
                
                red_channel.blit(shots_left_text_render, (190, 20))
                red_channel.blit(vignette, (0, 0))

                red_channel = red(red_channel)

                win.blit(red_channel, (0, 0))
                win.blit(liver, liver_pos)

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'present_2': # ----------------------PRESENT 2----------------------------
            import pygame, json, os, sys, time
            import scripts.saving

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

            present_opened = pygame.image.load(f'assets\\present\\present\\open_1.png').convert_alpha()

            def set_background(frame):
                background = pygame.image.load(f'assets\\present\\background\\background_2_{str(frame)}.png').convert_alpha()
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                return background

            background = set_background(background_frame)

            present_frame = 0
            present_time = 0

            def set_present(frame):
                present = pygame.image.load(f'assets\\present\\present\\idle_{str(frame)}.png').convert_alpha()
                #present = pygame.transform.scale(present, (WIDTH, HEIGHT))
                return present

            present = set_present(present_frame)


            confetti_frame = 0
            confetti_time = 0

            def set_confetti(frame):
                confetti = pygame.image.load(f'assets\\present\\confeti\\confetti_{str(frame)}.png').convert_alpha()
                #present = pygame.transform.scale(present, (WIDTH, HEIGHT))
                return confetti

            confetti = set_confetti(confetti_frame)


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

            self.gvliver = True

            scripts.saving.save(liver_gave_=self.gvliver, started_game_=self.started,floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level)

            while True:
                dt = time.time() - prev_time
                prev_time = time.time()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scripts.saving.save(floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.quit()
                        quit()
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not fade_alpha >= 1:
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

                            present = set_present(present_frame)
                        else:
                            present_frame = -1

                background_time += 2 * dt

                if background_time >= 0.5:
                    if background_frame <= 0:
                        background_time = 0
                        
                        background_frame += 1

                        background = set_background(background_frame)
                    else:
                        background_frame = -1

                if play_confetti:
                    confetti_time += 1 * dt
                    
                    if confetti_time >= 0.05:
                        if confetti_frame <= 10:
                            confetti_time = 0
                            
                            confetti_frame += 1

                            confetti = set_confetti(confetti_frame)
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
                        scripts.saving.save(tv_start_time_=int(pygame.mixer.music.get_pos() // 1000),floor_kideny_=self.organ[0],stomach_gave_=self.organ[1],golf_level_=self.golf_level, liver_gave_=self.gvliver, started_game_=self.started)
                        pygame.mixer.quit()
                        self.change_scene('patient_room_2')

                # win.blit(esc_text_render, (220, 20))

                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()
        elif self.current_scene == 'end_room': # ----------------------END ROOM----------------------------
            import pygame, os, sys, time
            import pygame.mixer
            import scripts.saving

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
                uhoh = pygame.image.load(f'assets\\animations\\uhoh\\{str(uhoh_frame)}.png')
                uhoh.set_colorkey((255, 255, 255))
                #uhoh = pygame.transform.scale(uhoh, (328 x 247))
                return uhoh

            uhoh = set_uhoh()

            patient_frame = 1
            patient_time = 0

            def set_patient():
                patient = pygame.image.load(f'assets\\people\\patient 3\\patient_3_{str(patient_frame)}.png')
                #patient = pygame.transform.scale(patient, (WIDTH, HEIGHT))
                return patient

            patient = set_patient()


            button_frame = 1
            button_time = 0

            def set_button():
                button = pygame.image.load(f'assets\\animations\\final button\\final_button_{str(button_frame)}.png')
                #uhoh = pygame.transform.scale(uhoh, (328 x 247))

                return button

            button = set_button()

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

                        patient = set_patient()
                    else:
                        patient_frame = 0

                win.blit(patient, (200, 60))
                win.blit(foreground, (0, 0))

                if uhoh_true:
                    uhoh_time += 2 * dt

                    if uhoh_time > 0.2 and uhoh_frame < 82:
                        uhoh_time = 0
                        uhoh_frame += 1

                        uhoh = set_uhoh()

                    win.blit(uhoh, (WIDTH // 10, 5))
                
                if show_button:
                    button_time += 1 * dt

                    if button_time > 0.5:
                        button_time = 0

                        if button_frame == 1:
                            button_frame = 0
                        else:
                            button_frame += 1

                        button = set_button()
                        

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

                        # Reseting the game while its running is a pain

                        scripts.saving.save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')
                        
                        self.started = False
                        self.floor_kideny = False
                        self.money = 0
                        self.golf_level = 1
                        self.organs_bought = []
                        self.organ = (False, False)
                        self.gvliver = False

                        scripts.saving.started_game = False
                        scripts.saving.floor_kideny = False
                        scripts.saving.stomach_gave = False
                        scripts.saving.liver_gave = False
                        scripts.saving.organs_bought = []
                        scripts.saving.money = 0
                        scripts.saving.golf_level = 1

                        scripts.saving.save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')

                        pygame.mixer.quit()
                        self.change_scene('menu')


                title ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

                pygame.display.set_caption(title)
                
                win.blit(fade_screen, (0, 0))
                clock.tick(144)
                
                pygame.display.flip()


    def change_scene(self, scene_id): #menu and map
        self.current_scene = str(scene_id)
        self.update_scene(func)


"""
        self.current_scene = 'menu'
        
        self.organs_bought = organs_bought
        self.stomach_gave = stomach_gave
        self.floor_kideny = floor_kideny

        self.money = money
        self.func = func

        self.organ = organ
        self.golf_level = level

        self.gvliver = liver
        self.started = started
"""

    
scene_manager = Scene_Manager(func, scripts.saving.organs_bought, scripts.saving.stomach_gave, scripts.saving.floor_kideny, scripts.saving.money, (scripts.saving.floor_kideny, scripts.saving.stomach_gave), scripts.saving.golf_level, scripts.saving.liver_gave, scripts.saving.started_game)
scene_manager.change_scene('menu')



