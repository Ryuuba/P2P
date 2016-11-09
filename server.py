#!/usr/bin/python
"""This module implements a basic napster-server"""
import napsterserver

def main():
    """Main function"""
    server = napsterserver.Napster(5)
    while True:
        server.accept()
        server.end()
    server.close()

if __name__ == '__main__':
    main()
