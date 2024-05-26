# ARQUIVO DE FUNÇÕES

import python.variaveis as var


def buscar_coordenadas(sala):
    for x in range(5):
        if sala in var.castelo[x]:
            y = var.castelo[x].index(sala)
            return (x, y)


def descobrir_sala(coordenadas):
    x = coordenadas[0]
    y = coordenadas[1]
    var.salas_descobertas[x][y] = True


def exibir_texto_entrada(coordenadas):
    x = coordenadas[0]
    y = coordenadas[1]

    print("Você foi para:", var.castelo[x][y])

    # Se for a primeira vez que o jogador está entrando na sala, exibe o texto de entrada
    if (var.salas_descobertas[x][y] == False):
        print(var.textos_entrada[x][y])

    
# AÇÕES
def movimentar():
    print("Deseja se movimentar para onde?")
    print("Possíveis movimentos: ")
    
    # pos_mov -> possíveis movimentos
    pos_mov = "Norte - Sul - Leste - Oeste"

    (x, y) = var.jogador[0]

    if (x == 0):
        pos_mov = pos_mov.replace("Norte - ", "")

    elif (x == 4):
        pos_mov = pos_mov.replace("Sul - ", "")

    if (y == 0):
        pos_mov = pos_mov.replace(" - Oeste", "")

    elif (y == 4):
        pos_mov = pos_mov.replace("Leste - ", "")

    print(pos_mov)
    
    while (True):
        movimento = input().casefold()
        print(movimento)

        match movimento:
            case _ if (movimento not in pos_mov.casefold().split(" - ")):
                print("Movimento inválido! Digite um dos possíveis movimentos:", pos_mov)
                continue
            
            case "norte":
                var.jogador[0][0] -= 1

            case "sul":
                var.jogador[0][0] += 1

            case "leste":
                var.jogador[0][1] += 1

            case "oeste":
                var.jogador[0][1] -= 1

        break
    
    exibir_texto_entrada(var.jogador[0])
    descobrir_sala(var.jogador[0])



def ver_mapa():
    print(f"+{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}+")

    for x in range(5):
        for y in range(5):
            # Se a sala já tiver sido descoberta (indicado em salas_descobertas[coordenada da sala]), aparecerá o nome dela no mapa, senão aparecerá "?"
            sala = var.castelo[x][y] if (var.salas_descobertas[x][y]) else "?"

            print("|{:^17}".format(sala), end="")

        print("|")
        print(f"+{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}|{'-'*17}+")

#def observar_sala():
    
#def usar_item():