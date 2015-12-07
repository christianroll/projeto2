#!/bin/bash
# O arquivo será salvo no mesmo diretorio do arquivo atual

echo -n "Digite o tamanho da janela (ex: 10): "
read cwnd
echo -n "Digite a probabilidade de perda: "
read pl
echo -n "Digite a probabilidade de corrompimento: "
read pc

echo "Iniciando sender.py e receiver.py..."
sleep 1

[[ -z $(lsof -t -i :9001) ]] || kill $(lsof -t -i :9001)
[[ -z $(lsof -t -i :9002) ]] || kill $(lsof -t -i :9002)

python sender.py $cwnd 0 $pc -p 9001 & sleep 2
python receiver.py 127.0.0.1 9001 ../LICENSE $pl 0 &

diff ../LICENSE ../LICENSE_rcvd

