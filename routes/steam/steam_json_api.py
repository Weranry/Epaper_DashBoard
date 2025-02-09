from.web.steam.get_steam import get_steam_data


def create_steam_json(api_key, steam_id):
    data = get_steam_data(api_key, steam_id)
    return data