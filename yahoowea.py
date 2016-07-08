#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from urllib.parse import urlencode
from urllib.request import urlopen
import json

code_emoji = {
    "0":"🌪",
    "1":"🌀",
    "2":"🌀",
    "3":"⚡️⚡🌩⛈️",
    "4":"⚡🌩️",
    "5":"☔️❄️🌧🌨",
    "6":"☔️🌧🌁",
    "7":"❄🌨️🌁",
    "8":"☔️",
    "9":"☔️",
    "10":"☔️",
    "11":"☔🌦️",
    "12":"☔🌦️",
    "13":"❄️",
    "14":"❄️",
    "15":"❄️🌨❄️",
    "16":"❄️🌨",
    "17":"☔️🤕",
    "18":"🌁😖",
    "19":"🌁",
    "20":"🌁",
    "21":"🌁",
    "22":"🌁",
    "23":"🌫",
    "24":"🌫",
    "25":"⛄",
    "26":"🌥",
    "27":"☁",
    "28":"⛅",
    "29":"☁",
    "30":"🌤",
    "31":"🌙",
    "32":"☀",
    "33":"🌟",
    "34":"🌤",
    "35":"🌧☔",
    "36":"🌡😌😰",
    "37":"☀☁🌩",
    "38":"🌩⛅🌩",
    "39":"🌩🌧🌩",
    "40":"🌧⛅🌧",
    "41":"🌨🌨❄❄❄",
    "42":"🌨⛅🌨",
    "43":"🌨🌨❄❄",
    "44":"☀⛅☀⛅",
    "45":"🌩⚡☔🌧🌧",
    "46":"🌨⛅🌨",
    "47":"☀⛅🌩⚡🌦",
    "3200":"❌"
}

def get_wea(place="上海"):
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\") and u='c'"%(place)
    yql_url = base_url + urlencode({'q':yql_query}) + "&format=json"
    result = urlopen(yql_url).read().decode("utf-8")

    data = json.loads(result)
    des = "<strong>"+data["query"]["results"]["channel"]["description"]+"</strong>\n\n"
    c = '℃'
    now = data["query"]["results"]["channel"]["item"]["condition"]["date"] + ":\n" + data["query"]["results"]["channel"]["item"]["condition"]["temp"] + c + ' ' +  code_emoji[data["query"]["results"]["channel"]["item"]["condition"]["code"]] + ' ' + data["query"]["results"]["channel"]["item"]["condition"]["text"] + "\n\n"
    fore = ''
    for x in data["query"]["results"]["channel"]["item"]["forecast"]:
        a = x["day"] + ", " + x["date"] + ":\n" + x["low"] + c + " - " + x["high"] + c + ' ' + code_emoji[x["code"]] + ' ' + x["text"] + "\n\n"
        fore += a
    answer = des + now + fore.rstrip("\n\n")

    return answer


if __name__ == "__main__":
#    from pprint import pprint
#    pprint(get_wea())
    print(get_wea())
