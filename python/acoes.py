import python.variaveis as var
import python.funcoes as funcao


def movimentar():
    try:  
        print("Deseja se movimentar para onde?")
        print("Possíveis movimentos: ", end="")
        
        # pos_mov -> possíveis movimentos
        pos_mov = []

        x_origem, y_origem = var.jogador["Localizacao"]
        x_destino, y_destino = x_origem, y_origem


        if (x_origem != 0): pos_mov.append("Norte")

        if (x_origem != 4): pos_mov.append("Sul")

        if (y_origem != 0): pos_mov.append("Oeste")

        if (y_origem != 4): pos_mov.append("Leste")


        # Movimentos inválidos que não aparecem na seleção de possíveis movimentos
        match x_origem, y_origem:
            case (3, 3) | (4, 3) | (0, 3) if (not var.passagem_secreta_descoberta) :
                pos_mov.remove("Leste")
                
            case (2, 4) if (not var.cavaleiros_reais_derrotados):
                pos_mov.remove("Sul")
                
            case (1,4):
                pos_mov.remove("Norte")
                
                
        funcao.print_lento(", ".join(pos_mov))
        
        while (True):
            movimento = input().casefold()

            match movimento:
                case _ if (movimento not in [mov.casefold() for mov in pos_mov]):
                    print("Movimento inválido! Digite um dos possíveis movimentos:", ", ".join(pos_mov))
                    continue
                
                case "norte": x_destino -= 1

                case "sul": x_destino += 1

                case "leste": y_destino += 1

                case "oeste": y_destino -= 1

            break
        
        
        if ((x_destino, y_destino) in var.mov_invalidos.keys()) and ((x_origem, y_origem) in var.mov_invalidos[(x_destino, y_destino)]):
            explicacao = var.mov_invalidos[(x_destino, y_destino)][0]
            funcao.print_lento(f"Você não consegue ir para o {movimento.capitalize()}, porque {explicacao}")
            
            var.jogador["Localizacao"] = x_origem, y_origem
            
        else:
            var.jogador["Localizacao"] = x_destino, y_destino
            
            funcao.descobrir_sala((x_destino, y_destino))
            funcao.print_lento("Você foi para: "+ var.castelo[x_destino][y_destino])

    except:
        print("Erro ao ler o input!")
    
    finally:
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
        
        funcao.indisponibilizar_interacao(var.inimigos[inimigo]["Ação"])
        
    else:
        funcao.print_lento("Sua vida chegou à zero, você morreu...")
        funcao.print_lento("Você misteriosamente se encontra no início do castelo")
        
        var.jogador["Vida"] = 100
        var.jogador["Localizacao"] = [0,0]
        
        
    funcao.enter_para_continuar()
        

