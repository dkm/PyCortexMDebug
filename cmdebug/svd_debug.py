import traceback
import sys


## For the exception trace code
#######################################################################################
#
# gef is distributed under the MIT License (MIT)
# Copyright (c) 2013-2018 crazy rabbidz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
PYTHON_MAJOR = sys.version_info[0]

if PYTHON_MAJOR == 2:
	from HTMLParser import HTMLParser
	from cStringIO import StringIO
	from urllib import urlopen
	import ConfigParser as configparser
	import xmlrpclib

	# Compat Py2/3 hacks
	range = xrange
	FileNotFoundError = IOError
	ConnectionRefusedError = socket.error

	left_arrow = "<-"
	right_arrow = "->"
	down_arrow = "\\->"
	horizontal_line = "-"
	vertical_line = "|"
	cross = "x"
	tick = "v"
	gef_prompt = "gef> "
	gef_prompt_on = "\001\033[1;32m\002{0:s}\001\033[0m\002".format(gef_prompt)
	gef_prompt_off = "\001\033[1;31m\002{0:s}\001\033[0m\002".format(gef_prompt)

elif PYTHON_MAJOR == 3:
	from html.parser import HTMLParser
	from io import StringIO
	from urllib.request import urlopen
	import configparser
	import xmlrpc.client as xmlrpclib

	# Compat Py2/3 hack
	long = int
	unicode = str

	left_arrow = " \u2190 "
	right_arrow = " \u2192 "
	down_arrow = "\u21b3"
	horizontal_line = "\u2500"
	vertical_line = "\u2502"
	cross = "\u2718 "
	tick = "\u2713 "
	gef_prompt = "gef\u27a4  "
	gef_prompt_on = "\001\033[1;32m\002{0:s}\001\033[0m\002".format(gef_prompt)
	gef_prompt_off = "\001\033[1;31m\002{0:s}\001\033[0m\002".format(gef_prompt)

else:
	raise Exception("WTF is this Python version??")


class Color:
	"""Colorify class."""
	colors = {
		"normal"	 : "\033[0m",
		"gray"	   : "\033[1;30m",
		"red"	    : "\033[31m",
		"green"	  : "\033[32m",
		"yellow"	 : "\033[33m",
		"blue"	   : "\033[34m",
		"pink"	   : "\033[35m",
		"bold"	   : "\033[1m",
		"underline"      : "\033[4m",
		"underline_off"  : "\033[24m",
		"highlight"      : "\033[3m",
		"highlight_off"  : "\033[23m",
		"blink"	  : "\033[5m",
		"blink_off"      : "\033[25m",
	}

	@staticmethod
	def redify(msg):	   return Color.colorify(msg, attrs="red")
	@staticmethod
	def greenify(msg):	 return Color.colorify(msg, attrs="green")
	@staticmethod
	def blueify(msg):	  return Color.colorify(msg, attrs="blue")
	@staticmethod
	def yellowify(msg):	return Color.colorify(msg, attrs="yellow")
	@staticmethod
	def grayify(msg):	  return Color.colorify(msg, attrs="gray")
	@staticmethod
	def pinkify(msg):	  return Color.colorify(msg, attrs="pink")
	@staticmethod
	def boldify(msg):	  return Color.colorify(msg, attrs="bold")
	@staticmethod
	def underlinify(msg):  return Color.colorify(msg, attrs="underline")
	@staticmethod
	def highlightify(msg): return Color.colorify(msg, attrs="highlight")
	@staticmethod
	def blinkify(msg):	 return Color.colorify(msg, attrs="blink")

	@staticmethod
	def colorify(text, attrs):
		"""Color a text following the given attributes."""
		# if get_gef_setting("gef.disable_color")==True: return text
		colors = Color.colors
		msg = [colors[attr] for attr in attrs.split() if attr in colors]
		msg.append(text)
		if colors["highlight"] in msg :   msg.append(colors["highlight_off"])
		if colors["underline"] in msg :   msg.append(colors["underline_off"])
		if colors["blink"] in msg :       msg.append(colors["blink_off"])
		msg.append(colors["normal"])
		return "".join(msg)

def show_last_exception():
	"""Display the last Python exception."""
	print("")
	exc_type, exc_value, exc_traceback = sys.exc_info()
	print(" Exception raised ")
	print("{}: {}".format(Color.colorify(exc_type.__name__, attrs="bold underline red"), exc_value))
	print(" Detailed stacktrace ")
	for fs in traceback.extract_tb(exc_traceback)[::-1]:
		if PYTHON_MAJOR==2:
		    filename, lineno, method, code = fs
		else:
		    filename, lineno, method, code = fs.filename, fs.lineno, fs.name, fs.line

		print("""{} File "{}", line {:d}, in {}()""".format(down_arrow, Color.yellowify(filename),
								    lineno, Color.greenify(method)))
		print("   {}    {}".format(right_arrow, code))

	# print(" Last 10 GDB commands ".center(80, horizontal_line))
	# gdb.execute("show commands")
	# print(" Runtime environment ".center(80, horizontal_line))
	# print("* GDB: {}".format(gdb.VERSION))
	# print("* Python: {:d}.{:d}.{:d} - {:s}".format(sys.version_info.major, sys.version_info.minor,
	# 						sys.version_info.micro, sys.version_info.releaselevel))
	# print("* OS: {:s} - {:s} ({:s}) on {:s}".format(platform.system(), platform.release(),
	# 						 platform.architecture()[0],
	# 						 " ".join(platform.dist())))
	print(horizontal_line*80)
	print("")
	return
