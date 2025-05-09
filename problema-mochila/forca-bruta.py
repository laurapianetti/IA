# Problema da Mochila - Força Bruta
import random
import time

# Função para resolver o problema da mochila por força bruta
def mochila(peso_mochila, peso_obj, valor_obj, n):
    # condição de parada
    if n == 0 or peso_mochila == 0:
        return (0, 0)
    # se o peso do objeto atual é maior que a capacidade da mochila, testa o próximo objeto
    if peso_obj[n-1] > peso_mochila:
        return mochila(peso_mochila, peso_obj, valor_obj, n-1)
    # caso contrário, testa se é melhor incluir o objeto atual ou não
    else:
        valor_com, peso_com = mochila(peso_mochila - peso_obj[n-1], peso_obj, valor_obj, n-1)
        valor_com += valor_obj[n-1]
        peso_com += peso_obj[n-1]

        valor_sem, peso_sem = mochila(peso_mochila, peso_obj, valor_obj, n-1)

        if valor_com > valor_sem:
            return (valor_com, peso_com)
        else:
            return (valor_sem, peso_sem)

def main():

  # definindo as variáveis do problema
  capacidade_mochila = 30
  peso_mochila = 50
  valor_obj = []
  peso_obj = []

  # gerando os pesos e valores dos objetos aleatoriamente
  for _ in range(capacidade_mochila):
    valor_rand = random.randint(10, 100)
    valor_obj.append(valor_rand)
    peso_rand = random.randint(1, 20)
    peso_obj.append(peso_rand)

  inicio = time.time() # marca o tempo de execução

  valor_total, peso_total = mochila(peso_mochila, peso_obj, valor_obj, capacidade_mochila) 

  fim = time.time() # marca o tempo de execução

  print(f"Soma dos pesos: {peso_total}")
  print(f"Soma dos valores: {valor_total}")
  print(f"Tempo de execução: {fim - inicio}")

if __name__ == "__main__":
  main()