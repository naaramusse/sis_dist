import socket
import threading
import sys
import pickle


class Client:

<<<<<<< HEAD
    def __init__(self, host='localhost', port=4000):
=======
    def __init__(self, host='127.0.0.1', port=4000):
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd

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
<<<<<<< HEAD
                #   if int(pickle.loads(data).split()[0]) == int(self.id):

=======
             #   if int(pickle.loads(data).split()[0]) == int(self.id):
                msg = pickle.loads(data)
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
                print(msg)
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(msg.encode('utf-8'))


c = Client()
