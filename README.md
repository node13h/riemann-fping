# riemann-fping

This program is a wrapper around the [fping](https://fping.org/) utility. It will use the fping to collect the latency and packet loss information to multiple targets and send the collected data to a [RIEMANN](http://riemann.io/) instance.
It uses the [borntyping's riemann-client](https://github.com/borntyping/python-riemann-client) to talk to RIEMANN.

Both server certificate validation and custom client certificates are supported for TLS connections.


## Installing

You can install the latest released verison of the riemann-fping with pip:
```bash
pip install riemann-fping
```

## Using
```
$ riemann-fping --help
usage: riemann-fping [-h] [--host HOST] [--port PORT]
                     [--protocol {tcp,udp,tls}] [--timeout TIMEOUT]
                     [--keyfile KEYFILE] [--certfile CERTFILE]
                     [--ca-certs CA_CERTS] [--probe PROBE]
                     [--fping-cmd FPING_CMD] [--interval INTERVAL] [--debug]
                     target [target ...]

Pings multiple targets and sends results to RIEMANN

positional arguments:
  target

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           RIEMANN host (default: localhost)
  --port PORT           RIEMANN port (default: 5555)
  --protocol {tcp,udp,tls}
                        RIEMANN protocol (default: tcp)
  --timeout TIMEOUT     Timeout for the TCP connection to RIEMANN (default:
                        30)
  --keyfile KEYFILE     Key file for the TLS connection (default: None)
  --certfile CERTFILE   Certificate file for the TLS connection (default:
                        None)
  --ca-certs CA_CERTS   CA certificate file to authenticate the server
                        (default: None)
  --probe PROBE         Name of the probe (default: FQDN-OF-THE-HOST-RUNNING-ON)
  --fping-cmd FPING_CMD
                        Path to the fping command (default: /usr/sbin/fping)
  --interval INTERVAL   Event interval in seconds (default: 60)
  --debug               Enable debug mode (default: False)
```

## Contributing

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file



