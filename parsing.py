#!/usr/bin/env python3


def check_value(key: str, value: str) -> int:
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
        print(r'error: entry or exit key must be {number},{number} format')
        return 1
    
    try:
        if key == 'output_file':
            with open(value, 'r'):
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

def parsing(file: str) -> dict:
    r = {}
    try:
        with open(file, 'r') as f:
            for line in f:
                if not line.startswith('#'):
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
        return {}
    except NameError:
        print(r'error: each paramater must be in format key=value\n')
        return {}

    mandatory = ['width', 'height', 'entry', 'exit', 'output_file', 'perfect']
    try:
        for m in mandatory:
            if m not in r.keys():
                raise NameError(m)
    except NameError as n:
        print(f'error: "{n}" key not found in config.txt')
        return {}

    try:
        r['width'] = int(r['width'])
        r['height'] = int(r['height'])
        if r['width'] < 2 or r['height'] < 2:
            raise ValueError

        i = r['entry'].find(',')
        r['entry'] = [int(r['entry'][:i]), int(r['entry'][i+1:])]
        if r['entry'][0] >= r['width'] or r['entry'][1] >= r['height']:
            raise ValueError

        i = r['exit'].find(',')
        r['exit'] = [int(r['exit'][:i]), int(r['exit'][i+1:])]
        if r['exit'][0] >= r['width'] or r['exit'][1] >= r['height']:
            raise ValueError

        if any(i < 0 for i in r['entry']) or any(i < 0 for i in r['exit']):
            raise ValueError
        if r['entry'] == r['exit']:
            raise ValueError

        if r['perfect'].lower() == 'true':
            r['perfect'] = True
        else:
            r['perfect'] = False
        return r
    except ValueError as v:
        print('error')
        return {}


if __name__ == "__main__":
    parsing('config.txt')
