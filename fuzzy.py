import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Nazwa i zakres wartości funkcji wejściowych i wyjściowych
sq_error = ctrl.Antecedent(np.linspace(0, 20, 201), 'sq_error')
speed = ctrl.Antecedent(np.linspace(5, 75, 141), 'speed')
filter_level = ctrl.Consequent(np.linspace(1, 5, 21), 'filter_level', defuzzify_method='bisector')

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
rule1 = ctrl.Rule(sq_error['low'], filter_level['low'])
rule2 = ctrl.Rule(sq_error['medium'] & speed['low'], filter_level['medium-high'])
rule3 = ctrl.Rule(sq_error['high'] & speed['low'], filter_level['high'])
rule4 = ctrl.Rule(sq_error['medium'] & speed['medium'], filter_level['medium'])
rule5 = ctrl.Rule(sq_error['high'] & speed['medium'], filter_level['medium-high'])
rule6 = ctrl.Rule(sq_error['medium'] & speed['high'], filter_level['medium-low'])
rule7 = ctrl.Rule(sq_error['high'] & speed['high'], filter_level['medium'])

filter_leveling_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
filter_leveling = ctrl.ControlSystemSimulation(filter_leveling_ctrl)

# Obliczenie wartości funkcji wyjściowej dla zadanych paramterów wyjściowych
filter_leveling.input['sq_error'] = 6.5
filter_leveling.input['speed'] = 10
filter_leveling.compute()

print(filter_leveling.output['filter_level'])
filter_level.view(sim=filter_leveling)

input()
