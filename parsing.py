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
                k = line[:i]
                v = line[i+1:e]
                r.update({k: v})

    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for m in mandatory:
        if m not in r.keys():
            return {}

    r['WIDTH'] = int(r['WIDTH'])
    r['HEIGHT'] = int(r['HEIGHT'])
    i = r['ENTRY'].find(',')
    r['ENTRY'] = [int(r['ENTRY'][:i]), int(r['ENTRY'][i+1:])]
    i = r['EXIT'].find(',')
    r['EXIT'] = [int(r['EXIT'][:i]), int(r['EXIT'][i+1:])]
    if r['PERFECT'] == 'True':
        r['PERFECT'] = True
    else:
        r['PERFECT'] = False
    print(r)
    return r


if __name__ == "__main__":
    parsing()
