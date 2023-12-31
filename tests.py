import csv
import time
import random
from bloomfilter import BloomFilter

baby_csv = open('Popular-Baby-Names-Final.csv', "r", encoding='utf-8')
baby_len = 93890 # numero de elementos en la db
film_csv = open('Film-Names.csv', "r", encoding='utf-8')
film_len = 3809

TP = 1500 # true positives
TN = 500 # true negatives

# Primero generamos la secuencia de busqueda
search_sequence = []

baby_names = csv.reader(baby_csv, delimiter=",")
indexes = random.sample(range(baby_len), TP) # seleccionamos una muestra aleatoria de TP nombres de bebe
for index, row in enumerate(baby_names):
    if index in indexes:
        name = row[0]
        search_sequence.append((name, True)) # True para indicar de que este nombre si esta en la db

print(len(search_sequence))

film_names = csv.reader(film_csv, delimiter=",")
indexes = random.sample(range(film_len), TN) # seleccionamos una muestra aleatoria de TN nombres de peliculas
for index, row in enumerate(film_names):
    if index in indexes:
        name = row[0]
        search_sequence.append((name, False)) # False para indicar que este nombre no esta en la db

random.shuffle(search_sequence) # hacemos shuffle para desordenar la secuencia de busqueda
N = len(search_sequence) # numero de elementos a buscar
print(N)

print("Begin Tests")
for i in range(1,11):
    start = time.time()
    count = 0
    for name, status in search_sequence:
        baby_csv.seek(0)
        for row in baby_names:
            if name == row[0]:
                count += 1
    end = time.time()
    print(f"Test no filter: Time taken = {end-start} sec")

TOLERANCE = 0.01 # tolerancia de error
n = baby_len # numero de elementos en la db

for m in range(n, 10*n+1, n):
    print(f"============ m = {m} ============")
    for k in range(1, 10+1):
        bloom_filter = BloomFilter(m, k)

        baby_csv.seek(0)

        # Aplicamos el filtro a los nombres de bebe
        for row in baby_names:
            name = row[0]
            bloom_filter.add(name)
        
        # Busqueda
        FP = 0 # falsos positivos

        start = time.time()
        for name, status in search_sequence:
            if name in bloom_filter: # si el filtro dice que esta, lo buscamos en el archivo
                found = False
                baby_csv.seek(0)
                for row in baby_names:
                    if name == row[0]:
                        found = True
                if not found: # si no lo encontramos despues de recorrer la db, es un falso positivo
                    FP += 1
            
            else: # si el filtro dice que no esta, verificamos el one-side error
                assert status == False
        end = time.time()
        error = FP/TN
        print(f"Test filter k = {k}: Time taken = {end-start}, error = {error}")
