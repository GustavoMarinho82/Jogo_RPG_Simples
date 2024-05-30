from sys import stdout
from os import system
from time import sleep
import python.variaveis as var


def print_lento(texto):
    for letra in texto:
        print(letra, end="")
        stdout.flush()
        sleep(0.05)

    print("")


def iniciar_jogo():
    print("Você deseja ver o texto de início? (Sim/Não)")

    match input().casefold():
        case "sim" | "s":
            system("cls")
            print_lento(var.texto_de_inicio)
            sleep(1)
            input("(Pressione 'Enter' para iniciar a sua aventura)")
    
    system("cls")


def enter_para_continuar():
    sleep(1)
    input("(Pressione 'Enter' para continuar)")
    system("cls")


def obter_coordenadas(sala):
    for x in range(5):
        if sala in var.castelo[x]:
            y = var.castelo[x].index(sala)
            return (x, y)


def descobrir_sala(coordenadas):
    x, y = coordenadas
    var.salas_descobertas[x][y] = True


def desbloquear_interacao(interacao):
    var.interacoes_desbloqueadas.append(interacao)


# Printa as outras ações possíveis e retorna um trecho de código para o exec() no match de escolher uma ação
def outras_acoes():
    x, y = var.jogador["Local"]
    nome_sala = var.castelo[x][y]
    
    case_outras_acoes = "match numero_acao: \n\t" 
    numero_acao = 5

    for interacao in var.interacoes[nome_sala]:
        if (interacao in var.interacoes_desbloqueadas):
            print(f" ({numero_acao}): {interacao}")
            case_outras_acoes += f"case '{numero_acao}': acao.realizar_acao('{interacao}') \n\t"
            numero_acao += 1

    case_outras_acoes += "case _: \n\t\tprint('Ação inválida') \n\t\tfuncao.enter_para_continuar()"
    
    return case_outras_acoes