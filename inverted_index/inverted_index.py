import os
import re
import nltk

path_root = "C:/BCSpace/study/ThisSemester/Information Retrieval/lab/lab2"
dir_source = "mini_newsgroups_lab2"
dir_new = "new_newsgroups_lab2"  # new folder for the processed files
path_source = os.path.join(path_root, dir_source)
path_new = os.path.join(path_root, dir_new)
terms_data = {}
words_freq = {}
inverted_index = {}
file_list = [-1]
file_id = {}
file_dir = {}


def process_id():
    for root, dirs, files in os.walk(path_source, topdown=True):
        temp_list = []
        for name in files:
            temp_list.append(name)
            file_dir[name] = os.path.join(root, name)
            file_id[name] = root
        if len(temp_list) <= 0:
            continue
        temp_list.sort()
        file_list.extend(temp_list)

    for index in range(len(file_list)):
        file_id[file_list[index]] = index


def process_new_file():
    if not os.path.exists(path_new):
        os.mkdir(path_new)

    for root, dirs, files in os.walk(path_source, topdown=True):
        for dir_name in dirs:
            if not os.path.exists(os.path.join(path_new, dir_name)):
                os.mkdir(os.path.join(path_new, dir_name))

    for root, dirs, files in os.walk(path_source, topdown=True):
        for file_name in files:
            f = open(os.path.join(root, file_name), 'r', errors='ignore')
            text = f.read()
            rtval = re.search(r"Lines:\s+(\d+)", text)
            lines = int(rtval.group(1))
            f.seek(0)
            body = f.readlines()[-lines:]
            # print(len(body))
            f.close()
            f = open(os.path.join(root, file_name).replace('mini', 'new'), 'w+')
            for s in body:
                f.write(s)
            f.close()


def read_file(file_name):
    f = open(file_name, 'r')
    buffer = f.read()
    f.close()
    return buffer


def process_inverted_index():
    for root, dirs, files in os.walk(path_new, topdown=True):
        for file_name in files:
            doc = read_file(os.path.join(root, file_name))
            doc = doc.lower()
            word_tokenizer = nltk.RegexpTokenizer('[A-Za-z]+')
            terms = word_tokenizer.tokenize(doc)
            terms = set(terms)
            for term in terms:
                if term in terms_data:
                    terms_data[term].add(file_id[file_name])
                else:
                    terms_data[term] = {file_id[file_name]}
    for term, belongs in terms_data.items():
        lst = list(belongs)
        lst.sort()
        inverted_index[term] = lst
    f = open(os.path.join(path_root, 'inverted_index.csv'), 'w+')

    sorted_inverted_index = sorted(inverted_index.items(), key=lambda v: v[0])
    for word, l in sorted_inverted_index:
        f.write(word + ',' + str(len(l)))
        for it in l:
            f.write(',' + str(it))
        f.write('\n')


def merge_and(a, b):
    temp_list = []
    index_a = 0
    index_b = 0
    while index_a < len(a) or index_b < len(b):
        if index_b == len(b) or (index_a < len(a) and a[index_a] < b[index_b]):
            index_a = index_a + 1
        elif index_a == len(a) or a[index_a] > b[index_b]:
            index_b = index_b + 1
        else:
            temp_list.append(a[index_a])
            index_a = index_a + 1
            index_b = index_b + 1
    return temp_list


def merge_or(a, b):
    temp_list = []
    index_a = 0
    index_b = 0
    while index_a < len(a) or index_b < len(b):
        if index_b == len(b) or (index_a < len(a) and a[index_a] <= b[index_b]):
            temp_list.append(a[index_a])
            index_a = index_a + 1
        else:
            temp_list.append(b[index_b])
            index_b = index_b + 1
    return temp_list


def merge_not(a, b):
    temp_list = []
    index_a = 0
    index_b = 0
    while index_a < len(a) or index_b < len(b):
        if index_b == len(b) or (index_a < len(a) and a[index_a] < b[index_b]):
            temp_list.append(a[index_a])
            index_a = index_a + 1
        elif index_a == len(a) or a[index_a] > b[index_b]:
            index_b = index_b + 1
        else:
            index_a = index_a + 1
            index_b = index_b + 1
    return temp_list


def query():
    q = input()
    q = q.lower()
    word_tokenizer = nltk.RegexpTokenizer('[A-Za-z]+')
    terms = word_tokenizer.tokenize(q)
    ans = inverted_index[terms[0]]
    for index in range(1, len(terms), 2):
        if terms[index] == 'and':
            ans = merge_and(ans, inverted_index[terms[index + 1]])
        elif terms[index] == 'or':
            ans = merge_or(ans, inverted_index[terms[index + 1]])
        else:
            ans = merge_not(ans, inverted_index[terms[index + 1]])
    print(str(ans)[1:][:-1])


# process_new_file()
process_id()
process_inverted_index()
query()
