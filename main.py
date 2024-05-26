# ARQUIVO PRINCIPAL

import python.variaveis as var
import python.funcoes as funcao

while True:
    x = int(input())
    if (x == 0):
        funcao.ver_mapa()
    else:

        funcao.movimentar()
        print(var.jogador[0])