def realizar_interacao(interacao):
    match interacao:
        case _ if ("Pegar Escritura de" in interacao):
            magia = interacao.replace("Pegar Escritura de ", "")
            
            var.magias[magia]["Desbloqueada"] = True
            funcao.print_lento("Você aprendeu: " + magia)
            
            funcao.indisponibilizar_interacao(interacao)
            funcao.enter_para_continuar()


        case _ if ("Pegar" in interacao):
            item = interacao.replace("Pegar ", "")

            funcao.adicionar_item(item, 1)
            funcao.print_lento("Você obteve: " + item)
            
            funcao.indisponibilizar_interacao(interacao)
            funcao.enter_para_continuar()


        case _ if "Atacar" in interacao:
            inimigo = interacao.replace("Atacar ", "")
            atacar(inimigo)
            
            
        case "Pegar Armadura de Couro do esqueleto":
            atacar("Esqueleto")
            
            
        case "Interagir com o Pescador":
            funcao.print_lento("Pescador: Oh, uai. Nem vi que tinha alguém por aqui, tava distraído olhando o azulzão do lago que um dia foi meu sustento, até minha vara de pesca quebrar e eu ter que começar a comer essa comida véia e podre do castelo.")
            funcao.print_lento("\nPescador: Já faz um tempão que nenhum vivente aparece nesse castelo abandonado. Quer dizer, aparecer, aparece, mas eles vêm é pra saquear o tesouro do nosso rei morto. Só que no fim, todo mundo que se aventura por aqui só encontra a morte. O povo que mora no interior do castelo não gosta nadinha de humanos, mas pode ficar tranquilo comigo, sou só um véio pescador que não quer briga, então nem pense em puxar sua espada pra mim.")
            funcao.print_lento("\nPescador: Eu te digo pra desistir dessa aventura sua e passar o resto da vida de boa como eu, só pescando e sentindo a brisa do vento batendo no seu chapéu de pescador. Mas se você quer mesmo se aventurar por esse castelo, recomendo ficar longe da comida da cozinha real no meio do castelo, a não ser que você esteja morrendo de fome e precise recuperar as forças.")
            
            if ("Dar Vara de Pesca pro Pescador" in var.interacoes_desbloqueadas) and ("Dar Vara de Pesca pro Pescador" in var.interacoes_indisponiveis):
                funcao.print_lento("\nPescador: Ah, tô tão feliz com minha nova vara de pesca :)")
                
            else:
                funcao.print_lento("\nPescador: Ah, como eu queria minha vara de pesca de volta...")

            if (var.salas_descobertas[2][2] == False):
                funcao.print_lento("\nNova sala descoberta: Cozinha Real")
                funcao.descobrir_sala((2, 2))
                
            funcao.enter_para_continuar()
        
        
        case "Espantar pássaro":
            funcao.print_lento("Num impulso sádico, você espanta o pobre pássaro distraído. Que ação repulsiva!")
            funcao.print_lento("Algumas penas se desprendem do pássaro e se espalham pela grama.")
            
            funcao.print_lento("\nNova ação desbloqueada: Pegar Pena")
            
            funcao.desbloquear_interacao("Pegar Pena")
            funcao.indisponibilizar_interacao("Espantar pássaro")
            
            funcao.enter_para_continuar()


        case "Dar Vara de Pesca pro Pescador":
            funcao.print_lento("Pescador: Nossa, ocê é bão demais! Agora finalmente vou poder pescar de novo. Como agradecimento, vou pescar um peixão bem bão pra ocê.")
            funcao.print_lento("\nNuma puxada bem rápida e forte, um peixe bem grande voa do mar até as sua mãos.")
            
            funcao.subtrair_item("Vara de Pesca", 1)
            funcao.adicionar_item("Peixe", 1)
            funcao.indisponibilizar_interacao("Dar Vara de Pesca pro Pescador")
            
            funcao.enter_para_continuar


        case "Inspecionar altares":
            pass
        
        case "Destrancar o acesso ao jardim":
            pass
        
        case "Acordar Arqueiro":
            pass
        
        case "Interagir com Cuidadora":
            pass
        
        case "Fazer carinho no cavalo":
            pass
        
        case "Rezar":
            pass
        
        case "Se aproximar da multidão de fantasmas":
            pass
        
        case "Interagir com o Juiz":
            pass
        
        case "Realizar o julgamento":
            pass
        
        case "Interagir com Padre":
            pass
        
        case "Reeabastecer poções nas fontes":
            pass
        
        case "Comer restos de comida":
            pass
        
        case "Checar registros de batalhas (Descobre o porque do rei morreu)":
            pass
        
        case "Vasculhar":
            match var.jogador["Localização"]:
                case _: 
                    pass
        
        case "Liberar passagem secreta":
            pass
        
        case "Checar registros sobre comandante":
            pass
        
        case "Checar registros sobre o mago":
            pass
        
        case "Checar registros sobre o rei":
            pass
        
        case "Interagir com o Velho":
            pass
        
        case "Atacar o Mago":
            pass
        
        case "Furtar os itens do Mago":
            pass
        
        case "Resolver enigma":
            pass
        
        case "Pegar Vara de Pesca":
            pass
        
        case "Inspecionar estátuas":
            pass
        
        case "Despetrificar estátuas":
            pass
