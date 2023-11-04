"""최대 이진 힙(Max Binary Heap)을 이용하여 우선순위 큐를 구현.

"""

from multipledispatch import dispatch

__all__ = [
    'Data',
    'PriorityQueue'
]

# type alias
Value = object
Priority = int


class Data():
    """(값, 우선순위) 쌍의 데이터 객체."""

    def __init__(self, value: any = None, priority: int = 0) -> (None):
        """
        Parameters
        ----------
        value : Any | None, default None
            데이터의 값. 
        priority : int, default 0
            데이터의 우선순위. 숫자가 높을 수록 최우선순위.

        """
        self.value: any = value
        self.priority: int = priority


class PriorityQueue():
    def __init__(self, max_mode: bool = True) -> (None):
        """우선순위 큐의 최대 크기를 고정시키지 않고, 
        데이터가 들어오는 대로 저장하는 동적 방식 사용. 

        Parameters
        ----------
        max_mode : bool, default True
            max binary heap으로 할 지에 대한 변수. 
            True시 max binary heap, 즉 priority의 값이 큰 데이터가 힙 구조의
            상위 계층에 위치하도록 함. (dequeue시 priority의 값이 가장 큰 데이터가 추출된다)
            False 시 min binary heap, 즉, priority 값이 작은 데이터가 
            힙 구조의 상위 계층에 위치하도록 함. (dequeue시 priority의 값이 가장 작은 데이터가 추출된다)

        Attributes
        ----------
        self.heap_array : list[Data], default [None]
            인덱스 계산 편의상 배열 내 데이터의 저장 위치는 
            1부터 시작함. 즉, 인덱스 0은 비워둠. 
        
        """
        self.heap_array: list[Data] = [None]
        self.N = len(self.heap_array) - 1
        self.max_mode = max_mode

    def __contains__(self, search: Value | Priority) -> (bool):
        """search가 우선순위 큐에 있는지 검사한 후, 존재하면 True, 
        그렇지 않으면 False 반환.
        """
        # 매개변수 search의 자료형이 int가 아니라면 해당 변수는
        # Value에 해당된다고 가정.
        if not isinstance(search, int):
            for data in self.heap_array[1:]:
                if search == data.value: return True
            return False
        else:
            for data in self.heap_array[1:]:
                if search == data.priority: return True
            return False

    def __repr__(self):
        if not self.isEmpty():
            return_data = []
            for data_obj in self.heap_array[1:]:
                return_data.append((data_obj.value, data_obj.priority))
            return str(return_data)
        return "None"

    def clear(self) -> (None):
        """우선순위 큐 내부를 모두 비운다."""
        del self.heap_array
        self.heap_array: list[Data] = [None]

    def showAll(self) -> (list[tuple[Value, Priority]]):
        """우선순위 큐 내 모든 데이터 반환."""
        all_data = []
        for data in self.heap_array[1:]:
            all_data.append((data.value, data.priority))
        return all_data

    def isEmpty(self) -> (bool):
        """현재 우선순위 큐가 비어있는지 확인. 
        비어있으면 True 반환.
        """
        return self.getCurrentSize() == 0

    def getCurrentSize(self) -> (int):
        """현재 힙 내에 저장된 데이터의 수 업데이트 및 반환."""
        self.N = len(self.heap_array) - 1
        return self.N

    def peek(self) -> (Data | None):
        """최우선순위 데이터를 반환. 
        검색만 하고 실제로 큐에서 제거하진 않는다. 
        """
        return self.heap_array[1] if not self.isEmpty() else None

    def __isLess(self, a: Data | None, b: Data | None) -> (bool | None):
        """a < b ?

        힙 내에 존재하는 두 데이터 간 우선순위의 대소를 비교 후, 
        a가 작으면 True, b가 작으면 False 반환. 
        만약 a, b 중 하나라도 None이면 None을 반환. 
        """
        if (a is None) or (b is None): return None
        return a.priority < b.priority

    def __switchData(self, a_index: int | None, b_index: int | None) -> (None):
        """
        힙 내에 두 데이터의 위치를 바꾼다. 
        바꾸고자 하는 두 데이터의 인덱스를 입력한다. 
        a, b 인덱스 매개변수 중 하나라도 None이면 아무런 작업을 수행하지 않음. 
        """
        if a_index is None or b_index is None: return
        self.heap_array[a_index], self.heap_array[b_index] = \
        self.heap_array[b_index], self.heap_array[a_index]

    def __getParent(self, child_index: int) -> (tuple[Data, int] | None):
        """
        힙 내의 특정 데이터의 부모 데이터 및 부모 데이터의 인덱스를 반환.
        부모 데이터가 존재하지 않으면 None을 반환.
        """
        parent_index = child_index // 2
        if parent_index >= 1:
            return (self.heap_array[parent_index], parent_index)
        return None

    def __getChild(self, parent_index: int) \
        -> (tuple[tuple[Data, int] | tuple[None, None], tuple[Data, int] | tuple[None, None]]):
        """
        힙 내의 특정 데이터의 두 자식 데이터를 반환. 
        자식 데이터가 존재하지 않으면 None을 반환. 
        """
        lchild_index = parent_index * 2
        rchild_index = parent_index * 2 + 1
        #if lchild_index <= self.N:
        if lchild_index <= self.getCurrentSize():
            lchild = (self.heap_array[lchild_index], lchild_index)
        else: lchild = (None, None)
        #if rchild_index <= self.N:
        if rchild_index <= self.getCurrentSize():
            rchild = (self.heap_array[rchild_index], rchild_index)
        else: rchild = (None, None)
        return (lchild, rchild)

    @dispatch(object, int)
    def enqueue(self, value: any, priority: int) -> (None):
        """새 데이터 입력. 

        Parameters
        ----------
        value : Any
            값. 
        priority : int
            우선순위 값.

        """
        self.__enqueue(Data(value, priority))

    @dispatch(tuple)
    def enqueue(self, value_priority: tuple[any, int]) -> (None):
        """새 데이터 입력.

        Parameters
        ----------
        value_priority : (value, priority)

        """
        self.__enqueue(Data(value_priority[0], value_priority[1]))

    def __enqueue(self, new_data: Data) -> (None):
        """새 데이터 입력. 
        
        Parameters
        ----------
        new_data
            Data(value, priority) 형태로 작성.
            반드시 Data 객체를 사용하여 값과 우선순위를 전달해야 함.
        
        """
        self.heap_array.append(new_data)

        # 힙 구조 재구성
        target_index = self.getCurrentSize()
        target_data = self.heap_array[target_index]
        parent = self.__getParent(target_index)
        while parent:
            parent_data, parent_index = parent
            if self.max_mode:
                condition = self.__isLess(parent_data, target_data)
            else:
                condition = self.__isLess(target_data, parent_data)
            if condition:
                self.__switchData(parent_index, target_index)
                target_index = parent_index
                target_data = self.heap_array[target_index]
                parent = self.__getParent(target_index)
            else: break  # 이미 경로 내 정렬이 모두 끝났으므로 작업 종료.

    def dequeue(self) -> (Data | None):
        """최우선순위 데이터 반환 후 우선순위 큐 내에서 삭제. 

        최대 이진 힙의 경우, 힙 구조 변경 시 두 자식 노드들 중 더 큰 
        우선순위 값을 가지는 자식 노드와 부모 노드의 위치를 바꾼다. 
        최소 이진 힙의 경우, 힙 구조 변경 시 두 자식 노드들 중 더 작은 
        우선순위 값을 가지는 자식 노드와 부모 노드의 위치를 바꾼다. 

        Returns
        -------
        Data
            Data 객체
        None
            큐 내에 데이터가 하나도 없을 때 반환됨. 
        
        """
        try:
            return_data = self.heap_array[1]
        except IndexError:
            print("우선순위 큐가 비어있어 추출할 데이터가 없습니다.")
            return None

        if self.getCurrentSize() <= 1:
            # 힙 구조에 딱 하나의 값만 존재하는 경우 (그리고 해당 값을 삭제하려는 경우),
            # 힙 구조를 재구성할 필요가 없다.
            del self.heap_array[-1]
            return return_data

        # 힙 구조 재구성
        self.__switchData(1, self.getCurrentSize())
        del self.heap_array[-1]
        target_index = 1
        target_data = self.heap_array[target_index]
        lchild, rchild = self.__getChild(target_index)
        while (lchild or rchild) != (None, None):
            lchild_data, lchild_index = lchild
            rchild_data, rchild_index = rchild
            if self.max_mode:
                condition1 = self.__isLess(target_data, lchild_data) or \
                self.__isLess(target_data, rchild_data)
            else:
                condition1 = self.__isLess(lchild_data, target_data) or \
                self.__isLess(rchild_data, target_data)
            condition2 = self.__isLess(lchild_data, rchild_data)

            if condition1:
                if condition2 is True:
                    if self.max_mode:
                        self.__switchData(target_index, rchild_index)
                        target_index = rchild_index
                    else:
                        self.__switchData(target_index, lchild_index)
                        target_index = lchild_index
                    target_data = self.heap_array[target_index]
                elif condition2 is False:
                    if self.max_mode:
                        self.__switchData(target_index, lchild_index)
                        target_index = lchild_index
                    else:
                        self.__switchData(target_index, rchild_index)
                        target_index = rchild_index
                    target_data = self.heap_array[target_index]
                else:
                    # if condition2 is None
                    if self.max_mode:
                        if rchild_data is None and self.__isLess(target_data, lchild_data):
                            self.__switchData(target_index, lchild_index)
                    else:
                        if rchild_data is None and self.__isLess(lchild_data, target_data):
                            self.__switchData(target_index, lchild_index)
                    target_index = lchild_index
                    target_data = self.heap_array[target_index]
                lchild, rchild = self.__getChild(target_index)
            else: break  # 이미 경로 내 정렬이 모두 끝났으므로 작업 종료.
        return return_data


