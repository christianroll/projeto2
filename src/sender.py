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
from util import recebe_dados, envia_dados, TIPO_DADO
# importando funcoes para teste
import unicodedata
from util import cria_pacotes, envia_um_pacote, TIPO_EOF
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
    #filename = recebe_dados(sdr_sock)
    filename, addr = sdr_sock.recvfrom(400)
    print("Nome do arquivo: {}".format(filename))

    if (os.path.isfile(filename)):
        with open(filename, mode="r") as sdr_file:
            teste = sdr_file.read()
            # print("Dados: {}".format(teste))
            #sdr_sock.sendto(teste, ('', 9002))
            # print("Enviando dados".format(filename))
            # envia_dados(teste, TIPO_DADO, sdr_sock, '', 9002, args.cwnd)
            pacote = cria_pacotes(teste, TIPO_DADO)
            # print("pacote: {}".format(pacote))
            
            n = 0
            while n < len(pacote):
                envia_um_pacote(sdr_sock, pacote[n], '', 9002)
                print("pack: {}".format(n))
                print("pacote: {}".format(pacote[n]))
                n += 1
            print("Enviou tudo")
            fim = 'final'
            fim2 = unicodedata.normalize('NFKD', fim).encode('ascii', 'ignore')
            pacotefinal = cria_pacotes(fim2, TIPO_DADO)
            print("pacotefinal: {}".format(pacotefinal[0]))
            envia_um_pacote(sdr_sock, pacotefinal[0], '', 9002)
    else:
        print ("Arquivo inexistente")
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
