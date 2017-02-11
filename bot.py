#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: bot.py
## Created by 请叫我喵 Alynx
# sxshax@gmail.com, http://alynx.xyz/


### Launch.

## Importing.
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


AUTHOR = "AlynxZhou"
VERSION = "4.0"


## Get args.
aparser = argparse.ArgumentParser(description="A telegram bot program.")
#aparser.add_argument("-t", "--token", help="Get the file that stored the bot token.", action="store")
#aparser.add_argument("-a", "--admin", help="Get the admin user\'s name", action="store")
aparser.add_argument("config", action="store", type=str, help="The bot config file.")
args = aparser.parse_args()


print("A telegram bot program written by \033[32m%s\033[0m, ver \033[32m%s\033[0m."%(AUTHOR,VERSION))
print("Starting bot at \033[32m%s\033[0m..."%(str(datetime.datetime.now())))


## Import telepot.
try:
	import telepot
	from telepot.delegate import pave_event_space, per_from_id, create_open
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
assets = {}
assets["bhelp_list"] = resource.file_to_list("assets/bhelp.txt")
assets["greeting_list"] = resource.file_to_list("assets/greeting.txt")
assets["joke_list"] = resource.file_to_list("assets/joke.txt")
assets["fuck_list"] = resource.fuck_list
assets["code_list"] = resource.code_list
#talk_list = resource.file_to_list("assets/talk.txt")
assets["redo_dict"] = resource.json_to_dict("assets/redo.json")
assets["rule_dict"] = resource.json_to_dict("assets/rule.json")
assets["echo_list"] = resource.eval_to_list("assets/echo.txt")

## Define an expection.
#class UserClose(TelepotException):
#	pass


## A switch of bot.
switch = True


## Define a bot class.
class TeleBot(telepot.helper.UserHandler):
	def __init__(self, *args, **kwargs):
		super(TeleBot, self).__init__(*args, **kwargs)
		self._count = {
			"chat": 0,
			"fuck": 0
			#"talk": 0
		}

	def on_chat_message(self, msg):
		self._now = str(datetime.datetime.now())

		global redo_dict
		global rule_dict
		global switch
		global echo_list

		self._parse = None
		self._diswebview = None
		self._sticker = None
		self._upload = None
		self._download = None
		self._answer = None
		self._refuse = False

		self._content_type, self._chat_type, self._chat_id = telepot.glance(msg)

		try:
			self._first_name = msg["from"]["first_name"]
			self._username = msg["from"]["username"]
			self._user_id = msg["from"]["id"]
			self._msg_id = msg["message_id"]
		except KeyError as e:
			self.on_close(e)

		try:
			{
				"text": self.on_text,
				"sticker": self.on_sticker,
				"photo": self.on_photo,
				"document": self.on_document
			}[self._content_type](msg)
		except KeyError:
			pass

		# Return.
		if self._sticker != None and switch:
			bot.sendChatAction(self._chat_id, "typing")
			bot.sendSticker(self._chat_id, self._sticker, disable_notification=None, reply_to_message_id=self._msg_id, reply_markup=None)
			print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with sticker \"\033[32m%s\033[0m\"."%(self._now, self._text_log, self._username, self._answer))

		if self._upload != None and switch:
			try:
				with open(self._upload, 'rb') as self._filename:
					bot.sendChatAction(self._chat_id, "upload_document")
					bot.sendDocument(self._chat_id, self._filename, reply_to_message_id=self._msg_id)
			except:
				self._answer = "Upload failed."

		if self._download != None and switch:
			try:
				bot.download_file(self._download, self._document)
			except:
				self._answer = "Download failed."
				self._refuse = True

		if self._answer != None and switch:
			self._count["chat"] += 1
			## Send result.
			if (self._content_type == "text" and self._sticker == None):
				## Store redo message.
				#global redo_dict
				assets["redo_dict"][self._username] = self._text_orig
				if not self._chat_id in echo_list:
					echo_list.append(self._chat_id)

				bot.sendChatAction(self._chat_id, "typing")
				bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
				print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._text_log, self._username, self._answer))

			elif self._content_type == "sticker":
				bot.sendChatAction(self._chat_id, "typing")
				bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
				print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got sticker \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\"."%(self._now, self._sticker_emoji, self._username, self._answer))

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
		global echo_list

		if len(redo_dict) > 77:
			redo_dict = {}
		if len(rule_dict) > 77:
			rule_dict = {}
		while len(echo_list) > 7:
			echo_list.pop(0)

		## Journal.
		try:
			print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Closed an delegator with @\033[34m%s\033[0m by calling on_close()."%(self._now, self._username))
		except:
			print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Closed an delegator by calling on_close()."%(self._now))
		print("--------------------------------------------")


### Now it starts run.
print("Getting bot information...")

### Generate a bot object.
bot = telepot.DelegatorBot(
	TOKEN, [
			pave_event_space()(
			per_from_id(),
			create_open, TeleBot, timeout=30
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
	resource.dict_to_json(config_file, {"token": TOKEN, "admin": ADMIN, "tuling_api_key": "get_it_from_tuling123.com"})

print("\033[7m############################################\033[0m")
print("\033[7m#\033[0m" + "      ".center(42) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35mconfigfile\033[0m: %s"%(config_file)).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35mbotid\033[0m: %s"%(info["id"])).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35musername\033[0m: %s"%(info["username"])).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35mfirstname\033[0m: %s"%(info["first_name"])).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + ("\033[35madminuser\033[0m: %s"%(ADMIN)).center(51) + "\033[7m#\033[0m")
print("\033[7m#\033[0m" + "      ".center(42) + "\033[7m#\033[0m")
print("\033[7m############################################\033[0m")


print("\033[33mBot\033[0m: I am listening...")
print("--------------------------------------------")


try:
	bot.message_loop(run_forever=True)
except KeyboardInterrupt:
	resource.dict_to_json("assets/redo.json", redo_dict)
	resource.dict_to_json("assets/rule.json", rule_dict)
	resource.list_to_file("assets/echo.txt", echo_list)
	exit()
except:
	pass
