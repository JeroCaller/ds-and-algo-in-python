import unittest
import sys
from dirimporttool import get_super_dir_directly
for i in range(1, 4):
    super_dir = get_super_dir_directly(__file__, i)
    sys.path.append(super_dir)
sys.path.append(super_dir)

from tree_.tree import Tree, PathTree
from tree_.tree import REMOVEALL, REMOVEONE, DONTREMOVE
from tree_.tree import (ParentNoneError, NodeNotFoundError, 
NodeAlreadyExistsError, PathAlreadyExistsError, RootNotUniqueError)


class TestTree(unittest.TestCase):
    def setUp(self):
        desc = self.shortDescription()
        if desc == "default_root": self.tree = Tree(default_root=True)
        else: self.tree = Tree()

    def tearDown(self):
        self.tree.clear()

    def testEmptyTree(self):
        self.assertEqual(self.tree.lenTree(), 0)
        self.assertEqual(self.tree.search('a'), None)
        self.assertEqual(self.tree.getChildren('a'), None)
        self.assertEqual(self.tree.getParent('a'), None)
        self.assertEqual(self.tree.remove('a', REMOVEALL), False)
        self.assertEqual(self.tree.lenTree(), 0)

    def testDefaultRoot(self):
        """
        default_root
        Tree() 생성자의 default_root가 제대로 실행되는 지 테스트. 
        """
        self.assertEqual(self.tree.lenTree(), 1)
        self.assertEqual(self.tree.search('root'), 'root')
        
        self.tree.append('a', 'root')
        self.assertEqual(self.tree.lenTree(), 2)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.getParent('a'), 'root')
        self.assertEqual(self.tree.getChildren('root'), ['a'])

    def testClear(self):
        self.tree.clear()
        self.assertEqual(self.tree.getRoot(), None)
        self.assertEqual(self.tree.getAdjList(), {})
        self.assertEqual(self.tree._r_adj_list, {})
        self.assertEqual(self.tree.lenTree(), 0)
        self.assertEqual(self.tree.getRaiseErrorMode(), False)

    def testAppendAutoRoot(self):
        """
        root 노드가 없는 트리에 부모 노드가 명시되지 않았을 때 
        new_node가 root 노드로 설정되는지와, 부모 노드가 명시되었을 때 
        부모 노드가 root 노드가 되고, new_node가 그 root 노드의 자식 노드로 
        설정되는 지 테스트. 
        """
        # test 1
        self.tree.append('a')
        self.assertEqual(self.tree._root, 'a')
        self.assertEqual(self.tree.lenTree(), 1)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.getChildren('a'), [])
        self.assertEqual(self.tree.getParent('a'), None)
        self.tree.clear()

        # test 2
        self.tree.append('b', 'a')
        self.assertEqual(self.tree._root, 'a')
        self.assertEqual(self.tree.lenTree(), 2)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.search('b'), 'b')
        self.assertEqual(self.tree.getChildren('a'), ['b'])
        self.assertEqual(self.tree.getParent('b'), 'a')

    def testAppendSimple(self):
        self.tree.append('a')
        self.tree.append('b', 'a')
        self.assertEqual(self.tree.lenTree(), 2)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.search('b'), 'b')
        self.assertEqual(self.tree.getChildren('a'), ['b'])
        self.assertEqual(self.tree.getParent('b'), 'a')
        self.assertEqual(self.tree.getParent('a'), None)
        self.assertEqual(self.tree.getChildren('b'), [])
        self.assertEqual(self.tree.getChildren('c'), None)

    def testAppendAllSimple(self):
        data = [
            'a.b'
        ]
        self.tree.appendAll(data)
        self.assertEqual(self.tree.lenTree(), 2)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.search('b'), 'b')
        self.assertEqual(self.tree.getChildren('a'), ['b'])
        self.assertEqual(self.tree.getParent('b'), 'a')
        self.assertEqual(self.tree.getParent('a'), None)
        self.assertEqual(self.tree.getChildren('b'), [])
        self.assertEqual(self.tree.getChildren('c'), None)

    def testAppendAllSeveralTimes(self):
        """
        default_root
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
        data1 = [
            'root.a', 'root.b', 'a.c'
        ]
        self.tree.appendAll(data1, raise_error=True)
        data2 = [
            'root.d', 'b.e'
        ]
        self.tree.appendAll(data2, raise_error=True)
        self.assertEqual(self.tree.lenTree(), 6)

    def testAppendError(self):
        """
        default_root
        Tree().append() 메서드에서 발생할 수 있는 에러 테스트. 
        """
        # test 1
        with self.assertRaises(ParentNoneError):
            self.tree.append(new_node='a', raise_error=True)
        
        # test 2
        with self.assertRaises(NodeNotFoundError):
            self.tree.append('a', 'rot', raise_error=True)

        # test 3
        self.tree.append('a', 'root')
        with self.assertRaises(NodeAlreadyExistsError):
            self.tree.append('a', 'root', raise_error=True)
        
        with self.assertRaises(NodeAlreadyExistsError):
            self.tree.append('root', 'root', raise_error=True)

    def testReplaceSimple(self):
        self.tree.append('a')
        self.tree.append('b', 'a')
        self.tree.replace('b', 'c')
        self.assertEqual(self.tree.search('b'), None)
        self.assertEqual(self.tree.search('c'), 'c')
        self.assertEqual(self.tree.lenTree(), 2)
        self.assertEqual(self.tree.getParent('c'), 'a')
        self.assertEqual(self.tree.getChildren('a'), ['c'])
        self.assertEqual(self.tree.getChildren('c'), [])
        self.assertEqual(self.tree.getChildren('b'), None)
        self.assertEqual(self.tree.getParent('b'), None)

    def testReplaceComplex(self):
        """
        default_root

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
        """
        data = [
            'root.a1.b1.c1.d1.e1', 'root.a1.b1.c1.d1.e2',
            'root.a1.b1.c1.d2', 'root.a1.b1.c2', 'b1.c3', 
            'a1.b2', 'root.a2.b3.c4', 'a2.b4',
        ]
        self.tree.appendAll(data)
        
        self.tree.replace('c1', 'c0')
        self.assertEqual(self.tree.search('c1'), None)
        self.assertEqual(self.tree.getChildren('c0'), ['d1', 'd2'])
        self.assertEqual(self.tree.lenTree(), 15)
    
    def testRemoveSimple(self):
        """
        a
        ├ b
        │ └ e
        └ c
          └ d
        ======
        adj_list = {
            'a': ['b', 'c'], 
            'b': ['e'], 
            'c': ['d'],
            'e': [], 
            'd': [], 
        }
        """
        data = [
            'a.b', 'a.c', 'c.d', 'b.e'
        ]
        self.tree.appendAll(data)
        self.assertEqual(self.tree._root, 'a')
        self.assertEqual(self.tree.lenTree(), 5)

        self.assertEqual(self.tree.remove('b', REMOVEONE), True)
        self.assertEqual(sorted(self.tree.getChildren('a')), ['c', 'e'])
        self.assertEqual(self.tree.getParent('e'), 'a')
        self.assertEqual(self.tree.search('b'), None)
        self.assertEqual(self.tree.lenTree(), 4)

        self.assertEqual(self.tree.remove('c', REMOVEALL), True)
        self.assertEqual(self.tree.search('c'), None)
        self.assertEqual(self.tree.search('d'), None)
        self.assertEqual(self.tree.getChildren('a'), ['e'])
        self.assertEqual(self.tree.lenTree(), 2)

        self.assertEqual(self.tree.remove('a', DONTREMOVE), False)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.search('e'), 'e')
        self.assertEqual(self.tree._root, 'a')
        self.assertEqual(self.tree.lenTree(), 2)

        self.assertEqual(self.tree.remove('e', DONTREMOVE), True)
        self.assertEqual(self.tree.search('e'), None)
        self.assertEqual(self.tree.search('a'), 'a')
        self.assertEqual(self.tree.lenTree(), 1)
    
    def testRemoveComplex(self):
        """
        default_root

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
        self.tree.appendAll(data)
        
        # test 1
        self.tree.remove('c1', REMOVEONE)
        actual_result = self.tree.getChildren('b1')
        actual_result.sort()
        expected_result = ['c2', 'c3', 'd1', 'd2']
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(self.tree.getParent('d1'), 'b1')
        self.assertEqual(self.tree.getParent('d2'), 'b1')
        self.assertEqual(self.tree.search('c1'), None)
        self.assertEqual(self.tree.lenTree(), 14)
        # c1이 포함되어있던 하위 트리에서의 c1의 삭제가 
        # 전혀 다른 하위 트리에도 영향을 주는가? (주지 않아야 한다.)
        self.assertEqual(self.tree.search('a2'), 'a2')
        self.assertEqual(self.tree.getChildren('a2'), ['b3', 'b4'])
        self.assertEqual(self.tree.getParent('c4'), 'b3')

        # test2
        self.tree.remove('b1', REMOVEALL)
        self.assertEqual(self.tree.getChildren('a1'), ['b2'])
        self.assertEqual(self.tree.getChildren('b2'), [])
        self.assertEqual(self.tree.lenTree(), 7)
        # 'b1'이 포함되어있던 하위 트리의 전체 삭제가 
        # 전혀 다른 하위 트리에도 영향을 주는가? (주지 않아야 한다.)
        self.assertEqual(self.tree.getChildren('root'), ['a1', 'a2'])
        self.assertEqual(self.tree.getChildren('a2'), ['b3', 'b4'])
        self.assertEqual(self.tree.getChildren('b3'), ['c4'])
        self.assertEqual(self.tree.getChildren('b4'), [])

        # test 3-1
        self.tree.remove('a1', DONTREMOVE)
        self.assertEqual(self.tree.search('a1'), 'a1')
        self.assertEqual(self.tree.lenTree(), 7)

        # test 3-2
        self.tree.remove('c4', DONTREMOVE)
        self.assertEqual(self.tree.search('c4'), None)
        self.assertEqual(self.tree.lenTree(), 6)
        self.assertEqual(self.tree.getChildren('b3'), [])

        # test 4
        self.tree.remove('b4', REMOVEALL)
        self.assertEqual(self.tree.search('b4'), None)
        self.assertEqual(self.tree.getChildren('a2'), ['b3'])
        self.assertEqual(self.tree.lenTree(), 5)

        # test 5
        self.tree.remove('b3', REMOVEONE)
        self.assertEqual(self.tree.search('b3'), None)
        self.assertEqual(self.tree.getChildren('a2'), [])
        self.assertEqual(self.tree.lenTree(), 4)

    def testIfItWorksRegardlessRaiseErrorMode(self):
        """
        트리 자료구조 제작 시 append 등의 특정 메서드에서 
        raise_error 키워드 인자 값을 달리 하면 입력하는 데이터가 
        같아도 결과가 달라지는 에러가 발생할 때가 있다. 이를 
        방지하기 위한 테스트. 
        """
        tree_obj1 = Tree(default_root=True)
        tree_obj2 = Tree(default_root=True)

        tree_obj1.append('a', 'root')
        tree_obj2.append('a', 'root', raise_error=True)
        self.assertEqual(tree_obj1.lenTree(), tree_obj2.lenTree())

    def testAlwaysRaiseErrorMode(self):
        """
        Tree() 클래스의 인스턴스 속성 중 하나인 
        always_raise_error 속성에 따라 예외 발생 통제가 잘 되는지 
        테스트. 
        """
        # test 1
        tree_obj = Tree(default_root=True, always_raise_error=True)
        with self.assertRaises(ParentNoneError):
            tree_obj.append('a')
        with self.assertRaises(NodeAlreadyExistsError):
            tree_obj.append('root', 'root')
        with self.assertRaises(NodeNotFoundError):
            tree_obj.append('b', 'a')
        with self.assertRaises(NodeNotFoundError):
            tree_obj.replace('a', 'aa')
        with self.assertRaises(NodeAlreadyExistsError):
            tree_obj.replace('root', 'root')
        self.assertEqual(tree_obj.lenTree(), 1)
        self.assertEqual(tree_obj._root, 'root')

        # test 2
        tree_obj = Tree(default_root=True)
        tree_obj.append('a')
        tree_obj.append('root', 'root')
        tree_obj.append('b', 'a')
        self.assertEqual(tree_obj.lenTree(), 1)
        self.assertEqual(tree_obj._root, 'root')

        # test 3
        # 메서드를 통한 always_raise_error 모드 활성화 테스트.
        tree_obj.setRaiseErrorMode(True)
        with self.assertRaises(ParentNoneError):
            tree_obj.append('a')
        with self.assertRaises(NodeAlreadyExistsError):
            tree_obj.append('root', 'root')
        with self.assertRaises(NodeNotFoundError):
            tree_obj.append('b', 'a')
        with self.assertRaises(NodeNotFoundError):
            tree_obj.replace('a', 'aa')
        with self.assertRaises(NodeAlreadyExistsError):
            tree_obj.replace('root', 'root')
        self.assertEqual(tree_obj.lenTree(), 1)
        self.assertEqual(tree_obj._root, 'root')


