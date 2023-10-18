from sub_modules.my_queue import DynamicQueue

# type alias
Array = list
Index = int

def insert_element_binary_search(array: Array, insert_element: int) -> (Array):
    """
    기존 배열에 insert_element로 입력된 숫자를 오름차순에 맞게 
    적절한 위치에 삽입한다. 
    기존 배열은 이미 오름차순으로 정렬되어 있어야 한다.
    반환값으로 삽입이 완료된 배열을 반환한다.
    """
    N = len(array)
    target_idx = None # 삽입할 인덱스
    low_idx = 0
    high_idx = N - 1

    # 삽입할 인덱스 찾기
    while low_idx <= high_idx:
        mid_idx = (low_idx + high_idx) // 2
        if low_idx == mid_idx:
            if insert_element > array[mid_idx]:
                target_idx = mid_idx + 1
            else:
                target_idx = mid_idx
            break

        if insert_element < array[mid_idx]:
            high_idx = mid_idx - 1
        elif insert_element > array[mid_idx]:
            low_idx = mid_idx + 1
        elif insert_element == array[mid_idx]:
            target_idx = mid_idx
            break

    # 삽입하기
    array = array[:target_idx] + [insert_element] + array[target_idx:]
    return array

def reverse_sorted_array(array: Array) -> (Array):
    """
    이미 오름차순 또는 내림차순으로 정렬된 배열의 정렬 순서를 
    거꾸로 만듦. 예) 오름차순 -> 내림차순
    """
    N = len(array)
    mid = (N - 1) // 2
    for i in range(mid + 1):
        j = (N - 1) - i
        array[i], array[j] = array[j], array[i]
    return array

def selection_sort(array: Array) -> (Array):
    N = len(array)
    for i in range(N-1):
        min_idx = i
        for j in range(i+1, N):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
    return array

def insertion_sort(array: Array) -> (Array):
    N = len(array)
    for i in range(1, N):
        for j in range(i, 0, -1):
            if array[j-1] <= array[j]: break
            array[j], array[j-1] = array[j-1], array[j]
    return array

def binary_insertion_sort(array: Array) -> (Array):
    N = len(array)
    sub_array = [array[0]]
    for i in range(1, N):
        sub_array = insert_element_binary_search(sub_array, array[i])
    return sub_array

def merge_sort(array: Array) -> (Array):
    N = len(array)

    def recursive_sort(low_idx: int, high_idx: int) -> (None):
        if low_idx >= high_idx: return
        mid_idx = (low_idx + high_idx) // 2
        recursive_sort(low_idx, mid_idx)
        recursive_sort(mid_idx + 1, high_idx)
        merge(low_idx, mid_idx, high_idx)

    def merge(low_idx: Index, mid_idx: Index, high_idx: Index) -> (None):
        l_sub_array = array[low_idx:mid_idx+1]
        r_sub_array = array[mid_idx+1:high_idx+1]
        lp = low_idx
        rp = mid_idx + 1
        for i in range(low_idx, high_idx+1):
            if l_sub_array == []:
                # 왼쪽 부분 배열이 합병 배열에 모두 들어간 경우.
                # 남은 오른쪽 부분 배열을 합병 배열에 모두 넣는다.
                array[i] = r_sub_array[0]
                del r_sub_array[0]
            elif r_sub_array == []:
                # 오른쪽 부분 배열이 합병 배열에 모두 들어간 경우.
                # 남은 왼쪽 부분 배열을 합병 배열에 모두 넣는다. 
                array[i] = l_sub_array[0]
                del l_sub_array[0]
            elif l_sub_array >= r_sub_array:
                array[i] = r_sub_array[0]
                del r_sub_array[0]
            else:
                array[i] = l_sub_array[0]
                del l_sub_array[0]

    recursive_sort(0, N-1)
    return array

def quick_sort(array: Array) -> (Array):
    import random

    def recursive_qsort(low_idx: Index, high_idx: Index) -> (None):
        if low_idx >= high_idx: return
        
        init_pivot_idx = random.randint(low_idx, high_idx)
        #init_pivot_idx = low_idx
        final_pivot_idx = partition(low_idx, high_idx, init_pivot_idx)
        recursive_qsort(low_idx, final_pivot_idx-1)
        recursive_qsort(final_pivot_idx+1, high_idx)

    def partition(low_idx: Index, high_idx: Index, p_idx: Index) -> (Index):
        """
        피벗값을 기준으로 피벗값보다 작은 값들은 피벗값의 왼쪽으로,
        더 큰 값들은 오른쪽으로 몰아넣는다. 
        반환값은 피벗값의 최종 위치 인덱스이다.
        """
        def swap(i: Index, j: Index) -> (None):
            """
            주어진 두 인덱스의 데이터를 서로 바꾼다. 
            """
            array[i], array[j] = array[j], array[i]
        
        if low_idx != p_idx: 
            swap(low_idx, p_idx)
            p_idx = low_idx

        iter_idx = p_idx + 1
        while iter_idx <= high_idx:
            if array[p_idx] > array[iter_idx]:
                swap(p_idx+1, iter_idx)
                swap(p_idx, p_idx+1)
                p_idx += 1
            iter_idx += 1
        return p_idx

    recursive_qsort(0, len(array)-1)
    return array

