# Copyright (C) 2017 Sergej Alikov <sergej.alikov@gmail.com>

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

import unittest

from riemann_fping import fping


class FpingTestCase(unittest.TestCase):
    def test_get_fping_summary_args(self):
        obj = fping.Fping('/usr/local/bin/fping', 'probe.example.com', interval=21)

        args = obj.get_fping_summary_args(['target1.example.com', 'target2.example.com'])

        self.assertEqual(args, [
            '/usr/local/bin/fping',
            '-D', '-B', '1', '-r', '0', '-O', '0', '-p', '1000', '-l', '-Q', '21',
            'target1.example.com', 'target2.example.com',
        ])

    def test_fping_parse_summary(self):
        output = (
            '[12:01:02]\n'
            'target1.example.com : xmt/rcv/%loss = 10/10/0%, min/avg/max = 47.4/53.9/65.3\n'
            'target2.example.com : xmt/rcv/%loss = 10/10/0%, min/avg/max = 1.0/50.1/100.2\n'
            '[12:01:12]\n'
            'target1.example.com : xmt/rcv/%loss = 5/10/50%, min/avg/max = 100.3/150.0/200.4\n'
            'target2.example.com : xmt/rcv/%loss = 2/10/80%, min/avg/max = 32.9/80.4/130.1\n'
        )

        obj = fping.Fping('/usr/local/bin/fping', 'probe.example.com', interval=10)

        data = list(obj.parse(output))

        self.assertEqual(data, [
            {
                'service': 'fping/min',
                'host': 'probe.example.com',
                'metric_f': 47.4,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/avg',
                'host': 'probe.example.com',
                'metric_f': 53.9,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/max',
                'host': 'probe.example.com',
                'metric_f': 65.3,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/loss',
                'host': 'probe.example.com',
                'metric_f': 0.0,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/min',
                'host': 'probe.example.com',
                'metric_f': 1,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/avg',
                'host': 'probe.example.com',
                'metric_f': 50.1,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/max',
                'host': 'probe.example.com',
                'metric_f': 100.2,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/loss',
                'host': 'probe.example.com',
                'metric_f': 0.0,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/min',
                'host': 'probe.example.com',
                'metric_f': 100.3,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/avg',
                'host': 'probe.example.com',
                'metric_f': 150.0,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/max',
                'host': 'probe.example.com',
                'metric_f': 200.4,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/loss',
                'host': 'probe.example.com',
                'metric_f': 50,
                'ttl': 20,
                'attributes': {'target': 'target1.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/min',
                'host': 'probe.example.com',
                'metric_f': 32.9,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/avg',
                'host': 'probe.example.com',
                'metric_f': 80.4,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/max',
                'host': 'probe.example.com',
                'metric_f': 130.1,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            },
            {
                'service': 'fping/loss',
                'host': 'probe.example.com',
                'metric_f': 80,
                'ttl': 20,
                'attributes': {'target': 'target2.example.com'},
                'tags': ['fping'],
            }])


if __name__ == '__main__':
    unittest.main()
