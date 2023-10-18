import unittest
import sys
from dirimporttool import get_super_dir_directly
super_dir = get_super_dir_directly(__file__, 2)
sys.path.append(super_dir)
from stack.my_stack import StaticStack


class TestStack(unittest.TestCase):
    def setUp(self):
        self.st = StaticStack(10)
        self.desc = self.shortDescription()
        self.dataset = ['사과', '바나나', '당근', '참외']

        if self.desc == "need_dataset":
            for data in self.dataset:
                self.st.push(data)

    def test_is_empty(self):
        """
        빈 스택 테스트.
        """
        self.assertEqual(self.st.__repr__(), '[]')
        self.assertEqual(self.st.is_empty(), True)
        self.assertEqual(self.st.getLength(), 0)

    def test_push(self):
        """
        스택에 항목 삽입 테스트.
        """
        # test1
        data = '오렌지'
        self.st.push(data)
        self.assertEqual(self.st.__repr__(), "['오렌지']")
        self.assertEqual(self.st.getLength(), 1)
        self.assertEqual(self.st.is_empty(), False)

        # test2
        for data in self.dataset:
            self.st.push(data)
        expected_result = "['오렌지', '사과', '바나나', '당근', '참외']"
        self.assertEqual(self.st.__repr__(), expected_result)
        self.assertEqual(self.st.getLength(), 5)
        self.assertEqual(self.st.is_empty(), False)

        # test3
        st2 = StaticStack(0)
        actual_result = st2.push('코끼리')
        self.assertEqual(actual_result, False)
        self.assertEqual(st2.is_empty(), True)

    def test_pop(self):
        """
        need_dataset\n
        pop 테스트.
        """
        # test1
        st2 = StaticStack(5)
        self.assertEqual(st2.pop(), None)

        # test2
        self.assertEqual(self.st.pop(), '참외')
        self.assertEqual(self.st.getLength(), 3)

    def test_peek(self):
        """
        need_dataset\n
        스택 맨 끝 항목 조회 기능 테스트.
        """
        # test1
        st2 = StaticStack(0)
        with self.assertRaises(IndexError):
            st2.peek()

        # test2
        self.assertEqual(self.st.peek(), '참외')
        self.assertEqual(self.st.getLength(), 4)

    def test_set_new_size(self):
        """
        need_dataset\n
        setNewSize 메서드 테스트.
        """
        # test1
        self.st.setNewSize(20)
        self.assertEqual(self.st.size_, 20)

        # test2
        self.st.setNewSize(5)
        self.assertEqual(self.st.size_, 5)

        # test3
        self.st.setNewSize(3)
        self.assertEqual(self.st.size_, 5)

    def test_clear(self):
        """
        need_dataset\n
        스택을 모두 비우는 테스트.
        """
        # test1
        self.st.clear()
        self.assertEqual(self.st.is_empty(), True)
        self.assertEqual(self.st.getLength(), 0)
        self.assertEqual(getattr(self.st, 'stack'), [])
        self.assertEqual(self.st.__repr__(), '[]')


if __name__ == '__main__':
    unittest.main()
    