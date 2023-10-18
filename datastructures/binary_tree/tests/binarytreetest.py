import sys
import dirimporttool

for i in range(1, 2+1):
    super_dir = dirimporttool.get_super_dir_directly(__file__, i)
    sys.path.append(super_dir)
    print(super_dir)

from binary_tree.binarytree import BinaryTree, AVLTree, GA
from binary_tree.binarytree import NodeValue


class PrintBorderlineDecor():
    """출력 경계선 관련 데코레이터 클래스"""
    def __init__(
            self, 
            borderline_char: str = '=',
            repeat_num: int = 60,
            ):
        """
        매개변수 설명) \n
        borderline_char: 경계선으로 지정할 문자.
        repeat_num: borderline_char로 지정된 문자로 경계선을 그을 때 문자의 반복 횟수. 
        """
        self.border = borderline_char
        self.repeat = repeat_num

    def __call__(self, func: callable):
        def wrapper(*args, **kwargs):
            print(self.border * self.repeat)
            result = func(*args, **kwargs)
            print(self.border * self.repeat)
            return result
        return wrapper


@PrintBorderlineDecor(repeat_num=60)
def printBinaryNodes(
    bt_inst: BinaryTree | AVLTree, 
    find_value: NodeValue | None = None
    ):
    """
    이진 트리 내 노드들의 상태를 모두 출력.
    """
    result_nodes = bt_inst.getAll(GA.ASCDEPTH)
    num_nodes = bt_inst.getLen()
    print("현재 이진 트리 내 노드 상태")
    if result_nodes is None: print("노드 없음.")
    else: 
        for node in result_nodes: print(node)
    print(f"현재 노드의 개수: {num_nodes}")
    if find_value:
        existence = find_value in bt_inst
        print(f"찾고자 하는 노드의 값: {find_value}, 존재 여부: {existence}")


class TestFailureDecor():
    """
    테스트 실패 관련 데코레이터. 
    테스트 메서드 중 원하는 결과와 전혀 다른 결과가 나온 메서드에 대해서 
    해당 테스트가 실패했다는 것을 표시하고, 그 원인과 해결책을 서술할 수 있도록 
    고안한 데코레이터. 
    """
    def __init__(
            self, 
            reason: str = None, 
            rusure: bool = False,
            solution: str = None):
        """
        매개변수)
        reason: 테스트 실패 원인을 문자열로 적은 변수. 실패 원인을 파악하지 못했다면 None으로 둔다. \n
        rusure: 테스트 실패 원인이 확실한지에 대한 변수. True: 확실, False: 확실하지는 않은 추측. \n
        solution: 테스트 실패 원인에 대한 해결책 문자열. 해결책을 모르겠다면 None으로 둔다. \n
        """
        self.reason = reason
        self.rusure = rusure
        self.solution = solution

    def __call__(self, func: callable):
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} 테스트 메서드(또는 함수)는 테스트에 실패했습니다.")
            self.printReason()
            self.printSolution()
            return_result = func(*args, **kwargs)
            return return_result
        return wrapper
    
    @PrintBorderlineDecor(borderline_char="-")
    def printReason(self):
        if self.reason:
            if self.rusure:
                print("실패 원인을 파악하였습니다. 다음의 내용은 확실합니다.")
            else:
                print("실패 원인에 대해 확실치는 않지만 추측한 내용이 있습니다.")
            print("다음은 테스트 실패 원인입니다.")
            print(self.reason)
        else:
            print("아직 실패 원인을 파악하지 못했습니다.")

    @PrintBorderlineDecor(borderline_char="-")
    def printSolution(self):
        if self.solution:
            print("테스트 실패 원인에 대해서는 다음과 같은 내용으로 " \
                  + "해결할 수 있을 것으로 추측됩니다.")
            print(self.solution)
        else:
            print("아직 테스트 실패 원인에 대한 해결책을 찾지 못했습니다.")


