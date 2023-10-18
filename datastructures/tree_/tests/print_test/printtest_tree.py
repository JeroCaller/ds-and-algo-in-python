import sys
from pprint import pprint
from dirimporttool import get_super_dir_directly

for i in range(1, 4):
    super_dir = get_super_dir_directly(__file__, i)
    sys.path.append(super_dir)
sys.path.append(super_dir)

from tree_.tree import Tree
from tree_.tree import REMOVEALL, REMOVEONE, DONTREMOVE

def test_append_all():
    """
    예상 트리 구조)
    root
    ├ 살 것들
    │   └ 마트
    │       └ 당근
    └ 할 일
        ├ 공부
        │    └ 과목
        │        ├ 자료구조
        │        └ 프로그래밍 언어
        │             └ 파이썬
        └ 집안일
            └ 설거지
                └ 접시
    """
    tree_obj = Tree()
    data = [
        'root.살 것들.마트', '마트.당근', 'root.할 일.공부', 
        'root.할 일.집안일', '공부.과목.자료구조', '과목.프로그래밍 언어.파이썬',
        '집안일.설거지.접시',
    ]
    tree_obj.appendAll(data)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    pprint(tree_obj._adj_list)

def test_append_all_simple():
    """
    data = ['a.b']
    ->
    a
    └ b
    """
    tree_obj = Tree()
    data = ['a.b']
    tree_obj.appendAll(data, True)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    print(tree_obj._adj_list)

def test_append_all_simple2():
    """
    data = ['a.b', 'b.c']
    -> 
    a
    └ b
      └ c
    """
    tree_obj = Tree()
    data = ['a.b', 'b.c']
    tree_obj.appendAll(data, raise_error=True)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    print(tree_obj._adj_list)

def test_appendAll_complex():
    """
    root
    ├ a1
    │ ├ b1
    │ │ ├ c1
    │ │ │ ├ d1
    │ │ │ │ ├ e1
    │ │ │ │ └ e2
    │ │ │ └ d2
    │ │ ├ c2
    │ │ └ c3
    │ └ b2
    └ a2
      ├ b3
      │ └ c4
      └ b4
    ======
    adj_list = {
        'root': ['a1', 'a2'], 
        'a1': ['b1', 'b2'], 
        'b1': ['c1', 'c2', 'c3'], 
        'c1': ['d1', 'd2'], 
        'd1': ['e1', 'e2'], 
        'e1': [],
        'e2': [],
        'd2': [],
        'c2': [],
        'c3': [],
        'b2': [],
        'a2': ['b3', 'b4'],
        'b3': ['c4'],
        'c4': [], 
        'b4': [], 
        }
    """
    data = [
        'root.a1.b1.c1.d1.e1', 'root.a1.b1.c1.d1.e2',
        'root.a1.b1.c1.d2', 'root.a1.b1.c2', 'b1.c3', 
        'a1.b2', 'root.a2.b3.c4', 'a2.b4',
    ]
    tree_obj = Tree(default_root=True)
    tree_obj.appendAll(data, raise_error=True)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    pprint(tree_obj._adj_list)
    print("-----")
    print(f"The number of nodes in the tree: {tree_obj.lenTree()}")

def test_append_simple():
    """
    data: a, b
    ->
    a
    └ b
    """
    tree_obj = Tree()
    tree_obj.append('a', raise_error=False)
    tree_obj.append('b', 'a', raise_error=False)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    pprint(tree_obj._adj_list)

def test_append_simple2():
    """
    data: a, b, c
    ->
    a
    └ b
      └ c
    """
    tree_obj = Tree()
    tree_obj.append('a')
    tree_obj.append('b', 'a')
    tree_obj.append('c', 'b')
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    pprint(tree_obj._adj_list)

def test_append_error():
    """
    append() 메서드에서 발생할 수 있는 예외 테스트.
    """
    tree_obj = Tree(default_root=True)
    tree_obj.append('a', raise_error=True)

