"""연결리스트(linked list) 자료구조 구현 모듈. 
단일 연결리스트, 단일 연결리스트를 이용한 큐와 스택 자료구조, 
이중 연결리스트, 원형 연결리스트를 구현함. 

"""

__all__ = [
    'LinkedList',
    'LinkedListQueue',
    'LinkedListStack',
    'DoublyLinkedList',
    'CircularLinkedList',
    'Node',
    'DPNode'
]

# For type alias.
Node_ = object
DPNode_ = object
Value = object

class Node():
    """하나의 노드를 구현하는 클래스."""
    node_counter = 0

    def __init__(
            self,
            value: Value = None,
            pointer: Node_ = None,
        ):
        """
        Parameters
        ----------
        value : Any | None, default None
            노드의 값
        pointer : Node | None, default None
            현재 노드의 다음 노드를 가리키는 포인터.
            포인터에는 다음 노드의 메모리 주소값을 저장하므로
            해당 매개변수는 다음 Node 객체를 대입받아야 한다.  
        
        """
        self.value: Value = value
        self.pointer: Node | None = pointer
        Node.node_counter += 1

    def __del__(self):
        Node.node_counter -= 1


class DPNode():
    """Double pointer node.
    각각 다음 노드와 이전 노드를 가리키는 포인터 두 개를 가지는 노드 객체. 
    """
    dpnode_counter = 0

    def __init__(
            self,
            value: Value = None,
            next_pointer: DPNode_ = None,
            prev_pointer: DPNode_ = None
        ):
        """
        Parameters
        ----------
        value : Any | None, default None
            노드의 값. 
        next_pointer : DPNode | None, default None
            현재 노드가 가리킬 다음 노드 DPNode 객체.
        prev_pointer : DPNode | None, default None
            현재 노드가 가리킬 이전 노드 DPNode 객체.
        
        """
        self.value = value
        self.next_pointer: DPNode | None = next_pointer
        self.prev_pointer: DPNode | None = prev_pointer
        DPNode.dpnode_counter += 1

    def __del__(self):
        DPNode.dpnode_counter -= 1


