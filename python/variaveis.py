# ARQUIVO DE VARIÁVEIS

# jogador = [localização, vida]
jogador = [[0, 0], 100]

# itens = {ID}
itens = {0: ()}

# inventário = {"ID do Item": Quantidade, ...}
inventário = {0: 3}

# equipamento -> [0: Arma, 1: Armadura, 2: Anel] 
# (equipamentos equipados pelo jogador)
equipamentos = [0, 0 ,0]

# catelo -> [linha de salas][sala] | [0][0] -> "Início"
castelo = (["Início", "Estábulos", "Tribunal", "Corredor Estreito", "Sala do Tesouro?"], ["Pátio", "Sala Aberta", "Armazém", "Biblioteca", "Aposentos"], ["Ponte Acidentada", "Capela", "Cozinha Real", "Sala do Trono", "Guardas Reais"], ["Jardim", "Refeitório", "QG", "Armaria", "Quarto do Rei"], ["Torre de Vigia", "Guarita", "Masmorra", "Torre do Mago", "Sala do Tesouro"])

# salas_descobertas -> usada para indicar quais salas já foram descobertas pelo jogador. Cada coordenada representa a sala com a mesma coordenada em castelo
salas_descobertas = [[False for _ in range(5)] for _ in range(5)]
salas_descobertas[0][0] = True

# textos_entrada
textos_entrada = [["Texto entrada" for _ in range(5)] for _ in range(5)]

inimigos = []

texto_de_inicio = ""