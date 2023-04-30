from typing import Tuple, Dict
from BitMath import BitMath
import math

class TickBitmap:
    """
    TickBitmap class represents a data structure for managing and querying initialized ticks
    in a Uniswap V3 pool.
    """

    bitmap = dict()

    def __init__(self):
        """
        Initializes a new TickBitmap instance.
        """
        pass

    def position(self, _tick: int) -> Tuple[int, int]:
        """
        Calculates the word position and bit position of the given tick in the bitmap.

        :param _tick: The tick to find the position for.
        :return: A tuple containing the word position and bit position.
        """
        wordPos = int(_tick) >> 8
        bitPos = int(math.fabs(_tick % 256))

        return (wordPos, bitPos)

    def flipTick(self, _tick: int, _tickSpacing: int) -> None:
        """
        Flips the state of the given tick in the bitmap.

        :param _tick: The tick to flip.
        :param tickSpacing: The tick spacing to ensure the tick is correctly spaced.
        """
        assert(_tick % _tickSpacing == 0)
        wordPos, bitPos = self.position(_tick / _tickSpacing)
        mask = 1 << bitPos
        self.bitmap[wordPos] = self.bitmap.get(wordPos, 0) ^ mask

    def nextInitializedTickWithinOneWord(self, _tick: int, _tickSpacing: int, _lte: bool) -> Tuple[int, bool]:
        """
        Finds the next initialized tick within one 256-bit word of the bitmap.

        :param _tick: The reference tick.
        :param _tickSpacing: The tick spacing to ensure the tick is correctly spaced.
        :param _lte: Whether to search for ticks less than or equal to the reference tick, or greater than the reference tick.
        :return: A tuple containing the next initialized tick and a boolean indicating whether the tick is initialized.
        """
        compressed = _tick // _tickSpacing
        if _tick < 0 and _tick % _tickSpacing != 0:
            compressed -= 1

        if _lte:
            wordPos, bitPos = self.position(compressed)

            mask = (1 << int(bitPos)) - 1 + (1 << int(bitPos))
            masked = self.bitmap.get(wordPos, 0) & mask
            initialized = masked != 0

            if initialized:
                most_significant_bit = BitMath.most_significant_bit(masked)
                nextTick = (compressed - math.fabs(bitPos -  most_significant_bit)) * _tickSpacing
            else:
                nextTick = (compressed - bitPos) * _tickSpacing
        else:
            wordPos, bitPos = self.position(compressed + 1)

            mask = ~((1 << bitPos) - 1)
            masked = self.bitmap.get(wordPos, 0) & mask
            initialized = masked != 0

            if initialized:
                least_significant_bit = BitMath.least_significant_bit(masked)
                nextTick = (compressed + 1 + math.fabs(least_significant_bit - bitPos)) * _tickSpacing
            else:
                nextTick = (compressed + 1 + (255 - bitPos)) * _tickSpacing

        return (int(nextTick), initialized)

if __name__ == "__main__":
    
    ticks = [20, 40, 50, 80, 110, 120, 130, 200, 300]
    tickSpacing = 10

    tickBitmap = TickBitmap()
    for tick in ticks:
        tickBitmap.flipTick(tick, tickSpacing)
        print(bin(tickBitmap.bitmap[0]))

    t1 = tickBitmap.nextInitializedTickWithinOneWord(111, tickSpacing, True)
    t2 = tickBitmap.nextInitializedTickWithinOneWord(111, tickSpacing, False)
    t3 = tickBitmap.nextInitializedTickWithinOneWord(1110, tickSpacing, False)
    t4 = tickBitmap.nextInitializedTickWithinOneWord(1110, tickSpacing, True)
    t5 = tickBitmap.nextInitializedTickWithinOneWord(110, tickSpacing, False)
    print(tickBitmap.bitmap)