from io import open


# jogador = {"Local": [linha_do_castelo, coluna_do_castelo], ...}
jogador = {"Localizacao": [0, 0], "Vida": 100, "Mana": 100, "Max Mana": 100}


# O tipo do item é baseado no seu id: 0~1-> poções | 2~10-> diversos | 11~17-> anéis | 21~29-> armas | 31~37-> armaduras
itens = {} 

with open('arquivos_variaveis/itens.txt', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(" - ")) == 4):
        id, nome, descricao, efeito = linha.split(" - ")
        itens[int(id)] = {"Nome": nome, "Descrição": descricao, "Efeito": int(efeito)}


# inventario = {"ID do Item": Quantidade, ...}
inventario = {0: 3, 1: 3, 11: 1, 21: 1, 31: 1}
"""inventario = {item: 1 for item in itens.keys()}"""


# equipamentos -> ["Arma": id_do_item, ...] (itens equipados pelo jogador)
equipamentos = {"Arma": 21, "Armadura": 31, "Anel": 11}


# castelo -> [linha de salas][sala] | [0][0] -> "Início"
castelo = (["Início", "Estábulos", "Tribunal", "Corredor Estreito", "Sala do Tesouro?"], 
           ["Pátio", "Sala Aberta", "Armazém", "Biblioteca", "Aposentos"], 
           ["Ponte Acidentada", "Capela", "Cozinha Real", "Sala do Trono", "Guardas Reais"], 
           ["Jardim", "Refeitório", "QG", "Armaria", "Quarto do Rei"], 
           ["Torre de Vigia", "Guarita", "Masmorra", "Torre do Mago", "Sala do Tesouro"])


# salas_descobertas -> usada para indicar quais salas já foram descobertas pelo jogador. Cada coordenada representa a sala com a mesma coordenada em castelo
salas_descobertas = [[True if ((x,y) == (0,0)) else False for x in range(5)] for y in range(5)]


textos_observacao = {}

with open('arquivos_variaveis/Textos_Observacao.txt', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(": ")) == 2):
        sala, texto_observacao = linha.split(": ")
        textos_observacao[sala] = texto_observacao


# interacoes_desbloqueadas -> interações que podem ser realizadas | interacoes_indisponiveis -> interações que não podem ser desbloqueadas
interacoes = {}
interacoes_desbloqueadas = []
interacoes_indisponiveis = ["Pegar Pena", "Dar vara de pesca pro Pescador", "Atacar Arqueiro", "Realizar o julgamento", "Reeabastecer poções nas fontes", "Liberar passagem secreta", "Atacar o Mago", "Furtar os itens do Mago", "Despetrificar estátuas", "Atacar Guardas"]

with open('arquivos_variaveis/acoes.txt', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(": ")) == 2):
        sala, acoes = linha.split(": ")
        acoes = acoes.split(", ")
        interacoes[sala] = list(acoes)



with open("arquivos_variaveis/Texto_Inicial.txt", mode="r", encoding="utf-8") as arq:
    texto_de_inicio = arq.read()

#inimigos = []

with open("arquivos_variaveis/Boas_Vindas.txt", mode="r", encoding="utf-8") as arq:
    boas_vindas = arq.read()


texto_lento_ativado = True