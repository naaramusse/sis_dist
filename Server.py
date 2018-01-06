import socket
import threading
import sys

COMMANDS = {'1': ['Exibe este menu'],
            '2': ['Lista dos clientes conectados'],
            '3': ['Cria um grupo: informe o nome e clientes conectados'],
            '4': ['Informe o grupo para enviar msg'],
            '0': ['Interrompe a conexao com o cliente '],
            }


class Server():

    def __init__(self, host="localhost", port=4000):
        self.group = []
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
        #self.accept_connection()

    def commands(self, msg, client):
        command = msg.split()

        if command[0] == '0':
            self.sock.close()
            sys.exit()

        elif command[0] == '1':
            msg = self.print_menu()
            self.msg_client(msg, [], client)

        elif command[0] == '2':
            msg = self.list_connections()
            self.msg_client(msg, [], client)

        elif command[0] == '3':
            try:
                self.create_group(command[1], command[2:])
            except:
                msg = 'De um nome para o grupo e informe os clientes\n'
                self.msg_client(msg, [], client)
                return

        elif command[0] == '4':
            self.msg_to_group(command[1], [], command[2:])

        else:
            pass

    def print_menu(self):
        menu = ''

        for cmd, v in COMMANDS.items():
            menu += "{0}:\t{1}".format(cmd, v[0])

        return menu

    def msg_client(self, msg, sender, receiver):
        con = self.clients.get(receiver)
        try:
            data = sender.recv(1024)
            if data and sender != receiver:
                con.send(msg)
        except:
            self.clients.remove(sender)

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
                            self.commands(data, c)
                    except:
                        pass

    def list_connections(self):
        results = ''
        for i, connection in enumerate(self.clients):
            # print(connection)
            results += str(i) + '   ' + str(connection.getsockname()[1]) + '   ' + str(
                connection.getpeername()) + '\n'
        return results

    def create_group(self, label, group):
        group.append(label)
        self.group.append(group)
        for i in self.group:
            print(i)

    def msg_to_group(self, label, client, msg):

        condition = filter(lambda x: x[0] == label, self.group)
        group = list(condition)
        print(group)

        for i, c in self.clients:
            try:
                if str(c.getsockname()[1]) != str(client.getsockname()[1]) and str(c.getpeername()) == group[i + 1]:
                    # Garante que o cliente não envie a msg para si mesmo
                    c.send(msg)
            except:
                self.clients.remove(c)


if __name__ == "__main__":
    s = Server()
