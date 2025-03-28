import requests

def get_sunnyclock_data(lon, lat):
    """
    从7Timer API获取天气数据
    返回处理后的天气数据字典
    """
    url = f"https://www.7timer.info/bin/api.pl?lon={lon}&lat={lat}&product=astro&output=json"
    response = requests.get(url)
    data = response.json()
    
    # 提取24小时内的数据点
    forecast_data = [entry for entry in data["dataseries"] if entry["timepoint"] <= 24]
    
    # 只取前8个数据点以与visualization适配
    forecast_data = forecast_data[:8]
    
    # 为每个数据点创建数组
    timepoints = []
    cloudcover = []
    seeing = []
    transparency = []
    lifted_index = []
    rh2m = []
    wind_direction = []
    wind_speed = []
    temp2m = []
    prec_type = []
    
    # 填充数据
    for entry in forecast_data:
        timepoints.append(entry["timepoint"])
        cloudcover.append(entry["cloudcover"])
        seeing.append(entry["seeing"])
        transparency.append(entry["transparency"])
        lifted_index.append(entry["lifted_index"])
        rh2m.append(entry["rh2m"])
        wind_direction.append(entry["wind10m"]["direction"])
        wind_speed.append(entry["wind10m"]["speed"])
        temp2m.append(entry["temp2m"])
        prec_type.append(entry["prec_type"])
    
    return {
        "timepoints": timepoints,
        "cloudcover": cloudcover,
        "seeing": seeing,
        "transparency": transparency,
        "lifted_index": lifted_index,
        "rh2m": rh2m,
        "wind_direction": wind_direction,
        "wind_speed": wind_speed,
        "temp2m": temp2m,
        "prec_type": prec_type
    }