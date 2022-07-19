_primes = []

# Obtenido de http://www.primos.mat.br/2T_en.html
with open('2T_part1.txt') as f:
    for line in f:
        for prime in line.split():
            _primes.append(int(prime))

primes = _primes