import ssl

from riemann_client.transport import TCPTransport, HOST, PORT, TIMEOUT


class TLSTransport(TCPTransport):
    def __init__(
            self, host=HOST, port=PORT, timeout=TIMEOUT,
            keyfile=None, certfile=None, ca_certs=None):

        super(TLSTransport, self).__init__(host, port, timeout)
        self.keyfile = keyfile
        self.certfile = certfile
        self.ca_certs = ca_certs

    def connect(self):
        super(TLSTransport, self).connect()
        self.socket = ssl.wrap_socket(
            self.socket,
            keyfile=self.keyfile,
            certfile=self.certfile,
            ssl_version=ssl.PROTOCOL_TLSv1,
            cert_reqs=ssl.CERT_REQUIRED,
            ca_certs=self.ca_certs)
