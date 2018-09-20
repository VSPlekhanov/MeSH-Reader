#!/usr/bin/python3.5
import re
from argparse import ArgumentParser
import json

numbers_to_terms = {}
terms_to_numbers = {}
entries_to_terms = {}
terms_to_entries = {}
non_latin_entries = []


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
            res[i].add(numbers_to_terms['.'.join(id_arr)])
    return res


def find_children(ids, n):
    res = []
    for i in range(1, n + 1):
        string_pattern = '(\.\d+){' + str(i) + '}'
        res += [{child for curr_id in ids for key, child in numbers_to_terms.items() if
                 len(key) == len(curr_id) + 4 * i and
                 re.compile(re.escape(curr_id) + string_pattern).fullmatch(key)}]
        if len(res[i - 1]) == 0:
            res.pop(i - 1)
            break
    return res


def init_mesh():
    global non_latin_entries
    mesh_file = 'd2018.bin'
    with open(mesh_file, mode='rb') as file:
        mesh = file.readlines()
    term = 'none'
    for line in mesh:
        mesh_term = re.search(b'MH = (.+)$', line)
        mesh_number = re.search(b'MN = (.+)$', line)
        mesh_entry = re.search(b'ENTRY = ([^|]+)(.*)$', line)
        if mesh_term:
            term = mesh_term.group(1).decode('ascii').lower()
        if mesh_number:
            number = mesh_number.group(1).decode('ascii')
            numbers_to_terms[number] = term
            if term in terms_to_numbers:
                terms_to_numbers[term] = terms_to_numbers[term] + [number]
            else:
                terms_to_numbers[term] = [number]
        if mesh_entry:
            try:
                entry = mesh_entry.group(1)
                entry = entry.decode('ascii').strip().lower().replace(',', '')
            except UnicodeDecodeError:
                non_latin_entries += [entry]
                continue
            entries_to_terms[entry] = term
            if term in terms_to_entries:
                terms_to_entries[term] = terms_to_entries[term] + [entry]
            else:
                terms_to_entries[term] = [entry]


def tmp():
    tmp_dict = {}
    with open('dict.json', 'a') as d:
        for key, value in terms_to_entries.items():
            tmp_dict['key'] = 'key: ' + key
            tmp_dict['value'] = ['value: ' + val for val in value]
            d.write(json.dumps(tmp_dict) + '\n')


def main(term):
    if term == 'exit()':
        exit(0)
    if term not in terms_to_numbers:
        if term in entries_to_terms:
            main(entries_to_terms[term])
        else:
            print('There is no term \"' + term + '\"')
    else:
        print('\t\t\t\t' + term)
        parents = find_parents(terms_to_numbers[term], int(args.n_parents))
        for i in range(len(parents) - 1, -1, -1):
            print('\nparents: ' + str(i + 1) + ' level\n\t' + '\n\t'.join(parents[i]))

        for i, level_of_children in enumerate(find_children(terms_to_numbers[term], int(args.n_children)), 1):
            print('\nchildren ' + str(i) + ' level:\n\t' + '\n\t'.join(level_of_children))

        if term in terms_to_entries:
            print('\nentries:\n\t' + '\n\t'.join(terms_to_entries[term]))
        print('\nnumbers:\n\t' + '\n\t'.join(terms_to_numbers[term]))
        with open('entries_map.json', 'w') as out:
            out.write(json.dumps(entries_to_terms))
        with open('entries_map_reversed.json', 'w') as r_out:
            r_out.write(json.dumps(terms_to_entries))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-nc', '--n-children', dest='n_children', default=100,
                        help='show n top level children (default: shows all levels of children)')
    parser.add_argument('-np', '--n-parents', dest='n_parents', default=100,
                        help='show n top level parents (default: shows all levels of parents)')
    args = parser.parse_args()
    init_mesh()
    # tmp()
    while True:
        main(input('\nInput term: \t\t\t\t\t\t\t\t (type exit() to close program)\n\t').lower())
