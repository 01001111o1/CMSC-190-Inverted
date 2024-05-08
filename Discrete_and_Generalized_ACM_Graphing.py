import numpy as np
import matplotlib.pyplot as plt
from Generalized_ACM_Period import minimalPeriod, _2DGDCM
from Unrestrained_ACM_Generation import rand_acm_matrix
from sympy import factorint
from numpy.random import randint

########################### DISCRETE CAT MAP (2) ###########################
# dACM = _2DGDCM(1, 1)
# dACM_Period = [None] * 2001
# x = range(2, 2001)

# for N in x:
# 	dACM_Period[N] = minimalPeriod(dACM, N)

# plt.title("Minimal Period for the Discrete Cat Map") 
# plt.xlabel("N")
# plt.ylabel("Minimal Period")
# plt.plot(x, dACM_Period[2:])

# plt.show()
########################### DISCRETE CAT MAP (2) ###########################

########################### GENERALIZED CAT MAP (3) ###########################
#a, b = 7, 11
#a, b = 37, 41
# a, b = 101, 171

# dACM = _2DGDCM(a, b)
# x = range(2, 2001)
# gACM_Period = [minimalPeriod(dACM, N) for N in x]

# plt.title(f'Minimal Period for the Generalized Cat Map with $a = {a}$ and $b = {b}$') 
# plt.xlabel("N")
# plt.ylabel("Minimal Period")
# plt.plot(x, gACM_Period)
# plt.show()
########################### GENERALIZED CAT MAP (3) ###########################


########################### UNRESTRICTED CAT MAP ##############################
# x = range(2, 2001)
# def order(N : int) -> int:

# 	factor_dict : dict[int, int] = factorint(N)
# 	p, k = list(factor_dict.keys()), list(factor_dict.values())
# 	r = len(p)
# 	cardinality = 1 

# 	for i in range(r):
# 		cardinality *= p[i] ** (4 * k[i] - 3) * (p[i] - 1) * (p[i] ** 2 - 1)

# 	return cardinality

# gACM = [n ** 2 for n in x]
# uACM = [order(n) for n in x]

# plt.plot(x, gACM, color = 'blue', label = "Number of Viable Transformation Matrices for the Generalized Cat Map")
# plt.plot(x, uACM, color = 'red', label = r'Cardinality of $GL(2, \mathrm{\mathbb{Z}}_N)$')
# plt.legend()
# plt.show()
########################### UNRESTRICTED CAT MAP ##############################

########################### UNRESTRICTED CAT MAP VS GENERALIZED CAT MAP MINIMAL PERIOD ##############################
# N = 1001
# uACM = []
# gACM = []
# x = range(2, N)

# for n in x:
# 	s = 0
# 	t = 0
# 	for _ in range(15):
# 		a = randint(0, n - 1)
# 		b = randint(0, n - 1)
# 		s += minimalPeriod(_2DGDCM(a, b), n)
# 		_, _, period = rand_acm_matrix(n)
# 		t += period
# 	uACM.append(t / 15)
# 	gACM.append(s / 15)

# plt.plot(x, uACM, color = "red", label = "Unrestricted ACM Average Minimal Period")
# plt.plot(x, gACM, color = "blue", label = "Generalized ACM Average Minimal Period")
# plt.legend()
# plt.show()
########################### UNRESTRICTED CAT MAP VS GENERALIZED CAT MAP MINIMAL PERIOD ##############################

########################### UNRESTRICTED CAT MAP PRIME VS COMPOSITE MINIMAL PERIOD ##############################
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 
		151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 
		317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 
		503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 
		701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 
		911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

composites = [i for i in range(2, 1001) if i not in primes]

# pACM = []
# cACM = []
# x = range(2, 10)

# for n in x:
# 	s = 0
# 	t = 0
# 	for _ in range(15):
# 		_, _, period = rand_acm_matrix(n)
# 		t += period
	
# 	if n in primes:
# 		pACM.append(t / 15)
# 		cACM.append(0)
# 	else: 
# 		cACM.append(t / 15)
# 		pACM.append(0)

# plt.plot(x, pACM, color = "red", label = "Average Minimal Period for Prime Numbers")
# plt.plot(x, cACM, color = "blue", label = "Average Minimal Period for Composite Numbers")
# plt.legend()
# plt.show()
########################### UNRESTRICTED CAT MAP PRIME VS COMPOSITE MINIMAL PERIOD ##############################

########################### UNRESTRICTED CAT MAP PRIME VS COMPOSITE KEY SPACE##############################
# x = range(2, 2001)
# pACM = []
# cACM = []

# def order(N : int) -> int:

# 	factor_dict : dict[int, int] = factorint(N)
# 	p, k = list(factor_dict.keys()), list(factor_dict.values())
# 	r = len(p)
# 	cardinality = 1 

# 	for i in range(r):
# 		cardinality *= p[i] ** (4 * k[i] - 3) * (p[i] - 1) * (p[i] ** 2 - 1)

# 	return cardinality

# for n in x:
# 	k = order(n)

# 	if n in primes:
# 		pACM.append(k)
# 		cACM.append(0)
# 	else:
# 		cACM.append(k)
# 		pACM.append(0)

# plt.plot(x, pACM, color = 'blue', label = "Key Space for Prime Values of N")
# plt.plot(x, cACM, color = 'red', label = "Key Space for Composite Values of N")
# plt.legend()
# plt.show()
########################### UNRESTRICTED CAT MAP PRIME VS COMPOSITE KEY SPACE##############################

