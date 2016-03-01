#!/usr/bin/python3

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


    def __init__(self, hostname, port):
        esPrimer = True
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
            print ('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print ('Request received:')
            request = recvSocket.recv(2048)
            print (request)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)

            print ('Answering back...')

            recvSocket.send(bytes("HTTP/1.1" + returnCode + "\r\n\r\n" + htmlAnswer + "\r\n",'UTF-8'))
            recvSocket.close()


class sumadorApp(webApp):
    def parse(self, request):
        try:
            num = int(request.split()[1][1:])
            valido = True
        except ValueError:
            valido = False
            num = 0
        return num, valido

    def process(self, parsedRequest):
        num, valido = parsedRequest
        if not valido:
                respuesta = '<html><body><h1>Solo manejo enteros</h1></body></html>'
                return ("200 OK", respuesta)
        if self.esPrimer:
            self.primernum = num
            self.esPrimer = False
            respuesta = '<html><body><h1>Dame otro</h1></body></html>'
            return ("200 OK", respuesta)
        else:
            segundonum = num
            suma = self.primernum + segundonum
            self.esPrimer = True
            return ("HTTP/1.1 200 OK\r\n\r\n",
                    "<html><body><h1> " + str(suma) +
                    "</h1></body></html>" + "\r\n")



    def __init__(self, hostname, port):
        self.esPrimer = True
        super(sumadorApp,self).__init__(hostname,port)


if __name__ == "__main__":
    testWebApp = sumadorApp("localhost", 1235)
