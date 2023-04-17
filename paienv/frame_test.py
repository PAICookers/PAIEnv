import unittest
import random
from itertools import product
from typing import List, Tuple
from paitest.frames.frame import (
    FrameGen,
    Coord,
    Coord2Addr,
    Addr2Coord,
    CoordOffset,
    Direction,
    FrameDecoder,
    FrameGen,
)
from paitest.frames.frame_params import ConfigFrameMask as CFM


def test_chip_coord_split(coord: Coord) -> Tuple[int, int]:
    addr = Coord2Addr(coord)
    high3 = (
        addr >> CFM.TEST_CHIP_ADDR_COMBINATION_OFFSET
    ) & CFM.TEST_CHIP_ADDR_HIGH3_MASK
    low7 = addr & CFM.TEST_CHIP_ADDR_LOW7_MASK

    return high3, low7


def test_chip_addr_combine(high3: int, low7: int) -> Coord:
    _high3 = high3 & CFM.TEST_CHIP_ADDR_HIGH3_MASK
    _low7 = low7 & CFM.TEST_CHIP_ADDR_LOW7_MASK

    addr = (_high3 << CFM.TEST_CHIP_ADDR_COMBINATION_OFFSET) | _low7

    return Addr2Coord(addr)


def random_gen_core_coord(N: int) -> List[Coord]:
    def _CoordGenerator():
        coordinates = set()

        while True:
            x = random.randint(0, 31)
            y = random.randint(0, 31)

            if (x, y) not in coordinates and Coord(x, y) < Coord(0b11100, 0b11100):
                coordinates.add((x, y))
                yield Coord(x, y)

    generator = _CoordGenerator()
    core_coord_list = [next(generator) for _ in range(N)]

    return core_coord_list


class CoordAttrTestCase(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_Coord_init_assertion(self):
        for i in range(-31, 32):
            for j in range(-31, 32):
                if i < 0 or j < 0:
                    with self.assertRaises(ValueError):
                        a = Coord(i, j)
                else:
                    if random.random() < 0.5:
                        a = Coord(i, j)
                    else:
                        coord_tuple = (i, j)
                        a = Coord(coord_tuple)
        
        with self.assertRaises(ValueError):
            a = Coord([1, 2])
        
        with self.assertRaises(ValueError):
            a = Coord((1, 2), 2)
        
        with self.assertRaises(ValueError):
            a = Coord(1)
        
        a = Coord((1, 2))

    def test_CoordOffset_init_assertion(self):
        for i in range(-32, 32):
            for j in range(-32, 32):
                if i < -31 or j < -31:
                    with self.assertRaises(ValueError):
                        offset = CoordOffset(i, j)

    def test_Coord_Direction_alg(self):
        core_coord_list = list(product(range(32), range(32)))
        dirc_list = list(Direction)

        for core_coord in core_coord_list:
            for dirc in dirc_list:
                if (0 <= core_coord[0] + dirc.value.x < 32) and (
                    0 <= core_coord[1] + dirc.value.y < 32
                ):
                    test_chip_coord = Coord(core_coord) + dirc.value
                    # Coord + CoordOffset = Coord
                    self.assertIsInstance(test_chip_coord, Coord)
                    # Coord - Coord = CoordOffset
                    offset = test_chip_coord - Coord(core_coord)
                    self.assertIsInstance(offset, CoordOffset)
                else:
                    with self.assertRaises(ValueError):
                        test_chip_coord = Coord(core_coord) + dirc.value

    def test_Coord_compare(self):
        coord_std = Coord(16, 16)
        coords = [
            Coord(17, 18),
            Coord(16, 17),
            Coord(17, 16),
            Coord(16, 16),
            Coord(15, 16),
            Coord(16, 15),
            Coord(6, 14),
            Coord(17, 15),
            Coord(15, 17),
        ]

        self.assertGreater(coords[0], coord_std)
        self.assertGreaterEqual(coords[1], coord_std)
        self.assertGreaterEqual(coords[2], coord_std)
        self.assertEqual(coords[3], coord_std)
        self.assertEqual(coords[3], (16, 16))
        self.assertLessEqual(coords[4], coord_std)
        self.assertLessEqual(coords[5], coord_std)
        self.assertLess(coords[6], coord_std)
        self.assertLess(coords[7], coord_std)
        self.assertLess(coords[8], coord_std)

    def tearDown(self) -> None:
        return super().tearDown()


class TestChipTestCase(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_test_chip_split(self):
        coord_list = list(product(range(32), range(32)))

        for coord in coord_list:
            addr = Coord2Addr(Coord(coord))
            out_high3, out_low7 = test_chip_coord_split(Coord(coord))

            self.assertEqual(out_high3, int(addr / 128))
            self.assertEqual(out_low7, int(addr % 128))

    def test_test_chip_combine(self):
        coord_list = []

        for _ in range(1000):
            coord_list.append(Coord(random.randint(0, 31), random.randint(0, 31)))

        for coord in coord_list:
            high3, low7 = test_chip_coord_split(coord)
            out_coord = test_chip_addr_combine(high3, low7)

            self.assertEqual(out_coord.x, coord.x)
            self.assertEqual(out_coord.y, coord.y)

    def tearDown(self) -> None:
        return super().tearDown()


class FrameGenFunctionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_func_GenParamReg_random_test(self):
        test_chip_coord_input_list: list[Coord] = []
        output = []

        for i in range(32):
            for j in range(32):
                test_chip_coord_input_list.append(Coord(i, j))

        for test_chip_coord_input in test_chip_coord_input_list:
            output = FrameGen._GenParamReg(test_chip_coord_input)

            self.assertEqual(len(output), 3)

            test_chip_addr_high3 = (
                output[1] >> CFM.TEST_CHIP_ADDR_HIGH3_OFFSET
            ) & CFM.TEST_CHIP_ADDR_HIGH3_MASK
            test_chip_addr_low7 = (
                output[2] >> CFM.TEST_CHIP_ADDR_LOW7_OFFSET
            ) & CFM.TEST_CHIP_ADDR_LOW7_MASK

            output_test_chip_addr = (
                test_chip_addr_high3 << CFM.TEST_CHIP_ADDR_COMBINATION_OFFSET
            ) | test_chip_addr_low7

            self.assertEqual(output_test_chip_addr, Coord2Addr(test_chip_coord_input))

    def tearDown(self) -> None:
        return super().tearDown()


class FrameDecoderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.decoder = FrameDecoder()
        self.valid_type_list = [
            0b0000,
            0b0001,
            0b0010,
            0b0011,
            0b0100,
            0b0101,
            0b0110,
            0b0111,
            0b1000,
            0b1001,
            0b1010,
            0b1011,
        ]

        return super().setUp()

    def test_decode_info(self):
        pass

    def tearDown(self) -> None:
        return super().tearDown()
