# ARQUIVO DE AÇÕES

import python.variaveis as var
import python.funcoes as funcao


def movimentar():
    print("Deseja se movimentar para onde?")
    print("Possíveis movimentos: ", end="")
    
    # pos_mov -> possíveis movimentos
    pos_mov = []

    x, y = var.jogador["Local"]


    if (x != 0): pos_mov.append("Norte")

    elif (x != 4): pos_mov.append("Sul")

    if (y != 0): pos_mov.append("Oeste")

    elif (y != 4): pos_mov.append("Leste")

    funcao.print_lento(", ".join(pos_mov))
    

    while (True):
        movimento = input().casefold()

        match movimento:
            case _ if (movimento not in [mov.casefold() for mov in pos_mov]):
                print("Movimento inválido! Digite um dos possíveis movimentos:", ", ".join(pos_mov))
                continue
            
            case "norte": var.jogador["Local"][0] -= 1

            case "sul": var.jogador["Local"][0] += 1

            case "leste": var.jogador["Local"][1] += 1

            case "oeste": var.jogador["Local"][1] -= 1

        break
    
    x, y = var.jogador["Local"]

    funcao.descobrir_sala((x, y))
    funcao.print_lento("Você foi para: "+ var.castelo[x][y])

    funcao.enter_para_continuar()


def ver_mapa():
    print(f"+{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}+")

    for x in range(5):
        for y in range(5):
            # Se a sala já tiver sido descoberta (indicado em salas_descobertas[coordenada da sala]), aparecerá o nome dela no mapa, senão aparecerá "?"
            sala = var.castelo[x][y] if (var.salas_descobertas[x][y]) else "?"

            print("|{:^17}".format(sala), end="")

        print("|")
        print(f"+{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}+")

    funcao.enter_para_continuar()


def observar_sala():
    x, y = var.jogador["Local"]
    nome_sala = funcao.obter_nome_sala((x, y))
    desbloqueadas = [] #desbloqueadas -> interações desbloqueadas nessa observação

    funcao.print_lento(var.textos_observacao[x][y])


    for interacao in var.interacoes[nome_sala]:
        # Confere se a interação não está na lista das já desbloqueadas e nem da das indisponíveis
        if (interacao not in (var.interacoes_desbloqueadas + var.interacoes_indisponiveis)):
            funcao.desbloquear_interacao(interacao)
            desbloqueadas.append(interacao)


    if (len(desbloqueadas) == 1):
        funcao.print_lento("Nova interação desbloqueada: " + desbloqueadas[0])

    elif (desbloqueadas):
        funcao.print_lento("Novas interações desbloqueadas: " + ", ".join(desbloqueadas))


    funcao.enter_para_continuar()



#def realizar_acao(nome_acao):

#def abrir_inventário():

#def usar_item():

#def atacar():