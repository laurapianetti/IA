import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cria os antecedentes com o universo de discurso.
comida = ctrl.Antecedent(np.linspace(0, 1, 100), 'comida')
servico = ctrl.Antecedent(np.linspace(0, 1, 100), 'servico')
gorjeta = ctrl.Consequent(np.linspace(0, 0.2, 100), 'gorjeta')

######### FUNÇÕES DE PERTINÊNCIA #########
# qualidade da comida
comida['ruim'] = fuzz.trimf(comida.universe,  [-0.4, 0, 0.4])
comida['boa'] = fuzz.trimf(comida.universe,  [0.1, 0.5, 0.9])
comida['saborosa'] = fuzz.trimf(comida.universe,  [0.6, 1, 1.4])

# servico
servico['ruim'] = fuzz.trimf(servico.universe,  [-0.4, 0, 0.4])
servico['aceitavel'] = fuzz.trimf(servico.universe, [0.1, 0.5, 0.9])
servico['otimo'] = fuzz.trimf(servico.universe,  [0.6, 1, 1.4])

# gorjeta
gorjeta['pequena'] = fuzz.trimf(gorjeta.universe,  [-0.06, 0, 0.06])
gorjeta['media'] = fuzz.trimf(gorjeta.universe,  [0.04, 0.1, 0.16])
gorjeta['alta'] = fuzz.trimf(gorjeta.universe,  [0.14, 0.2, 0.26])

######### REGRAS #########
rule1 = ctrl.Rule(comida['ruim'] & servico['ruim'], gorjeta['pequena'])
rule2 = ctrl.Rule(comida['ruim'] & servico['aceitavel'], gorjeta['pequena'])
rule3 = ctrl.Rule(comida['ruim'] & servico['otimo'], gorjeta['media'])

rule4 = ctrl.Rule(comida['boa'] & servico['ruim'], gorjeta['pequena'])
rule5 = ctrl.Rule(comida['boa'] & servico['aceitavel'], gorjeta['media'])
rule6 = ctrl.Rule(comida['boa'] & servico['otimo'], gorjeta['alta'])

rule7 = ctrl.Rule(comida['saborosa'] & servico['ruim'], gorjeta['pequena'])
rule8 = ctrl.Rule(comida['saborosa'] & servico['aceitavel'], gorjeta['media'])
rule9 = ctrl.Rule(comida['saborosa'] & servico['otimo'], gorjeta['alta'])

gorjeta_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9 ])
gorjeta_simulation = ctrl.ControlSystemSimulation(gorjeta_ctrl)

def gera_inputs(num_inputs):
    comida_input = []
    servico_input = []
    for _ in range(num_inputs):
        comida_input.append(np.random.uniform(0, 1))
        servico_input.append(np.random.uniform(0, 1))
    return comida_input, servico_input

def fuzzy(num_inputs):
    comida_input, servico_input = gera_inputs(num_inputs)
    resultados = []
    for i in range(num_inputs):
        gorjeta_simulation.input['comida'] = comida_input[i]
        gorjeta_simulation.input['servico'] = servico_input[i]
        gorjeta_simulation.compute()
        resultados.append(gorjeta_simulation.output['gorjeta'])
    return resultados

if __name__ == "__main__":
    num_inputs = 100
    resultados = fuzzy(num_inputs)

    print(f"Menor gorjeta: {min(resultados):.2f}")
    print(f"Maior gorjeta: {max(resultados):.2f}")

    # Representando a superfície 3D
    x = np.linspace(0, 1, 30)  # comida
    y = np.linspace(0, 1, 30)  # servico
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            gorjeta_simulation.input['comida'] = X[i, j]
            gorjeta_simulation.input['servico'] = Y[i, j]
            gorjeta_simulation.compute()
            Z[i, j] = gorjeta_simulation.output['gorjeta']

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel('Qualidade da Comida')
    ax.set_ylabel('Qualidade do Serviço')
    ax.set_zlabel('Gorjeta')
    ax.set_title('Superfície Fuzzy para Gorjeta')
    plt.savefig("superficie_gorjeta.png", dpi=300)
    plt.show()
