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
files = [
    "resource.py",
    "ipcn.py",
    "httpapi.py"
]
for filename in files:
    if not os.path.exists(filename):
        print("\033[46m\033[31mERROR\033[0m: No avaliable \"\033[32m%s\033[0m\" was found. Please reinstall telebot."%(filename))
        exit()

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
print("A telegram bot program written by \033[32m%s\033[0m, ver \033[32m%s\033[0m."%(AUTHOR,VERSION))
print("Starting bot at \033[32m%s\033[0m..."%(now))


## Import telepot.
try:
    import telepot
    from telepot.delegate import per_from_id, create_open
    #from telepot.exception import TelepotException
except ImportError:
    print("\033[44m\033[33mWARNING\033[0m: Telepot api is lost...")
    print("Installing requirement via \"\033[32m$ sudo pip3 install telepot\033[0m\"...")
    try:
        subprocess.check_output("sudo pip3 install telepot", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except:
        print("\033[46m\033[31mERROR\033[0m: Install failed.")
        print("Maybe you should run \"\033[32m$ sudo pip3 install telepot\033[0m\" by yourself?")
        exit()

    import telepot
    from telepot.delegate import per_from_id, create_open
    #from telepot.exception import TelepotException


## Deal with args.
conf_rewrite = False

config_file = args.config
if config_file == None:
    print("\033[44m\033[33mWARNING\033[0m: It seems that you haven\'t choose a config file.")
    print("You are expected to make a config file like YOURBOTNAME.json, which contains you bot token from the BotFather, the admin user name and the Tuling Chat API Key, then run the program again by \"\033[32m$ python3 ./bot.py YOURBOTNAME.json\033[0m\".")
    config_file = input("However, you can also type your config file here and then press [ENTER] to make it continue: ")

try:
    with open(config_file) as config_open:
        bot_json = json.loads(config_open.read(), encoding="utf-8")
    TOKEN = bot_json["token"]
    ADMIN = bot_json["admin"]
    tuling_api_key = bot_json["tuling_api_key"]
except:
    TOKEN = None
    ADMIN = None
    tuling_api_key = None
    print("\033[44m\033[33mWARNING\033[0m: No avaliable \"\033[32m%s\033[0m\" was found."%(config_file))
    print("Writing a new config file with following settings...")
    conf_rewrite = True


if TOKEN == None or TOKEN == '' or TOKEN == "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI":
    print("\033[44m\033[33mWARNING\033[0m: It seems that you doesn't have an avalible bot token.")
    print("You are expected to get a bot token from the BotFather. It's a string on behalf of your bot.")
    print("If you haven\'t got it, you should ask the BotFather, and run the program again by \"\033[32m$ python3 ./bot.py YOURBOTNAME.json\033[0m\".")
    TOKEN = input("However, you can also type your bot token here and then press [ENTER] to make it continue: ")
    conf_rewrite = True

if ADMIN == None or ADMIN == '' or ADMIN == "Nobody":
    print("\033[44m\033[33mWARNING\033[0m: It seems that you haven\'t choose an admin user.")
    print("You are expected to choose an adminuser to use some advanced functions.")
    print("The admin user is usually yourself, so you should find your username which maybe also called nickname in the Settings of Telegram, notice the \'\033[32m@\033[0m\' is not a part of your username. If you haven\'t set it, you should set a username, and run the program again by \"\033[32m$ python3 ./bot.py YOURBOTNAME.json\033[0m\".")
    ADMIN = input("However, you can also type your admin user name here and then press [ENTER] to make it continue: ")
    conf_rewrite = True

if tuling_api_key == None or tuling_api_key == '' or tuling_api_key == "get_it_from_tuling123.com":
    print("\033[44m\033[33mWARNING\033[0m: It seems that you haven\'t set a Tuling Chat Api Key.")
    print("If no key the program will fallback to Qingyunke Chat Api, which doesn\'t need a key.")
    print("For a better chat experience, please go to \033[4mhttp://turling123.com/\033[0m, sign up for a key, and run the program again by \"\033[32m$ python3 ./bot.py YOURBOTNAME.json\033[0m\".")
    tuling_api_key == None


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
code_list = resource.code_list
#talk_list = resource.file_to_list("assets/talk.txt")
redo_dict = resource.json_to_dict("assets/redo.json")
rule_dict = resource.json_to_dict("assets/rule.json")


## Define an expection.
#class UserClose(TelepotException):
#    pass

### Used to store the message when a delegator closed.


## Define a bot class.
class TeleBot(telepot.helper.UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(TeleBot, self).__init__(seed_tuple, timeout)
        self._count = {
            "chat": 0,
            "fuck": 0
#            "talk": 0
        }


    def on_chat_message(self, msg):
        self._now = str(datetime.datetime.now())

        global redo_dict
        global rule_dict


        self._parse = None
        self._diswebview = None
        self._upload = None
        self._answer = None
        self._download = None
        self._refuse = False

        self._content_type, self._chat_type, self._chat_id = telepot.glance(msg)
        self._first_name = msg["from"]["first_name"]
        self._username = msg["from"]["username"]
        self._user_id = msg["from"]["id"]
        self._msg_id = msg["message_id"]

        ## To judge if the content is a text and deal with it.
        if self._content_type == "text":
            self._text_orig = self._text_log = msg["text"]

            ## Redo message?
            if self._text_orig == "/redo" or (self._text_orig == "/redo@" + info["username"]):
                try:
                    self._text_orig = redo_dict[self._username]
                    #redo_dict.pop(self._username)
                except KeyError:
                    #self._answer = "Sorry, but no your last message was found."
                    pass

            try:
                rule_dict.pop('')
            except:
                pass


            self._text_list = self._text_orig.split(None, 1)    # When sep was None, it will be any number spaces, and 1 means split once. Be care that S.split(, 1) will get an error, use S.split(None, 1) instead (from the help doc).
            try:
                self._text = self._text_list[0].lstrip('/')
                self._text_2 = self._text_list[1]
            except IndexError:
                self._text = self._text_list[0].lstrip('/')
                self._text_2 = None
            self._text = self._text.split('@' + info["username"], 1)[0]


            # Handle.
            if self._text == "start":
                self._answer = "Welcome! \nPlease type \"/help\" to get a help list."

            elif self._text == "help":
                self._answer = bhelp_list[0]
                self._parse = "HTML"
                self._diswebview = True

            elif self._text == "hello":
                self._answer = "Hello, " + self._first_name + "! " + random.choice(greeting_list)

            elif self._text == "joke":
                self._answer = random.choice(joke_list)

            elif self._text == "time":
                self._answer = "Now is " + str(datetime.datetime.now()) + "."
            elif self._text == "weather":
                if self._text_2 != None:
                    self._answer = httpapi.get_wea(self._text_2)
                    self._parse = "HTML"
                else:
                    self._answer = "Please add a valid place, for instance, \"/weather 上海\", \"/weather 安徽 合肥\" or \"/weather 中国 辽宁 大连\"."

            elif self._text == "fuck":
                try:
                    self._answer = fuck_list[self._count["fuck"]]
                    self._count["fuck"] += 1
                except IndexError:
                    self._count["fuck"] = 0
                    self._answer = fuck_list[self._count["fuck"]]
                    self._count["fuck"] += 1

            elif self._text == "talk":
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

            elif self._text == "count":
                self._answer = "Total chat: %d"%(self._count["chat"] + 1)

            elif self._text == "ipcn":
                if self._username == ADMIN:
                    self._answer = ipcn.get_ip()
                else:
                    self._answer = "Sorry, you are not allowed to obtain the ip address in order to keep the bot safe."

            elif self._text == "cmd":
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

            elif self._text == "send":
                if self._text_2 != None:
                    if self._username == ADMIN:
                        self._upload = self._text_2
                        self._answer = "Sent."
                    else:
                        self._answer = "Sorry, you are not allowed to get a file in order to keep the bot safe."
                else:
                    self._answer = None

            elif self._text == "code":
                resource.dict_to_json("assets/redo.json", redo_dict)
                resource.dict_to_json("assets/rule.json", rule_dict)
                ## Zip file.
                with zipfile.ZipFile('telebot.zip', 'w', zipfile.ZIP_DEFLATED) as self._telebot_zip:
                    for self._code in code_list:
                        self._telebot_zip.write(self._code, "telebot" + os.sep + self._code)
                self._upload = "telebot.zip"
                self._answer = "Sent code.\nYou should extract it to your directories and get your bot token. Then run \"$ python3 ./bot.py YOURBOTNAME.json\".\nFor more information, click <a href=\"https://github.com/S-X-ShaX/telebot/\">My TeleBot on GitHub</a>."
                self._parse = "HTML"

            elif self._text == "rule":
                if self._text_2 != None and "@@" in self._text_2:
                    self._rule_list = self._text_2.split("@@")
                    if self._rule_list[-1] != '':
                        for self._rule_key in self._rule_list[0:-1]:
                            if self._rule_key != '' and self._rule_key != '\n':
                                rule_dict[self._rule_key.lower()] = self._rule_list[-1]
                    else:
                        for self._rule_key in self._rule_list[0:-1]:
                            try:
                                rule_dict.pop(self._rule_key.lower())
                            except:
                                pass
                    self._answer = "Set rule!"
                else:
                    if len(rule_dict) != 0:
                        self._answers = "Total rules (case insensitive):\n"
                        for key in sorted(rule_dict, key=str.lower):
                            self._answers += (key + " => " + rule_dict[key] + '\n')
                        self._answer = self._answers.rstrip('\n')
                    else:
                        self._answer = "No rule."
                resource.dict_to_json("assets/rule.json", rule_dict)

            elif self._text == "redo":
                self._answer = "Sorry, but no your last message was found."

            else:
                if random.random() <= 0.7:
                    self._answers = ''
                    for key in rule_dict:
                        if key in self._text_orig.lower():
                            if not rule_dict[key] in self._answers:
                                self._answers += rule_dict[key] + '\n'
                                self._answer = self._answers.rstrip('\n')


        ## To judge if the content is a photo.
        elif self._content_type == "photo":
            if self._chat_type == "private":
                if self._username == ADMIN:
                    self._download = msg["photo"][-1]["file_id"]
                    self._document = "Image/IMG_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".jpg"
                    self._answer = "Got photo \"%s\"."%(self._document)
                else:
                    self._refuse = True
                    self._answer = "Sorry, only the admin user can save a photo on the bot."


        ## To judge if the content is a document.
        elif self._content_type == "document":
            if self._chat_type == "private":
                if self._username == ADMIN:
                    self._download = msg["document"]["file_id"]
                    self._document = "File/" + msg["document"]["file_name"]
                    self._answer = "Got document \"%s\"."%(self._document)
                else:
                    self._refuse = True
                    self._answer = "Sorry, only the admin user can save a document on the bot."


        # Return.
        if self._upload != None:
            try:
                with open(self._upload, 'rb') as self._filename:
                    bot.sendChatAction(self._chat_id, "upload_document")
                    bot.sendDocument(self._chat_id, self._filename)
            except:
                self._answer = "Upload failed."

        if self._download != None:
            try:
                bot.download_file(self._download, self._document)
            except:
                self._answer = "Download failed."
                self._refuse = True

        if self._answer != None:
            self._count["chat"] += 1
            ## Send result.
            if self._content_type == "text":
                ## Store redo message.
                #global redo_dict
                redo_dict[self._username] = self._text_orig

                bot.sendChatAction(self._chat_id, "typing")
                bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
                print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._text_log, self._username, self._answer))

            elif self._content_type == "photo":
                bot.sendChatAction(self._chat_id, "typing")
                bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
                if not self._refuse:
                    print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got photo \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._document, self._username, self._answer))
                else:
                    print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Refused to save a photo from from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._username, self._answer))

            elif self._content_type == "document":
                bot.sendChatAction(self._chat_id, "typing")
                bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
                if not self._refuse:
                    print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got document \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._document, self._username, self._answer))
                else:
                    print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Refused to save a document from from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._username, self._answer))
            print("--------------------------------------------")


    def on_close(self, exception):
        self._now = str(datetime.datetime.now())

        global redo_dict
        global rule_dict

        if len(redo_dict) > 77:
            redo_dict = {}
        if len(rule_dict) > 77:
            rule_dict = {}

        ## Journal.
        print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Closed an delegator with @\033[34m%s\033[0m by calling on_close()."%(self._now, self._username))
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
    conf_rewrite = False
    print("\033[46m\033[31mERROR\033[0m: Your token is invaild.")
    print("Please check what your config file \"%s\" contains."%(config_file))
    print("It should contain your token string in the token line.")
    print("Or you may need to check your network and system time, you can\'t connect to the bot server if your time is wrong or your network is down, and your bot token may also be considered invaild by the program.")
    exit()

if conf_rewrite:
    #with open(config_file, 'w') as config_open:
        #config_open.write(json.dumps({"token": TOKEN, "admin": ADMIN, "tuling_api_key": "get_it_from_tuling123.com"}, ensure_ascii=False))
    resource.dict_to_json(config_file, {"token": TOKEN, "admin": ADMIN, "tuling_api_key": "get_it_from_tuling123.com"})

print("\033[7m############################################\033[0m")
print("\033[7m#\033[0m" + "  ".center(42) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35mconfigfile\033[0m: %s"%(config_file)).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35mbotid\033[0m: %s"%(info["id"])).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35musername\033[0m: %s"%(info["username"])).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35mfirstname\033[0m: %s"%(info["first_name"])).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35madminuser\033[0m: %s"%(ADMIN)).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + "  ".center(42) + "\033[7m#\033[0m")
print("\033[7m############################################\033[0m")


print("\033[33mBot\033[0m: I am listening...")
print("--------------------------------------------")


try:
    bot.message_loop(run_forever=True)
except KeyboardInterrupt:
    resource.dict_to_json("assets/redo.json", redo_dict)
    resource.dict_to_json("assets/rule.json", rule_dict)
    exit()
except:
    pass
