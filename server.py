#!/usr/bin/python
"""This module implements a basic napster-server"""
import napsterserver

def main():
    """Main function"""
    server = napsterserver.Napster(5)
    while True:
        client_data = server.accept()
        server.manage_client_connection(client_data[0], client_data[1])
    server.close()

if __name__ == '__main__':
    main()
