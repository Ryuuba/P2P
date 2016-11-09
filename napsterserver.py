import socket
import marshal
import random
import thread
import time

HCNX = "conx"
HQRY = "qry_"
HOK = "OK__"
HRES = "resp"
NAPSTERHOST = '127.0.0.1'
NAPSTERPORT = 1024


class Napster(object):
    """A simple NAPSTER server
       Attributes:
       A dictionary named content storing <music, peerset> pairs
       A list port_list keeping <holder, port> pairs
       """
    __content = {}
    __port_list = {}
    __port = None
    __host = None
    __backlog = None
    __listener = None
    #Initialization of server
    def __init__(self, backlog):
        self.__host = NAPSTERHOST
        self.__port = NAPSTERPORT
        self.__backlog = backlog
        print self.__host, ' ', self.__port, ' ', backlog
        self.__listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__listener.bind((self.__host, self.__port))
        self.__listener.listen(self.__backlog)

    def __get_header(self, client_socket):
        """Returns the 4-bit header of the application msg"""
        response = client_socket.recv(4)
        return response

    def __add_content(self, client_socket, client_addr):
        """Add entries to the dictionary content"""
        data = client_socket.recv(4096)
        contentlst = marshal.loads(data)
        holder = client_addr[0], self.__port_list[client_addr[0]]
        for filename in contentlst:
            if filename in self.__content:
                self.__content[filename].add(holder)
            else:
                peerset = set([holder])
                print peerset
                self.__content[filename] = peerset

    def __send_ok(self, client_socket, client_addr):
        """Send a message OK to a client"""
        msg = HOK + str(self.__port_list[client_addr[0]])
        client_socket.send(msg)

    def __response_query(self, client_socket, client_addr):
        """Send the peerset associated to a given filename to a client"""
        print "Processing query from", client_addr[0]
        filename = client_socket.recv(128)
        if filename in self.__content:
            response = marshal.dumps(self.__content[filename])
            client_socket.send(response)
        else:
            response = marshal.dumps(self.__content)
            client_socket.send(response)

    def __handler(self, client_socket, client_addr):
        """Method to be executed as a thread"""
        print "Thread ", thread.get_ident(), " is working"
        time.sleep(5)
        while 1:
            header = client_socket.recv(4)
            if not header:
                print "No valid message received"
                client_socket.close()
                break
            elif header == HCNX:
                print "connection from ", client_addr[0]
                self.__add_content(client_socket, client_addr)
                self.print_content()
                self.__send_ok(client_socket, client_addr)
            elif header == HQRY:
                print "query from ", client_addr[0]
                self.__response_query(client_socket, client_addr)
            else:
                print "Close connection with ", client_addr[0]
                client_socket.close()
                break

    def manage_client_connection(self, client_socket, client_addr):
        """Manages communications with clients"""
        thread.start_new_thread(self.__handler, (client_socket, client_addr))

    def accept(self):
        """Waits for incoming connections"""
        self.__listener.settimeout(60)
        print "Waiting for connections. . ."
        client_socket, client_addr = self.__listener.accept()
        if client_addr[0] not in self.__port_list:
            self.__port_list[client_addr[0]] = random.randint(1025, 49151)
        return client_socket, client_addr

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

    def print_content(self):
        """Prints the dictionary content"""
        for filename, lst in self.__content.items():
            print filename, lst
