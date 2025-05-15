import numpy as np
import matplotlib.pyplot as plt
import time
import random
from matplotlib.animation import FuncAnimation

# Variáveis globais para os parâmetros do gráfico
melhores_fitness = []
fitness_medio = []
populacoes_geracoes = []

# Função Alpine2
def alpine2(x):
    return np.prod(np.sqrt(x) * np.sin(x))

# Função para definir a população inicial (aleatoriamente)
def populacao_inicial(tamanho_populacao, num_dimensoes):
    return [np.random.uniform(0.1, 10, num_dimensoes) for _ in range(tamanho_populacao)]

# Função para definir o fitness (própria função)
def fitness(individuo):
    return alpine2(individuo)

# Função para fazer a seleção dos pais (torneio)
def selecao_torneio(populacao, tamanho_torneio):
    pais = []
    for _ in range(tamanho_torneio):
        torneio = random.sample(populacao, tamanho_torneio)
        torneio.sort(key=fitness, reverse=True)
        pais.append(torneio[0])
    return pais

# Função para cruzar dois indivíduos 
def recombinacao(pai1, pai2, alpha=0.3):
    p1, p2 = np.array(pai1), np.array(pai2)
    d = np.abs(p1 - p2)
    low = np.minimum(p1, p2) - alpha * d
    high = np.maximum(p1, p2) + alpha * d
    return np.random.uniform(low, high)

# Função para aplicar mutação em um indivíduo (perturbação gaussiana)
def mutacao(individuo, taxa_mutacao, sigma=0.5):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] += np.random.normal(0, sigma)
            individuo[i] = np.clip(individuo[i], 0.1, 10)
    return individuo

# Função para criar a nova geração
def nova_geracao(populacao, taxa_mutacao, tamanho_torneio):
    nova_populacao = []
    while len(nova_populacao) < len(populacao):
        pais = selecao_torneio(populacao, tamanho_torneio)
        filho = recombinacao(pais[0], pais[1])
        filho_mutado = mutacao(filho, taxa_mutacao)
        nova_populacao.append(filho_mutado)
    return nova_populacao

# Função principal do Algoritmo Genético
def algoritmo_genetico(tamanho_populacao, num_dimensoes, num_geracoes, taxa_mutacao, tamanho_torneio):
    populacao = populacao_inicial(tamanho_populacao, num_dimensoes)

    for _ in range(num_geracoes):
        populacao = nova_geracao(populacao, taxa_mutacao, tamanho_torneio)
        # Salva a população de cada geração
        populacoes_geracoes.append(populacao)

        # Calcula o fitness máximo e médio da população
        fitness_geracao = [fitness(individuo) for individuo in populacao]
        melhores_fitness.append(max(fitness_geracao))
        fitness_medio.append(sum(fitness_geracao) / len(fitness_geracao))

    melhor_solucao = max(populacao, key=fitness)
    return melhor_solucao

if __name__ == "__main__":
    # Definindo os parâmetros do algoritmo genético
    num_dimensoes = 2
    tamanho_populacao = 100
    num_geracoes = 50
    taxa_mutacao = 0.1
    tamanho_torneio = 3

    inicio = time.time() # marca o tempo de execução

    # Executando o algoritmo genético
    melhor_solucao = algoritmo_genetico(tamanho_populacao, num_dimensoes, num_geracoes, taxa_mutacao, tamanho_torneio)

    fim = time.time() # marca o tempo de execução

    melhor_solucao = np.round(melhor_solucao, 4)
    print(f"Para n = {num_dimensoes} o máximo é de {alpine2(melhor_solucao):.4f} em x*={melhor_solucao}")
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")

    # Gerar o vídeo da convergência com os indivíduos ao longo das gerações
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')

    pontos, = ax.plot([], [], 'o', label='Indivíduos', color='blue')
    ax.legend()

    def atualizar(frame):
        geracao = populacoes_geracoes[frame]
        x1 = [ind[0] for ind in geracao]
        x2 = [ind[1] for ind in geracao]
        pontos.set_data(x1, x2)
        ax.set_title(f'Evolução dos Indivíduos - Geração {frame + 1} de {num_geracoes}')
        return pontos,

    anim = FuncAnimation(fig, atualizar, frames=num_geracoes, interval=200, blit=False)

    anim.save('evolucao_individuos.mp4', writer='ffmpeg')
    plt.show()