class TestBinaryTree():
    def __init__(
            self, 
            data: list[NodeValue] = [19, 14, 53, 3, 15, 26, 58, 29]
            ):
        self.bt = BinaryTree()
        self.test_data = data
        self.__insertAllData()

    def getBinaryTree(self) -> (BinaryTree): return self.bt
    def __resetBinaryTree(self):
        """
        새로운 빈 이진 트리를 만들어 리셋시킨다. 
        """
        self.bt = BinaryTree()

    def __insertAllData(self):
        self.bt.insertSeveralData(self.test_data)

    def changeData(self, new_data: list[NodeValue]) -> (None):
        """
        이진 트리에 들어갈 테스트 데이터를 바꾼다. 
        새 데이터로 구성된 완전히 새로운 이진 트리로 리셋된다. 
        """
        self.test_data = new_data
        self.__resetBinaryTree()
        self.__insertAllData()

    def removeNothing(self):
        """
        이진 트리에 없는 값을 삭제하려는 경우.
        """
        self.bt.remove(1)
        printBinaryNodes(self.bt)

    def removeLeafNode(self, target_value: NodeValue = 15):
        """
        리프 노드 삭제 테스트.
        """
        self.bt.remove(target_value)
        printBinaryNodes(self.bt, target_value)

    def removeNodeWithoutLc(self, target_value: NodeValue = 26):
        """
        왼쪽 자식 노드가 없는 노드 삭제 테스트.
        """
        self.bt.remove(target_value)
        printBinaryNodes(self.bt, target_value)

    def removeRootNode(self):
        """
        루트 노드 삭제 테스트. 
        """
        target_value = self.test_data[0]
        self.bt.remove(target_value)
        printBinaryNodes(self.bt)

    def removeNodeWithTwoChild(self, target_value: NodeValue = 53):
        """
        두 자식 노드 모두 존재하는 노드 삭제 테스트. 
        """
        self.bt.remove(target_value)
        printBinaryNodes(self.bt, target_value)

    def popNode(self, target_value: NodeValue = 53):
        """
        search 기능과 remove 기능이 동시에 작동하는지 테스트.
        """
        self.bt.popNode(target_value)
        printBinaryNodes(self.bt, target_value)

    def searchTest(self, target_value: NodeValue = 14):
        """
        찾고자 하는 값의 노드를 잘 반환하는지 테스트. 
        검색만으로는 이진 트리의 구조에 아무런 영향이 안 가는지 테스트.
        """
        result_node = self.bt.search(target_value)
        print("검색된 노드 정보")
        print(result_node)
        printBinaryNodes(self.bt, target_value)

    @PrintBorderlineDecor()
    def getAllTest(self, mode: GA = GA.JUSTGIVEME):
        """
        getAll() 메서드 테스트. 
        """
        results = self.bt.getAll(mode)
        for node in results:
            print(node)

    @PrintBorderlineDecor()
    def iterAscendingTestOnlyValue(self):
        """
        이진 트리 내 모든 노드들의 값을 오름차순으로 반환하는지 테스트.
        """
        self.bt.ascendingOrderWithNode(False)
        print("iter 값 테스트 출력.")
        for value in self.bt:
            print(value)

    @PrintBorderlineDecor()
    def iterAscendingTestWithNode(self):
        """
        이진 트리 내 모든 노드들을 값 기준 오름차순으로 반환하는지 테스트. 
        """
        self.bt.ascendingOrderWithNode(True)
        print("iter 노드 테스트 출력")
        for node in self.bt:
            print(node)

    def clearBT(self):
        """
        clear() 메서드 테스트. 이진 트리 내 모든 노드들을 삭제하고 
        빈 트리로 리셋시키는지 테스트. 
        """
        print(f"The number of nodes: {self.bt.remainingNodeNumbers()}")
        self.bt.clear()
        printBinaryNodes(self.bt)
        print(f"The number of nodes: {self.bt.remainingNodeNumbers()}")


