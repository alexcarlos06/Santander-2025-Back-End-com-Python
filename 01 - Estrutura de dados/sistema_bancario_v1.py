import os


def limpar_terminal(mensagem=True):
    if mensagem:
        input('Pressione ENTER para continuar!')
    os.system("cls" if os.name == "nt" else "clear")


def menu(itens_menu: list, dados_mestre: dict):
    limpar_terminal(False)
    opcoes_menu = {}
    while True:
        for indice, item in enumerate(itens_menu):
            opcoes_menu[str(indice+1)] = item
        opcoes_menu[str(indice+2)] = "Sair"
        monta_texto_menu(opcoes_menu=opcoes_menu,
                         agencia=dados_mestre["agencia"], conta=dados_mestre["conta"], usuario=dados_mestre["usuario"])
        opcao = input('Informe uma opção conforme o menu acima: ')
        print()
        if opcoes_menu.get(opcao, None) == "Sair":
            return sair(), opcao, opcoes_menu

        elif opcoes_menu.get(opcao, None) != None:
            return False, opcao, opcoes_menu

        else:
            print("Opção inválida.")
            limpar_terminal()


def monta_texto_menu(opcoes_menu: dict, agencia: str = "", conta: str = "", usuario: str = ''):
    cabecalho = f"{'-'*12} Menu {'-'*12}"
    rodape = f"{'-'*30}"
    conta_logada = f"Agencia: {agencia} Conta: {conta}"
    usuario = f"Olá, {usuario}"
    print(rodape)
    print(f"{conta_logada:^30}")
    print(f"{usuario:^30}")
    print(cabecalho)
    for chave, valor in opcoes_menu.items():
        print(f"{chave}  - {valor}")
    print(rodape)


def recebe_valor(mensagem: str, ponto_flutuante=True):
    while True:
        try:
            valor = input(f"{mensagem}: ").strip()
            if ponto_flutuante:
                valor = float(valor)
            else:
                valor = int(valor)
            return valor
        except ValueError:
            print()
            print(f"O Valor informado [{valor}] não é um valor válido!")


def sair():
    limpar_terminal(mensagem=False)
    print(f"{'-'*30}")
    print(f"{'-'*5} Sistema Encerrado {'-'*6}")
    print(f"{'-'*30}")
    return True


def sair_da_conta(dados_meste: dict):
    dados_meste["agencia"] = "0001"
    dados_meste["conta"] = 0
    dados_meste["usuario"] = 'Acesse sua conta'
    print("Obrigado por utilizar nossos serviços")
    limpar_terminal()


def valida_conta_logada(conta):
    if conta == 0:
        print("Conta não encontrada!")
        print("Favor cadastrar um usuário e conta.")
        print()
        limpar_terminal()
        return False
    return True


def saque(*, lista_de_contas: list, conta: int):
    limpar_terminal(mensagem=False)
    print(f'{"-" * 20} Saque {"-" * 20}')
    if valida_conta_logada(conta=conta):
        _, dados = filtra_conta(conta=conta, lista_contas=lista_de_contas)
        numero_saques = dados["numero_saques"]
        limite_quantidade_saques = dados["limite_quantidade_saques"]
        limite_por_saque = dados["limite_por_saque"]
        saldo = dados['saldo']
        if numero_saques >= limite_quantidade_saques:
            print("Saque não permitido pois excede o limite da quantidade de saques!")
        else:
            valor_solicitado = recebe_valor(
                "Informe um valor para saque ou 0 para voltar")
            if valor_solicitado > saldo:
                print("Saque não permitido pois excede o saldo em conta!")
                print(f"Saldo em conta R$ {saldo:.2f}")
            elif valor_solicitado > limite_por_saque:
                print("Saque não permitido pois excede o limite de valor por saque!")
                print(f"Limite por saque R$ {limite_por_saque:.2f}")
            else:
                if valor_solicitado != 0:
                    dados["saldo"] -= valor_solicitado
                    dados["numero_saques"] += 1
                    dados["movimentacao_conta"].append(
                        f"Saque R$ {valor_solicitado:.2f} (-)")
                    print("Saque efetuado com sucesso!")
        limpar_terminal()


