#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Filename:bot.py

### Launching.
import os
import random
import datetime
import argparse
import subprocess

AUTHOR = "S-X-ShaX"
VERSION = "3.3"
now = str(datetime.datetime.now())
print("A telegram bot program written by %s,Ver %s."%(AUTHOR,VERSION))
print("Starting bot at %s..."%(now))

try:
    import telepot
    from telepot.delegate import per_from_id, create_open
except ImportError:
    print("ERROR:It seems that there is no telepot api installed.")
    print("Maybe you should install it first via \"# pip3 install telepot\"?")
    exit()


## Deal with the args.
parser = argparse.ArgumentParser(description="A telegram bot program.")
parser.add_argument("-t","--token",help="Get the file that stored the bot token.",action="store")
parser.add_argument("-a","--admin",help="Get the admin user\" name",action="store")
args = parser.parse_args()

token_file = args.token
if token_file == None:
    print("\nWARNING:It seems that you haven\'t choose a token file.")
    print("You are expected to make a tokenfile like YOURBOTNAME.token,which contains you bot token from the BotFather,and then run the program again by \"$ python3 ./bot.py --token YOURBOTNAME.token --admin ADMINUSER\".")
    TOKEN = input("However,you can also type your token here and then press [ENTER] to make it continue: ")
else:
    try:
        with open(token_file) as token_open:
            TOKEN = token_open.read().rstrip()
    except FileNotFoundError:
        print("ERROR:No avaliable \"%s\" was found."%(token_file))
        exit()

ADMIN = args.admin
if ADMIN == None:
    print("\nWARNING:It seems that you haven\'t choose an admin user.")
    print("You are expected to choose an adminuser to use some advanced functions.")
    print("The admin user is usually yourself,so you should find your username which maybe also called nickname in the Settings of Telegram,notice the \'@\' is not a part of your username.if you haven\'t set it,you should set a username,and run the program again by \"$ python3 ./bot.py --token YOURBOTNAME.token --admin ADMINUSER\".")
    ADMIN = input("However,you can also type your admin user name here and then press [ENTER] to make it continue: ")

### Check dictonaries.
if os.path.exists("Image") == False:
    os.mkdir("Image")
if os.path.exists("Video") == False:
    os.mkdir("Video")
if os.path.exists("Audio") == False:
    os.mkdir("Audio")
if os.path.exists("File") == False:
    os.mkdir("File")

### This is some assistant function.
def greet():
    try:
        with open("greeting.txt") as greeting_open:
            greeting_list = greeting_open.read().split("\n$")[1:-1]
    except FileNotFoundError:
        print("ERROR:No avaliable \"greeting.txt\" was found.")
        exit()
    return greeting_list
greeting_list = greet()


def bhelp():
    try:
        with open("bhelp.txt") as bhelp_open:
            bhelp_list = bhelp_open.read().split("\n$")[1:-1]
    except FileNotFoundError:
        print("ERROR:No avaliable \"bhelp.txt\" was found.")
        exit()
    return bhelp_list
bhelp_list = bhelp()


def joke():
    try:
        with open("joke.txt") as joke_open:
            joke_list = joke_open.read().split("\n$")[1:-1]
    except FileNotFoundError:
        print("ERROR:No avaliable \"joke.txt\" was found.")
        exit()
    return joke_list
joke_list = joke()


#class MessageCounter(telepot.helper.ChatHandler):
#    def __init__(self, seed_tuple, timeout):
#    super(MessageCounter, self).__init__(seed_tuple, timeout)
#    self._count = 0

#    def on_chat_message(self, msg):
#    self._count += 1
#    self.sender.sendMessage(self._count)

