#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 15 Oct 2015 10:34:19 -0300


"""
UDP Receiver
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys


__authors__ = (
                'Christian Rollmann',
                'Isaac Mitsuaki Saito',
                'Julio Batista Silva',
                'Marcelo Fernandes Tedeschi'
              )
__license__ = "GPL v3"
__version__ = "1.0"


def main(args):
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP Receiver')
    parser.add_argument('hostname', help='Sender hostname')
    parser.add_argument('port', type=int, help='Sender port')
    parser.add_argument('filename', help='Filename')
    parser.add_argument('PL', type=float, help='Packet Loss probability')
    parser.add_argument('PC', type=float, help='Packet Corruption probability')
    parser.add_argument('--version', action='version',
                        version='%(prog)s v' + __version__)
    args = parser.parse_args()

    sys.exit(main(args))
