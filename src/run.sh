#!/bin/bash
# O arquivo será salvo no mesmo diretorio do arquivo atual

[[ -z $(lsof -t -i :9001) ]] || kill $(lsof -t -i :9001)
[[ -z $(lsof -t -i :9002) ]] || kill $(lsof -t -i :9001)

python sender.py 10 0 0 -p 9001 &
sleep 2
python receiver.py 127.0.0.1 9001 ../LICENSE 0.4 0 &
diff ../LICENSE ../LICENSE_rcvd
