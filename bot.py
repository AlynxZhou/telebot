#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename:bot.py

### Launching.
import os
import random
import datetime
import argparse
import subprocess

from urllib.request import urlopen
#from html.parser import HTMLParser
from ipcn import IPCNParser
from yahoowea import get_wea

AUTHOR = "S-X-ShaX"
VERSION = "3.3"
now = str(datetime.datetime.now())
print("A telegram bot program written by %s,Ver %s."%(AUTHOR,VERSION))
print("Starting bot at %s..."%(now))

try:
    import telepot
    from telepot.delegate import per_from_id, create_open
#    from telepot.exception import TelepotException
except ImportError:
    print("ERROR:It seems that there is no telepot api installed.")
    print("Maybe you should install it first via \"# pip3 install telepot\"?")
    exit()


## Deal with the args.
aparser = argparse.ArgumentParser(description="A telegram bot program.")
aparser.add_argument("-t","--token",help="Get the file that stored the bot token.",action="store")
aparser.add_argument("-a","--admin",help="Get the admin user\" name",action="store")
args = aparser.parse_args()

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

### Check directories.
if os.path.exists("Image") == False:
    os.mkdir("Image")
if os.path.exists("Video") == False:
    os.mkdir("Video")
if os.path.exists("Audio") == False:
    os.mkdir("Audio")
if os.path.exists("File") == False:
    os.mkdir("File")

### These are some assistant function.
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

fuck_list = [
    "NO!I'm not a bad girl and I haven't!😡",
    "I know as a good girl I must behave myself but I had to say.Fuck you!💢",
    "It's so painful and unbearable!😖",
    "Oh!NO!Don't move!😲",
    "Ya Mie Die!Softly,please!😫",
    "Ah,seems end,so comfortable.😌",
    "Good boy,now I become your girl.😁"
]

## Define an expection.
#class UserClose(TelepotException):
#    pass


## Define a bot class.
class TeleBot(telepot.helper.UserHandler):
    def __init__(self,seed_tuple,timeout):
        super(TeleBot,self).__init__(seed_tuple,timeout)
#        self._answerer = telepot.helper.Answerer(self.bot)
        self._count = {
            "chat":0,
            "fuck":0
        }


    def on_chat_message(self,msg):
        self._now = str(datetime.datetime.now())

        self._count["chat"] += 1
        self._parse = None

        content_type,chat_type,chat_id = telepot.glance(msg)
#        self.sender = telepot.helper.Sender(self.bot,msg["chat"]["id"])
        self._first_name = msg["from"]["first_name"]
        self._username = msg["from"]["username"]
        self._msg_id = msg["message_id"]

        ## To judge if the content is a text and deal with it.
        if content_type == "text":
            self._text_orig = msg["text"]

            try:
                self._text_list = self._text_orig.split(' ',1)
                self._text = self._text_list[0]
                self._text_2 = self._text_list[1]
            except IndexError:
                self._text_2 = None
            if ('@' + info["username"]) in self._text:
                self._text = self._text.split('@' + info["username"],1)[0]


            # Handle.
            if self._text == "/start":
                self._answer = "Welcome!\nPlease type \"/help\" to get a help list."

            elif self._text == "/help":
                self._answer = bhelp_list[0]
                self._parse = "HTML"

            elif self._text == "/hello":
                self._answer = "Hello," + self._first_name + "!"+ random.choice(greeting_list)

            elif self._text == "/joke":
                self._answer = random.choice(joke_list)

            elif self._text == "/time":
                self._answer = "Now is " + str(datetime.datetime.now()) + "."
            elif self._text == "/weather":
                if self._text_2 != None:
                    self._answer = get_wea(self._text_2)
                else:
                    self._answer = "Please add a valid city,for instance,\"/weather 上海\"."

            elif self._text == "/fuck":
                try:
                    self._answer = fuck_list[self._count["fuck"]]
                    self._count["fuck"] += 1
                except IndexError:
                    self._count["fuck"] = 0
                    self._answer = fuck_list[self._count["fuck"]]
                    self._count["fuck"] += 1

            elif self._text == "/count":
                self._answer = self._count["chat"]

            elif self._text == "/ipcn":
                iparser = IPCNParser()
                self._ipcn = urlopen("http://ip.cn/").read().decode("utf-8")
                iparser.feed(self._ipcn)
                self._answer = iparser.result

            elif self._text == "/cmd":
                if self._text_2 != None:
                    if self._username == ADMIN:
                        try:
                            self._answer = "Result:\n" + subprocess.check_output(self._text_2,shell=True,stderr=subprocess.STDOUT,universal_newlines=True)
                        except subprocess.CalledProcessError:
                            self._answer = "Sorry,invalid command."
                    else:
                        self._answer = "Sorry,you are not allowed to run a command in order to keep the bot safe."
                else:
                    self._answer = None

            elif self._text == "/send":
                if self._text_2 != None:
                    if self._username == ADMIN:
                        bot.sendChatAction(chat_id,"upload_document")
                        try:
                            with open(self._text_2) as self._document:
                                bot.sendDocument(chat_id,self._document)
                        except:
                            with open(self._text_2,"rb") as self._document:
                                bot.sendDocument(chat_id,self._document)
                        self._answer = "Sent."
                    else:
                        self._answer = "Sorry,you are not allowed to get a file in order to keep the bot safe."
                else:
                    self._answer = None

            elif self._text == "/code":
                dir = [
                    "bot.py",
                    "ipcn.py",
                    "yahoowea.py",
                    "greeting.txt",
                    "bhelp.txt",
                    "joke.txt",
                    "README.md"
                ]
                for self._code_file in dir:
                    with open(self._code_file) as self._code_byte:
                        bot.sendChatAction(chat_id,"upload_document")
                        bot.sendDocument(chat_id,self._code_byte)
                """
                with open("ipcn.py") as self._ipcn_py:
                    self.sender.sendChatAction("upload_document")
                    self.sender.sendDocument(self._ipcn_py)
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
            """
                self._answer = "Sent code.\nYou should make directories as \"Image/\" \"Video/\" \"Audio/\" \"File/\" before you run it.\nFor more information,click <a href=\"https://github.com/S-X-ShaX/telebot/\">My TeleBot on GitHub</a>."
                self._parse = "HTML"

#            elif self._text == "/close":
#                self.on_close(UserClose)
#                self._answer = None

            else:
                self._answer = None


### Return.
#            print(">>> %s"%(now))
            if self._answer != None:
                ## Send result.
                bot.sendChatAction(chat_id,"typing")
                bot.sendMessage(chat_id,self._answer,reply_to_message_id=self._msg_id,parse_mode=self._parse)
                print(">>> %s\nBot:Got text \"%s\" from @%s and answered with \"%s\"."%(self._now,self._text_orig,self._username,self._answer))
            else:
                print(">>> %s\nBot:Got text \"%s\" from @%s."%(self._now,self._text,self._username))
            print("--------------------------------------------")


    def on_close(self, exception):
        self._now = str(datetime.datetime.now())
#        print(">>> %s"%(now))
        print(">>> %s\nBot:Close an delegator with @%s by calling on_close()."%(self._now,self._username))
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


### Now it starts run.
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
