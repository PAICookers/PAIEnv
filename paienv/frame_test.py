import unittest
import random
from itertools import product
from paitest.frames.frame import FrameGen, Coord, Coord2Addr, Addr2Coord, CoordOffset, Direction, FrameDecoder
from paitest.frames.frame_params import ConfigFrameMask as CFM


def test_chip_coord_split(coord: Coord) -> tuple[int, int]:
    addr = Coord2Addr(coord)
    high3 = (
        addr >> CFM.TEST_CHIP_ADDR_COMBINATION_OFFSET) & CFM.TEST_CHIP_ADDR_HIGH3_MASK
    low7 = addr & CFM.TEST_CHIP_ADDR_LOW7_MASK

    return high3, low7


def test_chip_addr_combine(high3: int, low7: int) -> Coord:
    _high3 = high3 & CFM.TEST_CHIP_ADDR_HIGH3_MASK
    _low7 = low7 & CFM.TEST_CHIP_ADDR_LOW7_MASK

    addr = (_high3 << CFM.TEST_CHIP_ADDR_COMBINATION_OFFSET) | _low7

    return Addr2Coord(addr)


class CoordAttrTestCase(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_Coord_init_assertion_test(self):
        for i in range(-31, 32):
            for j in range(-31, 32):
                if i < 0 or j < 0:
                    with self.assertRaises(ValueError):
                        a = Coord(i, j)

    def test_CoordOffset_init_assertion(self):
        for i in range(-31, 32):
            for j in range(-31, 32):
                a = CoordOffset(i, j)

    def test_Coord_Direction_alg(self):

        core_coord_list = list(product(range(32), range(32)))
        dirc_list = list(Direction)

        for core_coord in core_coord_list:
            for dirc in dirc_list:
                if (0 <= core_coord[0] + dirc.value.x < 32) and (0 <= core_coord[1] + dirc.value.y < 32):
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

        coord1 = Coord(16, 20)
        coord2 = Coord(16, 16)
        coord3 = Coord(15, 8)
        coord4 = Coord(2, 1)
        coord5 = Coord(15, 31)

        self.assertLessEqual(coord2, coord1)
        self.assertLess(coord3, coord2)
        self.assertGreater(coord5, coord4)
        self.assertEqual(coord4, Coord(2, 1))
        self.assertGreaterEqual(coord1, coord2)

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
            coord_list.append(
                Coord(random.randint(0, 31), random.randint(0, 31)))

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
                output[1] >> CFM.TEST_CHIP_ADDR_HIGH3_OFFSET) & CFM.TEST_CHIP_ADDR_HIGH3_MASK
            test_chip_addr_low7 = (
                output[2] >> CFM.TEST_CHIP_ADDR_LOW7_OFFSET) & CFM.TEST_CHIP_ADDR_LOW7_MASK

            output_test_chip_addr = (
                test_chip_addr_high3 << CFM.TEST_CHIP_ADDR_COMBINATION_OFFSET) | test_chip_addr_low7

            self.assertEqual(output_test_chip_addr,
                             Coord2Addr(test_chip_coord_input))

    def tearDown(self) -> None:
        return super().tearDown()


class FrameDecoderTestCase(unittest.TestCase):

    def setUp(self) -> None:

        self.decoder = FrameDecoder()
        self.valid_type_list = [
            0b0000, 0b0001, 0b0010, 0b0011,
            0b0100, 0b0101, 0b0110, 0b0111,
            0b1000, 0b1001, 0b1010, 0b1011
        ]
        self.random_frames_list = []

        for _ in range(100):
            self.random_frames_list.append(random.randint(0, (1 << 64) - 1))

        return super().setUp()

    def test_subtype_property_test(self):
        pass

    def test_payload_property_test(self):
        pass

    def test_decode_test(self):
        pass

    def tearDown(self) -> None:
        return super().tearDown()
