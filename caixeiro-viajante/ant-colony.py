import csv
import time
import numpy as np

# Le arquivo CSV e preenche a matriz de distâncias
def preenche_matriz_dist(arq):
    matriz = []
    with open(arq, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile)
        for linha in leitor:
            matriz.append(linha)
    return matriz

# Inicializa nível de feromônio como 1 para todas as arestas
def inicializa_feromonio(num_cidades):
    return np.ones((num_cidades, num_cidades))

def calcula_prob_transicao(matriz_dist, matriz_feromonio, cidade_atual, cidades_nao_visitadas):
    num_cidades = len(matriz_dist)
    prob_transicao = np.zeros(num_cidades)

    for i in cidades_nao_visitadas:
        dist = float(matriz_dist[cidade_atual][i])
        if dist > 0:  # Evita divisão por zero
            prob_transicao[i] = matriz_feromonio[cidade_atual][i] / dist

    soma = np.sum(prob_transicao)
    if soma > 0:
        prob_transicao = prob_transicao / soma
    return prob_transicao

def calcula_distancia_total(matriz_dist, caminho):
    dist = sum(float(matriz_dist[caminho[i]][caminho[i + 1]]) for i in range(len(caminho) - 1))
    dist += float(matriz_dist[caminho[-1]][caminho[0]])  # Volta para a cidade inicial 
    return dist

def calcula_deposito_feromonio(caminho, num_cidades, feromonio_excretado):
    # para cada aresta, se pertence ao caminho, calcula o depósito de feromônio
 
        
    

def atualiza_nivel_feromonio(matriz_feromonio, num_cidades, taxa_evaporacao, matriz_deposito):
    for i in range(num_cidades):
        for j in range(num_cidades):
            matriz_feromonio[i][j] = taxa_evaporacao * matriz_feromonio[i][j] + matriz_deposito[i][j] 

    return matriz_feromonio

def algoritmo_ant_colony(matriz_dist, num_cidades, num_formigas, matriz_feromonio, num_iteracoes):
    melhor_caminho = None
    melhor_distancia = float('inf')

    for _ in range(num_iteracoes):
        for _ in range(num_formigas):
            caminho = []
            cidades_nao_visitadas = list(range(num_cidades))
            cidade_atual = np.random.choice(cidades_nao_visitadas)
            caminho.append(cidade_atual)
            cidades_nao_visitadas.remove(cidade_atual)

            while cidades_nao_visitadas:
                prob_transicao = calcula_prob_transicao(matriz_dist, matriz_feromonio, cidade_atual, cidades_nao_visitadas)
                proxima_cidade = np.random.choice(cidades_nao_visitadas, p=prob_transicao) # Escolhe a próxima cidade com base na probabilidade
                caminho.append(proxima_cidade)
                cidades_nao_visitadas.remove(proxima_cidade)
                cidade_atual = proxima_cidade

            # Calcula a distância total do caminho
            distancia_total = calcula_distancia_total(matriz_dist, caminho)

            # Atualiza o melhor caminho e distância se necessário
            if distancia_total < melhor_distancia:
                melhor_distancia = distancia_total
                melhor_caminho = caminho

        matriz_deposito = calcula_deposito_feromonio(caminho, feromonio_excretado)

        matriz_feromonio = atualiza_nivel_feromonio(matriz_feromonio, num_cidades, taxa_evaporacao, matriz_deposito)

    return melhor_caminho, melhor_distancia

if __name__ == "__main__":
    arq = 'distancia_matrix.csv'
    num_formigas = 10
    num_iteracoes = 100
    taxa_evaporacao = 0.95
    feromonio_excretado = 50

    matriz_dist = preenche_matriz_dist(arq)
    num_cidades = len(matriz_dist[0])

    matriz_feromonio = inicializa_feromonio(num_cidades)


    