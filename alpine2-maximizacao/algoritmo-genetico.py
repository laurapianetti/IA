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

# Função para cruzar dois indivíduos (crossover BLX‑α)
def recombinacao(pai1, pai2, alfa=0.3):
    p1, p2 = np.array(pai1), np.array(pai2)
    d = np.abs(p1 - p2)
    menor = np.minimum(p1, p2) - alfa * d
    maior = np.maximum(p1, p2) + alfa * d
    return np.random.uniform(menor, maior)

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
    num_geracoes = 40
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
    fig, ax = plt.subplots(figsize=(6,6))
    fig.canvas.manager.set_window_title('Algoritmo Genético - Maximização Alpine2')
    ax.set_xlim(0.1, 10)
    ax.set_ylim(0.1, 10)
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')

    # Plota as curvas de nível da função Alpine2
    xs = np.linspace(0.1, 10, 300)
    ys = np.linspace(0.1, 10, 300)
    X, Y = np.meshgrid(xs, ys)
    Z = np.sqrt(X)*np.sin(X) * np.sqrt(Y)*np.sin(Y)
    contours = ax.contour(
        X, Y, Z,
        levels=20,     
        cmap='viridis',
        alpha=0.6
    )
    fig.colorbar(contours, ax=ax, label='alpine2(x1,x2)')

    # Plota os pontos da população (inicialmente vazios)
    pontos, = ax.plot([], [], 'o', color='blue', ms=4, label='Indivíduos')
    ax.legend(loc='upper right')

    # Função de atualização dos pontos a cada frame
    def atualizar(frame):
        ger = populacoes_geracoes[frame]
        x1 = [ind[0] for ind in ger]
        x2 = [ind[1] for ind in ger]
        pontos.set_data(x1, x2)
        ax.set_title(f'Geração {frame+1} de {num_geracoes}')
        return pontos,

    # Monta e salva a animação
    anim = FuncAnimation(fig, atualizar,
                         frames=num_geracoes,
                         interval=200,
                         blit=False)
    anim.save('evolucao_individuos.mp4', writer='ffmpeg', dpi=200)
    plt.show()

    # Gerar o gráfico da evolução do fitness médio e do melhor fitness
    fig = plt.figure(figsize=(8, 5))
    fig.canvas.manager.set_window_title('Algoritmo Genético - Maximização Alpine2')
    plt.plot(range(1, num_geracoes+1), melhores_fitness,   label='Melhor Fitness')
    plt.plot(range(1, num_geracoes+1), fitness_medio,      label='Fitness Médio')
    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.title('Evolução do Fitness ao Longo das Gerações')
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('evolucao_fitness.png', dpi=300)

    plt.show()