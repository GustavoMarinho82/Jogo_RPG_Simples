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
            case (4, 1) if (not var.guarda_sem_nome_derrotado):
                pos_mov.remove("Oeste")
                
            case (3, 3) | (4, 3):
                pos_mov.remove("Leste")
                
            case (0, 3) if (not var.passagem_secreta_descoberta):
                pos_mov.remove("Leste")
                
            case (2,0) | (0,4):
                pos_mov.remove("Sul")
                
            case (2, 4) if (not var.guardas_reais_derrotados):
                pos_mov.remove("Sul")
                
            case (3,0) | (1,4):
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
            funcao.limpar_terminal()
            funcao.print_lento(f"Você não consegue ir para o {movimento}, porque {explicacao}")
            
            var.jogador["Localizacao"] = x_origem, y_origem
                
        elif ((x_destino, y_destino) == (4,4)):
                var.fim_de_jogo = True
                var.vitoria = True
        
        else:
            var.jogador["Localizacao"] = x_destino, y_destino
            
            funcao.descobrir_sala((x_destino, y_destino))
            funcao.print_lento("Você foi para: "+ var.castelo[x_destino][y_destino])

    except:
        print("Movimento cancelado!")

    
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

        if (nome_sala == "Ponte acidentada"):
            funcao.descobrir_sala((3,0))
            funcao.descobrir_sala((4,0))
        
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


def abrir_inventario(em_batalha):
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
        case 15: dano += var.itens[15]["Efeito"]
        case 16: defesa += var.itens[16]["Efeito"]

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

            if (item_selecionado in ([0, 1] + (list(range(11, 38)) if (not em_batalha) else []))) and (item_selecionado not in var.equipamentos.values()):
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
    if (var.equipamentos["Anel"] == 14):
        var.jogador["Vida"] = 100
        var.jogador["Mana"] = var.jogador["Max Mana"]
        
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
        texto.append("  (5): Fugir")

        print(f" {'_'*28} ")

        for linha in texto:
            print(f"|{linha:<28}|")

        print(f"|{'_'*28}|")

        
        numero_acao = input("\nRealize uma digitando seu respectivo número: ")
        
        funcao.limpar_terminal()
        
        match numero_acao:
            case "1":
                arma = var.itens[var.equipamentos["Arma"]]["Nome"]
                dano_dado = var.itens[var.equipamentos["Arma"]]["Efeito"] + (var.itens[15]["Efeito"] if (var.equipamentos["Anel"] == 15) else 0)
                dano_dado = 1 if (var.equipamentos["Arma"] in [27, 28, 29]) else dano_dado
                    
                vida_inimigo -= dano_dado
                
                funcao.print_lento(f"Você atacou {inimigo} com {arma}.")
                funcao.print_lento(f"Você deu {dano_dado} de dano em {inimigo}.")
                
                funcao.enter_para_continuar()
                
            case "2":
                nomes_magias = [magia for magia in var.magias.keys() if (var.magias[magia]["Desbloqueada"])]
                
                if (len(nomes_magias) == 0):
                    funcao.print_lento("Você ainda não conhece nenhuma magia...")
                    
                    funcao.enter_para_continuar()
                    
                    continue
                
                else:
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
                        
                        case "sair" | "s": continue
                            
                        case _:
                            print("Magia inválida!")
                            funcao.enter_para_continuar()
                            continue
                    
                    
                    if (var.magias[magia_usada]["Custo"] > var.jogador["Mana"]):
                        print("Não foi possível usar a magia por falta de mana!")
                        
                        funcao.enter_para_continuar()
                        
                        continue
                        
                    else:
                        var.jogador["Mana"] -= var.magias[magia_usada]["Custo"]
                        dano_dado = var.magias[magia_usada]["Dano"] + (20 if (var.equipamentos["Arma"] in [28, 29]) else 0)
                        vida_inimigo -= dano_dado
                        
                        funcao.print_lento(f"Você usou: {magia_usada}!")
                        funcao.print_lento(f"Você deu {dano_dado} de dano em {inimigo}.")
                        
                        funcao.enter_para_continuar()

                        
            case "3":
                var.jogador["Mana"] = min(var.jogador["Mana"] + int(0.25*var.jogador["Max Mana"]), var.jogador["Max Mana"])
                
                funcao.print_lento("Você está canalizando a sua mana...")
                funcao.print_lento("Parte da sua mana foi recuperada!")
                
                funcao.enter_para_continuar()

            case "4": 
                abrir_inventario(True)
                continue
            
            case "5":
                funcao.print_lento("Você conseguiu fugir com êxito.")
                break
                
            case _:
                print('Ação inválida!') 
                funcao.enter_para_continuar()
                continue
            
    
        if (vida_inimigo <= 0):
            break
        
        texto_ataque = var.inimigos[inimigo]["Texto Ataque"]
        dano_recebido = var.inimigos[inimigo]["Dano"] - var.itens[var.equipamentos["Armadura"]]["Efeito"] - (var.itens[16]["Efeito"] if (var.equipamentos["Anel"] == 16) else 0)
        dano_recebido = 1 if (dano_recebido <= 0) else dano_recebido
        
        var.jogador["Vida"] -= dano_recebido
        
        funcao.print_lento(f"{inimigo} {texto_ataque}!")
        funcao.print_lento(f"Você recebeu {dano_recebido} de dano.")
        
        funcao.enter_para_continuar()
        
        
        # O turno vira "??", antes de virar um número de 3 algarismos. Pra caixa do modo de batalha não ficar estranha
        turno = (turno + 1) if (turno not in [99, "??"]) else "??"
            
    
    if (vida_inimigo <= 0):
        funcao.print_lento(f"Parabéns! O inimigo foi derrotado!")
        
        drop = var.inimigos[inimigo]["Drop"]
        
        if (drop != "nenhum"):
            funcao.print_lento(f"{inimigo} dropou {drop}.")
            funcao.adicionar_item(drop, 1)
        
        funcao.indisponibilizar_interacao("Atacar " + inimigo)
           
           
        match inimigo:
            case "Esqueleto":
                funcao.indisponibilizar_interacao("Pegar Armadura de Couro do esqueleto")
                
            case "Rato":
                funcao.desbloquear_interacao("Atacar Rato")
                
            case "Guarda":
                var.guarda_sem_nome_derrotado = True
                
            case "Arqueiro": 
                var.mov_invalidos.pop((4,2))
                var.arqueiro_nos_estabulos = False
                
            case "Bibliotecário":
                var.mov_invalidos.pop((4,3))
                
                funcao.print_lento("\nO Bibliotecário era quem estava mantendo a barreira que te impedia de acessar a torre do mago.")
                funcao.print_lento("Com a sua morte, agora é possível acessá-la.")
                
            case "Guardas Reais":
                var.guardas_reais_derrotados = True
                funcao.indisponibilizar_interacao("Inspecionar estátuas")
                
            case "Mago":
                funcao.desbloquear_interacao("Furtar os itens do Mago")
                
                funcao.print_lento("\nNova interação desbloqueada: Furtar os itens do Mago")
            
            
        funcao.print_lento("\nAgora você pode continuar a sua aventura.")
        

    elif (var.jogador["Vida"] <= 0):
        funcao.print_lento("Sua vida chegou à zero, você morreu...")
        funcao.print_lento("Você misteriosamente se encontra no início do castelo.")
        
        var.jogador["Vida"] = 100
        var.jogador["Mana"] = var.jogador["Max Mana"]
        var.jogador["Localizacao"] = [0,0]


