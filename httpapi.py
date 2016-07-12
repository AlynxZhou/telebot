#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: httpapi.py


from urllib.parse import urlencode
from urllib.request import urlopen, Request
import json


### For yahoo weather api.
def get_wea(place="上海"):
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\") and u='c'"%(place)
    yql_url = base_url + urlencode({'q': yql_query}) + "&format=json"
    data = json.loads(urlopen(yql_url).read().decode("utf-8"))

    code_emoji = {
        "0": "🌪",
        "1": "🌀",
        "2": "🌀",
        "3": "⚡️⚡🌩⛈️",
        "4": "⚡🌩️",
        "5": "☔️❄️🌧🌨",
        "6": "☔️🌧🌁",
        "7": "❄🌨️🌁",
        "8": "☔️",
        "9": "☔️",
        "10": "☔️",
        "11": "☔🌦️",
        "12": "☔🌦️",
        "13": "❄️",
        "14": "❄️",
        "15": "❄️🌨❄️",
        "16": "❄️🌨",
        "17": "☔️🤕",
        "18": "🌁😖",
        "19": "🌁",
        "20": "🌁",
        "21": "🌁",
        "22": "🌁",
        "23": "🌫",
        "24": "🌫",
        "25": "⛄",
        "26": "🌥",
        "27": "☁",
        "28": "⛅",
        "29": "☁",
        "30": "🌤",
        "31": "🌙",
        "32": "☀",
        "33": "🌟",
        "34": "🌤",
        "35": "🌧☔",
        "36": "🌡😌😰",
        "37": "☀☁🌩",
        "38": "🌩⛅🌩",
        "39": "🌩🌧🌩",
        "40": "🌧⛅🌧",
        "41": "🌨🌨❄❄❄",
        "42": "🌨⛅🌨",
        "43": "🌨🌨❄❄",
        "44": "☀⛅☀⛅",
        "45": "🌩⚡☔🌧🌧",
        "46": "🌨⛅🌨",
        "47": "☀⛅🌩⚡🌦",
        "3200": "❌"
    }

    des = "<strong>" + data["query"]["results"]["channel"]["description"] + ":</strong>\n\n"
    c = '℃'
    now = data["query"]["results"]["channel"]["item"]["condition"]["date"] + ":\n" + data["query"]["results"]["channel"]["item"]["condition"]["temp"] + c + ' ' +  code_emoji[data["query"]["results"]["channel"]["item"]["condition"]["code"]] + ' ' + data["query"]["results"]["channel"]["item"]["condition"]["text"] + "\n\n"
    fore = ''
    for x in data["query"]["results"]["channel"]["item"]["forecast"]:
        a = x["day"] + ", " + x["date"] + ":\n" + x["low"] + c + " - " + x["high"] + c + ' ' + code_emoji[x["code"]] + ' ' + x["text"] + "\n\n"
        fore += a
    answer = des + now + fore.rstrip("\n\n")

    return answer


### For Tuling chat api.
def get_talk(APIKey, info="你好"):
    base_url = "http://www.tuling123.com/openapi/api"
    json_data = json.dumps({"key": APIKey, "info": info})
    #post_data = "POST http://www.tuling123.com/ HTTP/1.1\nContent-Type: application/json;charset=utf-8\n\n" + json_data

    req = Request(base_url, json_data.encode("utf-8"), headers={"Content-Type": "application/json"})
    with urlopen(req) as r:
        result = json.loads(r.read().decode("utf-8"))

    return result["text"]


### For qingyunke chat api.
"""
def get_talk(msg="你好"):
    base_url = "http://api.qingyunke.com/api.php?"
    all_url = base_url + urlencode({"key": "free", "appid": "0", "msg": msg})
    data = json.loads(urlopen(all_url).read().decode("utf-8"))

    if data["result"] == 0:
        result = data["content"]
    elif data["result"] == 1:
        result = "Sorry, but something seems wrong."

    return result
"""

if __name__ == "__main__":
#    from pprint import pprint
#    pprint(get_wea())
    print(get_wea())
    print(get_talk(APIKey))
