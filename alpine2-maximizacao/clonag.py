import numpy as np
import matplotlib.pyplot as plt
import time
import random
from matplotlib.animation import FuncAnimation

# Função Alpine2
def alpine2(x):
    return np.prod(np.sqrt(x) * np.sin(x))

# Função para definir a população inicial (aleatoriamente)
def anticorpos_inicial(num_anticorpos, num_dimensoes):
    return [np.random.uniform(0.1, 10, num_dimensoes) for _ in range(num_anticorpos)]

# Função para definir afinidades (própria função)
def afinidades(anticorpos):
    afinidades = []
    for anticorpo in anticorpos:
        afinidades.append(alpine2(anticorpo))
    return afinidades

def selecao_melhores_afinidades(anticorpos, afinidades, m):
    indices = np.argsort(afinidades)[-m:]  # Seleciona os M maiores afinidades
    return anticorpos[indices], afinidades[indices]


def clonagem(anticorpos, afinidades, total_clones):
    soma_afinidades = np.sum(afinidades)
    clones = []
    for i in range(len(anticorpos)):
        qtd_clones = int((afinidades[i] / soma_afinidades) * total_clones)
        clones.extend([anticorpos[i]] * qtd_clones)
    return np.array(clones)

# Hipermutação: anticorpos melhores tem mutação menor e piores tem mutação maior
def hipermutacao(anticorpos, afinidades, beta=0.1):
    afin_max = np.max(afinidades)
    taxas_mutacao = (1 - (afinidades / afin_max)) * beta
    anticorpos_mutada = []

    for i in range(len(anticorpos)):
        mutacao = np.random.normal(0, taxas_mutacao[i], size=anticorpos[i].shape)
        anticorpos_mutada.append(anticorpos[i] + mutacao)

    return np.array(anticorpos_mutada)

# Função para gerar os indivíduos que faltam após clonagem
def nova_geracao(num_anticorpos, total_clones, num_dimensoes):
    qntd = num_anticorpos - total_clones
    return anticorpos_inicial(qntd, num_dimensoes)

# Função principal do Algoritmo Imunológico
def clonalg(num_anticorpos, num_dimensoes, num_geracoes, m, total_clones):
    anticorpos = anticorpos_inicial(num_anticorpos, num_dimensoes)

    for _ in range(num_geracoes):
        melhores_anti, afinidades_melhores = selecao_melhores_afinidades(anticorpos, afinidades(anticorpos), m)
        clones = clonagem(melhores_anti, afinidades_melhores, total_clones)
        clones = hipermutacao(clones, afinidades(clones))
        novos = nova_geracao(num_anticorpos, total_clones, num_dimensoes)
        anticorpos = np.vstack((clones, novos))

    afin = afinidades(anticorpos)
    idx_melhor = np.argmax(afin)
    melhor_solucao = anticorpos[idx_melhor]
    return melhor_solucao, idx_melhor

if __name__ == "__main__":
    num_dimensoes = 2
    num_anticorpos = 50
    num_geracoes = 40
    m = 5
    total_clones = 45

    inicio = time.time() # marca o tempo de execução

    # Executando o algoritmo imunológico
    melhor_solucao = clonalg(num_anticorpos, num_dimensoes, num_geracoes, m, total_clones)

    fim = time.time() # marca o tempo de execução

    print(f"Para n = {num_dimensoes} o máximo é de {alpine2(melhor_solucao):.4f} em x*={melhor_solucao}")
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")