class TestAVLTree():
    def __init__(self, data: list[NodeValue] = None):
        self.avl = AVLTree()
        self.bt = BinaryTree()  # 비교군
        self.test_data = data
        if self.test_data:
            self.avl.insertSeveralData(self.test_data)
            self.bt.insertSeveralData(self.test_data)

    def getAVLTreeObj(self) -> (AVLTree): return self.avl
    def getBinaryTreeObj(self) -> (BinaryTree): return self.bt
    def setData(self, new_data: list[NodeValue]):
        """
        새로운 데이터들로 이진 트리 재구성. 기존의 이진 트리 내 
        노드들은 모두 삭제되고 새로 대입된 데이터들로 채워진다. 
        """
        del self.avl
        del self.bt
        self.avl = AVLTree()
        self.bt = BinaryTree()
        self.test_data = new_data
        self.avl.insertSeveralData(self.test_data)
        self.bt.insertSeveralData(self.test_data)

    def testInsertUnitRR(
            self, 
            new_three_data: list[NodeValue] = [10, 20, 40]
            ):
        """
        데이터는 단 세 개만으로 구성. 자동 균형을 유지하는 지 테스트. 
        """
        self.setData(new_three_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertUnitLL(
            self, 
            new_three_data: list[NodeValue] = [40, 20, 10]
            ):
        """
        데이터는 단 세 개만으로 구성. 자동 균형을 유지하는 지 테스트. 
        """
        self.setData(new_three_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertUnitLR(
            self,
            new_three_data: list[NodeValue] = [40, 10, 20]
            ):
        """
        데이터는 단 세 개만으로 구성. 자동 균형을 유지하는 지 테스트. 
        """
        self.setData(new_three_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertUnitRL(
            self,
            new_three_data: list[NodeValue] = [10, 40, 20]
            ):
        """
        데이터는 단 세 개만으로 구성. 자동 균형을 유지하는 지 테스트. 
        """
        self.setData(new_three_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertFullLL(
        self,
        new_data: list[NodeValue] = [100, 90, 80, 105, 95, 85, 75]
        ):
        """
        데이터는 테스트에서 주요하게 볼 데이터 3개와, 
        각 데이터 노드의 양쪽 자식 노드들을 채워 구성. 
        자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertFullRR(
            self,
            new_data: list[NodeValue] = [80, 90, 100, 75, 85, 95, 105]
            ):
        """
        데이터는 테스트에서 주요하게 볼 데이터 3개와, 
        각 데이터 노드의 양쪽 자식 노드들을 채워 구성. 
        자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertFullLR(
            self,
            new_data: list[NodeValue] = [100, 80, 90, 95, 75, 85, 105]
            ):
        """
        데이터는 테스트에서 주요하게 볼 데이터 3개와, 
        각 데이터 노드의 양쪽 자식 노드들을 채워 구성. 
        자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertFullRL(
            self,
            new_data: list[NodeValue] = [80, 100, 90, 75, 85, 95, 105]
            ):
        """
        데이터는 테스트에서 주요하게 볼 데이터 3개와, 
        각 데이터 노드의 양쪽 자식 노드들을 채워 구성. 
        자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertGrandSubTreesLL(
            self,
            new_data: list[NodeValue] = [
                100, 90, 80, 105, 95, 85, 75,
                70, 77, 83, 87, 93, 97, 103, 107
            ]
            ):
        """
        테스트에서 위치가 다른 노드와 직접 바뀌는 주 데이터 3개와 
        그 데이터 노드들의 자식 노드들, 그리고 그 자식 노드들을 하위 트리의 루트 노드
        로 하는 손주 노드들로 구성. 자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertGrandSubTreesRR(
            self,
            new_data: list[NodeValue] = [
                80, 90, 100, 75, 85, 95, 105,
                73, 77, 83, 87, 93, 97, 103, 107
            ]
            ):
        """
        테스트에서 위치가 다른 노드와 직접 바뀌는 주 데이터 3개와 
        그 데이터 노드들의 자식 노드들, 그리고 그 자식 노드들을 하위 트리의 루트 노드
        로 하는 손주 노드들로 구성. 자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertGrandSubTreesLR(
            self,
            new_data: list[NodeValue] = [
                100, 80, 90, 95, 75, 85, 105,
                73, 77, 83, 87, 93, 97, 103, 107
            ]
            ):
        """
        테스트에서 위치가 다른 노드와 직접 바뀌는 주 데이터 3개와 
        그 데이터 노드들의 자식 노드들, 그리고 그 자식 노드들을 하위 트리의 루트 노드
        로 하는 손주 노드들로 구성. 자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)
    
    def testInsertGrandSubTreesRL(
            self,
            new_data: list[NodeValue] = [
                80, 100, 90, 75, 85, 95, 105,
                73, 77, 83, 87, 93, 97, 103, 107
            ]
            ):
        """
        테스트에서 위치가 다른 노드와 직접 바뀌는 주 데이터 3개와 
        그 데이터 노드들의 자식 노드들, 그리고 그 자식 노드들을 하위 트리의 루트 노드
        로 하는 손주 노드들로 구성. 자동 균형을 유지하는지 테스트. 
        """
        self.setData(new_data)
        printBinaryNodes(self.bt)
        printBinaryNodes(self.avl)

    def testInsertAndBalanceMidLL(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 83, 81
            ]
            ):
        """
        기울어진 곳이 최상위 노드가 포함되지 않은 하위 트리 내에서 발생 시 
        균형을 자동으로 유지하는지 테스트.
        """
        self.setData(new_data)
        print("testInsertAndBalanceMidLL 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)

    def testInsertAndBalanceMidRR(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 86, 87
            ]
            ):
        """
        기울어진 곳이 최상위 노드가 포함되지 않은 하위 트리 내에서 발생 시 
        균형을 자동으로 유지하는지 테스트.
        """
        self.setData(new_data)
        print("testInsertAndBalanceMidRR 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)

    def testInsertAndBalanceMidLR(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 83, 84
            ]
            ):
        """
        기울어진 곳이 최상위 노드가 포함되지 않은 하위 트리 내에서 발생 시 
        균형을 자동으로 유지하는지 테스트.
        """
        self.setData(new_data)
        print("testInsertAndBalanceMidLR 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)

    def testInsertAndBalanceMidRL(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 87, 86
            ]
            ):
        """
        기울어진 곳이 최상위 노드가 포함되지 않은 하위 트리 내에서 발생 시 
        균형을 자동으로 유지하는지 테스트.
        """
        self.setData(new_data)
        print("testInsertAndBalanceMidRL 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)

    def testRemoveUnitLL(
            self, 
            new_data: list[NodeValue] = [100, 110, 90, 80],
            target_value: NodeValue = 110
            ):
        """
        기존 노드 삭제 시 트리 구조가 Left-Left일 때 자동 균형 유지하는지 테스트. 
        맨 처음 데이터의 수는 4개로 하고 그 중 하나를 삭제한다.
        """
        self.setData(new_data)
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveUnitRR(
            self,
            new_data: list[NodeValue] = [80, 90, 70, 100],
            target_value: NodeValue = 70
            ):
        """
        기존 노드 삭제 시 트리 구조가 Right-Right 일 때 
        자동 균형 유지하는지 테스트. 
        맨 처음 데이터의 수는 4개로 하고 그 중 하나를 삭제한다.
        """
        self.setData(new_data)
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveUnitLR(
            self,
            new_data: list[NodeValue] = [100, 110, 80, 90],
            target_value: NodeValue = 110
            ):
        """
        기존 노드 삭제 시 트리 구조가 Left-Right 일 때 
        자동 균형 유지하는지 테스트. 
        맨 처음 데이터의 수는 4개로 하고 그 중 하나를 삭제한다.
        """
        self.setData(new_data)
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveUnitRL(
            self,
            new_data: list[NodeValue] = [80, 70, 100, 90],
            target_value: NodeValue = 70
            ):
        """
        기존 노드 삭제 시 트리 구조가 Right-Left 일 때 
        자동 균형 유지하는지 테스트. 
        맨 처음 데이터의 수는 4개로 하고 그 중 하나를 삭제한다.
        """
        self.setData(new_data)
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveFullLL(
            self,
            new_data: list[NodeValue] = [
                100, 90, 110, 115, 80, 95, 75, 85
            ],
            target_value: NodeValue = 110
            ):
        """
        기존 노드 삭제 시 트리 구조가 Left-Left 일 때 
        자동 균형 유지하는지 테스트. 
        기본 데이터 노드 수 4개와 각 노드의 자식 노드를 채운 상태에서 
        테스트를 진행한다. 
        """
        self.setData(new_data)
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveFullRR(
            self,
            new_data: list[NodeValue] = [
                80, 75, 90, 77, 85, 100, 95, 105
            ],
            target_value: NodeValue = 75
            ):
        """
        기존 노드 삭제 시 트리 구조가 Right-Right 일 때 
        자동 균형 유지하는지 테스트. 
        기본 데이터 노드 수 4개와 각 노드의 자식 노드를 채운 상태에서 
        테스트를 진행한다. 
        """
        self.setData(new_data)
        print("testRemoveFullRR 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveFullLR(
            self,
            new_data: list[NodeValue] = [
                100, 110, 80, 105, 90, 75, 85, 95
            ],
            target_value: NodeValue = 105
            ):
        """
        기존 노드 삭제 시 트리 구조가 Left-Right 일 때 
        자동 균형 유지하는지 테스트. 
        기본 데이터 노드 수 4개와 각 노드의 자식 노드를 채운 상태에서 
        테스트를 진행한다. 
        """
        self.setData(new_data)
        print("testRemoveFullLR 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveFullRL(
            self,
            new_data: list[NodeValue] = [
                80, 75, 100, 70, 90, 105, 85, 95
            ],
            target_value: NodeValue = 75
            ):
        """
        기존 노드 삭제 시 트리 구조가 Right-Left 일 때 
        자동 균형 유지하는지 테스트. 
        기본 데이터 노드 수 4개와 각 노드의 자식 노드를 채운 상태에서 
        테스트를 진행한다. 
        """
        self.setData(new_data)
        print("testRemoveFullRL 테스트 메서드 실행 결과")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        printBinaryNodes(self.avl)

    def testRemoveAndBalanceMidLL(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 95, 70, 115, 83, 87, 81
            ],
            target_value: NodeValue = 87
            ):
        """
        노드가 제거되어 균형을 맞춰야 하는 세 노드들 중 최상위 노드가 포함되지 
        않은 경우의 테스트. 
        """
        self.setData(new_data)
        print("testRemoveAndBalanceMidLL 테스트 메서드 실행 결과")
        print("삭제 전 이진 트리 상황")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        print("삭제 후 이진 트리 상황")
        printBinaryNodes(self.avl)

    def testRemoveAndBalanceMidRR(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 95, 70, 115, 83, 87, 89
            ],
            target_value: NodeValue = 83
            ):
        """
        노드가 제거되어 균형을 맞춰야 하는 세 노드들 중 최상위 노드가 포함되지 
        않은 경우의 테스트. 
        """
        self.setData(new_data)
        print("testRemoveAndBalanceMidRR 테스트 메서드 실행 결과")
        print("삭제 전 이진 트리 상황")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        print("삭제 후 이진 트리 상황")
        printBinaryNodes(self.avl)

    def testRemoveAndBalanceMidLR(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 95, 70, 115, 87, 83, 84
            ],
            target_value: NodeValue = 87
            ):
        """
        노드가 제거되어 균형을 맞춰야 하는 세 노드들 중 최상위 노드가 포함되지 
        않은 경우의 테스트. 
        """
        self.setData(new_data)
        print("testRemoveAndBalanceMidLR 테스트 메서드 실행 결과")
        print("삭제 전 이진 트리 상황")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        print("삭제 후 이진 트리 상황")
        printBinaryNodes(self.avl)

    def testRemoveAndBalanceMidRL(
            self,
            new_data: list[NodeValue] = [
                90, 80, 100, 75, 110, 85, 95, 70, 115, 83, 87, 86
            ],
            target_value: NodeValue = 83
            ):
        """
        노드가 제거되어 균형을 맞춰야 하는 세 노드들 중 최상위 노드가 포함되지 
        않은 경우의 테스트. 
        """
        self.setData(new_data)
        print("testRemoveAndBalanceMidRL 테스트 메서드 실행 결과")
        print("삭제 전 이진 트리 상황")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        print("삭제 후 이진 트리 상황")
        printBinaryNodes(self.avl)

    def testRemoveAndSuccessiveBalancing(
        self,
        new_data: list[NodeValue] = [
            100, 80, 120, 60, 90, 110, 140, 40, 70, 85, 95, 115, 130, 
            160, 20, 50, 75, 87, 180, 10
        ],
        target_value: NodeValue = 100
        ):
        """
        이진 트리 중 노드 하나 제거 시 균형 조정이 연속으로 2번 일어나는 경우
        를 테스트. _removeMin() 메서드 내 균형 조정 기능과 _remove() 메서드 내 
        균형 조정 기능을 연속으로 사용하는 상황을 테스트.
        """
        self.setData(new_data)
        print("testRemoveAndSuccessiveBalancing 테스트 메서드 실행 결과")
        print("삭제 전 이진 트리 상황")
        printBinaryNodes(self.avl)
        self.avl.remove(target_value)
        print("삭제 후 이진 트리 상황")
        printBinaryNodes(self.avl)


def test_suites_binary_tree():
    test_data = [19, 14, 53, 3, 15, 26, 58, 29]
    bt_test = TestBinaryTree(test_data)
    printBinaryNodes(bt_test.getBinaryTree())

    # 테스트하고자 하는 메서드만 주석 해제하여 실행하면 됨.

    #bt_test.removeNothing()
    #bt_test.removeLeafNode()
    #bt_test.removeNodeWithoutLc()
    #bt_test.removeRootNode()
    #bt_test.removeNodeWithTwoChild(14)
    #bt_test.popNode()
    #bt_test.searchTest()
    #bt_test.getAllTest(GA.ASCDEPTH)
    bt_test.getAllTest(GA.ASCDEPTH)
    #bt_test.iterAscendingTestOnlyValue()
    #bt_test.iterAscendingTestWithNode()
    #bt_test.clearBT()

def test_suites_AVL_tree():
    avl_test = TestAVLTree()

    # 테스트하고자 하는 메서드만 주석 해제하여 실행하면 됨.

    #avl_test.testInsertUnitRR([10, 20, 40])
    #avl_test.testInsertUnitLL()
    #avl_test.testInsertUnitLR()
    #avl_test.testInsertUnitRL()
    #avl_test.testInsertFullLL()
    #avl_test.testInsertFullRR()
    #avl_test.testInsertFullLR()
    #avl_test.testInsertFullRL()
    #avl_test.testInsertGrandSubTreesRR()
    #avl_test.testInsertGrandSubTreesLL()
    #avl_test.testInsertGrandSubTreesLR()
    #avl_test.testInsertGrandSubTreesRL()
    #avl_test.testInsertAndBalanceMidLL()
    #avl_test.testInsertAndBalanceMidRR()
    #avl_test.testInsertAndBalanceMidLR()
    #avl_test.testInsertAndBalanceMidRL()
    #avl_test.testRemoveUnitLL()
    avl_test.testRemoveUnitRR()
    #avl_test.testRemoveUnitLR()
    #avl_test.testRemoveUnitRL()
    #avl_test.testRemoveFullLL()
    #avl_test.testRemoveFullLL(target_value=115)
    #avl_test.testRemoveFullRR()
    #avl_test.testRemoveFullLR()
    #avl_test.testRemoveFullRL()
    #avl_test.testRemoveAndBalanceMidLL()
    #avl_test.testRemoveAndBalanceMidRR()
    #avl_test.testRemoveAndBalanceMidLR()
    #avl_test.testRemoveAndBalanceMidRL()
    #avl_test.testRemoveAndSuccessiveBalancing()
    

if __name__ == '__main__':
    # 테스트하고자 하는 메서드만 주석 해제하여 실행하면 됨.

    test_suites_binary_tree()
    #test_suites_AVL_tree()
    pass