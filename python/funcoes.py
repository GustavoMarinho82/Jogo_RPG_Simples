from os import system, name as sysname
from sys import stdout
from time import sleep
import python.variaveis as var


def limpar_terminal():
    match sysname:
        case "nt": system("cls")
        case _: system("clear")

        
def print_lento(texto):
    for letra in texto:
        print(letra, end="")
        stdout.flush()
        sleep(0.05 if (var.texto_lento_ativado) else 0)

    print("")


def enter_para_continuar():
    sleep(1)
    input("(Pressione 'Enter' para continuar)")
    limpar_terminal()


def obter_coordenadas(sala):
    for x in range(5):
        if sala in var.castelo[x]:
            y = var.castelo[x].index(sala)
            return (x, y)


def descobrir_sala(coordenadas):
    x, y = coordenadas
    var.salas_descobertas[x][y] = True


def disponiblizar_interacao(interacao):
    if (interacao in var.interacoes_indisponiveis):
        var.interacoes_indisponiveis.remove(interacao)


def indisponiblizar_interacao(interacao):
    var.interacoes_indisponiveis.append(interacao)
    var.interacoes_desbloqueadas.remove(interacao)


def desbloquear_interacao(interacao):
    var.interacoes_desbloqueadas.append(interacao)


def organizar_inventario():
    ids_itens = list(var.inventario.keys())
    ids_itens.sort()
    inventario_organizado = {}

    for id_item in ids_itens:
        inventario_organizado[id_item] = var.inventario[id_item]
    
    var.inventario = inventario_organizado
 

def adicionar_item(item, quantidade):
    for id_item in var.itens.keys():
        if (var.itens[id_item]["Nome"] == item):
            if (id_item in var.inventario.keys()):
                var.inventario[id_item] += quantidade
        
            else:
                var.inventario[id_item] = quantidade
            
            break


def subtrair_item(item, quantidade):
    for id_item in var.itens.keys():
        if (var.itens[id_item]["Nome"] == item):
            var.inventario[id_item] -= quantidade

            break


def tela_de_inicio():
    while (True):
        print(var.boas_vindas)
        print("(1): Iniciar jogo")
        print("(2): Carregar jogo já salvo")
        print("(3):", "Desativar" if (var.texto_lento_ativado) else "Ativar", "textos lentos")
        
        opcao = input("O que você deseja fazer (Digite o número correspondente): ")

        match opcao:
            case "1":
                escolha = input("Você deseja ver o texto de início? (Sim/Não): ")
                
                match escolha.casefold():
                    case "sim" | "s":
                        limpar_terminal()
                        print_lento(var.texto_de_inicio)
                        sleep(1)
                        input("(Pressione 'Enter' para iniciar a sua aventura)")

            case "2": continue #Não implementado ainda

            case "3": 
                var.texto_lento_ativado = False if (var.texto_lento_ativado) else True
                limpar_terminal()
                continue

            case _: 
                limpar_terminal()
                continue

        limpar_terminal()
        break


# Printa as outras ações possíveis e retorna um trecho de código para o exec() no match de escolher uma ação
def outras_acoes():
    x, y = var.jogador["Localizacao"]
    nome_sala = var.castelo[x][y]
    
    if (nome_sala in var.interacoes.keys()):
        case_outras_acoes = "match numero_acao: \n\t" 
        numero_acao = 5

        for interacao in var.interacoes[nome_sala]:
            if (interacao in var.interacoes_desbloqueadas):
                print(f" ({numero_acao}): {interacao}")
                case_outras_acoes += f"case '{numero_acao}': acao.realizar_acao('{interacao}') \n\t"
                numero_acao += 1

        case_outras_acoes += "case _: \n\t\tprint('Ação inválida') \n\t\tfuncao.enter_para_continuar()"
        
        return case_outras_acoes
    
    else:
        return "print('Ação inválida') \nfuncao.enter_para_continuar()"