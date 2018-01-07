import socket
import threading
import sys

COMMANDS = {'1': ['Exibe este menu'],
            '2': ['Lista dos clientes conectados'],
            '3': ['Cria um grupo: informe o nome e clientes conectados'],
            '4': ['Informe o grupo para enviar msg'],
            'sair': ['Interrompe a conexao com o cliente '],
            }


class Server:

    def __init__(self, host="localhost", port=4000):
        self.group = []
        self.clients = {}
        self.address = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        accept = threading.Thread(target=self.accept_connection)
        # process = threading.Thread(target=self.process_connection)

        accept.daemon = True
        accept.start()

        # process.daemon = True
        # process.start()
        self.accept_connection()

    def commands(self, client, msg):

        command = msg.split()
        receiver = ''

        if command[0] == 'sair':
            self.sock.close()
            sys.exit()

        elif command[0] == '1':
            msg = self.print_menu()
            client.send(msg.encode('utf-8'))

        elif command[0] == '2':
            msg = self.list_connections()
            client.send(msg.encode('utf-8'))

        elif command[0] == '3':
            try:
                self.create_group(command[1], command[2:])
            except:
                client.send('De um nome para o grupo e informe os clientes\n'.encode('utf-8'))
                return

        elif command[0] == '4':
            self.msg_to_group(command[1], [], command[2:])

        else:
            for n in self.clients:
                if command[0].startswith(n): #verifica se eh substring
                    receiver = command[0]
                break
            self.msg_client(msg, client, receiver)

    @staticmethod
    def print_menu():
        menu = ''
        for i, v in list(COMMANDS.items()):
            menu += "{0}:\t{1}".format(i, v[0]) + '\n'
        return menu

    def msg_client(self, msg, sender, receiver):
        con = self.clients.get(receiver)
        try:
            if msg and sender != receiver:
                msg = sender + " " + msg
                con.send(msg)
        except:
            pass

    def accept_connection(self):

        while True:
            try:
                connection, address = self.sock.accept()
                connection.setblocking(1)
                self.get_client(connection)

            except:
                pass

    def get_client(self, con):
        con.send('Informe seu nome:'.encode('utf-8'))
        nickname = con.recv(1024).decode('utf-8')
        self.clients[nickname] = con

        self.receive_msg(con)

    def receive_msg(self, client):

        while True:
            try:
                msg = client.recv(4026).decode('utf-8')
                self.commands(client, msg)
            except:
                break

    def list_connections(self):

        results = 'Lista de clientes conectados no momento:\n'

        for client, con in list(self.clients.items()):
            results += "{0}:\t{1}".format(client, str(con.getpeername())) + '   ' + "\n"

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
                pass


if __name__ == "__main__":
    s = Server()
