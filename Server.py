import socket
import threading
import sys

COMMANDS = {'Menu': ['Exibe este menu'],
            'lista': ['Lista dos clientes conectados'],
            'broadcast': ['envia msg para todos clients conectados'],
            'sair': ['Interrompe a connection com o cliente selecionado'],
            }


class Server():

    def __init__(self, host="localhost", port=4000):

        self.clients = []
        self.address = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        accept = threading.Thread(target=self.accept_connection)
        process = threading.Thread(target=self.process_connection)

        accept.daemon = True
        accept.start()

        process.daemon = True
        process.start()

        while True:
            msg = input('->')
            if msg == 'sair':
                self.sock.close()
                sys.exit()
            elif msg == 'menu':
                self.print_menu()
            elif msg == 'lista':
                self.list_connections()
           # elif msg == 'broadcast':
            #    self.msg_clients()
            else:
                pass

    def print_menu(self):
        for cmd, v in COMMANDS.items():
            print("{0}:\t{1}".format(cmd, v[0]))
        return

    def msg_clients(self, msg, client):
        for c in self.clients:
            try:
                if c != client: #Garante que o cliente não envie a msg para si mesmo
                    c.send(msg)
            except:
                self.clients.remove(c)

    def accept_connection(self):

        while True:
            try:
                connection, address = self.sock.accept()
                connection.setblocking(1)
                self.clients.append(connection)
                self.address.append(address)
            except:
                pass

    def process_connection(self):

        while True:
            if len(self.clients) > 0:
                for c in self.clients:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_clients(data, c)
                    except:
                        pass

    def list_connections(self):
        results = ''
        for i, connection in enumerate(self.clients):
            print(connection)
            print('---')
            results += str(i) + '   ' + str(connection.getsockname()[1]) + '   ' + str(
                connection.getpeername()) + '\n'
        print('----- clients -----' + '\n' + results)


s = Server()
