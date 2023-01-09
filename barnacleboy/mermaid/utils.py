import itertools
import math
from string import ascii_uppercase
from typing import Generator, Union


def next_power(target: Union[int, float], base: Union[int, float] = 2) -> int:
    """Return the next power of base that is greater than or equal to target.

    Args:
        target: The target number.
        base: The base of the power.

    Returns:
        The next power of base that is greater than or equal to target.

    Examples:
        >>> next_power(10)
        4
        >>> next_power(10, 3)
        3

    """
    return int(math.ceil(math.log(target, base)))


def generate_internal_ids(n_nodes: int) -> Generator[str, None, None]:
    """Generate a list of node ids using the alphabet.

    Args:
        n_nodes: The number of entities to generate ids for.

    Returns:
        A generator of node ids.

    Examples:
        >>> list(generate_internal_ids(5))
        ['A', 'B', 'C', 'D', 'E']
        >>> list(generate_internal_ids(27))
        ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR',
        'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA']

    """
    n_characters = max(next_power(n_nodes, len(ascii_uppercase)), 1)
    character_sets = itertools.product(ascii_uppercase, repeat=n_characters)
    for idx, characters in enumerate(character_sets):
        if idx >= n_nodes:
            break
        yield "".join(characters)


def init_string(base_config: dict, object_config: dict) -> str:
    """Generate the mermaid init.

    Args:
        base_config: The configuration of MermaidBase.
        object_config: The configuration for the object.

    Returns:
        A string representation of the object.

    """
    config = base_config.copy()
    config.update(object_config)
    config_string = f"%%{str(config)}%%\n"
    return config_string.replace("'init'", "init")
