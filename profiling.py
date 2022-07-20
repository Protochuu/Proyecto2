from dataclasses import dataclass, field
from itertools import islice
from typing import Tuple, List, Iterator, Optional

import matplotlib.pyplot as plt

from random import randrange, randint, choice

from Map import Map
from MapHash import MapHash
from MapSV import MapSV
from MapAVL import MapAVL

import timeit

from loguru import logger


@dataclass(frozen=True)
class constants:
    CHAR_RANGE: Tuple[int, int]= (32, 125)
    STRING_LENGTH: int = 10
    KEY_VALUE_PAIR_COUNT: int = 2 ** 12
    KEY_MAX_INT: int = 1024
    REPS: int = 100


def get_random_char() -> str:
    return chr(randrange(*constants.CHAR_RANGE))


def generate_random_keys() -> Tuple[str]:
    logger.info('Generando llaves...')

    strings: List[str] = []

    for _ in range(constants.KEY_VALUE_PAIR_COUNT):
        new_string = ''.join((get_random_char() for _ in range(constants.STRING_LENGTH)))
        strings.append(new_string)

    return tuple(strings)


def generate_random_values() -> Tuple[int]:
    logger.info('Generando valores...')

    integers: List[int] = []

    for _ in range(constants.KEY_VALUE_PAIR_COUNT):
        integers.append(randint(0, constants.KEY_MAX_INT))

    return tuple(integers)


def profile_insert(map: Map, pairs: Iterator[Tuple[str, int]]):
    for key, value in pairs:
        map.insert(key, value)


def profile_erase(map: Map, keys: Iterator[str]):
    for key in keys:
        try:
            map.erase(key)
        except KeyError:
            pass


def profile_at(map: Map, keys: Iterator[str]):
    for key in keys:
        map.at(key)


@dataclass
class Results:
    class_name: str = None

    insert_time_v_n: List[Tuple[int, float]] = field(default_factory=list)
    erase_time_v_n: List[Tuple[int, float]] = field(default_factory=list)
    at_time_v_n: List[Tuple[int, float]] = field(default_factory=list)


def profile(map_cls: type = None) -> Results:
    strings = generate_random_keys()
    integers = generate_random_values()

    n_elements = [2 ** i for i in range(0, 12)]

    results = Results(class_name=map_cls.__name__)

    for n in n_elements:
        logger.info(f'Eliminando {n} elementos para {map_cls.__name__}')

        timeit_globals = {
            'map_cls': map_cls,
            'profile_erase': profile_erase,
            'strings': strings,
            'integers': integers,
            'n': n,
        }

        setup = """
from itertools import islice
from random import choice

map = map_cls()

for key, value in islice(zip(strings, integers), n + 1):
    map.insert(key, value)
    
slice = list(islice(strings, n))

random_keys = []

for _ in range(n):
    random_keys.append(choice(slice))
"""

        time = timeit.timeit('profile_erase(map, random_keys)',
                             setup=setup,
                             globals=timeit_globals,
                             number=constants.REPS)

        results.erase_time_v_n.append(time / constants.REPS)

    for n in n_elements:
        logger.info(f'Insertando {n} elementos para {map_cls.__name__}')

        timeit_globals = {
            'map_cls': map_cls,
            'profile_insert': profile_insert,
            'strings': strings,
            'integers': integers,
            'n': n,
        }

        setup = """
from itertools import islice
map = map_cls()
pairs = islice(zip(strings, integers), n)
"""

        time = timeit.timeit('profile_insert(map, pairs)',
                      setup=setup,
                      globals=timeit_globals,
                      number=constants.REPS)

        results.insert_time_v_n.append(time / constants.REPS)

    for n in n_elements:
        logger.info(f'Obteniendo {n} elementos para {map_cls.__name__}')

        timeit_globals = {
            'map_cls': map_cls,
            'profile_at': profile_at,
            'strings': strings,
            'integers': integers,
            'n': n,
        }

        setup = """
from itertools import islice
from random import choice

map = map_cls()

for key, value in islice(zip(strings, integers), n):
    map.insert(key, value)

slice = list(islice(strings, n))

random_keys = []

for _ in range(n):
    random_keys.append(choice(slice))
"""

        time = timeit.timeit('profile_at(map, random_keys)',
                             setup=setup,
                             globals=timeit_globals,
                             number=constants.REPS)

        results.at_time_v_n.append(time / constants.REPS)

    return results