def deposito(lista_de_contas: list, conta: int, /):
    limpar_terminal(mensagem=False)
    print(f'{"-" * 18} Depósito {"-" * 18}')
    if valida_conta_logada(conta=conta):
        valor_deposito = recebe_valor(
            "Informe um valor para depósito ou 0 para voltar")
        if valor_deposito > 0:
            _, dados = filtra_conta(conta=conta, lista_contas=lista_de_contas)
            dados["saldo"] += valor_deposito
            dados["movimentacao_conta"].append(
                f"Depósito R$ {valor_deposito:.2f} (+)")
            print("Depósito efetuado com sucesso!")
            limpar_terminal()
        else:
            limpar_terminal(mensagem=False)


def extrato(lista_de_contas: list, /, *, conta: int):
    limpar_terminal(mensagem=False)
    print(f'{"-"*18} Extrato {"-"*18}')
    if valida_conta_logada(conta=conta):
        _, dados = filtra_conta(conta=conta, lista_contas=lista_de_contas)
        saldo = dados["saldo"]
        limite_quantidade_saques = dados["limite_quantidade_saques"]
        numero_saques = dados["numero_saques"]
        print(f'Saldo atual: R$ {saldo:.2f}')
        print(
            f'Saques disponíveis: {limite_quantidade_saques - numero_saques}')
        print()
        print('Movimentações efetuadas:')

        if len(dados["movimentacao_conta"]) > 0:
            for movimentacao in dados["movimentacao_conta"]:
                print(movimentacao)
        else:
            print('Sem movimentações para exibir no extrato!')

        print(f'{"-"*45}')
        print()
        limpar_terminal()


def atualiza_saldo(valor, saldo):
    return saldo + valor if valor != None else 0


def filtra_cpf(lista_de_usuarios, cpf):
    nome = ""
    dados = {}
    cpf_disponivel = True if cpf not in [x["cpf"]
                                         for x in lista_de_usuarios] else False
    if not cpf_disponivel:
        dados = [x for x in lista_de_usuarios if x["cpf"] == cpf][0]
        nome = dados["dados"]["nome"]
    return cpf_disponivel, dados, nome


def filtra_conta(lista_contas, conta):
    conta_disponivel = True if conta in [x["conta"]
                                         for x in lista_contas] else False
    dados = {}
    if conta_disponivel:
        dados = [x for x in lista_contas if x["conta"] == conta][0]
    return conta_disponivel, dados


def criar_usuario(dados_mestre: dict):
    cpf = recebe_valor(
        "Informe seu cpf (Apenas números) ou 0 para voltar", ponto_flutuante=False)
    if cpf == 0:
        limpar_terminal(False)
        return
    cpf_disponivel, _, nome = filtra_cpf(
        lista_de_usuarios=dados_mestre["lista_usuarios"], cpf=cpf)
    if cpf_disponivel:
        nome = input("Informe seu nome completo: ").strip()
        data_de_nascimento = input(
            "Informe sua data de nascimento (DD/MM/AAAA): ").strip()
        endereco = input("Informe seu endereço completo: ").strip()

        dados = {"cpf": cpf, "dados":
                 {"nome": nome, "nascimento": data_de_nascimento, "endereco": endereco}}
        dados_mestre["lista_usuarios"].append(dados)
        print(f"Usuário {dados["dados"]["nome"]} Criado com sucesso!")
    else:
        print(f"CPF já Cadastrado para {nome}")
    limpar_terminal()


