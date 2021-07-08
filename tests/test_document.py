import unittest

from question_answering.dataset.sentence import Sentence
from question_answering.dataset.document import Document


class TestDocument(unittest.TestCase):
    def test_document_ctor(self):
        sentence1 = Sentence('Tôi là sinh viên trường Đại học Tôn Đức Thắng tại Quận 7')
        sentence2 = Sentence('Tôi là thành viên câu lạc bộ học thuật ICON')

        document = Document([sentence1, sentence2])
        list1 = document.sentences
        list2 = [sentence1, sentence2]
        self.assertListEqual(list1, list2)

        document = Document(sentence1)
        list1 = document.sentences
        list2 = [sentence1]
        self.assertListEqual(list1, list2)

    def test_document_has(self):
        sentence1 = Sentence('Tôi là sinh viên trường Đại học Tôn Đức Thắng tại Quận 7')
        sentence2 = Sentence('Tôi là thành viên câu lạc bộ học thuật ICON')
        document = Document([sentence1, sentence2])

        self.assertTrue(document.has('đại_học'))
        self.assertTrue(document.has('tôn_đức_thắng'))
        self.assertTrue(document.has('thành_viên'))
        self.assertTrue(document.has('câu_lạc_bộ'))
        self.assertTrue(document.has('học_thuật'))

    def test_document_count(self):
        sentence1 = Sentence('Tôi là sinh viên trường Đại học Tôn Đức Thắng tại Quận 7')
        sentence2 = Sentence('Tôi là thành viên câu lạc bộ học thuật ICON')
        document = Document([sentence1, sentence2])

        self.assertEqual(document.count('tôi'), 2)
        self.assertEqual(document.count('là'), 0)
        self.assertEqual(document.count('sinh_viên'), 1)
        self.assertEqual(document.count('thành_viên'), 1)


if __name__ == '__main__':
    unittest.main()
