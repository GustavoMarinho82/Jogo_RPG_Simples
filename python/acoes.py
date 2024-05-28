# ARQUIVO DE AÇÕES

import python.variaveis as var
import python.funcoes as funcao


def movimentar():
    print("Deseja se movimentar para onde?")
    print("Possíveis movimentos: ", end="")
    
    # pos_mov -> possíveis movimentos
    pos_mov = "Norte - Sul - Leste - Oeste"

    x, y = var.jogador[0]


    if (x == 0): pos_mov = pos_mov.replace("Norte - ", "")

    elif (x == 4): pos_mov = pos_mov.replace("Sul - ", "")

    if (y == 0): pos_mov = pos_mov.replace(" - Oeste", "")

    elif (y == 4): pos_mov = pos_mov.replace("Leste - ", "")

    print(pos_mov)
    

    while (True):
        movimento = input().casefold()

        match movimento:
            case _ if (movimento not in pos_mov.casefold().split(" - ")):
                print("Movimento inválido! Digite um dos possíveis movimentos:", pos_mov)
                continue
            
            case "norte": var.jogador[0][0] -= 1

            case "sul": var.jogador[0][0] += 1

            case "leste": var.jogador[0][1] += 1

            case "oeste": var.jogador[0][1] -= 1

        break
    
    x, y = var.jogador[0]

    funcao.descobrir_sala((x, y))
    print("Você foi para:", var.castelo[x][y])

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
    x, y = var.jogador[0]
    nome_sala = funcao.obter_nome_sala((x, y))

    print(var.textos_observacao[x][y])

    for interacao in var.interacoes[nome_sala]:
        # Confere se a interação não está na lista das já desbloqueadas e nem da das indisponíveis
        if (interacao not in (var.interacoes_desbloqueadas + var.interacoes_indisponiveis)):
            funcao.desbloquear_interacao(interacao, nome_sala)

    funcao.enter_para_continuar()



#def realizar_acao(nome_acao):

#def abrir_inventário():

#def usar_item():

#def atacar():