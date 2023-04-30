# **next Initialized Tick Within One Word**

    tick = 111
    tickSpacing = 10
    compressed = int24(tick / tickSpacing)

    # **tick < 0 and tick % _tickSpacing != 0**

        compressed--

    # **zeroForOne == true**

        wordPos = int(compressed) >> 8
        bitPos = int(compressed) % 256
        mask = (1 << int(bitPos)) - 1 + (1 << int(bitPos))
        1000000000100000011100100110100 -> bitmap
        0000000000000000000111111111111 -> mask
        ---------------------------------------------------------
        0000000000000000000100100110100 -> masked = bitmap & mask

        **masked != 0**
            nextTick = (compressed - int(bitPos - most_significant_bit(masked))) * tickSpacing
        **masked == 0**
            nextTick = (compressed - bitPos) * _tickSpacing

    # zeroForOne == false

        wordPos = int(compressed + 1) >> 8
        bitPos = int(compressed + 1) % 256
        mask = ~((1 << bitPos) - 1)
        1000000000100000011100100110100 -> bitmap
        1111111111111111111000000000000 -> mask
        --------------------------------------------------------
        1000000000100000011000000000000 -> masked = bitmap & mask

        masked != 0
            nextTick = (compressed + 1 + int(least_significant_bit(masked) - bitPos)) * _tickSpacing
        masked == 0
            nextTick = (compressed + 1 + (255 - bitPos)) * _tickSpacing

>>>>>>> 448f8f1 (First commit)
