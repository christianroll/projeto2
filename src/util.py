#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 03 Dec 2015 14:12:23 -0200

"""
Util functions
"""

import binascii
from collections import namedtuple

__authors__ = (
    'Christian Rollmann',
    'Isaac Mitsuaki Saito',
    'Julio Batista Silva',
    'Marcelo Fernandes Tedeschi'
)
__license__ = "GPL v3"
__version__ = "1.0"

DATA_ID = 0b0101010101010101
MSS = 2000
HEADER_LEN = 8  # tamanho do cabecalho, crc + seq num
pkt = namedtuple("pkt", ["seq_num", "chk_sum", "pkt_type", "data", "acked"])


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
        pacotes.append(pkt(num=num, sum=crc32(data), tipo=DATA_ID, data=data, acked=False))
        enviados += a_enviar
        to_send = min(MSS - HEADER_LEN, len(dados) - enviados)
        num += 1

    return pacotes
