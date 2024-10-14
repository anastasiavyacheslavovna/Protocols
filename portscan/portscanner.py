import socket
from multiprocessing.pool import ThreadPool
import argparse

import TCP_scan
import UDP_scan
from port import Port
from addition import start_print, RES, what_port


def scan_and_safe_port(ip: str, port: int, out: list[Port], scan):
    res = scan.scan_port(ip, port)
    if res.open_or_close:
        out.append(what_port(res))
        RES.append(res.answer())


def find_open_ports(ip: str, port_from: int, port_of_include: int, scan) -> list[Port]:
    pool = ThreadPool()
    ports = []

    for port in range(port_from, port_of_include + 1):
        pool.apply_async(func=scan_and_safe_port, args=(ip, port, ports, scan))

    pool.close()
    pool.join()
    return ports


def main(host: str, port_from: int, port_to: int, tsp: bool, udp: bool):
    try:
        ip = socket.gethostbyname(host)
    except socket.error:
        print('host don\'t find')
        return

    if not tsp and not udp:
        print('don\'t now type scan')
        return

    start_print()
    print('scan start')

    if tsp:
        find_open_ports(ip, port_from, port_to, TCP_scan)

    if udp:
        find_open_ports(ip, port_from, port_to, UDP_scan)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="IP адрес или host, у которого необходимо просканировать порты", type=str)
    parser.add_argument("-t", help="TCP сканирование", action="store_true", default=False)
    parser.add_argument("-u", help="UDP сканирование", action="store_true", default=False)
    parser.add_argument("-p", "--ports", help="Диапазон портов сканирования (включительно)", type=int,
                        default=[1, 1024], nargs=2)

    args = parser.parse_args()

    main(args.host, args.ports[0], args.ports[1], args.t, args.u)