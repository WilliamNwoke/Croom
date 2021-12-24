import socket
import select
import sys

BUF_SZ = 10
Host_IP = '127.0.0.1'
Host_Port = int(sys.argv[1])


class Server(object):
    def __init__(self):
        self.host = Host_IP
        self.port = Host_Port
        
    def chat_handler(self, node_sock):
        '''
            Function to receive chat from nodes
        '''
        try:
            chat_header = node_sock.recv(BUF_SZ)
            if not len(chat_header):
                return False
            chat_length = int(chat_header.decode('utf-8').strip())
            return {'header': chat_header, 'data': node_sock.recv(chat_length)}
        except:
            return False

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((Host_IP, Host_Port))
        server_socket.listen()
        sockets_list = [server_socket]
        nodes = {}

        print(f'Listening => Host: {Host_IP}. Port: {Host_Port}')

        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            for known_node_socket in read_sockets:
                if known_node_socket == server_socket:
                    node_sock, client_address = server_socket.accept()
                    user = self.chat_handler(node_sock)

                    if user is False:
                        continue

                    sockets_list.append(node_sock)
                    nodes[node_sock] = user
                    print(f"{user['data'].decode('utf-8')} connected")
                else:
                    chat = self.chat_handler(known_node_socket)
                    if chat is False:
                        print('{} Has left'.format(nodes[known_node_socket]['data'].decode('utf-8')))

                        sockets_list.remove(known_node_socket)
                        del nodes[known_node_socket]
                        continue

                    node = nodes[known_node_socket]
                    for node_sock in nodes:
                        if node_sock != known_node_socket:
                            node_sock.send(node['header'] + node['data'] + chat['header'] + chat['data'])

            for known_node_socket in exception_sockets:
                sockets_list.remove(known_node_socket)
                del nodes[known_node_socket]


