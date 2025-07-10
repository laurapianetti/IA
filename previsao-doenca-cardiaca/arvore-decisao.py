import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

def le_base_dados(arquivo):
    return pd.read_csv(arquivo)

def converte_caracteristicas_em_numeros(dados):
    # Convertendo colunas categóricas para numéricas
    label_encoder = LabelEncoder()
    colunas_categoricas = dados.select_dtypes(include=['object']).columns

    for col in colunas_categoricas:
        dados[col] = label_encoder.fit_transform(dados[col])

    return dados

def retorna_features_e_target(dados):
    # Separando as features e o target
    X = dados.drop(columns=['HeartDisease'])
    y = dados['HeartDisease']
    
    return X, y

def arvore_decisao(X_treino, y_treino, X_teste):
    classificador = DecisionTreeClassifier(random_state=42, max_depth=6, min_samples_split=10, min_samples_leaf=5)
    classificador.fit(X_treino, y_treino)
    return classificador.predict(X_teste)
    
def floresta_aleatoria(X_treino, y_treino, X_teste):
    classificador = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10, min_samples_split=5)
    classificador.fit(X_treino, y_treino)
    return classificador.predict(X_teste)

def analisa_profundidade_floresta(X, y, num_ite=30):
    n_features = X.shape[1]
    medias = []
    profundidades = list(range(1, n_features+1))
    for max_depth in profundidades:
        acuracias = []
        for i in range(num_ite):
            X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=i, stratify=y)
            clf = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=max_depth, min_samples_split=5)
            clf.fit(X_treino, y_treino)
            pred = clf.predict(X_teste)
            acuracias.append(accuracy_score(y_teste, pred))
        medias.append(np.mean(acuracias))
    fig =plt.figure(figsize=(10,5))
    fig.canvas.manager.set_window_title('Análise de Profundidade da Floresta Aleatória')
    plt.plot(profundidades, medias, marker='o')
    plt.xlabel('Profundidade Max')
    plt.ylabel('Média da Acurácia')
    plt.title('Média da Acurácia vs Profundidade da Árvore (max_depth)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('analise_profundidade.png')
    plt.show()

if __name__ == "__main__":
    arquivo = 'heart.csv'
    num_ite = 30

    inicio = time.time()

    dados = le_base_dados(arquivo)
    dados = converte_caracteristicas_em_numeros(dados)

    X, y = retorna_features_e_target(dados)

    acuracias_ad = []
    acuracias_fa = []

    for i in range(num_ite):
        X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=i, stratify=y)

        pred_ad = arvore_decisao(X_treino, y_treino, X_teste)
        acuracias_ad.append(accuracy_score(y_teste, pred_ad))

        pred_fa = floresta_aleatoria(X_treino, y_treino, X_teste)
        acuracias_fa.append(accuracy_score(y_teste, pred_fa))

    media_ad = np.mean(acuracias_ad)
    desvio_ad = np.std(acuracias_ad)

    media_fa = np.mean(acuracias_fa)
    desvio_fa = np.std(acuracias_fa)

    fim = time.time()

    print(f"Árvore de Decisão: {media_ad:.2f} média (std = {desvio_ad:.2f}) em {num_ite} execuções")
    print(f"Floresta Aleatória: {media_fa:.2f} média (std = {desvio_fa:.2f}) em {num_ite} execuções")
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")

    analisa_profundidade_floresta(X, y, num_ite=30)