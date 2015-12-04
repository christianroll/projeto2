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
import unicodedata

__authors__ = (
    'Christian Rollmann',
    'Isaac Mitsuaki Saito',
    'Julio Batista Silva',
    'Marcelo Fernandes Tedeschi'
)
__license__ = "GPL v3"
__version__ = "1.0"


# Receiver UDP port
RCV_PORT = 9002

TIPO_DADO = 0b0101010101010101
TIPO_NOME = 0b0000000011111111
TIPO_ACK = 0b1010101010101010
TIPO_EOF = 0b1111111100000000
MSS = 2000
TIMEOUT = 5
HEADER_LEN = 10  # Tamanho do cabecalho = num_seq(4) + checksum(4) + tipo(2)


# Struct para pacotes
Pacote = namedtuple("Pacote", ["num_seq", "chksum", "tipo", "data"])


# Checksum com CRC32.
# Retornar unsigned int de 32 bits gasta metade do espaço de uma string em hex
def crc32(data):
    buf = (binascii.crc32(data) & 0xFFFFFFFF)
    return buf


# Cria *uma lista* de pacotes (tuplas) para serem enviados
# O arquivo é dividido em vários pacotes de tamanho "MSS - HEADER_LEN"
# A função `min` é utilizada para quando último pacote for menor que esse valor
def cria_pacotes(dados, tipo=TIPO_DADO):
    num = 0
    pacotes = []
    enviados = 0
    a_enviar = min(MSS - HEADER_LEN, len(dados) - enviados)

    while a_enviar > 0:
        data = dados[enviados:enviados + a_enviar]
        pacotes.append(Pacote(
            num_seq=num,  # Número de sequência
            chksum=crc32(data),  # Checksum
            tipo=tipo,  # DADO ou ACK em 16 bits
            data=data))  # (MSS - HEADER_LEN) bytes de dados
        enviados += a_enviar
        a_enviar = min(MSS - HEADER_LEN, len(dados) - enviados)
        num += 1

    return pacotes


# Converte bytes para tupla pacote
def processa_pacote(dado):
    pkt = Pacote._make(unpack('IIH' + str(len(dado) - HEADER_LEN) + 's', dado))
    return pkt


# Envia pacote ACK
def envia_ack(sock, num_seq, host, porta):
    ack_pkt = Pacote(num_seq=num_seq, chksum=0, tipo=TIPO_ACK, data='')
    envia_um_pacote(sock, ack_pkt, host, porta)


# Envia um pacote pelo socket
def envia_um_pacote(sock, pkt, host, porta):
    dado = pack('IIH' + str(len(pkt.data)) + 's', pkt.num_seq, pkt.chksum, pkt.tipo, pkt.data)
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
            # Se a janela estiver cheia, ela espera os acks para esvaziar a janela.
            # Espera pelos acks timeout segundos
            pronto = select.select([sock], [], [], TIMEOUT)
            if pronto[0]:
                dado, addr = sock.recvfrom(MSS)
            # Janela cheia e nenhum ACK recebido antes de timeout
            else:
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
    # envia_um_pacote(cria_pacotes('', tipo=TIPO_EOF))
    



# Funcao para receber dados
def recebe_dados(sock, host, porta):
    pkt = Pacote(num_seq=0, chksum=0, tipo=0, data='')
    dados = ''

    while (pkt.tipo != TIPO_EOF):
        data, addr = sock.recvfrom(MSS)
        pkt = processa_pacote(data)

        print("received: {}".format(pkt))
        print("\n")

        if pkt.tipo != TIPO_ACK:
            continue
        else:
            print("Ack received") 

        cksum = crc32(pkt.data)
        if (pkt.chksum == cksum):
            envia_ack(sock, pkt.num_seq, host, porta)
            dados += pkt.data

    return dados
