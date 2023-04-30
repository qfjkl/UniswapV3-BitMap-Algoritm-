class BitMath:
    """
    BitMath class provides functionality for computing bit properties of an unsigned integer.
    """

    @staticmethod
    def most_significant_bit(x: int) -> int:
        """
        Returns the index of the most significant bit of the number, where the least significant
        bit is at index 0 and the most significant bit is at index 255.
        
        :param x: The value for which to compute the most significant bit, must be greater than 0.
        :return: The index of the most significant bit.
        """
        assert x > 0
        r = 0

        if x >= (1 << 128):
            x >>= 128
            r += 128
        if x >= (1 << 64):
            x >>= 64
            r += 64
        if x >= (1 << 32):
            x >>= 32
            r += 32
        if x >= (1 << 16):
            x >>= 16
            r += 16
        if x >= (1 << 8):
            x >>= 8
            r += 8
        if x >= (1 << 4):
            x >>= 4
            r += 4
        if x >= (1 << 2):
            x >>= 2
            r += 2
        if x >= 2:
            r += 1

        return r

    @staticmethod
    def least_significant_bit(x: int) -> int:
        """
        Returns the index of the least significant bit of the number, where the least significant
        bit is at index 0 and the most significant bit is at index 255.
        
        :param x: The value for which to compute the least significant bit, must be greater than 0.
        :return: The index of the least significant bit.
        """
        assert x > 0
        r = 255

        if (x & ((1 << 128) - 1)) > 0:
            r -= 128
        else:
            x >>= 128
        if (x & ((1 << 64) - 1)) > 0:
            r -= 64
        else:
            x >>= 64
        if (x & ((1 << 32) - 1)) > 0:
            r -= 32
        else:
            x >>= 32
        if (x & ((1 << 16) - 1)) > 0:
            r -= 16
        else:
            x >>= 16
        if (x & ((1 << 8) - 1)) > 0:
            r -= 8
        else:
            x >>= 8
        if (x & ((1 << 4) - 1)) > 0:
            r -= 4
        else:
            x >>= 4
        if (x & ((1 << 2) - 1)) > 0:
            r -= 2
        else:
            x >>= 2
        if (x & 1) > 0:
            r -= 1

        return r
