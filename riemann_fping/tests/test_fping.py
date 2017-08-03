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
    def test_fping_parse_summary(self):
        output = (
            '[12:01:02]\n'
            'host1.example.com : xmt/rcv/%loss = 10/10/0%, min/avg/max = 47.4/53.9/65.3\n'
            'host2.example.com : xmt/rcv/%loss = 10/10/0%, min/avg/max = 1.0/50.1/100.2\n'
            '[12:01:12]\n'
            'host1.example.com : xmt/rcv/%loss = 5/10/50%, min/avg/max = 100.3/150.0/200.4\n'
            'host2.example.com : xmt/rcv/%loss = 2/10/80%, min/avg/max = 32.9/80.4/130.1\n'
        )

        obj = fping.Fping(delay=10)

        data = list(obj.parse(output))

        self.assertEqual(data, [
            {
                'service': 'fping/min',
                'host': 'host1.example.com',
                'metric': 47.4,
                'ttl': 20,
            },
            {
                'service': 'fping/avg',
                'host': 'host1.example.com',
                'metric': 53.9,
                'ttl': 20,
            },
            {
                'service': 'fping/max',
                'host': 'host1.example.com',
                'metric': 65.3,
                'ttl': 20,
            },
            {
                'service': 'fping/loss',
                'host': 'host1.example.com',
                'metric': 0.0,
                'ttl': 20,
            },
            {
                'service': 'fping/min',
                'host': 'host2.example.com',
                'metric': 1,
                'ttl': 20,
            },
            {
                'service': 'fping/avg',
                'host': 'host2.example.com',
                'metric': 50.1,
                'ttl': 20,
            },
            {
                'service': 'fping/max',
                'host': 'host2.example.com',
                'metric': 100.2,
                'ttl': 20,
            },
            {
                'service': 'fping/loss',
                'host': 'host2.example.com',
                'metric': 0.0,
                'ttl': 20,
            },
            {
                'service': 'fping/min',
                'host': 'host1.example.com',
                'metric': 100.3,
                'ttl': 20,
            },
            {
                'service': 'fping/avg',
                'host': 'host1.example.com',
                'metric': 150.0,
                'ttl': 20,
            },
            {
                'service': 'fping/max',
                'host': 'host1.example.com',
                'metric': 200.4,
                'ttl': 20,
            },
            {
                'service': 'fping/loss',
                'host': 'host1.example.com',
                'metric': 50,
                'ttl': 20,
            },
            {
                'service': 'fping/min',
                'host': 'host2.example.com',
                'metric': 32.9,
                'ttl': 20,
            },
            {
                'service': 'fping/avg',
                'host': 'host2.example.com',
                'metric': 80.4,
                'ttl': 20,
            },
            {
                'service': 'fping/max',
                'host': 'host2.example.com',
                'metric': 130.1,
                'ttl': 20,
            },
            {
                'service': 'fping/loss',
                'host': 'host2.example.com',
                'metric': 80,
                'ttl': 20,
            }])


if __name__ == '__main__':
    unittest.main()
