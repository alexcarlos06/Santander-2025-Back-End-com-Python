# Entrada do número de pacientes
n = int(input().strip())

# Lista para armazenar pacientes
pacientes = []

# Loop para entrada de dados
for _ in range(n):
    nome, idade, status = input().strip().split(", ")
    idade = int(idade)
    pacientes.append((nome, idade, status))


# TODO: Ordene por prioridade: urgente > idosos > demais:
pacientes_ordenados = sorted(pacientes, key=lambda x: (
    0 if x[2].upper() == 'URGENTE' else (1 if x[1] >= 60 else 2),-x[1]))

# TODO: Exiba a ordem de atendimento com título e vírgulas:

print("Ordem de Atendimento:", ", ".join([x[0] for x in pacientes_ordenados]))