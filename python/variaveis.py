from io import open


# jogador = {"Local": [linha_do_castelo, coluna_do_castelo], ...}
jogador = {"Localizacao": [0, 0], "Vida": 100, "Mana": 100, "Máximo de Mana": 100}


# itens = {id: {"Nome": x, "Descrição": y}, ...}  |  Tipos de itens: 0~1-> poções | 2~10-> diversos | 11~17-> anéis | 21~29-> armas | 31~37-> armaduras
itens = {}

arq = open('arquivos_variaveis/itens.txt', 'r', encoding='utf-8')
linhas = arq.readlines()

for linha in linhas:
    linha = linha.strip()

    if (linha != "") and (len(linha.split(" - ")) == 3):
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


# castelo -> [linha de salas][sala] | [0][0] -> "Início"
castelo = (["Início", "Estábulos", "Tribunal", "Corredor Estreito", "Sala do Tesouro?"], ["Pátio", "Sala Aberta", "Armazém", "Biblioteca", "Aposentos"], ["Ponte Acidentada", "Capela", "Cozinha Real", "Sala do Trono", "Guardas Reais"], ["Jardim", "Refeitório", "QG", "Armaria", "Quarto do Rei"], ["Torre de Vigia", "Guarita", "Masmorra", "Torre do Mago", "Sala do Tesouro"])


# salas_descobertas -> usada para indicar quais salas já foram descobertas pelo jogador. Cada coordenada representa a sala com a mesma coordenada em castelo
salas_descobertas = [[False for _ in range(5)] for _ in range(5)]
salas_descobertas[0][0] = True


textos_observacao = {}

arq = open('arquivos_variaveis/Textos_Observacao.txt', 'r', encoding='utf-8')
linhas = arq.readlines()

for linha in linhas:
    linha = linha.strip()

    if (linha != "") and (len(linha.split(": ")) == 2):
        sala, texto_observacao = linha.split(": ")
        textos_observacao[sala] = texto_observacao

arq.close()

""" Função para checar a variável textos_observacao
for a, b in textos_observacao.items():
    print(a, b)
"""


# interacoes_desbloqueadas -> interações que podem ser realizadas | interacoes_indisponiveis -> interações que não podem ser desbloqueadas
interacoes = {}
interacoes_desbloqueadas = []
interacoes_indisponiveis = ["Pegar pena", "Dar vara de pesca pro Pescador", "Atacar Arqueiro", "Realizar o julgamento", "Reeabastecer poções nas fontes", "Liberar passagem secreta", "Atacar o Mago", "Furtar os itens do Mago", "Despetrificar estátuas", "Atacar Guardas"]

arq = open('arquivos_variaveis/acoes.txt', 'r', encoding='utf-8')
linhas = arq.readlines()

for linha in linhas:
    linha = linha.strip()

    if (linha != "") and (len(linha.split(": ")) == 2):
        sala, acoes = linha.split(": ")
        acoes = acoes.split(", ")
        interacoes[sala] = list(acoes)

arq.close()

""" Função para checar a variável interacoes
for a, b in interacoes.items():
    print(a, b)
"""


#inimigos = []

arq = open("arquivos_variaveis/Texto_Inicial.txt", mode="r", encoding="utf-8")
texto_de_inicio = arq.read()
arq.close()

arq = open("arquivos_variaveis/Boas_Vindas.txt", mode="r", encoding="utf-8")
boas_vindas = arq.read()
arq.close()

texto_lento_ativado = True