#!/usr/bin/env python3
#-*- coding: utf-8 -*-

### Filename: ipcn.py
## Created by 请叫我喵 | S-X-ShaX
# sxshax@gmail.com, http://sxshax.xyz/

from urllib.request import urlopen
from html.parser import HTMLParser

class IPCNParser(HTMLParser):
	def __init__(self):
		super(IPCNParser, self).__init__()
		self._okay = False
		self._code = 0
		self.result = None

	def handle_starttag(self, tag, attrs):
		if tag == "div" and attrs == [('id', 'result')]:
			self._okay = True
		if self._okay and tag == "code":
			self._code += 1

	def handle_endtag(self, tag):
		if self._okay and tag == "code":
			self._code += 1
		if tag == "div":
			self._okay = False

	def handle_data(self, data):
		if self._okay and self._code == 1:
			self.result = data

iparser = IPCNParser()

def get_ip():
	with urlopen("http://ip.cn/") as url_open:
		ipcn = url_open.read().decode("utf-8")
	iparser.feed(ipcn)
	return iparser.result

if __name__ == "__main__":
	print(get_ip())
