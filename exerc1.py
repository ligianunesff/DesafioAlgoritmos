import random

# Dados de exemplo (pesos e valores dos itens)
pesos = [10, 20, 30, 40, 50, 35, 25, 15, 45, 55]
valores = [100, 120, 130, 160, 200, 180, 150, 110, 170, 220]
peso_maximo = 150  # Peso máximo da mochila

# Parâmetros do algoritmo genético
num_geracoes = 50
num_individuos = 10
taxa_mutacao = 0.1

# Função de fitness: Retorna o valor total e peso total de um cromossomo
def fitness(cromossomo):
    valor_total = 0
    peso_total = 0
    for i in range(len(cromossomo)):
        if cromossomo[i] == 1:
            valor_total += valores[i]
            peso_total += pesos[i]
    if peso_total > peso_maximo:
        return 0, peso_total  # Penaliza se ultrapassar o peso máximo
    return valor_total, peso_total

# Função de seleção: Seleciona os melhores indivíduos
def selecionar(populacao):
    populacao.sort(reverse=True, key=lambda x: x[0])  # Ordena pela pontuação de fitness
    return populacao[:num_individuos // 2]  # Mantém apenas a metade melhor

# Função de crossover: Cria novos filhos
def crossover(pai, mae):
    ponto_corte = random.randint(1, len(pai) - 1)
    filho1 = pai[:ponto_corte] + mae[ponto_corte:]
    filho2 = mae[:ponto_corte] + pai[ponto_corte:]
    return filho1, filho2

# Função de mutação: Diversidade genética
def mutacao(cromossomo):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]  # Inverte o valor (0 -> 1 ou 1 -> 0)

# Inicializa a população de forma aleatória
def inicializar_populacao():
    return [[random.randint(0, 1) for _ in range(len(pesos))] for _ in range(num_individuos)]

# Algoritmo genético principal
def algoritmo_genetico():
    populacao = inicializar_populacao()
    melhores_individuos = []  # Para armazenar o melhor indivíduo de cada geração
    medias_pesos_melhores_individuos = []  # Para armazenar a média dos pesos do melhor cromossomo de cada geração

    for geracao in range(num_geracoes):
        # Avalia o fitness de cada indivíduo na população
        populacao_avaliada = [(fitness(individuo)[0], individuo) for individuo in populacao]

        # Encontra o melhor indivíduo da geração
        melhor_individuo = max(populacao_avaliada, key=lambda x: x[0])
        melhores_individuos.append(melhor_individuo)

        # Calcula a média dos pesos do melhor cromossomo da geração
        _, peso_total_melhor = fitness(melhor_individuo[1])
        media_pesos_melhor_individuo = peso_total_melhor / sum(melhor_individuo[1]) if sum(melhor_individuo[1]) > 0 else 0
        medias_pesos_melhores_individuos.append(media_pesos_melhor_individuo)

        # Exibe informações da geração atual
        print(f"Geração {geracao + 1}: Melhor valor = {melhor_individuo[0]}, Cromossomo = {melhor_individuo[1]}, Média dos pesos do melhor cromossomo = {media_pesos_melhor_individuo}")

        # Seleciona a melhor metade da população
        populacao = [individuo for _, individuo in selecionar(populacao_avaliada)]

        # Realiza crossover para gerar novos indivíduos
        nova_populacao = []
        while len(nova_populacao) < num_individuos:
            pai = random.choice(populacao)
            mae = random.choice(populacao)
            filho1, filho2 = crossover(pai, mae)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        # Aplica mutação na nova população
        for individuo in nova_populacao:
            mutacao(individuo)

        populacao = nova_populacao

    # Exibe o melhor valor e cromossomo final
    melhor_valor_final, melhor_cromossomo_final = max(melhores_individuos, key=lambda x: x[0])
    print(f"\nMelhor indivíduo final: {melhor_cromossomo_final}, Valor: {melhor_valor_final}")

    return medias_pesos_melhores_individuos, melhores_individuos

# Executa o algoritmo genético
medias_pesos_melhores_individuos, melhores_individuos = algoritmo_genetico()

# Exibe a lista do melhor indivíduo de cada geração
print("\nMelhores indivíduos de cada geração:")
for i, (valor, individuo) in enumerate(melhores_individuos):
    print(f"Geração {i+1}: Valor = {valor}, Cromossomo = {individuo}")

# Exibe a média dos pesos do melhor cromossomo de cada geração
print("\nMédias dos pesos do melhor cromossomo de cada geração:")
for i, media in enumerate(medias_pesos_melhores_individuos):
    print(f"Geração {i+1}: Média dos pesos = {media}")
