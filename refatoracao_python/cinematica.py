# -*- coding: utf-8 -*-
from math import cos, sin, atan2, degrees, radians, pow, acos
from decimal import *
# import numpy
# from . import util



# Para converter numeros em graus
# cos_90_degrees = math.cos(math.radians(90))
# print(cos_90_degrees)



class Cinematica():

	def dir_transform(t1, t2, l1, l2, precisao):
		"""
		Transformação Direta - Passagem do espaço de juntas para espaço cartesiano

		Parâmetros:
			t1, t2 = Ângulo das juntas em graus
			l1, l2 = Comprimentos dos elos  em metros
			precisao = Precisão decimal para cálculos

		Retorno:
			x, y = Posições cartesianas
		"""

		# Vetores individuais para Elo 1
		r1 = (l1 * cos(radians(t1)), l1 * sin(radians(t1)))

		# Vetores individuais para Elo 2
		r2 = (l2 * cos(radians(t1 + t2)), l2 * sin(radians(t1 + t2)))

		# Realiza soma vetorial para posição final
		r3 = (r1[0] + r2[0], r1[1] + r2[1])

		# Arredonda valor para precisão decimal de três casas
		x = round(r3[0], precisao)
		y = round(r3[1], precisao)

		return x, y


	def inv_transform(x, y, l1, l2, precisao):
		"""
		Transformação Inversa - Passagem do espaço cartesiano para espaço das juntas

		Parâmetros:
			x, y = Posição cartesiana
			l1, l2 = Comprimentos dos elos  em metros
			precisao = Precisão decimal para cálculos

		Retorno:
			(t1, t2), (t1, t2) = Conjunto de ângulos possíveis para os elos (em graus)
		"""

		res_a = (0, 0)
		res_b = (0, 0)

		# Primeira possibilidade: t2 positivo

		try:
			t2 = acos((pow(x, 2) + pow(y, 2) - pow(l1, 2) - pow(l2, 2)) / (2*l1*l2))
		except:
			t2 = 0

		num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2)
		den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2)

		t1 = atan2(num, den)

		res_a = (round(degrees(t1), precisao), round(degrees(t2), precisao))

	# Segunda possibilidade: t2 negativo

		try:
			t2 = -acos((pow(x, 2)+pow(y, 2)-pow(l1, 2)-pow(l2, 2))/(2*l1*l2))
		except:
			t2 = 0

		num = y * (l1 + l2 * cos(t2)) - x * l2 * sin(t2)
		den = x * (l1 + l2 * cos(t2)) + y * l2 * sin(t2)
		t1 = atan2(num, den)

		res_b = (round(degrees(t1), precisao), round(degrees(t2), precisao))

		return res_a, res_b
	

	x, y = dir_transform(t1=45, t2=45, l1=0.4, l2=0.4, precisao=2)
	print(x, y)

	cj1, cj2 = inv_transform(x=x, y=y, l1=0.4, l2=0.4, precisao=2)
	print(cj1, cj2)