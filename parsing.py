#!/usr/bin/env python3

from random import randint
from typing import Any


def check_value(key: str, value: str) -> int:
    """Validate the format of a single config key-value pair.

    Args:
        key: The config key in lowercase (e.g. 'width', 'entry').
        value: The raw string value from the config file.

    Returns:
        0 if valid, 1 if invalid (prints an error message).
    """
    try:
        if key == 'width' or key == 'height':
            int(value)
    except Exception:
        print('error: width or height key must only have one int paramater')
        return 1

    try:
        if key == 'entry' or key == 'exit':
            i = value.find(',')
            int(value[:i])
            int(value[i+1:])
    except ValueError:
        print('error: entry or exit key must be {int, int} format')
        return 1

    try:
        if key == 'output_file':
            with open(value, 'w'):
                ...
    except Exception:
        print('error: output_file must be valid, for example -> maze.txt')
        return 1

    try:
        if key == 'perfect':
            if value.lower() != 'true' and value.lower() != 'false':
                raise ValueError
    except Exception:
        print('error: perfect key must be set to "True" or "False"')
        return 1
    return 0


def parsing(file: str) -> dict[Any, Any]:
    """Parse and validate a maze configuration file.

    Reads KEY=VALUE pairs, ignores comment lines starting with '#',
    validates all mandatory keys, and converts values to proper types.

    Args:
        file: Path to the configuration file.

    Returns:
        A dict with typed values (width, height as int; entry, exit as
        list[int]; perfect as bool; seed as int; etc.), or an empty dict
        on any error.
    """
    r = dict[str, Any]()
    try:
        with open(file, 'r') as f:
            for line in f:
                if not line.startswith('#') and not line.isspace():
                    i = line.find('=')
                    if i == -1:
                        raise NameError
                    e = line.find('\n')
                    if e == -1:
                        e = len(line)
                    k = line[:i].lower()
                    v = line[i+1:e]
                    if check_value(k, v) == 1:
                        return {}
                    else:
                        r.update({k: v})
    except FileNotFoundError:
        print('error: "config.txt" file not found')
        return dict()
    except NameError:
        print(r'error: each paramater must be in format key=value\n')
        return dict()

    mandatory = ['width', 'height', 'entry', 'exit', 'output_file', 'perfect']
    try:
        for m in mandatory:
            if m not in r.keys():
                raise NameError(m)
    except NameError as n:
        print(f'error: "{n}" key not found in config.txt')
        return dict()

    try:
        v1 = int(r['width'])
        v2 = int(r['height'])
        if v1 < 2 or v2 > 2147483647 \
                or v2 < 2 or v1 > 2147483647:
            raise ValueError('width and length must be \
                             between 2 and 2147483647')
        r.pop("width")
        r.update({'width': v1})
        r.pop("height")
        r.update({'height': v2})

        i = str(r['entry']).find(',')
        e1 = [int(str(r['entry'])[:i]), int(str(r['entry'])[i+1:])]
        if e1[0] >= v1 or e1[1] >= v2:
            raise ValueError('entry must be in height and width range')
        r.pop("entry")
        r.update({'entry': e1})

        i = str(r['exit']).find(',')
        e2 = [int(str(r['exit'])[:i]), int(str(r['exit'])[i+1:])]
        if e2[0] >= v1 or e2[1] >= v2:
            raise ValueError('exit must be in height and width range')
        r.pop("exit")
        r.update({'exit': e2})

        if any(i < 0 for i in r['entry']) or any(i < 0 for i in r['exit']):
            raise ValueError('entry or exit has negative value')
        if r['entry'] == r['exit']:
            raise ValueError("entry and exit shouldn't have same coordinates")

        if r['perfect'].lower() == 'true':
            r['perfect'] = True
        else:
            r['perfect'] = False

        if 'seed' in r.keys() and r['seed'].isdigit():
            r['seed'] = int(r['seed'])
        if 'seed' not in r.keys():
            r.update({'seed': randint(0, 2147483647)})

        if 'animation' in r.keys() and r['animation'].lower() == 'true':
            r['animation'] = True
        elif 'animation' in r.keys():
            r['animation'] = False
        return r
    except ValueError as v:
        print(f'error: {v}')
        return dict()


if __name__ == "__main__":
    parsing('config.txt')
