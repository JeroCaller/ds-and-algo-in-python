import sys
from dirimporttool import get_super_dir_directly

for i in range(1, 4):
    super_dir = get_super_dir_directly(__file__, i)
    sys.path.append(super_dir)
sys.path.append(super_dir)

from tree_.tree import PathTree
from tree_.tree import REMOVEALL, REMOVEONE, DONTREMOVE, ALPHABET, LENGTH

# 테스트 함수 매개변수 passed는 해당 테스트 함수의 테스트가 
# 통과되었는지 여부를 표시하는 인자이다. 
# 테스트 통과 시 True, 실패 시 False, 예외 발생 시 None을 대입.

def test_appendAll_and_tree_structure(passed: bool | None):
    """
    data)
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ └ g
      │   └ h
      └ i
        ├ c
        │ ├ j
        │ └ k
        └ l
          └ m
            └ n
    """
    data = [
            'a.b.c.d.e', 'a.b.c.d.f', 'a.b.c.g.h', 'a.b.i.c.j', 
            'a.b.i.c.k', 'a.b.i.l.m.n'
    ]
    ptree = PathTree(always_raise_error=True)
    ptree.appendAll(data)
    print(ptree.getTreeStructure())
    print("-" * 30)
    print(ptree.getAllLeafAbs())

def test_appendAll_several_times(passed: bool | None):
    """
    a
    └ b
      └ c
        └ d
          ├ e
          └ f
    =>
    a
    └ b
      └ c
        ├ d
        │ ├ e
        │ └ f
        └ g
          └ h
    =>
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ └ g
      │   └ h
      └ i
        └ c
          ├ j
          └ k
    =>
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ └ g
      │   └ h
      └ i
        ├ c
        │ ├ j
        │ └ k
        └ l
          └ m
            └ n
    """
    ptree = PathTree(always_raise_error=True)
    data1 = ['a.b.c.d.e', 'a.b.c.d.f']
    data2 = ['a.b.c.g.h']
    data3 = ['a.b.i.c.j', 'a.b.i.c.k']
    data4 = ['a.b.i.l.m.n']
    all_data = [data1, data2, data3, data4]
    
    def append_and_print(data):
        ptree.appendAll(data)
        print(ptree.getTreeStructure())
        print('-----')
        print(ptree.lenTree())
        print(ptree.getAllLeafAbs())
        print("="*50)

    for d in all_data:
        append_and_print(d)

def test_append_and_tree_structure(passed: bool | None):
    """
    root
    ├ a
    │ └ c
    ├ b
    │ └ b
    └ d
    """
    ptree = PathTree(default_root=True, always_raise_error=True)
    ptree.append('a', 'root')
    ptree.append('c', 'a')
    ptree.append('b', 'root')
    ptree.append('b', 'b')
    ptree.append('d', 'root')
    print(ptree.getTreeStructure())
    print("-" * 30)
    print(ptree.getAllLeafAbs())

def test_replace_simple(passed: bool | None):
    """
    a
    └ b
    ->
    a
    └ c
    ->
    a
    └ c
      └ d
    ->
    a
    └ c
      └ b
    """
    ptree = PathTree(always_raise_error=True)
    ptree.append('a')
    ptree.append('b', 'a')
    print(ptree.getTreeStructure())
    print("-" * 50)
    ptree.replace('b', 'c')
    print(ptree.getTreeStructure())
    print("-" * 50)
    ptree.append('d', 'c')
    print(ptree.getTreeStructure())
    print("-" * 50)
    ptree.replace('a.c.d', 'b')
    print(ptree.getTreeStructure())
    print("-" * 50)

def test_remove_merging_case(passed: bool | None):
    """
    before)
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ └ g
      │   └ h
      └ i
        ├ c
        │ ├ j
        │ └ k
        └ l
          └ m
            └ n
    
    target: 'a.b.i'

    after)
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ ├ g
      │ │ └ h
      │ ├ j
      │ └ k
      └ l
        └ m
          └ n
    """
    data = [
            'a.b.c.d.e', 'a.b.c.d.f', 'a.b.c.g.h', 'a.b.i.c.j', 
            'a.b.i.c.k', 'a.b.i.l.m.n'
        ]
    ptree = PathTree(always_raise_error=True)
    ptree.appendAll(data)
    print(ptree.getTreeStructure())
    print("-" * 50)
    print(ptree.getAllLeafAbs())
    print("-" * 50)
    ptree.remove('a.b.i')
    print(ptree.getTreeStructure())
    print("-" * 50)
    print(ptree.getAllLeafAbs())
    print("-" * 50)

def test_repr(passed: bool | None):
    """
    data)
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ └ g
      │   └ h
      └ i
        ├ c
        │ ├ j
        │ └ k
        └ l
          └ m
            └ n
    """
    data = [
            'a.b.c.d.e', 'a.b.c.d.f', 'a.b.c.g.h', 'a.b.i.c.j', 
            'a.b.i.c.k', 'a.b.i.l.m.n'
        ]
    ptree = PathTree(always_raise_error=True)
    ptree.appendAll(data)
    print(ptree)

def test_getAllLeafAbs_length_sort(passed: bool | None):
    """
    data)
    a
    └ b
      ├ c
      │ ├ d
      │ │ ├ e
      │ │ └ f
      │ └ g
      │   └ h
      └ i
        ├ c
        │ ├ j
        │ └ k
        └ l
          └ m
            └ n
    """
    data = [
            'a.b.c.d.e', 'a.b.c.d.f', 'a.b.c.g.h', 'a.b.i.c.j', 
            'a.b.i.c.k', 'a.b.i.l.m.n'
        ]
    ptree = PathTree(always_raise_error=True)
    ptree.appendAll(data)
    print(ptree.getAllLeafAbs(LENGTH))
    print("-----")
    print(ptree.getAllLeafAbs(LENGTH, False))

def test_getAllLeafAbs_length_sort2(passed: bool | None):
    """
    a
    ├ b
    │ └ c 
    │   └ d
    ├ e
    │ ├ g
    │ │ └ i
    │ │   └ j
    │ │     └ k
    │ └ l
    │   └ m
    │     └ n
    └ o
      └ p
    """
    data = [
        'a.b.c.d', 'a.e.g.i.j.k', 'a.e.l.m.n', 'a.o.p'
    ]
    ptree = PathTree(always_raise_error=True)
    ptree.appendAll(data)
    print(ptree.getAllLeafAbs(LENGTH))
    print("-----")
    print(ptree.getAllLeafAbs(LENGTH, False))

if __name__ == '__main__':
    # 출력하고자 하는 함수 코드만 주석 해제.

    #test_appendAll_and_tree_structure(True)
    #test_appendAll_several_times(True)
    #test_append_and_tree_structure(True)
    #test_replace_simple(True)
    #test_remove_merging_case(True)
    #test_repr(True)
    #test_getAllLeafAbs_length_sort(True)
    test_getAllLeafAbs_length_sort2(True)
    pass
    