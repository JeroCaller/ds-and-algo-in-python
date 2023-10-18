# For type alias.
Node_ = object
DPNode_ = object
Value = object

class Node():
    node_counter = 0

    def __init__(
            self, 
            value: Value = None, 
            pointer: Node_ = None, 
        ):
        """
        하나의 노드를 구현하는 클래스. 
        매개변수
        -------
        value: 노드의 값
        pointer: 현재 노드의 다음 노드를 가리키는 포인터.
        포인터에는 다음 노드의 메모리 주소값을 저장하므로
        해당 매개변수는 다음 Node 객체를 대입받아야 한다.  
        """
        self.value: Value = value
        self.pointer: Node | None = pointer
        Node.node_counter += 1
    
    def __del__(self):
        Node.node_counter -= 1


class DPNode():
    """
    Double pointer node. 
    각각 다음 노드와 이전 노드를 가리키는 포인터 두 개를 가지는 노드 객체. 
    """
    dpnode_counter = 0

    def __init__(
            self, 
            value=None, 
            next_pointer: DPNode_ = None,
            prev_pointer: DPNode_ = None
        ):
        self.value = value
        self.next_pointer: DPNode | None = next_pointer
        self.prev_pointer: DPNode | None = prev_pointer
        DPNode.dpnode_counter += 1

    def __del__(self):
        DPNode.dpnode_counter -= 1


