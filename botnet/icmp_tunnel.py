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

localhost = socket.gethostbyname(socket.gethostname())
blocking = True


def socket_init():
    """
    Returns an initialized ICMP raw socket
    :return: Socket
    """
    # the public network interface
    HOST = socket.gethostbyname(socket.gethostname())
    print(HOST)
    # create a raw socket and bind it to the public interface
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.bind((HOST, 0))

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
    icmp.set_icmp_type(icmp.ICMP_ECHO)

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
            self.q.add(snif_icmp())


def send_file(dst, lines, buffersize=65500, delay=0):
    """
    Note any \n will result in a new line at the other end

    :param dst: Destination
    :param lines: lines of the file to send
    :param buffersize: Size of the buffer in which to send information
    :param delay: Time to wait between sends
    :return:
    """

    send_icmp(localhost, dst, "FILE-TRANSFER-START")
    strsum = ""
    for s in lines:
        if sys.getsizeof(strsum) + sys.getsizeof(s) + sys.getsizeof("\n") < buffersize:
            strsum += s + "\n"
        else:
            send_icmp(localhost, dst, strsum)
            strsum = ""
            time.sleep(delay)

    if len(strsum) > 0:
            send_icmp(localhost, dst, strsum)

    send_icmp(localhost, dst, "FILE-TRANSFER-END")
    Blocking = False

class FileReciever (threading.Thread):
    def __init__(self, buf):
        self.buf = buf
        threading.Thread.__init__(self)

    def run(self):
        filequeue = Queue.Queue()
        while snif_icmp() != "FILE-TRANSFER-END":
            filequeue.add(snif_icmp())
        self.buf = []
        while not filequeue.empty():
            line = ""
            lastch = ""
            for ch in filequeue.get():
                if lastch == "\\":
                    if ch == "n":
                        self.buf.append(line)
                        line = ""
                elif ch == "\\":
                    lastch = "\\"
                else:
                    line += ch
        print("Output File: "+self.buf)