def test_pq1():
    test_dataset = [
        ('고양이', 15),
        ('개', 13),
        ('고슴도치', 14),
        ('호랑이', 9),
        ('사자', 11),
        ('바다사자', 12),
        ('족제비', 14),
        ('수달', 8),
        ('뱀', 2),
        ('소', 1),
        ('펭귄', 10),
        ('북극곰', 8),
        ('곰', 6),
        ('원숭이', 9),
        ('침팬치', 7),
        ('고릴라', 4),
        ('기린', 5),
        ('치타', 12),
    ]
    #test_dataset = [('하마', -5), ('곰', -1)]

    pq = PriorityQueue()

    # enqueue 테스트
    for data in test_dataset:
        pq.enqueue(data)
    print(pq)
    print(f"Current size: {pq.getCurrentSize()}")

    pq.enqueue('독수리', 9)
    print(pq)
    print(f"Current size: {pq.getCurrentSize()}")

    # peek, dequeue 테스트
    print(f"Result of search for pq: {pq.peek().value, pq.peek().priority}")
    get_data = pq.dequeue()
    print(f"data is {get_data.value}, priority is {get_data.priority}")
    print(pq)
    print(f"Current size: {pq.getCurrentSize()}")

def test_pq2():
    test_data = [
        ('고양이', 13), ('개', 12), ('사자', 11), ('곰', 10), ('닭', 9)
    ]

    pq = PriorityQueue()
    for data in test_data: pq.enqueue(data)
    print(pq)
    pq.dequeue()
    print(pq)

def test_min_pq():
    test_data = [
        ('닭', 9), ('곰', 10), ('사자', 11), ('개', 12), ('고양이', 13)
    ]

    pq = PriorityQueue(max_mode=False)
    for data in test_data: pq.enqueue(data)
    print(pq)
    pq.dequeue()
    print(pq)

def test_pq_negative_p():
    test_data = [
        ('고양이', -12), ('사자', -13), ('치타', -11), ('곰', -4), ('바다사자', -7),
        ('개', -9), ('기린', -3),
    ]
    pq = PriorityQueue(False)
    for data in test_data: pq.enqueue(data)
    print(pq)
    pq.dequeue()
    print(pq)

if __name__ == '__main__':
    #test_pq1()
    #test_pq2()
    #test_min_pq()
    test_pq_negative_p()
    pass
