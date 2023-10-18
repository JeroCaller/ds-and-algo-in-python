from typing import Any


class StaticStack():
    def __init__(self, size_: int):
        """
        스택의 크기를 고정시킨 스택.

        size_ : 스택 최대 크기 설정.
        """
        self.stack: list = []
        self.size_: int = size_

    def is_empty(self) -> (bool):
        return self.stack == []

    def push(self, one_element) -> (bool):
        """
        맨 끝에 요소 삽입. 
        정해진 size_만큼만 삽입할 수 있다.\n
        return type)\n
        True: 삽입 성공.\n
        False: 삽입 실패.\n
        """
        if self.getLength() == self.size_:
            print("스택의 최대 크기에 도달하여 요소를 추가할 수 없습니다.")
            return False
        self.stack.append(one_element)
        return True

    def pop(self) -> (Any | None):
        """
        맨 끝 요소 추출 후 스택에서 제거.
        """
        try:
            return self.stack.pop()
        except IndexError:
            print("스택이 비어있어 반환할 아이템이 없습니다.")
            return
        
    def peek(self):
        """
        맨 끝 요소 조회. 
        """
        return self.stack[-1]
    
    def getLength(self) -> (int):
        """
        현재 스택에 들어있는 요소들의 수 반환.
        """
        return len(self.stack)
    
    def setNewSize(self, new_size: int):
        """
        스택의 최대 크기 재설정. 
        현재 스택에 들어있는 요소들의 수보다 더 작게 설정하지 못하도록 함.
        """
        if new_size < self.getLength():
            print("스택 내 항목들의 수보다 더 작게 설정할 수 없습니다.")
            print(f"현재 스택 내 항목들의 수: {self.getLength()}")
            return
        self.size_ = new_size

    def clear(self):
        """
        스택을 모두 비운다.
        """
        self.stack.clear()
    
    def __repr__(self):
        return repr(self.stack)
    

class DynamicStack(StaticStack):
    def __init__(self):
        """
        크기에 제한을 두지 않고 무한정 크기를 동적으로 늘릴 수 있는 스택.
        """
        self.stack: list = []

    def push(self, one_element):
        """
        맨 끝에 요소 삽입. 
        """
        self.stack.append(one_element)

    def setNewSize(self):
        """
        DynamicStack에서는 사용하지 않는 메서드. 
        """
        pass


def test_static_stack():
    stack = StaticStack(10)
    data = ["초록색", "분홍색", "노란색", '하늘색', '흰색']
    print("멘토스를 준비합니다.")
    for item in data:
        stack.push(item)
    print(f"멘토스 준비 완료. 상태: {stack}")
    print(f"현재 멘토스 양: {stack.getLength()}")
    print(f"맨 마지막에 있는 멘토스의 색은? {stack.peek()}")
    one_item = stack.pop()
    print(f"맨 마지막에 있는 {one_item} 멘토스를 꺼내 먹었다.")
    print(f"맨 마지막에 있는 멘토스의 색은? {stack.peek()}")
    print(f"멘토스 다 먹었나? {stack.is_empty()}")
    print(stack)
    
    
if __name__ == '__main__':
    test_static_stack()
    