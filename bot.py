#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: bot.py


### Launch.

### Importing.
import os
import json
import random
import zipfile
import datetime
import argparse
import subprocess

## Custom modules.
import resource
import ipcn
import httpapi


AUTHOR = "S-X-ShaX"
VERSION = "3.7"


## Get args.
aparser = argparse.ArgumentParser(description="A telegram bot program.")
#aparser.add_argument("-t", "--token", help="Get the file that stored the bot token.", action="store")
#aparser.add_argument("-a", "--admin", help="Get the admin user\'s name", action="store")
aparser.add_argument("config", action="store", type=str, help="The bot config file.")
args = aparser.parse_args()


now = str(datetime.datetime.now())
print("A telegram bot program written by %s, ver %s."%(AUTHOR,VERSION))
print("Starting bot at %s..."%(now))


## Import telepot.
try:
    import telepot
    from telepot.delegate import per_from_id, create_open
    #from telepot.exception import TelepotException
except ImportError:
    print("Telepot api is lost...")
    print("Installing requirement via \"$ sudo pip3 install telepot\"...")
    try:
        subprocess.check_output("sudo pip3 install telepot", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except:
        print("ERROR: Install failed.")
        print("Maybe you should run \"$ sudo pip3 install telepot\" by yourself?")
        exit()

    import telepot
    from telepot.delegate import per_from_id, create_open
    #from telepot.exception import TelepotException


## Deal with args.
conf_rewrite = False

config_file = args.config
if config_file == None:
    print("\nWARNING: It seems that you haven\'t choose a config file.")
    print("You are expected to make a config file like YOURBOTNAME.json, which contains you bot token from the BotFather, the admin user name and the Tuling Chat API Key, then run the program again by \"$ python3 ./bot.py YOURBOTNAME.json\".")
    config_file = input("However, you can also type your config file here and then press [ENTER] to make it continue: ")
    print('\n')

try:
    with open(config_file) as config_open:
        bot_json = json.loads(config_open.read(), encoding="utf-8")
    TOKEN = bot_json["token"]
    ADMIN = bot_json["admin"]
    tuling_api_key = bot_json["tuling_api_key"]
except FileNotFoundError:
    TOKEN = None
    ADMIN = None
    tuling_api_key = None
    print("\nWarning: No avaliable \"%s\" was found."%(config_file))
    print("Writing a new config file with following settings...")
    conf_rewrite = True


if TOKEN == None or TOKEN == '' or TOKEN == "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI":
    print("\nWARNING: It seems that you doesn't have an avalible bot token.")
    print("You are expected to get a bot token from the BotFather. It's a string on behalf of your bot.")
    print("If you haven\'t got it, you should ask the BotFather, and run the program again by \"$ python3 ./bot.py YOURBOTNAME.json\".")
    TOKEN = input("However, you can also type your bot token here and then press [ENTER] to make it continue: ")
    print('\n')
    conf_rewrite = True

if ADMIN == None or ADMIN == '' or ADMIN == "Nobody":
    print("\nWARNING: It seems that you haven\'t choose an admin user.")
    print("You are expected to choose an adminuser to use some advanced functions.")
    print("The admin user is usually yourself, so you should find your username which maybe also called nickname in the Settings of Telegram, notice the \'@\' is not a part of your username. If you haven\'t set it, you should set a username, and run the program again by \"$ python3 ./bot.py YOURBOTNAME.json\".")
    ADMIN = input("However, you can also type your admin user name here and then press [ENTER] to make it continue: ")
    print('\n')
    conf_rewrite = True

if tuling_api_key == None or tuling_api_key == '' or tuling_api_key == "get_it_from_tuling123.com":
    print("\nWARNING: It seems that you haven\'t set a Tuling Chat Api Key.")
    print("If no key the program will fallback to Qingyunke Chat Api, which doesn\'t need a key.")
    print("For a better chat experience, please go to http://turling123.com, sign up for a key, and run the program again by \"$ python3 ./bot.py YOURBOTNAME.json\".")
    print('\n')
    tuling_api_key == None


if conf_rewrite:
    with open(config_file, 'w') as config_open:
        config_open.write(json.dumps({"token": TOKEN, "admin": ADMIN, "tuling_api_key": "get_it_from_tuling123.com"}, ensure_ascii=False))


### Check directories.
dirs = [
    "Image",
    "Video",
    "Audio",
    "File"
]
for directory in dirs:
    resource.check_dir(directory)


### Get resources.
bhelp_list = resource.file_to_list("assets/bhelp.txt")
greeting_list = resource.file_to_list("assets/greeting.txt")
joke_list = resource.file_to_list("assets/joke.txt")
fuck_list = resource.fuck_list
#talk_list = resource.file_to_list("assets/talk.txt")

try:
    with open("assets/rule.json") as rule_open:
        rule_dict = json.loads(rule_open.read(), encoding="utf-8")
except:
    rule_dict = {}


## Define an expection.
#class UserClose(TelepotException):
#    pass

### Used to store the message when a delegator closed.

redo_dict = {}

## Define a bot class.
class TeleBot(telepot.helper.UserHandler):

    def __init__(self, seed_tuple,timeout):
        super(TeleBot, self).__init__(seed_tuple, timeout)
        self._count = {
            "chat": 0,
            "fuck": 0
#            "talk": 0
        }


    def on_chat_message(self, msg):
        self._now = str(datetime.datetime.now())

        self._count["chat"] += 1
        self._parse = None
        self._diswebview = None

        content_type, chat_type, chat_id = telepot.glance(msg)
        self._first_name = msg["from"]["first_name"]
        self._username = msg["from"]["username"]
        self._user_id = msg["from"]["id"]
        self._msg_id = msg["message_id"]

        ## To judge if the content is a text and deal with it.
        if content_type == "text":
            self._text_orig = self._text_log = msg["text"]

            ## Redo message?
            if self._text_orig == "/redo" or (self._text_orig == "/redo@" + info["username"]):
                try:
                    self._text_orig = self._text_redo
                except AttributeError:
                    try:
                        self._text_orig = self._text_redo = redo_dict[self._username]
                        redo_dict.pop(self._username)
                    except KeyError:
                        #self._answer = "Sorry, but no your last message was found."
                        pass

            try:
                self._text_list = self._text_orig.split(None, 1)    # When sep was None, it will be any number spaces, and 1 means split once. Be care that S.split(, 1) will get an error,use S.split(None, 1) instead (from the help doc).
                self._text = self._text_list[0]
                self._text_2 = self._text_list[1]
            except IndexError:
                self._text = self._text_list[0]
                self._text_2 = None
            if ('@' + info["username"]) in self._text:
                self._text = self._text.split('@' + info["username"], 1)[0]


            # Handle.
            if self._text == "/start":
                self._answer = "Welcome! \nPlease type \"/help\" to get a help list."

            elif self._text == "/help":
                self._answer = bhelp_list[0]
                self._parse = "HTML"
                self._diswebview = True

            elif self._text == "/hello":
                self._answer = "Hello, " + self._first_name + "! " + random.choice(greeting_list)

            elif self._text == "/joke":
                self._answer = random.choice(joke_list)

            elif self._text == "/time":
                self._answer = "Now is " + str(datetime.datetime.now()) + "."
            elif self._text == "/weather":
                if self._text_2 != None:
                    self._answer = httpapi.get_wea(self._text_2)
                    self._parse = "HTML"
                else:
                    self._answer = "Please add a valid place, for instance, \"/weather 上海\", \"/weather 安徽 合肥\" or \"/weather 中国 辽宁 大连\"."

            elif self._text == "/fuck":
                try:
                    self._answer = fuck_list[self._count["fuck"]]
                    self._count["fuck"] += 1
                except IndexError:
                    self._count["fuck"] = 0
                    self._answer = fuck_list[self._count["fuck"]]
                    self._count["fuck"] += 1

            elif self._text == "/talk":
                if self._text_2 != None:
                    if tuling_api_key == None:
                        self._answer = httpapi.get_qtalk(self._text_2)
                    else:
                        self._answer = httpapi.get_ttalk(tuling_api_key, self._text_2, str(self._user_id))
                else:
                    self._answer = "Please add what you want to talk about, for example \"/talk 你好\"."
                """
                try:
                    self._answer = talk_list[self._count["talk"]]
                    self._count["talk"] += 1
                except IndexError:
                    self._count["talk"] = 0
                    self._answer = talk_list[self._count["talk"]]
                    self._count["talk"] += 1
                """

            elif self._text == "/count":
                self._answer = self._count["chat"]

            elif self._text == "/ipcn":
                if self._username == ADMIN:
                    self._answer = ipcn.get_ip()
                else:
                    self._answer = "Sorry, you are not allowed to obtain the ip address in order to keep the bot safe."

            elif self._text == "/cmd":
                if self._text_2 != None:
                    if self._username == ADMIN:
                        try:
                            self._answer = subprocess.check_output(self._text_2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                        except subprocess.CalledProcessError:
                            self._answer = "Sorry, invalid command."
                    else:
                        self._answer = "Sorry, you are not allowed to run a command in order to keep the bot safe."
                else:
                    self._answer = None

            elif self._text == "/send":
                if self._text_2 != None:
                    if self._username == ADMIN:
                        bot.sendChatAction(chat_id, "upload_document")
                        try:
                            with open(self._text_2) as self._document:
                                bot.sendDocument(chat_id, self._document)
                        except:
                            with open(self._text_2, "rb") as self._document:
                                bot.sendDocument(chat_id, self._document)
                        self._answer = "Sent."
                    else:
                        self._answer = "Sorry, you are not allowed to get a file in order to keep the bot safe."
                else:
                    self._answer = None

            elif self._text == "/code":
                codes = [
                    "bot.py",
                    "resource.py",
                    "ipcn.py",
                    "httpapi.py",
                    "assets/greeting.txt",
                    "assets/bhelp.txt",
                    "assets/joke.txt",
                    "assets/rule.json",
                    "example_bot.json",
                    "README.md"
                ]
                ## Zip file.
                with zipfile.ZipFile('telebot.zip', 'w', zipfile.ZIP_DEFLATED) as self._telebot_zip:
                    for self._code in codes:
                        self._telebot_zip.write(self._code, "telebot" + os.sep + self._code)
                ## Send zip file, can't send as a zipfile object, must file object.
                with open('telebot.zip', 'rb') as self._codes:
                    bot.sendChatAction(chat_id, "upload_document")
                    bot.sendDocument(chat_id, self._codes)

                """
                for self._code_file in codes:
                    with open(self._code_file) as self._code_byte:
                        bot.sendChatAction(chat_id, "upload_document")
                        bot.sendDocument(chat_id, self._code_byte)
                """
                self._answer = "Sent code.\nYou should extract it to your directories and get your bot token. Then run \"$ python3 ./bot.py YOURBOTNAME.json\".\nFor more information, click <a href=\"https://github.com/S-X-ShaX/telebot/\">My TeleBot on GitHub</a>."
                self._parse = "HTML"

            elif self._text == "/rule":
                if self._text_2 != None and "@@" in self._text_2:
                    try:
                        self._rule_list = self._text_2.split("@@")
                        for self._rule_key in self._rule_list[0:-1]:
                            if self._rule_key != '' and self._rule_list[-1] != '':
                                global rule_dict
                                #rule_dict['/' + self._rule_key] = self._rule_list[-1]
                                rule_dict[self._rule_key] = self._rule_list[-1]
                                self._answer = "Get rule!"
                            else:
                                self._answer = "No avalible rule! You should use \"/rule /KEY1@@/KEY2@@/KEYn@@ANSWER\" to set a rule."
                    except AttributeError:
                        self._answer = "No avalible rule! You should use \"/rule /KEY1@@/KEY2@@/KEYn@@ANSWER\" to set a rule."
                else:
                    self._answer = "No avalible rule! You should use \"/rule KEY1,,KEY2,,...,,ANSWER\" to set a rule."

            elif self._text == "/redo":
                self._answer = "Sorry, but no your last message was found."

            else:
                try:
                    self._answer = rule_dict[self._text]
                except KeyError:
                    self._answer = None


            # Return.
            if self._answer != None:
                ## Store redo message.
                self._text_redo = self._text_orig
                ## Send result.
                bot.sendChatAction(chat_id, "typing")
                bot.sendMessage(chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
                print(">>> %s\nBot: Got text \"%s\" from @%s and answered with \"%s\"."%(self._now, self._text_log, self._username, self._answer))
            #else:
                #print(">>> %s\nBot: Got text \"%s\" from @%s."%(self._now, self._text_log, self._username))
                print("--------------------------------------------")
            #print("--------------------------------------------")

        """
        ## To judge if the content is a photo.
        elif content_type == "photo":
            file_id = msg["photo"][-1]["file_id"]
            if chat_type == "private":
                if username == ADMIN:
                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                    bot.downloadFile(file_id, "Image/IMG_%s.jpg"%(now))
                    bot.sendMessage(chat_id, "Got photo IMG_%s.jpg in Image/."%(now), reply_to_message_id=msg_id)
                    print("Bot: Got photo Image/IMG_%s.jpg from @%s."%(now, username))
                else:
                    answer = "Sorry, only the admin user can save a photo on the bot."
                    bot.sendMessage(chat_id, "%s"%(answer), reply_to_message_id=msg_id)
                    print("Bot: Refused save a photo from @%s."%(username))


        elif content_type == "document":
            file_id = msg["document"]["file_id"]
            file_name = msg["document"]["file_name"]
            if chat_type == "private":
                if username == ADMIN:
                    bot.downloadFile(file_id,  "File/%s"%(file_name))
                    bot.sendMessage(chat_id, "Got file %s in File/."%(file_name), reply_to_message_id=msg_id)
                    print("Bot: Got file File/%s from @%s."%(file_name, username))
                else:
                    answer = "Sorry, only the admin user can save a file on the bot."
                    bot.sendMessage(chat_id, "%s"%(answer), reply_to_message_id=msg_id)
                    print("Bot: Refused save a file from @%s."%(username))
        print("--------------------------------------------")
        """

    def on_close(self, exception):
        self._now = str(datetime.datetime.now())

        ## Store message.
        global redo_dict
        try:
            redo_dict[self._username] = self._text_redo
        except AttributeError:
            pass

        global rule_dict
        if len(rule_dict) > 77:
            rule_dict = {}
        if len(redo_dict) > 77:
            redo_dict = {}

        ## Journal.
        print(">>> %s\nBot: Close an delegator with @%s by calling on_close()."%(self._now, self._username))
        print("--------------------------------------------")


### Now it starts run.
print("Getting bot information...")

### Generate a bot object.
bot = telepot.DelegatorBot(
    TOKEN,
    [
        (
            per_from_id(),
            create_open(TeleBot, timeout=30)
        )
    ]
)


### Now it prints your bot information.
try:
    info = bot.getMe()
except KeyboardInterrupt:
    exit()
except:
    print("ERROR: Your token is invaild.")
    print("Please check what your config file \"%s\" contains."%(config_file))
    print("It should contain your token string in the token line, without anything else.")
    print("Or you may need to check your network and system time, you can\'t connect to the bot server if your time is wrong or your network is down, and your bot token may also be considered invaild by the program.")
    exit()

print("############################################")
print("#")
print("# configfile: %s"%(config_file))
print("# botid: %s"%(info["id"]))
print("# username: %s"%(info["username"]))
print("# firstname: %s"%(info["first_name"]))
print("# adminuser: %s"%(ADMIN))
print("#")
print("############################################")


print("Bot: I am listening...")
print("--------------------------------------------")


try:
    bot.message_loop(run_forever=True)
except KeyboardInterrupt:
    with open("assets/rule.json", 'w') as rule_open:
        rule_open.write(json.dumps(rule_dict, ensure_ascii=False))
    exit()
