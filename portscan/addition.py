import threading
import socket

from port import Port

RES = []


def printer():
    while True:
        try:
            print(RES.pop())
        except IndexError:
            pass

def start_print():
    thread = threading.Thread(target=printer, daemon=True)
    thread.start()

def what_port(port: Port) -> Port:
    try:
        port.description = socket.getservbyport(port.port, port.type)
    except socket.error:
        pass
    return port
