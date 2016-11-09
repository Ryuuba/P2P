import socket
import os
import marshal

HCNX = "conx"
HQRY = "qry_"
HOK = "OK__"
HRES = "resp"
NAPSTERHOST = '127.0.0.1'
NAPSTERPORT = 1024
PATH = "/home/adan/Music"
EXT = ".mp3"

class Peer(object):
    """A simple peer for Napster"""
    __list = []
    __content = ""
    __port = 0
    def __init__(self):
        self.__index = socket.socket()

    def connect(self):
        """Establishes a connection with napster server"""
        self.__index.connect((NAPSTERHOST, NAPSTERPORT))
        msg = HCNX + self.__content
        self.__index.send(msg)
        response = self.__index.recv(4)
        self.__port = self.__index.recv(8)
        return response

    def read_files(self):
        """Reads files from PATH directory"""
        path = os.listdir(PATH)
        for dat in path:
            filename = str(dat)
            if filename.find(EXT) != -1:
                self.__list.append(filename)
        self.__content += marshal.dumps(self.__list)

    def resolve_query(self, query):
        """Asks for the peerset associated to a filename"""
        msg = HQRY + query
        self.__index.send(msg)
        response = list(marshal.loads(self.__index.recv(4096)))
        return response

    def send_quit(self):
        """Sends a msg to finish the server process"""
        self.__index.send("exit")

    def print_file_list(self):
        """Prints the list of shared files"""
        for filename in self.__list:
            print filename

    def close(self):
        """Close the client's socket'"""
        self.__index.close()

    def get_connection_msg(self):
        """Retuns the data of the OK msg"""
        return self.__content

    def get_port(self):
        """Returns the port to receive queries from other peers"""
        return self.__port
