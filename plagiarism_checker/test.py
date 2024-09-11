import unittest
from optimize_main import cos  # 导入模块和函数
from optimize_main import read_text



class TestCosineSimilarity(unittest.TestCase):

    def test_cosine_similarity_identical_texts(self):
        text1 = ['hello', 'world']
        text2 = ['hello', 'world']
        result = cos(text1, text2)
        self.assertEqual(result, 1.0)

    def test_cosine_similarity_different_texts(self):
        text1 = ['hello', 'world']
        text2 = ['goodbye', 'world']
        result = cos(text1, text2)
        self.assertAlmostEqual(result, 0.5, places=4)

    def test_cosine_similarity_empty_texts(self):
        text1 = []
        text2 = []
        result = cos(text1, text2)
        self.assertEqual(result, 0.0)

    def test_cosine_similarity_one_empty_text(self):
        text1 = ['hello']
        text2 = []
        result = cos(text1, text2)
        self.assertEqual(result, 0.0)

    def test_cosine_similarity_single_word_texts(self):
        text1 = ['hello']
        text2 = ['hello']
        result = cos(text1, text2)
        self.assertEqual(result, 1.0)

    def test_cosine_similarity_complex_case(self):
        # 测试更复杂的文本
        text1 = ['the', 'quick', 'brown', 'fox']
        text2 = ['the', 'slow', 'brown', 'dog']
        result = cos(text1, text2)
        self.assertAlmostEqual(result, 0.5, places=4)

    def test_cosine_similarity_case_sensitivity(self):
        # 测试大写和小写字母的相似度
        text1 = ['Hello', 'world']
        text2 = ['hello', 'WORLD']
        result = cos(text1, text2)
        self.assertAlmostEqual(result, 1.0, places=4)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_text('non_existent_file.txt')

    def test_cosine_similarity_partial_overlap(self):
        # 测试部分重叠的文本
        text1 = ['word', 'overlap', 'test']
        text2 = ['overlap', 'test', 'only']
        result = cos(text1, text2)
        self.assertAlmostEqual(result, 0.6667, places=4)

def test_unknown_error(self):
    def faulty_read_text(path):
        raise Exception("未知错误")

    with self.assertRaises(Exception):
        faulty_read_text('some_path.txt')


if __name__ == '__main__':
    unittest.main()
