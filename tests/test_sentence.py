import unittest

from question_answering.dataset.sentence import Sentence


class TestSentence(unittest.TestCase):
    def test_sentence_ctor(self):
        sentence = Sentence('Tôi là sinh viên trường Đại học Tôn Đức Thắng tại Quận 7')
        list1 = sentence.words
        list2 = ['tôi', 'sinh_viên', 'trường', 'đại_học', 'tôn_đức_thắng', 'quận', '7']
        self.assertListEqual(list1, list2)

        sentence = Sentence(['Tôi', 'là', 'sinh_viên', 'trường', 'Đại_học', 'Tôn_Đức_Thắng', 'tại', 'Quận', '7'])
        list1 = sentence.words
        list2 = ['tôi', 'sinh_viên', 'trường', 'đại_học', 'tôn_đức_thắng', 'quận', '7']
        self.assertListEqual(list1, list2)

    def test_sentence_has(self):
        sentence = Sentence('Tôi là sinh viên trường Đại học Tôn Đức Thắng tại Quận 7')
        self.assertTrue(sentence.has('sinh_viên'))
        self.assertTrue(sentence.has('đại_học'))
        self.assertTrue(sentence.has('tôn_đức_thắng'))

    def test_sentence_count(self):
        sentence = Sentence('Tôi là sinh viên trường Đại học Tôn Đức Thắng tại Quận 7')
        self.assertEqual(sentence.count('tôi'), 1)
        self.assertEqual(sentence.count('là'), 0)
        self.assertEqual(sentence.count('sinh_viên'), 1)


if __name__ == '__main__':
    unittest.main()
