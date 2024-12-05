import unittest

class TestExample(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 1, 4)

if __name__ == '__main__':
    unittest.main()