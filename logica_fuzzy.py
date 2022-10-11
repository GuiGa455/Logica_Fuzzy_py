import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def main():
    #Variaveis de Entrada (Antecedent)
    atividade_fisica = ctrl.Antecedent(np.arange(0, 8, 1), 'atividade fisica')
    alimentacao = ctrl.Antecedent(np.arange(0, 11, 1), 'alimentação')

    #Variaveis de saída (Consequent)
    peso = ctrl.Consequent(np.arange(30, 200, 60), 'peso')

    # automf -> Atribuição de categorias automaticamente
    atividade_fisica['otima'] = fuzz.trapmf(atividade_fisica.universe, [0,1,2,4])
    atividade_fisica['ok'] = fuzz.trapmf(atividade_fisica.universe, [2,5,5,6])
    atividade_fisica['ruim'] = fuzz.trapmf(atividade_fisica.universe, [4,8,8,10])
    

    alimentacao['otima'] = fuzz.trimf(alimentacao.universe, [0,1,2,])
    alimentacao['ok'] = fuzz.trimf(alimentacao.universe, [1,5,6,])
    alimentacao['ruim'] = fuzz.trimf(alimentacao.universe, [5,8,10])
    

    # atribuicao sem o automf
    peso['baixo-peso'] = fuzz.gaussmf(peso.universe,40,25)
    peso['peso-normal'] = fuzz.gaussmf(peso.universe, 70, 25)
    peso['sobrepeso'] = fuzz.gaussmf(peso.universe, 120,25)
    peso['obeso'] = fuzz.gaussmf(peso.universe, 150,25)
    



    #Criando as regras
    regra_1 = ctrl.Rule(atividade_fisica['otima'] & alimentacao['otima'], peso['baixo-peso'])
    regra_2 = ctrl.Rule(atividade_fisica['ok'] | alimentacao['ok'], peso['peso-normal'])
    regra_3 = ctrl.Rule(atividade_fisica['ruim'] | alimentacao['ok'], peso['sobrepeso'])
    regra_4 = ctrl.Rule(alimentacao['ruim'] & atividade_fisica['ruim'], peso['obeso'])

    controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3,regra_4])


    #Simulando
    Calculopeso = ctrl.ControlSystemSimulation(controlador)

    notaAtividade = int(input('Atividade fisica (Quantos dias na semana?): '))

    notaServico = int(input('Alimentação: '))
    Calculopeso.input['atividade fisica'] = notaAtividade
    Calculopeso.input['alimentação'] = notaServico
    Calculopeso.compute()

    valorpeso = Calculopeso.output['peso']

    print("\atividade fisica %d \nalimentacao %d \npeso de %5.2f" %(
            notaAtividade,
            notaServico,
            valorpeso))


    atividade_fisica.view(sim=Calculopeso)
    alimentacao.view(sim=Calculopeso)
    peso.view(sim=Calculopeso)

    plt.show()
main()    