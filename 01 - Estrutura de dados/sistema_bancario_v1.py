import os


def limpar_terminal(mensagem=True):
    if mensagem:
        input('Pressione ENTER para continuar!')
    os.system("cls" if os.name == "nt" else "clear")


def menu(itens_menu: list):
    opcoes_menu = {}
    while True:
        for indice, item in enumerate(itens_menu):
            opcoes_menu[str(indice+1)] = item
        opcoes_menu[str(indice+2)] = "Sair"
        monta_texto_menu(opcoes_menu=opcoes_menu)
        opcao = input('Informe uma opção conforme o menu acima: ')
        print()
        if opcoes_menu.get(opcao, None) == "Sair":
            return sair(), opcao, opcoes_menu

        elif opcoes_menu.get(opcao, None) != None:
            return False, opcao, opcoes_menu

        else:
            print("Opção inválida.")
            limpar_terminal()
        


def monta_texto_menu(opcoes_menu: dict):
    cabecalho = f"{'-'*12} Menu {'-'*12}"
    rodape = f"{'-'*30}"
    print(cabecalho)
    for chave, valor in opcoes_menu.items():
        print(f"{chave}  - {valor}")
    print(rodape)


def recebe_valor(mensagem: str):
    while True:
        try:
            valor = input(f"{mensagem}: ")
            valor = float(valor)
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


def saque(saldo: float, numero_saques: int, limite_quantidade_saques: int, limite_por_saque: float, movimentacoes: list):
    limpar_terminal(mensagem=False)
    print(f'{"-" * 20} Saque {"-" * 20}')
    valor_saque = 0
    if numero_saques >= limite_quantidade_saques:
        print("Saque não permitido pois excede o limite da quantidade de saques!")
        print(f"Limite por saque R$ {limite_por_saque:.2f}")
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
            valor_saque = valor_solicitado
            if valor_solicitado != 0:
                movimentacoes.append(f"Saque R$ {valor_saque:.2f} (-)")
                print("Saque efetuado com sucesso!")   
        limpar_terminal() 
        return -valor_saque


def deposito(movimentacoes: list):
    limpar_terminal(mensagem=False)
    print(f'{"-" * 18} Depósito {"-" * 18}')
    valor_deposito = recebe_valor("Informe um valor para depósito ou 0 para voltar")
    if valor_deposito > 0:
        movimentacoes.append(f"Depósito R$ {valor_deposito:.2f} (+)")
        print("Depósito efetuado com sucesso!")
        limpar_terminal()
    else:
        limpar_terminal(mensagem=False)
    return valor_deposito


def extrato(saldo: float, numero_saques: int, limite_quantidade_saques: int, movimentacoes: list):
    limpar_terminal(mensagem=False)
    print(f'{"-"*18} Extrato {"-"*18}')
    print(f'Saldo atual: R$ {saldo:.2f}')
    print(f'Saques disponíveis: {limite_quantidade_saques - numero_saques}')
    print()
    print('Movimentações efetuadas:')

    if movimentacoes != None:
        for movimentacao in movimentacoes:
            print(movimentacao)
    else:
        print('    Movimentações não encontradas!')

    print(f'{"-"*45}')
    print()
    limpar_terminal()


def atualiza_saldo(valor, saldo):
    return saldo + valor if valor != None else 0


encerrar = False
itens_menu = ['Sacar', 'Depositar', 'Extrato']

saldo = 0
limite_por_saque = 500
numero_saques = 0
limite_quantidade_saques = 3
movimentacao_conta = []

while not encerrar:
    encerrar, opcao, opcoes_menu = menu(itens_menu)
    valor = 0
    if opcoes_menu[opcao] == itens_menu[0]:
        valor = saque(saldo=saldo, numero_saques=numero_saques, limite_quantidade_saques=limite_quantidade_saques,
                      limite_por_saque=limite_por_saque, movimentacoes=movimentacao_conta)
        numero_saques += 1 if valor < 0 else 0
    elif opcoes_menu[opcao] == itens_menu[1]:
        valor = deposito(movimentacoes=movimentacao_conta)
    elif opcoes_menu[opcao] == itens_menu[2]:
        extrato(saldo=saldo, numero_saques=numero_saques,
                limite_quantidade_saques=limite_quantidade_saques, movimentacoes=movimentacao_conta)

    saldo = atualiza_saldo(saldo=saldo, valor=valor)
