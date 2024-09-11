import os
import jieba  # jieba库，用于中文分词
import math
import re


def read_text(path):
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            return file.read()
    except FileNotFoundError:
        print("错误：文件未找到。请检查路径是否正确。")
    except Exception as e:
        print(f"发生未知错误：{e}")

def text_clean(str):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    str = pattern.sub("", str)
    # 文本清洗。定义正则表达式匹配模式，其中^匹配字符串的开头,保留a-z、A-Z、0-9和汉字
    new = []
    new = [i for i in jieba.cut(str, cut_all=False) if i != '']  # 进行分词。cut_all=False精确
    return new

def cos(new1, new2):
    word_set = set(new1).union(set(new2))
    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1
    text1_cut_index = [0] * len(word_dict)
    text2_cut_index = [0] * len(word_dict)
    for word in new1:
        text1_cut_index[word_dict[word]] += 1
    for word in new2:
        text2_cut_index[word_dict[word]] += 1
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(text1_cut_index)):
        sum += text1_cut_index[i] * text2_cut_index[i]
        sq1 += pow(text1_cut_index[i], 2)
        sq2 += pow(text2_cut_index[i], 2)
    try:
        cos_result = round(float(sum) / (math.sqrt(sq1)*math.sqrt(sq2)), 4)
    except ZeroDivisionError:
        cos_result = 0.0
    return cos_result

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