#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Filename: handler.py
# Created by 请叫我喵 Alynx.
# sxshax@gmail.com, http://alynx.xyz/

class Handler:
    def __init__(self, count):
        self._count = count

	def on_start(self):
		self._answer["text"] = "Welcome!\nPlease type \"/help\" to get a help list."

	def on_help(self):
		self._answer["text"] = bhelp_list[0]
		self._answer["parse"] = "HTML"
		self._answer["diswebview"] = True

	def on_hello(self):
		self._answer["text"] = "Hello, " + self._first_name + "! " + random.choice(greeting_list)

	def on_joke(self):
		self._answer["text"] = random.choice(joke_list)

	def on_time(self):
		self._answer["text"] = "Now is " + str(datetime.datetime.now()) + "."

	def on_weather(self):
		if self._text_2 != None:
			self._answer["text"] = httpapi.get_wea(self._text_2)
			self._answer["parse"] = "HTML"
		else:
			self._answer["text"] = "Please add a valid place, for instance, \"/weather 上海\", \"/weather 安徽 合肥\" or \"/weather 中国 辽宁 大连\"."

	def on_fuck(self):
		try:
			self._answer["text"] = fuck_list[self._count["fuck"]]
			self._count["fuck"] += 1
		except IndexError:
			self._count["fuck"] = 0
			self._answer["text"] = fuck_list[self._count["fuck"]]
			self._count["fuck"] += 1

	def on_talk(self):
		if self._text_2 != None:
			if tuling_api_key == None:
				self._answer["text"] = httpapi.get_qtalk(self._text_2)
			else:
				self._answer["text"] = httpapi.get_ttalk(tuling_api_key, self._text_2, str(self._user_id))
				self._answer["parse"] = "HTML"
		else:
			self._answer["text"] = "Please add what you want to talk about, for example \"/talk 你好\"."

	def on_count(self):
		self._answer["text"] = "<strong>Total chat:</strong>\n%d"%(self._count["chat"] + 1)
		self._answer["parse"] = "HTML"

	def on_ipcn(self):
		if self._username == ADMIN:
			if self._chat_type == "private":
				self._answer["text"] = ipcn.get_ip()
			else:
				self._answer["text"] = "Sorry, you should obtain the ip address via private chat in order to keep the bot safe."
		else:
			self._answer["text"] = "Sorry, you are not allowed to obtain the ip address in order to keep the bot safe."

	def on_cmd(self):
		if self._text_2 != None:
			if self._username == ADMIN:
				try:
					self._answer["text"] = "<strong>Result:</strong>\n" + subprocess.check_output(self._text_2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
					self._answer["parse"] = "HTML"
				except subprocess.CalledProcessError:
					self._answer["text"] = "Sorry, invalid command."
			else:
				self._answer["text"] = "Sorry, you are not allowed to run a command in order to keep the bot safe."

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
				self._answer["text"] = "Echoed."
			else:
				self._answer["text"] = "Sorry, only the ADMIN user can send an echo."
		resource.list_to_file("assets/echo.txt", echo_list)

	def on_send(self):
		if self._text_2 != None:
			if self._username == ADMIN:
				self._answer["upload"] = self._text_2
				self._answer["text"] = "Sent."
			else:
				self._answer["text"] = "Sorry, you are not allowed to get a file in order to keep the bot safe."

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
		self._answer["upload"] = "telebot.zip"
		self._answer["text"] = "Sent code.\nYou should extract it to your directories and get your bot token. Then run \"$ python3 ./bot.py YOURBOTNAME.json\".\nFor more information, click <a href=\"https://github.com/AlynxZhou/telebot/\">My TeleBot on GitHub</a>."
		self._answer["parse"] = "HTML"

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
			self._answer["text"] = "Set rule!"
		else:
			if len(rule_dict) != 0:
				self._answer["text"]s = "<strong>Total rules:</strong>\nFollowings are case insensitive.\n"
				for key in sorted(rule_dict, key=str.lower):
					self._answer["text"]s += (key + " <em>=></em> " + rule_dict[key] + '\n')
				self._answer["text"] = self._answer["text"]s.rstrip('\n')
				self._answer["parse"] = "HTML"
			else:
				self._answer["text"] = "No rule."
		resource.dict_to_json("assets/rule.json", rule_dict)

	def on_redo(self):
		self._answer["text"] = "Sorry, but no your last message was found."

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
				#self._answer["text"] = "Sorry, but no your last message was found."
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
				self._answer["text"] = "<strong>Status:</strong> Turned <em>OFF</em>."
				self._answer["parse"] = "HTML"
				redo_dict[self._username] = self._text_orig

				bot.sendChatAction(self._chat_id, "typing")
				bot.sendMessage(self._chat_id, self._answer["text"], reply_to_message_id=self._msg_id, parse_mode=self._answer["parse"], disable_web_page_preview=self._answer["diswebview"])
				print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\" and turned \033[30;41mOFF\033[0m."%(self._now, self._text_log, self._username, self._answer["text"]))
				print("--------------------------------------------")
			else:
				self._answer["text"] = "Sorry, only the admin user can switch the bot to OFF."

		elif self._text == "/switch" and not switch:
			switch = True
			self._answer["text"] = "<strong>Status:</strong> Turned <em>ON</em>."
			self._answer["parse"] = "HTML"
			redo_dict[self._username] = self._text_orig

			bot.sendChatAction(self._chat_id, "typing")
			bot.sendMessage(self._chat_id, self._answer["text"], reply_to_message_id=self._msg_id, parse_mode=self._answer["parse"], disable_web_page_preview=self._answer["diswebview"])
			print("\033[33m>>>\033[0m %s\n\033[33mBot\033[0m: Got text \"\033[32m%s\033[0m\" from @\033[34m%s\033[0m and answered with \"\033[32m%s\033[0m\" and turned \033[30;46mON\033[0m."%(self._now, self._text_log, self._username, self._answer["text"]))
			print("--------------------------------------------")
			self._answer["text"] = None	# Or it will answer twice.


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
				self._answer["text"]s = ''
				for key in rule_dict:
					if key in self._text_orig.lower():
						if not rule_dict[key] in self._answer["text"]s:
							self._answer["text"]s += rule_dict[key] + '\n'
							self._answer["text"] = self._answer["text"]s.rstrip('\n')
				#elif random.random() <= 0.33:
					#self._answer["sticker"] = random.choice(list(resource.sticker_dict.keys()))
					#self._answer["text"] = resource.sticker_dict[self._answer["sticker"]]

	def on_sticker(self, msg):
		self._answer["sticker"]_id = msg["sticker"]["file_id"]
		self._answer["sticker"]_emoji = msg["sticker"]["emoji"]
		#print("\"%s\": \'%s\',"%(self._answer["sticker"]_id, self._answer["sticker"]_emoji))
		if (self._answer["sticker"]_id, self._answer["sticker"]_emoji) in resource.red_sticker_dict.items():
			self._answer["text"] = random.choice(["红脸的关公战长沙！", "红脸哥～我是你的超级粉丝～", "红脸哥我要给你生一车猴子🐒！"])
		#else:
			#print("\"%s\": \'%s\',"%(self._answer["sticker"]_id, self._answer["sticker"]_emoji))

	def on_photo(self, msg):
		if self._chat_type == "private":
			if self._username == ADMIN:
				self._answer["download"] = msg["photo"][-1]["file_id"]
				self._document = "Image/IMG_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".jpg"
				self._answer["text"] = "Got photo \"<em>%s</em>\"."%(self._document)
				self._answer["parse"] = "HTML"
			else:
				self._answer["refuse"] = True
				self._answer["text"] = "Sorry, only the admin user can save a photo on the bot."

	def on_document(self, msg):
		if self._chat_type == "private":
			if self._username == ADMIN:
				self._answer["download"] = msg["document"]["file_id"]
				self._document = "File/" + msg["document"]["file_name"]
				self._answer["text"] = "Got document \"<em>%s</em>\"."%(self._document)
				self._answer["parse"] = "HTML"
			else:
				self._answer["refuse"] = True
				self._answer["text"] = "Sorry, only the admin user can save a document on the bot."

    def handle(self, msg):
        self._answer = {
            "text": None,
            "upload": None,
            "download": None,
            "sticker": None,
            "parse": None,
            "diswebview": None,
            "refuse": False
        }
