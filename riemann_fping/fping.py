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

import re

RE_HOST = r'(?P<host>.*)'
RE_XMT_RCV_LOSS = r'(?P<xmt>[0-9]+)\/(?P<rcv>[0-9]+)\/(?P<loss>[0-9.]+)%'
RE_MIN_AVG_MAX = r'(?P<min>[0-9.]+)\/(?P<avg>[0-9.]+)\/(?P<max>[0-9.]+)'

RE_FPING_SUMMARY = r'^{} : xmt\/rcv\/%loss = {}, min\/avg\/max = {}$'.format(
    RE_HOST, RE_XMT_RCV_LOSS, RE_MIN_AVG_MAX)


class Fping:
    def __init__(self, fping_cmd='/usr/sbin/fping', delay=10):
        self.fping_cmd = fping_cmd
        self.delay = delay

    def get_fping_summary_args(self, *targets):
        base_args = [
            self.fping_cmd,
            '-D', '-B', '1', '-r', '0', '-O', '0', '-p', '1000', '-l', '-Q',
            str(self.delay)
        ]
        return base_args + list(targets)

    def parse(self, fping_output):

        lines = fping_output.splitlines()
        re_summary = re.compile(RE_FPING_SUMMARY)

        for line in lines:

            match = re_summary.match(line)

            if match is not None:
                for measurement in ('min', 'avg', 'max', 'loss'):
                    yield {
                        'service': 'fping/{}'.format(measurement),
                        'host': match.group('host'),
                        'metric': float(match.group(measurement)),
                        'ttl': self.delay * 2,
                    }
