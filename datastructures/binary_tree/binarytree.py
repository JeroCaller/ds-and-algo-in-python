"""
이진 트리 (binary tree)를 구현하는 모듈.

추후 추가 기능)
이진 트리, AVL 트리를 재귀 호출 방식이 아닌 While문을 이용한 
무한 루프 방식으로 구현하기. 재귀 호출수 제한을 벗어날 수 있다. 
"""
from typing import Final, Generator
from sub_modules.my_queue import DynamicQueue

# type alias
BNode_ = object  # BNode 객체
NodeValue = int
Depth = int # Binary Tree에서의 노드의 깊이.

# 상수 정의
class GA():
    """
    BinaryTree().getAll() 메서드의 mode 매개변수에 넣을 수 있는 
    상수 모음.
    """
    ASCVALUE: Final = "ascending values"
    ASCDEPTH: Final = "ascending ASCDEPTH"
    JUSTGIVEME: Final = "just give me them all"


class BNode():
    node_count = 0

    def __init__(self, value_: NodeValue, depth: int = 0):
        """
        이진 트리 (binary tree)를 구성하는 노드를 구현하는 클래스.

        매개변수) \n
        value: 노드에 저장될 값. \n
        depth: 이진 트리 내에서 해당 노드의 깊이. 
        root는 깊이를 0이라 가정. 
        자식 쪽으로 한 칸씩 내려갈수록 깊이가 1씩 증가.
        
        속성) \n
        self.__left: 노드의 왼쪽 자식 노드. \n
        self.__right: 노드의 오른쪽 자식 노드. \n
        self.__value: 노드의 값. \n
        self._node_depth: 해당 노드의 이진 트리 내 깊이. \n
        self._node_number: 해당 노드의 숫자. BF를 구하는 용도. \n
        """
        self.__value: NodeValue = value_
        self.__left: BNode | None = None
        self.__right: BNode | None = None
        self._node_depth: Depth = depth
        self.__node_height: int = 1  # 1 이상이어야 함.
        BNode.node_count += 1

    def __del__(self): BNode.node_count -= 1
    def __lt__(self, other: BNode_): return self.depth < other.depth

    def __repr__(self):
        basic_info = f"Node object. its value: {self.value}, " + \
        f"its depth in BT: {self.depth}, height: {self.height}"
        lc = self.leftChild.value if self.leftChild else None
        rc = self.rightChild.value if self.rightChild else None
        additional_info = f" lc.value: {lc}, rc.value: {rc}"
        return basic_info + additional_info
    
    def calculateNodeHeight(self) -> (None):
        """
        해당 노드의 높이를 계산하는 메서드. 
        노드 높이는 Balance factor 계산에 쓰인다.
        """
        left_num = self.leftChild.height if self.leftChild else 0
        right_num = self.rightChild.height if self.rightChild else 0
        self.height = max(left_num, right_num) + 1
    
    def BalanceFactor(self) -> (int):
        """
        루트 노드의 각각 왼쪽과 오른쪽 하위 트리의 깊이 차를 구하는 메서드. 
        BF = 왼쪽 하위 트리의 깊이 - 오른쪽 하위 트리의 깊이. 
        BF > 0 -> 왼쪽 하위 트리가 더 깊음(왼쪽으로 쏠림). 
        BF < 0 -> 오른쪽 하위 트리가 더 깊음(오른쪽으로 쏠림).
        """
        left_num = self.leftChild.height if self.leftChild else 0
        right_num = self.rightChild.height if self.rightChild else 0
        return left_num - right_num
    
    @property
    def value(self) -> (NodeValue): return self.__value

    @value.setter
    def value(self, new_value: NodeValue) -> (None): self.__value = new_value

    @property
    def leftChild(self) -> (BNode_ | None): return self.__left
    
    @leftChild.setter
    def leftChild(self, new_left: BNode_) -> (None): self.__left = new_left

    @property
    def rightChild(self) -> (BNode_ | None): return self.__right

    @rightChild.setter
    def rightChild(self, new_right: BNode_) -> (None): self.__right = new_right

    @property
    def depth(self) -> (int): return self._node_depth

    @depth.setter
    def depth(self, new_depth: int) -> (None): self._node_depth = new_depth

    @property
    def height(self) -> (int): return self.__node_height

    @height.setter
    def height(self, new_height: int) -> (None): self.__node_height = new_height


