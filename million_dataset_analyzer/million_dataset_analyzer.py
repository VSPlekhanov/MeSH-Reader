#!/usr/bin/python3.5
import json
import re

minimum = 1000
maximum = 0
total = 0
data_len = 0
terms = {}
r_terms = {}
entries = {}
INDEX_FOR_RAW_DATA = 'letterAbstract'
INDEX_FOR_PROCESSED_DATA = 'letterAbstract_processed'
INDEX_2 = 'all_features'
p_entries = {}
r_p_entries = {}
zeros = 0
no_mesh_words = set()


def init_terms_maps():
    import json
    global terms, r_terms, entries, p_entries, r_p_entries
    with open('map.json', mode='r') as terms_map:
        terms = json.loads(terms_map.read())
    with open('map_reversed.json', mode='r') as r_terms_map:
        r_terms = json.loads(r_terms_map.read())
    with open('entries_map.json') as entries_map:
        entries = json.loads(entries_map.read())
    with open('p_entries_map.json') as _map:
        p_entries = json.loads(_map.read())
    with open('r_p_entries_map.json') as r_map:
        r_p_entries = json.loads(r_map.read())


def process_file(file):
    import json
    with open(file, mode='r') as input:
        return [json.loads(line) for line in input.readlines()]


def get_data_pairs(data):
    global data_len
    data_len += len(data)
    data_pairs = []
    for article in data:
        article_data = set()
        for i in range(1, len(article[INDEX_2])):
            if article[INDEX_2][i - 1] != '' and article[INDEX_2][i] != '':
                article_data.add(article[INDEX_2][i - 1] + ' ' + article[INDEX_2][i])
                # article_data.add(article[INDEX_2][i] + ' ' + article[INDEX_2][i - 1])

        data_pairs += [(article_data, article['id'])]
    return data_pairs


def get_data_words(data):
    global data_len
    data_len += len(data)
    return [({term for term in article[INDEX_2]}, article['id']) for article in data]


def compute(data):
    global r_terms, total, maximum, minimum, zeros, no_mesh_words
    for article, a_id in data:
        count = 0
        for term in article:
            if term in r_terms or term in r_p_entries:
                count += 1
        if count == 0:
            if a_id in no_mesh_words:
                print(a_id)
            zeros += 1
        total += count
        if count > maximum:
            maximum = count
        if count < minimum:
            minimum = count


def main():
    init_terms_maps()
    global total, terms, r_terms, minimum, maximum, r_p_entries, p_entries, zeros, no_mesh_words

    no_mesh_words = {
        32947044,
        22408454,
        29136075,
        29002729,
        35605507,
        26842075,
        23551529,
        23463712,
        24104293,
        28197861
    }


    # files_arr = ['../../small_data/part-00000-a2d14103-4a3f-44b2-bf68-f554c79953ff-c000.json']
    files_arr = [
        "../../million/processed/part-00000-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00001-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00002-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00003-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00004-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00005-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00006-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00007-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00008-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00009-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00010-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00011-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json",
        "../../million/processed/part-00012-792100ba-67d5-45dc-bb11-b7790fe70fdd-c000.json"
    ]

    for file in files_arr:
        compute(get_data_pairs(process_file(file)))

    print(len(entries))
    print('total = ' + str(total))
    print('articles count = ' + str(data_len))
    print('average = ' + str(total / data_len))
    print('min = ' + str(minimum))
    print('max = ' + str(maximum))
    print(zeros)


if __name__ == '__main__':
    main()
