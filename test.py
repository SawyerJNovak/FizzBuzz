import unittest
from main import fizzbuzz

class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        for i in [3, 6, 9, 12]:
            print(f'Testing fizzbuzz for: {i}')
            assert fizzbuzz(main.file_dir, main.file_name, main.con, 'FizzBuzz', 1) == 'fizz'

    def test_buzz(self):
        for i in [5, 10, 15, 20]:
            print(f'Testing fizzbuzz for: {i}')
            assert fizzbuzz(main.file_dir, main.file_name, main.con, 'FizzBuzz', 1) == 'fizz'

    def test_fizzbuzz(self):
        for i in [15, 30, 45, 60]:
            print(f'Testing fizzbuzz for: {i}')
            assert fizzbuzz(main.file_dir, main.file_name, main.con, 'FizzBuzz', 1) == 'fizzbuzz'

    def test_lucky(self):
        for i in [3, 13, 23, 30]:
            print(f'Testing fizzbuzz for: {i}')
            assert fizzbuzz(main.file_dir, main.file_name, main.con, 'FizzBuzz', 1) == 'lucky'
