import unittest
import random
import string
from paitest import paitest
from paitest.frames import FrameDecoder
from frame_test import random_gen_core_coord, Coord


class InitTestCase(unittest.TestCase):
    """
    Input random direction into paitest()
    """

    def setUp(self) -> None:
        self.direction_test_input_extra_list = []

        # Add some random strings
        for _ in range(100):
            _len = random.randint(0, 10)

            self.direction_test_input_extra_list.append(
                "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(_len)
                )
            )

        return super().setUp()

    def test_illigal_direction_init(self) -> None:
        for dirc in self.direction_test_input_extra_list:
            with self.assertRaises(KeyError):
                obj = paitest(dirc)

    def tearDown(self) -> None:
        return super().tearDown()


class PAITestTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.paitest = paitest("EAST")
        self.decoder = FrameDecoder()
        return super().setUp()

    def test_func_Get1GroupForNCoresWith1Param_cores_illegal_range(self) -> None:
        """Test number of cores > 1008"""
        N = 1008
        a = self.paitest.Get1GroupForNCoresWith1Param(N, save_dir="./test")
        self.assertIsInstance(a, tuple)

        with self.assertRaises(ValueError):
            N = 1009
            _ = self.paitest.Get1GroupForNCoresWith1Param(N, save_dir="./test")
    
    def test_func_Get1GroupForNCoresWithNParams_cores_illegal_range(self) -> None:
        """Test number of cores > 1008"""
        N = 1008
        a = self.paitest.Get1GroupForNCoresWithNParams(N, save_dir="./test")
        self.assertIsInstance(a, tuple)

        with self.assertRaises(ValueError):
            N = 1009
            _ = self.paitest.Get1GroupForNCoresWithNParams(N, save_dir="./test")
            
    def test_func_GetNGroupsFor1CoreWithNParams_cores_illegal_range(self) -> None:
        """Test number of cores > 1008"""
        N = 1008
        a = self.paitest.GetNGroupsFor1CoreWithNParams(N, save_dir="./test")
        self.assertIsInstance(a, tuple)

        with self.assertRaises(ValueError):
            N = 1009
            _ = self.paitest.GetNGroupsFor1CoreWithNParams(N, save_dir="./test")
            
    def test_func_ReplaceCoreCoord_cores_illegal_range(self) -> None:
        in_frame = random.randint(0, 2**64-1)
        a = self.paitest.ReplaceCoreCoord(in_frame, (21, 21))
        self.assertIsInstance(a, int)
        
        in_frame_list = [random.randint(0, 2**64-1), random.randint(0, 2**64-1), random.randint(0, 2**64-1)]
        b = self.paitest.ReplaceCoreCoord(in_frame_list, (21, 21))
        self.assertIsInstance(b, tuple)

        with self.assertRaises(ValueError):
            # Illegal core coordinate
            c = self.paitest.ReplaceCoreCoord(in_frame_list, (28, 28))

    def test_func_Get1GroupForNCoresWithNParams_is_core_masked(self) -> None:
        # 1. Test N > 1007
        N = 1009
        # Add masked core coordinate
        with self.assertRaises(ValueError):
            a = self.paitest.Get1GroupForNCoresWithNParams(
                N,
                masked_core_coord=(9, 9),
            )

        # 2. Test illegal masked core coordinate
        with self.assertRaises(ValueError):
            a = self.paitest.Get1GroupForNCoresWithNParams(
                N,
                masked_core_coord=(14, 31),
            )

        # 3. Test whether the core is masked
        masked_core_coords = random_gen_core_coord(1000)
        N = 10

        for masked_core_coord in masked_core_coords:
            a = self.paitest.Get1GroupForNCoresWithNParams(
                N,
                masked_core_coord=(masked_core_coord.x, masked_core_coord.y),
            )
            self.assertEqual(len(a), 3)
            self.assertEqual(len(a[0]), N * 3)
            self.assertEqual(len(a[1]), N)
            self.assertEqual(len(a[2]), N * 3)

            attr = self.decoder.decode(a[0][:3])
            self.assertNotEqual(attr.get("core_coord"), masked_core_coord)

    def test_func_Get1GroupForNCoresWith1Param_is_core_masked(self) -> None:
        # 1. Test N > 1007
        N = 1008

        with self.assertRaises(ValueError):
            a = self.paitest.Get1GroupForNCoresWith1Param(
                N,
                masked_core_coord=(9, 9),
            )

        # 2. Test illegal masked core coordinate
        with self.assertRaises(ValueError):
            a = self.paitest.Get1GroupForNCoresWith1Param(
                N,
                masked_core_coord=(29, 15),
            )

        # 3. Test whether the core is masked
        masked_core_coords = random_gen_core_coord(1000)
        N = 10

        for masked_core_coord in masked_core_coords:
            a = self.paitest.Get1GroupForNCoresWith1Param(
                N,
                masked_core_coord=(masked_core_coord.x, masked_core_coord.y),
            )
            self.assertEqual(len(a), 3)
            self.assertEqual(len(a[0]), N * 3)
            self.assertEqual(len(a[1]), N)
            self.assertEqual(len(a[2]), N * 3)

            attr = self.decoder.decode(a[0][:3])
            self.assertNotEqual(attr.get("core_coord"), masked_core_coord)
    
    def test_func_GetNGroupsFor1CoreWithNParams_is_core_masked(self) -> None:
        # 1. Test N > 1007
        N = 1009
        # Add masked core coordinate
        with self.assertRaises(ValueError):
            a = self.paitest.GetNGroupsFor1CoreWithNParams(
                N,
                masked_core_coord=(9, 9),
            )

        # 2. Test illegal masked core coordinate
        with self.assertRaises(ValueError):
            a = self.paitest.GetNGroupsFor1CoreWithNParams(
                N,
                masked_core_coord=(14, 31),
            )

        # 3. Test whether the core is masked
        masked_core_coords = random_gen_core_coord(1000)
        N = 10

        for masked_core_coord in masked_core_coords:
            a = self.paitest.GetNGroupsFor1CoreWithNParams(
                N,
                masked_core_coord=(masked_core_coord.x, masked_core_coord.y),
            )
            self.assertEqual(len(a), 3)
            self.assertEqual(len(a[0]), N * 3)
            self.assertEqual(len(a[1]), N)
            self.assertEqual(len(a[2]), N * 3)

            attr = self.decoder.decode(a[0][:3])
            self.assertNotEqual(attr.get("core_coord"), masked_core_coord)
            
    def test_func_ReplaceCoreCoord_is_core_replaced(self) -> None:
        # Generate frames
        masked_core_coords = random_gen_core_coord(100)
        masked_core_coord = masked_core_coords[0]
        N = 10
        cf, ti, to = self.paitest.GetNGroupsFor1CoreWithNParams(
            N,
            masked_core_coord=(masked_core_coord.x, masked_core_coord.y),
        )
        
        # Replace
        for i in range(100):
            cf_replaced = self.paitest.ReplaceCoreCoord(cf, (masked_core_coord.x, masked_core_coord.y))
        
            # Decode
            attr = self.decoder.decode(cf_replaced[:3])
            self.assertEqual(attr.get("core_coord"), masked_core_coord)


    def tearDown(self) -> None:
        return super().tearDown()