class LinkedList():
    """단일 연결리스트 클래스."""

    def __init__(self):
        """
        Attributes
        ----------
        self._head_pointer : Node | None, default None
            맨 앞 노드를 가리키는 포인터. Node 객체를 받는다.
        self._tail_pointer : Node | None, default None
            맨 뒤 노드를 가리키는 포인터. Node 객체를 받는다.
        self._length : int, default 0 
            연결 리스트 내 총 노드의 개수.
        self.link_char : str, default ' -> '
            해당 객체 출력 시 노드 간 연결 관계를 표현할 기호.
        self._iter_mode : bool, default True
            연결리스트를 반복할 때 노드 객체를 반환시킬 것인지, 노드의 
            값만을 반환시킬지를 결정하는 변수. 
        
        """
        self._head_pointer: Node | None = None
        self._tail_pointer: Node | None = None
        self._length = 0
        self.link_char = ' -> '
        self._iter_mode = True

    def __iter__(self):
        node = self._head_pointer
        while node:
            if self._iter_mode:
                yield node
            else:
                yield node.value
            node = node.pointer

    def iterMode(self, node_mode: bool = True) -> (None):
        """연결리스트를 __iter__()를 통해 반복할 때 노드 자체를 반환 시킬 것인지, 
        노드의 값만을 반환 시킬지 결정하는 메서드. 

        Parameters
        ----------
        node_mode : bool, default True
            True -> Node 객체를 반환하는 모드로 설정.
            False -> Node 객체의 value만을 반환하는 모드로 설정.
        
        """
        self._iter_mode = node_mode

    def whatKindOfLL(self) -> (str):
        """현재 해당 연결 리스트의 종류를 반환."""
        return '단일 연결 리스트'

    def getLength(self) -> (int):
        """현재 연결 리스트 내 총 노드 수 반환."""
        return self._length

    def __repr__(self):
        """현재 연결 리스트를 출력.
        연결 리스트가 비어있으면 빈 문자열 출력.
        """
        linked_list = []
        currentNode: Node | None = self._head_pointer
        while currentNode is not None:
            value_ = currentNode.value
            if not isinstance(value_, str):
                value_ = str(value_)
            linked_list.append(value_)
            currentNode = currentNode.pointer
        if linked_list:
            return self.link_char.join(linked_list)
        return "빈 연결리스트."

    def addNodeFront(self, new_value: Value) -> (None):
        """연결리스트의 맨 앞에 새 노드를 삽입. 

        Parameters
        ----------
        new_value : Value
            새 노드에 삽입할 새 value
        
        See Also
        --------
        addNodeBack : 새 노드를 연결리스트의 맨 뒤에 삽입하는 메서드.
        insertNode : 원하는 인덱스 위치에 새 노드를 삽입하는 메서드. 

        """
        self._addNodeFront(Node(new_value))

    def _addNodeFront(self, newNode: Node) -> (None):
        if self._head_pointer is None:
            # 연결 리스트에 아무런 노드도 없는 경우.
            self._head_pointer = newNode
            self._tail_pointer = newNode
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            newNode.pointer = self._head_pointer
            self._head_pointer = newNode
        self._length += 1

    def addNodeBack(self, new_value: Value) -> (None):
        """연결리스트의 맨 뒤에 새 노드 삽입.

        Parameters
        ----------
        new_value : Value
            새 노드에 삽입할 새로운 value

        See Also
        --------
        addNodeFront : 새 노드를 연결리스트의 맨 앞에 삽입하는 메서드. 
        insertNode : 원하는 인덱스 위치에 새 노드를 삽입하는 메서드.

        """
        self._addNodeBack(Node(new_value))

    def _addNodeBack(self, newNode: Node) -> (None):
        if self._tail_pointer is None:
            # 연결 리스트에 아무 노드도 없는 경우.
            self._tail_pointer = newNode
            self._head_pointer = newNode
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            self._tail_pointer.pointer = newNode
            self._tail_pointer = newNode
        self._length += 1

    def findNodeByIndex(self, index: int) -> (tuple[Node, int, Node | None]):
        """인덱스로 찾고자 하는 노드 반환. 

        Parameters
        ----------
        index : int
            인덱스의 시작 번호는 0이다. 

        Returns
        -------
        tuple[targetNode, index, prev_pointer | None]
            targetNode : Node
                인덱스에 해당하는 Node 객체.
            index : int
                해당 인덱스.
            prev_pointer : Node | None 
                targetNode의 이전 Node 객체. 없으면 None 반환. 

        Raises
        ------
        IndexError
            현재 연결 리스트의 노드 개수보다 더 큰 인덱스 값 대입 시,
            또는 인덱스에 음수 입력 시 해당 예외 발생.

        See Also
        --------
        findNodeByValue : 찾고자 하는 노드 객체를 value를 입력하여 찾는 메서드. 
        getValueByIndex : 찾고자 하는 노드의 value를 노드 객체의 인덱스를 입력하여 찾는 메서드. 
        
        """
        if self._length < index + 1 or index < 0:
            raise IndexError("연결 리스트의 길이에서 벗어나는 인덱스를 입력하였습니다.")
        cur_i = 0
        targetNode = self._head_pointer
        prev_pointer = self._head_pointer
        while cur_i != index:
            prev_pointer = targetNode
            targetNode = targetNode.pointer
            cur_i += 1
        if index == 0:
            prev_pointer = None
        return (targetNode, index, prev_pointer)

    def findNodeByValue(
            self,
            target_value: Value
        ) -> (tuple[Node, int, Node | None] | None):
        """찾고자 하는 값을 입력하면 해당 값을 보유한 노드 반환.

        Parameters
        ----------
        target_value : Value
            찾고자 하는 value

        Returns
        -------
        tuple[targetNode, target_index, prev_pointer]
            targetNode : Node
                찾고자 하는 value를 가진 Node 객체.
            target_index : int
                찾고자 하는 value를 가진 Node 객체의 인덱스. 
            prev_pointer : Node
                찾고자 하는 value를 가진 targetNode의 이전 Node 객체.
        None
            찾고자 하는 노드가 없을 때 반환됨. 

        See Also
        --------
        findNodeByIndex : 찾고자 하는 노드 객체를 인덱스를 입력하여 찾아주는 메서드. 
        getValueByIndex : 찾고자 하는 노드의 value를 노드 객체의 인덱스를 입력하여 찾는 메서드.
        
        """
        currentNode = self._head_pointer

        # 현재 선택된 노드의 이전 노드를 가리키는 포인터
        prev_pointer = self._head_pointer

        targetNode = None
        target_index = 0
        while True:
            if currentNode is None:
                break
            if currentNode.value == target_value:
                targetNode = currentNode
                if target_index == 0:
                    prev_pointer = None
                break
            prev_pointer = currentNode
            currentNode = currentNode.pointer
            target_index += 1
        if targetNode is None:
            return None
        return (targetNode, target_index, prev_pointer)

    def getValueByIndex(self, index: int) -> (Value):
        """찾고자 하는 값을 인덱스를 통해 찾음. 

        Parameters
        ----------
        index : int
            찾고자 하는 value를 가진 노드 객체의 인덱스.

        Returns
        -------
        Value : Node.value
            찾고자 하는 Value

        See Also
        --------
        findNodeByValue : 찾고자 하는 노드 객체를 value를 입력하여 찾는 메서드. 
        findNodeByIndex : 찾고자 하는 노드 객체를 인덱스를 입력하여 찾아주는 메서드.
        
        Notes
        -----
        내부적으로 findNodeByIndex() 메서드를 사용함. 

        """
        targetNode = self.findNodeByIndex(index)[0]
        return targetNode.value

    def insertNode(self, index: int, new_value: Value) -> (None):
        """연결 리스트에서 지정된 인덱스 위치에 새 노드 삽입.

        Parameters
        ----------
        index : int
            연결리스트 내에 새 노드를 삽입하고자 하는 인덱스 위치
        new_value : Value
            연결리스트 내에 삽입할 새 노드의 value

        See Also
        --------
        addNodeFront : 새 노드를 연결리스트의 맨 앞에 삽입하는 메서드. 
        addNodeBack : 새 노드를 연결리스트의 맨 뒤에 삽입하는 메서드.
        
        """
        self._insertNode(index, Node(new_value))

    def _insertNode(self, index: int, newNode: Node) -> (None):
        oldNode, _, prev_pointer = self.findNodeByIndex(index)
        newNode.pointer = oldNode
        if prev_pointer is None:
            # 삽입하고자 하는 인덱스 위치가 0임.
            self._head_pointer = newNode
        else:
            prev_pointer.pointer = newNode
        self._length += 1

    def _deleteNode(
            self,
            targetNode: Node,
            prev_pointer: Node | None
        ) -> (None):
        if prev_pointer is None:
            # 삭제하고자 하는 노드의 인덱스 위치가 0임.
            self._head_pointer = targetNode.pointer
        elif targetNode.pointer is None:
            # 삭제하고자 하는 요소가 연결 리스트의 맨 뒤에 존재하는 경우.
            self._tail_pointer = prev_pointer
            prev_pointer.pointer = None
        else:
            prev_pointer.pointer = targetNode.pointer
        targetNode.pointer = None
        del targetNode
        self._length -= 1

    def deleteNodeByIndex(self, index: int) -> (None):
        """인덱스에 해당하는 노드 삭제.

        Parameters
        ----------
        index : int
            연결리스트 내에서 삭제하고자 하는 노드의 인덱스

        See Also
        --------
        popFront : 연결 리스트의 맨 앞에 있는 노드를 추출 후 제거. 
        popBack : 연결 리스트의 맨 뒤에 있는 노드 추출 후 제거.
        deleteNodeByValue : 삭제하고자 하는 value와 일치하는 노드 삭제.

        """
        targetNode, _, prev_pointer = self.findNodeByIndex(index)
        self._deleteNode(targetNode, prev_pointer)

    def deleteNodeByValue(self, target_value: Value) -> (None):
        """삭제하고자 하는 값과 일치하는 노드를 삭제.
        
        Parameters
        ----------
        target_value : Value
            삭제하고자 하는 노드의 value
        
        See Also
        --------
        popFront : 연결 리스트의 맨 앞에 있는 노드를 추출 후 제거. 
        popBack : 연결 리스트의 맨 뒤에 있는 노드 추출 후 제거.
        deleteNodeByIndex : 인덱스 위치에 해당하는 노드 객체 삭제. 

        """
        try:
            search_result = self.findNodeByValue(target_value)
        except TypeError:
            print("TypeError: 찾고자 하는 값이 없습니다.")
        else:
            targetNode, _, prev_pointer = search_result
        self._deleteNode(targetNode, prev_pointer)

    def popFront(self, node_mode: bool = True) -> (Node | Value):
        """연결 리스트의 맨 앞에 있는 노드를 추출 후 제거. 

        Parameters
        ----------
        node_mode : bool, default True
            True -> Node 객체를 반환. 
            False -> Node 객체의 value 반환.

        Returns
        -------
        Node
            Node 객체. `node_mode` 매개변수를 True로 설정 시 반환되는 타입.
        Value
            Node.value. 'node_mode' 매개변수를 False로 설정 시 반환되는 타입. 

        Raises
        ------
        IndexError
            빈 연결 리스트에서 pop 시도 시, IndexError 예외 발생. 

        See Also
        --------
        popBack : 연결 리스트의 맨 뒤에 있는 노드 추출 후 제거.
        deleteNodeByIndex : 인덱스 위치에 해당하는 노드 객체 삭제. 
        deleteNodeByValue : 삭제하고자 하는 value와 일치하는 노드 삭제.
        
        """
        node_to_pop = self.findNodeByIndex(0)[0]
        self.deleteNodeByIndex(0)
        if node_mode: return node_to_pop
        return node_to_pop.value

    def popBack(self, node_mode: bool = True) -> (Node | Value):
        """연결 리스트의 맨 뒤에 있는 노드 추출 후 제거. 

        Parameters
        ----------
        node_mode : bool, default True 
            True -> Node 객체를 반환. 
            False -> Node 객체의 value 반환.

        Returns
        -------
        Node
            Node 객체. `node_mode` 매개변수를 True로 설정 시 반환되는 타입.
        Value
            Node.value. 'node_mode' 매개변수를 False로 설정 시 반환되는 타입. 
        
        Raises
        ------
        IndexError
            빈 연결 리스트에서 pop 시도 시, IndexError 예외 발생. 

        See Also
        --------
        deleteNodeByIndex : 인덱스 위치에 해당하는 노드 객체 삭제. 
        deleteNodeByValue : 삭제하고자 하는 value와 일치하는 노드 삭제.
        popFront : 연결 리스트의 맨 앞에 있는 노드를 추출 후 제거.
        
        """
        last_index = self.getLength() - 1
        node_to_pop = self.findNodeByIndex(last_index)[0]
        self.deleteNodeByIndex(last_index)
        if node_mode: return node_to_pop
        return node_to_pop.value

    def clear(self) -> (None):
        """연결 리스트를 모두 비운다. 
        즉, 연결 리스트 내 모든 노드들을 삭제한다.

        """
        # 사실 self._head_pointer = None으로 해도
        # 연결리스트의 맨 앞에 있는 Node 객체의 reference count를 0으로 만들어
        # 파이썬의 garbage collector가 자동으로 그 뒤에 연결되어 있는
        # 모든 노드들도 메모리 상에서 삭제할 것이다.
        # 그러나 여기서는 노드 객체의 삭제를 좀 더 명시적으로 확인하기 위해
        # 일부러 이 메서드의 코드를 작성함.

        node = self._head_pointer
        while node:
            nextNode = node.pointer
            node.pointer = None
            del node
            node = nextNode

        self._head_pointer: Node | None = None
        self._tail_pointer: Node | None = None
        self._length = 0
        Node.node_counter = 0

    def _remainingNodeNumbers(self) -> (int):
        """메모리 할당 해제 테스트용. 
        특정 노드 삭제 또는 clear() 메서드 호출로 인해 Node 객체가 삭제되는 지 
        테스트 용. 
        해당 연결리스트 내 노드의 개수 반환. 
        둘 이상의 연결 리스트 사용 시 하나의 연결 리스트 내 
        Node 객체의 수를 정확히 판별하지 못할 수 있으므로 
        단 하나의 연결리스트만 생성하고 테스트하기를 권장.
        """
        return Node.node_counter


