import python.funcoes as funcao
import python.acoes as acao


def main():
    funcao.iniciar_jogo()

    while (True):
        print("Possíveis ações:")
        print(" (1): Ver o mapa")
        print(" (2): Mover-se para outra sala")
        print(" (3): Abrir inventário")
        print(" (4): Observar a sala atual")

        case_outras_acoes = funcao.outras_acoes()
        
        numero_acao = input("Realize uma digitando seu respectivo número: ")

        funcao.limpar_terminal()

        match numero_acao:
            case "1": acao.ver_mapa()
            case "2": acao.movimentar()
            case "3": print() #abrir_inventário()
            case "4": acao.observar_sala()
            case _:
                exec(case_outras_acoes)


if (__name__ == "__main__"):
    main()