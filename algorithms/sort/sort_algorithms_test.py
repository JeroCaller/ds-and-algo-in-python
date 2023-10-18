from timeit import timeit
from random import randint
from collections import defaultdict
from typing import Callable
import sort_algorithms as soal

# type alias
TimeResult = float  # 시간 측정 결과
FunctionName = str
Function = Callable[[soal.Array], soal.Array]
N_ = int
TimeResultSet = defaultdict[FunctionName, list[tuple[N_, TimeResult]]]

# [
#     [N_, TimeResult1, TimeResult2, ...],
#     [N_, TimeResult1, TimeResult2, ...],
#     ...
# ]
TableForPrint = list[tuple[N_, TimeResult]]

def geometric_sequence(
            base: int, 
            x_range: tuple[int] = (1, 2),
            x_interval: int = 1
            ) -> (list[int]):
        """
        a^x 수열 반환. 
        예) 2^x, min_x: 1, max_x: 5 
        -> (2^1, 2^2, 2^3, 2^4, 2^5)
        >>> geometric_sequence(2, 1, 5)
        >>> (2, 4, 8, 16, 32)
        """
        min_x, max_x = x_range
        return [pow(base, x) for x in range(min_x, max_x+1, x_interval)]


class TestKit():
    def __init__(
            self,
            N_list: list[int],
            number: int = 100,
            setup_module: str = "sort_algorithms",
            funcs: list[Function] = [None],
            round_digit: int = 4
            ):
        """
        매개변수) \n
        N_list: 테스트에 쓰일 입력값들의 크기 리스트. \n
        number: timeit() 함수의 number 매개변수에 대입할 수. \n
        setup_module: timeit() 함수의 setup 매개변수에 대입할 모듈명의 문자열. \n
        funcs: 시간 테스트할 함수들의 이름들을 리스트 안에 담는다. \n
        round_digit: 측정된 시간을 표시할 소수점 자리수.
        """
        self.N_list = N_list
        self.funcs = funcs
        self.number = number
        self.setup_module = setup_module
        self.round_digit = round_digit

        self.test_array_set = self.generate_test_dataset()
        self.time_results = self.time_test()

    def generate_test_dataset(self) -> (list[list[int]]):
        """
        테스트에 쓰일 배열 생성. 배열 내 숫자는 무작위로 정한다. \n
        예) N_list = [1, 2, 4, 8] 
        -> 반환값: [[x], [x, x], [x, x, x, x], [x, x, x, x, x, x, x, x]]
        """
        all_dataset = []
        for N in self.N_list:
            one_array = []
            for n in range(N):
                one_array.append(randint(0, n))
            all_dataset.append(one_array)
        return all_dataset
    
    def time_test(self) -> (TimeResultSet):
        """
        입력값(리스트)의 크기에 따른 함수들의 실행 시간 동시 측정. \n
        """
        time_result: TimeResultSet = defaultdict(list)
        for func in self.funcs:
            func_name = func.__name__
            for one_array in self.test_array_set:
                N = len(one_array)
                stmt = f"{func_name}({one_array})"
                time = round(timeit(
                    stmt=stmt, 
                    number=self.number, 
                    setup=f"from {self.setup_module} import {func_name}"), 
                    self.round_digit
                    )
                time_result[func_name].append((N, time))
        return time_result

    def print_time_test(
            self, 
            get_result: bool = False
            ) -> (tuple[TimeResult, TableForPrint] | None):
        """
        time_result() 함수 반환값 출력. \n
        매개변수) \n
        get_result: True -> 시간 측정 데이터 반환. 
        False -> 출력만 하고 아무것도 반환시키지 않음.
        """
        field_names = ["N"]
        field_names.extend(list(self.time_results.keys()))

        # 출력을 위해 데이터 위치 재구성
        rows: TableForPrint = []
        all_data = self.time_results.values()
        row_idx = 0
        can_escape = False
        while True:
            row = []
            for i, one_func in enumerate(all_data):
                if row_idx == len(one_func):
                    can_escape = True
                    break
                if i == 0: row.append(one_func[row_idx][0])
                row.append(one_func[row_idx][1])
            rows.append(tuple(row))
            if can_escape: break
            row_idx += 1

        # field print
        white_space_repeat = 4
        for f_name in field_names:
            print(f"{f_name}", end=" " * white_space_repeat)
        print()
        
        N_str_sizes = []
        for row in rows:
            for n in row:
                N_str_sizes.append(len(str(n)))
                break
        max_str_size = max(N_str_sizes)

        # data print
        for i, dataset in enumerate(rows):
            for j, data in enumerate(dataset):
                if j == 0:
                    end_num = white_space_repeat + max_str_size - len(str(data))
                    print(f"{data:<}", end=' ' * end_num)
                else:
                    print(f"{data:<0{self.round_digit}}", end=' ' * white_space_repeat)
            print()
        
        if get_result:
            return (self.time_results, rows)
        else:
            return


if __name__ == '__main__':
    test_funcs = [
        soal.selection_sort,
        soal.insertion_sort,
        soal.binary_insertion_sort,
        soal.merge_sort,
        soal.quick_sort,
        soal.heap_sort,
    ]

    Ns = geometric_sequence(2, (1, 9))
    testkit = TestKit(N_list=Ns, funcs=test_funcs)
    testkit.print_time_test()
