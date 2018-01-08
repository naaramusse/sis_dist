import socket
import threading
import sys
import queue

COMMANDS = {'1': ['Exibe este menu'],
            '2': ['Lista dos clientes conectados'],
<<<<<<< HEAD
            '3': ['Cria um grupo: informe o nome e clientes conectados, (Formato:  grupo_nomeDoGrupo)'],
            'sair': ['Interrompe a conexao com o cliente '],
            'obs.': ['Para enviar msg para um grupo escreva o nome dele e em seguida a msg']
=======
            '3': ['Cria um grupo: informe o nome e clientes conectados'],
            '4': ['Informe o grupo para enviar msg'],
<<<<<<< HEAD
            'sair': ['Interrompe a conexao com o cliente '],
=======
            '0': ['Interrompe a conexao com o cliente '],
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d
            }


class Server:

    def __init__(self, host="localhost", port=4000):
        self.group = []
<<<<<<< HEAD
        self.clients = {}
=======
<<<<<<< HEAD
        self.clients = {}
=======
        self.clients = []
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d
        self.address = []
        self.queue = queue.Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)
        self.lock = threading.RLock()

        accept = threading.Thread(target=self.accept_connection)
<<<<<<< HEAD
=======
<<<<<<< HEAD
        # process = threading.Thread(target=self.process_connection)
=======
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d

        accept.daemon = True
        accept.start()

<<<<<<< HEAD
        self.accept_connection()

    def accept_connection(self):

        while True:
            try:
                self.lock.acquire()
                connection, address = self.sock.accept()
                connection.setblocking(False)
                self.get_client(connection)

            except:
                pass
            finally:
                self.lock.release()

    def get_client(self, con):
        con.send('Informe seu nome:'.encode('utf-8'))
        nickname = con.recv(1024).decode('utf-8')
        self.clients[nickname] = con

        self.receive_msg(con)

    def receive_msg(self, client):

        while True:
            try:
                self.lock.acquire()
                msg = client.recv(4026).decode('utf-8')
                self.handle_data(client, msg)
            except:
                break
            finally:
                self.lock.release()
=======
<<<<<<< HEAD
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

=======
<<<<<<< HEAD
        process.daemon = True
        process.start()
        #self.accept_connection()

    def commands(self, msg, client):
        command = msg.split()

        if command[0] == '0':
            self.sock.close()
            sys.exit()

=======
    def commands(self, msg, client):
        command = msg.split()

        if command[0] == '0':
            self.sock.close()
            sys.exit()

>>>>>>> 8a43430b72b1ba791b6213800a911c1316dfafc9
        elif command[0] == '1':
            msg = self.print_menu()
            self.msg_client(msg, [], client)

        elif command[0] == '2':
            msg = self.list_connections()
            self.msg_client(msg, [], client)

>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
        elif command[0] == '3':
            try:
                self.create_group(command[1], command[2:])
            except:
<<<<<<< HEAD
                client.send('De um nome para o grupo e informe os clientes\n'.encode('utf-8'))
=======
                msg = 'De um nome para o grupo e informe os clientes\n'
                self.msg_client(msg, [], client)
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
                return

        elif command[0] == '4':
            self.msg_to_group(command[1], [], command[2:])

        else:
<<<<<<< HEAD
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
=======
            pass

    def print_menu(self):
        menu = ''

        for cmd, v in COMMANDS.items():
            menu += "{0}:\t{1}".format(cmd, v[0])

>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
        return menu

    def msg_client(self, msg, sender, receiver):
        con = self.clients.get(receiver)
<<<<<<< HEAD
        try:
            if msg and sender != receiver:
                msg = sender + " " + msg
                con.send(msg)
        except:
            pass
=======
<<<<<<< HEAD
=======

>>>>>>> 8a43430b72b1ba791b6213800a911c1316dfafc9
        try:
            data = sender.recv(1024)
            if data and sender != receiver:
                con.send(msg)
        except:
            self.clients.remove(sender)
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d

    def handle_data(self, client, data):

        if data:
            msg = data.decode('utf-8')
            msg = msg.split()

            if msg[0].isdigit():
                self.commands(client, msg[0])
            else:
                data = msg.encode('utf-8')
                self.queue.put((msg[1], client, data))

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
<<<<<<< HEAD
                self.create_group(command[1], command[2:])
=======
                connection, address = self.sock.accept()
                connection.setblocking(1)
<<<<<<< HEAD
                self.get_client(connection)
=======
                self.clients.append(connection)
                self.address.append(address)
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd

>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d
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

<<<<<<< HEAD
    def send_msg(self):

        while True:
            if not self.queue.empty():
                receiver, sender, msg = self.queue.get()
                if receiver.startswith('grupo'):
                    msg = msg.split()
                    self.msg_to_group(msg[0], sender, msg[1:])
                else:
                    self.msg_client(msg, sender, receiver)
                self.queue.task_done()

    def msg_client(self, msg, sender, receiver):

        con = self.clients.get(receiver)
        try:
            self.lock.acquire()
            if msg and sender != receiver:
                msg = sender + " " + msg
                con.send(msg)
        except:
            pass

        finally:
            self.lock.release()
=======
<<<<<<< HEAD
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
=======
<<<<<<< HEAD
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
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d

=======
>>>>>>> 8a43430b72b1ba791b6213800a911c1316dfafc9
    def list_connections(self):
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d

        results = 'Lista de clientes conectados no momento:\n'

        for client, con in list(self.clients.items()):
            results += "{0}:\t{1}".format(client, str(con.getpeername())) + '   ' + "\n"

<<<<<<< HEAD
=======
=======
        results = ''
        for i, connection in enumerate(self.clients):
            # print(connection)
            results += str(i) + '   ' + str(connection.getsockname()[1]) + '   ' + str(
                connection.getpeername()) + '\n'
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d
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

<<<<<<< HEAD
        for nick, con in self.clients.items():
            for i in range(len(group)):
                try:
                    if client != group[1] and nick == group[1]:
                        # Garante que o cliente não envie a msg para si mesmo
                        con.send(msg)
                except:
                    pass
=======
        for i, c in self.clients:
            try:
                if str(c.getsockname()[1]) != str(client.getsockname()[1]) and str(c.getpeername()) == group[i + 1]:
                    # Garante que o cliente não envie a msg para si mesmo
                    c.send(msg)
            except:
<<<<<<< HEAD
                pass
=======
                self.clients.remove(c)
>>>>>>> 4afd54728609af2711589e57f8596d838baa74dd
>>>>>>> d99000e4551091b9e2d1491da2e6b8550c978d2d


if __name__ == "__main__":
    s = Server()
