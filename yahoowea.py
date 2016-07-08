#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from urllib.parse import urlencode
from urllib.request import urlopen
import json


def get_wea(place="上海"):
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\") and u='c'"%(place)
    yql_url = base_url + urlencode({'q':yql_query}) + "&format=json"
    result = urlopen(yql_url).read().decode("utf-8")

    data = json.loads(result)
    des = "<strong>"+data["query"]["results"]["channel"]["description"]+"</strong>\n"
    c = '℃'
    now = data["query"]["results"]["channel"]["item"]["condition"]["date"] + ": " + data["query"]["results"]["channel"]["item"]["condition"]["temp"] + c + ' ' + data["query"]["results"]["channel"]["item"]["condition"]["text"] + "\n"
    fore = ''
    for x in data["query"]["results"]["channel"]["item"]["forecast"]:
        a = x["day"] + ", " + x["date"] + ": " + x["low"] + c + " - " + x["high"] + c + ' ' + x["text"] + '\n'
        fore += a
    answer = des + now + fore.rstrip('\n')

    return answer


if __name__ == "__main__":
#    from pprint import pprint
#    pprint(get_wea())
    print(get_wea())
