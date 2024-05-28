# ARQUIVO DE FUNÇÕES

from os import system
from time import sleep
import python.variaveis as var


def enter_para_continuar():
    sleep(1)
    input("(Pressione 'Enter' para continuar)\n")
    system("cls")


def obter_coordenadas(sala):
    for x in range(5):
        if sala in var.castelo[x]:
            y = var.castelo[x].index(sala)
            return (x, y)


def obter_nome_sala(coordenadas):
    x, y = coordenadas
    nome_sala = var.castelo[x][y]

    return nome_sala


def descobrir_sala(coordenadas):
    x, y = coordenadas
    var.salas_descobertas[x][y] = True


def desbloquear_interacao(interacao, sala_interacao):
    var.interacoes_desbloqueadas.append(interacao)

    print("Nova interação desbloqueada em {}: {}".format(sala_interacao, interacao))


def obter_outras_acoes():
    nome_sala = obter_nome_sala(var.jogador[0])
    acoes_possiveis = []

    for interacao in var.interacoes[nome_sala]:
        if (interacao in var.interacoes_desbloqueadas):
            acoes_possiveis.append(interacao)
    
    return acoes_possiveis