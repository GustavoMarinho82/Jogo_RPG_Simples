# ARQUIVO DE FUNÇÕES

from sys import stdout
from os import system
from time import sleep
import python.variaveis as var

VELOCIDADE_TEXTO = 0.05

def print_lento(texto):
    for letra in texto:
        print(letra, end="")
        stdout.flush()
        sleep(VELOCIDADE_TEXTO)

    print("")


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


def desbloquear_interacao(interacao):
    var.interacoes_desbloqueadas.append(interacao)


def obter_outras_acoes():
    nome_sala = obter_nome_sala(var.jogador["Local"])
    acoes_possiveis = []

    for interacao in var.interacoes[nome_sala]:
        if (interacao in var.interacoes_desbloqueadas):
            acoes_possiveis.append(interacao)

    return acoes_possiveis