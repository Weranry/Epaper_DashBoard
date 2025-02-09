import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_steam_data(api_key, steam_id):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    start_time = time.time()
    urla = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={steam_id}&format=json"
    urlb = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
    # 设置verify=False来禁用证书验证
    responsea = requests.get(urla, verify=False)
    dataa = responsea.json()
    responseb = requests.get(urlb, verify=False)
    datab = responseb.json()

    total_playtime = 0
    for game in datab["response"]["games"]:
        total_playtime += game["playtime_forever"]

    total_playtime_hours = round(total_playtime / 60.0, 2)

    game_count = datab["response"]["game_count"]

    # 处理最近游玩游戏信息
    recent_game_count = len(dataa["response"]["games"])
    recent_game_names = []
    for game in dataa["response"]["games"]:
        playtime_2weeks = game.get('playtime_2weeks', 0)
        playtime_2weeks_hours = round(playtime_2weeks / 60, 2)
        recent_game_names.append(f"{game['name']}({playtime_2weeks_hours} h)")

    end_time = time.time()
    run_time = round(end_time - start_time, 2)

    data = {
        "total_playtime_hours": total_playtime_hours,
        "game_count": game_count,
        "recent_game_count": recent_game_count,
        "recent_game_names": recent_game_names,
        "run_time": run_time
    }
    return data