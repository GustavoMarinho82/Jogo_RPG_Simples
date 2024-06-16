from os import system, name as sysname
from sys import stdout
from time import sleep
import python.variaveis as var


def limpar_terminal():
    match sysname:
            case "nt": system("cls")
            case _: system("clear")

        
def print_lento(texto):
    try:
        for letra in texto:
            print(letra, end="")
            stdout.flush()
            sleep(var.texto_lento_velocidade)
            
        print("")
        
    except:
        print("(Output do texto cancelado pelo input Ctrl + c) (Não é recomendado continuar enviando esse input)")


def enter_para_continuar():
    sleep(1)
    input("(Pressione 'Enter' para continuar)")
    limpar_terminal()
        

def fechar_jogo(escolha):
    if (escolha):
        print_lento("Você tem certeza de que deseja fechar o jogo? Seu progresso será perdido.")

        if (input("Fechar o jogo? (Sim / Não): ").casefold() in ["sim", "s"]):
            var.fim_de_jogo = True
        
    else:
        var.fim_de_jogo = True
        
    limpar_terminal()
    
    
def obter_coordenadas(sala):
    for x in range(5):
        if sala in var.castelo[x]:
            y = var.castelo[x].index(sala)
            return (x, y)


def descobrir_sala(coordenadas):
    x, y = coordenadas
    var.salas_descobertas[x][y] = True


def disponibilizar_interacao(interacao):
    if (interacao in var.interacoes_indisponiveis):
        var.interacoes_indisponiveis.remove(interacao)


def indisponibilizar_interacao(interacao):
    var.interacoes_indisponiveis.append(interacao)


def desbloquear_interacao(interacao):
    disponibilizar_interacao(interacao)
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


def atualizar_max_mana():
    var.jogador["Max Mana"] = 100   
    id_arma, id_armadura, id_anel = var.equipamentos.values()

    if (id_arma in [27, 28, 29]):
        var.jogador["Max Mana"] += var.itens[id_arma]["Efeito"]
    
    if (id_armadura == 36):
        var.jogador["Max Mana"] += 25

    elif (id_armadura == 37):
        var.jogador["Max Mana"] += 45

    if (id_anel == 17):
        var.jogador["Max Mana"] += 30

    var.jogador["Mana"] = var.jogador["Max Mana"]


def tela_de_inicio():
    while (True):
        try:
            print(var.boas_vindas)
            print("(1): Iniciar jogo")
            print("(2): Fechar o jogo")
            print("(3): Alterar a velocidade dos textos lentos")
            
            
            opcao = input("O que você deseja fazer (Digite o número correspondente): ")

            limpar_terminal()
            
            match opcao:
                case "1":
                    escolha = input("Você deseja ver a introdução? (Sim / Não): ")
                    
                    match escolha.casefold():
                        case "sim" | "s":
                            limpar_terminal()
                            print_lento(var.texto_de_inicio)
                            sleep(1)
                            input("(Pressione 'Enter' para iniciar a sua aventura)")

                case "2":
                    fechar_jogo(False)
                
                case "3": 
                    while (True):
                        velocidade_anterior = var.texto_lento_velocidade
                        
                        print("(1): Rápida")
                        print("(2): Média")
                        print("(3): Lenta")
                        print("(4): Desativar textos lentos")
                        print("(5): Voltar")
                        
                        velocidade = input("Selecione uma velocidade: ")
                        
                        limpar_terminal()
                        
                        match velocidade:
                            case "1": var.texto_lento_velocidade = 0.01
                            case "2": var.texto_lento_velocidade = 0.025
                            case "3": var.texto_lento_velocidade = 0.05
                            case "4": var.texto_lento_velocidade = 0
                            case "5": break
                            case _:
                                print("Opção inválida!")
                                enter_para_continuar()
                                break
                        
                        print_lento("Essa é uma amostragem da velocidade escolhida. Você tem certeza de que deseja alterar a velocidade dos textos lentos para essa? ")
                        
                        resposta = input("(Sim / Não): ")
                        
                        if (resposta.casefold() not in ["sim", "s"]):
                            var.texto_lento_velocidade = velocidade_anterior
                            limpar_terminal()
                            continue
                            
                        break
                    
                    continue


                case _: 
                    print("Opção inválida!")
                    enter_para_continuar()
                    continue

            limpar_terminal()
            break
        
        except:
            limpar_terminal()


def encerramento():
    print_lento("Você finalmente chegou na sala do tesouro! E dessa vez é a verdadeira.")
    print_lento("Diante de seus olhos, uma vasta coleção de riquezas se revela, reluzindo sob a luz suave que penetra pelas frestas das paredes de pedra. Ouro, joias, artefatos raros e relíquias de tempos antigos preenchem a sala, espalhando um brilho encantador por todo o ambiente.")
    print_lento("Com uma sensação de triunfo e alívio, você agora é o ser mais rico de todas as terras que se tem conhecimento. A partir de agora, sua vida estará repleta de conforto e luxos, graças ao tesouro saqueado do finado rei Karyon.")
    print_lento("\nCom isso, sua jornada chega ao fim. Obrigado por jogar!")


# Printa as outras ações possíveis e retorna um trecho de código para o exec() no match de escolher uma ação
def outras_acoes():
    x, y = var.jogador["Localizacao"]
    nome_sala = var.castelo[x][y]
    
    if (nome_sala in var.interacoes.keys()):
        case_outras_acoes = "match numero_acao: \n\t" 
        numero_acao = 6

        for interacao in var.interacoes[nome_sala]:
            if (interacao in var.interacoes_desbloqueadas) and (interacao not in var.interacoes_indisponiveis):
                print(f" ({numero_acao}): {interacao}")
                case_outras_acoes += f"case '{numero_acao}': acao.realizar_interacao('{interacao}') \n\t"
                numero_acao += 1

        case_outras_acoes += "case _: \n\t\tprint('Ação inválida!') \n\t\tfuncao.enter_para_continuar()"
        
        return case_outras_acoes
    
    else:
        return "print('Ação inválida!') \nfuncao.enter_para_continuar()"