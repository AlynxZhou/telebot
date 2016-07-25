#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: prepare.py

import os
import json

def check_dir(directory):
    if os.path.exists(directory) == False:
        os.mkdir(directory)

def check_file(filename):
    if os.path.exists(filename) == False:
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
