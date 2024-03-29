#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 15 Oct 2015 10:24:55 -0300

"""
UDP Sender
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys
import socket
# from util import envia_dados, TIPO_DADO
from util import *
import os

__authors__ = (
    'Christian Rollmann',
    'Isaac Mitsuaki Saito',
    'Julio Batista Silva',
    'Marcelo Fernandes Tedeschi'
)
__license__ = "GPL v3"
__version__ = "1.0"


def main(args):
    try:
        sdr_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sdr_sock.bind(("", args.port))
        print("Abriu socket UDP na porta {}".format(args.port))
    except socket.error:
        print("Failed to open UDP socket")
    except Exception, e:
        print("Error: '{}'".format(e))

    print("waiting on port: {} ".format(args.port))
    filename, addr = sdr_sock.recvfrom(400)  # Nome do arquivo deve caber
    print("Nome do arquivo: {}".format(filename))

    if (os.path.isfile(filename)):
        with open(filename, mode="r") as sdr_file:
            envia_dados(sdr_file.read(), TIPO_DADO, sdr_sock, RCV_HOST, RCV_PORT, args.cwnd, args.PC, args.v)
            print("\t- Enviou todos os pacotes com sucesso...")
            print("-------------------------------------------------\n")
    else:
        print("Arquivo inexistente")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP Sender')
    parser.add_argument('-p', '--port', type=int, default=9001, help='Port')
    parser.add_argument('cwnd', help='Window size')
    parser.add_argument('PL', type=float, help='Packet Loss probability')
    parser.add_argument('PC', type=float, help='Packet Corruption probability')
    parser.add_argument('--version', action='version', version='%(prog)s v' + __version__)
    parser.add_argument('-v', help="verbose", action="store_true")
    args = parser.parse_args()

    sys.exit(main(args))
