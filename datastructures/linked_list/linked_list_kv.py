"""
키-값 형태의 데이터를 담을 수 있는 연결 리스트 구현.
"""
try:
    import my_linked_list as mll
except ModuleNotFoundError:
    import linked_list.my_linked_list as mll
from multipledispatch import dispatch

# type alias
Key = object
Value = object
Item = tuple[Key, Value]
NodeKV_ = object
Index = int

# 상수 정의
class NodeAttr():
    KEY = "key"
    VALUE = "VALUE"
    ITEM = "ITEM"


class NodeKV():
    node_counter = 0

    def __init__(
            self, 
            key: Key = None,
            value: Value = None,
            pointer: NodeKV_ = None
        ):
        """
        하나의 노드를 구현하는 클래스. 
        매개변수
        -------
        key: 노드의 키. \n
        value: 노드의 값. \n
        pointer: 현재 노드의 다음 노드를 가리키는 포인터. \
        포인터에는 다음 노드의 메모리 주소값을 저장하므로 \
        해당 매개변수는 다음 Node 객체를 대입받아야 한다. \n
        """
        self._key: Key = key
        self._value: Value = value
        self._item: Item = (self._key, self._value)
        self.pointer: NodeKV = pointer
        NodeKV.node_counter += 1

    def __del__(self): NodeKV.node_counter -= 1

    @property
    def key(self) -> (Key): return self._key

    @key.setter
    def key(self, new_key: Key) -> (None): 
        self._key = new_key
        self._item = (self._key, self._value)

    @property
    def value(self) -> (Value): return self._value

    @value.setter
    def value(self, new_value: Value) -> (None): 
        self._value = new_value
        self._item = (self._key, self._value)

    @property
    def item(self) -> (Item): return self._item


