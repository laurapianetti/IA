import time
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# População inicial corresponde aos anticorpos
def populacao_inicial(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = np.random.uniform(0.1, 10, (3, 4))  # 3 vetores, cada um com 4 atributos
        populacao.append(individuo)
    return np.array(populacao)

# Calcula afinidades dos anticorpos com base na porcentagem de acerto das classificações
def afinidades(anticorpos, X, y):
    afinidades = []

    for individuo in anticorpos:
        predicoes = []
        for x in X:
            # Calcula distâncias entre x (características do antígeno) e os 3 vetores do indivíduo
            distancias = np.linalg.norm(individuo - x, axis=1)
            classe_previsao = np.argmin(distancias)
            predicoes.append(classe_previsao)   
        
        predicoes = np.array(predicoes)
        acertos = np.sum(predicoes == y)
        fitness = acertos / len(y)
        afinidades.append(fitness)

    return np.array(afinidades)


def selecao_melhores_afinidades(anticorpos, afinidades, m):
    indices = np.argsort(afinidades)[-m:]  # Seleciona os M maiores afinidades
    return anticorpos[indices], afinidades[indices]

def clonagem(anticorpos, afinidades, total_clones):
    soma_afinidades = np.sum(afinidades)
    clones = []
    clones_qtd = []
    clones_qtd_int = []

    # Calcula quantidade de clones em float e armazena
    for i in range(len(anticorpos)):
        qtd = (afinidades[i] / soma_afinidades) * total_clones
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
def hipermutacao(anticorpos, afinidades, beta=0.05):
    afin_max = np.max(afinidades)
    taxas_mutacao = (1 - (afinidades / afin_max)) * beta
    anticorpos_mutada = []

    for i in range(len(anticorpos)):
        mutacao = np.random.normal(0, taxas_mutacao[i], size=anticorpos[i].shape)
        anticorpos_mutada.append(anticorpos[i] + mutacao)

    return np.array(anticorpos_mutada)

# Gera os indivíduos que faltam após clonagem
def nova_geracao(num_anticorpos, total_clones):
    qntd = num_anticorpos - total_clones
    return populacao_inicial(qntd)

# Função principal do Algoritmo Imunológico
def clonalg(num_anticorpos, num_geracoes, m, total_clones, X_train, y_train):
    anticorpos = populacao_inicial(num_anticorpos)

    for _ in range(num_geracoes):
        melhores_anti, afinidades_melhores = selecao_melhores_afinidades(anticorpos, afinidades(anticorpos, X_train, y_train), m)
        clones = clonagem(melhores_anti, afinidades_melhores, total_clones)
        clones = hipermutacao(clones, afinidades(clones, X_train, y_train))
        novos = nova_geracao(num_anticorpos, total_clones)
        anticorpos = np.vstack((clones, novos))

    # Encontra o anticorpo com a maior afinidade (melhor solução encontrada)
    afinidades_finais = afinidades(anticorpos, X_train, y_train)
    indice_melhor = np.argmax(afinidades_finais)
    melhor_solucao = anticorpos[indice_melhor]
    return melhor_solucao

# Avaliação no conjunto de teste
def avaliar_solucao(individuo, X, y):
    predicoes = []
    for x in X:
        distancias = np.linalg.norm(individuo - x, axis=1)
        classe_predita = np.argmin(distancias)
        predicoes.append(classe_predita)
    predicoes = np.array(predicoes)
    return np.mean(predicoes == y)

if __name__ == "__main__":
    num_anticorpos = 50
    num_geracoes = 40
    m = 5
    total_clones = 45

    inicio = time.time() # marca o tempo de execução

    iris = load_iris() # Carrega o dataset Iris
    X = iris.data # Atributos (largura e comprimento das pétalas e sépalas)
    y = iris.target # Rótulos (espécies de flores)
    
    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=42)

    # Executando o algoritmo imunológico
    melhor_solucao = clonalg(num_anticorpos, num_geracoes, m, total_clones, X_train, y_train)

    fim = time.time() # marca o tempo de execução

    print("Melhor solução encontrada (vetores protótipos por classe):\n", melhor_solucao)
    acuracia_teste = avaliar_solucao(melhor_solucao, X_test, y_test)
    print(f"Acurácia no conjunto de teste: {acuracia_teste:.4f}")
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")

    # Nomes das classes de flores
    nomes_classes = iris.target_names
    cores = ['r', 'g', 'b']

    # Gráfico para SÉPALAS (atributos 0 e 1)
    plt.figure(figsize=(8, 6))
    for classe, cor in zip(np.unique(y), cores):
        plt.scatter(X[y == classe, 0], X[y == classe, 1], label=nomes_classes[classe], alpha=0.5, color=cor)
    for i, (vetor, cor) in enumerate(zip(melhor_solucao, cores)):
        plt.arrow(0, 0, vetor[0], vetor[1], head_width=0.2, head_length=0.3, fc=cor, ec=cor, linewidth=2, length_includes_head=True)
        plt.text(vetor[0], vetor[1], f'Protótipo {nomes_classes[i]}', fontsize=10, color=cor)
    plt.xlabel('Comprimento da Sépala')
    plt.ylabel('Largura da Sépala')
    plt.title('Sépalas - Dados e Vetores Protótipos')
    plt.legend()
    plt.grid()
    plt.show()

    # Gráfico para PÉTALAS (atributos 2 e 3)
    plt.figure(figsize=(8, 6))
    for classe, cor in zip(np.unique(y), cores):
        plt.scatter(X[y == classe, 2], X[y == classe, 3], label=nomes_classes[classe], alpha=0.5, color=cor)
    for i, (vetor, cor) in enumerate(zip(melhor_solucao, cores)):
        plt.arrow(0, 0, vetor[2], vetor[3], head_width=0.2, head_length=0.3, fc=cor, ec=cor, linewidth=2, length_includes_head=True)
        plt.text(vetor[2], vetor[3], f'Protótipo {nomes_classes[i]}', fontsize=10, color=cor)
    plt.xlabel('Comprimento da Pétala')
    plt.ylabel('Largura da Pétala')
    plt.title('Pétalas - Dados e Vetores Protótipos')
    plt.legend()
    plt.grid()
    plt.show()