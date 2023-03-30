# -*- coding: utf-8 -*-
from math import cos, sin, atan2, degrees, radians, pow, acos
from decimal import *
import struct


from refatoracao_python.functions import start, stop, get_sensors, sim, axis_A, axis_B, tool, abs_dif, client, tamanho_elo_1, tamanho_elo_2



class Move():

	def moveJ(t1, t2, interpolation=True):
		"""
		Movimenta para uma posição no espaço das juntas

		Parâmetros:
		t1, t2 = Ângulo das juntas (em graus)
		interoplation = Deve ser realizada a interpolação de tempo ou não (True | False), padrão True
		"""

		# Configurações
		threshold = 0.01

		# Interpolation
		vel_max = 2
		vel_max_a = vel_max
		vel_max_b = vel_max

		if interpolation:
			s1, s2 = get_sensors()

			dif_elo_a = abs_dif(s1, t1)
			dif_elo_b = abs_dif(s2, t2)

			if dif_elo_a < dif_elo_b and dif_elo_a >= threshold:
				delta_t_a = dif_elo_a / vel_max_a
				vel_max_b = dif_elo_b / delta_t_a
			if dif_elo_b > dif_elo_a and dif_elo_b >= threshold:
				delta_t_b = dif_elo_b / vel_max_b
				vel_max_a = dif_elo_a / delta_t_b

		sim.setJointTargetVelocity(axis_A, 0, [vel_max_a, vel_max_a])
		sim.setJointTargetVelocity(axis_B, 0, [vel_max_b, vel_max_b])

		# End Interpolation

		sim.setJointTargetPosition(axis_A, radians(t1))
		sim.setJointTargetPosition(axis_B, radians(t2))

		while True:
			s1, s2 = get_sensors()

			moved_a = True if abs(s1 - t1) <= threshold else False
			moved_b = True if abs(s2 - t2) <= threshold else False

			if moved_a and moved_b:
				break

			client.step()