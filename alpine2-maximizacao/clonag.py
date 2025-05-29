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
    return np.array([np.random.uniform(0.1, 10, num_dimensoes) for _ in range(num_anticorpos)])

# Função para definir afinidades (própria função)
def afinidades(anticorpos):
    return np.array([max(0, alpine2(anticorpo)) for anticorpo in anticorpos])

# Seleciona M melhores anticorpos
def selecao_melhores_afinidades(anticorpos, afinidades, m):
    indices = np.argsort(afinidades)[-m:]  # Seleciona os M maiores afinidades
    return anticorpos[indices], afinidades[indices]


def clonagem(anticorpos, afinidades, total_clones):
    soma_afinidades = np.sum(afinidades)
    clones = []
    clones_qtd = []
    clones_qtd_int = []
    soma = 0

    # Calcula quantidade de clones em float e armazena
    for i in range(len(anticorpos)):
        qtd = (afinidades[i] / soma_afinidades) * total_clones
        soma += qtd
        clones_qtd.append(qtd)
        clones_qtd_int.append(int(qtd))

    # Calcula quantos clones faltam
    dif = round(total_clones - sum(clones_qtd_int))

    # Pega as partes decimais para decidir quem recebe os clones restantes
    partes_decimais = [q - int(q) for q in clones_qtd]
    # Ordem decrescente
    indices_desc = np.argsort(partes_decimais)[::-1]

    # Distribui os clones faltantes para os anticorpos com maiores partes decimais
    for i in range(dif):
        clones_qtd_int[indices_desc[i]] += 1

    # Gera os clones
    for i in range(len(anticorpos)):
        clones.extend([anticorpos[i]] * clones_qtd_int[i])

    return np.array(clones)

# Hipermutação: anticorpos melhores tem mutação menor e piores tem mutação maior
def hipermutacao(anticorpos, afinidades, beta=0.01):
    afin_max = np.max(afinidades)
    taxas_mutacao = (1 - (afinidades / afin_max)) * beta
    anticorpos_mutada = []

    for i in range(len(anticorpos)):
        mutacao = np.random.normal(0, taxas_mutacao[i], size=anticorpos[i].shape)
        novo = anticorpos[i] + mutacao
        novo = np.clip(novo, 0.1, 10)  # Garante que x > 0
        anticorpos_mutada.append(novo)

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

    # Encontra o anticorpo com a maior afinidade (melhor solução encontrada)
    afinidades_vals = afinidades(anticorpos)
    indice_melhor = np.argmax(afinidades_vals)
    melhor_solucao = anticorpos[indice_melhor]
    return melhor_solucao

if __name__ == "__main__":
    num_dimensoes = 2
    num_anticorpos = 300
    num_geracoes = 300
    m = 30
    total_clones = 280

    inicio = time.time() # marca o tempo de execução

    # Executando o algoritmo imunológico
    melhor_solucao = clonalg(num_anticorpos, num_dimensoes, num_geracoes, m, total_clones)

    fim = time.time() # marca o tempo de execução

    print(f"Para n = {num_dimensoes} o máximo é de {alpine2(melhor_solucao):.4f} em x*={melhor_solucao}")
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")