class LinkedList():
    def __init__(self):
        """
        self.head_pointer: 맨 앞 노드를 가리키는 포인터. Node 객체를 받는다.\n
        self.tail_pointer: 맨 뒤 노드를 가리키는 포인터. Node 객체를 받는다.\n
        self.length: 연결 리스트 내 총 노드의 개수.
        """
        self.head_pointer: Node | None = None
        self.tail_pointer: Node | None = None
        self.length = 0
        self.link_char = ' -> '
        self._iter_mode = True

    def __iter__(self):
        node = self.head_pointer
        while node:
            if self._iter_mode: yield node
            else: yield node.value
            node = node.pointer

    def iterMode(self, node_mode: bool = True) -> (None):
        """
        연결리스트를 __iter__()를 통해 반복할 때 노드 자체를 반환 시킬 것인지, 
        노드의 값만을 반환 시킬지 결정하는 메서드. 
        
        매개변수
        -------
        node_mode: True -> Node 객체를 반환. False -> Node 객체의 value만을 반환. 
        """
        self._iter_mode = node_mode

    def whatKindOfLL(self) -> (str):
        """
        현재 해당 연결 리스트의 종류를 반환.
        """
        return '단일 연결 리스트'

    def getLength(self) -> (int):
        """
        현재 연결 리스트 내 총 노드 수 반환.
        """
        return self.length

    def __repr__(self):
        """
        현재 연결 리스트를 출력.
        연결 리스트가 비어있으면 빈 문자열 출력.
        """
        linked_list = []
        current_node: Node | None = self.head_pointer
        while current_node is not None:
            value_ = current_node.value
            if type(value_) != str:
                value_ = str(value_)
            linked_list.append(value_)
            current_node = current_node.pointer
        if linked_list:
            return self.link_char.join(linked_list)
        else:
            return "빈 연결리스트."
        
    def addNodeFront(self, new_value: Value) -> (None):
        """
        연결 리스트의 맨 앞에 새 노드를 삽입.
        """
        self._addNodeFront(Node(new_value))

    def _addNodeFront(self, new_node: Node) -> (None):
        if self.head_pointer is None:
            # 연결 리스트에 아무런 노드도 없는 경우.
            self.head_pointer = new_node
            self.tail_pointer = new_node
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            new_node.pointer = self.head_pointer
            self.head_pointer = new_node
        self.length += 1

    def addNodeBack(self, new_value: Value) -> (None):
        """
        연결 리스트의 맨 뒤에 새 노드 삽입.
        """
        self._addNodeBack(Node(new_value))

    def _addNodeBack(self, new_node: Node) -> (None):
        if self.tail_pointer is None:
            # 연결 리스트에 아무 노드도 없는 경우.
            self.tail_pointer = new_node
            self.head_pointer = new_node
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            self.tail_pointer.pointer = new_node
            self.tail_pointer = new_node
        self.length += 1

    def findNodeByIndex(self, index: int) -> (tuple[Node, int, Node | None]):
        """
        인덱스로 찾고자 하는 노드 반환. 
        인덱스의 시작 번호는 0이다. 
        현재 연결 리스트의 노드 개수보다 더 큰 인덱스 값 대입 시,
        또는 인덱스에 음수 입력 시
        IndexError 예외 발생.
        """
        if self.length < index + 1 or index < 0:
            raise IndexError("연결 리스트의 길이에서 벗어나는 인덱스를 입력하였습니다.")
        cur_i = 0
        target_node = self.head_pointer
        prev_pointer = self.head_pointer
        while cur_i != index:
            prev_pointer = target_node
            target_node = target_node.pointer
            cur_i += 1
        if index == 0:
            prev_pointer = None
        return (target_node, index, prev_pointer)
    
    def findNodeByValue(self, target_value: Value) -> (tuple[Node, int, Node | None] | None):
        """
        찾고자 하는 값이 특정 노드의 값과 같은 경우 그 노드와 그 노드의 인덱스 반환.
        찾고자 하는 노드가 없다면 None을 반환.
        """
        current_node = self.head_pointer
        
        # 현재 선택된 노드의 이전 노드를 가리키는 포인터
        prev_pointer = self.head_pointer

        target_node = None
        target_index = 0
        while True:
            if current_node is None:
                break
            if current_node.value == target_value:
                target_node = current_node
                if target_index == 0:
                    prev_pointer = None
                break
            prev_pointer = current_node
            current_node = current_node.pointer
            target_index += 1
        if target_node is None:
            return None
        else:
            return (target_node, target_index, prev_pointer)
        
    def getValueByIndex(self, index: int) -> (Value):
        """
        찾고자 하는 값을 인덱스를 통해 찾음. 
        findNodeByIndex() 메서드를 사용함. 
        """
        target_node = self.findNodeByIndex(index)[0]
        return target_node.value
        
    def insertNode(self, index: int, new_value: Value) -> (None):
        """
        연결 리스트에서 지정된 인덱스 위치에 새 노드 삽입.
        """
        self._insertNode(index, Node(new_value))
        
    def _insertNode(self, index: int, new_node: Node) -> (None):
        old_node, old_index, prev_pointer = self.findNodeByIndex(index)
        new_node.pointer = old_node
        if prev_pointer is None:
            # 삽입하고자 하는 인덱스 위치가 0임.
            self.head_pointer = new_node
        else:
            prev_pointer.pointer = new_node
        self.length += 1

    def _deleteNode(self, target_node: Node, prev_pointer: Node | None) -> (None):
        if prev_pointer is None:
            # 삭제하고자 하는 노드의 인덱스 위치가 0임.
            self.head_pointer = target_node.pointer
        elif target_node.pointer is None:
            # 삭제하고자 하는 요소가 연결 리스트의 맨 뒤에 존재하는 경우.
            self.tail_pointer = prev_pointer
            prev_pointer.pointer = None
        else:
            prev_pointer.pointer = target_node.pointer
        target_node.pointer = None
        del target_node
        self.length -= 1
        
    def deleteNodeByIndex(self, index: int) -> (None):
        """
        인덱스에 해당하는 노드 삭제.
        """
        target_node, target_index, prev_pointer = self.findNodeByIndex(index)
        self._deleteNode(target_node, prev_pointer)

    def deleteNodeByValue(self, target_value: Value) -> (None):
        """
        삭제하고자 하는 값과 일치하는 노드를 삭제.
        """
        try:
            search_result = self.findNodeByValue(target_value)
        except TypeError:
            print("TypeError: 찾고자 하는 값이 없습니다.")
        else:
            target_node, target_index, prev_pointer = search_result
        self._deleteNode(target_node, prev_pointer)

    def popFront(self, node_mode: bool = True) -> (Node | Value):
        """
        연결 리스트의 맨 앞에 있는 노드를 추출 후 제거. 
        빈 연결 리스트에서 pop 시도 시, IndexError 예외 발생. 
        매개변수
        -------
        node_mode: True -> Node 객체를 반환. False -> Node 객체의 value 반환.
        """
        node_to_pop = self.findNodeByIndex(0)[0]
        self.deleteNodeByIndex(0)
        if node_mode: return node_to_pop
        else: return node_to_pop.value
    
    def popBack(self, node_mode: bool = True) -> (Node | Value):
        """
        연결 리스트의 맨 뒤에 있는 노드 추출 후 제거. 
        빈 연결 리스트에서 pop 시도 시, IndexError 예외 발생. 
        매개변수
        -------
        node_mode: True -> Node 객체를 반환. False -> Node 객체의 value 반환.
        """
        last_index = self.getLength() - 1
        node_to_pop = self.findNodeByIndex(last_index)[0]
        self.deleteNodeByIndex(last_index)
        if node_mode: return node_to_pop
        else: return node_to_pop.value
    
    def clear(self) -> (None):
        """
        연결 리스트를 모두 비운다. 
        즉, 연결 리스트 내 모든 노드들을 삭제한다.
        """
        node = self.head_pointer
        while node:
            next_node = node.pointer
            node.pointer = None
            del node
            node = next_node

        self.head_pointer: Node | None = None
        self.tail_pointer: Node | None = None
        self.length = 0

    def remainingNodeNumbers(self) -> (int):
        """
        메모리 할당 해제 테스트용. 
        특정 노드 삭제 또는 clear() 메서드 호출로 인해 Node 객체가 삭제되는 지 
        테스트 용. 
        해당 연결리스트 내 노드의 개수 반환. 
        둘 이상의 연결 리스트 사용 시 하나의 연결 리스트 내 
        Node 객체의 수를 정확히 판별하지 못할 수 있으므로 
        단 하나의 연결리스트만 생성하고 테스트하기를 권장.
        """
        return Node.node_counter


