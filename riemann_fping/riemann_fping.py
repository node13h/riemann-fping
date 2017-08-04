# This file is part of riemann-fping.

# Automated is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import argparse
import logging
import socket

from riemann_client.transport import TCPTransport, UDPTransport
from riemann_client.client import Client

from riemann_fping.transport import TLSTransport
from riemann_fping import fping


class SendError(Exception):
    def __init__(self, message, summary):
        self.summary = summary
        return super().__init__(message)


def parsed_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Pings multiple targets and sends results to RIEMANN')

    parser.add_argument(
        '--host', type=str, default='localhost', help='RIEMANN host')
    parser.add_argument(
        '--port', type=int, default=5555, help='RIEMANN port')
    parser.add_argument(
        '--protocol', type=str, default='tcp', choices=('tcp', 'udp', 'tls'),
        help='RIEMANN protocol')
    parser.add_argument(
        '--timeout', type=int, default=30,
        help='Timeout for the TCP connection to RIEMANN')
    parser.add_argument(
        '--keyfile', type=str,
        help='Key file for the TLS connection')
    parser.add_argument(
        '--certfile', type=str,
        help='Certificate file for the TLS connection')
    parser.add_argument(
        '--ca-certs', type=str,
        help='CA certificate file to authenticate the server')

    parser.add_argument(
        '--probe', type=str, default=socket.getfqdn(),
        help='Name of the probe')

    parser.add_argument(
        '--fping-cmd', type=str, default='/usr/sbin/fping',
        help='Path to the fping command')
    parser.add_argument(
        '--interval', type=int, default=60,
        help='Event interval in seconds')

    parser.add_argument(
        '--debug', action='store_true', help='Enable debug mode')

    parser.add_argument('target', nargs='+')

    args = parser.parse_args(args)

    if args.protocol == 'tls' and args.ca_certs is None:
        parser.error('--ca-certs is required for the TLS protocol')

    return args


def send_summary(client, summary):
    event = client.create_event(summary)

    try:
        with client:
            logging.debug('Sending event {}'.format(client.create_dict(event)))
            client.send_event(event)
    except (KeyboardInterrupt, SystemExit):
        raise

    except Exception as e:
        raise SendError(str(e), summary)


def main():
    args = parsed_args(sys.argv[1:])

    logging_level = logging.DEBUG if args.debug else logging.WARNING
    logging.basicConfig(level=logging_level)

    try:
        if args.protocol == 'tcp':
            transport = TCPTransport(args.host, args.port, args.timeout)
        elif args.protocol == 'tls':
            transport = TLSTransport(
                args.host, args.port, args.timeout,
                keyfile=args.keyfile, certfile=args.certfile, ca_certs=args.ca_certs)
        elif args.protocol == 'udp':
            transport = UDPTransport(args.host, args.port)
        else:
            raise RuntimeError('Transport {} is not supported'.format(args.transport))

        fp = fping.Fping(args.fping_cmd, args.probe, interval=args.interval)

        client = Client(transport)

        for summary in fp.ping_summaries(args.target):
            try:
                send_summary(client, summary)
            except SendError as e:
                logging.warning('Unable to send {} to {} ({})'.format(
                    e.summary, args.host, e))

    except Exception as e:
        if args.debug:
            raise
        else:
            logging.error('Unhandled exception ({})'.format(e))
            return 1

    return 0
