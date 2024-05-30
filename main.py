# ARQUIVO PRINCIPAL

from os import system
#from time import sleep
#import python.variaveis as var
import python.funcoes as funcao
import python.acoes as acao

while (True):
    print("Possíveis ações:")
    print(" (1): Ver o mapa")
    print(" (2): Mover-se para outra sala")
    print(" (3): Abrir inventário")
    print(" (4): Observar a sala atual")

    '''outras_acoes = funcao.obter_outras_acoes()

    for i in range(len(outras_acoes)):
            print(f" ({i+5}): {outras_acoes[i]}") '''

    numero_acao = input("Realize uma digitando seu respectivo número: ")

    system("cls")

    match numero_acao:
        case "1": acao.ver_mapa()
        case "2": acao.movimentar()
        case "3": print() #abrir_inventário()
        case "4": acao.observar_sala()

        # case (i+5): realizar_acao(acao[i])
        
        case _: 
            print("Ação inválida")
            funcao.enter_para_continuar()