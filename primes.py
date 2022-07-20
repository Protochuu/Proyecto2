_primes = []

# Obtenido de http://www.primos.mat.br/2T_en.html
with open('2T_part1.txt') as f:
    count = 0
    for line in f:
        if count == 100000:
            break

        for prime in line.split():
            _primes.append(int(prime))

        count += 1


primes = _primes