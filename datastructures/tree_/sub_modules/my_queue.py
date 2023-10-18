from typing import Any


class StaticQueue():
    """큐의 왼쪽에서 데이터 삽입, 오른쪽에서 데이터 추출 가능한 구조."""
    def __init__(self, limit_size: int = 10):
        self.en_stack = []
        self.de_stack = []
        self.limit_size = limit_size  # queue가 담을 수 있는 총 아이템 수 지정.

    def _transfer(self):
        while self.en_stack:
            self.de_stack.append(self.en_stack.pop())

    def isEmpty(self) -> bool:
        return self.en_stack == [] and self.de_stack == []
    
    def getCurrentSize(self) -> int:
        return len(self.en_stack) + len(self.de_stack)
    
    def enqueue(self, item):
        cur_size = self.getCurrentSize()
        if cur_size != self.limit_size:
            self.en_stack.append(item)
        else:
            print("큐에 데이터가 꽉 차서 더 이상 삽입할 수 없습니다.")

    def dequeue(self) -> Any | None:
        if not self.de_stack:
            self._transfer()
        try:
            return self.de_stack.pop()
        except IndexError:
            print("큐가 비어서 출력할 데이터가 없습니다.")
            return
        
    def seek_peek(self) -> Any | None:
        if not self.de_stack:
            if self.en_stack:
                return self.en_stack[0]
            else:
                return
        return self.de_stack[-1]
    
    def clear(self) -> None:
        """
        큐를 비운다.
        """
        self.en_stack.clear()
        self.de_stack.clear()
    
    def __repr__(self):
        if self.en_stack == [] and self.de_stack == []:
            return repr([])
        
        self.total_queue = []  # self.en_queue + self.de_queue
        temp_stack = []
        if self.en_stack:
            temp_stack = self.en_stack.copy()
            while temp_stack:
                self.total_queue.append(temp_stack.pop())
        if self.de_stack:
            self.total_queue.extend(self.de_stack)
        return repr(self.total_queue)
    

class DynamicQueue(StaticQueue):
    """
    크기 제한없이 동적으로 데이터를 enqueue및 dequeue할 수 있는 동적 큐.
    """
    def __init__(self) -> None:
        self.en_stack = []
        self.de_stack = []

    def enqueue(self, item: any) -> None:
        self.en_stack.append(item)


def test_static_queue():
    q = StaticQueue()
    data = ['a', 'b', 'c', 'd']
    print("현재 큐는 비어있나요? ", q.isEmpty())
    print("큐에 데이터 삽입.")
    for item in data:
        q.enqueue(item)
    print("현재 큐는 비어있나요? ", q.isEmpty())
    print("최신 데이터: ", q.dequeue())
    print("현재 큐에서 제일 먼저 출력될 아이템: ", q.seek_peek())
    print("현재 큐에 존재하는 총 아이템 개수: ", q.getCurrentSize())
    print(q)
        

if __name__ == '__main__':
    test_static_queue()
