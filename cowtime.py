#!/usr/bin/python

# Imports
import os, re, sys, argparse, time
import fcntl, termios, struct
from subprocess import check_output
from subprocess import call

# The brains
class CowTime:
	light = False
	def __init__(self, interface, delay, light, proc):
		self.interface = interface
		self.delay = delay
		self.light = light
                self.proc = proc
		self.width = self.terminal_size() - 8 

		while(True):
			self.loadProcTime()
			self.cowSayWhat()
			time.sleep(self.delay)

	def terminal_size(self):
		h, w, hp, wp = struct.unpack('HHHH',
			fcntl.ioctl(0, termios.TIOCGWINSZ,
			struct.pack('HHHH', 0, 0, 0, 0)))
		return w

	def loadProcTime(self):
		# Get the response from netstat and break it up by row
                upTime = check_output(["ps", "-p", self.proc, "-o", "etime="])
                self.upTime = upTime.split('\n')

		self.say = "Uptime " + self.upTime[0]

	def printCenter(self, txt):
		print(str.center(txt, self.width))

	def cowSayWhat(self):

		if self.light == False:
			os.system('clear')
			call(["figlet", "-w", str(self.width), "-c", "cowtime"])
			self.printCenter("____________________________________")
			self.printCenter("< " + self.say + " >")
			self.printCenter("------------------------------------")
			self.printCenter("    \   ^__^        ")
			self.printCenter("     \  (oo)\_______")
			self.printCenter("            (__)\       )\/\\")
			self.printCenter("                ||----w |")
			self.printCenter("                ||     ||")
		else:
			print(self.say)

# The main class to handle threads, and inputs
class Main:
	# Setup some default varialbes
	interface = "en1"
	delay = 1.0
	version = "0.0.1"
	light = False

	def __init__(self, argv):
		parser = argparse.ArgumentParser(prog='CowTime')
		parser.add_argument("-l", "--light", help="The low calorie version", action='store_true')
		parser.add_argument("-i", "--interface", type=str, help="Change the network interface (defaults to en1)")
		parser.add_argument("-d", "--delay", type=float, help="Change the frequency we check your usage data (defaults to 30 seconds)")
		parser.add_argument("-v", '--version', action='version', version='%(prog)s 0.0.1')
		parser.add_argument("-p", "--process", type=str, help="Process you are monitoring")

		args = parser.parse_args()
		if args.delay:
			self.delay = float(args.delay)
		if args.interface:
			self.interface = args.interface
		if args.light:
			self.light = True
		if args.process:
			self.proc = args.process

		if self.light == False:
			print 'CowTime' + self.version
			print 'https://github.com/obihann/cowtime/'
			print 'This tool is protected by the GNU General Public License v2.'
			print 'Copyright Jeffrey Hann 2015'
			print '------------------------------------------------------------'

		try:
			self.net = CowTime(self.interface, self.delay, self.light, self.proc)
		except KeyboardInterrupt:
			sys.exit()

if __name__ == "__main__":
	main = Main(sys.argv[1:])
