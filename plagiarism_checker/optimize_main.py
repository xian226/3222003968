import os
import jieba  # jieba库，用于中文分词
import re


# 进行读取文本文件工作
def read_text(path):
    try:
        str = ''
        file = open(path, 'r', encoding='UTF-8')  # 打开文件，以 UTF-8 编码方式处理
        line = file.readline()
        while line:
            str += line
            line = file.readline()
        # 循环中再次调用file.readline()读取文件的一行
        file.close()
        return str
    except FileNotFoundError as e:
        print("错误：文件未找到。请检查路径是否正确。")
        raise e
    except Exception as e:
        print(f"发生未知错误：{e}")
        raise e


# 进行文本清洗和分词工作 (文本清洗：去除标点、统一大小写等)
def text_clean(str):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    str = pattern.sub("", str).lower()  # 转换为小写
    str = pattern.sub("", str)
    # 文本清洗。定义正则表达式匹配模式，其中^匹配字符串的开头,保留a-z、A-Z、0-9和汉字
    new = []
    new = [i for i in jieba.cut(str, cut_all=False) if i != '']  # 进行分词。cut_all=False精确
    return new


# 利用余弦公式来计算文本相似度
import numpy as np


def cos(new1, new2):
    vocabulary = set(new1).union(set(new2))
    word_dict = {word: i for i, word in enumerate(vocabulary)}
    vector1 = np.zeros(len(vocabulary), dtype=int)
    vector2 = np.zeros(len(vocabulary), dtype=int)

    for word in new1:
        vector1[word_dict[word]] += 1
    for word in new2:
        vector2[word_dict[word]] += 1

    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if norm1 == 0 or norm2 == 0:
        return 0.0
    else:
        return round(dot_product / (norm1 * norm2), 4)

def main():
    base_path = r'E:/plagiarism_checker/articles'
    output_paths = {
        'add': os.path.join(base_path, 'result/add_result.txt'),    #输出
        'del': os.path.join(base_path, 'result/del_result.txt'),
        'dis_1': os.path.join(base_path, 'result/dis_1_result.txt'),
        'dis_10': os.path.join(base_path, 'result/dis_10_result.txt'),
        'dis_15': os.path.join(base_path, 'result/dis_15_result.txt')
    }
    paths = [
        os.path.join(base_path, 'orig.txt'),  # 原文
        os.path.join(base_path, 'orig_0.8_add.txt'),
        os.path.join(base_path, 'orig_0.8_del.txt'),
        os.path.join(base_path, 'orig_0.8_dis_1.txt'),
        os.path.join(base_path, 'orig_0.8_dis_10.txt'),
        os.path.join(base_path, 'orig_0.8_dis_15.txt')
    ]
    # 读取和清洗文本
    texts = [text_clean(read_text(path)) for path in paths]
    # 计算相似度
    results = [
        cos(texts[0], texts[1]),  # orig.txt vs orig_0.8_add.txt
        cos(texts[0], texts[2]),  # orig.txt vs orig_0.8_del.txt
        cos(texts[0], texts[3]),  # orig.txt vs orig_0.8_dis_1.txt
        cos(texts[0], texts[4]),  # orig.txt vs orig_0.8_dis_10.txt
        cos(texts[0], texts[5])  # orig.txt vs orig_0.8_dis_15.txt
    ]
    # 打印结果
    for label, result in zip(output_paths.keys(), results):
        print(f"与{label}的相似度为： {result:.4f}")

    # 将结果记录到文件中
    for label, result in zip(output_paths.keys(), results):
        with open(output_paths[label], 'w', encoding='utf-8') as file:
            file.write(f"与{label}的相似度为： {result:.4f}\n")
            file.close()





if __name__ == '__main__':
    main()