class TeleBot(telepot.helper.ChatHandler):
    def __init__(self,seed_tuple,timeout):
        super(TeleBot,self).__init__(seed_tuple,timeout)
        self._count = 0
        self._fuck = 0
        self._parse = None

    def on_chat_message(self,msg):
        self._count += 1
        now = str(datetime.datetime.now())
        print(">>> %s"%(now))
        content_type,chat_type,chat_id = telepot.glance(msg)
        self._first_name = msg["from"]["first_name"]
        self._username = msg["from"]["username"]
        self._msg_id = msg["message_id"]

        ## To judge if the content is a text and deal with it.
        if content_type == "text":
            self._text = msg["text"]
            self._textlist = self._text.split(";% ")
            self._text_1 = self._textlist[0]
            self._text_2 = self._textlist[-1]

            if self._text == "/start" or self._text == "/start@" + info["username"]:
                self._answer = "Welcome!\nPlease type \"/help\" to get a help list."
            elif self._text == "/help" or self._text == "/help@" + info["username"]:
                self._answer = bhelp_list[0]
                self._parse = "HTML"
            elif self._text == "/hello" or self._text == "/hello@" + info["username"]:
                self._answer = "Hello," + self._first_name + "!"+ random.choice(greeting_list)
            elif self._text == "/joke" or self._text == "/joke@" + info["username"]:
                self._answer = random.choice(joke_list)
            elif self._text == "/time" or self._text == "/time@" + info["username"]:
                self._answer = "Now is " + str(datetime.datetime.now()) + "."
            elif self._text == "/fuck" or self._text == "/fuck@" + info["username"]:
                self._answer = "NO!'m not a GAY!"
                self._fuck += 1
            elif (self._text == "/fuckagain" or self._text == "/fuckagain@" + info["username"]) and self._fuck == 1:
                self._answer = "Fuck you!"
            elif self._text == "/count" or self._text == "/count@" + info["username"]:
                self._answer = self._count
            elif self._text_1 == "/cmd" or self._text_1 == "/cmd@" + info["username"]:
                if self._username == ADMIN:
                    self._answer = "Result:\n" + subprocess.check_output(self._text_2,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
                else:
                    self._answer = "Sorry,you are not allowed to run a command in order to keep the bot safe."
            elif self._text_1 == "/send" or self._text_1 == "/send@" + info["username"]:
                if self._username == ADMIN:
                    self.sender.sendChatAction("upload_document")
                    try:
                        with open(self._text_2) as self._document:
                            self.sender.sendDocument(self._document)
                    except:
                        with open(self._text_2,"rb") as self._document:
                            self.sender.sendDocument(self._document)
                    self._answer = "Sended."
                else:
                    self._answer = "Sorry,you are not allowed to get a file in order to keep the bot safe."
            elif self._text == "/code" or self._text =="/code@" + info["username"]:
                with open("bot.py") as self._bot_py:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._bot_py)
                with open("greeting.txt") as self._greeting_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._greeting_txt)
                with open("bhelp.txt") as self._bhelp_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._bhelp_txt)
                with open("joke.txt") as self._joke_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._joke_txt)
                with open("talk.txt") as self._talk_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._talk_txt)
                with open("README.md") as self._README_md:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._README_md)
                self._answer = "Sent code.\nYou should make directories as \"Image/\" \"Video/\" \"Audio/\" \"File/\" before you run it.\nFor more information,click <a href=\"https://github.com/S-X-ShaX/telebot/\">My TeleBot on GitHub</a>."
                self._parse = "HTML"
            else:
                self._answer = None


            ## Send result.
            if self._answer != None:
                self.sender.sendChatAction("typing")
                if self._parse != None:
                    self.sender.sendMessage(self._answer,reply_to_message_id=self._msg_id,parse_mode=self._parse)
                else:
                    self.sender.sendMessage(self._answer,reply_to_message_id=self._msg_id)
                ## Give a journal.
                #print(">>> %s"%(now))
                print("Bot:Got text \"%s\" from @%s and answered with \"%s\"."%(self._text,self._username,self._answer))
            else:
                print("Bot:Got text \"%s\" from @%s."%(self._text,self._username))
            self._parse = None
            print("--------------------------------------------")


    def on_close(self, exception):
        now = str(datetime.datetime.now())
        print(">>> %s"%(now))
        print("Bot:Close an delegator with @%s by calling on_close() due to timeout."%(self._username))
        print("--------------------------------------------")


## To judge if the content is a photo.
#        elif content_type == "photo":
#            file_id = msg["photo"][-1]["file_id"]
#            if chat_type == "private":
#                if username == ADMIN:
#                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
#                    bot.downloadFile(file_id, "Image/IMG_%s.jpg"%(now))
#                    bot.sendMessage(chat_id,"Got photo IMG_%s.jpg in Image/."%(now),reply_to_message_id=msg_id)
#                    print("Bot:Got photo Image/IMG_%s.jpg from @%s."%(now,username))
#                else:
#                    answer = "Sorry,only the admin user can save a photo on the bot."
#                    bot.sendMessage(chat_id,"%s"%(answer),reply_to_message_id=msg_id)
#                    print("Bot:Refused save a photo from @%s."%(username))

#        elif content_type == "document":
#            file_id = msg["document"]["file_id"]
#            file_name = msg["document"]["file_name"]
#            if chat_type == "private":
#                if username == ADMIN:
#                    bot.downloadFile(file_id, "File/%s"%(file_name))
#                    bot.sendMessage(chat_id,"Got file %s in File/."%(file_name),reply_to_message_id=msg_id)
#                    print("Bot:Got file File/%s from @%s."%(file_name,username))
#                else:
#                    answer = "Sorry,only the admin user can save a file on the bot."
#                    bot.sendMessage(chat_id,"%s"%(answer),reply_to_message_id=msg_id)
#                    print("Bot:Refused save a file from @%s."%(username))

#                print("--------------------------------------------")


### Now it start run.
print("Getting bot information...")

bot = telepot.DelegatorBot(
    TOKEN,
    [
        (
            per_from_id(),
            create_open(TeleBot,timeout=30)
        )
    ,]
)


### Now it prints your bot information.
try:
    info = bot.getMe()
except KeyboardInterrupt:
    exit()
except:
    print("ERROR:Your token is invaild.")
    print("Please check what your token file \"%s\" contains."%(token_file))
    print("It should only contain your token in one line,without anything else.")
    print("Or you may need to check your network and system time,you can\'t connect to the bot server if your time is wrong or your network is down,and your bot token canalso be considered invaild.")
    exit()

print("############################################")
print("#")
print("# tokenfile:%s"%(token_file))
print("# botid:%s"%(info["id"]))
print("# username:%s"%(info["username"]))
print("# firstname:%s"%(info["first_name"]))
print("# adminuser:%s"%(ADMIN))
print("#")
print("############################################")

print("Bot:I am listening...")
print("--------------------------------------------")

try:
    bot.message_loop(run_forever=True)
except KeyboardInterrupt:
    exit()
