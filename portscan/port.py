class Port:
    def __init__(self, host: str, port: int, open_or_close: bool = False):
        self.host = host
        self.port = port
        self.open_or_close = open_or_close
        self.type = ""
        self.description = ""

    def set_open(self):
        self.open_or_close = True
        return self

    def set_close(self):
        self.open_or_close = False
        return self

    def answer(self):
        return f'{"" if self.open_or_close else "close"} {self.port} {self.type} {self.description}'
