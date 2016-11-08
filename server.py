#!/usr/bin/python
import napsterserver

server = napsterserver.Napster(5)
while True:
  server.accept()
  while True:
    header = server.getHeader()
    if header == napsterserver.headerCNX:
      print "connection from " + repr(server.getClientAddr())
      server.addContent()
      server.printContent()
      server.sendOK()
    elif header == napsterserver.headerQRY:
      print "query from " + repr(server.getClientAddr())
      server.responseQuery()
    else:
      break
  server.end()
server.close()
