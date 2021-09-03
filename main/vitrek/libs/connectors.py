import socket
import time


# base abstract class
class Connector:

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def send(self, msg=''):
        raise NotImplementedError

    def receive(self, buffer=1024):
        raise NotImplementedError


# classic ethernet tcp/ip connection
class TCPConnector(Connector):
    def __init__(self, ip='172.16.3.204', port=10733):
        self.session = None
        self.ip = ip
        self.port = port
        self.is_connected = False

    def connect(self):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.session.connect((self.ip, self.port))
            self.is_connected = True
            return True
        except socket.error:
            self.session.close()
            return False

    def disconnect(self):
        try:
            self.session.close()
            self.is_connected = False
            return True
        except socket.error:
            return False

    def send(self, command=''):
        try:
            command += '\r\n'
            self.session.send(command.encode('ascii'))
            return True
        except socket.error:
            return False

    def receive(self, buffer=1024):
        try:
            return (self.session.recv(buffer).decode('ascii')).rstrip()
        except socket.error:
            return False


# Ajax solution. Ethernet udp - optic fiber - rs232 interface.
class UDPRSConnector(Connector):
    def __init__(self, ip='172.16.3.204', port=5070):
        self.__session = None
        self.__ip = ip
        self.__port = port
        self.udp_timeout = 5
        self.sleep_after_send = 0  # sec
        self.is_connected = False

    def connect(self):
        self.__session = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.__session.settimeout(self.udp_timeout)

        try:
            self.__session.connect((self.__ip, self.__port))
            self.is_connected = True
            return True
        except socket.error:
            self.__session.close()
            return False

    def disconnect(self):
        try:
            if self.__session is not None:
                self.__session.close()
                self.is_connected = False
            return True
        except socket.error:
            return False

    def send(self, command=''):
        try:
            command += '\r\n'
            self.__session.send(command.encode())
            time.sleep(self.sleep_after_send)
            return True
        except socket.error:
            return False

    def receive(self, buffer=1024):
        try:
            # sys_info = self.__session.recv(buffer)  # adapter sends two upd packets. It don't uses. We need second.
            data = b''
            while True:
                recv = self.__session.recv(buffer)  # receive all garbage packets and get first part of data
                if not (b'!C' in recv):
                    data = recv
                    break

            if b'\r\n' not in data:  # if data is not full, adapter will send second part of data
                data += self.__session.recv(buffer)
            return data.decode().strip()
        except socket.error:
            return False


if __name__ == "__main__":
    pass
