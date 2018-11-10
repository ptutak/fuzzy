import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Nazwa i zakres wartości funkcji wejściowych i wyjściowych
sq_error = ctrl.Antecedent(np.linspace(0, 20, 201), 'sq_error')
speed = ctrl.Antecedent(np.linspace(5, 75, 141), 'speed')
filter_level = ctrl.Consequent(np.linspace(1, 5, 21), 'filter_level')

# Określenie paramtrów funkcji wyjściowych
sq_error['low'] = fuzz.gaussmf(sq_error.universe, 0, 4)
sq_error['medium'] = fuzz.gaussmf(sq_error.universe, 10, 4)
sq_error['high'] = fuzz.gaussmf(sq_error.universe, 20, 4)

speed['low'] = fuzz.gaussmf(speed.universe, 5, 15)
speed['medium'] = fuzz.gaussmf(speed.universe, 40, 15)
speed['high'] = fuzz.gaussmf(speed.universe, 75, 15)

# Określenie parametrów funkcji wyjściowych
filter_level['low'] = fuzz.trapmf(filter_level.universe, [1, 1, 1.25, 1.75])
filter_level['medium-low'] = fuzz.trapmf(filter_level.universe, [1.25, 1.75, 2.25, 2.75])
filter_level['medium'] = fuzz.trapmf(filter_level.universe, [2.25, 2.75, 3.25, 3.75])
filter_level['medium-high'] = fuzz.trapmf(filter_level.universe, [3.25, 3.75, 4.25, 4.75])
filter_level['high'] = fuzz.trapmf(filter_level.universe, [4.25, 4.75, 5, 5])

# Wyświetlenie funkcji wejściowych i wyjściowych
sq_error.view()
speed.view()
filter_level.view()

# Reguły
rule1 = ctrl.Rule(sq_error['low'] | speed['low'], filter_level['low'])
rule2 = ctrl.Rule(speed['medium'], filter_level['medium'])
rule3 = ctrl.Rule(speed['high'] | sq_error['medium'], filter_level['high'])

rule1.view()

filter_levelping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
filter_levelping = ctrl.ControlSystemSimulation(filter_levelping_ctrl)

# Obliczenie wartości funkcji wyjściowej dla zadanych paramterów wyjściowych
filter_levelping.input['sq_error'] = 6.5
filter_levelping.input['speed'] = 9.8
filter_levelping.compute()

print(filter_levelping.output['filter_level'])
filter_level.view(sim=filter_levelping)

input()
