#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 03 Dec 2015 14:12:23 -0200

"""
Util functions
"""

import binascii
import random
from collections import namedtuple
from struct import pack
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
TIPO_ACK = 0b1010101010101010
MSS = 2000
HEADER_LEN = 8  # tamanho do cabecalho, crc + seq num

pacote = namedtuple("pacote", ["num", "sum", "tipo", "data", "acked"])
ack = namedtuple("pacote", ["num", "sum", "tipo"])


def crc32(data):
    buf = (binascii.crc32(data) & 0xFFFFFFFF)
    return "%08X" % buf


# Cria pacotes para serem enviados
# O arquivo é dividido em vários pacotes de tamanho "MSS - HEADER_LEN".
# A função `min` é utilizada para quando último pacote for menor que esse valor
def cria_pacotes(dados, tipo=TIPO_DADO):
    num = 0
    pacotes = []
    enviados = 0
    a_enviar = min(MSS - HEADER_LEN, len(dados) - enviados)

    while a_enviar > 0:
        data = dados[enviados:enviados + a_enviar]
        pacotes.append(pacote(
            num=num,  # Número de sequência
            sum=crc32(data),  # Checksum
            tipo=tipo,  # DADO ou ACK em 16 bits
            data=data,  # (MSS - HEADER_LEN) bytes de dados
            acked=False))  # Se foi acked
        enviados += a_enviar
        a_enviar = min(MSS - HEADER_LEN, len(dados) - enviados)
        num += 1

    return pacotes


# Processa pacote ACK para o tipo a ser usados no programa
def processa_pac_ack(dado):
    # Converte dados para o tipo pacote ack a ser utilizado
    pac_ack = ack._make(unpack('iHH', dado))
    return pac_ack


# Processa pacote de dados para tipos a serem usados no programa
def processa_pacote(dado):
    # Converte dados para o tipo pacote a ser utilizado no programa
    novo_pacote = pacote._make(unpack('iHH' + str(len(dado) - HEADER_LEN) + 's', dado) + (False,))
    return novo_pacote


# Envia pacote to tipo ACK para a maquina, usando o socket
def envia_ack(socket, num, host, porta):
    # Primeiro cria o pacote ACK
    dado = pack('iHH', num, 0, TIPO_ACK)
    socket.sendto(dado, (host, porta))


# Envia pacote para o servidor
def envia_pacote(socket, pacote, host, porta):
    # Primeiro gera o dado a ser enviado
    dado = pack('iHH' + str(len(pacote.data)) + 's', pacote.num, int(pacote.sum), pacote.tipo, pacote.data)
    socket.sendto(dado, (host, porta))


# Rotina para corromper o pacote
def corrompe_pacote(pacote, probabilidade=1):
    r = random.random()
    if (r <= probabilidade):
        pacote.data = pacote.data[::-1]
    return pacote