class LinkedListQueue():
    """연결 리스트를 큐처럼 FIFO 구조로 사용함."""

    def __init__(self):
        self._ll = LinkedList()

    def __repr__(self):
        return repr(self._ll)

    def whatKindOfLL(self) -> (str):
        """현재 해당 연결 리스트의 종류를 반환."""
        return '큐 형태의 단일 연결 리스트'

    def isEmpty(self) -> (bool):
        return True if self._ll.getLength() == 0 else False

    def getLength(self) -> (int):
        return self._ll.getLength()

    def enqueue(self, new_value: Value) -> (None):
        self._ll.addNodeBack(new_value)

    def dequeue(self, only_value: bool = True) -> (Node | Value):
        """
        Parameters
        ----------
        only_value : bool, default True
            True: 값만 반환.
            False: 노드 자체를 반환.
        
        """
        result = self._ll.popFront()
        return result.value if only_value else result

    def showPeek(self) -> (Value):
        """큐에서 맨 처음으로 나올 값을 조회함."""
        return self._ll.findNodeByIndex(0)[0].value

    def clear(self):
        """큐를 비운다."""
        self._ll.clear()


class LinkedListStack():
    """연결리스트를 LIFO 구조의 stack처럼 사용한다."""
    def __init__(self) -> (None):
        self._lls = LinkedList()

    def __repr__(self):
        return repr(self._lls)

    def whatKindOfLL(self) -> (str):
        """현재 해당 연결 리스트의 종류를 반환."""
        return '스택 형태의 단일 연결 리스트'

    def isEmpty(self) -> (bool):
        return True if self._lls.getLength() == 0 else False

    def getLength(self) -> (int):
        return self._lls.getLength()

    def push(self, new_value: Value) -> (None):
        self._lls.addNodeBack(new_value)

    def pop(self, only_value: bool = True) -> (Value | Node):
        """스택 맨 끝 항목을 반환하고 스택에서 제거.

        Parameters
        ----------
        only_value : bool, default True
            True: 값만 반환. 
            False: 노드 자체를 반환.
        
        """
        result = self._lls.popBack()
        return result.value if only_value else result

    def searchPeek(self) -> (Value):
        """스택 맨 끝 항목 조회."""
        return self._lls.findNodeByIndex(self.getLength()-1)[0].value

    def clear(self):
        """스택 내 모든 항목 제거."""
        self._lls.clear()


