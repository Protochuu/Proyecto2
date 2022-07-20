from dataclasses import dataclass, field
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
    KEY_VALUE_PAIR_COUNT: int = 2 ** 16
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
        logger.info(key)
        try:
            map.erase(key)
        except KeyError:
            logger.error('Clave no encontrada.')


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

    n_elements = [2 ** i for i in range(0, 16)]

    results = Results(class_name=map_cls.__name__)

    for n in n_elements:
        logger.info(f'Eliminando {n} elementos para {map_cls.__name__}')

        map = map_cls()

        for key, value in zip(strings, integers):
            map.insert(key, value)

        logger.info('here1')

        random_keys = []

        for _ in range(n):
            random_keys.append(choice(strings))

        logger.info('here2')

        random_keys = tuple(random_keys)

        time = timeit.timeit(lambda: profile_erase(map, random_keys),
                             number=constants.REPS)

        results.erase_time_v_n.append(time / constants.REPS)

    for n in n_elements:
        logger.info(f'Obteniendo {n} elementos para {map_cls.__name__}')

        map = map_cls()

        for key, value in zip(strings, integers):
            map.insert(key, value)

        random_keys = []

        for _ in range(n):
            random_keys.append(choice())

        random_keys = tuple(random_keys)

        time = timeit.timeit(lambda: profile_at(map, random_keys),
                      number=constants.REPS)

        results.erase_time_v_n.append(time / constants.REPS)

    return results


def plot_results(results: List[Results]):
    map_hash = results[0]
    map_sv = results[1]
    map_avl = results[2]

    n_elements = [2 ** i for i in range(0, 16)]

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

    exps = [i for i in range(0, 16)]

    method = 'insert'

    text = ''

    for i, map_hash_data, map_sv_data, map_avl_data in zip(exps,
                                                           map_hash.insert_time_v_n,
                                                           map_sv.insert_time_v_n,
                                                           map_avl.insert_time_v_n):

        text += f'2^{i} \\, Elementos&{map_hash_data} \, \\text{{s}}&{map_sv_data} \, \\text{{s}}&{map_avl_data} \, \\text{{s}}\\\\'

    with open(f'{method}.txt', 'w') as f:
        f.write(text)

    method = 'at'

    text = ''

    for i, map_hash_data, map_sv_data, map_avl_data in zip(exps,
                                                           map_hash.at_time_v_n,
                                                           map_sv.at_time_v_n,
                                                           map_avl.at_time_v_n):

        text += f'2^{i} \\, Elementos&{map_hash_data} \, \\text{{s}}&{map_sv_data} \, \\text{{s}}&{map_avl_data} \, \\text{{s}}\\\\'

    with open(f'{method}.txt', 'w') as f:
        f.write(text)

    method = 'erase'

    text = ''

    for i, map_hash_data, map_sv_data, map_avl_data in zip(exps,
                                                           map_hash.erase_time_v_n,
                                                           map_sv.erase_time_v_n,
                                                           map_avl.erase_time_v_n):

        text += f'2^{i} \\, Elementos&{map_hash_data} \, \\text{{s}}&{map_sv_data} \, \\text{{s}}&{map_avl_data} \, \\text{{s}}\\\\'

    with open(f'{method}.txt', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    results: List[Results] = []

    for map_cls in (MapHash, MapSV, MapAVL):
        results.append(profile(map_cls))

    plot_results(results)
    results_to_latex(results)
