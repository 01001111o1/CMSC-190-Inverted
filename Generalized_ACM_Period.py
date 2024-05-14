import numpy as np

#Minimum Period of a N x N image using a dims Dimensional Generalized Discrete Cat Map
def minimalPeriod(A: list[list[int]], N : int, dims : int = 2) -> int:
    
    Ak = A % N
    k = 1

    while not np.array_equal(Ak, np.identity(dims)):
        k += 1
        Ak = (A @ Ak) % N

    return k

#Returns the 2 dimensionsal generalized discrete cat map with parameters p and q
def _2DGDCM(p : int = 1, q : int = 1) -> list[list[int]]:
    return np.array([[1, p], [q, p * q + 1]])

print(minimalPeriod(_2DGDCM(2, 3), 10))