class BinaryTree():
    def __init__(self):
        """
        왼쪽 자식 노드의 값 < 부모 노드의 값 < 오른쪽 노드의 값.
        """
        self._root: BNode | None = None
        self._node_depth: Depth = 0
        self._num_node = 0  # 이진 트리 내 총 노드 개수.
        self._node_list: list[BNode] = []  # self.getAll 전용.
        self._ascending_with_node: bool = False

    def ascendingOrderWithNode(self, mode_set: bool = False) -> (None):
        """
        오름차순으로 노드 반환 시 노드 자체를 반환할 것인지, 
        노드의 값들만을 반환할 것인지를 설정하는 메서드. 
        True시 노드 자체를 반환. False시 노드의 값만 반환.
        """
        self._ascending_with_node = mode_set

    def __iter__(self) \
        -> (Generator[BNode, BNode, BNode] \
        | Generator[NodeValue, NodeValue, NodeValue] | None):
        """
        이진 트리 내 모든 노드들을 노드 값들의 오름차순으로 
        반환하는 이터레이터.
        """
        if self._ascending_with_node:
            for node in self._ascendingOrder(self._root):
                yield node
        else:
            for value in self._ascendingOrder(self._root):
                yield value

    def _ascendingOrder(
            self, 
            node: BNode
            ) \
        -> (Generator[BNode, BNode, BNode] \
        | Generator[NodeValue, NodeValue, NodeValue] | None):
        """
        왼쪽 자식 노드 값 < 부모 노드 값 < 오른쪽 자식 노드 값이란 
        사실을 이용하여 오름차순으로 숫자들을 반환한다. 
        """
        if node is None: return
        
        if self._ascending_with_node:
            for nod in self._ascendingOrder(node.leftChild):
                yield nod
            yield node
            for nod in self._ascendingOrder(node.rightChild):
                yield nod
        else:
            for value in self._ascendingOrder(node.leftChild):
                yield value
            yield node.value
            for value in self._ascendingOrder(node.rightChild):
                yield value

    def getAll(self, mode: GA = GA.JUSTGIVEME) -> (list[BNode] | None):
        """
        이진 트리 내 모든 노드 반환. 
        """
        self._node_list = []
        if mode == GA.ASCVALUE:
            self._getAllAscendingValue(self._root)
        elif mode == GA.ASCDEPTH:
            #self._getAllAscendingDepth(self._root)
            self._getAllAscendingDepth2(self._root)
        else:
            self._getAll(self._root)
        return self._node_list if len(self._node_list) != 0 else None

    def _getAll(self, node: BNode) -> (None):
        """
        이진 트리의 높이가 0인 노드부터 self._node_list에 추가하는 
        메서드. 
        """
        if node is None: return
        if node.leftChild: self._getAll(node.leftChild)
        if node.rightChild: self._getAll(node.rightChild)
        self._node_list.append(node)

    def _getAllAscendingValue(self, node: BNode) -> (None):
        """
        이진 트리 내 모든 노드들을 노드값들의 오름차순으로 나열된 
        배열로 구성하여 리스트에 담는 메서드.
        """
        if node is None: return

        if node.leftChild:
            self._getAllAscendingValue(node.leftChild)
        self._node_list.append(node)
        if node.rightChild:
            self._getAllAscendingValue(node.rightChild)

    def _getAllAscendingDepth(self, node: BNode) -> (None):
        """
        self.getAll()의 서브 메서드. 
        이진 트리 내 모든 노드들을 노드의 깊이 순으로 나열된 배열을 구성하는 
        메서드. 즉, 최상위 루트 노드가 배열의 맨 왼쪽에 위치하게끔 함. 
        """
        self._getAll(node)
        temp_list: list[tuple[Depth, BNode]] = []
        for nod in self._node_list:
            temp_list.append((nod.depth, nod))
        temp_list.sort()
        self._node_list.clear()
        for val, nod in temp_list:
            self._node_list.append(nod)

    def _getAllAscendingDepth2(self, node: BNode) -> (None):
        """
        BFS 알고리즘을 이용하여 깊이 오름차순으로 노드들을 배열한다. 
        """
        queue = DynamicQueue(False)
        queue.enqueue(node)
        while not queue.isEmpty():
            n: BNode = queue.dequeue()
            self._node_list.append(n)
            if n.leftChild:
                queue.enqueue(n.leftChild)
            if n.rightChild:
                queue.enqueue(n.rightChild)
        queue.clear()

    def getLen(self) -> (int):
        """
        이진 트리 내 총 노드의 수 반환.
        """
        return self._num_node

    def __contains__(self, target_value: NodeValue) -> (bool):
        """
        이진 트리에 특정 값이 있는지 조사. 있는지 없는지만 알려준다. 
        사용법: target_value in BinaryTree 객체. 
        반환값은 반드시 bool이어야 함.
        """
        node = self._root
        while node:
            if target_value == node.value: return True
            if target_value < node.value: node = node.leftChild
            else: node = node.rightChild
        return False
    
    def search(self, target_value: NodeValue) -> (BNode | None):
        """
        찾고자 하는 값과 일치하는 노드를 반환. 
        """
        return self._search(self._root, target_value)

    def _search(
            self, 
            node: BNode, 
            target_value: NodeValue
            ) -> (BNode | None):
        """
        self.search() 메서드를 돕는 서브 메서드.
        """
        if node is None: return None
        if node.value == target_value: return node
        elif node.value > target_value: 
            node = self._search(node.leftChild, target_value)
        else:
            node = self._search(node.rightChild, target_value)
        return node

    def insert(self, new_value: NodeValue) -> (None):
        self._node_depth = 0
        self._root = self._insert(self._root, new_value)
        self._num_node += 1

    def _insert(
            self, 
            node: BNode | None, 
            value: NodeValue
            ) -> (BNode):
        """
        self.insert() 메서드를 돕는 서브 메서드. 
        반환값은 node 매개변수로 대입된 루트 노드. 
        """
        if node is None: return BNode(value, self._node_depth)

        self._node_depth += 1
        if value <= node.value:
            node.leftChild = self._insert(node.leftChild, value)
        else:
            node.rightChild = self._insert(node.rightChild, value)
        return node
    
    def insertSeveralData(self, values: list[NodeValue]) -> (None):
        """
        여러 노드들을 이진 트리에 한꺼번에 삽입한다.
        """
        for val in values: self.insert(val)
    
    def remove(self, target_value: NodeValue) -> (None):
        self._root = self._remove(self._root, target_value)

    def _remove(
            self, 
            node: BNode | None, 
            target_value: NodeValue
            ) -> (BNode | None):
        """
        self.remove() 메서드를 돕는 서브 메서드. 
        반환값은 매개변수 node. 단, 이 메서드를 실행하고 나면 
        구조가 바뀐 하위 트리를 가지게 될 것이다.
        """
        if node is None: return None

        if target_value < node.value:
            node.leftChild = self._remove(node.leftChild, target_value)
        elif target_value > node.value:
            node.rightChild = self._remove(node.rightChild, target_value)
        else:
            if node.leftChild is None: 
                self._num_node -= 1
                if node.rightChild: node.rightChild.depth -= 1
                return node.rightChild
            if node.rightChild is None: 
                self._num_node -= 1
                if node.leftChild: node.leftChild.depth -= 1
                return node.leftChild

            # 아래 코드는 삭제하고자 하는 노드가 두 자식 노드를 
            # 모두 가지고 있을 경우를 처리하는 코드임.

            node_to_be_removed: BNode = node
            depth_of_original = node.depth

            # 삭제되어 사라질 노드 자리를 대체하기 위해
            # 대체할 노드를 삭제할 노드의 오른쪽 하위 트리의 
            # 최소값을 가지는 노드로 가져와 대체한다.
            # 이를 위해 우선 삭제할 노드의 오른쪽 노드를 먼저 
            # 가리켜야 한다.
            node = node.rightChild

            # 최소값을 가지는 노드는 왼쪽 자식 노드를 가지지 않는 노드이다.
            # 해당 노드를 탐색한다.  
            while node.leftChild: node = node.leftChild

            node.rightChild = self._removeMin(node_to_be_removed.rightChild)

            # 삭제될 노드의 빈자리를 채우는 최소값 노드의 왼쪽 자식 노드는
            # 삭제될 노드의 왼쪽 자식 노드를 가리키도록 한다.
            node.leftChild = node_to_be_removed.leftChild
            node.depth = depth_of_original
            self._num_node -= 1
        return node

    def _removeMin(self, node: BNode) -> (BNode | None):
        """
        self._remove() 메서드를 돕는 서브 메서드. 
        최소값을 가지는 노드가 삭제될 노드 자리로 갈 때, 
        최소값을 가지는 노드의 빈자리를 
        최소값 노드의 하위 오른쪽 자식 노드로 대체.
        반환값은 구조 조정을 마친 루트 노드.
        """
        if node.leftChild is None: return node.rightChild
        node.leftChild = self._removeMin(node.leftChild)
        node.leftChild.depth -= 1
        return node
    
    def popNode(self, target_value: NodeValue) -> (None):
        """
        찾고자 하는 값과 일치하는 노드를 반환한 후, 해당 노드를 이진 트리
        에서 삭제.
        """
        self.search(target_value)
        self.remove(target_value)

    def clear(self) -> (None):
        """
        이진 트리 내 모든 노드들을 제거하여 빈 이진 트리로 리셋시킨다. 
        """
        def delete_all(node: BNode) -> (None):
            if node is None: return

            if node.leftChild:
                delete_all(node.leftChild)
            if node.rightChild:
                delete_all(node.rightChild)
            del node

        delete_all(self._root)
        #del self._root
        self._root: BNode | None = None
        self._node_depth = 0
        self._num_node = 0  # 이진 트리 내 총 노드 개수.
        self._node_list = []  # self.getAll 전용.
        self._ascending_with_node = False

    def remainingNodeNumbers(self) -> (int):
        """
        clear() 메서드 사용 시 정말로 모든 노드가 삭제되는지 확인하기 위한 용도. 
        BNode() 객체의 클래스 속성을 이용하므로, 정확한 개수 확인을 위해선 
        단 하나의 BinaryTree 객체만을 형성해 테스트 해보는 것이 좋다. 
        """
        return BNode.node_count
    

