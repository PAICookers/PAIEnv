from paitest import GenTestCases, TestChipDirection
from pathlib import Path


if __name__ == "__main__":
    GenTestCases(Path("./test"), TestChipDirection.EAST, 10)