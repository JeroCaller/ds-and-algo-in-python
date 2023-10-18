import unittest
import sys
from dirimporttool import get_super_dir_directly
super_dir = get_super_dir_directly(__file__, 2)
sys.path.append(super_dir)
from linked_list.linked_list_kv import (LinkedList)


class TestLinkedList(unittest.TestCase):
    def setUp(self) -> (None):
        self.ll = LinkedList()
        self.test_dataset = [
            ('책', 12000),
            ('계산기', 5000),
            ('이어폰', 20000),
            ('립밤', 5000),
        ]
        self.desc = self.shortDescription()

        if self.desc == 'need_dataset':
            for data in self.test_dataset:
                self.ll.addNodeBack(data)

    def tearDown(self) -> (None):
        self.ll.clear()

    def testEmpty(self):
        """
        빈 연결리스트 테스트. 
        """
        self.assertEqual(self.ll.__repr__(), "<empty>")
        self.assertEqual(self.ll.getLength(), 0)
        self.assertEqual(self.ll.items(), [])
        self.assertEqual(self.ll.keys(), [])
        self.assertEqual(self.ll.values(), [])

    def testIter(self):
        """
        need_dataset\n
        __iter__() 메서드 테스트. 
        """
        self.ll.iterMode(False)
        all_items = []
        for item in self.ll:
            all_items.append(item)
        self.assertEqual(
            all_items,
            [
                ('책', 12000),
                ('계산기', 5000),
                ('이어폰', 20000),
                ('립밤', 5000),
            ]
            )
        
    def testRepr(self):
        """
        need_dataset\n
        __repr__() 메서드 테스트. 
        """
        expected_result = \
        "('책', 12000) -> ('계산기', 5000) -> ('이어폰', 20000) -> ('립밤', 5000)"
        self.assertEqual(self.ll.__repr__(), expected_result)

    def testFindNodeByKey(self):
        """
        need_dataset\n
        FindNodeByKey() 메서드 테스트. 
        """
        find_node, find_idx, p = self.ll.findNodeByKey('계산기')
        self.assertEqual(find_node.item, ('계산기', 5000))
        self.assertEqual(find_node.key, '계산기')
        self.assertEqual(find_node.value, 5000)
        self.assertEqual(find_idx, 1)

    def testAddNodeFront(self):
        """
        need_dataset\n
        addNodeFront() 메서드 테스트. 
        """
        # test 1
        self.ll.addNodeFront('우산', 10000)
        expected_result = [
            ('우산', 10000),
            ('책', 12000),
            ('계산기', 5000),
            ('이어폰', 20000),
            ('립밤', 5000),
        ]
        self.assertEqual(self.ll.items(), expected_result)
        self.assertEqual(self.ll.keys(), ['우산', '책', '계산기', '이어폰', '립밤'])
        self.assertEqual(self.ll.values(), [10000, 12000, 5000, 20000, 5000])
        self.assertEqual(self.ll.getLength(), 5)
        ex_re = "('우산', 10000) -> ('책', 12000) -> ('계산기', 5000) -> ('이어폰', 20000) -> ('립밤', 5000)"
        self.assertEqual(self.ll.__repr__(), ex_re)

        # test 2
        # 기존의 연결리스트에 존재하는 동일한 키와 다른 값을 입력하는 경우.
        self.ll.addNodeFront('계산기', 20000)
        ex_re = [
            ('우산', 10000), 
            ('책', 12000),
            ('계산기', 20000),
            ('이어폰', 20000),
            ('립밤', 5000),
        ]
        self.assertEqual(self.ll.items(), ex_re)
        self.assertEqual(self.ll.keys(), ['우산', '책', '계산기', '이어폰', '립밤'])
        self.assertEqual(self.ll.values(), [10000, 12000, 20000, 20000, 5000])
        self.assertEqual(self.ll.getLength(), 5)
        ex_re = "('우산', 10000) -> ('책', 12000) -> ('계산기', 20000) -> ('이어폰', 20000) -> ('립밤', 5000)"
        self.assertEqual(self.ll.__repr__(), ex_re)

    def testAddNodeBack(self):
        """
        need_dataset\n
        addNodeBack() 메서드 테스트. 
        """
        # test 1
        ex_re = [
            ('책', 12000),
            ('계산기', 5000),
            ('이어폰', 20000),
            ('립밤', 5000),
        ]
        self.assertEqual(self.ll.items(), ex_re)
        self.assertEqual(self.ll.keys(), ['책', '계산기', '이어폰', '립밤'])
        self.assertEqual(self.ll.values(), [12000, 5000, 20000, 5000])
        self.assertEqual(self.ll.getLength(), 4)

        # test 2
        self.ll.addNodeBack('책', 20000)
        ex_re = [
            ('책', 20000),
            ('계산기', 5000),
            ('이어폰', 20000),
            ('립밤', 5000),
        ]
        self.assertEqual(self.ll.items(), ex_re)
        self.assertEqual(self.ll.keys(), ['책', '계산기', '이어폰', '립밤'])
        self.assertEqual(self.ll.values(), [20000, 5000, 20000, 5000])
        self.assertEqual(self.ll.getLength(), 4)

    def testPop(self):
        """
        need_dataset\n
        popFront(), popBack() 메서드 테스트. 
        """
        self.assertEqual(self.ll.popFront(False), ('책', 12000))
        self.assertEqual(self.ll.getLength(), 3)
        self.assertEqual(self.ll.remainingNodeNumbers(), 3)
        self.assertEqual(self.ll.items(), [
            ('계산기', 5000),
            ('이어폰', 20000),
            ('립밤', 5000),
        ])
        self.assertEqual(self.ll.keys(), ['계산기', '이어폰', '립밤'])
        self.assertEqual(self.ll.values(), [5000, 20000, 5000])

        self.assertEqual(self.ll.popBack(False), ('립밤', 5000))
        self.assertEqual(self.ll.getLength(), 2)
        self.assertEqual(self.ll.remainingNodeNumbers(), 2)
        self.assertEqual(self.ll.items(), [
            ('계산기', 5000),
            ('이어폰', 20000),
        ])
        self.assertEqual(self.ll.keys(), ['계산기', '이어폰'])
        self.assertEqual(self.ll.values(), [5000, 20000])

    def testDeleteNodeByKey(self):
        """
        need_dataset\n
        deleteNodeByKey() 메서드 테스트.
        """
        # test 1
        # 중간에 있는 노드 삭제 테스트.
        target_key = '이어폰'
        self.ll.deleteNodeByKey(target_key)
        ex_re = [
            ('책', 12000),
            ('계산기', 5000),
            ('립밤', 5000),
        ]
        self.assertEqual(self.ll.items(), ex_re)
        self.assertEqual(self.ll.keys(), ['책', '계산기', '립밤'])
        self.assertEqual(self.ll.values(), [12000, 5000, 5000])
        self.assertEqual(self.ll.getLength(), 3)
        self.assertEqual(self.ll.remainingNodeNumbers(), 3)
        self.assertEqual(self.ll.getValueByKey(target_key), None)
        self.assertEqual(self.ll.findNodeByKey(target_key), (None, None, None))

        # test 2
        # 맨 처음에 있는 노드 삭제 테스트. 
        target_key = '책'
        self.ll.deleteNodeByKey(target_key)
        ex_re = [
            ('계산기', 5000),
            ('립밤', 5000),
        ]
        self.assertEqual(self.ll.items(), ex_re)
        self.assertEqual(self.ll.keys(), ['계산기', '립밤'])
        self.assertEqual(self.ll.values(), [5000, 5000])
        self.assertEqual(self.ll.getLength(), 2)
        self.assertEqual(self.ll.remainingNodeNumbers(), 2)
        self.assertEqual(self.ll.getValueByKey(target_key), None)
        self.assertEqual(self.ll.findNodeByKey(target_key), (None, None, None))

        # test 3
        # 맨 마지막에 있는 노드 삭제 테스트. 
        target_key = '립밤'
        self.ll.deleteNodeByKey(target_key)
        ex_re = [
            ('계산기', 5000),
        ]
        self.assertEqual(self.ll.items(), ex_re)
        self.assertEqual(self.ll.keys(), ['계산기'])
        self.assertEqual(self.ll.values(), [5000])
        self.assertEqual(self.ll.getLength(), 1)
        self.assertEqual(self.ll.remainingNodeNumbers(), 1)
        self.assertEqual(self.ll.getValueByKey(target_key), None)
        self.assertEqual(self.ll.findNodeByKey(target_key), (None, None, None))

if __name__ == '__main__':
    unittest.main()
    