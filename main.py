from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
my_birthday = '01-06'

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
xh_id = 'os09R5x2CF4XeMm_UuL4lJO-Sag8'
dh_id = 'os09R51dM3W6TDID04zT6Z_1Lc30'
template_id = os.environ["TEMPLATE_ID"]

together_day = os.environ["TOGETHER_DATE"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], str(weather['wind']), math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_tomorrow_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][1]
  return weather['weather'], str(weather['wind']), math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days +1

def get_together_day():
  delta = today - datetime.strptime(together_day, "%Y-%m-%d")
  return delta.days +1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_my_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + my_birthday, "%Y-%m-%d")
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
wea, wind, temperature, min_temperature, max_temperature = get_weather()
t_wea, t_wind, t_min_temperature, t_max_temperature = get_tomorrow_weather()
data = {
  "city":{"value":city, "color":get_random_color()},
  "weather":{"value":wea, "color":get_random_color()},
  "wind":{"value":wind, "color":get_random_color()},
  "temperature":{"value":temperature, "color":get_random_color()},
  "min_temperature":{"value":min_temperature, "color":get_random_color()},
  "max_temperature":{"value":max_temperature, "color":get_random_color()},
  "t_weather":{"value":t_wea, "color":get_random_color()},
  "t_wind":{"value":t_wind, "color":get_random_color()},
  "t_min_temperature":{"value":t_min_temperature, "color":get_random_color()},
  "t_max_temperature":{"value":t_max_temperature, "color":get_random_color()},
  "love_days":{"value":get_count(), "color":get_random_color()},
  "birthday_left":{"value":get_birthday(), "color":get_random_color()},
  "birthday_me":{"value":get_my_birthday(), "color":get_random_color()},
  "words":{"value":get_words(), "color":get_random_color()},
  "together_day":{"value":get_together_day(), "color":get_random_color()}
}
# data = {
#   "weather":{"value":wea, "color":},
#   "temperature":{"value":temperature, "color":get_random_color()},
#   "min_temperature":{"value":min_temperature, "color":get_random_color()},
#   "max_temperature":{"value":max_temperature, "color":get_random_color()},
#   "love_days":{"value":get_count(), "color":get_random_color()},
#   "birthday_left":{"value":get_birthday(), "color":get_random_color()},
#   "words":{"value":words1, "color":get_random_color()}
# }
res = wm.send_template(user_id, template_id, data)
res = wm.send_template(xh_id, template_id, data)
res = wm.send_template(dh_id, template_id, data)
print(res)