class AVLTree(BinaryTree):
    """
    자가 균형 이진 트리 중 하나. 왼쪽 하위 트리와 오른쪽 하위 트리의 불균형을 
    스스로 탐지하고 이를 스스로 고쳐 균형을 유지한다. 
    """
    class SelfBalancingTools():
        def solveWhenLeftLeaning(self, node: BNode) -> (BNode):
            """
            노드가 왼쪽으로 치우쳐져 있을 때 이를 고치는 메서드.
            """
            if node.BalanceFactor() >= 2:
                if node.leftChild.BalanceFactor() >= 0:
                    # Left-Left
                    node = self.__rotateRight(node)
                else:
                    # Left-Right
                    node = self.__rotateLeftRight(node)
            return node
        
        def solveWhenRightLeaning(self, node: BNode) -> (BNode):
            """
            노드가 오른쪽으로 치우쳐져 있을 때 이를 해결하는 메서드. 
            """
            if node.BalanceFactor() <= -2:
                if node.rightChild.BalanceFactor() <= 0:
                    # Right-Right
                    node = self.__rotateLeft(node)
                else:
                    # Right-Left
                    node = self.__rotateRightLeft(node)
            return node
        
        def __recalculateDepthInSubTree(
                self,
                root_of_subtree: BNode,
                increase: bool
                ) -> (None):
            """
            주어진 하위 트리의 루트 노드로부터 해당 루트 노드를 포함한 
            하위 트리의 모든 노드들의 depth 값을 조정하는 메서드. \n
            매개변수)\n
            root_of_subtree: 하위 트리의 루트 노드 객체. \n
            increase: 하위 트리 내 모든 노드들의 depth값을 증가시킬지 감소시킬지 
            알려주는 매개변수. True -> 1씩 증가, False -> 1씩 감소.
            """
            current_node = root_of_subtree
            if current_node is None: return

            self.__recalculateDepthInSubTree(
                current_node.leftChild,
                increase
            )
            self.__recalculateDepthInSubTree(
                current_node.rightChild,
                increase
            )
            if increase:
                current_node.depth += 1
            else:
                current_node.depth -= 1
        
        def __rotateRight(self, node: BNode) -> (BNode):
            new_root = node.leftChild
            node.leftChild = new_root.rightChild
            new_root.rightChild = node

            new_root.depth -= 1
            node.depth += 1
            new_root.leftChild.depth -= 1
            self.__recalculateDepthInSubTree(node.rightChild, True)
            self.__recalculateDepthInSubTree(
                new_root.leftChild.leftChild,
                False
            )
            self.__recalculateDepthInSubTree(
                new_root.leftChild.rightChild,
                False
            )
            node.calculateNodeHeight()
            return new_root

        def __rotateLeftRight(self, node: BNode) -> (BNode):
            new_root = node.leftChild.rightChild
            new_left = node.leftChild

            new_left.rightChild = new_root.leftChild
            node.leftChild = new_root.rightChild
            new_root.leftChild = new_left
            new_root.rightChild = node

            new_root.depth -= 2
            node.depth += 1
            self.__recalculateDepthInSubTree(
                node.rightChild,
                True
            )
            self.__recalculateDepthInSubTree(
                node.leftChild,
                False
            )
            self.__recalculateDepthInSubTree(
                new_left.rightChild,
                False
            )
            node.calculateNodeHeight()
            new_left.calculateNodeHeight()
            return new_root
        
        def __rotateLeft(self, node: BNode) -> (BNode):
            new_root = node.rightChild
            node.rightChild = new_root.leftChild
            new_root.leftChild = node

            new_root.depth -= 1
            node.depth += 1
            new_root.rightChild.depth -= 1
            self.__recalculateDepthInSubTree(
                node.leftChild,
                True
            )
            self.__recalculateDepthInSubTree(
                new_root.rightChild.leftChild,
                False
            )
            self.__recalculateDepthInSubTree(
                new_root.rightChild.rightChild,
                False
            )
            node.calculateNodeHeight()
            return new_root

        def __rotateRightLeft(self, node: BNode) -> (BNode):
            new_root = node.rightChild.leftChild
            new_right = node.rightChild

            node.rightChild = new_root.leftChild
            new_right.leftChild = new_root.rightChild
            new_root.leftChild = node
            new_root.rightChild = new_right

            node.depth += 1
            new_root.depth -= 2
            self.__recalculateDepthInSubTree(
                node.leftChild,
                True
            )
            self.__recalculateDepthInSubTree(
                node.rightChild,
                False
            )
            self.__recalculateDepthInSubTree(
                new_right.leftChild,
                False
            )
            node.calculateNodeHeight()
            new_right.calculateNodeHeight()
            return new_root
    

    def __init__(self):
        super().__init__()
        self.solver = AVLTree.SelfBalancingTools()

    def _insert(
            self, 
            node: BNode | None, 
            value: NodeValue
            ) -> (BNode):
        """
        self.insert() 메서드를 돕는 서브 메서드. 
        반환값은 node 매개변수로 대입된 루트 노드. 
        """
        if node is None: return BNode(value, self._node_depth)

        self._node_depth += 1
        if value <= node.value:
            node.leftChild = self._insert(node.leftChild, value)
            node.calculateNodeHeight()
            node = self.solver.solveWhenLeftLeaning(node)
        else:
            node.rightChild = self._insert(node.rightChild, value)
            node.calculateNodeHeight()
            node = self.solver.solveWhenRightLeaning(node)
        node.calculateNodeHeight()
        return node
    
    def _remove(
            self, 
            node: BNode | None, 
            target_value: NodeValue
            ) -> (BNode | None):
        """
        self.remove() 메서드를 돕는 서브 메서드. 
        반환값은 매개변수 node. 단, 이 메서드를 실행하고 나면 
        구조가 바뀐 하위 트리를 가지게 될 것이다.
        """
        if node is None: return None

        if target_value < node.value:
            node.leftChild = self._remove(node.leftChild, target_value)
            node = self.solver.solveWhenRightLeaning(node)
        elif target_value > node.value:
            node.rightChild = self._remove(node.rightChild, target_value)
            node = self.solver.solveWhenLeftLeaning(node)
        else:
            if node.leftChild is None: 
                self._num_node -= 1
                if node.rightChild: node.rightChild.depth -= 1
                return node.rightChild
            if node.rightChild is None: 
                self._num_node -= 1
                if node.leftChild: node.leftChild.depth -= 1
                return node.leftChild

            # 아래 코드는 삭제하고자 하는 노드가 두 자식 노드를 
            # 모두 가지고 있을 경우를 처리하는 코드임.

            node_to_be_removed: BNode = node
            depth_of_original = node.depth

            # 삭제되어 사라질 노드 자리를 대체하기 위해
            # 대체할 노드를 삭제할 노드의 오른쪽 하위 트리의 
            # 최소값을 가지는 노드로 가져와 대체한다.
            # 이를 위해 우선 삭제할 노드의 오른쪽 노드를 먼저 
            # 가리켜야 한다.
            node = node.rightChild

            # 최소값을 가지는 노드는 왼쪽 자식 노드를 가지지 않는 노드이다.
            # 해당 노드를 탐색한다.  
            while node.leftChild: node = node.leftChild

            node.rightChild = self._removeMin(node_to_be_removed.rightChild)

            # 삭제될 노드의 빈자리를 채우는 최소값 노드의 왼쪽 자식 노드는
            # 삭제될 노드의 왼쪽 자식 노드를 가리키도록 한다.
            node.leftChild = node_to_be_removed.leftChild
            node.depth = depth_of_original
            node = self.solver.solveWhenLeftLeaning(node)
            self._num_node -= 1
        node.calculateNodeHeight()
        return node

    def _removeMin(self, node: BNode) -> (BNode | None):
        """
        self._remove() 메서드를 돕는 서브 메서드. 
        최소값을 가지는 노드가 삭제될 노드 자리로 갈 때, 
        최소값을 가지는 노드의 빈자리를 
        최소값 노드의 하위 오른쪽 자식 노드로 대체.
        반환값은 구조 조정을 마친 루트 노드.
        """
        if node.leftChild is None: return node.rightChild
        node.leftChild = self._removeMin(node.leftChild)
        node.leftChild.depth -= 1
        node = self.solver.solveWhenRightLeaning(node)
        node.calculateNodeHeight()
        return node


if __name__ == '__main__':
    pass