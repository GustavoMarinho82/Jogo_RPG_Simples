import python.funcoes as funcao
import python.acoes as acao
import python.variaveis as var


def main():
    funcao.tela_de_inicio()

    while (not var.fim_de_jogo):
        print("Possíveis ações:")
        print(" (1): Fechar jogo")
        print(" (2): Ver o mapa")
        print(" (3): Mover-se para outra sala")
        print(" (4): Abrir inventário / Ver status")
        print(" (5): Observar a sala atual")


        case_outras_acoes = funcao.outras_acoes()
        
        try:
            numero_acao = input("Realize uma digitando seu respectivo número: ")

            funcao.limpar_terminal()

            match numero_acao:
                case "1": funcao.fechar_jogo(True)
                case "2": acao.ver_mapa()
                case "3": acao.movimentar()
                case "4": acao.abrir_inventario(False)
                case "5": acao.observar_sala()
                case _:
                    exec(case_outras_acoes)
                    
        except:
            print("(Ação cancelada pelo input Ctrl + c) (Não é recomendado continuar enviando esse input)")
            funcao.enter_para_continuar()


    if (var.vitoria):
        funcao.encerramento()


if (__name__ == "__main__"):
    main()