# -*- coding: utf-8 -*-

import nclib

NHC_PORT = 8000

class NhcConnection:

    def __init__(self, host, port = NHC_PORT):
        self._socket = nclib.Netcat((host, port), udp=False)

    def __del__(self):
        self._socket.shutdown(1)
        self._socket.close()

    def _receive_until(self, s):
        return self._socket.recv_until(s)

    def receive(self):
        return self._socket.recv().decode()

    def read(self):
        return self._receive_until(b'\r')

    def send(self, msg):
        self._socket.send(msg.encode())
        return self.read()
