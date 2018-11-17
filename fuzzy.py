import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from mayavi import mlab

sq_error_space = np.linspace(0, 20, 201)
speed_space = np.linspace(5, 75, 141)
filter_level_space = np.linspace(0.25, 5.75, 201)

# Nazwa i zakres wartości funkcji wejściowych i wyjściowych
sq_error = ctrl.Antecedent(sq_error_space, 'sq_error')
speed = ctrl.Antecedent(speed_space, 'speed')
filter_level = ctrl.Consequent(filter_level_space, 'filter_level', defuzzify_method='mom')

# Określenie paramtrów funkcji wyjściowych
sq_error['low_err'] = fuzz.gaussmf(sq_error.universe, 0, 4)
sq_error['medium_err'] = fuzz.gaussmf(sq_error.universe, 10, 4)
sq_error['high_err'] = fuzz.gaussmf(sq_error.universe, 20, 4)

speed['low_sp'] = fuzz.gaussmf(speed.universe, 5, 15)
speed['medium_sp'] = fuzz.gaussmf(speed.universe, 40, 15)
speed['high_sp'] = fuzz.gaussmf(speed.universe, 75, 15)

# Określenie parametrów funkcji wyjściowych
filter_level['low'] = fuzz.trapmf(filter_level.universe, [0.25, 0.75, 1.25, 1.75])
filter_level['medium-low'] = fuzz.trapmf(filter_level.universe, [1.25, 1.75, 2.25, 2.75])
filter_level['medium'] = fuzz.trapmf(filter_level.universe, [2.25, 2.75, 3.25, 3.75])
filter_level['medium-high'] = fuzz.trapmf(filter_level.universe, [3.25, 3.75, 4.25, 4.75])
filter_level['high'] = fuzz.trapmf(filter_level.universe, [4.25, 4.75, 5.25, 5.75])


# Wyświetlenie funkcji wejściowych i wyjściowych
sq_error.view()
speed.view()
filter_level.view()

# Reguły
rule1 = ctrl.Rule(sq_error['low_err'], filter_level['low'])
rule2 = ctrl.Rule(sq_error['medium_err'] & speed['low_sp'], filter_level['medium-high'])
rule3 = ctrl.Rule(sq_error['high_err'] & speed['low_sp'], filter_level['high'])
rule4 = ctrl.Rule(sq_error['medium_err'] & speed['medium_sp'], filter_level['medium'])
rule5 = ctrl.Rule(sq_error['high_err'] & speed['medium_sp'], filter_level['medium-high'])
rule6 = ctrl.Rule(sq_error['medium_err'] & speed['high_sp'], filter_level['medium-low'])
rule7 = ctrl.Rule(sq_error['high_err'] & speed['high_sp'], filter_level['medium'])

# Stworzenie systemu rozmytego przetwarzającego reguły
filter_leveling_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
filter_leveling = ctrl.ControlSystemSimulation(filter_leveling_ctrl)

# Obliczenie wartości funkcji wyjściowej dla przykładowych parametrów sq_error = 6.5, speed = 10
filter_leveling.input['sq_error'] = 1
filter_leveling.input['speed'] = 10
filter_leveling.compute()
filter_level.view(sim=filter_leveling)

filter_leveling.input['sq_error'] = 6.5
filter_leveling.input['speed'] = 10
filter_leveling.compute()
filter_level.view(sim=filter_leveling)

filter_leveling.input['sq_error'] = 16
filter_leveling.input['speed'] = 5
filter_leveling.compute()
filter_level.view(sim=filter_leveling)

filter_leveling.input['sq_error'] = 20
filter_leveling.input['speed'] = 35
filter_leveling.compute()
filter_level.view(sim=filter_leveling)

# Wypisanie wyników
print(filter_leveling.output['filter_level'])

# Wyrysowanie symulacji obliczonego wyniku
filter_level.view(sim=filter_leveling)

# Stworzenie punktów kontrolnych dla wyliczanej powierzchni
x, y = np.meshgrid(sq_error_space, speed_space)
z = np.zeros_like(x)

# Wyliczenie wartości dla wszystkich punktów
sim = ctrl.ControlSystemSimulation(filter_leveling_ctrl, flush_after_run=len(sq_error_space)*len(speed_space)+1)

for i in range(len(speed_space)):
    for j in range(len(sq_error_space)):
        sim.input['sq_error'] = x[i, j]
        sim.input['speed'] = y[i, j]
        sim.compute()
        z[i, j] = round(sim.output['filter_level'])

# Wykreślenie wykresu 3d dla wszystkich punktów
s = mlab.mesh(x, y, z, opacity=0.5)
ax = mlab.axes(xlabel='sq_error', ylabel='speed', zlabel='filter_level', line_width=1.0)
ax.axes.font_factor = 0.5
mlab.show()
