#-*-coding:utf-8-*-
import numpy as np

#Recibe un modelo de markov (matrix A, B y Pi) y un conjunto de observaciones, y devuelve el estado más probable dada la secuencia
def run(model, observations):
	factors, alphas = get_alhpas(model, observations, len(observations)-1, np.empty((0,)))

	de_factor = np.prod(factors)
	
	return alphas/de_factor

def get_alhpas(model, observations, t, factors):
	states = model.get_pi_matrix().shape
	alphas = np.zeros(states)
	if t == 0:
		for row in range(states[0]):
			for column in range(states[1]):
				alphas[row, column] = model.get_b_matrix()[row, column, observations[0]]
	else:
		factors, prev_alphas = get_alhpas(model, observations, t-1, factors)
		for row in range(states[0]):
			for column in range(states[1]):
				values = []

				for row_2 in range(states[0]):
					for column_2 in range(states[1]):
						if is_reachable((row_2, column_2), (row, column)):
							direction = get_direction((row_2, column_2), (row, column))
							if direction == -1:
								raise ValueError("Direccion = -1, salida {0}, llegada {1}".format((row_2, column_2), (row, column)))

							values.append(model.get_a_matrix()[row_2, column_2, direction]*alphas[row_2, column_2])
						else:
							values.append(0.0)

				values = sum(values)
				alphas[row, column] = model.get_b_matrix()[row, column, observations[t]]

	factor = 1 / alphas.sum()
	factors = np.append(factors, factor)
	return factors, alphas*factor



def is_reachable(departure, arrival):
	res = False
	
	if not departure == arrival:
		if departure[0] == arrival[0] and abs(departure[1] - arrival[1]) == 1:
			res = True
		if departure[1] == arrival[1] and abs(departure[0] - arrival[0]) == 1:
			res = True

	return res

def get_direction(departure, arrival):
	direction = -1

	if departure[0] == arrival[0] and departure[1] - arrival[1] == 1:
		direction = 0 #N
	elif departure[1] == arrival[1] and departure[0] - arrival[0] == -1:
		direction = 1 #E
	elif departure[0] == arrival[0] and departure[1] - arrival[1] == -1:
		direction = 2 #S
	elif departure[1] == arrival[1] and departure[0] - arrival[0] == 1:
		direction = 3 #O

	return direction