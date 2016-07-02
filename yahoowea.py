#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from urllib.parse import urlencode
from urllib.request import urlopen
import json
#from pprint import pprint

def get_wea(place="上海"):
    base_url = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\") and u='c'"%(place)
    yql_url = base_url + urlencode({'q':yql_query}) + "&format=json"
    result = urlopen(yql_url).read().decode("utf-8")

    data = json.loads(result)
#    pprint(data)
    return data["query"]["results"]["channel"]["item"]["forecast"]
#pprint(data["query"]["results"]["channel"]["item"]["forecast"])
