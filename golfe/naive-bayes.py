import pandas as pd

def cria_conjunto_dados():
    dados = {
    'Outlook': ['Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny', 'Rainy', 'Overcast', 'Overcast', 'Sunny'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    'Windy': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    'Play Golf': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
    }

    return pd.DataFrame(dados)

def naive_bayes(outlook, temperature, humidity, windy, dados):
    total = len(dados)
    sim = dados[dados['Play Golf'] == 'Yes']
    nao = dados[dados['Play Golf'] == 'No']

    qntd_sim = len(sim)
    qntd_nao = len(nao)

    v_sim = qntd_sim / total
    v_nao = qntd_nao / total

    # Jogar golfe
    v_outlook_sim = len(sim[sim['Outlook'] == outlook]) / qntd_sim
    v_temperature_sim = len(sim[sim['Temperature'] == temperature]) / qntd_sim
    v_humidity_sim = len(sim[sim['Humidity'] == humidity]) / qntd_sim
    v_windy_sim = len(sim[sim['Windy'] == windy]) / qntd_sim
    v_jogar = v_sim * v_outlook_sim * v_temperature_sim * v_humidity_sim * v_windy_sim

    # Não jogar golfe
    v_outlook_nao = len(nao[nao['Outlook'] == outlook]) / qntd_nao
    v_temperature_nao = len(nao[nao['Temperature'] == temperature]) / qntd_nao
    v_humidity_nao = len(nao[nao['Humidity'] == humidity]) / qntd_nao
    v_windy_nao = len(nao[nao['Windy'] == windy]) / qntd_nao
    v_nao_jogar = v_nao * v_outlook_nao * v_temperature_nao * v_humidity_nao * v_windy_nao

    return v_jogar, v_nao_jogar 

def calcula_probabilidades(v_jogar, v_nao_jogar):
    total = v_jogar + v_nao_jogar
    prob_jogar = v_jogar / total
    prob_nao_jogar = v_nao_jogar / total
    return prob_jogar, prob_nao_jogar

if __name__ == "__main__":
    # Lê os valores do usuário
    outlook = input("Digite o Outlook (Sunny, Overcast, Rainy): ")
    temperature = input("Digite a Temperature (Hot, Mild, Cool): ")
    humidity = input("Digite a Humidity (High, Normal): ")
    windy = input("Digite o Windy (Weak, Strong): ")

    dados = cria_conjunto_dados()
    v_jogar, v_nao_jogar = naive_bayes(outlook, temperature, humidity, windy, dados)

    prob_jogar, prob_nao_jogar = calcula_probabilidades(v_jogar, v_nao_jogar)

    # Imprime resultado
    if v_jogar > v_nao_jogar:
        print("Você deve jogar golfe!")
    else:
        print("Você não deve jogar golfe.")

    print(f"A probabilidade de jogar golfe é: {prob_jogar*100:.2f}%")
    print(f"A probabilidade de não jogar golfe é: {prob_nao_jogar*100:.2f}%")
