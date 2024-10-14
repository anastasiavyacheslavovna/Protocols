from getpass import getpass
import socket

from addition import ExceptionImap, get_head, print_head


class ImapClient:
    def __init__(self, user: str, server: str, port: int, sll: bool):
        self.user = user
        self.server = server
        self.port = port
        self.sll = sll
        self.socket: [socket.socket, None] = None
        self.password = getpass(prompt="Your password")


    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(3)
        try:
            self.socket.connect((self.server, self.port))
            if self.sll:
                self.socket = self.sll.wrap_socket(self.socket)
            self.get_answer()
            self.login()
        except ExceptionImap as e:
            self.socket.close()
            self.socket = None
            raise e
        return self


    def send(self, msg: str):
        if self.socket is None:
            raise ExceptionImap('Connection is None')
        msg = msg + '\n'
        self.socket.send(msg.encode("utf-8"))

    def get_answer(self):
        if self.socket is None:
            raise ExceptionImap('Connection is None')
        msg = b''
        while True:
            try:
                read = self.socket.revc(1024)
                msg += read
                if len(read) < 1024:
                    break
            except Exception:
                break
        ans = msg.decode('utf-8')
        if "BAD" in ans or "NO" in ans:
            raise ExceptionImap(ans)
        while not any([i in ans for i in ['NO', 'BAD', 'OK']]):
            ans += self.get_answer()
        return ans


    def login(self):
        self.send(f'CM0 LOGIN {self.user} {self.password}')
        self.get_answer()


    def print_title(self, num: int):
        self.send(f'CMD3 FETCH {num} (BODY[HEADER.FIELDS (Date From To Subject)] BODYSTRUCTURE)')
        ans = get_head(self.get_answer())
        print_head(ans)


    def read_letter(self, from_letter: int, to_letter: int, mail: str):
        self.send(f"CMD1 SELECT {mail}")
        try:
            count = int(self.get_answer().split('\n')[1].split(' ')[1]) + 1
        except:
            return
        for i in range(count - from_letter, count - to_letter - 1, -1):
            self.print_title(i)
        return self


    def close(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
