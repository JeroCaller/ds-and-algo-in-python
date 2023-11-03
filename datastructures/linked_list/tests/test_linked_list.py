"""
my_linked_list의 여러 형태의 연결 리스트들을 모두 테스트하는 모듈. 
"""

import unittest
from collections import namedtuple
import sys

from dirimporttool import get_super_dir_directly
super_dir = get_super_dir_directly(__file__, 2)
sys.path.append(super_dir)

from linked_list.my_linked_list import (
    LinkedList, LinkedListQueue, LinkedListStack, 
    DoublyLinkedList, CircularLinkedList)


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.linked_list = LinkedList()
        self.desc = self.shortDescription()

        # 테스트에 따른 fixture 설정.
        if self.desc == "test_add_node_front":
            self.linked_list.addNodeFront('a')

        elif self.desc == "test_add_node_back":
            test_nodes = ['a', 'b']
            for one_node in test_nodes:
                self.linked_list.addNodeBack(one_node)

        elif self.desc == 'need_dataset':
            test_values = ['a', 'b', 'c', 'd']
            for one_value in test_values:
                self.linked_list.addNodeBack(one_value)

    def tearDown(self):
        self.linked_list.clear()

    def test_empty(self):
        """
        비어있는 연결 리스트 출력 테스트
        """
        self.assertEqual(self.linked_list.__repr__(), "빈 연결리스트.")
        self.assertEqual(self.linked_list.getLength(), 0)

    def test_add_node_front(self):
        """
        test_add_node_front\n
        노드 하나를 맨 앞에 삽입하는 데에 성공하는지 테스트.
        """
        expected_result = ' -> '.join(['a'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 1)

    def test_add_node_back(self):
        """
        test_add_node_back\n
        노드 하나를 맨 뒤에 삽입하는 테스트.
        """
        expected_result = ' -> '.join(['a', 'b'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 2)

    def test_find_node_by_index(self):
        """
        need_dataset\n
        주어진 인덱스의 노드를 찾을 수 있는지 테스트.
        """
        # test1
        test_index = 2
        actual_result = self.linked_list.findNodeByIndex(test_index)
        actual_result = (
            actual_result[0].value, 
            actual_result[1],
            actual_result[2].value,
            )
        expected_result = ('c', 2, 'b')
        self.assertEqual(actual_result, expected_result)

        # test2
        test_index = -1
        with self.assertRaises(IndexError):
            self.linked_list.findNodeByIndex(test_index)

        # test3. IndexError 테스트.
        test_index = 4
        with self.assertRaises(IndexError):
            self.linked_list.findNodeByIndex(test_index)

        # test4
        test_index = 0
        actual_result = self.linked_list.findNodeByIndex(test_index)
        actual_result = (
            actual_result[0].value, 
            actual_result[1],
            actual_result[2],
            )
        expected_result = ('a', 0, None)
        self.assertEqual(actual_result, expected_result)

        # test5
        test_index = 0
        actual_result = self.linked_list.getValueByIndex(test_index)
        expected_result = 'a'
        self.assertEqual(actual_result, expected_result)

    def test_find_node_by_value(self):
        """
        need_dataset\n
        주어진 값에 해당하는 노드를 찾을 수 있는지 테스트.
        """
        # test1
        test_value = 'b'
        actual_result = self.linked_list.findNodeByValue(test_value)
        actual_result = (
            actual_result[0].value, 
            actual_result[1],
            actual_result[2].value
            )
        expected_result = ('b', 1, 'a')
        self.assertEqual(actual_result, expected_result)

        # test2
        test_value = 'e'
        actual_result = self.linked_list.findNodeByValue(test_value)
        expected_result = None
        self.assertEqual(actual_result, expected_result)

        # test3
        test_value = 'a'
        actual_result = self.linked_list.findNodeByValue(test_value)
        actual_result = (
            actual_result[0].value, 
            actual_result[1],
            actual_result[2],
            )
        expected_result = ('a', 0, None)
        self.assertEqual(actual_result, expected_result)
        
    def test_insert_node(self):
        """
        need_dataset\n
        특정 위치에 노드가 삽입되는지 테스트.
        """
        # test1
        target_index = 2
        new_value = '가'
        self.linked_list.insertNode(target_index, new_value)
        expected_result = ' -> '.join(['a', 'b', '가', 'c', 'd'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 5)
        
        # test2
        target_index = 0
        new_value = '나'
        self.linked_list.insertNode(target_index, new_value)
        expected_result = ' -> '.join(['나', 'a', 'b', '가', 'c', 'd'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 6)
        
    def test_delete_node_by_index(self):
        """
        need_dataset\n
        지정된 인덱스 위치의 노드를 삭제할 수 있는지 테스트.
        """
        # test1
        target_index = 2
        self.linked_list.deleteNodeByIndex(target_index)
        expected_result = ' -> '.join(['a', 'b', 'd'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 3)
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 3)

        # test2
        target_index = 0
        self.linked_list.deleteNodeByIndex(target_index)
        expected_result = ' -> '.join(['b', 'd'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 2)
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 2)

        # test3
        target_index = self.linked_list.getLength() - 1
        self.linked_list.deleteNodeByIndex(target_index)
        expected_result = ' -> '.join(['b'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 1)
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 1)

        # test4
        target_index = 5
        with self.assertRaises(IndexError):
            self.linked_list.deleteNodeByIndex(target_index)

        # test5
        ll = LinkedList()
        with self.assertRaises(IndexError):
            ll.deleteNodeByIndex(0)

        self.linked_list.clear()
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 0)

    def test_delete_node_by_value(self):
        """
        need_dataset\n
        주어진 값과 일치하는 값을 가지는 노드를 삭제하는지 테스트.
        """
        # test1
        target_value = 'c'
        self.linked_list.deleteNodeByValue(target_value)
        expected_result = ' -> '.join(['a', 'b', 'd'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 3)
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 3)

        # test2
        target_value = 'a'
        self.linked_list.deleteNodeByValue(target_value)
        expected_result = ' -> '.join(['b', 'd'])
        self.assertEqual(self.linked_list.__repr__(), expected_result)
        self.assertEqual(self.linked_list.getLength(), 2)
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 2)

        # test3
        target_value = 'a'
        with self.assertRaises(TypeError):
            self.linked_list.deleteNodeByValue(target_value)

    def test_pop_front_and_back(self):
        """
        need_dataset\n
        popFront(), popBack() 메서드 테스트.
        """
        # test1
        actual_result = self.linked_list.popFront().value
        self.assertEqual(actual_result, 'a')
        self.assertEqual(self.linked_list.getLength(), 3)

        self.linked_list.addNodeFront('a')
        actual_result = self.linked_list.popFront(False)
        self.assertEqual(actual_result, 'a')
        self.assertEqual(self.linked_list.getLength(), 3)

        # test2
        actual_result = self.linked_list.popBack().value
        self.assertEqual(actual_result, 'd')
        self.assertEqual(self.linked_list.getLength(), 2)

        self.linked_list.addNodeBack('d')
        actual_result = self.linked_list.popBack(False)
        self.assertEqual(actual_result, 'd')
        self.assertEqual(self.linked_list.getLength(), 2)

        # test3
        ll = LinkedList()
        with self.assertRaises(IndexError):
            ll.popFront()
        with self.assertRaises(IndexError):
            ll.popBack()

    def test_clear(self):
        """
        need_dataset\n
        연결 리스트를 모두 비울 수 있는지 테스트.
        """
        # test1
        self.linked_list.clear()
        self.assertEqual(self.linked_list.__repr__(), "빈 연결리스트.")
        self.assertEqual(self.linked_list.getLength(), 0)
        self.assertEqual(self.linked_list._remainingNodeNumbers(), 0)

        # test2
        ll = LinkedList()
        ll.clear()
        self.assertEqual(ll.__repr__(), "빈 연결리스트.")
        self.assertEqual(ll.getLength(), 0)
        self.assertEqual(ll._remainingNodeNumbers(), 0)

    def test_iter(self):
        """
        need_dataset\n
        __iter__() 테스트.
        """
        self.linked_list.iterMode(False)
        all_data = []
        for data in self.linked_list:
            all_data.append(data)
        self.assertEqual(all_data, ['a', 'b', 'c', 'd'])


class TestLLQueue(unittest.TestCase):
    """
    LinkedListQueue 클래스 테스트.
    """
    def setUp(self):
        self.llq = LinkedListQueue()
        self.desc = self.shortDescription()
        self.dataset = ['a', 'b', 'c', 'd']

        if self.desc == 'need_dataset':
            for data in self.dataset:
                self.llq.enqueue(data)
    
    def tearDown(self):
        self.llq.clear()

    def test_empty(self):
        """
        빈 큐_연결리스트 테스트.
        """
        # test1
        self.assertEqual(self.llq.__repr__(), '빈 연결리스트.')
        self.assertEqual(self.llq.isEmpty(), True)
        self.assertEqual(self.llq.getLength(), 0)

        # test2
        with self.assertRaises(IndexError):
            self.llq.dequeue()
        with self.assertRaises(IndexError):
            self.llq.showPeek()

    def test_enqueue_and_dequeue(self):
        """
        need_dataset\n
        enqueue, dequeue 테스트.
        """
        # test1
        result = self.llq.dequeue()
        self.assertEqual(result, 'a')
        self.assertEqual(self.llq.getLength(), 3)
        expected_result = ' -> '.join(['b', 'c', 'd'])
        self.assertEqual(self.llq.__repr__(), expected_result)

        # test2
        self.llq.enqueue('e')
        self.assertEqual(self.llq.getLength(), 4)
        expected_result = ' -> '.join(['b', 'c', 'd', 'e'])
        self.assertEqual(self.llq.__repr__(), expected_result)

    def test_peek(self):
        """
        need_dataset\n
        큐 맨 끝 항목 조회 테스트.
        """
        self.assertEqual(self.llq.showPeek(), 'a')

        # 조회 만으로는 큐에 변화가 없다.
        self.assertEqual(self.llq.getLength(), 4)

    def test_clear(self):
        """
        need_dataset\n
        큐 내 모든 항목들을 삭제하는지 테스트.
        """
        self.assertEqual(self.llq.getLength(), 4)

        self.llq.clear()
        self.assertEqual(self.llq.__repr__(), '빈 연결리스트.')
        self.assertEqual(self.llq.isEmpty(), True)
        self.assertEqual(self.llq.getLength(), 0)


class TestLLStack(unittest.TestCase):
    """
    LinkedListStack 클래스 테스트.
    """
    def setUp(self):
        self.lls = LinkedListStack()
        self.desc = self.shortDescription()
        self.dataset = ['a', 'b', 'c', 'd']

        if self.desc == 'need_dataset':
            for data in self.dataset:
                self.lls.push(data)

    def tearDown(self):
        self.lls.clear()

    def test_empty(self):
        """
        빈 스택_연결리스트 테스트.
        """
        # test1
        self.assertEqual(self.lls.__repr__(), '빈 연결리스트.')
        self.assertEqual(self.lls.isEmpty(), True)
        self.assertEqual(self.lls.getLength(), 0)

        # test2
        with self.assertRaises(IndexError):
            self.lls.pop()
        with self.assertRaises(IndexError):
            self.lls.searchPeek()

    def test_push_and_pop_and_peek(self):
        """
        need_dataset\n
        스택 내 항목 삽입 및 추출 및 검색 테스트.
        """
        # test1
        self.assertEqual(self.lls.getLength(), 4)
        expected_result = ' -> '.join(['a', 'b', 'c', 'd'])
        self.assertEqual(self.lls.__repr__(), expected_result)
        self.assertEqual(self.lls.isEmpty(), False)

        # test2
        pop_result = self.lls.pop()
        self.assertEqual(pop_result, 'd')
        expected_result = ' -> '.join(['a', 'b', 'c'])
        self.assertEqual(self.lls.__repr__(), expected_result)

        # test3
        search_result = self.lls.searchPeek()
        self.assertEqual(search_result, 'c')
        self.assertEqual(self.lls.getLength(), 3)

    def test_clear(self):
        """
        need_dataset\n
        clear() 테스트.
        """
        # test1
        stack_status = ' -> '.join(['a', 'b', 'c', 'd'])
        self.assertEqual(self.lls.__repr__(), stack_status)
        self.assertEqual(self.lls.isEmpty(), False)
        self.assertNotEqual(self.lls.getLength(), 0)

        self.lls.clear()
        self.assertEqual(self.lls.__repr__(), '빈 연결리스트.')
        self.assertEqual(self.lls.isEmpty(), True)
        self.assertEqual(self.lls.getLength(), 0)

        # test2
        lls2 = LinkedListStack()
        lls2.clear()
        self.assertEqual(lls2.__repr__(), '빈 연결리스트.')
        self.assertEqual(lls2.isEmpty(), True)
        self.assertEqual(lls2.getLength(), 0)


class TestDoublyLinkedList(unittest.TestCase):
    """
    my_linked_list.py의 DoublyLinkedList 클래스 테스트.
    """
    def setUp(self):
        self.dll = DoublyLinkedList()
        self.desc = self.shortDescription()
        self.dataset = ['a', 'b', 'c', 'd']

        if self.desc == 'need_dataset':
            for data in self.dataset:
                self.dll.addNodeBack(data)

    def tearDown(self):
        self.dll.clear()

    def testEmpty(self):
        """
        비어있는 이중 연결리스트 테스트.
        """
        self.assertEqual(self.dll.__repr__(), "빈 연결리스트.")
        self.assertEqual(self.dll.getLength(), 0)
        self.assertEqual(self.dll._remainingNodeNumbers(), 0)

    def testPrint(self):
        """
        need_dataset\n
        이중 연결리스트 출력 테스트.
        """
        expected_result = "a <-> b <-> c <-> d"
        self.assertEqual(self.dll.__repr__(), expected_result)

    def testAddNodeFront(self):
        """
        addNodeFront() 메서드 테스트.
        """
        # test1
        dll2 = DoublyLinkedList()
        dll2.addNodeFront('a')
        self.assertEqual(dll2.__repr__(), 'a')
        self.assertEqual(dll2.getLength(), 1)

        # test2
        dll2.addNodeFront('b')
        self.assertEqual(dll2.__repr__(), 'b <-> a')
        self.assertEqual(dll2.getLength(), 2)
        dll2.clear()

    def testAddNodeBack(self):
        """
        addNodeBack() 메서드 테스트.
        """
        # test1
        dll2 = DoublyLinkedList()
        dll2.addNodeBack('a')
        self.assertEqual(dll2.__repr__(), 'a')
        self.assertEqual(dll2.getLength(), 1)

        # test2
        dll2.addNodeBack('b')
        self.assertEqual(dll2.__repr__(), 'a <-> b')
        self.assertEqual(dll2.getLength(), 2)
        dll2.clear()

    def testFindNodeByIndex(self):
        """
        need_dataset\n
        findNodeByIndex() 메서드 테스트.
        """
        def get_result(index: int):
            found_result = self.dll.findNodeByIndex(index)
            cur_node = found_result[0]
            cur_node_value = cur_node.value
            prev_node = cur_node.prev_pointer
            next_node = cur_node.next_pointer
            cur_index = found_result[1]
            return (
                cur_node_value,
                prev_node,
                next_node,
                cur_index
            )
        
        nicknames = 'cur_node_value, prev_node, next_node, cur_index'
        NodeResult = namedtuple('NodeResult', nicknames)

        # test1
        result = NodeResult._make(get_result(0))
        self.assertEqual(result.cur_node_value, 'a')
        self.assertEqual(result.prev_node, None)
        self.assertEqual(result.next_node.value, 'b')
        self.assertEqual(result.cur_index, 0)
        self.assertEqual(self.dll.getLength(), 4)

        # test2
        result = NodeResult._make(get_result(3))
        self.assertEqual(result.cur_node_value, 'd')
        self.assertEqual(result.prev_node.value, 'c')
        self.assertEqual(result.next_node, None)
        self.assertEqual(result.cur_index, 3)
        self.assertEqual(self.dll.getLength(), 4)

        # test3
        result = NodeResult._make(get_result(1))
        self.assertEqual(result.cur_node_value, 'b')
        self.assertEqual(result.prev_node.value, 'a')
        self.assertEqual(result.next_node.value, 'c')
        self.assertEqual(result.cur_index, 1)
        self.assertEqual(self.dll.getLength(), 4)

    def testFindNodeByValue(self):
        """
        need_dataset\n
        findNodeByValue() 메서드 테스트.
        """
        def get_result(target_value):
            found_result = self.dll.findNodeByValue(target_value)
            cur_node = found_result[0]
            cur_node_value = cur_node.value
            prev_node = cur_node.prev_pointer
            next_node = cur_node.next_pointer
            cur_index = found_result[1]
            return (
                cur_node_value,
                prev_node,
                next_node,
                cur_index
            )
        
        nicknames = 'cur_node_value, prev_node, next_node, cur_index'
        NodeResult = namedtuple('NodeResult', nicknames)

        # test1
        result = NodeResult._make(get_result('a'))
        self.assertEqual(result.cur_node_value, 'a')
        self.assertEqual(result.prev_node, None)
        self.assertEqual(result.next_node.value, 'b')
        self.assertEqual(result.cur_index, 0)
        self.assertEqual(self.dll.getLength(), 4)

        # test2
        result = NodeResult._make(get_result('d'))
        self.assertEqual(result.cur_node_value, 'd')
        self.assertEqual(result.prev_node.value, 'c')
        self.assertEqual(result.next_node, None)
        self.assertEqual(result.cur_index, 3)
        self.assertEqual(self.dll.getLength(), 4)

        # test3
        result = NodeResult._make(get_result('b'))
        self.assertEqual(result.cur_node_value, 'b')
        self.assertEqual(result.prev_node.value, 'a')
        self.assertEqual(result.next_node.value, 'c')
        self.assertEqual(result.cur_index, 1)
        self.assertEqual(self.dll.getLength(), 4)

    def testInsertNode(self):
        """
        need_dataset\n
        insertNode() 메서드 테스트.
        기존 이중 연결 리스트에 새 노드를 잘 삽입할 수 있는지 테스트.
        """
        # test1
        self.dll.insertNode(1, 'e')
        expected_result = "a <-> e <-> b <-> c <-> d"
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 5)

        # test2
        self.dll.insertNode(0, '0')
        expected_result = "0 <-> a <-> e <-> b <-> c <-> d"
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 6)

        # test3
        self.dll.insertNode(self.dll.getLength()-1, 'f')
        expected_result = "0 <-> a <-> e <-> b <-> c <-> f <-> d"
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 7)

    def testDeleteNodeByIndex(self):
        """
        need_dataset\n
        deleteNodeByIndex() 메서트 테스트.
        """
        # test1
        target_index = 0
        self.dll.deleteNodeByIndex(target_index)
        expected_result = 'b <-> c <-> d'
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 3)
        self.assertEqual(self.dll._remainingNodeNumbers(), 3)

        # test2
        target_index = 1
        self.dll.deleteNodeByIndex(target_index)
        expected_result = 'b <-> d'
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 2)
        self.assertEqual(self.dll._remainingNodeNumbers(), 2)

        # test3
        target_index = 1
        self.dll.deleteNodeByIndex(target_index)
        expected_result = 'b'
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 1)
        self.assertEqual(self.dll._remainingNodeNumbers(), 1)

        # test4
        with self.assertRaises(IndexError):
            self.dll.deleteNodeByIndex(1)

        # test5
        with self.assertRaises(IndexError):
            self.dll.deleteNodeByIndex(-1)

    def testDeleteNodeByValue(self):
        """
        need_dataset\n
        deleteNodeByValue() 메서드 테스트.
        """
        # test1
        target_value = 'a'
        self.dll.deleteNodeByValue(target_value)
        expected_result = 'b <-> c <-> d'
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 3)
        self.assertEqual(self.dll._remainingNodeNumbers(), 3)

        # test2
        target_value = 'c'
        self.dll.deleteNodeByValue(target_value)
        expected_result = 'b <-> d'
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 2)
        self.assertEqual(self.dll._remainingNodeNumbers(), 2)

        # test3
        target_value = 'd'
        self.dll.deleteNodeByValue(target_value)
        expected_result = 'b'
        self.assertEqual(self.dll.__repr__(), expected_result)
        self.assertEqual(self.dll.getLength(), 1)
        self.assertEqual(self.dll._remainingNodeNumbers(), 1)

        # test4
        with self.assertRaises(TypeError):
            self.dll.deleteNodeByValue('아')

    def testPopFrontAndBack(self):
        """
        need_dataset\n
        popFront(), popBack() 메서드 테스트. 
        LinkedList로부터 상속받은 DoublyLinkedList 클래스에서도 
        해당 메서드들이 잘 작동하는지 보기 위함. 
        """
        # test1
        actual_result = self.dll.popFront().value
        self.assertEqual(actual_result, 'a')
        self.assertEqual(self.dll.__repr__(), 'b <-> c <-> d')
        self.assertEqual(self.dll.getLength(), 3)

        # test2
        actual_result = self.dll.popBack().value
        self.assertEqual(actual_result, 'd')
        self.assertEqual(self.dll.__repr__(), 'b <-> c')
        self.assertEqual(self.dll.getLength(), 2)

        # test3
        dll2 = DoublyLinkedList()
        with self.assertRaises(IndexError):
            dll2.popFront()
        with self.assertRaises(IndexError):
            dll2.popBack()

        dll2.clear()

    def testClear(self):
        """
        need_dataset\n
        clear() 메서드 테스트. 
        LinkedList로부터 상속받은 DoublyLinkedList 클래스에서도 
        해당 메서드가 잘 작동하는지 보기 위함. 
        """
        # test1
        self.assertNotEqual(self.dll.getLength(), 0)
        self.dll.clear()
        self.assertEqual(self.dll.__repr__(), "빈 연결리스트.")
        self.assertEqual(self.dll.getLength(), 0)

        # test2
        self.dll.clear()
        self.assertEqual(self.dll.__repr__(), "빈 연결리스트.")
        self.assertEqual(self.dll.getLength(), 0)

    def testIter(self):
        """
        need_dataset\n
        __iter__() 메서드 테스트. 
        """
        self.dll.iterMode(False)
        all_data = []
        for data in self.dll:
            all_data.append(data)
        self.assertEqual(all_data, ['a', 'b', 'c', 'd'])


