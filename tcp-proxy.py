#!/usr/bin/env python3

import os
import socket
from threading import Thread
from prompt_toolkit import prompt

buf_size = 4096


class ProxyToServer(Thread):
    def __init__(self, host, port):
        super(ProxyToServer, self).__init__()

        self.client = None
        self.port = port
        self.host = host

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:
            data = self.server.recv(buf_size)

            if data:
                print("from server>", data.hex())

                self.client.sendall(data)


class ClientToProxy(Thread):
    def __init__(self, host, port):
        super(ClientToProxy, self).__init__()

        self.server = None
        self.port = port
        self.host = host

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)

        self.client, _addr = sock.accept()

    def run(self):
        while True:
            data = self.client.recv(buf_size)

            if data:
                print("from client>", data.hex())

                self.server.sendall(data)


class Proxy(Thread):
    def __init__(self, from_host, from_port, to_host, to_port):
        super(Proxy, self).__init__()

        self.from_host = from_host
        self.from_port = from_port

        self.to_host = to_host
        self.to_port = to_port

        print("Proxying from %s:%s to %s:%s" % (from_host, from_port, to_host, to_port))

    def run(self):
        while True:
            self.to_proxy = ClientToProxy(self.from_host, self.from_port)
            self.to_server = ProxyToServer(self.to_host, self.to_port)

            self.to_proxy.server = self.to_server.server
            self.to_server.client = self.to_proxy.client

            self.to_proxy.start()
            self.to_server.start()


master = Proxy("0.0.0.0", 1337, "127.0.0.1", 1338)
master.start()

def quit():
    # master.to_server.server.close()
    os._exit(0)

while True:
    try:
        cmd = input("$ ")
        if "quit" in cmd:
            quit()
    except Exception as e:
        print("Error:", e)
