import numpy as np

# Dataset corresponde aos antígenos
def gera_dataset():
    dataset = np.array([
        [5.1, 3.5, 1.4, 0.2, 'setosa'],
        [4.9, 3.0, 1.4, 0.2, 'setosa'],
        [4.7, 3.2, 1.3, 0.2, 'setosa'],
        [4.6, 3.1, 1.5, 0.2, 'setosa'],
        [5.0, 3.6, 1.4, 0.2, 'setosa'],
        [5.4, 3.9, 1.7, 0.4, 'setosa'],
        [4.6, 3.4, 1.4, 0.3, 'setosa'],
        [5.0, 3.4, 1.5, 0.2, 'setosa'],
        [4.4, 2.9, 1.4, 0.2, 'setosa'],
        [4.9, 3.1, 1.5, 0.1, 'setosa'],
        [7.0, 3.2, 4.7, 1.4, 'versicolor'],
        [6.4, 3.2, 4.5, 1.5, 'versicolor'],
        [6.9, 3.1, 4.9, 1.5, 'versicolor'],
        [5.5, 2.3, 4.0, 1.3, 'versicolor'],
        [6.5, 2.8, 4.6, 1.5, 'versicolor'],
        [5.7, 2.8, 4.5, 1.3, 'versicolor'],
        [6.3, 3.,  4.,  1.,   'versicolor'],
        [4.,  2.,  3.,   .1 , 'virginica'],
        [6.,   .8 , .6 , .8 , 'virginica']
    ])
    return dataset

# População inicial corresponde aos anticorpos
def populacao_inicial(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = np.random.uniform(0.1, 10, 4) # 4 valores (largura, comprimento, largura, comprimento)
        populacao.append(individuo)
    return np.array(populacao)

def afinidades(anticorpos, dataset):
    afinidades = []
    caracteristicas = dataset[:, :-1].astype(float) 
    rotulos = dataset[:, -1] 

    for individuo in anticorpos:
        predicoes = []
        for _ in range(len(caracteristicas)):
            # Calcula a distância do indivíduo para todos os antígenos
            distancias = np.linalg.norm(caracteristicas - individuo, axis=1)
            # Encontra o índice do antígeno mais próximo
            idx_mais_proximo = np.argmin(distancias)
            # Prediz a classe do mais próximo
            predicoes.append(rotulos[idx_mais_proximo])
        predicoes = np.array(predicoes)
        acertos = np.sum(predicoes == rotulos)
        afinidade = acertos / len(rotulos)  # porcentagem de acertos
        afinidades.append(afinidade)
    return np.array(afinidades)

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
        anticorpos_mutada.append(anticorpos[i] + mutacao)

    return np.array(anticorpos_mutada)

# Gera os indivíduos que faltam após clonagem
def nova_geracao(num_anticorpos, total_clones, num_dimensoes):
    qntd = num_anticorpos - total_clones
    return populacao_inicial(qntd, num_dimensoes)

# Função principal do Algoritmo Imunológico
def clonalg(num_anticorpos, num_dimensoes, num_geracoes, m, total_clones):

if __name__ == "__main__":
    num_anticorpos = 50
    num_geracoes = 40
    m = 5
    total_clones = 45
