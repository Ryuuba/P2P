import socket
import marshal
import random
import thread

HCNX = "conx"
HQRY = "qry_"
HOK = "OK__"
HRES = "resp"
NAPSTERHOST = '127.0.0.1'
NAPSTERPORT = 1024


class Napster(object):
    """A simple NAPSTER server
       Attributes:
       A dictionary named content storing <music, holder> pairs
       A list porList keeping <holder, port> pairs
       """
    __content = {}
    __port_list = {}
    __client_addr = None
    __client_connection = None
    #Initialization of server
    def __init__(self, backlog):
        self.__host = NAPSTERHOST
        self.__port = NAPSTERPORT
        self.__backlog = backlog
        print repr(self.__host) + ' ' + repr(self.__port) + ' ' + repr(backlog)
        self.__listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__listener.bind((self.__host, self.__port))
        self.__listener.listen(self.__backlog)

    def accept(self):
        """Waits for incoming connections"""
        self.__client_connection, self.__client_addr = self.__listener.accept()
        if self.__client_addr[0] not in self.__port_list:
            self.__port_list[self.__client_addr[0]] = random.randint(1025, 49151)

    def get_header(self):
        """Returns the 4-bit header of the application msg"""
        response = self.__client_connection.recv(4)
        return response

    def add_content(self):
        """Add entries to the dictionary content"""
        data = self.__client_connection.recv(4096)
        contentlst = marshal.loads(data)
        holder = self.__client_addr[0], self.__port_list[self.__client_addr[0]]
        for filename in contentlst:
            if filename in self.__content:
                self.__content[filename].add(holder)
            else:
                peerset = set([holder])
                print peerset
                self.__content[filename] = peerset

    def send_ok(self):
        """Send a message OK to a client"""
        msg = HOK + str(self.__port_list[self.__client_addr[0]])
        self.__client_connection.send(msg)

    def response_query(self):
        """Send the peerset associated to a given filename to a client"""
        filename = self.__client_connection.recv(128)
        if filename in self.__content:
            response = marshal.dumps(self.__content[filename])
            self.__client_connection.send(response)
        else:
            response = marshal.dumps(self.__content)
            self.__client_connection.send(response)

    def end(self):
        """Finishes the communication with a client"""
        self.__client_connection.close()

    def close(self):
        """Close the listener socket"""
        self.__listener.close()

    #Getter and setters
    def get_host(self):
        """Returns the ip of the server"""
        return self.__host

    def get_port(self):
        """Returns the port associated to the server process"""
        return self.__port

    def get_client_addr(self):
        """Returns a the pair (ip, port) associated to a client"""
        return self.__client_addr

    def print_content(self):
        """Prints the dictionary content"""
        for filename, lst in self.__content.items():
            print filename, lst