def realizar_interacao(interacao):
    match interacao:
        case _ if ("Pegar Escritura de" in interacao):
            magia = interacao.replace("Pegar Escritura de ", "")
            
            var.magias[magia]["Desbloqueada"] = True
            funcao.print_lento(f"Você aprendeu uma nova magia: {magia}.")
            
            funcao.indisponibilizar_interacao(interacao)


        case _ if ("Pegar" in interacao) and (interacao != "Pegar Armadura de Couro do esqueleto"):
            item = interacao.replace("Pegar ", "")
                
            funcao.adicionar_item(item, 1)
            funcao.print_lento(f"Você obteve: {item}.")
            
            if (item == "Vara de Pesca") and ("Interagir com o Pescador" in var.interacoes_desbloqueadas):
                funcao.disponibilizar_interacao("Dar Vara de Pesca pro Pescador")
                
            funcao.indisponibilizar_interacao(interacao)


        case _ if "Atacar" in interacao:
            inimigo = interacao.replace("Atacar ", "")
            atacar(inimigo)
            
            
        case _ if "Interagir" in interacao:
            match interacao.replace("Interagir com ", ""):
                
                case "o Pescador":
                    funcao.print_lento("Pescador: Uai? Nem vi que tinha alguém por aqui, tava distraído olhando o azulzão do lago que um dia foi meu sustento, até minha vara de pesca quebrar e eu ter que começar a comer essa comida véia e podre do castelo.")
                    funcao.print_lento("Pescador: Já faz um tempão que nenhum vivente aparece nesse castelo abandonado. Quer dizer, aparecer, aparece, mas eles vêm é pra saquear o tesouro do nosso rei morto. Só que no fim, todo mundo que se aventura por aqui só encontra a morte. O povo que mora no interior do castelo não gosta nadinha de humanos, mas pode ficar tranquilo comigo, sou só um véio pescador que não quer briga, então nem pense em puxar sua espada pra mim.")
                    funcao.print_lento("Pescador: Eu te digo pra desistir dessa aventura sua e passar o resto da vida de boa como eu, só pescando e sentindo a brisa do vento batendo no chapéu de pescador. Mas se você quer mesmo se aventurar por esse castelo, recomendo ficar longe da comida da cozinha real no meio do castelo, a não ser que você esteja morrendo de fome e precise recuperar as forças.")
                    
                        
                    if ("Dar Vara de Pesca pro Pescador" in var.interacoes_desbloqueadas) and ("Dar Vara de Pesca pro Pescador" in var.interacoes_indisponiveis):
                        funcao.print_lento("\nPescador: Ah, tô tão feliz com minha nova vara de pesca :)")
                        
                    else:
                        funcao.print_lento("\nPescador: Ah, como eu queria minha vara de pesca de volta...")


                    if (var.salas_descobertas[2][2] == False):
                        funcao.print_lento("\nNova sala descoberta: Cozinha Real")
                        funcao.descobrir_sala((2, 2))
                        

                    if ((8 in [id_item for id_item, qtd in var.inventario.items() if (qtd != 0)]) and ("Dar Vara de Pesca pro Pescador" not in var.interacoes_desbloqueadas)):
                        funcao.desbloquear_interacao("Dar Vara de Pesca pro Pescador")
                        funcao.print_lento("\nNova interação desbloqueada: Dar Vara de Pesca pro Pescador")
                
                
                case "Cuidadora":
                    if (var.arqueiro_nos_estabulos == False):
                        funcao.print_lento("Cuidadora: Oh, olá. Você não parece ser tão violento quantos os outros humanos que vieram aqui.")
                        funcao.print_lento("Cuidadora: Eu sou só uma solitária ex-servente, então fico feliz de receber uma visita em tanto tempo.")
                        funcao.print_lento("Cuidadora: Atualmente, eu passo os meus dias como uma reles cuidadora do cavalo do meu desaparecido pai, ele foi único cavalo que conseguiu sobreviver ao feitiço que protegeu esse castelo.")
                        funcao.print_lento("Cuidadora: Ops, estou falando de algo que você não se importa...")
                        
                        if (22 not in var.inventario.keys()):
                            funcao.print_lento("Cuidadora: Bem, é muito perigoso se aventurar sozinho por este castelo, pegue isto.")
                            
                            funcao.adicionar_item("Espada Reta de Ferro", 1)
                            funcao.print_lento("\nVocê recebeu uma Espada Reta de Ferro da Cuidadora.")
                            
                    else:
                        funcao.print_lento("Cuidadora: Socorro! O cavalo do meu pai está assustado, por favor não o machuque, ele não tem culpa. Apenas tire esse arqueiro de cima dele.")
                    
                    
                case "o Juiz":
                    funcao.print_lento("Juiz: Você será punido por invandir esse ambiente está com um caso em andamento.")
                    funcao.print_lento("Juiz: É bom que apresente alguma prova relevante ou, até mesmo, a resolução do caso, senão você receberá a pena de morte após o fim desse caso.")
                    
                    if ("Realizar o julgamento" not in var.interacoes_desbloqueadas):
                        funcao.desbloquear_interacao("Realizar o julgamento")
                        
                        funcao.print_lento("\nNova interação desbloqueada: Realizar o julgamento.")
                    
                    
                case "Padre":
                    funcao.print_lento("Padre: Olá, tem alguém aí? Sou apenas um servo do divino Miarli.")
                    funcao.print_lento("Padre: Como pode ver, não consigo fazer uso da minha visão, perdida por causa daquele maldito feitiço lançado pelo herege Lincaindir.") 
                    funcao.print_lento("Padre: Eu sempre adverti ao rei Karyon que manter aquele mago no castelo só resultaria em retaliação por se desviar dos dogmas, mas seu desejo por poder e dominação o levou a dar cada vez mais influência a ele.")
                    funcao.print_lento("Padre: E veja o que aconteceu: o rei está morto, seu castelo está em ruínas e seu povo pagou com a vida por causa daquele maldito feitiço.")
                    
                    funcao.print_lento("\nPadre: Enfim, eu vim aqui buscar um pouco de poção desta fonte, mas fui atacado por esses ratos.")
                    funcao.print_lento("Padre: Quando lancei um círculo de proteção já era tarde demais, não conseguia mais mover minha perna por causa da dor. Então, resolvi esperar pela recuperação dela, mas acabei perdendo a capacidade de mover as duas pernas para sempre por causa de alguma doença desses roedores imundos.")
                    funcao.print_lento("Padre: Agora, só espero dia após dia pelo livramento deste sofrimento. Acho que essa é minha punição por não ter impedido a ascensão de Lincaindir e os desejos de dominação de nosso rei, que levaram à sua morte...")
                    funcao.print_lento("Padre: Mas antes, tem uma coisa que eu preciso fazer: passar a palavra de Miarli para frente. Você aceitaria ouvir as palavras deste velho padre?")
                        
                    funcao.desbloquear_interacao("Reabastecer poções nas fontes")
                    funcao.desbloquear_interacao("Ouvir a palavra de Miarli")
                    funcao.indisponibilizar_interacao("Interagir com Padre")
                        
                    funcao.print_lento("\nNovas interações desbloqueadas: Reabastecer poções nas fontes, Ouvir a palavra de Miarli.")
                   
                    
                case "o Velho":
                    funcao.print_lento("Você acordou o velho, dessa vez sem assustar ninguém.")
                    
                    funcao.print_lento("\nVelho: Hm? Quem ousou acordar-me de minha hibernação de recuperação?")
                    funcao.print_lento("Velho: Espere, um humano? Tire sua existência desse castelo sagrado, ó descendente dos assasinos de Karyon!")
                    
                    funcao.print_lento("\nNuma explosão de mana, o velho levanta de seu descanso com um cajado para te atacar.")
                    
                    funcao.desbloquear_interacao("Atacar Mago")
                    funcao.indisponibilizar_interacao("Interagir com o Velho")
                    
                    funcao.enter_para_continuar()
                    
                    atacar("Mago")
                    
             
        case _ if "Checar registros" in interacao:
            match interacao.replace("Checar registros ", ""):
                case "de batalhas":
                    funcao.print_lento("Você decide dar uma olhada no último registro de batalha disponível. Ele conta sobre a última batalha travada pelo reino de Karyon antes do desaparecimento do seu castelo.")
                    funcao.print_lento("Essa foi a primeira grande batalha travada sem o comadante Zeeisor, devido ao seu repentino desaparecimento, e foi a última do rei Karyon, por causa de sua morte nessa mesma batalha.")
                    funcao.print_lento("\nEssa sangrenta batalha foi travada nas planícies de Elreimi, sob o domínio ao reino humano de Hisui, por causa da ricas minas que haviam naquela região.")
                    funcao.print_lento("Após 12 dias de combate, o rei Karyon foi morto em combate pelo general Soykao, o que virou a balança batalha e concedeu a vitória ao reino de Hisui.")
                    funcao.print_lento("Muitos dizem que a ausência do comadante Zeeisor foi o que resultou na morte do rei, porém naquele momento o reino não tinha tempo de achar um culpado.")
                    funcao.print_lento("Pois, os súditos e os estrategistas estavam em pânico com medo dos possíveis ataques que o reino sofreria agora que seu poderoso e insubstituível rei estava morto.")
                
                
                case "sobre o general":
                    funcao.print_lento("Zeeisor possuía uma aparência monstruosa, com três olhos, quatro braços e seis chifres. Ele causava medo até mesmo em seus aliados, por causa de seu temperamento e pelo imenso tamanho da sua claymore.")
                    funcao.print_lento("Ele não passou muito tempo como soldado e nem como comandante, pois rapidamente acendeu à posição de general pela sua força esmagadora, seus feitos em batalhas e seu estilo de luta não convencional.")
                    funcao.print_lento("Zeeisor não comandava suas tropas por meio de estratégias e táticas, mas sim pelos seus instintos. O que se provou ser muito efetivo por meio de sua sequência de vitórias.")
                    funcao.print_lento("Dessa forma, o general era uma peça extremante essecial para o reino, principalmente pelo desejo sem fim de dominação e do apreço do rei Karyon pela guerra.")
                    funcao.print_lento("Porém, certo dia Zeeisor simplesmente desapareceu, deixando o reino e, até mesmo, sua própria filha, que era uma servente do castelo, sem dar sequer uma explicação. Ninguém sabe onde ele está e o que causou o seu desaparecimento.")
                    funcao.print_lento("Muitos apontam o seu desaparecimento como a causa pela morte do rei, e consequentemente, pela derrota na batalha das planícies de Elreimi.")
                    
                    funcao.print_lento("\nParece que você descobriu uma informação útil.")
                    var.assassino_descoberto = True
                
                case "sobre o mago":
                    funcao.print_lento("O poderoso elfo Lincaindir, há pouca informação conhecida sobre sua existência antes de fazer parte da corte real.")
                    funcao.print_lento("Ninguém sabe de onde ele veio, da sua idade e nem da origem de seu extenso conhecimento sobre os planos e da magia de maneira geral.")
                    funcao.print_lento("Mas todos reconhecem seu poder e sua influência na conquista de mais terras para o domínio de vossa majestade Karyon.")
                    funcao.print_lento("Relatos dizem que ele é capaz de manipular a magia negra como bem entende, o que gerou muitas desconfiança por parte do clero do castelo. Mas, mesmo assim, dizem que ele ainda sofre das inevitáveis consequências de utilizar esse tipo de magia.")
                    funcao.print_lento("Após a morte de Karyon, Lincaindir jurou proteger o castelo de futuras invasões dos reinos humanos. Para isso, ele disse que iria lançar um feitiço de magia negra para mover o castelo para um local distante o suficiente para não ser achado.")
                    funcao.print_lento("Muitos foram contra o uso desse feitiço de magia negra, mas eles não conseguiram convencer os súditos do castelo do mesmo. A única coisa que podemos fazer agora é confiar na capacidade do nosso mago real.")
                
                
                case "sobre o rei":
                    funcao.print_lento("Karyon só podia ser descrito como excêntrico, poderoso e carismático. Um rei insubstituível, que levou seu reino, que possuía o mesmo nome que ele, a se torna o mais rico e temido.")
                    funcao.print_lento("O rei era aficionado pela guerra, não atoa que ele era conhecido como o Rei da Guerra. Esse seu amor pelo conflito resultou na queda de vários outros reinos pela mão de seu exército.")
                    funcao.print_lento("Seu castelo, que possuía o mesmo nome que ele e de seu reino, era conhecido por ser uma fortaleza impenetrável, que escondia todas as riquezas pessoais do rei, riquezas essas que valiam mais que reinos inteiros.")
                    funcao.print_lento("Mas, infelizmente, sua glória acabou na batalha das planícies de Elreimi, com a sua morte. Ele não deixou nenhum descendente e ninguém estava preparado para assumir o trono no seu lugar.")
                    funcao.print_lento("Pois, ninguém pensava que a morte de Karyon seria algo possível. E com isso, seu reino caiu em luto e desepero que pareciam destinados a durar para sempre.")
                
                
        case "Vasculhar":
            match var.jogador["Localizacao"]:
                case [0, 3]: 
                    if (var.equipamentos["Anel"] != 13):
                        funcao.print_lento("Você vasculha inutilmente...")
                        
                        if (13 in var.inventario.keys()):
                            funcao.print_lento("Você sente uma sensação estranha em algum dos itens do seu inventário.")
                            
                        else:
                            funcao.print_lento("Você tem a sensação de que está deixando alguma passar.")
                    
                    else:
                        funcao.print_lento("O seu anel brilha quando você se aproxima do fim do corredor. De repente, uma pequena porta reluzente aparece naquela parede antes vazia.")
                        
                        if ("Liberar passagem secreta" not in var.interacoes_desbloqueadas):
                            funcao.desbloquear_interacao("Liberar passagem secreta")
                            
                            funcao.print_lento("\nNova interação desbloqueada: Liberar passagem secreta.")
                
                
                case [3, 2]:
                    funcao.print_lento("Durante a sua procura por algo de valor, você tropeça no tapete vermelho da sala, ainda bem que não havia ninguém por perto para ver isso...")
                    funcao.print_lento("Quando você ia ajeitar o tapete movido pelo seu tombo, você nota que o chão e a parte inferior do tapete estavam sujos com um resíduo preto de cheiro estranho.")
                    
                    funcao.print_lento("\nParece que você descobriu uma informação útil.")
                    var.local_crime_descoberto = True
                
                
                case [3, 3]: 
                    funcao.print_lento("Após vasculhar bastante, você finalmente encontra uma arma que pode utilizar, mesmo que ela esteja um pouco enferrujada. Você também encontra um compartimento secreto contendo uma claymore e um anel.")
                    
                    if ("Pegar Anel do Combatente" not in var.interacoes_desbloqueadas):
                        funcao.desbloquear_interacao("Pegar Anel do Combatente")
                        funcao.desbloquear_interacao("Pegar Clava de Bronze Enferrujada")
                        funcao.desbloquear_interacao("Analisar claymore")
                        
                        funcao.print_lento("\nNovas interações desbloqueadas: Pegar Anel do Combatente, Pegar Clava de Bronze Enferrujada, Analisar claymore.")
                
                
                case [1, 4]: 
                    funcao.print_lento("Você revira os aposentos em busca de algum item de valor, mas no fim você só encontra alguns anéis e colares que não parecem valer muito, uma vara de pesca e uma caixinha escondida em um quarto que parece pertencer a um guerreiro.")
                    
                    if ("Pegar Vara de Pesca" not in var.interacoes_desbloqueadas):
                        funcao.desbloquear_interacao("Pegar Vara de Pesca")
                        funcao.desbloquear_interacao("Abrir caixinha")
                
                        funcao.print_lento("\nNovas interações desbloqueadas: Pegar Vara de Pesca, Abrir caixinha.")
                        
                        
                case [3, 4]: 
                    funcao.print_lento("Durante sua busca, você encontra diversos itens de valor, mas sente que há algo ainda mais valioso esperando por você, e que esse algo está bem perto.")
                    
                    
        case "Pegar Armadura de Couro do esqueleto":
            funcao.print_lento("Você ia pegar a armadura de couro, mas o esqueleto despertou.")
            funcao.enter_para_continuar()
            
            atacar("Esqueleto")
            
        
        case "Espantar pássaro":
            funcao.print_lento("Num impulso sádico, você espanta o pobre pássaro distraído. Que ação repulsiva!")
            funcao.print_lento("Algumas penas se desprendem do pássaro e se espalham pela grama.")
            
            funcao.print_lento("\nNova ação desbloqueada: Pegar Pena")
            
            funcao.desbloquear_interacao("Pegar Pena")
            funcao.indisponibilizar_interacao("Espantar pássaro")


        case "Dar Vara de Pesca pro Pescador":
            funcao.print_lento("Pescador: Nossa, ocê é bão demais! Agora finalmente vou poder pescar de novo. Como agradecimento, vou pescar um peixão bem bão pra ocê.")
            funcao.print_lento("\nNuma puxada bem rápida e forte, um peixe bem grande voa do mar até as sua mãos.")
            
            funcao.subtrair_item("Vara de Pesca", 1)
            funcao.adicionar_item("Peixe", 1)
            funcao.indisponibilizar_interacao("Dar Vara de Pesca pro Pescador")
            
            funcao.print_lento("\nVocê obteve: Peixe.")

        
        case "Destrancar acesso ao jardim":
            funcao.print_lento("Você destranca a porta da torre de vigia.")
            
            var.mov_invalidos.pop((3,0))
            var.mov_invalidos.pop((4,0))
            funcao.indisponibilizar_interacao("Destrancar acesso ao jardim")
        
        
        case "Acordar Arqueiro":
            funcao.print_lento("Você dá um susto no arqueiro para acordá-lo.")
            funcao.print_lento("Ele imediatamente dá um pulo e desce a torre numa velocidade extremamente alta.")
            funcao.print_lento("Parece que ele seguiu ao norte após chegar na guarita.")
            
            var.arqueiro_nos_estabulos = True
            
            funcao.indisponibilizar_interacao("Acordar Arqueiro")
            funcao.desbloquear_interacao("Atacar Arqueiro")
            
            funcao.print_lento("\nNova interação desbloqueada em: Estábulos")
        
        
        case "Fazer carinho no cavalo":
            if (var.arqueiro_nos_estabulos == False):
                funcao.print_lento("Você faz carinho no cavalo...")
                funcao.print_lento("Ele relincha para você...")
                funcao.print_lento("Ele parece gostar mais de você agora...")
                
            else:
                funcao.print_lento("Não é possível fazer carinho no cavalo agora, porque tem um arqueiro em cima dele tentando te atacar.")
            
        
        case "Rezar":
            funcao.print_lento("Você se ajoelha para a grande estátua e começa a rezar...")
            funcao.print_lento("Mana completamente recuperada.")
            
            var.jogador["Mana"] = var.jogador["Max Mana"]
        
        
        case "Se aproximar da multidão de espíritos":
            funcao.print_lento("Ao se aproximar da multidão de espíritos, você vê que eles estão envolta de um anel brilhante jogado no chão.")
            
            funcao.desbloquear_interacao("Pegar Anel Abençoado")
            funcao.indisponibilizar_interacao("Se aproximar da multidão de espíritos")
            
            funcao.print_lento("\nNova interação desbloqueada: Pegar Anel Abençoado.")
        
        
        case "Reabastecer poções nas fontes":
            funcao.print_lento("Você reabastece suas poções a partir das fontes estranhas...")
            
            funcao.adicionar_item("Poção de Vida", 3 - var.inventario[0])
            funcao.adicionar_item("Poção de Mana", 3 - var.inventario[1])
            
        
        case "Ouvir a palavra de Miarli":
            funcao.print_lento("Você ouve as palavras do velho padre sobre a sua crença em um ser chamado Miarli.")
            funcao.print_lento("Após o padre terminar o que ele tinha para dizer, ele se deita no chão e o seu círculo de proteção desaparece.")
            funcao.print_lento("Você tenta falar algo pra ele, mas ele não te responde e nem se move.")
            
            funcao.indisponibilizar_interacao("Ouvir a palavra de Miarli")
            
            funcao.adicionar_item("Marca de Miarli", 1)
            var.mov_invalidos.pop((3,1))
            
            funcao.print_lento("\nVocê obteve: Marca de Miarli.")
        
        
        case "Comer restos de comida":
            funcao.print_lento("Você come os restos de comida espalhados pela cozinha. Eles possuem um gosto meio duvidoso.")
            funcao.print_lento("Vida completamente recuperada.")
            
            var.jogador["Vida"] = 100


        case "Analisar claymore":
            funcao.print_lento("Essa claymore possui diversas manchas de um resíduo seco de cor preta em volta de sua lâmina...")
            funcao.print_lento("Você decide lamber o líquido e vê que ele possui um gosto azedo, parece ser sangue de orc.")

            funcao.print_lento("\nParece que você descobriu uma informação útil.")
            var.arma_crime_descoberta = True
            
            
        case "Liberar passagem secreta":
            funcao.print_lento("Passagem secreta liberada.")
            
            var.passagem_secreta_descoberta = True
            funcao.indisponibilizar_interacao("Liberar passagem secreta")

        
        case "Furtar os itens do Mago":
            funcao.print_lento("Você furta os itens do corpo enfraquecido e sem vida do Mago.")
            funcao.print_lento("\nVocê obteve: Cajado Desgastado de Lincaindir e Túnica de Lincaindir.")
            funcao.print_lento("E aprendeu uma nova magia poderosa: Tempestade de Raios.")
            
            funcao.adicionar_item("Cajado Desgastado de Lincaindir", 1)
            funcao.adicionar_item("Túnica de Lincaindir", 1)
            var.magias["Tempestade de Raios"]["Desbloqueada"] = True
            
            funcao.indisponibilizar_interacao("Furtar os itens do Mago")
            
            
        case "Abrir caixinha":
            funcao.print_lento("Ao abrir a caixinha, você encontra o que parece ser um anel de casamento e um tablete de pedra mágico com a imagem da cuidadora do estábulo mais jovem, junto com um ser monstruoso que possuía seis chifres.")
            
            funcao.print_lento("\nParece que você descobriu uma informação útil.")
            var.motivo_crime_descoberto = True
            
            
        case "Inspecionar estátuas":
            funcao.print_lento("Você encara as imóveis e realistas estátuas...")
            funcao.print_lento("Elas se assemelham com as outras estátuas de guardas que você viu em vários lugares do castelo.")
            funcao.print_lento("Mas essas na sua frente possuem algumas diferenças visuais e te passam uma sensação estranha, mas você não sabe o motivo desse sentimento.")
            funcao.print_lento("Estranho...")
            
            if ((9 in [id_item for id_item, qtd in var.inventario.items() if (qtd != 0)]) and ("Despetrificar estátuas" not in var.interacoes_desbloqueadas)):
                funcao.desbloquear_interacao("Despetrificar estátuas")
                
                funcao.print_lento("\nE se essas estátuas não forem estátuas...")
                funcao.print_lento("\nNova interação desbloqueada: Despetrificar estátuas.")
                
            
        
        case "Despetrificar estátuas":
            funcao.print_lento("Você despeja um pouco de água sagrada nas estátuas de pedra em frente à grande porta...")
            funcao.print_lento("As estátuas de pedra se quebram diante de seus olhos e guardas reais emergem delas.")
            
            funcao.desbloquear_interacao("Atacar Guardas Reais")
            funcao.indisponibilizar_interacao("Despetrificar estátuas")
            
            funcao.enter_para_continuar()
            
            atacar("Guardas Reais")


        # Enigmas     
        case "Inspecionar altares":
            funcao.print_lento("Eles parecem ser altares de oferenda, com pedestais em suas partes superiores, onde é possível colocar itens.")
            funcao.enter_para_continuar()
            
            itens_altares = [0, 0, 0]
            
            while (True):
                try:
                    print("Altar da esquerda:", "Nenhum" if (itens_altares[0] == 0) else var.itens[itens_altares[0]]["Nome"])
                    print("Altar do meio:", "Nenhum" if (itens_altares[1] == 0) else var.itens[itens_altares[1]]["Nome"])
                    print("Altar da direita:", "Nenhum" if (itens_altares[2] == 0) else var.itens[itens_altares[2]]["Nome"])
                        
                    print("\nO que você deseja fazer?:")
                    print(" (1): Pôr um item num altar")
                    print(" (2): Retirar os itens dos altares")
                    print(" (3): Ler as escrituras dos altares")
                    print(" (4): Sair")

                    numero_acao = input("Digite seu respectivo número: ")
                    
                    funcao.limpar_terminal()
                    
                    match numero_acao:
                        case "1":
                            print("Você deseja por um item em qual altar?")
                            print(" (1): Altar da esquerda")
                            print(" (2): Altar do meio")
                            print(" (3): Altar da direita")
                            print(" (4): Voltar")
                            
                            numero_altar = input("Digite seu respectivo número: ")
                            
                            funcao.limpar_terminal()
                            
                            match numero_altar:
                                case _ if numero_altar in ["1", "2", "3"]:
                                    print(f" {'_'*38} ")
                                    print("| {:<02} | {:<31} |".format("ID", "NOME DO ITEM"))
                                    print(f"|{'='*4}|{'='*33}|")

                                    itens_validos = [id_item for id_item, quantidade in var.inventario.items() if ((quantidade != 0) and (id_item not in ([0, 1] + itens_altares)))]
                                    
                                    for id_item in itens_validos:
                                        nome = var.itens[id_item]["Nome"]

                                        print("| {:>02} | {:<31} |".format(id_item, nome))

                                    print(f"|{'_'*4}|{'_'*33}|")
                                    
                                    try:
                                        n_item = int(input("\nSelecione um item para pôr no altar (Digite o ID do item): "))
                                        
                                        funcao.limpar_terminal()
                                        
                                        if (n_item in itens_validos):
                                            match numero_altar:
                                                case "1": itens_altares[0] = n_item
                                                case "2": itens_altares[1] = n_item
                                                case "3": itens_altares[2] = n_item


                                        else:
                                            print("O ID do item não foi encontrado!")
                                            
                                            funcao.enter_para_continuar()
                                        
                                    except:
                                        funcao.limpar_terminal()
                                    

                                case "4":
                                    pass
                                
                                case _:
                                    print("Altar inválido!")
                                    funcao.enter_para_continuar()
                        
                        case "2":
                            itens_altares = [0, 0, 0]
                            funcao.print_lento("Os itens foram retirados dos altares e postos no seu inventário novamente.")
                            
                            funcao.enter_para_continuar()
                            
                        case "3":
                            print("Altar da esquerda: A ESPADA PODE MARCAR OS VIVOS COM FERIMENTOS, ENQUANTO ELA PODE MARCAR O PAPEL COM CONHECIMENTO.")
                            print("Altar do meio: ABENÇOADA PELA SUA BELEZA, ARRANCADA DE SEU PRÓPRIO LAR POR ELA. ABENÇOADA PELA SUA BELEZA, OU MELHOR, AMALDIÇOADA PELA SUA BELEZA.")
                            print("Altar da direita: VIVO E SALTITANTE ENQUANTO MOLHADO, MORTO E COZIDO ENQUANTO SECO.")
                            
                            funcao.enter_para_continuar()
                            
                        case "4":
                            break
                        
                        case _:
                            print("Ação inválida!")
                            
                            funcao.enter_para_continuar()
                            
                except:
                    funcao.limpar_terminal()
                
                
                if (itens_altares == [3, 2, 4]):
                    funcao.print_lento("De repente, os altares começam a emitir uma luz pelos seus pedestais...")
                    funcao.print_lento("Os itens somem e uma chave surge do pedestal do meio.")
                    
                    funcao.print_lento("\nVocê obteve: Chave da Biblioteca.")
                    
                    funcao.adicionar_item("Chave da Biblioteca", 1)
                    funcao.subtrair_item("Flor", 1)
                    funcao.subtrair_item("Pena", 1)
                    funcao.subtrair_item("Peixe", 1)
                    
                    var.mov_invalidos.pop((1,3))
                    
                    funcao.indisponibilizar_interacao("Inspecionar altares")
                    
                    break
                
        
        case "Realizar o julgamento":
            if (False in [var.arma_crime_descoberta, var.local_crime_descoberto, var.motivo_crime_descoberto, var.assassino_descoberto]):
                funcao.print_lento("Você sente que você não possuí pistas o suficiente para resolver esse caso. Mas mesmo assim você inicia o julgamento.\n")
        
            arma_escolhida = local_escolhido = motivo_escolhido = assassino_escolhido = ""
            
            armas_possiveis = ["Espada Reta de Ferro", "Adaga Cerimonial", "Alabarda do Guarda sem Nome", "Espada do Cavaleiro Negro", "Rapieira", "Clava de Bronze", "Cimitarra"]
            locais_possiveis = ["Jardim", "Torre de Vigia", "Estábulos", "Refeitório", "Guarita", "Armazém", "Masmorra", "Armaria", "Aposentos"]
            motivos_possiveis = ["Inveja da sua futura promoção", "Preconceito por ser um orc", "Não adorar Miarli", "Ser promovido à comandante sem ter nascido na casta nobre"]
            assassinos_possiveis = ["Pescador", "Cuidadora", "Cavaleiro Misterioso", "Padre", "Bibliotecário", "Guarda Real", "Mago Lincaidir", "Rei Karyon"]
            
            if (var.arma_crime_descoberta):
                armas_possiveis.insert(3, "Claymore")
            
            if (var.local_crime_descoberto):
                locais_possiveis.insert(7, "QG")
            
            if (var.motivo_crime_descoberto):
                motivos_possiveis.insert(0, "Caso romântico entre Wuverborn e a cuidadora")
                
            if (var.assassino_descoberto):
                assassinos_possiveis.insert(6, "General Zeeisor")
                
            
            funcao.print_lento("Juiz: Wuverborn, um jovem soldado promisor que estava prestes a ser promovido à comandante, foi assassinado pouco tempo antes do desaparecimento do general Zeeisor e da morte do rei Karyon. Seu corpo foi encontrado na masmorra, mas tudo indica que ele não foi assassinado lá.")
            funcao.print_lento("Juiz: Esse orc possuía diversos feitos em batalha e todos esperavam muito mais dele no futuro. Até o dia de hoje, seu caso permanece sem uma resolução, o que impediu o início da investigação acerca do sumiço do general.")
            funcao.print_lento("\nJuiz: Com isso, vamos dar início ao julgamento.")
            funcao.enter_para_continuar()

            while (True):
                try:
                    parte = 0
                    
                    while (parte < 4):
                        match parte:
                            case 0:
                                texto = "Juiz: Qual foi a arma foi usada no crime?"
                                opcoes = armas_possiveis
                                
                            case 1:
                                texto = "Juiz: Qual foi o local onde o crime ocorreu?"
                                opcoes = locais_possiveis
                                
                            case 2:
                                texto = "Juiz: Qual foi a motivação por trás do crime?"
                                opcoes = motivos_possiveis
                                
                            case 3:
                                texto = "Juiz: Quem foi o assassino?"
                                opcoes = assassinos_possiveis

                                
                        funcao.print_lento(texto)
                        
                        for n_opcao in range(len(opcoes)):
                            print(f" ({n_opcao+1}): {opcoes[n_opcao]}")
                            
                        
                        escolha = int(input("Digite seu respectivo número: "))
                        
                        if (escolha in range(1, len(opcoes)+1)):
                            match parte:
                                case 0: arma_escolhida = opcoes[escolha-1]
                                case 1: local_escolhido = opcoes[escolha-1]
                                case 2: motivo_escolhido = opcoes[escolha-1]
                                case 3: assassino_escolhido = opcoes[escolha-1]
                            
                            parte += 1
                            
                            funcao.limpar_terminal()
                            
                        else:
                            funcao.limpar_terminal()
                            
                            print("Opção inválida!")
                            
                            funcao.enter_para_continuar()
                    
                    
                    print("Resumo do caso:")
                    print(" Arma:", arma_escolhida)
                    print(" Local:", local_escolhido)
                    print(" Motivo:", motivo_escolhido)
                    print(" Assassino:", assassino_escolhido)
                    
                    reposta = input("Você tem certeza que está tudo correto? (Sim / Não): ")
                    
                    if (reposta.casefold() in ["sim", "s"]):
                        funcao.limpar_terminal()
                        
                        if ([arma_escolhida, local_escolhido, motivo_escolhido, assassino_escolhido] == ["Claymore", "QG", "Caso romântico entre Wuverborn e a cuidadora", "General Zeeisor"]):
                            funcao.print_lento("Juiz: Tudo parece se encaixar agora.")
                            funcao.print_lento("\nJuiz: Wuveborn estava tendo um caso com a filha do general Zeeisor, que atualmente vive nos estábulos desse castelo cuidando do cavalo do seu pai.")
                            funcao.print_lento("Juiz: Ambos decidiram não contar sobre seu o romance, por medo da desaprovação do general, que gostaria que sua filha se casasse com um nobre.")
                            funcao.print_lento("Juiz: Porém, Wuveborn seria promovido a comandante e acabou se aproximando do general pelos seus feitos nas guerras, o que acabou gerando uma confiança no soldado.")
                            funcao.print_lento("Juiz: Com essa confiança, Wuverborn decidiu contar ao general, no QG à noite quando ninguém mais estivesse por perto, que estava se relacionando com a sua filha.")
                            funcao.print_lento("Juiz: O que desencadeou uma fúria no general, que matou Wuverborn ali mesmo com sua famosa claymore. Após isso, Zeeisor escondeu a arma do crime na armaria e o corpo do futuro comandante na masmorra.")
                            funcao.print_lento("Juiz: E logo depois fugiu do castelo, por vergonha de ter matado um soldado tão promissor e, principalmente, por não conseguir dizer a própria filha que matou o amor de sua vida.")
                            
                            funcao.print_lento("\nJuiz: Com isso, dois casos foram resolvidos: o assassinato de Wuveborn e o desaparecimento do general. Você foi absolvido da pena de morte e tem o direito de escolher uma recompensa pelos seus esforços...")
                            funcao.print_lento("Juiz: Então, você deseja acessar a sala que guarda os tesouros do nosso finado rei? Pois bem, como você libertou esse tribunal de seus casos pendentes, e pela minha desconfiança de que você realmente irá conseguir acessar a sala do tesouro desse castelo, será concedido a você a chave para essa sala.")
                            funcao.print_lento("Juiz: A sala do tesouro se encontra extremo sudeste deste castelo, sendo acessada pelo quarto do rei.")
                            
                            funcao.descobrir_sala((3,4))
                            funcao.descobrir_sala((4,4))
                            funcao.adicionar_item("Chave da Sala do Tesouro", 1)
                            var.mov_invalidos.pop((4,4))
                            
                            funcao.print_lento("\nVocê obteve: Chave da Sala do Tesouro.")
                            
                            funcao.indisponibilizar_interacao("Realizar o julgamento")
                            funcao.indisponibilizar_interacao("Interagir com o Juiz")
                            break
                            
                        else:
                            funcao.print_lento("Juiz: Não parece estar certo. Você será condenado a morte de novo!")
                            funcao.print_lento("Você falhou em tentar resolver esse caso...")
                            break
                
                    else:
                        funcao.limpar_terminal()
                        continue
                    
                except:
                    funcao.limpar_terminal()
                    print("Inválido!")
                    funcao.enter_para_continuar()
        
        
        case "Resolver enigma":
            while(True):
                try:
                    print("O que você deseja fazer?:")
                    print(" (1): Puxar as alavancas dos altares")
                    print(" (2): Ler o texto gravado no pedestal")
                    print(" (3): Sair")
        
                    numero_acao = input("Digite seu respectivo número: ")
                    
                    funcao.limpar_terminal()
                    
                    match numero_acao:
                        case "1":
                            ordem = [" ", " ", " ", " "]
                            turno = 0
                            
                            while (turno < 4):
                                print("Ordem: ", " - ".join(ordem))
                                
                                print("\nVocê deseja puxar a alavanca de qual pedra?")
                                print(" (1): Altar da Cobra")
                                print(" (2): Altar da Raposa")
                                print(" (3): Altar do Lobo")
                                print(" (4): Altar do Urso")
                                
                                numero_altar = input("Digite seu respectivo número: ")
                                
                                funcao.limpar_terminal()
                                
                                match numero_altar:
                                    case "1": ordem[turno] = "Cobra"
                                    case "2": ordem[turno] = "Raposa"
                                    case "3": ordem[turno] = "Lobo"
                                    case "4": ordem[turno] = "Urso"
                                    case _: 
                                        print("Altar inválido!")
                                        funcao.enter_para_continuar()
                                        
                                        continue
                                
                                turno += 1
                                
                            
                            if (ordem == ["Cobra", "Urso", "Raposa", "Lobo"]):
                                funcao.print_lento("De repente, do pedestal, abre-se um compartimento...")
                                funcao.print_lento("Você encontrou um frasco com água cristalina dentro e uma outra alavanca.")
                                funcao.print_lento("Ao puxar essa alavanca, você ouve um barulho vindo da porta. Parece que você está livre agora.")
                                
                                funcao.print_lento("\nVocê obteve: Frasco com Água Sagrada.")
                                
                                funcao.adicionar_item("Frasco com Água Sagrada", 1)
                                var.mov_invalidos.pop((0,3))
                                
                                funcao.indisponibilizar_interacao("Resolver enigma")
                                
                                break
                            
                            else:
                                funcao.print_lento("Nada aconteceu...")
                                funcao.print_lento("Talvez a ordem das alavancas esteja errada.")
                            
                        case "2":
                            print("Está escrito o seguinte:")
                            print(" O primeiro teme a todos, enquanto o segundo não teme ninguém.")
                            print(" O terceiro come o que ele pode, tendo preferência pelo primeiro.")
                            print(" O quarto teme o segundo, mas só quando está sozinho.\n")
                            
                        case "3":
                            break
                        
                        case _:
                            print("Ação inválida!")

                    funcao.enter_para_continuar()
                    
                except:
                    funcao.limpar_terminal()
                    print("Ação inválida!")
                    funcao.enter_para_continuar()
    
    funcao.enter_para_continuar()