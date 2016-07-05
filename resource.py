#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename:prepare.py

import os

def check_dir(directory):
    if os.path.exists(directory) == False:
        os.mkdir(directory)


def file_to_list(filename):
    try:
        with open(filename) as file_open:
            file_list = file_open.read().split("\n$")[1:-1]
    except FileNotFoundError:
        print("ERROR:No avaliable \"%s\" was found."%(filename))
        exit()
    return file_list


fuck_list = [
    "NO!I'm not a bad girl and I haven't!😡",
    "I know as a good girl I must behave myself but I had to say.Fuck you!💢",
    "It's so painful and unbearable!😖",
    "Oh!NO!Don't move!😲",
    "Ya Mie Die!Softly,please!😫",
    "Ah,seems end,so comfortable.😌",
    "Good boy,now I become your girl.😁"
]
