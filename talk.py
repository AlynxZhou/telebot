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
parser = argparse.ArgumentParser(description='A telegram bot program.')
parser.add_argument('-t','--token',help='Get the file that stored the bot token.',action='store')
#parser.add_argument('-a','--admin',help='Get the admin user\' name',action='store')
args = parser.parse_args()

token_file = args.token
if token_file == None:
	print('\nWARNING:It seems that you haven\'t choose a token file.')
	print('You are expected to make a tokenfile like YOURBOTNAME.token,which contains you bot token from the BotFather,and then run the program again by \'$ python3 ./bot.py --token YOURBOTNAME.token --admin ADMINUSER\'.')
	TOKEN = input('However,you can also type your token here and then press [ENTER] to make it continue: ')
#	print('')
else:
	try:
		with open(token_file) as token_open:
			TOKEN = token_open.read().rstrip()
	except FileNotFoundError:
		print('ERROR:No avaliable \'%s\' was found.'%(token_file))
		exit()

#ADMIN = args.admin
#if ADMIN == None:
#	print('\nWARNING:It seems that you haven\'t choose an admin user.')
#	print('You are expected to choose an adminuser to use some advanced functions.')
#	print('The admin user is usually yourself,so you should find your username which maybe also called nickname in the Settings of Telegram,notice the \'@\' is not a part of your username.if you haven\'t set it,you should set a username,and run the program again by \'$ python3 ./bot.py --token YOURBOTNAME.token --admin ADMINUSER\'.')
#	ADMIN = input('However,you can also type your admin user name here and then press [ENTER] to make it continue: ')
#	print('')
def talk():
	try:
		with open('talk.txt') as greeting_open:
			talk_list = greeting_open.read().split('\n$')[0:-1]

	except FileNotFoundError:
		print('ERROR:No avaliable \'talk.txt\' was found.')
		exit()
	return talk_list
talk_list = talk()
class TalkBot(telepot.helper.ChatHandler):
	def __init__(self,seed_tuple,timeout):
		super(TalkBot,self).__init__(seed_tuple,timeout)
		self._count = 0

	def on_chat_message(self,msg):
		now = str(datetime.datetime.now())
		print('>>> %s'%(now))
		content_type,chat_type,chat_id = telepot.glance(msg)
		first_name = msg['from']['first_name']
		username = msg['from']['username']
		msg_id = msg['message_id']

## To judge if the content is a text and deal with it.
		if content_type == 'text':
			text = msg['text']

		self._count += 1

		self.sender.sendChatAction('typing')
		self.sender.sendMessage(talk_list[self._count],reply_to_message_id=msg_id)
		print('Bot:Got text \'%s\' from @%s and answered with \'%s\'.'%(text,username,talk_list[self._count]))
		print('--------------------------------------------')


### Now it start run.
print('Getting bot information...')

bot = telepot.DelegatorBot(
	TOKEN,
	[
		(
			per_from_id(),
			create_open(TalkBot,timeout=30)
		)
	,]
)


### Now it prints your bot information.
try:
	info = bot.getMe()
except KeyboardInterrupt:
    exit()
except:
	print('ERROR:Your token is invaild.')
	print('Please check what your token file \'%s\' contains.'%(token_file))
	print('It should only contain your token in one line,without anything else.')
	print('Or you may need to check your network and system time,you can\'t connect to the bot server if your time is wrong or your network is down,and your bot token canalso be considered invaild.')
	exit()

print('############################################')
print('#')
print('# tokenfile:%s'%(token_file))
print('# botid:%s'%(info['id']))
print('# username:%s'%(info['username']))
print('# firstname:%s'%(info['first_name']))
#print('# adminuser:%s'%(ADMIN))
print('#')
print('############################################')

print('Bot:I am listening...')
print('--------------------------------------------')

try:
    bot.message_loop(run_forever=True)
except KeyboardInterrupt:
    exit()
