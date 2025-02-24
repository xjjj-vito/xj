from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY'].split(";")
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split(";")
template_id = os.environ["TEMPLATE_ID"]


def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['date'], \
           weather["humidity"], \
           weather["wind"], \
           weather["airQuality"], \
           weather['weather'], \
           weather["province"], \
           weather["city"], \
           math.floor(weather['temp']), \
           math.floor(weather['high']), \
           math.floor(weather['low'])

'''
日期
湿度
风向
空气质量
天气
省份
城市
当前温度
最高气温
最低气温
'''


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

da, humidity, wind, airQuality, wea, pro, ci, temperature, highest, lowest = get_weather(city[0])
da, s_humidity, s_wind, s_airQuality, s_wea, s_pro, s_ci, s_temperature, s_highest, s_lowest = get_weather(city[1])
# 日期，湿度，  风向，  空气质量，   天气，省份， 城市， 温度，       最高温，   最低温
data = {
    # 学校
    "s_humidity": {"value": s_humidity, "color": get_random_color()},
    "s_wind": {"value": s_wind, "color": get_random_color()},
    "s_airQuality": {"value": s_airQuality, "color": get_random_color()},
    "s_province": {"value": s_pro, "color": get_random_color()},
    "s_city": {"value": s_ci, "color": get_random_color()},
    "s_weather": {"value": s_wea, "color": get_random_color()},
    "s_temperature": {"value": s_temperature, "color": get_random_color()},
    "s_highest": {"value": s_highest, "color": get_random_color()},
    "s_lowest": {"value": s_lowest, "color": get_random_color()},
    # 家乡
    "humidity": {"value": humidity, "color": get_random_color()},
    "wind": {"value": wind, "color": get_random_color()},
    "airQuality": {"value": airQuality, "color": get_random_color()},
    "province": {"value": pro, "color": get_random_color()},
    "city": {"value": ci, "color": get_random_color()},
    # 原来的代码
    "weather": {"value": wea, "color": get_random_color()},
    "temperature": {"value": temperature, "color": get_random_color()},
    "highest": {"value": highest, "color": get_random_color()},
    "lowest": {"value": lowest, "color": get_random_color()},

    "date": {"value": da, "color": get_random_color()},

    "love_days": {"value": get_count(), "color": get_random_color()},
    "birthday_left": {"value": get_birthday(), "color": get_random_color()},
    "words": {"value": get_words(), "color": get_random_color()},

}
count = 0
for user_id in user_ids:
    res = wm.send_template(user_id, template_id, data)
    count += 1
print("发送了" + str(count) + "条消息")