def heap_sort(array: Array) -> (Array):
    """
    최대 이진 힙 (Max Binary Heap)을 이용하여 숫자가 들어간 배열을 정렬.
    """
    N = len(array)

    def swap(i: Index, j: Index) -> (None): array[i], array[j] = array[j], array[i]
    def is_less(i: Index, j: Index) -> (bool): return array[i] < array[j]

    def get_parent_idx(child_idx: Index) -> (Index):
        """
        최대 이진 힙의 자식 데이터의 부모 데이터 인덱스 반환.
        """
        return ((child_idx-1) // 2)
    
    def get_child_idx(parent_idx: Index, heap_end_idx: Index) \
        -> (tuple[Index | None, Index | None]):
        """
        최대 이진 힙에서 부모 데이터의 두 자식 데이터 인덱스 반환. 
        자식 데이터가 존재하지 않으면 None으로 반환.
        """
        lchild_idx = parent_idx * 2 + 1
        rchild_idx = parent_idx * 2 + 2
        if lchild_idx > heap_end_idx: lchild_idx = None
        if rchild_idx > heap_end_idx: rchild_idx = None
        return (lchild_idx, rchild_idx)
    
    def go_up(child_idx: Index) -> (None):
        """
        힙 내 새 데이터 삽입 시 힙 재구성.
        """
        parent_idx = get_parent_idx(child_idx)
        while parent_idx >= 0:
            if is_less(parent_idx, child_idx):
                swap(parent_idx, child_idx)
                child_idx = parent_idx
            else: break
            parent_idx = get_parent_idx(child_idx)

    def go_down(heap_end_idx: Index) -> (None):
        """
        힙 내 최대값 추출 시 힙 재구성.
        """
        target_idx = 0
        lc_idx, rc_idx = get_child_idx(target_idx, heap_end_idx)
        while lc_idx or rc_idx:
            if rc_idx is None:
                if is_less(target_idx, lc_idx):
                    swap(target_idx, lc_idx)
                    target_idx = lc_idx
                break
                
            if is_less(target_idx, lc_idx) or is_less(target_idx, lc_idx):
                if is_less(lc_idx, rc_idx): 
                    swap(target_idx, rc_idx)
                    target_idx = rc_idx
                else: 
                    swap(target_idx, lc_idx)
                    target_idx = lc_idx
                lc_idx, rc_idx = get_child_idx(target_idx, heap_end_idx)
            else: break

    def make_max_binary_heap():
        heap_end_idx = 0
        while heap_end_idx < N:
            go_up(heap_end_idx)
            heap_end_idx += 1

    def hsort(heap_end_idx: Index):
        if heap_end_idx == 0: return
        swap(0, heap_end_idx)
        go_down(heap_end_idx-1)
        hsort(heap_end_idx-1)

    make_max_binary_heap()
    hsort(N-1)
    return array

def tim_sort(array: Array) -> (Array):
    """
    구현 원리는 다음 사이트에 언급된 내용들을 최대한 구현하려고 하였음. 
    https://d2.naver.com/helloworld/0315536
    """
    # 미완성

    N = len(array)
    if N < 32: return binary_insertion_sort(array)
    
    def decide_minrun_size() -> (tuple[int, int]):
        """
        총 run의 개수가 2의 제곱수가 되도록 하는 
        minrun 사이즈를 결정하여 이를 반환. 
        반환값) (minrun의 크기, 총 minrun의 개수)
        """
        decided_minrun_size = 0
        for minrun_size in range(32, 64+1):
            if N < minrun_size: break
            total_minruns = divmod(N, minrun_size)
            if total_minruns[1] != 0: total_minruns[0] += 1
            if total_minruns[0] & (total_minruns[0] - 1) == 0:
                # 해당 수가 2의 거듭제곱일 경우.
                decided_minrun_size = total_minruns[0]
                return decided_minrun_size, total_minruns[0]

    class RunInfo():
        def __init__(
                self, 
                run_start_idx: Index = None, 
                run_end_idx: Index = None, 
                ):
            self.run_start_idx = run_start_idx
            self.run_end_idx = run_end_idx
            self.run_size = self.run_end_idx - self.run_start_idx
    

    def galloping_mode():
        ...

    def merge(runA: RunInfo, runB: RunInfo) -> (None):
        if runA.run_size > runB.run_size:
            copied_list = array[runB.run_start_idx:runB.run_end_idx+1]
            runA_i = runA.run_end_idx
            runB_i = runB.run_end_idx
            for i in range(runB.run_end_idx, runA.run_start_idx-1, -1):
                if runA_i < runA.run_start_idx:
                    array[i] = copied_list.pop()
                elif len(copied_list) == 0:
                    array[i] = array[runA_i]
                    runA_i -= 1
                elif array[runA_i] >= copied_list[-1]:
                    array[i] = array[runA_i]
                    runA_i -= 1
                else: array[i] = copied_list.pop()
        else:
            copied_list = array[runA.run_start_idx:runA.run_end_idx+1]
            runA_i = runA.run_start_idx
            runB_i = runB.run_start_idx
            for i in range(runA.run_start_idx, runB.run_end_idx+1):
                if len(copied_list) == 0:
                    array[i] = array[runB_i]
                    runB_i += 1
                elif runB_i > runB.run_end_idx:
                    array[i] = copied_list[0]
                    del copied_list[0]
                elif copied_list[0] < array[runB_i]:
                    array[i] = copied_list[0]
                    del copied_list[0]
                else:
                    array[i] = array[runB_i]
                    runB_i += 1

    # 배열을 run들로 나누고 하나의 run의 크기를 최대로 확장한 후,
    # 각 run에 삽입 정렬 실시.
    mr, total_num_of_runs = decide_minrun_size()
    run_start_idx = 0
    run_end_idx = mr - 1
    is_ascending = True
    run_idx_info = DynamicQueue(total_num_of_runs)  # list[RunInfo]
    while True:
        if run_end_idx > N - 1:
            if run_start_idx <= N - 1: run_end_idx = N - 1
            else: break
        array = binary_insertion_sort(array[run_start_idx:run_end_idx+1])
        if array[run_start_idx] > array[run_end_idx]:
            array = reverse_sorted_array(array[run_start_idx:run_end_idx+1])
            is_ascending = False
        else: is_ascending = True
        while True:
            # run 확장시키기.
            if is_ascending:
                if array[run_end_idx] <= array[run_end_idx+1]:
                    run_end_idx += 1
                else: break
            else:
                if array[run_end_idx] > array[run_end_idx+1]:
                    run_end_idx += 1
                else: 
                    array = reverse_sorted_array(array[run_start_idx:run_end_idx+1])
                    break
        run_inst = RunInfo(run_start_idx, run_end_idx)
        run_idx_info.enqueue(run_inst)
        run_start_idx = run_end_idx + 1
        run_end_idx = run_start_idx + mr - 1

    # run들을 하나로 병합하기. 인접한 run들의 크기를 고려한다.
    while True:
        run_num = run_idx_info.getCurrentSize()
        if run_num == 1: break
        if run_num == 2:
            runA = run_idx_info.dequeue()
            runB  = run_idx_info.dequeue()
            merge(runA, runB)
            break
        else:
            three_runs: list[RunInfo] = [run_idx_info.dequeue() for i in range(3)]

            def find_run_with_size(runs: list[RunInfo]) -> (RunInfo):
                largest_run = runs.pop()
                for run in runs:
                    if largest_run.run_size < run.run_size:
                        largest_run = run
                return largest_run
            
            largest_run = find_run_with_size(three_runs)
            second_run = find_run_with_size(three_runs)
            smallest_run = three_runs.pop()
            if smallest_run.run_size + second_run.run_size > largest_run.run_size:
                ...

    return array

if __name__ == '__main__':
    test_data = [12, 5, 4, 8, 3, 9, 1, 10]
    expected_result = [1, 3, 4, 5, 8, 9, 10, 12]

    selection_result = selection_sort(test_data.copy())
    print(f"selection_result: {selection_result}, {selection_result == expected_result}")

    insertion_result = insertion_sort(test_data.copy())
    print(f"insertion_result: {insertion_result}, {insertion_result == expected_result}")

    binary_insert_result = binary_insertion_sort(test_data.copy())
    print(f"binary_insertion_result: {binary_insert_result}, " + \
          f"{binary_insert_result == expected_result}")

    merge_result = merge_sort(test_data.copy())
    print(f"merge_result: {merge_result}, {merge_result == expected_result}")

    quick_result = quick_sort(test_data.copy())
    print(f"quick_result: {quick_result}, {quick_result == expected_result}")

    heap_result = heap_sort(test_data.copy())
    print(f"heap_result: {heap_result}, {heap_result == expected_result}")

    python_result = sorted(test_data)
    print(f"python_sorted_result: {python_result}, {python_result == expected_result}")

    reverse_expected = sorted(test_data, reverse=True)
    reverse_result = reverse_sorted_array(python_result)
    print(f"reversed_result: {reverse_result}, {reverse_result == reverse_expected}")

    print(f"Original array: {test_data}")
