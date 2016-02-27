"""
Created by Kyle Carretto with the wonderful help of the Impacket Framwork:
                                        https://github.com/CoreSecurity/impacket/tree/master/impacket
"""
import socket
import os
import sys
import select
import time
import threading

from impacket import ImpactDecoder
from impacket import ImpactPacket
from Queue import Queue

def getlocalip():
	"""
		Thanks to Alexander @ stackoverflow for a quick, portable way to get an IP.
	"""
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

localhost = getlocalip()

def socket_init():
    """
    Returns an initialized ICMP raw socket
    :return: Socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind((localhost, 0))

    # Include IP headers
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packages
    if os.name == 'nt':
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    return s


def send_icmp(src, dst, data):
    """
    Build an ICMP Packet with specified data, and send it
    """
    ip = ImpactPacket.IP()
    ip.set_ip_src(src)
    ip.set_ip_dst(dst)

    icmp = ImpactPacket.ICMP()
    icmp.set_icmp_type(icmp.ICMP_ECHOREPLY)

    icmp.contains(ImpactPacket.Data(data))
    ip.contains(icmp)
    icmp.set_icmp_id(1)
    icmp.set_icmp_cksum(0)
    icmp.auto_checksum = 1

    s = socket_init()

    s.sendto(ip.get_packet(), (dst, 0))
    s.close()

def snif_icmp():
    """
        returns the next available ICMP Data
    :return: data
    """
    s = socket_init()
    if s in select.select([ s ], [], [])[0]:
        data = s.recvfrom(65535)[0]

        decoder = ImpactDecoder.IPDecoder()
        rip = decoder.decode(data)
        ricmp = rip.child()
        data = ricmp.get_data_as_string()
    s.close()
    return data


class Listener (threading.Thread):
    def __init__(self, q):
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.q.put(snif_icmp())