class LinkedList(mll.LinkedList):
    def __init__(self):
        super().__init__()
        self.head_pointer: NodeKV | None = None
        self.tail_pointer: NodeKV | None = None

    def __iter__(self):
        node = self.head_pointer
        while node:
            if self._iter_mode: yield node
            else: yield node.item
            node = node.pointer

    def __repr__(self):
        linked_list = []
        current_node: NodeKV | None = self.head_pointer
        while current_node:
            key_, value_ = current_node.key, current_node.value
            #if type(key_) != str: key_ = str(key_)
            #if type(value_) != str: value_ = str(value_)
            linked_list.append(str((key_, value_)))
            current_node = current_node.pointer
        if linked_list: return self.link_char.join(linked_list)
        else: return "<empty>"

    def whatKindOfLL(self) -> (str):
        """
        현재 해당 연결 리스트의 종류를 반환.
        """
        return 'key-value 단일 연결 리스트'
    
    def _findAndFix(self, k: Key, new_v: Value) -> (None):
        """
        연결리스트 내 주어진 키와 일치하는 키를 가지는 노드의 value를 
        new_v로 바꿈. 
        """
        node = self.head_pointer
        while node:
            if node.key == k: 
                node.value = new_v
                return
            node = node.pointer
    
    @dispatch(tuple)
    def addNodeFront(self, new_kv: tuple[Key, Value]) -> (None):
        new_key, new_value = new_kv
        target_node = self.findNodeByKey(new_key)[0]
        if target_node:
            self._findAndFix(new_key, new_value)
            return
        self._addNodeFront(NodeKV(new_key, new_value))
    
    @dispatch(Key, Value)
    def addNodeFront(self, new_key: Key, new_value: Value) -> (None):
        """
        연결리스트의 맨 앞에 노드 삽입. 
        만약 기존의 연결리스트 내에 이미 동일한 키가 존재한다면, 해당 노드의 
        value를 new_value로 새로 바꾼다. (이 때는 새로운 노드를 삽입하지 않는다)
        """
        target_node = self.findNodeByKey(new_key)[0]
        if target_node:
            self._findAndFix(new_key, new_value)
            return
        self._addNodeFront(NodeKV(new_key, new_value))

    def _addNodeFront(self, new_node: NodeKV) -> (None):
        super()._addNodeFront(new_node)

    @dispatch(tuple)
    def addNodeBack(self, new_kv: tuple[Key, Value]) -> (None):
        new_key, new_value = new_kv
        target_node = self.findNodeByKey(new_key)[0]
        if target_node:
            self._findAndFix(new_key, new_value)
            return
        self._addNodeBack(NodeKV(new_key, new_value))

    @dispatch(Key, Value)
    def addNodeBack(self, new_key: Key, new_value: Value) -> (None):
        """
        연결리스트의 맨 뒤에 노드 삽입. 
        만약 기존의 연결리스트 내에 이미 동일한 키가 존재한다면, 해당 노드의 
        value를 new_value로 새로 바꾼다. (이 때는 새로운 노드를 삽입하지 않는다)
        """
        target_node = self.findNodeByKey(new_key)[0]
        if target_node:
            self._findAndFix(new_key, new_value)
            return
        self._addNodeBack(NodeKV(new_key, new_value))

    def _addNodeBack(self, new_node: NodeKV) -> (None):
        super()._addNodeBack(new_node)
    
    def findNodeByIndex(self, index: Index) -> (tuple[NodeKV, Index, NodeKV | None]):
        return super().findNodeByIndex(index)
    
    def findNodeByValue(self, target_value: Value) -> (tuple[NodeKV, Index, NodeKV | None] | None):
        return super().findNodeByValue(target_value)
    
    def getValueByIndex(self, index: Index) -> (Value):
        return super().getValueByIndex(index)
    
    def insertNode(
            self, 
            index: Index,
            new_key: Key,
            new_value: Value
        ) -> (None):
        self._insertNode(index, NodeKV(new_key, new_value))

    def _insertNode(
            self, 
            index: int, 
            new_node: NodeKV
        ) -> (None):
        super()._insertNode(index, new_node)
    
    def _deleteNode(self, target_node: NodeKV, prev_pointer: NodeKV | None) -> (None):
        super()._deleteNode(target_node, prev_pointer)
    
    def popFront(self, node_mode: bool = True) -> (NodeKV | Item):
        node_to_pop = self.findNodeByIndex(0)[0]
        self.deleteNodeByIndex(0)
        if node_mode: return node_to_pop
        else: return node_to_pop.item
    
    def popBack(self, node_mode: bool = True) -> (NodeKV | Item):
        last_index = self.getLength() - 1
        node_to_pop = self.findNodeByIndex(last_index)[0]
        self.deleteNodeByIndex(last_index)
        if node_mode: return node_to_pop
        else: return node_to_pop.item

    def remainingNodeNumbers(self) -> (int): return NodeKV.node_counter

    def clear(self) -> (None):
        super().clear()
        self.head_pointer: NodeKV | None = None
        self.tail_pointer: NodeKV | None = None

    def findNodeByKey(self, target_key: Key) \
        -> (tuple[NodeKV, Index, NodeKV] | tuple[None, None, None]):
        """
        주어진 키를 통해 연결리스트 내의 해당 키와 일치하는 키를 가지는 
        노드와 그 노드의 인덱스를 반환. 
        """
        node = self.head_pointer
        prev_pointer = None
        cur_i = 0
        while node:
            if node.key == target_key: return (node, cur_i, prev_pointer)
            prev_pointer = node
            node = node.pointer
            cur_i += 1
        return (None, None, None)

    def getValueByKey(self, target_key: Key) -> (Value | None):
        """
        주어진 key를 통해 key에 대응되는 value를 찾아 반환. 
        존재하지 않는 경우 None을 반환. 
        """
        node = self.head_pointer
        while node:
            if node.key == target_key: return node.value
            node = node.pointer
        return None
    
    def deleteNodeByKey(self, target_key: Key) -> (None):
        """
        주어진 키와 일치하는 키를 가진 노드를 삭제. 
        """
        target_node, index, prev_pointer = self.findNodeByKey(target_key)
        if target_node is None: return
        self._deleteNode(target_node, prev_pointer)
    
    def _iterAndReturn(
            self, 
            return_what: NodeAttr
            ) -> (list[Key] | list[Value] | list[Item]):
        """
        연결리스트 내 모든 노드들을 순회하면서 
        노드들의 키, 값 또는 (키-값) 요소를 리스트로 반환. 

        매개변수
        -------
        return_what: 노드의 무엇을 반환할 것인지 결정. \
        가능한 값들) NodeAttr.KEY, NodeAttr.VALUE, NodeATTR.ITEM 
        """
        node = self.head_pointer
        if node is None: return []

        result = []
        while node:
            if return_what == NodeAttr.KEY: result.append(node.key)
            elif return_what == NodeAttr.VALUE: result.append(node.value)
            else: result.append(node.item)
            node = node.pointer
        return result

    def items(self) -> (list[Item]):
        """
        현재 연결리스트 내 모든 노드들의 key-value들을 리스트로 반환. 
        비어 있는 연결리스트의 경우 빈 리스트를 반환. 
        """
        return self._iterAndReturn(NodeAttr.ITEM)

    def keys(self) -> (list[Key]):
        """
        현재 연결리스트 내 모든 노드들의 key만을 리스트로 반환 .
        비어 있는 연결리스트의 경우 빈 리스트를 반환.
        """
        return self._iterAndReturn(NodeAttr.KEY)
    
    def values(self) -> (list[Value]):
        """
        현재 연결리스트 내 모든 노드들의 value만을 리스트로 반환 .
        비어 있는 연결리스트의 경우 빈 리스트를 반환.
        """
        return self._iterAndReturn(NodeAttr.VALUE)
    

class LinkedListQueue(mll.LinkedListQueue):
    ...


if __name__ == '__main__':
    pass
    