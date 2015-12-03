#!/usr/bin/env python2
# -*-*- encoding: utf-8 -*-*-
# Created: Thu, 03 Dec 2015 14:12:23 -0200

"""
Util functions
"""

import binascii
import random
import select
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


# Receiver UDP port
RCV_PORT = 9001

TIPO_DADO = 0b0101010101010101
TIPO_NOME = 0b0000000011111111
TIPO_ACK = 0b1010101010101010
TIPO_EOF = 0b1111111100000000
MSS = 2000
TIMEOUT = 5
HEADER_LEN = 8  # tamanho do cabecalho, crc + seq num

pacote = namedtuple("pacote", ["num", "sum", "tipo", "data", "acked"])
ack = namedtuple("pacote", ["num", "sum", "tipo"])


def crc32(data):
    buf = (binascii.crc32(data) & 0xFFFFFFFF)
    return buf
    #return "%08X" % buf


# Cria *uma lista* de pacotes para serem enviados
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
    novo_pacote = pacote._make(unpack('iIH' + str(len(dado) - HEADER_LEN) + 's', dado) + (False,))
    return novo_pacote


# Envia pacote to tipo ACK para a maquina, usando o socket
def envia_ack(sock, num, host, porta):
    # Primeiro cria o pacote ACK
    dado = pack('iIH', num, 0, TIPO_ACK)
    sock.sendto(dado, (host, porta))


# Envia pacote para o servidor
def envia_um_pacote(sock, pkt, host, porta):
    # Primeiro gera o dado a ser enviado
    dado = pack('iIH' + str(len(pkt.data)) + 's', pkt.num, int(pkt.sum), pkt.tipo, pkt.data)
    sock.sendto(dado, (host, porta))


# Rotina para corromper o pacote
def corrompe_pacote(pkt, probabilidade=1):
    r = random.random()
    if (r <= probabilidade):
        pkt.data = pkt.data[::-1]
    return pkt


# Envia pacotes utilizando a funcao envia_um_pacote
def envia_pacotes(sock, pacotes, host, porta, window):
    ultimo_sem_ack = 0
    sem_ack = 0

    while ultimo_sem_ack < len(pacotes):
        if sem_ack < window and (sem_ack + ultimo_sem_ack) < len(pacotes):
            envia_um_pacote(sock, pacotes[ultimo_sem_ack + sem_ack], host, porta)
            sem_ack += 1
        else:
            # Listen for ACKs
            pronto = select.select([sock], [], [], TIMEOUT)
            if pronto[0]:
                dado, addr = sock.recvfrom(MSS)
            else:  # Window is full and no ACK received before timeout
                print "Timeout, seq num =", ultimo_sem_ack
                sem_ack = 0
                continue
            # Confirma se o pacote é mesmo do servidor
            if addr[0] != host:
                continue
            # Decodifica dados
            pkt = processa_pacote(dado)
            # Confirma se o pacote é mesmo oum pacote ack
            if pkt.tipo != TIPO_ACK:
                continue
            # Verifica o seq num para ver se é mesmo o pacote mandado
            if pkt.num == ultimo_sem_ack:
                ultimo_sem_ack += 1
                sem_ack -= 1
            else:
                sem_ack = 0


# Funcao que cria pacotes, envia os pacotes e manda fim de arquivo (EOF)
def envia_dados(dados, tipo, sock, host, porta, window):
    envia_pacotes(sock, cria_pacotes(dados, tipo), host, porta, window)
    envia_um_pacote(cria_pacotes('', tipo=TIPO_EOF))


# Funcao para receber dados
def recebe_dados(sock):
    pkt = pacote(num=0, sum=0, tipo=0, data='', acked=False)
    dados = ''

    while (pkt.tipo is not TIPO_EOF):
        data, addr = sock.recvfrom(MSS)
        pkt = processa_pacote(data)

        if pkt.tipo != TIPO_ACK:
            continue

        cksum = crc32(pkt.data)
        if (pkt.sum == cksum):
            envia_ack(sock, pkt.num, pkt.host, pkt.porta)
            dados += pkt.data

    return dados
