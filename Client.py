import socket
import threading
import sys
import pickle


class Client:

    def __init__(self, host='localhost', port=4000):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))

        print('my Id')
        print(self.sock.getsockname()[1])

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
            try:
                msg = self.sock.recv(4096).decode('utf-8')
                print('-----')
                #   if int(pickle.loads(data).split()[0]) == int(self.id):

                print(msg)
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(msg.encode('utf-8'))


c = Client()
