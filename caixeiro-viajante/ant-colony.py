import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

# Calcula a probabilidade de transição entre cidades por meio da fórmula
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

# Calcula a distância total do caminho percorrido pelas formigas
def calcula_distancia_total(matriz_dist, caminho):
    dist = sum(float(matriz_dist[caminho[i]][caminho[i + 1]]) for i in range(len(caminho) - 1))
    dist += float(matriz_dist[caminho[-1]][caminho[0]])  # Volta para a cidade inicial 
    return dist

# Calcula o depósito de feromônio deixado pelas formigas em cada aresta do caminho percorrido
def calcula_deposito_feromonio(caminho, num_cidades, feromonio_excretado, matriz_dist):
    matriz_deposito = np.zeros((num_cidades, num_cidades))
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]
        matriz_deposito[cidade_atual][proxima_cidade] += feromonio_excretado / float(matriz_dist[cidade_atual][proxima_cidade])
        matriz_deposito[proxima_cidade][cidade_atual] += feromonio_excretado / float(matriz_dist[proxima_cidade][cidade_atual])
    
    return matriz_deposito
        
# Atualiza o nível de feromônio na matriz com base na taxa de evaporação e no depósito de feromônio
def atualiza_nivel_feromonio(matriz_feromonio, num_cidades, taxa_evaporacao, matriz_deposito):
    for i in range(num_cidades):
        for j in range(num_cidades):
            matriz_feromonio[i][j] = taxa_evaporacao * matriz_feromonio[i][j] + matriz_deposito[i][j] 

    return matriz_feromonio

# Algoritmo de Colônia de Formigas para o problema do Caixeiro Viajante
def algoritmo_ant_colony(matriz_dist, num_cidades, num_formigas, matriz_feromonio, num_iteracoes):
    melhor_caminho = None
    melhor_distancia = float('inf')
    historico_melhor_distancia = [] # Para fazer o gráfico de evolução

    for _ in range(num_iteracoes):
        caminhos = []
        distancias = []
        for _ in range(num_formigas):
            caminho = []
            cidades_nao_visitadas = list(range(num_cidades))
            cidade_atual = np.random.choice(cidades_nao_visitadas)
            caminho.append(cidade_atual)
            cidades_nao_visitadas.remove(cidade_atual)

            while cidades_nao_visitadas:
                prob_transicao = calcula_prob_transicao(matriz_dist, matriz_feromonio, cidade_atual, cidades_nao_visitadas)
                prob_cidades_nao_visitadas = prob_transicao[cidades_nao_visitadas] # Seleciona apenas as probabilidades das cidades não visitadas
                prob_cidades_nao_visitadas = prob_cidades_nao_visitadas / prob_cidades_nao_visitadas.sum()
                proxima_cidade = np.random.choice(cidades_nao_visitadas, p=prob_cidades_nao_visitadas)
                caminho.append(proxima_cidade)
                cidades_nao_visitadas.remove(proxima_cidade)
                cidade_atual = proxima_cidade

            # Calcula a distância total do caminho
            distancia_total = calcula_distancia_total(matriz_dist, caminho)
            caminhos.append(caminho)
            distancias.append(distancia_total)

            # Atualiza o melhor caminho e distância se necessário
            if distancia_total < melhor_distancia:
                melhor_distancia = distancia_total
                melhor_caminho = caminho
            
        # Soma o depósito de todas as formigas
        matriz_deposito = np.zeros((num_cidades, num_cidades))
        for caminho in caminhos:
            matriz_deposito += calcula_deposito_feromonio(caminho, num_cidades, feromonio_excretado, matriz_dist)

        # Elitismo: reforça o melhor caminho global
        matriz_deposito += calcula_deposito_feromonio(melhor_caminho, num_cidades, feromonio_excretado * parametro_elitismo, matriz_dist)

        matriz_feromonio = atualiza_nivel_feromonio(matriz_feromonio, num_cidades, taxa_evaporacao, matriz_deposito)

        historico_melhor_distancia.append(melhor_distancia)  # Armazena a melhor distância de cada iteração

    return melhor_caminho, melhor_distancia, historico_melhor_distancia

if __name__ == "__main__":
    # Inicialização dos parâmetros do algoritmo
    arq = 'distancia_matrix.csv'
    num_formigas = 10
    num_iteracoes = 200
    taxa_evaporacao = 0.95
    feromonio_excretado = 50
    parametro_elitismo = 2  # Fator de reforço para o melhor caminho encontrado

    matriz_dist = preenche_matriz_dist(arq)
    num_cidades = len(matriz_dist[0])

    matriz_feromonio = inicializa_feromonio(num_cidades)

    # Executa o algoritmo de colônia de formigas
    melhor_caminho, melhor_distancia, historico_ditancias = algoritmo_ant_colony(matriz_dist, num_cidades, num_formigas, matriz_feromonio, num_iteracoes)
    
    print(f"Melhor caminho: {melhor_caminho}")
    print(f"Melhor distância: {melhor_distancia}")

    # Gráfico da evolução das gerações
    fig = plt.figure()
    fig.canvas.manager.set_window_title('Algoritmo de Colônia de Formigas - Problema do Caixeiro Viajante')
    plt.plot(historico_ditancias)
    plt.xlabel('Geração')
    plt.ylabel('Melhor distância encontrada')
    plt.title('Evolução da melhor solução por geração')
    plt.grid()
    plt.show()