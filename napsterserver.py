import socket
import marshal
import random

headerCNX = "conx"
headerQRY = "qry_"
headerOK = "OK__"
headerRES = "resp"
napsterHost = '127.0.0.1'
napsterPort = 1024


class Napster:
  """A simple napster server"""
  __content = {}
  __portList = {}
  #Initialization of server
  def __init__(self, backlog):
    self.__host = napsterHost
    self.__port = napsterPort
    self.__backlog = backlog
    print repr(self.__host) + ' ' + repr(self.__port) + ' ' + repr(backlog)
    self.__listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__listener.bind((self.__host, self.__port))
    self.__listener.listen(self.__backlog)
  
  def accept(self):
    self.__clientConnection, self.__clientAddr = self.__listener.accept()
    if self.__clientAddr[0] not in self.__portList:
      self.__portList[self.__clientAddr[0]] = random.randint(1025,65535)

  def getHeader(self):
    self.__msgHeader = self.__clientConnection.recv(4)
    return self.__msgHeader
  
  def addContent(self):
    data = self.__clientConnection.recv(4096)
    contentlst = marshal.loads(data)
    holder = self.__clientAddr[0], self.__portList[self.__clientAddr[0]]
    for filename in contentlst:
      if filename in self.__content:
        self.__content[filename].add(holder)
      else:
        peerset = set([holder])
        print peerset
        self.__content[filename] = peerset

  def sendOK(self):
    msg = headerOK + str(self.__portList[self.__clientAddr[0]])
    self.__clientConnection.send(msg)
  
  def responseQuery(self):
    filename = self.__clientConnection.recv(128)
    if filename in self.__content:
      response = marshal.dumps(self.__content[filename])
      self.__clientConnection.send(response)
    else:
      response = marshal.dumps(self.__content)
      self.__clientConnection.send(response)      

  def end(self):
    self.__clientConnection.close()

  def close(self):
    self.__listener.close()

  #Getter and setters
  def getHost(self):
    return self.__host
  
  def getPort(self):
    return self.__port
  
  def getClientAddr(self):
    return self.__clientAddr
  
  def getDataSize(self):
    return self.__dataSize
  
  def setHost(self, host):
    self.__host = host
  
  def setPort(self, port):
    self.__port = port

  def printContent(self):
    for filename, lst in self.__content.items():
      print filename, lst
