# Break down Bitmap algorithm in case of UniswapV3

**Assume we have initialized ticks at the following tick indices: 20, 40, 50, 80, 110, 120, 130, 200, 300.**
**We'll use a hypothetical UniswapV3 pool with a tick spacing of 10 for simplicity.**

## **Finding Next Initialized Tick Within One Word Step**

    tick = 111
    tickSpacing = 10
    zeroForOne = true

    compressed = tick / tickSpacing -> (11)

    zeroForOne == true

        wordPos = int(compressed) >> 8 -> 0
        bitPos = int(compressed) % 256 -> (11)
        mask = (1 << int(bitPos)) - 1 + (1 << int(bitPos))
        1000000000100000011100100110100 -> bitmap
        0000000000000000000111111111111 -> mask
        ---------------------------------------------------------
        0000000000000000000100100110100 -> masked = bitmap & mask

        masked != 0
            most_significant_bit_of_masked = (11)
            nextTick = (compressed - bitPos - most_significant_bit_of_masked) * tickSpacing
        
        masked == 0
            nextTick = (compressed - bitPos) * _tickSpacing

    zeroForOne == false

        wordPos = int(compressed + 1) >> 8 -> (0)
        bitPos = int(compressed + 1) % 256 -> (12)
        mask = ~((1 << bitPos) - 1) -> (-4096)
        1000000000100000011100100110100 -> bitmap
        1111111111111111111000000000000 -> mask
        --------------------------------------------------------
        1000000000100000011000000000000 -> masked = bitmap & mask (1074802688)

        masked != 0
            least_significant_bit_of_masked = 12
            nextTick = (compressed + 1 + least_significant_bit_of_masked - bitPos) * _tickSpacing -> (120)

        masked == 0
            nextTick = (compressed + 1 + (255 - bitPos)) * _tickSpacing

## **Result Of Seach**

## _masked != 0_

    zeroForOne = True
    nextTick = 110

    zeroForOne = False
    nextTick = 120

## _masked == 0_

    zeroForOne = True
    nextTick = 0

    zeroForOne = False
    nextTick = 2550

## **Most Significant Bit Step**

    masked = 2356
    x = masked
    r = 0

    x >= (1 << 8)
        x = (100100110100) >> 8 = 1001 -> (9)
        r = 8
    x >= (1 << 2)
        x = (1001) >> 2 = 10 -> (2)
        r = r + 2
    x >= 2
        r = r + 1

## **Result**

    Most significant bit = 11

## **least Significant Bit Step**

    masked = 1074802688 (1000000000100000011000000000000)
    x = masked
    r = 255

    x & ((1 << 128) -1) > 0
        r = r - 128
    x & ((1 << 64) - 1) > 0
        r = r - 64
    x & ((1 << 32) - 1) > 0
        r = r - 32
    x & ((1 << 16) - 1) > 0
        r = r - 16
    x & ((1 << 8) - 1) == 0
        x = x >> 8 -> 4198448 (10000000001000000110000)
    x & ((1 << 4) - 1) == 0
        x = x >> 4 -> 262403 (1000000000100000011)
    x & ((1 << 2) - 1) > 0
        r = r - 2
    (x & 1) > 0
        r = r - 1

## **Result :**

    Least significant Bit = 12 
