import unittest
import sys

from dirimporttool import get_super_dir_directly
super_dir = get_super_dir_directly(__file__, 2)
sys.path.append(super_dir)

from queue_.my_queue import StaticQueue, DynamicQueue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.q = StaticQueue(5)
        self.desc = self.shortDescription()
        self.dataset = ['빨강', '주황', '노랑', '초록', '파랑']

        if self.desc == 'need_dataset':
            for data in self.dataset:
                self.q.enqueue(data)

    def test_empty(self):
        """
        빈 큐 테스트.
        """
        self.q.setMsgMode(False)

        self.assertEqual(self.q.__repr__(), '[]')
        self.assertEqual(self.q.isEmpty(), True)
        self.assertEqual(self.q.getCurrentSize(), 0)
        self.assertEqual(self.q.dequeue(), None)
        self.assertEqual(self.q.seek_peek(), None)

    def test_enqueue_dequeue(self):
        """
        큐 항목 삽입 및 추출 테스트.
        """
        self.q.setMsgMode(False)

        # test1
        self.q.enqueue('빨강')
        self.assertEqual(self.q.seek_peek(), '빨강')
        self.assertEqual(self.q.__repr__(), "['빨강']")
        self.assertEqual(self.q.getCurrentSize(), 1)

        # test2
        self.q.enqueue('주황')
        self.assertEqual(self.q.seek_peek(), '빨강')
        self.assertEqual(self.q.__repr__(), "['주황', '빨강']")
        self.assertEqual(self.q.getCurrentSize(), 2)

        # test3
        get_item = self.q.dequeue()
        self.assertEqual(get_item, '빨강')
        self.assertEqual(self.q.seek_peek(), '주황')
        self.assertEqual(self.q.__repr__(), "['주황']")
        self.assertEqual(self.q.getCurrentSize(), 1)

        # test4
        self.q.enqueue('빨강')
        self.assertEqual(self.q.seek_peek(), '주황')
        self.assertEqual(self.q.__repr__(), "['빨강', '주황']")
        self.assertEqual(self.q.getCurrentSize(), 2)

        # test5
        get_item = self.q.dequeue()
        self.assertEqual(get_item, '주황')
        self.assertEqual(self.q.seek_peek(), '빨강')
        self.assertEqual(self.q.__repr__(), "['빨강']")
        self.assertEqual(self.q.getCurrentSize(), 1)

    def test_clear(self):
        """
        need_dataset\n
        큐 내 모든 데이터 삭제 테스트.
        """
        self.q.setMsgMode(False)
        # test1
        self.assertEqual(self.q.getCurrentSize(), 5)
        self.q.clear()
        self.assertEqual(self.q.getCurrentSize(), 0)
        self.assertEqual(self.q.__repr__(), '[]')
        self.assertEqual(self.q.isEmpty(), True)
        self.assertEqual(self.q.dequeue(), None)
        self.assertEqual(self.q.seek_peek(), None)

        # test2
        self.q.clear()
        self.assertEqual(self.q.getCurrentSize(), 0)
        self.assertEqual(self.q.__repr__(), '[]')
        self.assertEqual(self.q.isEmpty(), True)
        self.assertEqual(self.q.dequeue(), None)
        self.assertEqual(self.q.seek_peek(), None)


class TestDynamicQueue(unittest.TestCase):
    def setUp(self):
        self.q = DynamicQueue()
        self.desc = self.shortDescription()
        self.dataset = ['빨강', '주황', '노랑', '초록', '파랑']

        if self.desc == 'need_dataset':
            for data in self.dataset:
                self.q.enqueue(data)

    def tearDown(self):
        self.q.clear()

    def test_empty(self):
        """
        빈 큐 테스트.
        """
        self.q.setMsgMode(False)

        self.assertEqual(self.q.__repr__(), '[]')
        self.assertEqual(self.q.isEmpty(), True)
        self.assertEqual(self.q.getCurrentSize(), 0)
        self.assertEqual(self.q.dequeue(), None)
        self.assertEqual(self.q.seek_peek(), None)

    def test_enqueue_dequeue(self):
        """
        큐 항목 삽입 및 추출 테스트.
        """
        self.q.setMsgMode(False)
        # test1
        self.q.enqueue('빨강')
        self.assertEqual(self.q.seek_peek(), '빨강')
        self.assertEqual(self.q.__repr__(), "['빨강']")
        self.assertEqual(self.q.getCurrentSize(), 1)

        # test2
        self.q.enqueue('주황')
        self.assertEqual(self.q.seek_peek(), '빨강')
        self.assertEqual(self.q.__repr__(), "['주황', '빨강']")
        self.assertEqual(self.q.getCurrentSize(), 2)

        # test3
        get_item = self.q.dequeue()
        self.assertEqual(get_item, '빨강')
        self.assertEqual(self.q.seek_peek(), '주황')
        self.assertEqual(self.q.__repr__(), "['주황']")
        self.assertEqual(self.q.getCurrentSize(), 1)

        # test4
        self.q.enqueue('빨강')
        self.assertEqual(self.q.seek_peek(), '주황')
        self.assertEqual(self.q.__repr__(), "['빨강', '주황']")
        self.assertEqual(self.q.getCurrentSize(), 2)

        # test5
        get_item = self.q.dequeue()
        self.assertEqual(get_item, '주황')
        self.assertEqual(self.q.seek_peek(), '빨강')
        self.assertEqual(self.q.__repr__(), "['빨강']")
        self.assertEqual(self.q.getCurrentSize(), 1)

    def test_clear(self):
        """
        need_dataset\n
        큐 내 모든 데이터 삭제 테스트.
        """
        self.q.setMsgMode(False)
        # test1
        self.assertEqual(self.q.getCurrentSize(), 5)
        self.q.clear()
        self.assertEqual(self.q.getCurrentSize(), 0)
        self.assertEqual(self.q.__repr__(), '[]')
        self.assertEqual(self.q.isEmpty(), True)
        self.assertEqual(self.q.dequeue(), None)
        self.assertEqual(self.q.seek_peek(), None)

        # test2
        self.q.clear()
        self.assertEqual(self.q.getCurrentSize(), 0)
        self.assertEqual(self.q.__repr__(), '[]')
        self.assertEqual(self.q.isEmpty(), True)
        self.assertEqual(self.q.dequeue(), None)
        self.assertEqual(self.q.seek_peek(), None)


if __name__ == '__main__':
    unittest.main()
    