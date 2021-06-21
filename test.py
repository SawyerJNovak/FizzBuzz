import unittest
from main import fizzbuzz

class TestFizzBuzz(unittest.TestCase):
    def test_fizzbuzz(self):
        for i in [3, 6, 9, 12]:
            print(f'Testing fizzbuzz for: {i}')
            assert fizzbuzz(main.file_dir, main.file_name, main.con, 'FizzBuzz', 1) == 'fizz'
