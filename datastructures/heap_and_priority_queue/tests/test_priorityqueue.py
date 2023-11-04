import unittest
import sys

from dirimporttool import get_super_dir_directly
super_dir = get_super_dir_directly(__file__, 2)
sys.path.append(super_dir)

from heap_and_priority_queue.priorityqueue import PriorityQueue


class TestPQ(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            ('고양이', 15), ('개', 13), ('고슴도치', 14), ('호랑이', 9),
            ('사자', 11), ('바다사자', 12), ('족제비', 14), ('수달', 8),
            ('뱀', 2), ('소', 1), ('펭귄', 10), ('북극곰', 8),
            ('곰', 6), ('원숭이', 9), ('침팬치', 7), ('고릴라', 4),
            ('기린', 5), ('치타', 12),
        ]
        
    def testEmptyPQ(self):
        """
        우선순위 큐 생성 후 출력 테스트. 
        """
        pq = PriorityQueue()
        self.assertEqual(pq.isEmpty(), True)
        self.assertEqual(pq.getCurrentSize(), 0)
        self.assertEqual(pq.__repr__(), "None")
        self.assertEqual(pq.peek(), None)
        self.assertEqual(pq.dequeue(), None)
        self.assertEqual('곰' in pq, False)

    def testEnqueue(self):
        """
        데이터 삽입 테스트. 
        """
        pq = PriorityQueue()
        # case 1
        pq.enqueue('하마', 1)
        self.assertEqual(pq.__repr__(), str([('하마', 1)]))
        self.assertEqual(pq.getCurrentSize(), 1)
        self.assertEqual(pq.isEmpty(), False)

        # case 2
        pq.enqueue(('곰', 12))

        peek_data = pq.peek()
        self.assertEqual(peek_data.value, "곰")
        self.assertEqual(peek_data.priority, 12)

        all_data = pq.showAll()
        all_data.sort()
        self.assertEqual(all_data, sorted([('하마', 1), ('곰', 12)]))

        self.assertEqual(pq.isEmpty(), False)
        self.assertEqual(pq.getCurrentSize(), 2)
        self.assertEqual('곰' in pq, True)
        self.assertEqual(1 in pq, True)

        # case 3
        pq.clear()
        test_data = [
            ('독수리', 5), ('하마', 1), ('기린', 12)
        ]
        for data in test_data:
            pq.enqueue(data)

        expected_result = [('기린', 12), ('독수리', 5), ('하마', 1)]
        self.assertEqual(sorted(pq.showAll()), sorted(expected_result))

    def testDequeue(self):
        """
        데이터 추출 및 삭제 테스트. 
        """
        pq = PriorityQueue()
        
        # case 1
        pq.enqueue('곰', 12)
        get_result = pq.dequeue()
        self.assertEqual(get_result.value, '곰')
        self.assertEqual(get_result.priority, 12)
        self.assertEqual(pq.getCurrentSize(), 0)
        self.assertEqual(pq.isEmpty(), True)
        self.assertEqual(pq.showAll(), [])

        # case 2
        get_result = pq.dequeue()
        self.assertEqual(get_result, None)

if __name__ == '__main__':
    unittest.main()
    