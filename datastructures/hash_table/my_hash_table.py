from sub_modules.linked_list_kv import LinkedList

# type alias
Key = object
Value = object
Item = tuple[Key, Value]

class HashTable():
    """
    해시 함수: digit folding과 division method 방식 사용.\n
    해시 충돌 해결법: chaining 방식 사용.
    """
    def __init__(self, size: int) -> (None):
        """
        매개변수 설명)\n
        size: 해시테이블 크기. (총 버킷 수)
        """
        self.size = size
        self.buckets: list[LinkedList] = []
        self.load_factor = 0.75  # 부하율
        self.threshold = self.size * self.load_factor
        self.__createHashTable()

    def getAllData(self) -> (list[tuple]):
        """
        해시 테이블 내 모든 데이터 반환.
        반환 형태: [(key, value), (key, value), ...]
        """
        all_data = []
        for ll in self.buckets:
            all_data.extend(ll.items())
        return all_data

    def __createHashTable(self) -> (None):
        """
        해시테이블 생성.\n
        각 버킷마다 빈 연결 리스트를 생성한다.
        """
        for i in range(self.size):
            self.buckets.append(LinkedList())

    def hashKey(self, key) -> (int):
        """
        키의 해싱값 (숫자) 반환. 
        키가 문자열일 경우로 상정하고 실행.
        만약 키가 문자열이 아닌 int, float 같은 경우,
        문자열로 형 변환 시킨다.
        """
        if type(key) != str:
            key = str(key)

        unicode_value_total = 0
        for one_char in key:
            unicode_value_total += ord(one_char)
        
        hash_value = unicode_value_total % self.size
        return hash_value

    def addData(self, new_data: tuple) -> (None):
        """
        해시 테이블에 새 키-값 데이터 삽입.\n
        만약 기존의 키에 연결된 값을 바꾸기 위해 
        기존 키를 입력한 경우, 해당 버킷의 값만 바꾼다.
        new_data: (key, value)
        """
        key, value = new_data
        index = self.hashKey(key)
        target_linked_list = self.buckets[index]
        target_linked_list.addNodeBack(key, value)

        # 해시 테이블 크기 자동 재조정
        self.autoResize()

    def addDataAll(self, new_dataset: list[Item]) -> (None):
        """
        여러 데이터들을 한꺼번에 해시 테이블에 삽입한다.\n
        """
        for kv in new_dataset:
            self.addData(kv)

    def removeData(self, target_key: Key) -> (None):
        """
        지정된 키와 일치하는 키-값 데이터 삭제.
        """
        index = self.hashKey(target_key)
        target_ll = self.buckets[index]
        target_ll.deleteNodeByKey(target_key)

    def findData(self, key: Key) -> (Value):
        """
        주어진 key에 대응되는 값을 반환.
        """
        index = self.hashKey(key)
        target_linked_list = self.buckets[index]
        return target_linked_list.getValueByKey(key)
    
    def getLength(self) -> (int):
        """
        현재 저장된 데이터 수 반환. 
        해시테이블의 전체 크기를 반환하는 것이 아니라, 
        빈 버킷은 제외하고 기존 데이터의 수만 계산하여 반환. 
        """
        all_data = self.getAllData()
        return len(all_data)
    
    def getHTSize(self) -> (int):
        """
        현재 해시테이블의 크기 반환.
        """
        self.size = len(self.buckets)
        return self.size

    def printCurrentHT(self) -> (None):
        """
        현재 해시테이블에 저장된 데이터 구조 출력.
        해시 충돌로 인해 한 버킷에 여러 노드가 연결되어 있는 상태도
        보여줘야 함.
        """
        for i, ll in enumerate(self.buckets):
            print(f"index: {i}, in a bucket: {ll}")

    def clear(self) -> (None):
        """
        해시 테이블을 모두 비운다.
        즉, 모든 데이터를 지운다.
        """
        for ll in self.buckets:
            ll.clear()
        
    def autoResize(self) -> (None):
        """
        해시 테이블의 크기를 재조정함.
        """
        current_data_len = self.getLength()
        if self.threshold > current_data_len:
            # 저장된 데이터의 수가 해시 테이블의 전체 크기 대비
            # 부하율을 넘지 않은 경우, 아무런 작업도 하지 않음.
            return
        
        new_size = 2 * self.getHTSize() + 1
        self.size = new_size
        new_table = [LinkedList() for i in range(new_size)]
        for key, value in self.getAllData():
            new_index = self.hashKey(key)
            target_ll = new_table[new_index]
            target_ll.addNodeBack((key, value))
        self.buckets = new_table
        self.threshold = self.size * self.load_factor
        
    def checkHashCollision(self) -> (tuple[bool, int, int]):
        """
        현재 해시 테이블에 해시 충돌이 일어났는지 확인. 
        한 버킷의 연결리스트의 노드가 둘 이상일 경우 해시 충돌이 일어난 것임. 
        현재 해시 테이블에서 한 버킷이 최대로 가지는 노드 수도 같이 반환.\n
        return type)\n
        (bool, col_depth, no_buckets) 
        -> (해시 충돌 여부, 버킷 당 최대 연결리스트 길이, 해시 충돌난 버킷의 수)
        """
        depth_of_buckets = []
        is_collision = False
        for ll in self.buckets:
            ll_length = ll.getLength()
            if ll_length > 1:
                is_collision = True
            depth_of_buckets.append(ll_length)
        no_buckets = 0
        no_buckets = sum(map(lambda x: 1 if x > 1 else 0, depth_of_buckets))
        return (is_collision, max(depth_of_buckets), no_buckets)


