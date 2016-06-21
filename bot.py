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

    def on_chat_message(self,msg):
        self._count += 1
        now = str(datetime.datetime.now())
        #print(">>> %s"%(now))
        content_type,chat_type,chat_id = telepot.glance(msg)
        first_name = msg["from"]["first_name"]
        username = msg["from"]["username"]
        msg_id = msg["message_id"]

        ## To judge if the content is a text and deal with it.
        if content_type == "text":
            text = msg["text"]
            textlist = text.split(";% ")
            text_1 = textlist[0]
            text_2 = textlist[-1]

            if text == "/start" or text == "/start@" + info["username"]:
                answer = "Welcome!\nPlease type \"/help\" to get a help list."
            elif text == "/help" or text == "/help@" + info["username"]:
                answer = bhelp_list[0]
            elif text == "/hello" or text == "/hello@" + info["username"]:
                greeting = random.choice(greeting_list)
                answer = "Hello," + first_name + "!"+greeting
            elif text == "/joke" or text == "/joke@" + info["username"]:
                answer = random.choice(joke_list)
            elif text == "/time" or text =="/time@" + info["username"]:
                time = str(datetime.datetime.now())
                answer = "Now is " + time + "."
            elif text == "/fuck" or text == "/fuck@" + info["username"]:
                answer = "NO!I\"m not a GAY!"
                self._fuck += 1
            elif text == "fuck again" and self._fuck == 1:
                answer = "Fuck you!"
            elif text == "/count" or text == "/count@" + info["username"]:
                answer = self._count
            elif text_1 == "/cmd" or text_1 == "/cmd@" + info["username"]:
                if username == ADMIN:
                    answer = "Result:\n" + subprocess.check_output(text_2,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
                else:
                    answer = "Sorry,you are not allowed to run a command in order to keep the bot safe."
            elif text_1 == "/send" or text_1 == "/send@" + info["username"]:
                if username == ADMIN:
                    self.sender.sendChatAction("upload_document")

                    try:
                        with open(text_2) as document:
                            self.sender.sendDocument(document)
                    except:
                        with open(text_2,"rb") as document:
                            self.sender.sendDocument(document)
                    answer = "Sended."
                else:
                    answer = "Sorry,you are not allowed to get a file in order to keep the bot safe."
            elif text == "/code" or text =="/code@" + info["username"]:
                with open("bot.py") as bot_py:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(bot_py)
                with open("greeting.txt") as greeting_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(greeting_txt)
                with open("bhelp.txt") as bhelp_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(bhelp_txt)
                with open("joke.txt") as joke_txt:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(joke_txt)
                answer = "Sent code.\nYou should make dictionaries \"Image/\" \"Video/\" \"Audio/\" \"File/\" before you run it."
            else:
                answer = None


            ## Send result.
            if answer != None:
                self.sender.sendChatAction("typing")
                self.sender.sendMessage(answer,reply_to_message_id=msg_id)
                #bot.sendMessage(chat_id,"%s"%(answer),reply_to_message_id=msg_id)
                ## Give a journal.
                print(">>> %s"%(now))
                print("Bot:Got text \"%s\" from @%s and answered with \"%s\"."%(text,username,answer))
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
