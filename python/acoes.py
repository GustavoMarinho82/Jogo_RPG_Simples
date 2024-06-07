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


# Usar/Equipar um item
def usar_item(id_item):
    match (id_item):
        #Poção de Vida
        case 0: 
            var.jogador["Vida"] = min((var.jogador["Vida"] + var.itens[id_item]["Efeito"]), 100)
            funcao.subtrair_item(var.itens[id_item]["Nome"], 1)

        #Poção de Mana
        case 1: 
            var.jogador["Mana"] = min((var.jogador["Mana"] + var.itens[id_item]["Efeito"]), var.jogador["Max Mana"])
            funcao.subtrair_item(var.itens[id_item]["Nome"], 1)

        #Anéis
        case _ if id_item in range(11, 18):
            var.equipamentos["Anel"] = id_item

        #Armas
        case _ if id_item in range(21, 30):
            var.equipamentos["Arma"] = id_item

        #Armaduras
        case _ if id_item in range(31, 38): 
            var.equipamentos["Armadura"] = id_item

    funcao.atualizar_max_mana()


def abrir_inventario():
    funcao.limpar_terminal()
    funcao.organizar_inventario()

    # STATUS E ITENS EQUIPADOS
    _, vida, mana, max_mana = var.jogador.values()
    id_arma, id_armadura, id_anel = var.equipamentos.values()

    dano = var.itens[id_arma]["Efeito"] if (id_arma not in [27, 28, 29]) else 0
    defesa = var.itens[id_armadura]["Efeito"]
    x, y = var.jogador["Localizacao"]
    arma = var.itens[id_arma]["Nome"]
    armadura = var.itens[id_armadura]["Nome"]
    anel = var.itens[id_anel]["Nome"]

    match (id_anel):
        case 15: dano += 2
        case 16: defesa += 2

    texto_vida = "Vida: {:>03}/100".format(vida)
    texto_mana = "Mana: {:>03}/{:<03}".format(mana, max_mana)
    texto_dano = f"Dano: {dano}"
    texto_defesa =  f"Defesa: {defesa}"
    texto_local = f"Local: {var.castelo[x][y]}"
    texto_arma = f"Arma: {arma}"
    texto_armadura = f"Armadura: {armadura}"
    texto_anel = f"Anel: {anel}"

    print(f" {'_'*73} ")
    print("| {:^29} | {:^39} |".format("STATUS", "ITENS EQUIPADOS"))
    print(f"|{'='*31}|{'='*41}|")
    print("| {:<13} | {:<13} | {:<39} |".format(texto_vida, texto_dano, texto_arma))
    print("| {:<13} | {:<13} | {:<39} |".format(texto_mana, texto_defesa, texto_armadura))
    print("| {:<29} | {:<39} |".format(texto_local, texto_anel))
    print(f"|{'_'*31}|{'_'*41}|")


    # INVENTÁRIO
    print(f" {'_'*44} ")
    print("| {:<02} | {:<31} |{:^5}|".format("ID", "NOME DO ITEM", "QTD"))
    print(f"|{'='*4}|{'='*33}|{'='*5}|")
    
    for id_item, quantidade in var.inventario.items():
        if (quantidade != 0):
            nome = var.itens[id_item]["Nome"]

            print("| {:>02} | {:<31} |{:^5}|".format(id_item, nome, quantidade))

    print(f"|{'_'*4}|{'_'*33}|{'_'*5}|")


    # USAR / EQUIPAR ITEM 
    try:
        item_selecionado = int(input("\nDeseja selecionar algum item? (Digite o ID do item / Não): "))
        
        funcao.limpar_terminal()

        # Confere se o id selecionado está entre os id's dos itens presentes no inventário que estão em quantidade maior que 0
        if (item_selecionado in [ids for ids, qtd in var.inventario.items() if (qtd > 0)]):
            nome = var.itens[item_selecionado]["Nome"]
            descricao = var.itens[item_selecionado]["Descrição"]
            usar = True if (item_selecionado in [0,1]) else False
                            
            funcao.print_lento(f"Nome: {nome}")
            funcao.print_lento(f"Descrição: {descricao}")

            if (item_selecionado in ([0, 1] + list(range(11, 38)))):
                resposta = input("Você deseja " + ("usar" if (usar) else "equipar") + " esse item? (Sim / Não): ")

                if (resposta.casefold() in ["sim", "s"]):
                    usar_item(item_selecionado)
                    
                    funcao.limpar_terminal()
                    funcao.print_lento("Você "+ ("usou " if (usar) else "equipou ") + nome)
                    funcao.enter_para_continuar()

            else:
                funcao.enter_para_continuar()

        else:
            funcao.print_lento("O ID do item não foi encontrado!")
            funcao.enter_para_continuar()

    # Esse try e except servem para não executar o trecho do código de usar/equipar item, caso seja inserido um 'não' ou qualquer outra string
    except:
        pass

    funcao.limpar_terminal()


#def atacar():


def realizar_interacao(interacao):
    match interacao:
        case "Pegar Armadura de Couro do esqueleto":
            # atacar(esqueleto)
            pass

        case "Pegar Escritura":
            # desbloqueia magia
            pass

        case _ if ("Pegar" in interacao):
            item = interacao.replace("Pegar ", "")

            funcao.adicionar_item(item, 1)
            funcao.indisponiblizar_interacao(interacao)

            funcao.print_lento("Você obteve:", item)
            funcao.enter_para_continuar()