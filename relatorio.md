# Relatório


## Descrição do projeto

O objetivo deste projeto é usar sockets UDP e implementar um protocolo confiável de transferência de dados.


## Descrição da Implementação

O projeto foi implementado em Python. Optamos por implementar o protocolo go-back-N, o qual consiste no envio de um determinado número de pacotes sem que os anteriores tenham sido reconhecidos. É definido um número de pacotes que podem ser enviados sem que seja necessário aguardar pelo reconhecimento de cada um deles. Esta quantidade de pacotes pode ser vista como a "janela". Utilizamos da seguinte animação para auxílio: http://www.ccs-labs.org/teaching/rn/animations/gbn_sr/.

Nosso projeto se dividiu em 3 códigos:

### receiver.py

Responsável por enviar o nome do arquivo desejado e caso este exista no sender.py, recebe o arquivo em pacotes e quando tiver todo o dado recebido na memória, o escreve em um arquivo.


### sender.py

Fica no aguardo de solicitações na porta especificada. Ao receber um nome de arquivo, verifica se este existe na pasta do projeto. Se existir, envia ao receiver.py.

### util.py

É aqui onde todas as nossas funções foram implementadas.
A seguir será explicado as funções e sub-funções mais importantes! 

Temos duas macro funções que chamam funções menores:

####envia_dados(dados, tipo, sock, host, porta, window, pc, verbose): 

Chama a função (1) e depois a função (5) no receiver.py

(1) envia_pacotes(...): responsável por implementar o envio de pacotes a partir do go-back-n. Primeiramente ela chama a função (2) e em seguida analisa a janela e verifica se é possível enviar um pacote, se for possível chama a função (3), logo depois fica no aguardo de acks dos pacotes que enviou e também trata acks que não foram recebidos.

(2) cria_pacotes(...): responsável por pegar o arquivo quebrá-lo em uma lista de pacotes (tuplas), inserindo também o cabeçalho (número de sequencia, checksum, tipo, dado) para ser enviado.

(3) envia_um_pacote(...): responsável por chamar a função (4) o pacote a partir da probabilidade desejada e enviar o pacote ao receiver.py.

(4)corrompe_pacote(...): a partir da probabilidade inserida, faz um random e se este for menor que a probabilidade, inverte o dado do pacote.

(5) envia_sem_dados(...): responsável apenas por enviar o fim do arquivo em um pacote só com cabeçalho.

####recebe_dados(...):

Responsável por receber pacotes no receiver.py. Trata os pacotes recebidos através da retirada do cabeçalho na função (6) e em seguida faz a checagem do checksum, verificando se houve corrompimento do pacote. Se checksum ok, aceita pacote e volta ack, através da chamada da função (7), para o sender.py 

(6) processa_pacote(...): Retira o cabeçalho do pacote recebido

(7) envia_ack(...): monta pacote com numero de sequencia a ser confirmado, checksum=0, tipo ack e sem dado.

## Alunos

*   [Christian Rollmann (414514)](https://github.com/christianroll)
*   [Isaac Mitsuaki Saito (344320)](https://github.com/zacmks)
*   [Julio Batista Silva (351202)](https://github.com/jbsilva)
*   [Marcelo Fernandes Tedeschi (414450)](https://github.com/marcelotedeschi)
