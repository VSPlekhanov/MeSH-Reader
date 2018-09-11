import re
import json

terms = {}
numbers = {}
raw2processed = {}


def init_mesh():
    with open('tmp.txt', mode='r') as file:
        mesh = file.readlines()
    term = 'none'
    for line in mesh:
        mesh_term = re.search('MH = (.+)$', line)
        mesh_number = re.search('MN = (.+)$', line)
        if mesh_term:
            term = mesh_term.group(1).lower()
        if mesh_number:
            number = mesh_number.group(1)
            numbers[number] = term
            if term in terms:
                terms[term] = terms[term] + [(number)]
            else:
                terms[term] = [number]


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
    for i in range(1, n + 1):
        string_pattern = '(\.\d+){' + str(i) + '}'
        # children_set = set()
        #
        # for key, child in numbers.items():
        #     for curr_id in ids:

        res += [{child for curr_id in ids for key, child in numbers.items() if
                 len(key) == len(curr_id) + 4 * i and
                 re.compile(re.escape(curr_id) + string_pattern).fullmatch(key)}]
        if len(res[i - 1]) == 0:
            res.pop(i - 1)
            break
    return res


if __name__ == '__main__':
    with open('data.json') as file:
        data = json.loads(file.read())
    print(len(data))
    # init_mesh()
    # print(len(terms))
    # print(len(numbers))
    # print(terms)
    # print(numbers)
