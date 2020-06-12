import os


path = "C:/BCSpace/study/ThisSemester/Information Retrieval/lab/lab1/20_newsgroups/alt.atheism"
word_freq = {}


def process_file(dst):  # 读文件到缓冲区
    try:  # 打开文件
        f = open(dst, 'r', errors='ignore')
    except IOError as s:
        print(s)
        return None
    try:  # 读文件到缓冲区
        bvffer = f.read()
    except:
        print("Read File Error! " + dst)
        return None
    f.close()
    return bvffer


for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        text = process_file(os.path.join(root, name))
        # text = text.lower()
        # for ch in '“‘!;,.?”':
        #     text = text.lower().replace(ch, " ")
        words = text.strip().split()
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

sorted_word_freq = sorted(word_freq.items(), key=lambda v: v[1], reverse=True)
for item in sorted_word_freq[:1000]:  # 输出 Top 10 的单词
    print(item[0], item[1])
