
from uuid import uuid4

class Request:
    def __init__(self, headers = {}, method = "GET", path = "/", query = {}, body = {}, protocol = "HTTP/1.1", host = "localhost", port = 80, scheme = "http", ):
        self.headers = headers
        self.method = method
        self.path = path
        self.query = query
        self.body = body
        self.protocol = protocol
        self.host = host
        self.port = port
        self.scheme = scheme
        self.id = uuid4()

    def __str__(self):
        return f"{self.protocol} {self.method} {self.host}:{self.port}{self.path}\n{self.headers}\n{self.body}"
    
    