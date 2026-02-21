#!/usr/bin/env python3


def parsing() -> dict:
    r = {}
    with open('config.txt', 'r') as f:
        for line in f:
            if not line.startswith('#'):
                i = line.find('=')
                e = line.find('\n')
                if e == -1:
                    e = len(line)
                k = line[:i].lower()
                v = line[i+1:e]
                r.update({k: v})

    # for key in r.keys():
    #     print(key)
    #     key = key.lower()
    #     print(key)

    mandatory = ['width', 'height', 'entry', 'exit', 'output_file', 'perfect']
    for m in mandatory:
        print(m)
        print(r.keys())
        if m not in r.keys():
            return {}

    r['width'] = int(r['width'])
    r['height'] = int(r['height'])
    i = r['entry'].find(',')
    r['entry'] = [int(r['entry'][:i]), int(r['entry'][i+1:])]
    i = r['exit'].find(',')
    r['exit'] = [int(r['exit'][:i]), int(r['exit'][i+1:])]
    if r['perfect'] == 'True':
        r['perfect'] = True
    else:
        r['perfect'] = False
    print(r)
    return r


if __name__ == "__main__":
    parsing()
