#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 15 Oct 2015 10:34:19 -0300


"""
UDP Receiver

Resquests a file from sender
Waits to receive all packets
"""


from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys

import socket
from util import MSS, RCV_PORT, crc32 as checksum


__authors__ = (
                'Christian Rollmann',
                'Isaac Mitsuaki Saito',
                'Julio Batista Silva',
                'Marcelo Fernandes Tedeschi'
              )
__license__ = "GPL v3"
__version__ = "1.0"


def main(args):

    # Receiver opens UDP socket
    try:
        rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rcv_sock.bind('', RCV_PORT)
    except socket.error:
        print("Failed to open UDP socket")
        sys.exit(1)

    rcv_sock.timeout(10)

    # Request the file "filename" from Sender
    rcv_sock.sendto(args.filename, (args.hostname, args.port))

    # The sender returns if the file exists
    data, addr = rcv_sock.recvfrom(MSS)

    # If the file exists, start receiving from sender
    with open(args.filename + "_rcvd", mode="wd") as rcvd_file:
        seq_num = 0
        try:
            while True:
                data, addr = rcv_sock.recvfrom(MSS)

                # File completely received
                if (data == "EOF"):
                    print("DEBUG: File received")
                    rcv_sock.close()
                    break

        except socket.error:
            print("Socket error")
            continue

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