def criar_conta(dados_mestre: dict):
    cpf = recebe_valor(
        "informe o CPF para criar a conta (Apenas números) ou 0 oara voltar", False)
    if cpf == 0:
        limpar_terminal(mensagem=False)
        return
    cpf_disponivel, dados, nome = filtra_cpf(
        lista_de_usuarios=dados_mestre["lista_usuarios"], cpf=cpf, )
    if cpf_disponivel:
        print("Usuário não encontrado.")
        print("Crie um usuário para seguir com a criação da conta!")
        limpar_terminal()
    else:
        limite_por_saque = 500
        numero_saques = 0
        limite_quantidade_saques = 3
        agencia = "0001"
        movimentacao_conta = []
        dados_bancarios = {"usuario": cpf, "agencia": agencia, "conta": dados_mestre["sequencia_conta"] + 1, "saldo": 0, "limite_quantidade_saques": limite_quantidade_saques,
                           "numero_saques": numero_saques, "limite_por_saque": limite_por_saque, "movimentacao_conta": movimentacao_conta}
        dados_mestre["lista_de_contas"].append(dados_bancarios)
        dados_mestre["sequencia_conta"] += 1
        print(
            f"Conta {dados_bancarios['conta']} criada com sucesso para {nome}!")
        print()
        limpar_terminal()


def acessar_conta(dados_mestre: dict):
    conta = recebe_valor("Informe o número da conta", False)
    conta_disponivel, dados_conta = filtra_conta(
        dados_mestre["lista_de_contas"], conta=conta)
    if conta_disponivel:
        _, _, usuario = filtra_cpf(
            lista_de_usuarios=dados_mestre["lista_usuarios"], cpf=dados_conta['usuario'])
        dados_mestre['conta'] = dados_conta['conta']
        dados_mestre['agencia'] = dados_conta['agencia']
        dados_mestre['usuario'] = usuario
    else:
        print(f"Conta {conta}, não encontrada")
    limpar_terminal()


def menu_login():
    dados_mestre["encerrar"], opcao, opcoes_menu = menu(
        itens_menu_inicial, dados_mestre=dados_mestre)
    if opcoes_menu[opcao] == itens_menu_inicial[0]:
        criar_usuario(dados_mestre=dados_mestre)
    elif opcoes_menu[opcao] == itens_menu_inicial[1]:
        criar_conta(dados_mestre=dados_mestre)
    elif opcoes_menu[opcao] == itens_menu_inicial[2]:
        acessar_conta(dados_mestre=dados_mestre)


def menu_logado():
    dados_mestre["encerrar"], opcao, opcoes_menu = menu(
        itens_menu, dados_mestre=dados_mestre)
    if opcoes_menu[opcao] == itens_menu[0]:
        saque(
            lista_de_contas=dados_mestre["lista_de_contas"], conta=dados_mestre["conta"])
    elif opcoes_menu[opcao] == itens_menu[1]:
        deposito(
            dados_mestre["lista_de_contas"], dados_mestre["conta"])
    elif opcoes_menu[opcao] == itens_menu[2]:
        extrato(dados_mestre["lista_de_contas"], conta=dados_mestre["conta"])
    elif opcoes_menu[opcao] == itens_menu[3]:
        criar_usuario(dados_mestre=dados_mestre)
    elif opcoes_menu[opcao] == itens_menu[4]:
        criar_conta(dados_mestre=dados_mestre)
    elif opcoes_menu[opcao] == itens_menu[5]:
        acessar_conta(dados_mestre=dados_mestre)
    elif opcoes_menu[opcao] == itens_menu[6]:
        sair_da_conta(dados_meste=dados_mestre)


def main():
    while not dados_mestre["encerrar"]:
        if len(dados_mestre["lista_usuarios"]) == 0 or len(dados_mestre["lista_de_contas"]) == 0 or dados_mestre["conta"] == 0:
            menu_login()
        else:
            menu_logado()


dados_mestre = {"lista_usuarios": [], "lista_de_contas": [], "encerrar": False,
                "conta": 0, "agencia": "0001", "usuario": 'Acesse sua conta', "sequencia_conta": 0}


itens_menu = ['Sacar', 'Depositar', 'Extrato',
              "Criar Usuário", "Criar Conta", "Acessar outra conta", "Sair da Conta"]

itens_menu_inicial = ['Criar Usuário', "Criar Conta", "Acessar Conta"]

main()
