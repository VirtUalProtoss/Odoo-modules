
import socket


class rs232tcp():

    sock = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            print 'Connecting to', self.host, str(self.port)
            self.sock.connect((self.host, self.port))
            return 0
        except socket.error, e:
            print e
            return e

    def send(self, data):
        print 'Sending', data
        self.sock.send(data)

    def write(self, data):
        print 'Writing', data
        self.sock.send(data)

    def recv(self, timeout=None):
        data = self.sock.recv(timeout)
        print 'Receiving', data
        return data

    def read(self, length=1):
        data = self.sock.recv(length)
        print 'Reading', length, 'of', data
        return data
