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
# from util import RCV_PORT, envia_dados, recebe_dados, TIPO_NOME
# import temporario para teste
from util import *


__authors__ = (
                'Christian Rollmann',
                'Isaac Mitsuaki Saito',
                'Julio Batista Silva',
                'Marcelo Fernandes Tedeschi'
              )
__license__ = "GPL v3"
__version__ = "1.0"

RCV_CWND = 10


def main(args):

    # Receiver abre socket UDP
    try:
        rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rcv_sock.bind(('', RCV_PORT))
    except socket.error:
        print("Failed to open UDP socket")
        sys.exit(1)

    #rcv_sock.settimeout(10)

    # Request the file "filename" from Sender
    #envia_dados(args.filename, TIPO_NOME, rcv_sock, args.hostname, args.port, RCV_CWND)

    filenam = args.filename
    rcv_sock.sendto(filenam, (args.hostname, args.port))

    # # If the file exists, start receiving from sender
    # dados = recebe_dados(rcv_sock)
    # printf("Dados: {}".format(dados))

    
    dados = recebe_dados(rcv_sock, args.hostname, args.port)
    print("\n\n")
    print("dados: {}".format(dados))
    # bla = processa_pacote(dados)
    # print("\n\n")
    # print("Teste: {}".format(bla))    


    # pkt = Pacote(num_seq=0, chksum=0, tipo=0, data='')
    # dados = ''

    # while (pkt.tipo != TIPO_EOF):
    #     data, addr = rcv_sock.recvfrom(4000)
    #     pkt = processa_pacote(data)
    #     print("received: {}".format(pkt))
    #     print("\n")
       
    #     if (pkt.tipo != TIPO_ACK):
    #         continue
    #     else: 
    #         print("Ack received") 

    #     cksum = crc32(pkt.data)
    #     if (pkt.chksum == cksum):
    #         envia_ack(rcv_sock, pkt.num_seq, '', 9001)
    #         dados += pkt.data

    rcv_sock.close()

    # Escreve dados em um arquivo
    #with open(args.filename + "_rcvd", mode="wd") as rcvd_file:
    #    rcvd_file.write(dados)

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
