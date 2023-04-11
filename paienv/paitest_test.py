import unittest
import random
import string
from paitest import paitest


class InitTestCase(unittest.TestCase):
    '''
        Input random direction into paitest()
    '''

    def setUp(self) -> None:
        
        self.direction_test_input_extra_list = []

        # Add some random strings
        for _ in range(100):
            _len = random.randint(0, 10)

            self.direction_test_input_extra_list.append(
                ''.join(random.choice(string.ascii_letters + string.digits)
                        for _ in range(_len))
            )

        return super().setUp()

    def test_random_direction_init_test(self):
        for dirc in self.direction_test_input_extra_list:
            with self.assertRaises(KeyError):
                obj = paitest(dirc)

    def tearDown(self) -> None:
        return super().tearDown()


class RandomFramesTestCase(unittest.TestCase):
    '''
        Generate random N configuration frames type II from paitest.

        Check whether the 'test_chip_addr' is correct
    '''

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
