from unittest import TestCase
from unittest.mock import patch
from Task_7_6 import isprime, goldbach, check_even, get_value, main_prog
from Task_7_6 import NoValue, NotIntValue, StringValue



class TestGoldbachMock(TestCase):

    def test_is_prime(self):
        self.assertTrue(isprime(7))
        self.assertFalse(isprime(8))

    def test_check_even(self):
        self.assertTrue(check_even(12))
        self.assertFalse(check_even(13))
        self.assertFalse(check_even(None))
        self.assertFalse(check_even('qwerq'))
        self.assertFalse(check_even([1,2,3]))

    # @patch('Task_7_6.get_value', return_value =8)
    @patch('Task_7_6.get_value', return_value='q')
    def test_main_prog(self,input):
        self.assertTrue(main_prog())
