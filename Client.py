import socket
import threading
import sys
import queue


class Client:

    def __init__(self, host='localhost', port=4000):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.queue = queue.Queue()

        self.id = self.sock.getsockname()[1]
        msgrecv = threading.Thread(target=self.msg_recv)

        msgrecv.daemon = True
        msgrecv.start()

        self.run()

    def run(self):
        while True:
            msg = input()
            if msg != 'sair':
                self.queue.put(msg)
            else:
                self.sock.close()
                sys.exit()

            if not self.queue.empty():
                data = self.queue.get()
                self.send_msg(data)
                self.queue.task_done()

    def msg_recv(self):
        while True:
            try:
                msg = self.sock.recv(4096).decode()
                print('-----')
                print(msg)
            except:
                self.sock.close()

    def send_msg(self, msg):
        try:
            self.sock.send(msg.encode())
        except:
            self.sock.close()

c = Client()
