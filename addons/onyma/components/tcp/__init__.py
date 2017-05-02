# -*- coding: utf-8 -*-

__author__ = 'virtual'


import cPickle
import socket
import struct
import select
import sys
import signal
from datetime import datetime


marshall = cPickle.dumps
unmarshall = cPickle.loads


def send(channel, *args):
    buf = marshall(args)
    value = socket.htonl(len(buf))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buf)

def receive(channel):

    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error, e:
        return ''

    buf = ""

    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    return unmarshall(buf)[0]


class Server(object):

    def __init__(self, host, port=8765, backlog=5):
        self.clients = 0
        # Client map
        self.clientmap = {}
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        #print 'Listening to port', port, '...'
        self.server.listen(backlog)
        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        # Close the server
        print 'Shutting down server...'
        # Close existing client sockets
        for o in self.outputs:
            o.close()

        self.server.close()

    def shutdown(self):
        # Close the server
        print 'Shutting down server...'
        # Close existing client sockets
        for o in self.outputs:
            o.close()

        self.server.close()

    def setRequestHandler(self, handler):
        self.requestHandler = handler

    def serve(self):

        inputs = [self.server, sys.stdin, ]
        self.outputs = []

        running = 1

        while running:

            try:
                inputready, outputready, exceptready = select.select(inputs, self.outputs, [])
            except select.error, e:
                break

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    #print 'server: got connection %d from %s' % (client.fileno(), address)

                    self.clients += 1

                    inputs.append(client)
                    self.clientmap[client] = (address, client.fileno())
                    result = self.requestHandler.serve(self.clientmap[client], {
                        'action': 'connect',
                        'address': address,
                    })
                    if result:
                        print 'Sending result to client', result, client
                        send(client, result)
                    self.outputs.append(client)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    # handle all other sockets
                    try:
                        data = receive(s)
                        if data:
                            # SProcess data
                            result = self.requestHandler.serve(self.clientmap[s], data)
                            if result:
                                #print 'Sending result to client', result, s
                                send(s, result)
                        else:
                            #print 'Client disconnected: %d' % (s.fileno(), )
                            self.clients -= 1
                            result = self.requestHandler.serve(self.clientmap[s], {
                                'action': 'disconnect',
                                'address': self.clientmap[s],
                            })
                            if result:
                                #print 'Sending result to client', result, s
                                send(s, result)
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                    except socket.error, e:
                        # Remove
                        inputs.remove(s)
                        self.outputs.remove(s)

        self.server.close()


class Client(object):

    data = None

    def __init__(self, host='127.0.0.1', port=8765):
        # Quit flag
        self.flag = False
        self.port = int(port)
        self.host = host

    def connect(self, host=None, port=None):
        if host:
            self.host = host

        if port:
            self.port = int(port)
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            return 0
        except socket.error, e:
            return socket.error

    def send(self, data):
        send(self.sock, data)

    def recv(self):
        return receive(self.sock)

    def shutdown(self):
        self.sock.close()

    def setRequestHandler(self, handler):
        self.requestHandler = handler

    def loop(self, timeout=60):
        result = None
        #ntime = datetime.now()
        self.flag = False
        while not self.flag:
            #print 'Client loop alive'
            if self.data:
                send(self.sock, self.data)
                self.data = None
            try:
                # Wait for input from stdin & socket

                inputready, outputready, exceptready = select.select([self.sock], [self.sock],[self.sock])

                for e in exceptready:
                    if e == self.sock:
                        print 'Except', e
                    else:
                        print 'socket is:', e

                for o in outputready:
                    if o == self.sock:
                        if self.data:
                            send(o, self.data)
                            self.data = None
                        else:
                            pass

                for i in inputready:
                    if i == self.sock:
                        data = receive(self.sock)
                        if data:
                            self.requestHandler.serve(self.sock.fileno(), data)
                            self.flag = True
                            break
                    else:
                        print 'socket is:', i

                #data = receive(self.sock)
                #if data:
                #    self.requestHandler.serve(self.sock.fileno(), data)

            except socket.timeout:
                print 'timeout.'
                self.sock.close()
                break

            except socket.error, e:
                print 'error', socket.errno
                self.sock.close()
                return socket.error

            except KeyboardInterrupt:
                print 'Interrupted.'
                self.sock.close()
                break

            #if (datetime.now()- ntime).seconds > timeout:
            #    break

        #return result
