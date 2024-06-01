from io import open


# jogador = {"Local": [linha_do_castelo, coluna_do_castelo], ...}
jogador = {"Local": [0, 0], "Vida": 100}


# itens = {ID: {"Nome": x, "Descrição": y}, ...}  |  Tipos de itens: 0~1-> poções | 2~10-> diversos | 11~17-> anéis | 21~29-> armas | 31~37-> armaduras
itens = {}

arq = open('diversos/itens.txt', 'r', encoding='utf-8')
linhas = arq.readlines()

for linha in linhas:
    linha = linha.strip()

    if (linha != ""):
        id, nome, descricao = linha.split(" - ")
        itens[int(id)] = {"Nome": nome, "Descrição": descricao}

arq.close()

""" Função para checar a variável itens 
for a, b in itens.items():
    print(a, b)
"""

# inventario = {"ID do Item": Quantidade, ...}
inventario = {0: 3, 1: 3, 11: 1, 21: 1, 31: 1}


# equipamento -> [0: Arma, 1: Armadura, 2: Anel] (itens equipados pelo jogador)
equipamentos = [20, 30, 11]


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
arq.close()