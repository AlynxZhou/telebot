# TeleBot

A telegram bot program\.

## Usage:

First clone it via git.

````
$ git clone git@github.com:S-X-ShaX/telebot.git
````

You need to install python3, pip3 and use pip to install telepot, if you forget to install telepot, the program will install by itself\. Such as:

````bash
$ sudo apt-get install python3 python3-pip
$ sudo pip3 install telepot
````

Now you have to **sign up a new bot** from [the BotFather](https://telegram.me/BotFather), then put your token and your username into a config file:

````bash
$ cd /Where/you/cloned/TeleBot/
$ cp example_bot.json YOURBOTNAME.json
$ ${EDITOR} YOURBOTNAME.json
````

After `"token": ` was your bot token, after `"admin": ` was your username \(nikename, no '@'\!\), and if you want, [get Tuling Chat Api Key](http://tuling123.com/), add it after `"tuling_api_key": `\. Don't forget json format\.

Finally run:

````bash
$ python3 ./bot.py YOURBOTNAME.json
````

Do not kill it\. You could use [GNU Screen](https://www.gnu.org/software/screen/)\.

I will complete it gradually\. Thanks\.
