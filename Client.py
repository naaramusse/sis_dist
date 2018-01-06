import socket
import threading
import sys
import pickle


class Client:

    def __init__(self, host='127.0.0.1', port=4000):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))

        print('my Id')
        print(self.sock.getsockname()[1])

        self.id = self.sock.getsockname()[1]
        msgrecv = threading.Thread(target=self.msg_recv)

        msgrecv.daemon = True
        msgrecv.start()

        while True:
            msg = input('->')
            if msg != 'sair':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                print('-----')
             #   if int(pickle.loads(data).split()[0]) == int(self.id):
                msg = pickle.loads(data)
                print(msg)
            except:
                pass

    def send_msg(self, msg):

        #if msg.slipts()[0].isdigit():
         #   c.sendto(msg, self.id)
        #else:
        self.sock.send(pickle.dumps(msg))


c = Client()
