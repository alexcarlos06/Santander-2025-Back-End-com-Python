# Entrada do usuário
email = input().strip()

# TODO: Verifique as regras do e-mail:

status_email = "E-mail inválido"
valida_espaco = True if not " " in email else False
valida_arroba = True if "@" in email and email.count('@') == 1 else False 
lista_dominio = email.split('@')
if valida_arroba and valida_espaco and len(lista_dominio) == 2:
    valida_dominio = True if ".com" in lista_dominio[1] else false 
    valida_estrutura = True if not email.endswith('@') and not email[0]=="@" else False
    
    if valida_estrutura and valida_dominio:
        status_email = "E-mail válido"

print(status_email)