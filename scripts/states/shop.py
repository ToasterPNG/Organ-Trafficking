import pygame, json, os, sys, time

from scripts.saving import *
from scripts.shake import *


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

organs_bought = organs_bought


sfx_mixer = pygame.mixer.Channel(4)

contract_slide_1 = pygame.mixer.Sound('sounds/contract_slide_1.mp3')
contract_slide_2 = pygame.mixer.Sound('sounds/contract_slide_2.mp3')
contract_sign = pygame.mixer.Sound('sounds/contract_sign.mp3')

failed_purchase = pygame.mixer.Sound('sounds/failed_purchase.mp3')
wallet_open = pygame.mixer.Sound('sounds/wallet_open.mp3')

sfx_mixer.set_volume(0.5)

stomach_sold_out = False
title = ''

Currenct_Font = pygame.font.Font('fonts/Cash Currency.ttf', 32)
HighVoltage_Rough_Font = pygame.font.Font('fonts/HighVoltage Rough.ttf', 32)

money = money
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

for item in organs_bought:
    set_sould_out_command = item + '_sold_out = True'
    exec(set_sould_out_command)

def buy_window(title):
    global show_contract, organs_bought

    if not show_contract:
        sfx_mixer.play(contract_slide_1)
    
    show_contract = True
    organs_bought.append(title)

def check_contract_anmation(title):
    global contract_y_anim, vel_anim_y, signiture_counter_movement_y, frame_signature, signature_animation, signature_delay
    global stomach_sold_out, signature_delay, contract_leave_delay, money, show_contract

    set_sold_out = 'global ' + title + '_sold_out; ' + title + '_sold_out = True'

    if show_contract: # CONTRACT ANIMATION #
        exec(set_sold_out)

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
    
        win.blit(contract, (WIDTH // 2.7, contract_y_anim))
        win.blit(contract_stomach, (WIDTH // 2.7, contract_y_anim))


        if frame_signature > 1:
            win.blit(signature_animation, (WIDTH // 2.05, contract_y_anim * 2.27 + signiture_counter_movement_y))

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
        
def draw_sold_out():
    if stomach_sold_out:
        win.blit(sold_out, (520, 250))

def wallet_anim(action):
    global wallet_y, wallet_alpha, wallet, money_currenct_render

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

def reload_money_counter():
    global money_currenct_render

    money_currenct_render = Currenct_Font.render(str(money), True, (109, 34, 29))
    money_currenct_render = pygame.transform.rotozoom(money_currenct_render, 5, 1)

    money_currenct_render.set_alpha(wallet_alpha + 30)

wallet.set_alpha(wallet_alpha)
money_currenct_render.set_alpha(wallet_alpha + 30)

save(money_=money, organs_bought_=organs_bought)

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
            save(money_=money, organs_bought_=organs_bought)
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not fade_alpha >= 1:
                    start_fade = True
        if stomach_rect.collidepoint(pygame.mouse.get_pos()) and not show_contract:
            if not stomach_sold_out:
                hovered_stomach = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if money >= 560:
                        signature_delay, contract_leave_delay = 0, 0
                        title = "stomach"
                        buy_window(title)
                        money -= 560
                        save(money_=money, organs_bought_=organs_bought)
                        reload_money_counter()
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
    check_contract_anmation(title)
    wallet_anim(wallet_args)
    draw_sold_out()

    win.blit(wallet, (0, wallet_y))
    win.blit(money_currenct_render, (225, wallet_y + 20))

    win.blit(esc_text_render, (340, 20))

    if fade_alpha >= 1 and start_fade == False:
        fade_alpha -= 300 * dt

    if start_fade == True:
        if fade_alpha <= 255:
            fade_alpha += 300 * dt
        else:

            pygame.quit()
            os.system('python main.py')
            #import scripts.states.map

    title_ ='Organ Trafficking   FPS: ' + str(int(clock.get_fps()))

    pygame.display.set_caption(title_)
    
    win.blit(fade_screen, (0, 0))
            
    pygame.display.update()
    pygame.display.flip()