# 출력 테스트 모음
def print_borderline(func: callable):
    def wrapper(*args, **kwargs):
        print("=============================")
        result = func(*args, **kwargs)
        print("=============================")
        return result
    return wrapper

@print_borderline
def print_hashtable_test(dataset: list[tuple], size: int):
    ht = HashTable(size)
    ht.addDataAll(dataset)
    ht.printCurrentHT()
    print(ht.checkHashCollision())
    print(ht.getHTSize())

@print_borderline
def print_hashtable_with_bigger_size_test(
        old_dataset: list[tuple],
        old_size: int,
        new_dataset: list[tuple]
        ):
    ht = HashTable(old_size)
    ht.addDataAll(old_dataset)
    ht.printCurrentHT()
    print(f"현재 해시테이블 크기: {ht.getHTSize()}")
    print(f"현재 저장된 데이터 수: {ht.getLength()}")
    print("===========")

    ht.addDataAll(new_dataset)
    ht.printCurrentHT()
    print(f"현재 해시테이블 크기: {ht.getHTSize()}")
    print(f"현재 저장된 데이터 수: {ht.getLength()}")
    

if __name__ == '__main__':
    dataset = [
        ("사과", "apple"),
        ("바나나", "banana"),
        ("딸기", "strawberry"),
        ("오렌지", "orange"),
        ("포도", "grape"),
        ("꽃", "flower"),
        ("나무", "tree"),
        ("바다", "sea"),
        ("별", "star"),
        ("햇님", "sun")
    ]
    # 원하는 테스트 코드의 주석만 해제하여 실행.
    #print_hashtable_test(dataset, 10)
    #print_hashtable_test(dataset, 23)
    #print_hashtable_test(dataset, 47)
    #print_hashtable_test(dataset, 64)
    #print_hashtable_test(dataset, 100) # 해시 충돌 없음.

    new_dataset = [
        ("코딩", "coding"),
        ("밤바다", "night sea"),
        ("공기", "air"),
        ("공깃밥", "rice"),
        ("디버그", "debug"),
        ("에너지", "energy"),
    ]
    print_hashtable_with_bigger_size_test(dataset, 2*len(dataset)+1, new_dataset)
