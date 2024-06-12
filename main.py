import python.funcoes as funcao
import python.acoes as acao
#import python.variaveis as var


def main():
    funcao.tela_de_inicio()

    #var.jogador["Localizacao"] = [2, 0]
    
    while (True):
        print("Possíveis ações:")
        print(" (1): Ver o mapa")
        print(" (2): Mover-se para outra sala")
        print(" (3): Abrir inventário / Ver status")
        print(" (4): Observar a sala atual")

        case_outras_acoes = funcao.outras_acoes()
        
        numero_acao = input("Realize uma digitando seu respectivo número: ")

        funcao.limpar_terminal()

        match numero_acao:
            case "1": acao.ver_mapa()
            case "2": acao.movimentar()
            case "3": acao.abrir_inventario()
            case "4": acao.observar_sala()
            case _:
                exec(case_outras_acoes)


if (__name__ == "__main__"):
    main()