class DoublyLinkedList(LinkedList):
    """이중 연결 리스트."""

    def __init__(self):
        """
        Attributes
        ----------
        self._head_pointer : Node | None, default None
            맨 앞 노드를 가리키는 포인터. Node 객체를 받는다.
        self._tail_pointer : Node | None, default None
            맨 뒤 노드를 가리키는 포인터. Node 객체를 받는다.
        self._length : int, default 0 
            연결 리스트 내 총 노드의 개수.
        self.link_char : str, default ' <-> '
            해당 객체 출력 시 노드 간 연결 관계를 표현할 기호.
        self._iter_mode : bool, default True
            연결리스트를 반복할 때 노드 객체를 반환시킬 것인지, 노드의 
            값만을 반환시킬지를 결정하는 변수. 
        
        """
        super().__init__()
        self._head_pointer: DPNode | None = None
        self._tail_pointer: DPNode | None = None
        self._link_char = ' <-> '

    def __iter__(self):
        node = self._head_pointer
        while node:
            if self._iter_mode: yield node
            else: yield node.value
            node = node.next_pointer

    def __repr__(self):
        linked_list = []
        currentNode: DPNode | None = self._head_pointer
        while currentNode is not None:
            value_ = currentNode.value
            if not isinstance(value_, str): value_ = str(value_)
            linked_list.append(value_)
            currentNode = currentNode.next_pointer
        if linked_list:
            return self._link_char.join(linked_list)
        return "빈 연결리스트."

    def addNodeFront(self, new_value: DPNode) -> (None):
        self._addNodeFront(DPNode(new_value))

    def _addNodeFront(self, newNode: DPNode) -> (None):
        if self._head_pointer is None:
            # 연결 리스트에 아무런 노드도 없는 경우.
            self._head_pointer = newNode
            self._tail_pointer = newNode
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            newNode.next_pointer = self._head_pointer
            self._head_pointer.prev_pointer = newNode
            self._head_pointer = newNode
        self._length += 1

    def addNodeBack(self, new_value: Value) -> (None):
        self._addNodeBack(DPNode(new_value))

    def _addNodeBack(self, newNode: DPNode) -> (None):
        if self._tail_pointer is None:
            # 연결 리스트에 아무 노드도 없는 경우.
            self._tail_pointer = newNode
            self._head_pointer = newNode
        else:
            # 연결 리스트에 기존 노드들이 존재하는 경우.
            self._tail_pointer.next_pointer = newNode
            newNode.prev_pointer = self._tail_pointer
            self._tail_pointer = newNode
        self._length += 1

    def findNodeByIndex(self, index: int) -> (tuple[DPNode, int]):
        """인덱스로 찾고자 하는 노드 반환. 

        Parameters
        ----------
        index : int
            인덱스의 시작 번호는 0이다. 

        Returns
        -------
        tuple[targetNode, index]
            targetNode : DPNode
                인덱스에 해당하는 DPNode 객체.
            index : int
                해당 인덱스.

        Raises
        ------
        IndexError
            현재 연결 리스트의 노드 개수보다 더 큰 인덱스 값 대입 시,
            또는 인덱스에 음수 입력 시 해당 예외 발생.

        See Also
        --------
        findNodeByValue : 찾고자 하는 노드 객체를 value를 입력하여 찾는 메서드. 
        getValueByIndex : 찾고자 하는 노드의 value를 노드 객체의 인덱스를 입력하여 찾는 메서드. 
        
        """
        if self._length < index + 1 or index < 0:
            raise IndexError("연결 리스트의 길이에서 벗어나는 인덱스를 입력하였습니다.")
        cur_i = 0
        targetNode = self._head_pointer
        while cur_i != index:
            targetNode = targetNode.next_pointer
            cur_i += 1
        return (targetNode, index)

    def findNodeByValue(
            self,
            target_value: Value
        ) -> (tuple[DPNode, int] | None):
        """찾고자 하는 값을 입력하면 해당 값을 보유한 노드 반환.

        Parameters
        ----------
        target_value : Value
            찾고자 하는 value

        Returns
        -------
        tuple[targetNode, target_index]
            targetNode : DPNode
                찾고자 하는 value를 가진 Node 객체.
            target_index : int
                찾고자 하는 value를 가진 Node 객체의 인덱스. 

        None
            찾고자 하는 노드가 없을 때 반환됨. 

        See Also
        --------
        findNodeByIndex : 찾고자 하는 노드 객체를 인덱스를 입력하여 찾아주는 메서드. 
        getValueByIndex : 찾고자 하는 노드의 value를 노드 객체의 인덱스를 입력하여 찾는 메서드.
        
        """
        currentNode = self._head_pointer
        targetNode = None
        target_index = 0
        while True:
            if currentNode is None:
                break
            if currentNode.value == target_value:
                targetNode = currentNode
                break
            currentNode = currentNode.next_pointer
            target_index += 1
        if targetNode is None:
            return None
        return (targetNode, target_index)

    def insertNode(self, index: int, new_value: Value) -> (None):
        self._insertNode(index, DPNode(new_value))

    def _insertNode(self, index: int, newNode: DPNode) -> (None):
        oldNode = self.findNodeByIndex(index)[0]
        newNode.next_pointer = oldNode
        if oldNode.prev_pointer is None:
            # 삽입하고자 하는 인덱스 위치가 0임.
            self._head_pointer = newNode
            oldNode.prev_pointer = newNode
        else:
            newNode.prev_pointer = oldNode.prev_pointer
            oldNode.prev_pointer.next_pointer = newNode
            oldNode.prev_pointer = newNode
        self._length += 1

    def __deleteNode(self, targetNode: DPNode):
        if targetNode.prev_pointer is None:
            # 삭제하고자 하는 인덱스 위치가 0임.
            self._head_pointer = targetNode.next_pointer
            self._head_pointer.prev_pointer = None
        elif targetNode.next_pointer is None:
            # 삭제하고자 하는 요소가 맨 마지막에 위치한 경우.
            self._tail_pointer = targetNode.prev_pointer
            targetNode.prev_pointer.next_pointer = None
            targetNode.prev_pointer = None
        else:
            targetNode.prev_pointer.next_pointer = targetNode.next_pointer
            targetNode.next_pointer.prev_pointer = targetNode.prev_pointer
            targetNode.prev_pointer = None
        targetNode.next_pointer = None
        del targetNode
        self._length -= 1

    def deleteNodeByIndex(self, index: int) -> (None):
        targetNode = self.findNodeByIndex(index)[0]
        self.__deleteNode(targetNode)

    def deleteNodeByValue(self, target_value: Value) -> (None):
        try:
            search_result = self.findNodeByValue(target_value)
        except TypeError as exc:
            raise TypeError("TypeError: 찾고자 하는 값이 없습니다.") from exc
        targetNode = search_result[0]
        self.__deleteNode(targetNode)

    def clear(self) -> (None):
        node = self._head_pointer
        while node:
            nextNode = node.next_pointer
            node.next_pointer = None
            node.prev_pointer = None
            del node
            node = nextNode

        self._head_pointer: DPNode | None = None
        self._tail_pointer: DPNode | None = None
        self._length = 0
        DPNode.dpnode_counter = 0

    # 반환 타입 Node -> DPNode로 고침.
    def popFront(self) -> (DPNode | None): return super().popFront()
    def popBack(self) -> (DPNode | None): return super().popBack()
    def whatKindOfLL(self) -> (str): return "이중 연결 리스트"
    def _remainingNodeNumbers(self) -> (int): return DPNode.dpnode_counter