class LinkedListQueue():
    """
    연결 리스트를 큐처럼 FIFO 구조로 사용함.
    """
    def __init__(self):
        self.ll = LinkedList()

    def __repr__(self):
        return repr(self.ll)
    
    def whatKindOfLL(self) -> (str):
        """
        현재 해당 연결 리스트의 종류를 반환.
        """
        return '큐 형태의 단일 연결 리스트'

    def isEmpty(self) -> (bool):
        if self.ll.getLength() == 0:
            return True
        else:
            return False
        
    def getLength(self) -> (int):
        return self.ll.getLength()
    
    def enqueue(self, new_value: Value) -> (None):
        self.ll.addNodeBack(new_value)

    def dequeue(self, only_value: bool = True) -> (Node | Value):
        """
        only_value)\n
        True: 값만 반환.
        False: 노드 자체를 반환.
        """
        result = self.ll.popFront()
        if only_value:
            return result.value
        else:
            return result
        
    def showPeek(self) -> (Value):
        """
        큐에서 맨 처음으로 나올 값을 조회함.
        """
        return self.ll.findNodeByIndex(0)[0].value
    
    def clear(self):
        """
        큐를 비운다.
        """
        self.ll.clear()
    

class LinkedListStack():
    """
    연결리스트를 LIFO 구조의 stack처럼 사용한다.
    """
    def __init__(self) -> (None):
        self.lls = LinkedList()

    def __repr__(self):
        return repr(self.lls)
    
    def whatKindOfLL(self) -> (str):
        """
        현재 해당 연결 리스트의 종류를 반환.
        """
        return '스택 형태의 단일 연결 리스트'
    
    def isEmpty(self) -> (bool):
        return True if self.lls.getLength() == 0 else False
    
    def getLength(self) -> (int):
        return self.lls.getLength()
    
    def push(self, new_value: Value) -> (None):
        self.lls.addNodeBack(new_value)

    def pop(self, only_value: bool = True) -> (Value | Node):
        """
        스택 맨 끝 항목을 반환하고 스택에서 제거.
        only_value)\n
        True: 값만 반환. 
        False: 노드 자체를 반환.
        """
        result = self.lls.popBack()
        if only_value:
            return result.value
        else:
            return result
        
    def searchPeek(self) -> (Value):
        """
        스택 맨 끝 항목 조회.
        """
        return self.lls.findNodeByIndex(self.getLength()-1)[0].value
    
    def clear(self):
        """
        스택 내 모든 항목 제거.
        """
        self.lls.clear()


