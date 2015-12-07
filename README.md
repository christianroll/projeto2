# Redes de Computadores: Projeto 2 - Transferência Confiável de Dados Baseada em Janela com Repetição Seletiva ou Go-Back-N

Professor [Cesar Marcondes](https://github.com/cmarcond) - [DC UFSCar](http://www.dc.ufscar.br/)


## Descrição do projeto

Descrição completa em [Projeto_02-description.pdf](docs/Projeto_02-description.pdf)


## Requerimentos

*   [Python 2.7](https://www.python.org/)

## Instruções

Rodar no modo manual entrando com os parâmetros pelo terminal:

Em duas abas distintas no terminal rodar:

Programa sender.py:

    $ python sender.py <cwnd> <PL> <PC> -p <porta do sender>

Programa receiver.py:

    $ python receiver.py <localhost> <porta do sender> <nome do arquivo> <PL> <PC>

ou

Rodar no modo automático:
Basta executar o arquivo run.sh no terminal.

## Alunos

*   [Christian Rollmann (414514)](https://github.com/christianroll)
*   [Isaac Mitsuaki Saito (344320)](https://github.com/zacmks)
*   [Julio Batista Silva (351202)](https://github.com/jbsilva)
*   [Marcelo Fernandes Tedeschi (414450)](https://github.com/marcelotedeschi)
