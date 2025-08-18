import os 

menu = f"""
{"-"*12} Menu {"-"*12}
1. Depositar
2. Sacar
3. Extrato
0. Sair
{"-"*30}
"""

saldo = 0
limite = 500
extrato = f'{"-"*10} Extrato {"-"*10}\n'
numero_saques = 0
LIMITE_SAQUES = 3
movimentacao_conta = False


while True:

    print(menu)
    opcao = input('Informe uma opção conforme o menu acima: ')
    os.system('cls' if os.name == 'nt' else 'clear')
    if opcao == '1':
        
        print("Depósito selecionado.\n")
        try:
            valor = input("Informe o valor a ser depositado: ").replace(",", ".")
            valor = float(valor)
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero.")
            saldo += valor
            movimentacao_conta = True
            extrato += f'Depósito de R$ {valor:.2f} (+)\n'
            print(f'Deposito de R$ {valor:.2f} realizado com sucesso!')
        except ValueError:
            print(f'Valor {valor} não é aceito!')
            print("Informe um valor válido")
        finally:
            input('\nPRESSIONE ENTER PARA CONTINUAR')

    elif opcao == '2':
        print("Saque selecionado.\n")
        if numero_saques >= 3:
            print('Quantidade de saque excedido!')
            print(f'A quantidade de saque total é de {numero_saques} saque(s)')
            print('Para mais informações consulte seu Gerente')
        else:
            try:
                valor = input("Informe o valor que deseja sacar: ").replace(",", ".")
                valor = float(valor)
                if valor > limite:
                    print('Saque não permitido!')
                    print(f'Seu limite por saque é de R$ {limite}.')
                elif valor > saldo:
                    print('Saque não permitido!')
                    print(f'Seu saldo atual é de R$ {saldo:.2f}.')
                elif valor <= 0:
                    raise ValueError("O valor deve ser maior que zero.")
                else:
                    numero_saques += 1
                    saldo -= valor
                    movimentacao_conta = True
                    extrato += f'Saque de R$ {valor:.2f} (-)\n'
                    print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
            except ValueError:
                print(f'Valor {valor} não é aceito!')
                print("Informe um valor válido")
            finally:
                input('\nPRESSIONE ENTER PARA CONTINUAR')

    elif opcao == '3':
        print("Extrato selecionado.\n")
        if movimentacao_conta:
            print(extrato)
            print(f'{"."*20}')
            print(f'Saldo atual R$ {saldo}.')
        else:
            print('Não foram realizadas movimentações.')
        input('\nPRESSIONE ENTER PARA CONTINUAR')
    elif opcao == '0':
        print("Obrigado por utilizar nosso sistema bancário")
        print("Volte sempre!")
        break
    else:
        print(f"Opção *{opcao}* não cadastrada no menu!")
        print("Tente novamente com uma das opções do menu!.")
