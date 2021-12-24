BUF_SZ = 10
Host_IP = '127.0.0.1'
Host_Port = int(sys.argv[1])

def chat_handler(node_sock):
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