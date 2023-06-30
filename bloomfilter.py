import random
from bitarray import bitarray
from utils import str_to_int

class BloomFilter:
    """
    Esta clase representa un filtro de Bloom
    Attributes:
        m: int
            largo del arreglo de bits
        k: int
            numero de funciones de hash
        M: bitarray
            el arreglo de bits
    """
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.M = bitarray(m)
        self.M.setall(0)
        self.p = 200003 # primo mayor que el tamaño del universo
        self.a = random.randint(1, self.p)
    
    def add(self, x):
        x = str_to_int(x)
        for b in range(self.k):
            j = ((self.a * x + b) % self.p) % self.m # usamos distintos hashes de la familia universal
            self.M[j] = 1
    
    def __contains__(self, y):
        y = str_to_int(y)
        for b in range(self.k):
            j = ((self.a * y + b) % self.p) % self.m
            if self.M[j] == 0:
                return False
        return True