class DoublyLinkedList(LinkedList):
    """
    이중 연결 리스트.
    """
    def __init__(self):
        super().__init__()
        self.head_pointer: DPNode | None = None
        self.tail_pointer: DPNode | None = None
        self.link_char = ' <-> '

    def __iter__(self):
        node = self.head_pointer
        while node:
            if self._iter_mode: yield node
            else: yield node.value
            node = node.next_pointer

    def __repr__(self):
        linked_list = []
        current_node: DPNode | None = self.head_pointer
        while current_node is not None:
            value_ = current_node.value
            if type(value_) != str: value_ = str(value_)
            linked_list.append(value_)
            current_node = current_node.next_pointer
        if linked_list:
            return self.link_char.join(linked_list)
        else:
            return "빈 연결리스트."
        
    def addNodeFront(self, new_value: DPNode) -> (None):
        self._addNodeFront(DPNode(new_value))

    def _addNodeFront(self, new_node: DPNode) -> (None):
        if self.head_pointer is None:
            # 연결 리스트에 아무런 노드도 없는 경우.
            self.head_pointer = new_node
            self.tail_pointer = new_node
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            new_node.next_pointer = self.head_pointer
            self.head_pointer.prev_pointer = new_node
            self.head_pointer = new_node
        self.length += 1

    def addNodeBack(self, new_value: Value) -> (None):
        self._addNodeBack(DPNode(new_value))

    def _addNodeBack(self, new_node: DPNode) -> (None):
        if self.tail_pointer is None:
            # 연결 리스트에 아무 노드도 없는 경우.
            self.tail_pointer = new_node
            self.head_pointer = new_node
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            self.tail_pointer.next_pointer = new_node
            new_node.prev_pointer = self.tail_pointer
            self.tail_pointer = new_node
        self.length += 1

    def findNodeByIndex(self, index: int) -> (tuple[DPNode, int]):
        if self.length < index + 1 or index < 0:
            raise IndexError("연결 리스트의 길이에서 벗어나는 인덱스를 입력하였습니다.")
        cur_i = 0
        target_node = self.head_pointer
        while cur_i != index:
            target_node = target_node.next_pointer
            cur_i += 1
        return (target_node, index)
    
    def findNodeByValue(self, target_value: Value) -> (tuple[DPNode, int] | None):
        current_node = self.head_pointer
        target_node = None
        target_index = 0
        while True:
            if current_node is None:
                break
            if current_node.value == target_value:
                target_node = current_node
                break
            current_node = current_node.next_pointer
            target_index += 1
        if target_node is None:
            return
        else:
            return (target_node, target_index)
        
    def insertNode(self, index: int, new_value: Value) -> (None):
        self._insertNode(index, DPNode(new_value))
        
    def _insertNode(self, index: int, new_node: DPNode) -> (None):
        old_node = self.findNodeByIndex(index)[0]
        new_node.next_pointer = old_node
        if old_node.prev_pointer is None:
            # 삽입하고자 하는 인덱스 위치가 0임.
            self.head_pointer = new_node
            old_node.prev_pointer = new_node
        else:
            new_node.prev_pointer = old_node.prev_pointer
            old_node.prev_pointer.next_pointer = new_node
            old_node.prev_pointer = new_node
        self.length += 1

    def __deleteNode(self, target_node: DPNode):
        if target_node.prev_pointer is None:
            # 삭제하고자 하는 인덱스 위치가 0임.
            self.head_pointer = target_node.next_pointer
            self.head_pointer.prev_pointer = None
        elif target_node.next_pointer is None:
            # 삭제하고자 하는 요소가 맨 마지막에 위치한 경우.
            self.tail_pointer = target_node.prev_pointer
            target_node.prev_pointer.next_pointer = None
            target_node.prev_pointer = None
        else:
            target_node.prev_pointer.next_pointer = target_node.next_pointer
            target_node.next_pointer.prev_pointer = target_node.prev_pointer
            target_node.prev_pointer = None
        target_node.next_pointer = None
        del target_node
        self.length -= 1

    def deleteNodeByIndex(self, index: int) -> (None):
        target_node = self.findNodeByIndex(index)[0]
        self.__deleteNode(target_node)

    def deleteNodeByValue(self, target_value: Value) -> (None):
        try:
            search_result = self.findNodeByValue(target_value)
        except TypeError:
            raise TypeError("TypeError: 찾고자 하는 값이 없습니다.")
        else:
            target_node = search_result[0]
        self.__deleteNode(target_node)

    def clear(self) -> (None):
        node = self.head_pointer
        while node:
            next_node = node.next_pointer
            node.next_pointer = None
            node.prev_pointer = None
            del node
            node = next_node

        self.head_pointer: DPNode | None = None
        self.tail_pointer: DPNode | None = None
        self.length = 0

    # 반환 타입 Node -> DPNode로 고침.
    def popFront(self) -> (DPNode | None): return super().popFront()
    def popBack(self) -> (DPNode | None): return super().popBack()
    def whatKindOfLL(self) -> (str): return "이중 연결 리스트"
    def remainingNodeNumbers(self) -> (int): return DPNode.dpnode_counter


