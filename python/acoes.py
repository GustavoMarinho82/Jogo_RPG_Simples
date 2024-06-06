import python.variaveis as var
import python.funcoes as funcao


def movimentar():
    print("Deseja se movimentar para onde?")
    print("Possíveis movimentos: ", end="")
    
    # pos_mov -> possíveis movimentos
    pos_mov = []

    x, y = var.jogador["Localizacao"]


    if (x != 0): pos_mov.append("Norte")

    if (x != 4): pos_mov.append("Sul")

    if (y != 0): pos_mov.append("Oeste")

    if (y != 4): pos_mov.append("Leste")

    funcao.print_lento(", ".join(pos_mov))
    

    while (True):
        movimento = input().casefold()

        match movimento:
            case _ if (movimento not in [mov.casefold() for mov in pos_mov]):
                print("Movimento inválido! Digite um dos possíveis movimentos:", ", ".join(pos_mov))
                continue
            
            case "norte": var.jogador["Localizacao"][0] -= 1

            case "sul": var.jogador["Localizacao"][0] += 1

            case "leste": var.jogador["Localizacao"][1] += 1

            case "oeste": var.jogador["Localizacao"][1] -= 1

        break
    
    x, y = var.jogador["Localizacao"]

    funcao.descobrir_sala((x, y))
    funcao.print_lento("Você foi para: "+ var.castelo[x][y])

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
    x, y = var.jogador["Localizacao"]
    nome_sala = var.castelo[x][y]
    desbloqueadas = [] #desbloqueadas -> interações desbloqueadas nessa observação

    funcao.print_lento(var.textos_observacao[nome_sala])

    if (nome_sala in var.interacoes.keys()):
        for interacao in var.interacoes[nome_sala]:
            # Confere se a interação não está na lista das já desbloqueadas e nem da das indisponíveis
            if (interacao not in (var.interacoes_desbloqueadas + var.interacoes_indisponiveis)):
                funcao.desbloquear_interacao(interacao)
                desbloqueadas.append(interacao)


        if (len(desbloqueadas) == 1):
            funcao.print_lento("\nNova interação desbloqueada: " + desbloqueadas[0])

        elif (desbloqueadas):
            funcao.print_lento("\nNovas interações desbloqueadas: " + ", ".join(desbloqueadas))


    funcao.enter_para_continuar()


#def usar_item(id_item):


def abrir_inventario():
    funcao.limpar_terminal()
    funcao.organizar_inventario()

    # STATUS E ITENS EQUIPADOS
    _, vida, mana, max_mana = var.jogador.values()

    id_arma = var.equipamentos["Arma"]
    id_armadura = var.equipamentos["Armadura"]
    id_anel = var.equipamentos["Anel"]

    dano = var.itens[id_arma]["Efeito"] if (id_arma not in [27, 28, 29]) else 0
    defesa = var.itens[id_armadura]["Efeito"]
    arma = var.itens[id_arma]["Nome"]
    armadura = var.itens[id_armadura]["Nome"]
    anel = var.itens[id_anel]["Nome"]

    texto_vida = "Vida: {:>03}/100".format(vida)
    texto_mana = "Mana: {:>03}/{:<03}".format(mana, max_mana)
    texto_dano = f"Dano: {dano}"
    texto_defesa =  f"Defesa: {defesa}"
    texto_arma = f"Arma: {arma}"
    texto_armadura = f"Armadura: {armadura}"
    texto_anel = f"Anel: {anel}"

    print(f" {'_'*70} ")
    print("| {:^29} | {:^36} |".format("STATUS", "ITENS EQUIPADOS"))
    print(f"|{'='*31}|{'='*38}|")
    print("| {:<13} | {:<13} | {:<36} |".format(texto_vida, texto_dano, texto_arma))
    print("| {:<13} | {:<13} | {:<36} |".format(texto_mana, texto_defesa, texto_armadura))
    print("| {:<13} | {:<13} | {:<36} |".format("", "", texto_anel))
    print(f"|{'_'*15}|{'_'*15}|{'_'*38}|")


    # INVENTÁRIO
    print(f" {'_'*43} ")
    print("| {:<02} | {:<30} |{:^5}|".format("ID", "NOME DO ITEM", "QTD"))
    print(f"|{'='*4}|{'='*32}|{'='*5}|")
    
    for id_item, quantidade in var.inventario.items():
        nome = var.itens[id_item]["Nome"]

        print("| {:>02} | {:<30} |{:^5}|".format(id_item, nome, quantidade))

    print(f"|{'_'*4}|{'_'*32}|{'_'*5}|")

    funcao.enter_para_continuar()


#def atacar():


def realizar_acao(acao):
    match acao:
        case "Pegar Armadura de Couro do esqueleto":
            # atacar(esqueleto)
            pass

        case "Pegar Escritura":
            # desbloqueia magia
            pass

        case _ if ("Pegar" in acao):
            item = acao.replace("Pegar ", "")

            funcao.adicionar_item(item, 1)
            funcao.indisponiblizar_interacao(acao)

            funcao.print_lento("Você obteve:", item)
            funcao.enter_para_continuar()