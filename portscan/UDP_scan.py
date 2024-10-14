import socket
from typing import final

from port import Port


def scan_port(ip: str, port: int) -> Port:
    res = Port(ip, port)
    res.type = 'UDP'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(1)
        try:
            sock.sendto(b'ping', (ip, port))
            data, _ = sock.recvfrom(1024)

            if data.startswith(bytes([3, 3])):
                return res.set_close()
            else:
                return res.set_open()

        except socket.timeout:
            return res.set_open()
        except socket.error:
            return res.set_close()
