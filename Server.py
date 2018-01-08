import socket
import threading
import sys
import queue

COMMANDS = {'1': ['Exibe este menu'],
            '2': ['Lista dos clientes conectados'],
            '3': ['Cria um grupo: informe o nome e clientes conectados, (Formato:  grupo_nomeDoGrupo)'],
            'sair': ['Interrompe a conexao com o cliente '],
            'obs.': ['Para enviar msg para um grupo escreva o nome dele e em seguida a msg']
            }


class Server:

    def __init__(self, host="localhost", port=4000):
        self.group = []
        self.clients = {}
        self.address = []
        self.queue = queue.Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)
        self.lock = threading.RLock()

        accept = threading.Thread(target=self.accept_connection)
        send = threading.Thread(target=self.send_msg, daemon=True)

        accept.daemon = True
        accept.start()
        send.start()

        self.accept_connection()

    def accept_connection(self):
        while True:
            try:
                self.sock.setblocking(True)

                connection, address = self.sock.accept()
                print(connection    )
                #connection.setblocking(False)
                self.get_client(connection)

            except:
                pass
            finally:
                self.sock.setblocking(False)

    def get_client(self, con):
        con.send('Informe seu nome:'.encode('utf-8'))
        nickname = con.recv(1024).decode('utf-8')
        self.clients[nickname] = con
        self.receive_msg(con)

    def receive_msg(self, client):
        while True:
            try:
                self.sock.setblocking(True)
                msg = client.recv(4026).decode('utf-8')
                self.handle_data(client, msg)
            except:
                break
            finally:
                self.sock.setblocking(False)

    def handle_data(self, client, data):
        nick = ''
        for i, con in self.clients.items():
            if con == client:
                nick = i
        if data:
            msg = data.split()
            if msg[0].isdigit():
                self.commands(client, msg[0])
            else:
                self.queue.put((msg[1], nick, msg))

    def commands(self, client, msg):

        command = msg.split()

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
                client.send(
                    'De um nome para o grupo(Formato:  grupo_nomeDoGrupo) e informe os clientes\n'.encode('utf-8'))
                return
        else:
            self.send_msg()

    @staticmethod
    def print_menu():
        menu = ''
        for i, v in list(COMMANDS.items()):
            menu += "{0}:\t{1}".format(i, v[0]) + '\n'
        return menu

    def send_msg(self):
        while True:
            if not self.queue.empty():
                receiver, sender, msg = self.queue.get()
                print('send')
                print(msg)
                if receiver.startswith('grupo'):
                    msg = msg.split()
                    self.msg_to_group(msg[0], sender, msg[1:])
                else:
                    self.msg_client(msg[2:], sender, receiver)
                self.queue.task_done()

    def msg_client(self, msg, sender, receiver):
        con = self.clients[receiver]
        data = ' '
        try:
            self.sock.setblocking(True)
            if msg != receiver and sender != receiver :
                data = sender + ' diz ' + data.join(msg)
                con.send(data.encode())
        except:
            self.sock.setblocking(False)
            pass

        finally:
            self.sock.setblocking(False)

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

        for nick, con in self.clients.items():
            for i in range(len(group)):
                try:
                    if client != group[1] and nick == group[1]:
                        # Garante que o cliente não envie a msg para si mesmo
                        con.send(msg)
                except:
                    pass


if __name__ == "__main__":
    s = Server()
