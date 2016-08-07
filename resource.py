#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: prepare.py
## Created by 请叫我喵 | S-X-ShaX
# sxshax@gmail.com, http://sxshax.xyz/

import os
import json

def check_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def check_file(filename):
    if not os.path.exists(filename):
        print("\033[46m\033[31mERROR\033[0m: No avaliable \"\033[32m%s\033[0m\" was found. Please reinstall telebot."%(filename))
        exit()


def file_to_list(filename):
    try:
        with open(filename) as file_open:
            file_list = file_open.read().split("\n$")[1:-1]
    except FileNotFoundError:
        print("\033[46m\033[31mERROR\033[0m: No avaliable \"\033[32m%s\033[0m\" was found. Please reinstall telebot."%(filename))
        exit()
    return file_list

def json_to_dict(jsonname):
    try:
        with open(jsonname) as json_open:
            json_dict = json.loads(json_open.read(), encoding="utf-8")
    except:
        json_dict = {}
    return json_dict

def dict_to_json(jsonname, json_dict):
    with open(jsonname, 'w') as json_open:
        json_open.write(json.dumps(json_dict, ensure_ascii=False))

fuck_list = [
    "NO! I'm not a bad girl and I haven't! 😡",
    "I know as a good girl I must behave myself but I had to say. Fuck you! 💢",
    "It's so painful and unbearable! 😖",
    "Oh! NO! Don't move! 😲",
    "Ya Mie Die! Softly, please! 😫",
    "Ah, seems end, so comfortable. 😌",
    "Good boy, now I become your girl. 😁"
]


code_list = [
    "bot.py",
    "resource.py",
    "ipcn.py",
    "httpapi.py",
    "assets/greeting.txt",
    "assets/bhelp.txt",
    "assets/joke.txt",
    "assets/redo.json",
    "assets/rule.json",
    "example_bot.json",
    "README.md"
]

sticker_dict = {
    '😏': "BQADBQAD8wADLKMJAwIAASAwWY6tcQI",
    '😆': "BQADBQAD9wADLKMJA8ZcQcFMToG0Ag",
    '😈': "BQADBQAEAQACLKMJA3-06f6jb96LAg",
    '😨': "BQADBQADKwADpgZdBmTxGppaYRBuAg",
    '😅': "BQADBQADMwADpgZdBpqFuimq1w5hAg",
    '😱': "BQADBQADNQADpgZdBmKVEXNJr2kaAg",
    '😒': "BQADBQADNwADpgZdBhcQ3HscfB5lAg",
    '😎': "BQADBQADOQADpgZdBl8cN3R575QyAg",
    '😡': "BQADBQADOwADpgZdBoLZI9Y7COR9Ag",
    '😂': "BQADBQADPQADpgZdBk7bfJ2yYUyYAg",
    '😐': "BQADBQADPwADpgZdBo9txTncldVUAg",
    '😓': "BQADBQADQQADpgZdBpwl1GACX9VfAg",
    '😌': "BQADAQAD2QADvDyABZvpsisEqR7kAg",
    '☺️': "BQADAQAD2wADvDyABW9CLusYOiCoAg",
    '😝': "BQADAQAD-QADvDyABW4uCIg0LKHRAg",
    '😏': "BQADAQAD-wADvDyABXXfezhl0kIjAg",
    '😚': "BQADAQADEgEAArw8gAWXT_Qf4ljrcAI",
    '😮': "BQADAQADGgEAArw8gAVWAryCbQ5_VgI",
    '😀': "BQADAQADGAEAArw8gAUni8NOF1AX2wI",
    '😦': "BQADAQADzQADvDyABYJGrUt7qIfmAg"
}

red_sticker_dict = {
    '😈': "BQADAQAD8QADvDyABUxkJzm7ogVbAg",
    '😡': "BQADAQAD9QADvDyABWyO3YV_OpA6Ag",
    '😤': "BQADAQAD0wADvDyABWaQlvbgXycbAg",
    '😡': "BQADBQADFwQAAkKpAAEF7ptGl5jK0ykC",
    '😈': "BQADBQAEAQACLKMJA3-06f6jb96LAg",
    '😨': "BQADBQADKwADpgZdBmTxGppaYRBuAg",
    '😎': "BQADBQADOQADpgZdBl8cN3R575QyAg",
    '😱': "BQADBQADNQADpgZdBmKVEXNJr2kaAg",
    '😈': "BQADBQADGQQAAkKpAAEFIaGohi4vhFoC"
}
