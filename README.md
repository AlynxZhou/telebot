# TeleBot
A telegram bot program.

## Usage:

````bash
$ python3 bot.py --token TOKEN_FILE --admin ADMIN_USER
````

ADMIN\_USER should be *your telegram username(nickname)*.

## You should install telepot via pip.

Such as:
````bash
$ sudo apt-get install python3-pip
$ sudo pip3 install telepot
````

Then after you *sign up a new bot* from the **BotFather**,put you token into a token file:

````bash
$ cd /Where/you/cloned/TeleBot/
$ echo "YOUR_TOKEN" > ANYNAME.token
````

Then run:

````bash
$ python3 bot.py --token ANYNAME.token --admin YOURUSERNAME
````

Do not kill it.You could use *GNU Screen*.

I will complete it gradually.Thanks.
