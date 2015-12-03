#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 03 Dec 2015 14:12:23 -0200

"""
Util functions
"""

import binascii
from collections import namedtuple
from struct import unpack

__authors__ = (
    'Christian Rollmann',
    'Isaac Mitsuaki Saito',
    'Julio Batista Silva',
    'Marcelo Fernandes Tedeschi'
)
__license__ = "GPL v3"
__version__ = "1.0"

TIPO_DADO = 0b0101010101010101
TIPO_NOME = 0b0000000011111111
TIPO_ACK =  0b1010101010101010
MSS = 2000
HEADER_LEN = 8  # tamanho do cabecalho, crc + seq num

pacote = namedtuple("pacote", ["num", "sum", "tipo", "data", "acked"])
ack = namedtuple("pacote", ["num", "sum", "tipo"])


def crc32(data):
    buf = (binascii.crc32(data) & 0xFFFFFFFF)
    return "%08X" % buf


### Cria pacotes para serem enviados
def cria_pacotes(dados):
    num = 0;
    pacotes = []
    enviados = 0
    a_enviar = min(MSS - HEADER_LEN, len(dados) - enviados)

    while a_enviar > 0:
        data = dados[enviados:enviados + a_enviar];
        pacotes.append(pacote(num=num, sum=crc32(data), tipo=TIPO_DADO, data=data, acked=False))
        enviados += a_enviar
        a_enviar = min(MSS - HEADER_LEN, len(dados) - enviados)
        num += 1

    return pacotes

def parse_ack(dado):
    # Converda dados para o tipo pacote ack a ser utilizado
    pac_ack = ack._make(unpack('iHH', dado))
    return pac_ack



