import socket
import os
import marshal

headerCNX = "conx"
headerQRY = "qry_"
headerOK = "OK__"
headerRES = "resp"
napsterHost = '127.0.0.1'
napsterPort = 1024
path = "/home/adan/Music"
ext = ".mp3"

class Peer:
  """A simple peer for Napster"""
  __list = []
  __content = ""
  __port = 0
  def __init__(self):
    self.__index = socket.socket()

  def connect(self):
    self.__index.connect((napsterHost, napsterPort))
    msg = headerCNX + self.__content
    self.__index.send(msg)
    response = self.__index.recv(4)
    self.__port = self.__index.recv(8)
    return response

  def readFiles(self):
    self.__path = os.listdir(path)
    for dat in self.__path:
      filename = str(dat)
      if filename.find(ext) != -1:
        self.__list.append(filename)
    self.__content += marshal.dumps(self.__list)
  
  def resolveQuery(self, query):
    msg = headerQRY + query
    self.__index.send(msg)
    response = list(marshal.loads(self.__index.recv(4096)))
    return response

  def sendQuit(self):
    self.__index.send("exit")

  def printFileList(self):
    for filename in self.__list:
      print filename

  def close(self):
    self.__index.close()

  def getConnectionMsg(self):
    return self.__content
  
  def getPort(self):
    return self.__port