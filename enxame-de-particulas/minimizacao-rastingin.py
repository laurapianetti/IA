import numpy as np
import matplotlib.pyplot as plt

def rastrigin(x, A=10):
    x = np.asarray(x)
    n = len(x)
    return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))

def inicializa_nuvem_particulas(num_particulas, dim=2):
    return np.random.uniform(-5.12, 5.12, (num_particulas, dim))

def fitness(x):
    return rastrigin(x)

def ponderacao_inercia(w_min, w_max, iteracao, num_iteracoes):
    return w_max - (w_max - w_min) * (iteracao / num_iteracoes)

def calcula_velocidade(velocidade, posicao, melhor_individual, melhor_global, w_min, w_max, c1, c2, iteracao, num_iteracoes):
    r1 = np.random.uniform(0, 1)
    r2 = np.random.uniform(0, 1)
    vel_cognitiva = c1 * r1 * (melhor_individual - posicao)
    vel_social = c2 * r2 * (melhor_global - posicao)
    w = ponderacao_inercia(w_min, w_max, iteracao, num_iteracoes)
    return w * velocidade + vel_cognitiva + vel_social

def calcula_posicao(posicao, velocidade):
    return posicao + velocidade

def enxame_de_particulas(num_particulas, num_iteracoes, w_min, w_max, c1, c2):
    # Inicializa partículas
    posicoes = inicializa_nuvem_particulas(num_particulas)
    velocidades = np.zeros_like(posicoes)
    
    # Inicializa melhores individuais e global
    melhores_individuais = posicoes.copy()
    melhor_global = posicoes[np.argmin([fitness(p) for p in posicoes])]    
    
    for it in range(num_iteracoes):
        for i in range(num_particulas):
            # Calcula a velocidade da partícula
            velocidades[i] = calcula_velocidade(velocidades[i], posicoes[i], melhores_individuais[i], melhor_global, w_min, w_max, c1, c2, it, num_iteracoes)
            # Atualiza a posição da partícula
            posicoes[i] = calcula_posicao(posicoes[i], velocidades[i])
            
            # Atualiza o melhor individual
            if fitness(posicoes[i]) < fitness(melhores_individuais[i]):
                melhores_individuais[i] = posicoes[i]
        
        # Atualiza o melhor global
        melhor_global = melhores_individuais[np.argmin([fitness(p) for p in melhores_individuais])]    
    
    return melhor_global, fitness(melhor_global)

if __name__ == "__main__":
    # Parâmetros do algoritmo
    num_particulas = 1000  # Número de partículas na nuvem
    num_iteracoes = 100  # Número de iterações do algoritmo
    c1 = 1  # Coeficiente cognitivo
    c2 = 4  # Coeficiente social
    w_min = 0.4  # Peso de inércia mínimo
    w_max = 0.9  # Peso de inércia máximo

    # Executando o algoritmo de enxame de partículas
    melhor_posicao, melhor_valor = enxame_de_particulas(num_particulas, num_iteracoes, w_min, w_max, c1, c2)
    print(f"Melhor posição encontrada: {[f'{x:.2f}' for x in melhor_posicao]}")
    print(f"Melhor valor da função Rastrigin: {melhor_valor:.2f}")

    