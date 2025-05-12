import random
import time

# Função para gerar a população inicial (aleatoriamente)
def populacao_inicial(tamanho_populacao, tamanho_individuo, itens, peso_mochila):
    populacao = []
    while len(populacao) < tamanho_populacao:
        individuo = [random.randint(0, 1) for _ in range(tamanho_individuo)]
        if calcular_valor_peso(individuo, itens)[0] <= peso_mochila:
            populacao.append(individuo)
    return populacao

# Função para calcular o fitness de um indivíduo
def fitness(individuo, itens, peso_mochila):
    peso_total = 0
    valor_total = 0
    for i in range(len(individuo)):
        if individuo[i] == 1:
            peso_total += itens[i][0]
            valor_total += itens[i][1]
            if peso_total > peso_mochila:
                return 0
            
    return valor_total

# Função para selecionar os pais usando o torneio
def selecao_torneio(populacao, tamanho_torneio, itens, peso_mochila):
    pais = []
    for _ in range(tamanho_torneio):
        torneio = random.sample(populacao, tamanho_torneio)
        torneio.sort(key=lambda ind: fitness(ind, itens, peso_mochila), reverse=True)
        pais.append(torneio[0])
    return pais

# Função para cruzar dois indivíduos (recombinação de ponto único)
def recombinacao(pai1, pai2):
    ponto_cruzamento = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_cruzamento] + pai2[ponto_cruzamento:]
    filho2 = pai2[:ponto_cruzamento] + pai1[ponto_cruzamento:]
    return filho1, filho2

# Função para aplicar mutação em um indivíduo (inverte bits)
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]  # Inverte o bit 
    return individuo

# Função para criar a nova geração
def nova_geracao(populacao, taxa_mutacao, tamanho_torneio, itens, peso_mochila):
    nova_populacao = []
    while len(nova_populacao) < len(populacao):
        pais = selecao_torneio(populacao, tamanho_torneio, itens, peso_mochila)
        filhos = recombinacao(pais[0], pais[1])
        nova_populacao.append(mutacao(filhos[0], taxa_mutacao))
        nova_populacao.append(mutacao(filhos[1], taxa_mutacao))
    return nova_populacao

# Função para calcular o valor total e o peso total de um indivíduo
def calcular_valor_peso(individuo, itens):
    peso_total = sum(itens[i][0] for i in range(len(individuo)) if individuo[i] == 1)
    valor_total = sum(itens[i][1] for i in range(len(individuo)) if individuo[i] == 1)
    return peso_total, valor_total

# Função principal do algoritmo genético
def algoritmo_genetico(tamanho_populacao, tamanho_individuo, itens, peso_mochila, taxa_mutacao, tamanho_torneio, geracoes):
    populacao = populacao_inicial(tamanho_populacao, tamanho_individuo, itens, peso_mochila)
    for _ in range(geracoes):
        populacao = nova_geracao(populacao, taxa_mutacao, tamanho_torneio, itens, peso_mochila)
    melhor_individuo = max(populacao, key=lambda ind: fitness(ind, itens, peso_mochila))
    return melhor_individuo

# Função para criar os itens (peso e valor)
def criar_itens(quantidade_itens):
    itens = []
    for i in range(quantidade_itens):
        peso = random.randint(1, 20)
        valor = random.randint(10, 100)
        itens.append((peso, valor))
    return itens

# Main
if __name__ == "__main__":
    # Definindo os parâmetros do problema
    capacidade_mochila = 30
    peso_mochila = 50
    itens = criar_itens(capacidade_mochila)
    tamanho_populacao = 5
    tamanho_individuo = len(itens)
    taxa_mutacao = 0.03
    tamanho_torneio = 3
    geracoes = 50

    inicio = time.time() # marca o tempo de execução

    # Executando o algoritmo genético
    melhor_solucao = algoritmo_genetico(tamanho_populacao, tamanho_individuo, itens, peso_mochila, taxa_mutacao, tamanho_torneio, geracoes)

    fim = time.time() # marca o tempo de execução
    
    # Calculando o valor e peso da melhor solução encontrada
    peso_total, valor_total = calcular_valor_peso(melhor_solucao, itens)

    print(f"Soma dos pesos: {peso_total}")
    print(f"Soma dos valores: {valor_total}")
    print(f"Tempo de execução: {fim - inicio}")