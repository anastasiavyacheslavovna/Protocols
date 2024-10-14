import socket
from port import Port


def scan_port(ip: str, port: int) -> Port:
    res = Port(ip, port)
    res.type = "TCP"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
            return res.set_open()
        except socket.error:
            return res.set_close()