def test_appendAll_several_times():
    """
    Tree().appendAll() 메서드에 데이터들을 여러 번으로 나눠서 
        대입해도 트리에 잘 등록되는지 테스트. 
        예)
        tree_obj = Tree()
        data1 = [
            'root.a', 'root.b', 'a.c'
        ]
        tree_obj.appendAll(data1)
        ->
        root
        ├ a
        │ └ c
        └ b
        ->
        data2 = [
            'root.d', 'b.e'
        ]
        tree_obj.appendAll(data2)
        ->
        root
        ├ a
        │ └ c
        ├ b
        │ └ e
        └ d
    """
    tree_obj = Tree()
    data1 = [
            'root.a', 'root.b', 'a.c'
    ]
    tree_obj.appendAll(data1)
    data2 = [
        'root.d', 'b.e'
    ]
    tree_obj.appendAll(data2)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    pprint(tree_obj._adj_list)

def test_appendAll_error():
    """
    appendAll() 메서드에서 일어날 수 있는 에러 테스트. 
    """
    tree_obj = Tree(default_root=True)
    data = ['root', 'root']
    tree_obj.appendAll(data, raise_error=True)
    print(tree_obj)
    print("-----")
    print(tree_obj.getTreeStructure())
    print("-----")
    print("adj_list")
    pprint(tree_obj._adj_list)
    print("-----")
    print(f"The number of nodes in the tree: {tree_obj.lenTree()}")

def test_reverse_adj_list():
    """
    root
    └ main
        ├ interface.py
        ├ log
        │   ├ debug.log
        │   └ error.log
        ├ main.dy
        ├ sound.py
        └ system.py
    ->
    adj_list = {
        'root': ['main'], 
        'main': [
            'interface.py', 'log', 'main.py', 'sound.py', 'system.py'
        ],
        'interface.py': [],
        'log': ['debug.log', 'error.log'],
        'main.py': [], 
        'sound.py': [],
        'system.py': [], 
        'debug.log': [], 
        'error.log': [],
    }
    -> 
    r_adj_list = {
        'main': 'root', 
        'interface.py': 'main',
        'log': 'main',
        'main.py': 'main',
        'sound.py': 'main', 
        'system.py': 'main',
        'debug.log': 'log',
        'error.log': 'log',
    }
    """
    tree_obj = Tree()

    data = {
        'root': ['main'], 
        'main': [
            'interface.py', 'log', 'main.py', 'sound.py', 'system.py'
        ],
        'interface.py': [],
        'log': ['debug.log', 'error.log'],
        'main.py': [], 
        'sound.py': [],
        'system.py': [], 
        'debug.log': [], 
        'error.log': [],
    }
    tree_obj._adj_list = data
    pprint(tree_obj._reverseAdjList())

def test_remove_complex():
    """
    test_appendAll_complex() 함수의 데이터를 그대로 사용함. 
    """
    data = [
        'root.a1.b1.c1.d1.e1', 'root.a1.b1.c1.d1.e2',
        'root.a1.b1.c1.d2', 'root.a1.b1.c2', 'b1.c3', 
        'a1.b2', 'root.a2.b3.c4', 'a2.b4',
    ]
    tree_obj = Tree(default_root=True)
    tree_obj.appendAll(data)
    print("-----")
    print("삭제 전 원래 트리 모습.")
    print(tree_obj.getTreeStructure())
    print("-----")
    tree_obj.remove('c1', REMOVEONE)
    print("c1 노드 삭제 후 트리 모습. mode: REMOVEONE")
    print(tree_obj.getTreeStructure())
    print("-----")
    tree_obj.remove('b1', REMOVEALL)
    print("b1 노드 삭제 후 트리 모습. mode: REMOVEALL")
    print(tree_obj.getTreeStructure())
    print("-----")
    tree_obj.remove('a1', DONTREMOVE)
    print("a1 노드 삭제 시도 후 트리 모습. mode: DONTREMOVE")
    print(tree_obj.getTreeStructure())
    print("-----")
    tree_obj.remove('c4', DONTREMOVE)
    print("c4 노드 삭제 시도 후 트리 모습. mode: DONTREMOVE")
    print(tree_obj.getTreeStructure())
    print("-----")

if __name__ == '__main__':
    # 출력하고자 하는 함수 코드만 주석 해제.

    test_append_all()
    #test_reverse_adj_list()
    #test_append_all_simple()
    #test_append_all_simple2()
    #test_append_simple()
    #test_append_simple2()
    #test_append_error()
    #test_appendAll_several_times()
    #test_appendAll_error()
    #test_appendAll_complex()
    #test_remove_complex()
    pass
    