class TestPathTree(unittest.TestCase):
    def setUp(self):
        desc = self.shortDescription()
        if desc == 'default_root': self.ptree = PathTree(default_root=True)
        else: self.ptree = PathTree()

    def tearDown(self):
        self.ptree.clear()

    def testEmptyTree(self):
        self.assertEqual(self.ptree.lenTree(), 0)
        self.assertEqual(self.ptree._root, None)
        self.assertEqual(self.ptree.search('root'), None)
        self.assertEqual(self.ptree.getChildren('a'), None)
        self.assertEqual(self.ptree.getParent('b'), None)
        self.assertEqual(self.ptree.remove('c'), False)
        self.assertEqual(self.ptree.replace('a', 'c'), False)

    def testDefaultRoot(self):
        """
        default_root
        PathTree() 생성자의 default_root가 제대로 실행되는 지 테스트. 
        """
        self.assertEqual(self.ptree.lenTree(), 1)
        self.assertEqual(self.ptree.search('root'), ['root'])

    def testClear(self):
        self.ptree.clear()
        self.assertEqual(self.ptree.getRoot(), None)
        self.assertEqual(self.ptree.getAdjList(), {})
        self.assertEqual(self.ptree._r_adj_list, {})
        self.assertEqual(self.ptree.lenTree(), 0)
        self.assertEqual(self.ptree.getRaiseErrorMode(), False)

    def testChangeDelimiter(self):
        data = [
            'a.b.c.d.e', 'a.b.c.f', 'a.b.g.h', 'a.i.j'
        ]
        self.ptree.appendAll(data, True)
        self.ptree.delimiter = '/'
        self.assertEqual(self.ptree.delimiter, '/')
        self.assertEqual(self.ptree.lenTree(), 10)
        leaf_nodes = self.ptree.getAllLeafAbs()
        for node in leaf_nodes:
            self.assertIn('/', node)

    def testisAbsPath(self):
        self.assertEqual(self.ptree.isAbsPath('a.b'), True)
        self.assertEqual(self.ptree.isAbsPath('a'), False)

    def testBasename(self):
        self.assertEqual(self.ptree.basename('a.b.c'), 'c')
        self.assertEqual(self.ptree.basename('a'), 'a')

    def testDirname(self):
        self.assertEqual(self.ptree.dirname('a.b.c'), 'a.b')
        self.assertEqual(self.ptree.dirname('a'), '')

    def testSplitAbsPath(self):
        self.assertEqual(self.ptree.splitAbsPath('a.b.c'), ('a.b', 'c'))
        self.assertEqual(self.ptree.splitAbsPath('a'), ('', 'a'))

    def testCombineNodesToAbsPath(self):
        self.assertEqual(
            self.ptree.combineNodesToAbsPath('a.b.c', 'd.e'), 
            'a.b.c.d.e'
        )
        self.assertEqual(
            self.ptree.combineNodesToAbsPath('a.b.c', 'd'),
            'a.b.c.d'
        )
        self.assertEqual(
            self.ptree.combineNodesToAbsPath('a', 'b.c'),
            'a.b.c'
        )
        self.assertEqual(
            self.ptree.combineNodesToAbsPath('a', 'b'), 
            'a.b'
        )

    def testAppendAutoRoot(self):
        """
        root 노드가 없는 트리에 부모 노드가 명시되지 않았을 때 
        new_node가 root 노드로 설정되는지와, 부모 노드가 명시되었을 때 
        부모 노드가 root 노드가 되고, new_node가 그 root 노드의 자식 노드로 
        설정되는 지 테스트. 
        """
        # test 1
        self.ptree.append('a')
        self.assertEqual(self.ptree._root, 'a')
        self.assertEqual(self.ptree.lenTree(), 1)
        self.assertEqual(self.ptree.search('a'), ['a'])
        self.assertEqual(self.ptree.getChildren('a'), {'a': []})
        self.assertEqual(self.ptree.getParent('a'), [''])
        self.ptree.clear()

        # test 2
        self.ptree.append('b', 'a')
        self.assertEqual(self.ptree._root, 'a')
        self.assertEqual(self.ptree.lenTree(), 2)
        self.assertEqual(self.ptree.search('a'), ['a'])
        self.assertEqual(self.ptree.search('b'), ['a.b'])
        self.assertEqual(self.ptree.getChildren('a'), {'a': ['b']})
        self.assertEqual(self.ptree.getParent('b'), ['a'])

    def testAppendSimple(self):
        # test 1
        self.ptree.append('a')
        self.ptree.append('b', 'a')
        self.assertEqual(self.ptree.lenTree(), 2)
        self.assertEqual(self.ptree.search('a'), ['a'])
        self.assertEqual(self.ptree.search('b'), ['a.b'])
        self.assertEqual(self.ptree.getChildren('a'), {'a': ['b']})
        self.assertEqual(self.ptree.getParent('b'), ['a'])
        self.assertEqual(self.ptree.getParent('a'), [''])
        self.assertEqual(self.ptree.getChildren('b'), {'a.b': []})
        self.assertEqual(self.ptree.getChildren('c'), None)

        # test 2
        self.ptree.append('b', 'b')
        self.assertEqual(self.ptree.lenTree(), 3)
        self.assertEqual(self.ptree.search('b'), ['a.b', 'a.b.b'])
        self.assertEqual(
            self.ptree.getChildren('b'), 
            {'a.b': ['b'], 'a.b.b': []}
        )
        self.assertEqual(
            sorted(self.ptree.getParent('b')), 
            sorted(['a.b', 'a'])
        )
        self.assertEqual(self.ptree.search('a.b'), 'a.b')
        self.assertEqual(self.ptree.search('a.b.b'), 'a.b.b')
        self.assertEqual(self.ptree.getChildren('a.b'), ['b'])
        self.assertEqual(self.ptree.getChildren('a.b.b'), [])
        self.assertEqual(self.ptree.getParent('a.b'), 'a')
        self.assertEqual(self.ptree.getParent('a.b.b'), 'a.b')

    def testAppendAllSimple(self):
        # test 1
        data = ['a.b']
        self.ptree.appendAll(data)
        self.assertEqual(self.ptree.lenTree(), 2)
        self.assertEqual(self.ptree.search('a'), ['a'])
        self.assertEqual(self.ptree.search('b'), ['a.b'])
        self.assertEqual(self.ptree.getChildren('a'), {'a': ['b']})
        self.assertEqual(self.ptree.getParent('b'), ['a'])
        self.assertEqual(self.ptree.getParent('a'), [''])
        self.assertEqual(self.ptree.getChildren('b'), {'a.b': []})
        self.assertEqual(self.ptree.getChildren('c'), None)
        self.assertEqual(self.ptree.getRoot(), 'a')
        self.ptree.clear()

        # test 2
        data = ['a.a.b']
        self.ptree.appendAll(data)
        self.assertEqual(self.ptree.lenTree(), 3)
        self.assertEqual(self.ptree.search('a'), ['a', 'a.a'])
        self.assertEqual(self.ptree.search('b'), ['a.a.b'])
        self.assertEqual(
            self.ptree.getChildren('a'),
            {'a': ['a'], 'a.a': ['b']}
        )
        self.assertEqual(
            sorted(self.ptree.getParent('a')),
            sorted(['', 'a'])
        )
        self.assertEqual(self.ptree.getChildren('b'), {'a.a.b': []})
        self.assertEqual(self.ptree.getParent('b'), ['a.a'])
        self.assertEqual(self.ptree.search('a.a'), 'a.a')
        self.assertEqual(self.ptree.search('a.a.b'), 'a.a.b')
        self.assertEqual(self.ptree.getChildren('a.a'), ['b'])
        self.assertEqual(self.ptree.getParent('a.a.b'), 'a.a')
        self.assertEqual(self.ptree.getRoot(), 'a')
        self.assertEqual(
            self.ptree.search(self.ptree.getRoot()),
            ['a', 'a.a']
        )
        self.assertEqual(
            self.ptree.getAdjList()[self.ptree.getRoot()], 
            ['a']
        )

    def testAppendError(self):
        """
        default_root
        append() 메서드에서 발생할 수 있는 에러 테스트. 
        """
        self.ptree.setRaiseErrorMode(True)
        # test 1
        with self.assertRaises(ParentNoneError):
            self.ptree.append('a')

        # test 2
        with self.assertRaises(NodeNotFoundError):
            self.ptree.append('b', 'a')

        # test 3
        self.ptree.append('a', 'root')
        with self.assertRaises(PathAlreadyExistsError):
            self.ptree.append('a', 'root')

    def testAppendAllSeveralTimes(self):
        """
        default_root
        AppendAll() 메서드에 데이터들을 여러 번으로 나눠 대입해도 
        트리에 잘 등록되는지 테스트.
        예)
        data1 = [
            'root.a.c', 'root.b'
        ]
        ->
        root
        ├ a
        │ └ c
        └ b
        
        data2 = [
            'root.b.b', 'root.d'
        ]
        ->
        root
        ├ a
        │ └ c
        ├ b
        │ └ b
        └ d
        """
        data1 = ['root.a.c', 'root.b']
        self.ptree.appendAll(data1)
        data2 = ['root.b.b', 'root.d']
        self.ptree.appendAll(data2)
        self.assertEqual(self.ptree.lenTree(), 6)
        self.assertEqual(self.ptree.search('root.b.b'), 'root.b.b')
        self.assertEqual(self.ptree.getRoot(), 'root')

    def testAppendAllError(self):
        data = [
            'root.a.b', 'c.d.e'
        ]
        self.ptree.setRaiseErrorMode(True)
        with self.assertRaises(RootNotUniqueError):
            self.ptree.appendAll(data)
                
    def testAppendAbs(self):
        # test 1
        self.ptree.setRaiseErrorMode(True)
        path = 'a.b.c'
        self.ptree.appendAbs(path)
        self.assertEqual(self.ptree.search(path), path)
        self.assertEqual(self.ptree.lenTree(), 3)
        self.assertEqual(self.ptree.getParent(path), 'a.b')
        self.assertEqual(self.ptree.getChildren('b'), {'a.b': ['c']})
        self.assertEqual(self.ptree.getRoot(), 'a')

        # test 2
        path = 'a.a.a'
        self.ptree.appendAbs(path)
        self.assertEqual(self.ptree.search(path), path)
        self.assertEqual(self.ptree.lenTree(), 5)
        self.assertEqual(self.ptree.getRoot(), 'a')

        # test 3
        path = 'a.b.c.d'
        self.ptree.appendAbs(path)
        self.assertEqual(self.ptree.search(path), path)
        self.assertEqual(self.ptree.lenTree(), 6)
        self.assertEqual(self.ptree.getRoot(), 'a')

        # test 4
        path = 'a.b.e'
        self.ptree.appendAbs(path)
        self.assertEqual(self.ptree.search(path), path)
        self.assertEqual(self.ptree.lenTree(), 7)
        self.assertEqual(self.ptree.getRoot(), 'a')

        # test 5
        path = 'a.b.d'
        self.ptree.appendAbs(path)
        self.assertEqual(self.ptree.search(path), path)
        self.assertEqual(self.ptree.lenTree(), 8)
        self.assertEqual(self.ptree.search('d'), ['a.b.c.d', 'a.b.d'])
        self.assertEqual(self.ptree.getRoot(), 'a')

    def testAppendAbsError(self):
        """
        PathTree().AppendAbs() 메서드에서 일어날 수 있는 
        예외들 테스트. 
        """
        self.ptree.setRaiseErrorMode(True)
        self.ptree.appendAbs('a.b.c')

        # test 1
        with self.assertRaises(PathAlreadyExistsError):
            self.ptree.appendAbs('a.b.c')

        # test 2
        with self.assertRaises(RootNotUniqueError):
            self.ptree.appendAbs('10.j.q.k.a')

        self.assertEqual(self.ptree.getRoot(), 'a')
        self.assertEqual(self.ptree.lenTree(), 3)

    def testReplaceSimple(self):
        # test 1
        self.ptree.append('a')
        self.ptree.append('b', 'a')
        self.ptree.replace('b', 'c')
        self.assertEqual(self.ptree.search('b'), None)
        self.assertEqual(self.ptree.search('c'), ['a.c'])
        self.assertEqual(self.ptree.lenTree(), 2)
        self.assertEqual(self.ptree.getParent('c'), ['a'])
        self.assertEqual(self.ptree.getParent('b'), None)
        self.assertEqual(self.ptree.getChildren('c'), {'a.c': []})
        self.assertEqual(self.ptree.getChildren('b'), None)
        self.assertEqual(self.ptree.getChildren('a'), {'a': ['c']})

        # test 2
        self.ptree.append('d', 'c')
        self.ptree.replace('a.c.d', 'b')
        self.assertEqual(self.ptree.search('d'), None)
        self.assertEqual(self.ptree.lenTree(), 3)
        self.assertEqual(self.ptree.getParent('b'), ['a.c'])
        self.assertEqual(self.ptree.getChildren('b'), {'a.c.b': []})
        self.assertEqual(self.ptree.search('a.c.b'), 'a.c.b')

    def testReplaceError(self):
        self.ptree.setRaiseErrorMode(True)

        # test 1
        with self.assertRaises(NodeNotFoundError):
            self.ptree.replace('a', 'aa')

        # test 2
        data = [
            'a.b.c', 'a.b.d'
        ]
        self.ptree.appendAll(data)
        with self.assertRaises(PathAlreadyExistsError):
            self.ptree.replace('a.b.c', 'd')
        self.assertEqual(self.ptree.lenTree(), 4)
        self.assertEqual(self.ptree.getChildren('a.b'), ['c', 'd'])
        self.assertEqual(
            self.ptree.getAllLeafAbs(),
            ['a.b.c', 'a.b.d']
        )

    def testRemoveSimpleRemoveOne(self):
        """
        a
        ├ b
        │ └ e
        ├ c
        │ └ d
        ├ f
        │ └ f
        └ g
          └ g
            └ h
        """
        data = [
            'a.b.e', 'a.c.d', 'a.f.f', 'a.g.g.h'
        ]
        self.ptree.appendAll(data, raise_error=True)

        self.assertEqual(self.ptree.remove('b', REMOVEONE), True)
        self.assertEqual(self.ptree.search('b'), None)
        self.assertEqual(self.ptree.lenTree(), 9)
        self.assertNotIn('b', self.ptree.getChildren('a')['a'])
        self.assertEqual(self.ptree.remove('e', REMOVEONE), True)
        self.assertEqual(self.ptree.search('e'), None)
        self.assertEqual(self.ptree.lenTree(), 8)
        self.assertNotIn('e', self.ptree.getChildren('a')['a'])

        self.assertEqual(self.ptree.remove('g', REMOVEONE), True)
        self.assertEqual(self.ptree.search('g'), None)
        self.assertEqual(self.ptree.lenTree(), 6)
        self.assertIn('h', self.ptree.getChildren('a')['a'])

        self.assertEqual(self.ptree.remove('a.f', REMOVEONE), True)
        self.assertEqual(self.ptree.search('a.f'), 'a.f')
        self.assertEqual(self.ptree.search('a.f.f'), None)
        self.assertEqual(self.ptree.lenTree(), 5)

    def testRemoveSimpleRemoveAll(self):
        """
        data1)
        a
        ├ b
        │ ├ c
        │ │ ├ d
        │ │ │ └ e
        │ │ └ f
        │ └ g
        │   └ h
        └ i
          └ j

        data2)
        a
        ├ b
        │ ├ c
        │ │ ├ d
        │ │ │ └ e
        │ │ └ f
        │ └ d
        │   └ h
        ├ i
        │ └ j
        └ c
          └ c
        """
        data1 = [
            'a.b.c.d.e', 'a.b.c.f', 'a.b.g.h', 'a.i.j'
        ]
        self.ptree.appendAll(data1, True)
        expected_len = 10
        self.assertEqual(self.ptree.lenTree(), expected_len)

        self.assertEqual(self.ptree.remove('c', REMOVEALL), True)
        self.assertEqual(self.ptree.getChildren('a.b'), ['g'])
        expected_len -= 4
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('a.b.c.d.e'), None)
        self.assertEqual(self.ptree.search('a.i.j'), 'a.i.j')
        self.assertEqual(self.ptree.search('a.b.g.h'), 'a.b.g.h')

        self.assertEqual(self.ptree.remove('h', REMOVEALL), True)
        self.assertEqual(self.ptree.search('a.b.g.h'), None)
        self.assertEqual(self.ptree.search('a.b.g'), 'a.b.g')
        expected_len -= 1
        self.assertEqual(self.ptree.lenTree(), expected_len)

        self.assertEqual(self.ptree.remove('a', REMOVEALL), True)
        expected_len -= 5
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.getRoot(), None)
        self.assertEqual(self.ptree.getAdjList(), {})

        self.ptree.clear()

        data2 = [
            'a.b.c.d.e', 'a.b.c.f', 'a.b.d.h', 'a.i.j', 'a.c.c'
        ]
        self.ptree.appendAll(data2, True)
        expected_len = 12
        self.assertEqual(self.ptree.lenTree(), expected_len)

        self.assertEqual(self.ptree.remove('d', REMOVEALL), True)
        expected_len -= 4
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('d'), None)
        self.assertEqual(self.ptree.search('a.b.c.d.e'), None)
        self.assertEqual(self.ptree.search('a.b.d.h'), None)
        self.assertNotIn('d', self.ptree.getChildren('a.b.c'))
        self.assertNotIn('d', self.ptree.getChildren('a.b'))

        self.assertEqual(self.ptree.remove('c', REMOVEALL), True)
        expected_len -= 4
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('c'), None)
        self.assertEqual(self.ptree.search('f'), None)

        self.assertEqual(self.ptree.remove('a.i', REMOVEALL), True)
        expected_len -= 2
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('a.i.j'), None)
        self.assertEqual(self.ptree.getChildren('a'), {'a': ['b']})

    def testRemoveSimpleDontRemove(self):
        """
        data)
        a
        ├ b
        │ ├ c
        │ │ ├ d
        │ │ │ └ e
        │ │ └ f
        │ └ d
        │   └ h
        ├ i
        │ └ j
        └ c
          └ c
        """
        data = [
            'a.b.c.d.e', 'a.b.c.f', 'a.b.d.h', 'a.i.j', 'a.c.c'
        ]
        self.ptree.appendAll(data)
        expected_len = 12

        self.assertEqual(self.ptree.remove('e', DONTREMOVE), True)
        expected_len -= 1
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('e'), None)

        self.assertEqual(self.ptree.remove('b', DONTREMOVE), False)
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('b'), ['a.b'])

        self.assertEqual(self.ptree.remove('a.b.c.f', DONTREMOVE), True)
        expected_len -= 1
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('a.b.c.f'), None)

        self.assertEqual(self.ptree.remove('c', DONTREMOVE), True)
        expected_len -= 1
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('a.c.c'), None)
        self.assertEqual(self.ptree.search('a.c'), 'a.c')
        self.assertEqual(self.ptree.search('a.b.c'), 'a.b.c')
        self.assertEqual(self.ptree.getChildren('a.b.c'), ['d'])

    def testRemoveMergingCase(self):
        """
        data)
        a
        └ b
          └ c
            ├ d
            │ └ h
            └ e
              └ d
                └ f
        """
        data = [
            'a.b.c.d.h', 'a.b.c.e.d.f',
        ]
        self.ptree.appendAll(data, True)
        self.assertEqual(self.ptree.lenTree(), 8)

        self.assertEqual(self.ptree.remove('e'), True)
        self.assertEqual(self.ptree.lenTree(), 6)
        self.assertEqual(self.ptree.getChildren('a.b.c.d'), ['f', 'h'])

    def testRemoveMergingCase2(self):
        """
        example)
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
        self.ptree.appendAll(data, True)
        expected_len = 15
        self.assertEqual(self.ptree.lenTree(), expected_len)

        self.assertEqual(self.ptree.remove('a.b.i'), True)
        expected_len -= 2
        self.assertEqual(self.ptree.lenTree(), expected_len)
        self.assertEqual(self.ptree.search('i'), None)
        self.assertEqual(self.ptree.search('c'), ['a.b.c'])
        self.assertEqual(
            self.ptree.getChildren('c'), 
            {'a.b.c': ['d', 'g', 'j', 'k']}
        )
        self.assertEqual(self.ptree.getParent('c'), ['a.b'])
        self.assertEqual(self.ptree.search('a.b.l.m.n'), 'a.b.l.m.n')
        self.assertEqual(self.ptree.getChildren('a.b.c.d'), ['e', 'f'])
        self.assertEqual(self.ptree.getChildren('a.b.c.g'), ['h'])
        self.assertEqual(self.ptree.getChildren('a.b.c.j'), [])
        self.assertEqual(self.ptree.getChildren('a.b.c.k'), [])


if __name__ == '__main__':
    def one_test():
        suite = unittest.TestSuite()
        suite.addTest(TestPathTree("testRemoveSimpleRemoveOne"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    unittest.main()
    #one_test()
   