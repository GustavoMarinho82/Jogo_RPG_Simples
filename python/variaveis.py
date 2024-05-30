from io import open


# jogador = {"Local": [linha_do_castelo, coluna_do_castelo], ...}
jogador = {"Local": [0, 0], "Vida": 100}


# itens = {ID}
itens = {0: ()}


# inventário = {"ID do Item": Quantidade, ...}
inventário = {0: 3}


# equipamento -> [0: Arma, 1: Armadura, 2: Anel] (itens equipados pelo jogador)
equipamentos = [0, 0 ,0]


# catelo -> [linha de salas][sala] | [0][0] -> "Início"
castelo = (["Início", "Estábulos", "Tribunal", "Corredor Estreito", "Sala do Tesouro?"], ["Pátio", "Sala Aberta", "Armazém", "Biblioteca", "Aposentos"], ["Ponte Acidentada", "Capela", "Cozinha Real", "Sala do Trono", "Guardas Reais"], ["Jardim", "Refeitório", "QG", "Armaria", "Quarto do Rei"], ["Torre de Vigia", "Guarita", "Masmorra", "Torre do Mago", "Sala do Tesouro"])


# salas_descobertas -> usada para indicar quais salas já foram descobertas pelo jogador. Cada coordenada representa a sala com a mesma coordenada em castelo
salas_descobertas = [[False for _ in range(5)] for _ in range(5)]
salas_descobertas[0][0] = True


textos_observacao = [[f"Texto obs {x} {y}" for x in range(5)] for y in range(5)]
textos_observacao[0][0] = "Você observa o início e decide rezar antes de adentrar no castelo"


# interacoes_desbloqueadas -> interações que podem ser realizadas | interacoes_indisponiveis -> interações que não podem ser desbloqueadas
interacoes = {"Início": ("Rezar", "Encarar o nada")}
interacoes_desbloqueadas = []
interacoes_indisponiveis = []

#inimigos = []

arq = open("diversos/Texto_Inicial.txt", mode="r", encoding="utf-8")
texto_de_inicio = arq.read()