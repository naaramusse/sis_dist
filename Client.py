import socket
import threading
import sys
import queue


class Client:

    def __init__(self, host='localhost', port=4000):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.queue = queue.Queue()
        self.lock = threading.RLock()

        #print('my Id')
        #print(self.sock.getsockname()[1])

        self.id = self.sock.getsockname()[1]
        msgrecv = threading.Thread(target=self.msg_recv)

        msgrecv.daemon = True
        msgrecv.start()

        while True:
            msg = input()
            if msg != 'sair':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()

    def msg_recv(self):
        while True:
            with self.lock:
                try:
                    msg = self.sock.recv(4096).decode('utf-8')
                    print('-----')
                    #   if int(pickle.loads(data).split()[0]) == int(self.id):

                    print(msg)
                except:
                    self.sock.close()

    def send_msg(self, msg):
        with self.lock:
            try:
                self.sock.send(msg)
            except:
                self.sock.close()


c = Client()
