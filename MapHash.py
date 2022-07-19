from dataclasses import dataclass, field

from enum import Enum, auto
from typing import List

from Map import Map
from primes import primes

from loguru import logger

@dataclass(frozen=True)
class constants:
    ALPHA_TOL: float = 0.5
    PRIMARY_HASH_Z: int = 33


@dataclass
class Bucket:
    key: str = field(default='')
    value: int = field(default=0)

    _available: bool= field(default=True)
    _empty: bool = field(default=True)

    def set_key_value(self, key: str, value: int):
        self.key = key
        self.value = value

        self._empty = False
        self._available = True

    def remove(self):
        self.key = ''
        self.value = 0
        self._available = True

    def is_empty(self) -> bool:
        return self._empty

    def is_available(self) -> bool:
        return self._available


class MapHash(Map):
    def __init__(self):
        logger.debug('Se llamó al constructor de MapHash')

        self.prime_index: int = 1

        self.array_size: int = primes[self.prime_index]
        self.array: List[Bucket] = [Bucket() for _ in range(self.array_size)]

        self.buckets_no: int = 0

    def _should_rehash(self, bucket: Bucket):
        return not self._can_insert(bucket)

    @staticmethod
    def _can_insert(bucket: Bucket):
        return bucket.is_empty() or bucket.is_available()

    def _reallocate(self):
        to_rehash: List[Bucket] = [bucket for bucket in self.array if self._should_rehash(bucket)]

        self.prime_index += 1
        self.array_size = primes[self.prime_index]
        self.array = [Bucket() for _ in range(self.array_size)]

        for bucket in to_rehash:
            for j, _ in enumerate(self.array):
                hashed_key = self._hash(bucket.key, j)
                bucket = self.array[hashed_key]

                if self._can_insert(bucket):
                    self.array_size[hashed_key] = bucket
                    break

    def insert(self, key: str, value: int):
        if self.alpha > constants.ALPHA_TOL:
            self._reallocate()

        for j, _ in enumerate(self.array):
            bucket = self.array[self._hash(key, j)]

            if ( not bucket.is_empty() ) and (bucket.key == key):
                raise KeyError("Llave ya insertada.")

            if self._can_insert(bucket):
                bucket.set_key_value(key, value)
                self.buckets_no += 1

                break

    def _hash(self, key: str, j: int) -> int:
        return self._primary_hash(key) + (j * self._secondary_hash(key) % self.array_size)

    def _primary_hash(self, key: str) -> int:
        p = 0
        exp = 0

        for character in key:
            p += ord(character) * (constants.PRIMARY_HASH_Z ** exp)
            exp += 1

        return p % self.array_size

    def _secondary_hash(self, key: str) -> int:
        sum = 0

        for character in key:
            sum += ord(character)

        q = primes[self.prime_index - 1]

        return q - (sum % q)

    @property
    def alpha(self):
        return self.buckets_no / self.array_size

    def erase(self, key: str):
        for j, _ in enumerate(self.array):
            bucket = self.array[self._hash(key, j)]

            if bucket.key == key:
                bucket.remove()
                self.buckets_no -= 1

                break
            elif self._can_insert(bucket):
                raise KeyError("Llave no encontrada")

    def at(self, key: str) -> int:
        for j, _ in enumerate(self.array):
            bucket = self.array[self._hash(key, j)]

            if bucket.key == key:
                return bucket.value

        raise KeyError("Llave no encontrada.")

    def empty(self) -> bool:
        return self.buckets_no == 0

    def size(self) -> int:
        return self.buckets_no
