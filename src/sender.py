#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 15 Oct 2015 10:24:55 -0300

"""
UDP Sender
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys
import socket
from util import crc32 as checksum
import os


__authors__ = (
                'Christian Rollmann',
                'Isaac Mitsuaki Saito',
                'Julio Batista Silva',
                'Marcelo Fernandes Tedeschi'
              )
__license__ = "GPL v3"
__version__ = "1.0"




# MSS: Maximum segment size
MSS = 2000


def main(args):
    try:
        sdr_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sdr_sock.bind(("", args.port))
        print "waiting on port:", port
        data, addr = sdr_sock.recvfrom(MSS)
        #TODO: verificacao do checksum
        envia_ack(9001, num, host, porta)
        filename = processa_pacote(data)
        if (os.path.isfile(filename)):
            # If the file exists, start receiving from sender
            with open(filename + "_rcvd", mode="wd") as sdr_file:
                pkt = cria_pacotes(sdr_file.read())
            seq_num = 0
            try:
                while True:
            
            except socket.error:
                print("Socket error")
                continue
            
           






        else:
            print "Não existe arquivo"

    except socket.error:
        print("Failed to open UDP socket")
                
        
        



    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP Sender')
    parser.add_argument('-p', '--port', type=int, default=9001, help='Port')
    parser.add_argument('cwnd', help='Window size')
    parser.add_argument('PL', type=float, help='Packet Loss probability')
    parser.add_argument('PC', type=float, help='Packet Corruption probability')
    parser.add_argument('--version', action='version',
                        version='%(prog)s v' + __version__)
    args = parser.parse_args()

    sys.exit(main(args))