class CircularLinkedList(DoublyLinkedList):
    """
    원형 연결 리스트 구현. 이중 연결리스트를 이용하여 구현함.
    """
    def __init__(self): super().__init__()
    def whatKindOfLL(self) -> (str): return "원형 연결 리스트"

    def __iter__(self):
        node = self.head_pointer
        while True:
            if self._iter_mode: yield node
            else: yield node.value
            if node == self.tail_pointer: break
            node = node.next_pointer

    def __repr__(self):
        empty_msg = "빈 연결리스트."
        if self.head_pointer is None: return empty_msg

        linked_list = []
        current_node = self.head_pointer
        while True:
            value_ = current_node.value
            if type(value_) != str: value_ = str(value_)
            linked_list.append(value_)
            if current_node == self.tail_pointer: break
            current_node = current_node.next_pointer
        
        if linked_list:
            return self.link_char.join(linked_list)
        else:
            return empty_msg

    def addNodeFront(self, new_value: Value) -> (None):
        super().addNodeFront(new_value)
        #self.tail_pointer.next_pointer = self.head_pointer.prev_pointer
        if self.length > 1:
            self.tail_pointer.next_pointer = self.head_pointer
            self.head_pointer.prev_pointer = self.tail_pointer

    def addNodeBack(self, new_value: Value) -> (None):
        super().addNodeBack(new_value)
        #self.tail_pointer.next_pointer = self.head_pointer.prev_pointer
        if self.length > 1:
            self.tail_pointer.next_pointer = self.head_pointer
            self.head_pointer.prev_pointer = self.tail_pointer

    def __handleOverIndex(self, index: int) -> (int):
        """
        인덱스가 연결 리스트의 크기를 초과하는 경우, 
        이를 적절한 인덱스로 변환한다.\n
        ex1) ll_size = 10, index = 13\n
        -> index = index % ll_size\n
        = 13 % 10 = 3\n
        ex2) ll_size = 10, index = -12\n
        -> index = - (abs(index) % ll_size) = - (12 % 10) = -2\n
        -> index = (ll_size-1) + (-2) = 7\n
        """
        ll_size = self.getLength()
        if index < 0:
            if ll_size < abs(index):
                # ex) ll_size = 10, index = -12
                # -> index = - (abs(index) % ll_size) = -12 % 10 = -2
                index = - (abs(index) % ll_size)
            # ex) ll_size = 10, index = -2 -> index = (ll_size-1) + (-2) = 7
            index = (ll_size-1) + index
        elif index > ll_size - 1:
            # ex) ll_size = 10, index = 13 -> index = index % ll_size
            # = 13 % 10 = 3
            index = index % ll_size
        return index

    def findNodeByIndex(self, index: int) -> (tuple[DPNode, int]):
        """
        인덱스로 찾고자 하는 노드 반환. 
        인덱스의 시작 번호는 0이다. 
        현재 연결 리스트의 노드 개수보다 더 큰 인덱스 값 대입 시,
        또는 인덱스에 음수 입력 시
        순환시킨 인덱스를 사용한다. 
        따라서, 전체 크기에 벗어난 인덱스를 사용해도 에러가 일어나지 않도록 하였다. \n
        ex1) ll_size = 10, index = 13\n
        -> index = index % ll_size\n
        = 13 % 10 = 3\n
        ex2) ll_size = 10, index = -12\n
        -> index = - (abs(index) % ll_size) = - (12 % 10) = -2\n
        -> index = (ll_size-1) + (-2) = 7\n
        """
        index = self.__handleOverIndex(index)
        return super().findNodeByIndex(index)
    
    def insertNode(self, index: int, new_value: Value) -> (None):
        index = self.__handleOverIndex(index)
        super().insertNode(index, new_value)

    def deleteNodeByIndex(self, index: int) -> (None):
        index = self.__handleOverIndex(index)
        super().deleteNodeByIndex(index)

    def clear(self) -> (None):
        node = self.head_pointer
        while True:
            if node == self.tail_pointer:
                del node
                break
            next_node = node.next_pointer
            node.next_pointer = None
            node.prev_pointer = None
            del node
            node = next_node

        self.head_pointer: DPNode | None = None
        self.tail_pointer: DPNode | None = None
        self.length = 0


def test_ll():
    ll = LinkedList()
    test_data = [
        ('hi'), ('hello'), ('wow')
    ]
    for data in test_data:
        ll.addNodeBack(data)
    print(f"The current number of nodes: {Node.node_counter}")

    ll.clear()
    print(f"The current number of nodes: {Node.node_counter}")

def test_dll():
    dll = DoublyLinkedList()
    test_data = [
        ('hi'), ('hello'), ('wow')
    ]
    for data in test_data:
        dll.addNodeBack(data)
    print(f"The current number of nodes: {DPNode.dpnode_counter}")

    dll.clear()
    print(f"The current number of nodes: {DPNode.dpnode_counter}")

def test_cll():
    cll = CircularLinkedList()
    test_data = [
        ('hi'), ('hello'), ('wow')
    ]
    for data in test_data:
        cll.addNodeBack(data)
    print(f"The current number of nodes: {DPNode.dpnode_counter}")
    print(cll)

    cll.clear()
    print(f"The current number of nodes: {DPNode.dpnode_counter}")
    #print(cll)

if __name__ == '__main__':
    #test_ll()
    #test_dll()
    test_cll()
    pass