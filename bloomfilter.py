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
        p: int
            primo mayor que el tamaño del universo
    """
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.M = bitarray(m)
        self.M.setall(0)
        self.p = 100000007
    
    def add(self, x):
        x = str_to_int(x)
        for i in range(self.k):
            random.seed(i)
            a = random.randint(1, self.p-1)
            b = random.randint(0, self.p-1)
            j = ((a * x + b) % self.p) % self.m # usamos distintos hashes de la familia universal
            self.M[j] = 1
    
    def __contains__(self, y):
        y = str_to_int(y)
        for i in range(self.k):
            random.seed(i)
            a = random.randint(1, self.p-1)
            b = random.randint(0, self.p-1)
            j = ((a * y + b) % self.p) % self.m
            if self.M[j] == 0:
                return False
        return True
