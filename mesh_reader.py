#!/usr/bin/python3.5
import re
from argparse import ArgumentParser


def find_parents(ids, n):
    res = []
    for id in ids:
        id_arr = id.split('.')
        for i in range(n):
            if len(id_arr) == 1:
                break
            if len(res) < i + 1:
                res += [set()]
            id_arr.pop(len(id_arr) - 1)
            res[i].add(numbers['.'.join(id_arr)])
    return res


def find_children(ids, n):
    res = []
    for i in range(n):
        res += [{child for curr_id in ids for key, child in numbers.items() if
                 re.compile(re.escape(curr_id) + '(\.\d+){' + str(i + 1) + '}').fullmatch(key)}]
        if len(res[i]) == 0:
            res.pop(i)
            break
    return res


def init_mesh():
    mesh_file = 'd2018.bin'
    with open(mesh_file, mode='rb') as file:
        mesh = file.readlines()
    term = b'none'
    for line in mesh:
        mesh_term = re.search(b'MH = (.+)$', line)
        mesh_number = re.search(b'MN = (.+)$', line)
        if mesh_term:
            term = mesh_term.group(1).lower()
        if mesh_number:
            number = mesh_number.group(1)
            numbers[number.decode('utf-8')] = term.decode('ascii')
            if term in terms:
                terms[term] = terms[term] + [(number.decode('ascii'))]
            else:
                terms[term] = [number.decode('ascii')]


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-nc', '--n-children', dest='n_children', default=100,
                        help='show n top level children (default: shows all levels of children)')
    parser.add_argument('-np', '--n-parents', dest='n_parents', default=100,
                        help='show n top level parents (default: shows all levels of parents)')

    args = parser.parse_args()
    word = input().lower().encode('ascii')

    numbers = {}
    terms = {}

    init_mesh()
    if word not in terms:
        print('There is no word \"' + word.decode('ascii') + '\"')
    else:
        parents = find_parents(terms[word], int(args.n_parents))
        for i in range(len(parents) - 1, -1, -1):
            print('\nparents: ' + str(i + 1) + ' level\n\t' + '\n\t'.join(parents[i]))

        for i, level_of_children in enumerate(find_children(terms[word], int(args.n_children)), 1):
            print('\nchildren ' + str(i) + ' level:\n\t' + '\n\t'.join(level_of_children))

        print('\nnumbers:\n\t' + '\n\t'.join(terms[word]))
