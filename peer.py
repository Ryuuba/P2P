#!/usr/bin/python
import napsterpeer

peer = napsterpeer.Peer()
peer.readFiles()
response = peer.connect()
if response == napsterpeer.headerOK:
  print "Port for serving requests: ", peer.getPort()
  query = 'Caifanes_Sera por eso.mp3'
  peerList = peer.resolveQuery(query)
  print peerList
peer.sendQuit()
peer.close()