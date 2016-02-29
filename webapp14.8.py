#!/usr/bin/python

"""
Sumador Simple
"""

import socket
# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page.
        """
        respuesta = '<html><body><h1>It Works!</h1></body></html>'
        return ("200 OK", respuesta)

    def numero(self, request):
        num = int(request.split(' ')[1][1:])
        return num

    def suma(self, num, num2):
        suma = num + num2
        return suma


    def __init__(self, hostname, port):
        """Initialize the web application."""
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Let the port be reused if no process is actually using it
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to the address corresponding to the main name of the host
        mySocket.bind(('localhost', 1235))

        # Queue a maximum of 5 TCP connection requests

        mySocket.listen(5)

        # Accept connections, read incoming data, and answer back an HTML page
        #  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)
        num = None;
        suma = None;

        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'Request received:'
            peticion = recvSocket.recv(2048)
            print peticion
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            if(num == None):
                num = self.numero(request)
            elif (num != None):
                num2 = self.numero(request)
                resultado = self.suma(num, num2)
                num = resultado

            print 'Answering back...'

            recvSocket.send("HTTP/1.1" + returnCode +"\r\n\r\n" + htmlAnswer + "\r\n")
            recvSocket.close()


if __name__ == "__main__":
    testWebApp = webApp("localhost", 1235)
