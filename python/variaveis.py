from io import open


# jogador = {"Local": [linha_do_castelo, coluna_do_castelo], ...}
jogador = {"Localizacao": [0, 0], "Vida": 100, "Mana": 100, "Max Mana": 100}


# O tipo do item é baseado no seu id: 0~1-> poções | 2~10-> diversos | 11~17-> anéis | 21~29-> armas | 31~37-> armaduras
itens = {}

with open('arquivos_variaveis/Itens', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(" - ")) == 4):
        id, nome, descricao, efeito = linha.split(" - ")
        itens[int(id)] = {"Nome": nome, "Descrição": descricao, "Efeito": int(efeito)}


magias = {"Flecha de Luz": {"Dano": 40, "Custo": 50, "Desbloqueada": False}, "Bola de Fogo": {"Dano": 70, "Custo": 75, "Desbloqueada": False}, "Tempestade de Raios": {"Dano": 130, "Custo": 100, "Desbloqueada": False}}

# inventario = {"ID do Item": Quantidade, ...}
inventario = {0: 3, 1: 3, 11: 1, 21: 1, 31: 1}


# equipamentos -> ["Arma": id_do_item, ...] (itens equipados pelo jogador)
equipamentos = {"Arma": 21, "Armadura": 31, "Anel": 11}


# castelo -> [linha de salas][sala] | [0][0] -> "Início"
castelo = (["Início", "Estábulos", "Tribunal", "Corredor Estreito", "Sala do Tesouro?"], ["Pátio", "Sala Aberta", "Armazém", "Biblioteca", "Aposentos"], ["Ponte Acidentada", "Capela", "Cozinha Real", "Sala do Trono", "Guardas Reais"], ["Jardim", "Refeitório", "QG", "Armaria", "Quarto do Rei"], ["Torre de Vigia", "Guarita", "Masmorra", "Torre do Mago", "Sala do Tesouro"])


# salas_descobertas -> usada para indicar quais salas já foram descobertas pelo jogador. Cada coordenada representa a sala com a mesma coordenada em castelo
salas_descobertas = [[True if ((x,y) == (0,0)) else False for x in range(5)] for y in range(5)]


textos_observacao = {}

with open('arquivos_variaveis/Textos_Observacao', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(": ")) == 2):
        sala, texto_observacao = linha.split(": ")
        textos_observacao[sala] = texto_observacao


# interacoes_desbloqueadas -> interações que podem ser realizadas | interacoes_indisponiveis -> interações que não podem ser desbloqueadas
interacoes = {}
interacoes_desbloqueadas = ["Vasculhar"]
interacoes_indisponiveis = ["Pegar Pena", "Dar Vara de Pesca pro Pescador", "Atacar Arqueiro", "Pegar Anel Abençoado", "Realizar o julgamento", "Reabastecer poções nas fontes", "Ouvir a palavra de Miarli", "Liberar passagem secreta", "Atacar Mago", "Furtar os itens do Mago", "Pegar Anel do Combatente", "Pegar Clava de Bronze Enferrujada", "Analisar claymore", "Pegar Vara de Pesca", "Abrir caixinha", "Despetrificar estátuas", "Atacar Guardas Reais"]

with open('arquivos_variaveis/Interacoes', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(": ")) == 2):
        sala, acoes = linha.split(": ")
        acoes = acoes.split(", ")
        interacoes[sala] = list(acoes)


inimigos = {}

with open('arquivos_variaveis/Inimigos', 'r', encoding='utf-8') as arq:
    linhas = arq.readlines()

for linha in [linha.strip() for linha in linhas if (linha.strip() != "")]:
    if (len(linha.split(" - ")) == 5):
        nome, vida, dano, texto_ataque, drop = linha.split(" - ")
        inimigos[nome] = {"Vida": int(vida), "Dano": int(dano), "Texto Ataque": texto_ataque, "Drop": drop}


with open("arquivos_variaveis/Texto_Inicial", mode="r", encoding="utf-8") as arq:
    texto_de_inicio = arq.read()


with open("arquivos_variaveis/Boas_Vindas", mode="r", encoding="utf-8") as arq:
    boas_vindas = arq.read()


texto_lento_velocidade = 0.025


# mov_invalidos -> {destino: [texto_explicativo, origem(ns)], ...}
mov_invalidos = {(3,1): ["lá estava infestado de espíritos e você tem muito medo deles.", (3,0), (2,1), (3,2), (4,1)], (4,0): ["a porta da torre está trancada.", (3,0)], (3,0): ["a porta da torre está trancada.", (4,0)], (4,2): ["uma barreira mágica do próprio castelo te impede de entrar na masmorra. Somente guardas e prisioneiros podem passar por ela.", (4,1), (3,2), (4,3)], (1,3): ["a porta para biblioteca está trancada.", (0,3), (2,3), (1,2), (1,4)], (4,3): ["uma barreira protetora envolve a entrada para a torre do mago. Mas quem está mantendo essa barreira?", (4,2), (3,3)], (0,3): ["você não consegue abrir porta, parece que você está preso aqui.", (0,4)], (4,4): ["a porta está trancada, você vai precisar de uma chave para abrí-la.", (3,4)]}


# Variáveis do enigma do tribunal
arma_crime_descoberta = False
local_crime_descoberto = False
motivo_crime_descoberto = False
assassino_descoberto = False


guarda_sem_nome_derrotado = False
arqueiro_nos_estabulos = False
passagem_secreta_descoberta = False
guardas_reais_derrotados = False


fim_de_jogo = False
vitoria = False