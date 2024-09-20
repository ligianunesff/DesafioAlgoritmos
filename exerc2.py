import random
import numpy as np

# Função objetivo: f(x) = x^3 - 6x + 14
def funcao_objetivo(x):
    return x**3 - 6*x + 14

# Função para converter binário para número real na faixa [-10, 10]
def binario_para_real(cromossomo, n_bits=16, min_val=-10, max_val=10):
    decimal = int(''.join(map(str, cromossomo)), 2)
    proporcao = decimal / (2**n_bits - 1)
    return min_val + proporcao * (max_val - min_val)

# Função de fitness: minimizar a função objetivo quanto menor o valor, melhor o cromossomo
def fitness(cromossomo):
    x = binario_para_real(cromossomo)
    return -funcao_objetivo(x)  # Inverte o sinal para transformar em problema de maximização

# Inicializa a população de forma aleatória
def inicializar_populacao(tamanho_populacao, n_bits):
    return [[random.randint(0, 1) for _ in range(n_bits)] for _ in range(tamanho_populacao)]

# Seleção por torneio
def selecao_torneio(populacao, fitness_pop, k=3):
    selecionados = random.sample(range(len(populacao)), k)
    melhor_individuo = max(selecionados, key=lambda idx: fitness_pop[idx])
    return populacao[melhor_individuo]

# Crossover de 1 ponto
def crossover(pai, mae, n_pontos=1):
    if n_pontos == 1:
        ponto_corte = random.randint(1, len(pai) - 1)
        filho1 = pai[:ponto_corte] + mae[ponto_corte:]
        filho2 = mae[:ponto_corte] + pai[ponto_corte:]
    else:  # Crossover de 2 pontos
        ponto1 = random.randint(1, len(pai) - 2)
        ponto2 = random.randint(ponto1 + 1, len(pai) - 1)
        filho1 = pai[:ponto1] + mae[ponto1:ponto2] + pai[ponto2:]
        filho2 = mae[:ponto1] + pai[ponto1:ponto2] + mae[ponto2:]
    return filho1, filho2

# Mutação
def mutacao(cromossomo, taxa_mutacao):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            cromossomo[i] = 1 - cromossomo[i]  # Inverte o bit

# Elitismo: preserva os melhores indivíduos
def aplicar_elitismo(populacao, fitness_pop, porcentagem_elite):
    num_elite = int(porcentagem_elite * len(populacao))
    elite_indices = sorted(range(len(fitness_pop)), key=lambda i: fitness_pop[i], reverse=True)[:num_elite]
    return [populacao[i] for i in elite_indices]

# Algoritmo genético
def algoritmo_genetico(tamanho_populacao=10, n_geracoes=100, taxa_mutacao=0.01, n_bits=16, n_pontos_crossover=1, usar_elitismo=True, porcentagem_elite=0.1):
    # Inicializa a população
    populacao = inicializar_populacao(tamanho_populacao, n_bits)

    for geracao in range(n_geracoes):
        fitness_pop = [fitness(individuo) for individuo in populacao]

        # Exibe o melhor indivíduo da geração
        melhor_individuo = populacao[np.argmax(fitness_pop)]
        melhor_valor_x = binario_para_real(melhor_individuo)
        melhor_valor_funcao = funcao_objetivo(melhor_valor_x)
        print(f"Geração {geracao + 1}: Melhor x = {melhor_valor_x}, f(x) = {melhor_valor_funcao}")

        # Elitismo
        nova_populacao = aplicar_elitismo(populacao, fitness_pop, porcentagem_elite) if usar_elitismo else []

        # Preenche nova população por crossover
        while len(nova_populacao) < tamanho_populacao:
            pai = selecao_torneio(populacao, fitness_pop)
            mae = selecao_torneio(populacao, fitness_pop)
            filho1, filho2 = crossover(pai, mae, n_pontos=n_pontos_crossover)
            mutacao(filho1, taxa_mutacao)
            mutacao(filho2, taxa_mutacao)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        # Substitui a população pela nova
        populacao = nova_populacao[:tamanho_populacao]

    # Retorna o melhor indivíduo da última geração
    melhor_individuo = populacao[np.argmax(fitness_pop)]
    melhor_valor_x = binario_para_real(melhor_individuo)
    melhor_valor_funcao = funcao_objetivo(melhor_valor_x)
    return melhor_valor_x, melhor_valor_funcao

# Parâmetros do algoritmo genético
tamanho_populacao = 10
n_geracoes = 100
taxa_mutacao = 0.01
n_bits = 16
n_pontos_crossover = 2
usar_elitismo = True
porcentagem_elite = 0.1

# Executa o algoritmo genético
melhor_x, melhor_valor_funcao = algoritmo_genetico(tamanho_populacao, n_geracoes, taxa_mutacao, n_bits, n_pontos_crossover, usar_elitismo, porcentagem_elite)

print(f"\nMelhor valor encontrado: x = {melhor_x}, f(x) = {melhor_valor_funcao}")