def plot_results(results: List[Results]):
    map_hash = results[0]
    map_sv = results[1]
    map_avl = results[2]

    n_elements = [2 ** i for i in range(0, 12)]

    method = 'insert'

    plt.loglog(n_elements, map_hash.insert_time_v_n, label=f'MapHash {method}()')
    plt.loglog(n_elements, map_sv.insert_time_v_n, label=f'MapSV {method}()')
    plt.loglog(n_elements, map_avl.insert_time_v_n, label=f'MapAVL {method}()')

    plt.xscale('log', base=2)

    plt.xlabel('Número de elementos (N)')
    plt.ylabel('Tiempo (s)')
    plt.title(f'Comparación entre implementaciones, método {method}()')

    plt.legend()
    plt.savefig(f'{method}.png')
    plt.close()

    method = 'at'

    plt.loglog(n_elements, map_hash.at_time_v_n, label=f'MapHash {method}()')
    plt.loglog(n_elements, map_sv.at_time_v_n, label=f'MapSV {method}()')
    plt.loglog(n_elements, map_avl.at_time_v_n, label=f'MapAVL {method}()')

    plt.xscale('log', base=2)

    plt.xlabel('Número de elementos (N)')
    plt.ylabel('Tiempo (s)')
    plt.title(f'Comparación entre implementaciones, método {method}()')

    plt.legend()
    plt.savefig(f'{method}.png')
    plt.close()

    method = 'erase'

    plt.loglog(n_elements, map_hash.erase_time_v_n, label=f'MapHash {method}()')
    plt.loglog(n_elements, map_sv.erase_time_v_n, label=f'MapSV {method}()')
    plt.loglog(n_elements, map_avl.erase_time_v_n, label=f'MapAVL {method}()')

    plt.xscale('log', base=2)

    plt.xlabel('Número de elementos (N)')
    plt.ylabel('Tiempo (s)')
    plt.title(f'Comparación entre implementaciones, método {method}()')

    plt.legend()
    plt.savefig(f'{method}.png')
    plt.close()


def results_to_latex(results: List[Results]):
    map_hash = results[0]
    map_sv = results[1]
    map_avl = results[2]

    exps = [i for i in range(0, 12)]

    method = 'insert'

    text = ''

    for i, map_hash_data, map_sv_data, map_avl_data in zip(exps,
                                                           map_hash.insert_time_v_n,
                                                           map_sv.insert_time_v_n,
                                                           map_avl.insert_time_v_n):

        text += f'2^{{{i}}} \\, Elementos&{map_hash_data:.2E} \\, \\text{{s}}&{map_sv_data:.2E} \\, \\text{{s}}&{map_avl_data:.2E} \\, \\text{{s}}\\\\ \n'

    with open(f'{method}.txt', 'wb') as f:
        f.write(bytearray(text, 'ascii'))

    method = 'at'

    text = ''

    for i, map_hash_data, map_sv_data, map_avl_data in zip(exps,
                                                           map_hash.at_time_v_n,
                                                           map_sv.at_time_v_n,
                                                           map_avl.at_time_v_n):

        text += f'2^{{{i}}} \\, Elementos&{map_hash_data:.2E} \\, \\text{{s}}&{map_sv_data:.2E} \\, \\text{{s}}&{map_avl_data:.2E} \\, \\text{{s}}\\\\ \n'

    with open(f'{method}.txt', 'wb') as f:
        f.write(bytearray(text, 'ascii'))

    method = 'erase'

    text = ''

    for i, map_hash_data, map_sv_data, map_avl_data in zip(exps,
                                                           map_hash.erase_time_v_n,
                                                           map_sv.erase_time_v_n,
                                                           map_avl.erase_time_v_n):

        text += f'2^{{{i}}} \\, Elementos&{map_hash_data:.2E} \\, \\text{{s}}&{map_sv_data:.2E} \\, \\text{{s}}&{map_avl_data:.2E} \\, \\text{{s}}\\\\ \n'

    with open(f'{method}.txt', 'wb') as f:
        f.write(bytearray(text, 'ascii'))


if __name__ == '__main__':
    results: List[Results] = []

    for map_cls in (MapHash, MapSV, MapAVL):
        results.append(profile(map_cls))

    plot_results(results)
    results_to_latex(results)
