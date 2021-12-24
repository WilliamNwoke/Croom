"""
CPSC 5520, Seattle University
This is free and unencumbered software released into the public domain.
:Authors: Uchena
:Didn't use pickle because of extra bytes at the end of it
"""

import sys
import myNode
import myServer


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python3 lab6.py host_port, [command: server or client => |lower case| ]') 
        exit()

    print("   ''''''     ''''''      ''''''      ''''''     ''            '' ")
    print("  ''    ''    ''   ''    ''    ''    ''    ''    '' ''      '' '' ")
    print(" ''           ''  ''    ''      ''  ''      ''   ''   ''  ''   '' ")
    print(" ''           '' ''     ''      ''  ''      ''   ''     ''     '' ")
    print(" ''      ''   ''  ''     ''    ''    ''    ''    ''            '' ")
    print("  ''    ''    ''   ''     ''  ''      ''  ''     ''            '' ")
    print("   ''''''     ''    ''     ''''        ''''      ''            '' ")

    BUF_SZ = 10
    Host_IP = '127.0.0.1'
    Host_Port = int(sys.argv[1])
    
    myServer = myServer.Server()
    myNode = myNode.Node()

    print("What are you?\n")
    nodetype = input("server or client: \n")

    if nodetype == "server":
        myServer.run()
    if nodetype == "client":
        myNode.run()



    
                