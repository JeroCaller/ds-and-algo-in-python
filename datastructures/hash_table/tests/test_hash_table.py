import unittest
import sys
from dirimporttool import get_super_dir_directly
for i in range(1, 3):
    super_dir = get_super_dir_directly(__file__, i)
    sys.path.append(super_dir)
from hash_table.my_hash_table import HashTable

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
new_dataset = [
        ("코딩", "coding"),
        ("밤바다", "night sea"),
        ("공기", "air"),
        ("공깃밥", "rice"),
        ("디버그", "debug"),
        ("에너지", "energy"),
]


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(10)
        self.dataset = dataset
        self.desc = self.shortDescription()

        if self.desc == "need_dataset":
            self.ht.addDataAll(self.dataset)
    
    def test_empty_data(self):
        """
        빈 해시 테이블 출력 테스트.
        """
        self.assertEqual(self.ht.getAllData(), [])
        self.assertEqual(self.ht.getLength(), 0)
        self.assertEqual(self.ht.getHTSize(), 10)

    def test_clear(self):
        """
        need_dataset\n
        해시 테이블 내 모든 데이터를 삭제하는 지 테스트.
        """
        self.ht.clear()
        self.assertEqual(self.ht.getAllData(), [])
        self.assertEqual(self.ht.getLength(), 0)
        self.assertEqual(self.ht.getHTSize(), 21)

    def test_add_data(self):
        """
        (key, value) 데이터 삽입 테스트.
        """
        # test1
        self.ht.addData(('우와', 'wow'))
        self.ht.addData(('방', 'room'))
        saved_data = self.ht.getAllData()
        saved_data.sort()
        expected_result = [('우와', 'wow'), ('방', 'room')]
        expected_result.sort()
        self.assertEqual(saved_data, expected_result)
        self.assertEqual(self.ht.getLength(), 2)

        # test2
        self.ht.addData(('우와', 'WOW'))
        saved_data = self.ht.getAllData()
        saved_data.sort()
        expected_result = [('우와', 'WOW'), ('방', 'room')]
        expected_result.sort()
        self.assertEqual(saved_data, expected_result)
        self.assertEqual(self.ht.getLength(), 2)

    def test_add_data_all(self):
        """
        need_dataset\n
        데이터셋을 잘 삽입하는지 테스트.
        """
        actual_result = self.ht.getAllData()
        actual_result.sort()
        self.dataset.sort()
        self.assertEqual(actual_result, self.dataset)

    def test_find_data(self):
        """
        need_dataset\n
        주어진 key에 대응되는 값을 찾는 테스트.
        """
        # test1
        test_key = '꽃'
        result = self.ht.findData(test_key)
        self.assertEqual(result, "flower")

        # test2
        test_key = "불"
        result = self.ht.findData(test_key)
        self.assertEqual(result, None)

    def test_extend_ht_size(self):
        """
        need_dataset\n
        autoResize() 메서드 테스트. 
        """
        old_hash_collision = self.ht.checkHashCollision()
        old_ht_size = self.ht.getHTSize()
        test_old_data = ("꽃", "flower")
        old_hash_code = self.ht.hashKey(test_old_data[0])

        self.ht.addDataAll(new_dataset)
        new_hash_collision = self.ht.checkHashCollision()
        new_ht_size = self.ht.getHTSize()
        new_hash_code = self.ht.hashKey(test_old_data[0])

        self.assertEqual(old_hash_collision[0], True)
        self.assertTrue(old_hash_collision[1] > new_hash_collision[1])
        self.assertEqual(new_hash_collision[0], True)
        self.assertNotEqual(old_ht_size, new_ht_size)
        self.assertNotEqual(old_hash_code, new_hash_code)
        self.assertEqual(
            self.ht.findData(test_old_data[0]),
            test_old_data[1]
            )

    def test_check_hash_collision(self):
        """
        해시 충돌 여부 확인 테스트.
        """
        # test1
        ht = HashTable(10)
        ht.addDataAll(self.dataset)
        is_col, max_depth, num_buckets = ht.checkHashCollision()
        self.assertEqual(is_col, True)
        self.assertEqual(max_depth, 3)
        self.assertEqual(num_buckets, 2)

        # test2
        ht = HashTable(100)
        ht.addDataAll(self.dataset)
        is_col, max_depth, num_buckets = ht.checkHashCollision()
        self.assertEqual(is_col, False)
        self.assertEqual(max_depth, 1)
        self.assertEqual(num_buckets, 0)

    def test_remove_data(self):
        """
        need_dataset\n
        해시 테이블 내 특정 데이터를 삭제하는 removeData() 
        메서드 테스트.
        """
        target_data = ("포도", "grape")
        self.ht.removeData(target_data[0])
        all_data = self.ht.getAllData
        self.assertNotIn(all_data, target_data)


if __name__ == '__main__':
    unittest.main()
    