class CircularLinkedList(DoublyLinkedList):
    """원형 연결 리스트 구현. 
    이중 연결리스트를 이용하여 구현함.
    """
    def __init__(self): super().__init__()
    def whatKindOfLL(self) -> (str): return "원형 연결 리스트"

    def __iter__(self):
        node = self._head_pointer
        while True:
            if self._iter_mode: yield node
            else: yield node.value
            if node == self._tail_pointer: break
            node = node.next_pointer

    def __repr__(self):
        empty_msg = "빈 연결리스트."
        if self._head_pointer is None: return empty_msg

        linked_list = []
        currentNode = self._head_pointer
        while True:
            value_ = currentNode.value
            if not isinstance(value_, str): value_ = str(value_)
            linked_list.append(value_)
            if currentNode == self._tail_pointer: break
            currentNode = currentNode.next_pointer

        if linked_list:
            return self._link_char.join(linked_list)
        return empty_msg

    def addNodeFront(self, new_value: Value) -> (None):
        super().addNodeFront(new_value)
        #self._tail_pointer.next_pointer = self._head_pointer.prev_pointer
        if self._length > 1:
            self._tail_pointer.next_pointer = self._head_pointer
            self._head_pointer.prev_pointer = self._tail_pointer

    def addNodeBack(self, new_value: Value) -> (None):
        super().addNodeBack(new_value)
        #self._tail_pointer.next_pointer = self._head_pointer.prev_pointer
        if self._length > 1:
            self._tail_pointer.next_pointer = self._head_pointer
            self._head_pointer.prev_pointer = self._tail_pointer

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
        """인덱스로 찾고자 하는 노드 반환. 

        인덱스의 시작 번호는 0이다. 
        현재 연결 리스트의 노드 개수보다 더 큰 인덱스 값 대입 시,
        또는 인덱스에 음수 입력 시 순환시킨 인덱스를 사용한다. 
        따라서, 전체 크기에 벗어난 인덱스를 사용해도 에러가 일어나지 않도록 하였다. 

        ex1) ll_size = 10, index = 13
        -> index = index % ll_size
        = 13 % 10 = 3
        ex2) ll_size = 10, index = -12
        -> index = - (abs(index) % ll_size) = - (12 % 10) = -2
        -> index = (ll_size-1) + (-2) = 7

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
        node = self._head_pointer
        while True:
            if node == self._tail_pointer:
                del node
                break
            nextNode = node.next_pointer
            node.next_pointer = None
            node.prev_pointer = None
            del node
            node = nextNode

        self._head_pointer: DPNode | None = None
        self._tail_pointer: DPNode | None = None
        self._length = 0

    def _remainingNodeNumbers(self) -> (int):
        return DPNode.dpnode_counter


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
