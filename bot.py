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


now = str(datetime.datetime.now())
print("A telegram bot program written by \033[32m%s\033[0m, ver \033[32m%s\033[0m."%(AUTHOR,VERSION))
print("Starting bot at \033[32m%s\033[0m..."%(now))


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
bhelp_list = resource.file_to_list("assets/bhelp.txt")
greeting_list = resource.file_to_list("assets/greeting.txt")
joke_list = resource.file_to_list("assets/joke.txt")
fuck_list = resource.fuck_list
code_list = resource.code_list
#talk_list = resource.file_to_list("assets/talk.txt")
redo_dict = resource.json_to_dict("assets/redo.json")
rule_dict = resource.json_to_dict("assets/rule.json")
echo_list = resource.eval_to_list("assets/echo.txt")

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

	def on_start(self):
		self._answer = "Welcome! \nPlease type \"/help\" to get a help list."

	def on_help(self):
		self._answer = bhelp_list[0]
		self._parse = "HTML"
		self._diswebview = True

	def on_hello(self):
		self._answer = "Hello, " + self._first_name + "! " + random.choice(greeting_list)

	def on_joke(self):
		self._answer = random.choice(joke_list)

	def on_time(self):
		self._answer = "Now is " + str(datetime.datetime.now()) + "."

	def on_weather(self):
		if self._text_2 != None:
			self._answer = httpapi.get_wea(self._text_2)
			self._parse = "HTML"
		else:
			self._answer = "Please add a valid place, for instance, \"/weather 上海\", \"/weather 安徽 合肥\" or \"/weather 中国 辽宁 大连\"."

	def on_fuck(self):
		try:
			self._answer = fuck_list[self._count["fuck"]]
			self._count["fuck"] += 1
		except IndexError:
			self._count["fuck"] = 0
			self._answer = fuck_list[self._count["fuck"]]
			self._count["fuck"] += 1

	def on_talk(self):
		if self._text_2 != None:
			if tuling_api_key == None:
				self._answer = httpapi.get_qtalk(self._text_2)
			else:
				self._answer = httpapi.get_ttalk(tuling_api_key, self._text_2, str(self._user_id))
				self._parse = "HTML"
		else:
			self._answer = "Please add what you want to talk about, for example \"/talk 你好\"."

	def on_count(self):
		self._answer = "<strong>Total chat:</strong>\n%d"%(self._count["chat"] + 1)
		self._parse = "HTML"

	def on_ipcn(self):
		if self._username == ADMIN:
			if self._chat_type == "private":
				self._answer = ipcn.get_ip()
			else:
				self._answer = "Sorry, you should obtain the ip address via private chat in order to keep the bot safe."
		else:
			self._answer = "Sorry, you are not allowed to obtain the ip address in order to keep the bot safe."

	def on_cmd(self):
		if self._text_2 != None:
			if self._username == ADMIN:
				try:
					self._answer = "<strong>Result:</strong>\n" + subprocess.check_output(self._text_2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
					self._parse = "HTML"
				except subprocess.CalledProcessError:
					self._answer = "Sorry, invalid command."
			else:
				self._answer = "Sorry, you are not allowed to run a command in order to keep the bot safe."

	def on_echo(self):
		global echo_list
		temp_list = []
		for chat_id in echo_list:
			if not chat_id in temp_list:
				temp_list.append(chat_id)
		echo_list = temp_list
		if self._text_2 != None:
			if self._username == ADMIN:
				for chat_id in echo_list:
                                        try:
                                                bot.sendChatAction(chat_id, "typing")
                                                bot.sendMessage(chat_id, self._text_2)
                                        except:
                                                pass
				self._answer = "Echoed."
			else:
				self._answer = "Sorry, only the ADMIN user can send an echo."
		resource.list_to_file("assets/echo.txt", echo_list)

	def on_send(self):
		if self._text_2 != None:
			if self._username == ADMIN:
				self._upload = self._text_2
				self._answer = "Sent."
			else:
				self._answer = "Sorry, you are not allowed to get a file in order to keep the bot safe."

	def on_code(self):
		global redo_dict
		global rule_dict
		global echo_list
		resource.dict_to_json("assets/redo.json", redo_dict)
		resource.dict_to_json("assets/rule.json", rule_dict)
		resource.list_to_file("assets/echo.txt", echo_list)
		## Zip file.
		with zipfile.ZipFile("telebot.zip", 'w', zipfile.ZIP_DEFLATED) as self._telebot_zip:
			for self._code in code_list:
				self._telebot_zip.write(self._code, "telebot" + os.sep + self._code)
		self._upload = "telebot.zip"
		self._answer = "Sent code.\nYou should extract it to your directories and get your bot token. Then run \"$ python3 ./bot.py YOURBOTNAME.json\".\nFor more information, click <a href=\"https://github.com/AlynxZhou/telebot/\">My TeleBot on GitHub</a>."
		self._parse = "HTML"

	def on_rule(self):
		global rule_dict
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
				self._answers = "<strong>Total rules:</strong>\nFollowings are case insensitive.\n"
				for key in sorted(rule_dict, key=str.lower):
					self._answers += (key + " <em>=></em> " + rule_dict[key] + '\n')
				self._answer = self._answers.rstrip('\n')
				self._parse = "HTML"
			else:
				self._answer = "No rule."
		resource.dict_to_json("assets/rule.json", rule_dict)

	def on_redo(self):
		self._answer = "Sorry, but no your last message was found."

	def on_text(self, msg):
		global redo_dict
		global switch

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


		self._text_list = self._text_orig.split(None, 1)	# When sep was None, it will be any number spaces, and 1 means split once. Be care that S.split(, 1) will get an error, use S.split(None, 1) instead (from the help doc).
		try:
			self._text = self._text_list[0]#.lstrip('/')
			self._text_2 = self._text_list[1]
		except IndexError:
			self._text = self._text_list[0]#.lstrip('/')
			self._text_2 = None
		self._text = self._text.split('@' + info["username"], 1)[0]


		if self._text == "/switch" and switch:
			if self._username == ADMIN:
				switch = False
				self._answer = "<strong>Status:</strong> Turned <em>OFF</em>."
				self._parse = "HTML"
				redo_dict[self._username] = self._text_orig

				bot.sendChatAction(self._chat_id, "typing")
				bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
				print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\" and turned \033[30;41mOFF\033[0m."%(self._now, self._text_log, self._username, self._answer))
				print("--------------------------------------------")
			else:
				self._answer = "Sorry, only the admin user can switch the bot to OFF."

		elif self._text == "/switch" and not switch:
			switch = True
			self._answer = "<strong>Status:</strong> Turned <em>ON</em>."
			self._parse = "HTML"
			redo_dict[self._username] = self._text_orig

			bot.sendChatAction(self._chat_id, "typing")
			bot.sendMessage(self._chat_id, self._answer, reply_to_message_id=self._msg_id, parse_mode=self._parse, disable_web_page_preview=self._diswebview)
			print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\" and turned \033[30;46mON\033[0m."%(self._now, self._text_log, self._username, self._answer))
			print("--------------------------------------------")
			self._answer = None	# Or it will answer twice.


		# Handle.
		try:
			{
				"/start": self.on_start,
				"/help": self.on_help,
				"/hello": self.on_hello,
				"/joke": self.on_joke,
				"/time": self.on_time,
				"/weather": self.on_weather,
				"/fuck": self.on_fuck,
				"/talk": self.on_talk,
				"/count": self.on_count,
				"/ipcn": self.on_ipcn,
				"/cmd": self.on_cmd,
				"/echo": self.on_echo,
				"/send": self.on_send,
				"/code": self.on_code,
				"/rule": self.on_rule,
				"/redo": self.on_redo
			}[self._text]()
		except KeyError:
			if self._text.lstrip('/')[0] == '-':
				self._text_2 = self._text_orig.lstrip('/').lstrip('-')
				self.on_talk()
			else:
				self._answers = ''
				for key in rule_dict:
					if key in self._text_orig.lower():
						if not rule_dict[key] in self._answers:
							self._answers += rule_dict[key] + '\n'
							self._answer = self._answers.rstrip('\n')
				#elif random.random() <= 0.33:
					#self._sticker = random.choice(list(resource.sticker_dict.keys()))
					#self._answer = resource.sticker_dict[self._sticker]

	def on_sticker(self, msg):
		self._sticker_id = msg["sticker"]["file_id"]
		self._sticker_emoji = msg["sticker"]["emoji"]
		#print("\"%s\": \'%s\',"%(self._sticker_id, self._sticker_emoji))
		if (self._sticker_id, self._sticker_emoji) in resource.red_sticker_dict.items():
			self._answer = random.choice(["红脸的关公战长沙！", "红脸哥～我是你的超级粉丝～", "红脸哥我要给你生一车猴子🐒！"])
		#else:
			#print("\"%s\": \'%s\',"%(self._sticker_id, self._sticker_emoji))

	def on_photo(self, msg):
		if self._chat_type == "private":
			if self._username == ADMIN:
				self._download = msg["photo"][-1]["file_id"]
				self._document = "Image/IMG_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".jpg"
				self._answer = "Got photo \"<em>%s</em>\"."%(self._document)
				self._parse = "HTML"
			else:
				self._refuse = True
				self._answer = "Sorry, only the admin user can save a photo on the bot."

	def on_document(self, msg):
		if self._chat_type == "private":
			if self._username == ADMIN:
				self._download = msg["document"]["file_id"]
				self._document = "File/" + msg["document"]["file_name"]
				self._answer = "Got document \"<em>%s</em>\"."%(self._document)
				self._parse = "HTML"
			else:
				self._refuse = True
				self._answer = "Sorry, only the admin user can save a document on the bot."

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
				redo_dict[self._username] = self._text_orig
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
