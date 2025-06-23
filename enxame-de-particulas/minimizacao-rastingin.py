from matplotlib.animation import FuncAnimation
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
    historico_posicoes = [posicoes.copy()]
    historico_melhor_global = [melhor_global.copy()]

    
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
        
        historico_posicoes.append(posicoes.copy())
        historico_melhor_global.append(melhor_global.copy())


    return historico_posicoes, historico_melhor_global, melhor_global, fitness(melhor_global)

if __name__ == "__main__":
    # Parâmetros do algoritmo
    num_particulas = 50  # Número de partículas na nuvem
    num_iteracoes = 100  # Número de iterações do algoritmo
    c1 = 1.5  # Coeficiente cognitivo
    c2 = 1.5  # Coeficiente social
    w_min = 0.4  # Peso de inércia mínimo
    w_max = 0.9  # Peso de inércia máximo

    # Executando o algoritmo de enxame de partículas
    historico_posicoes, historico_melhor_global, melhor_posicao, melhor_valor = enxame_de_particulas(num_particulas, num_iteracoes, w_min, w_max, c1, c2)
    print(f"Melhor posição encontrada: {[f'{x:.4f}' for x in melhor_posicao]}")
    print(f"Melhor valor da função Rastrigin: {melhor_valor:.4f}")

    # Plotando o resultado
    x = np.linspace(-5.12, 5.12, 200)
    y = np.linspace(-5.12, 5.12, 200)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: rastrigin([x, y]))(X, Y)

    fig, ax = plt.subplots(figsize=(8, 6))
    cont = ax.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(cont, ax=ax)
    scat = ax.scatter([], [], c='red', s=20, label='Partículas')
    best, = ax.plot([], [], 'go', markersize=10, label='Melhor posição')
    ax.set_xlim(-5.12, 5.12)
    ax.set_ylim(-5.12, 5.12)
    ax.set_title('Otimização PSO - Distribuição das partículas')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    def update(frame):
        pos = historico_posicoes[frame]
        best_pos = historico_melhor_global[frame]
        scat.set_offsets(pos[:, :2])
        best.set_data([best_pos[0]], [best_pos[1]])
        ax.set_title(f'Minimização Rastrigin')
        return scat, best

    anim = FuncAnimation(fig, update, frames=len(historico_posicoes), interval=100, blit=True)

    # Para salvar como vídeo (requer ffmpeg)
    anim.save('pso_rastrigin.mp4', writer='ffmpeg')

    plt.show()
    