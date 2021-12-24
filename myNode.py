import socket
import errno
import sys

BUF_SZ = 10
Host_IP = '127.0.0.1'
Host_Port = int(sys.argv[1])


class Node(object):
    def __init__(self):
        self.host = Host_IP
        self.port = Host_Port

    def run(self):
            friendly_name = input("Username: ")

            node_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            node_sock.connect((self.host, self.port))
            node_sock.setblocking(False)

            username = friendly_name.encode('utf-8')
            header = f"{len(username):<{BUF_SZ}}".encode('utf-8')
            
            node_sock.send(header + username)
            
            while True:
                chat = input(f'{friendly_name}:  ')

                if chat:
                    chat = chat.encode('utf-8')
                    chat_header = f"{len(chat):<{BUF_SZ}}".encode('utf-8')
                    node_sock.send(chat_header + chat)

                try:
                    while True:
                        header = node_sock.recv(BUF_SZ)
                        if not len(header):
                            print('Connection closed by the server')
                            sys.exit()
                        USR_SZ = int(header.decode('utf-8').strip())
                        username = node_sock.recv(USR_SZ).decode('utf-8')

                        chat_header = node_sock.recv(BUF_SZ)

                        chat_length = int(chat_header.decode('utf-8').strip())
                        chat = node_sock.recv(chat_length).decode('utf-8')
                        print(f'{username}:  {chat}')
                except IOError as err:
                    if err.errno != errno.EAGAIN:
                        if err.errno != errno.EWOULDBLOCK:
                            print('Reading error: {}'.format(str(err)))
                            sys.exit()
                    continue
                except Exception as err:
                    print('Reading error: '.format(str(err)))
                    sys.exit()
