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


    def test_goldbah(self):
        self.assertTrue(goldbach(12))
        self.assertFalse(goldbach(177))

    @patch('builtins.input', return_value = 8)
    def test_get_value(self, inp):
        self.assertEqual(get_value(), 8)

    @patch('Task_7_6.get_value', return_value='q')
    def test_exit_main_prog(self, get_value):
        self.assertEqual(main_prog(), None)

    @patch('Task_7_6.get_value', side_effect = [8, 10, 11 ,12, 'we', 'q'])
    def test_main_prog(self, get_val):
        self.assertIn(main_prog(), [True, None])
