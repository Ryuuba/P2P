#!/usr/bin/python
"""This module implements a basic napster-peer"""
import napsterpeer

def main():
    """Main function"""
    peer = napsterpeer.Peer()
    peer.read_files()
    response = peer.connect()
    if response == napsterpeer.HOK:
        print "Port for serving requests: ", peer.get_port()
        query = 'Caifanes_Sera por eso.mp3'
        peer_list = peer.resolve_query(query)
        print peer_list
    peer.send_quit()
    peer.close()

if __name__ == '__main__':
    main()
