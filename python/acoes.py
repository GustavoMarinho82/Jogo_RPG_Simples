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
    
    magias_debloqueadas = [magia if (var.magias[magia]["Desbloqueada"]) else "?" for magia in var.magias.keys() ]

    print(f" {'_'*105} ")
    print("| {:^29} | {:^39} | {:^29} |".format("STATUS", "ITENS EQUIPADOS", "MAGIAS CONHECIDAS"))
    print(f"|{'='*31}|{'='*41}|{'='*31}|")
    print("| {:<13} | {:<13} | {:<39} | {:^29} |".format(texto_vida, texto_dano, texto_arma, magias_debloqueadas[0]))
    print("| {:<13} | {:<13} | {:<39} | {:^29} |".format(texto_mana, texto_defesa, texto_armadura, magias_debloqueadas[1]))
    print("| {:<29} | {:<39} | {:^29} |".format(texto_local, texto_anel, magias_debloqueadas[2]))
    print(f"|{'_'*31}|{'_'*41}|{'_'*31}|")


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


def atacar(inimigo):
    vida_inimigo = var.inimigos[inimigo]["Vida"]
    turno = 1

    while (var.jogador["Vida"] > 0):
        funcao.limpar_terminal()
        
        texto = []
        texto.append(" MODO DE BATALHA - Turno {:>02}".format(turno))
        texto.append(f"{'='*28}")
        texto.append(" Vida: {:>03}/100".format(var.jogador["Vida"]))
        texto.append(" Mana: {:>03}/{:<03}".format(var.jogador["Mana"], var.jogador["Max Mana"]))
        texto.append(f"{'='*28}")
        texto.append(" Possíveis ações:")
        texto.append("  (1): Bater com sua arma")
        texto.append("  (2): Usar magia")
        texto.append("  (3): Canalizar mana")
        texto.append("  (4): Abrir inventário")

        print(f" {'_'*28} ")

        for linha in texto:
            print(f"|{linha:<28}|")

        print(f"|{'_'*28}|")

        numero_acao = input("\nRealize uma digitando seu respectivo número: ")
        
        funcao.limpar_terminal()
        
        match numero_acao:
            case "1":
                arma = var.itens[var.equipamentos["Arma"]]["Nome"]
                dano_dado = var.itens[var.equipamentos["Arma"]]["Efeito"] + (2 if (var.equipamentos["Anel"] == 15) else 0)
                vida_inimigo -= dano_dado
                
                funcao.print_lento(f"Você atacou {inimigo} com {arma}")
                funcao.print_lento(f"{inimigo} recebeu {dano_dado} de dano")
                
                funcao.enter_para_continuar()
                
                
            case "2":
                
                    nomes_magias = [magia for magia in var.magias.keys() if (var.magias[magia]["Desbloqueada"])]
                    
                    if (len(nomes_magias) == 0):
                        funcao.print_lento("Você ainda não conhece nenhuma magia...")
                        
                        funcao.enter_para_continuar()
                        
                        continue
                    
                    else:
                        while (True):
                            print("Qual magia você deseja usar?")
                            
                            for n_magia in [n+1 for n in range(len(nomes_magias))]:
                                nome_magia = nomes_magias[n_magia-1]
                                custo_magia = var.magias[nome_magia]["Custo"]
                                
                                print(" ({}): {} ({} de mana)".format(n_magia, nome_magia, custo_magia))
                                
                            escolha = input("\nDigite o seu respectivo número ou 'Sair' para voltar: ")
                            
                            funcao.limpar_terminal()
                            
                            match(escolha.casefold()):
                                case "1": magia_usada = nomes_magias[0]
                                    
                                case "2" if (len(nomes_magias) > 1): magia_usada = nomes_magias[1]
                                
                                case "3" if (len(nomes_magias) > 2): magia_usada = nomes_magias[2]
                                
                                case "sair" | "s": break
                                    
                                case _:
                                    print("Magia inválida!")
                                    continue
                            
                            
                            if (var.magias[magia_usada]["Custo"] > var.jogador["Mana"]):
                                print("Não foi possível usar a magia por falta de mana!")
                                
                                funcao.enter_para_continuar()
                                
                                continue
                                
                            else:
                                var.jogador["Mana"] -= var.magias[magia_usada]["Custo"]
                                dano_dado = var.magias[magia_usada]["Dano"]
                                vida_inimigo -= dano_dado
                                
                                funcao.print_lento(f"Você usou: {magia_usada}!")
                                funcao.print_lento(f"{inimigo} recebeu {dano_dado} de dano")
                                
                                funcao.enter_para_continuar()

                            break
                        
                        
            case "3":
                var.jogador["Mana"] = min(var.jogador["Mana"] + int(0.25*var.jogador["Max Mana"]), var.jogador["Max Mana"])
                
                funcao.print_lento("Você está canalizando a sua mana...")
                funcao.print_lento("Parte da sua mana foi recuperada!")
                
                funcao.enter_para_continuar()


            case "4": 
                abrir_inventario()
                continue


            case _:
               print('Ação inválida!') 
               funcao.enter_para_continuar()
               continue
        
        
        if (vida_inimigo <= 0):
            break
        
        dano_recebido = var.inimigos[inimigo]["Dano"] - var.itens[var.equipamentos["Armadura"]]["Efeito"] - (2 if (var.equipamentos["Anel"] == 16) else 0)
        var.jogador["Vida"] -= dano_recebido
        
        funcao.print_lento(f"{inimigo} te ataca!")
        funcao.print_lento(f"Você recebeu {dano_recebido} de dano")
        
        funcao.enter_para_continuar()
        
        
        # O turno vira "??", antes de virar um número de 3 algarismos. Pra caixa do modo de batalha não ficar estranha
        turno = (turno + 1) if (turno not in [99, "??"]) else "??"
    
    if (vida_inimigo <= 0):
        funcao.print_lento(f"Parabéns! {inimigo} foi derrotado!")
        
        drop = var.inimigos[inimigo]["Drop"]
        
        if (drop != ""):
            funcao.print_lento(f"{inimigo} dropou {drop}")
            funcao.adicionar_item(drop, 1)
        
        funcao.print_lento("Agora você pode continuar a sua aventura")
        
        funcao.indisponiblizar_interacao(var.inimigos[inimigo]["Ação"])
        
    else:
        funcao.print_lento("Sua vida chegou à zero, você morreu...")
        funcao.print_lento("Você misteriosamente se encontra no início do castelo")
        
        var.jogador["Vida"] = 100
        var.jogador["Localizacao"] = [0,0]
        
        
    funcao.enter_para_continuar()
        

def realizar_interacao(interacao):
    match interacao:
        case "Pegar Armadura de Couro do esqueleto":
            atacar("Esqueleto")
            

        case "Pegar Escritura":
            # desbloqueia magia
            pass

        case _ if ("Pegar" in interacao):
            item = interacao.replace("Pegar ", "")

            funcao.adicionar_item(item, 1)
            funcao.indisponiblizar_interacao(interacao)

            funcao.print_lento("Você obteve:", item)
            funcao.enter_para_continuar()