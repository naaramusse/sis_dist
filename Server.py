import socket
import threading
import sys
import queue

COMMANDS = {'1': ['Exibe este menu'],
            '2': ['Lista dos clientes conectados'],
            '3': ['Cria um grupo: informe o nome e clientes conectados, (Formato: 3 grupo_nomeDoGrupo cliente1 cliente2)'],
            '4': ['Lista de grupos online'],
            '5': ['Entrar em um grupo - Formato: 5 grupo_nomeDoGrupo'],
            '6': ['Sair do grupo - Formato: 6 grupo_nomeDoGrupo '],
            '7': ['Apagar o grupo Formato: 7 grupo_nomeDoGrupo '],
            'sair': ['Desconectar do sistema '],
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
                print(connection)
                # connection.setblocking(False)
                self.get_client(connection)

            except:
                pass
            finally:
                self.sock.setblocking(False)

    def get_client(self, con):
        con.send('Informe seu nome:'.encode('utf-8'))
        nickname = con.recv(1024).decode('utf-8')
        self.clients[nickname] = con
        self.print_menu()
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
                self.commands(client, data)
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
                if command[1:]:
                    self.create_group(command[1:])
                    client.send('Grupo criado com sucesso\n'.encode('utf-8'))
            except:
                client.send(
                    'De um nome para o grupo(Formato:  grupo_nomeDoGrupo) e informe os clientes\n'.encode('utf-8'))
                return

        elif command[0] == '4':
            msg = self.list_groups()
            client.send(msg.encode('utf-8'))

        elif command[0] == '5':
            msg= self.subscribe(command[1], client)
            client.send(msg.encode('utf-8'))

        elif command[0] == '6':
            msg= self.unsubscribe(command[1], client)
            client.send(msg.encode('utf-8'))

        elif command[0] == '7':
            msg= self.del_group(command[1])
            client.send(msg.encode('utf-8'))
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
                    # msg = msg.split()
                    self.msg_to_group(receiver, sender, msg[2:])
                else:
                    self.msg_client(msg[2:], sender, receiver)
                self.queue.task_done()

    def msg_client(self, msg, sender, receiver):
        con = self.clients[receiver]
        data = ' '
        try:
            self.sock.setblocking(True)
            if msg != receiver and sender != receiver:
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

    def list_groups(self):

        results = ''
        resp = ''
        if len(self.group) != 0:
            for g in self.group:
                results += g['label'] + " "

                for key in list(g.keys()):
                    if key != 'label':
                        resp += key + " "
                results += resp + '\n'
        else:
            results = 'Nao ha grupos'

        return results

    def create_group(self, group):
        list_clients = {'label': group[0]}

        for i, con in self.clients.items():
            for nick in group:
                if i == nick:
                    list_clients[nick] = con

        self.group.append(list_clients)
        print('grupo criado')
        for i in self.group:
            print(i)

    def msg_to_group(self, label, client, msg):
        group = {}
        for a in self.group:
            if a['label'] == label:
                group = a.copy()

        print('msg para')
        print(group)
        data = ''

        for nick, con in group.items():
            if msg:
                try:
                    #self.sock.setblocking(True)
                    print('msg para grupo enviada')
                    # Garante que o cliente não envie a msg para si mesmo
                    data = client + ' diz ' + data.join(msg)
                    con.send(data.encode())
                except:
                    self.sock.setblocking(False)
                    pass

                finally:
                    self.sock.setblocking(False)

    def subscribe(self, label, client):
        nick = ''
        for i, con in self.clients.items():
            if con == client:
                nick = i
        for a in self.group:
            if a['label'] == label:
                a[nick] = client
        return ('Cadastrado com sucesso')

    def unsubscribe(self, label, client):
        nick = ''
        for i, con in self.clients.items():
            if con == client:
                nick = i
        for a in self.group:
            if a['label'] == label:
                del a[nick]
        return 'Descadastrado com sucesso'

    def del_group(self, label):

        for a in self.group:
            if a['label'] == label:
                self.group.remove(a)

        return 'Grupo apagado'


if __name__ == "__main__":
    s = Server()
