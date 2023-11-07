class Response:
    def __init__(self, headers = {}, status = 200, body = {}, protocol = "HTTP/1.1", ):
        self.headers = headers
        self.status = status
        self.body = body
        self.protocol = protocol
        self.latency = 0

    def set_latency(self, latency):
        self.latency = latency
