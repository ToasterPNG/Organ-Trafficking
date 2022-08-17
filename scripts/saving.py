import os, json

save_file, money, organs_bought, stomach_gave, floor_kideny, tv_stat_time, started_game, golf_level, liver_gave, key = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def sv_read():
    global save_file, money, organs_bought, stomach_gave, floor_kideny, tv_stat_time
    global started_game, golf_level, liver_gave, key
    
    try:
        save_file = open('save.json')
        save_file = json.load(save_file)

        for i in save_file['Game_Data']:
            money = i['money']
            organs_bought = i['organs_bought']
            stomach_gave = i['stomach_gave']
            floor_kideny = i['floor_kideny']
            tv_stat_time = i['tv_start_time']
            started_game = i['started_game']
            golf_level = i['golf_level']
            liver_gave = i['liver_gave']
            key = i['key']

    except:
        os.chdir('scripts')
        os.system('corupt.vbs')
        pygame.quit()
        sys.exit()

sv_read()

def save(money_=money, organs_bought_=organs_bought, stomach_gave_=stomach_gave, floor_kideny_=floor_kideny, tv_start_time_=tv_stat_time, started_game_=started_game, golf_level_=golf_level, liver_gave_=liver_gave, key_=key):
    global money, organs_bought
    # {"Game_Data": [{"money": 873,"organs_bought": []}]}
    save_string = """{
    "Game_Data": [
        {
        "money": """ + str(money_) + """,
        "organs_bought": """ + str(organs_bought_).replace("'", '"') + """,

        "stomach_gave": """ + str(stomach_gave_).lower().replace("'", '"') + """,
        "floor_kideny": """ + str(floor_kideny_).lower().replace("'", '"') + """,
        "liver_gave": """ + str(liver_gave_).lower().replace("'", '"') + """,
        "started_game": """ + str(started_game_).lower().replace("'", '"') + """,

        "tv_start_time": """ + str(tv_start_time_).lower().replace("'", '"') + """,
        "golf_level": """ + str(golf_level_).lower().replace("'", '"') + """,

        "key": """ + str(key_).lower().replace("'", '"') + """
        }
    ]
}"""
    # print(save_string)
    with open("save.json", "w") as save_file:
        save_file.write(save_string)
    print('Saved Game')

#def reset():
#    save(money_=0, organs_bought_=[], stomach_gave_='false', floor_kideny_='false', tv_start_time_=0, started_game_='false', golf_level_=1, liver_gave_='false', key_='false')