class TestCircleLL(unittest.TestCase):
    """
    원형 연결 리스트를 구현한 CircularLinkedList 클래스 테스트.
    """
    def setUp(self):
        self.cll = CircularLinkedList()
        self.desc = self.shortDescription()
        self.dataset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        if self.desc == 'need_dataset':
            for data in self.dataset:
                self.cll.addNodeBack(data)

    def tearDown(self):
        self.cll.clear()

    def testClear(self):
        """
        need_dataset\n
        clear() 메서드 테스트. 
        """
        self.assertEqual(self.cll.getLength(), 10)
        self.assertEqual(self.cll._remainingNodeNumbers(), 10)
        self.cll.clear()
        self.assertEqual(self.cll.__repr__(), "빈 연결리스트.")
        self.assertEqual(self.cll.getLength(), 0)
        self.assertEqual(self.cll._remainingNodeNumbers(), 0)

    def testInputData(self):
        """
        need_dataset\n
        원형 연결 리스트에 데이터들이 잘 삽입되는지 테스트.
        """
        ex_re = 'a <-> b <-> c <-> d <-> e <-> f <-> g <-> h <-> i <-> j'
        self.assertEqual(self.cll.__repr__(), ex_re)
        self.assertEqual(self.cll.getLength(), 10)

    def testFindNodeByOverIndex(self):
        """
        need_dataset\n
        findNodeByIndex() 메서드 테스트.
        인덱스가 전체 연결 리스트의 크기를 벗어나는 수를 가져도 
        제대로 작동되는지 테스트.
        """
        # test1
        index = 13
        actual_result = self.cll.findNodeByIndex(index)[0].value
        self.assertEqual(actual_result, 'd')

        # test2
        index = -2
        actual_result = self.cll.findNodeByIndex(index)[0].value
        self.assertEqual(actual_result, 'h')

        # test3
        index = -12
        actual_result = self.cll.findNodeByIndex(index)[0].value
        self.assertEqual(actual_result, 'h')

        # test4
        index = 86
        actual_result = self.cll.findNodeByIndex(index)
        self.assertEqual(actual_result[0].value, 'g')
        self.assertEqual(actual_result[1], 6)

    def testIter(self):
        """
        need_dataset\n
        __iter__() 메서드 테스트.
        """
        self.cll.iterMode(False)
        all_data = []
        for data in self.cll:
            all_data.append(data)
        self.assertEqual(
            all_data, 
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        )


def test_only_some_methods() -> (None):
    """
    테스트 도중 프로그램이 멈추는 현상이 발생. 
    my_linked_list.py 모듈의 while True에 의한 무한 루프 때문으로 확인. 
    정확히 어떤 부분에서 그러한 문제가 발생하는지 확인하기 위해 
    여러 테스트들을 분리하여 실행하기 위한 용도. 
    현재는 해당 문제가 해결됨. 
    """
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(TestLinkedList))
    #suite.addTest(unittest.makeSuite(TestLLQueue))
    #suite.addTest(unittest.makeSuite(TestLLStack))
    suite.addTest(unittest.makeSuite(TestDoublyLinkedList))
    #suite.addTest(unittest.makeSuite(TestCircleLL))
    #suite.addTest(TestCircleLL("testInputData"))
    #suite.addTest(TestCircleLL("testFindNodeByOverIndex"))

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    unittest.main()
    #test_only_some_methods()
    pass
