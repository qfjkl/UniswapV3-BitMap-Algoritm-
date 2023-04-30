# What is bitmap Algorithm?

A **bitmap algorithm** is a data structure and set of operations that use bit arrays (bitmaps) to represent and manipulate sets of data efficiently. Bitmap algorithms are often used for tasks like compression, encoding, or indexing, where the goal is to minimize storage requirements or processing time.

A **bitmap** is an array of bits, where each bit represents a state (e.g., true/false, 1/0, or set/unset) for an element in a dataset. By using bits rather than larger data structures, bitmap algorithms can greatly reduce the memory required to represent a dataset and optimize operations on that dataset.

Common operations performed using bitmap algorithms include:

**Set**: Set a particular bit to 1 or 0, indicating the presence or absence of an element in a dataset.

**Get**: Retrieve the value of a specific bit, indicating the presence or absence of an element in a dataset.

**Count**: Count the number of set bits (1s) in the bitmap, representing the number of elements in the dataset.

**Union**: Combine two bitmaps using the bitwise OR operation, resulting in a new bitmap representing the union of two datasets.

**Intersection**: Combine two bitmaps using the bitwise AND operation, resulting in a new bitmap representing the intersection of two datasets.

**Difference**: Combine two bitmaps using the bitwise AND and NOT operations, resulting in a new bitmap representing the difference between two datasets.

**Bitmap algorithms** can be applied to various use cases, such as databases, search engines, and graphics rendering. In the context of Uniswap V3, the TickBitmap is used to represent and manipulate the ticks where liquidity has been provided in a compact and efficient manner, allowing for optimized operations when working with the liquidity provided in the protocol.

## Break down Bitmap algorithm in case of UniswapV3

**Assume we have initialized ticks at the following tick indices: 20, 40, 50, 80, 110, 120, 130, 200, 300.**

**We'll use a hypothetical UniswapV3 pool with a tick spacing of 10 for simplicity.**

## Building Bitmap datas Structure

    Bitmap shape -> (wordPos, 256)
    Loop over all tick list
    
    Firt loop:
        tick = 20
        compressed = tick / tickSpacing -> (2)
        wordPos = compressed >> 8 -> (0)
        bitPos = compressed  % 256 -> (2)
        mask = 1 << bitPos -> (4)

        0 0 0 0
        1 1 1 1
        1 0 0 0  ( 0 XOR 4) 
        0 1 1 1
        -----------------
        1 0 0 0 -> Bitmap[wordPos] = 0 ^ mask -> 4

    Second loop:
        tick = 40
        compressed = tick / tickSpacing -> (4)
        wordPos = compressed >> 8 -> (0)
        bitPos = compressed  % 256 -> (4)
        mask = 1 << bitPos -> (16)

        0 1 0 0 0
        1 1 1 1 1
        1 0 0 0 0 (4 XOR 16) 
        0 1 1 1 1
        -----------------
        1 1 0 0 0 -> Bitmap[wordPos] = 4 ^ mask -> (20) 

    .   .   .   .   .
    .   .   .   .   .

    last loop:
        tick = 300
        compressed = tick / tickSpacing -> (30)
        wordPos = compressed >> 8 -> (0)
        bitPos = compressed  % 256 -> (30)
        mask = 1 << bitPos -> (1073741824)

        0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 0 0 1 0 0 1 1 0 1 0 0
        0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 1 1 0 1 1 0 0 1 0 1 1
        1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0   (1063220 XOR 1073741824)
        0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
        ---------------------------------------------------------------------
        1 1 0 0 0 -> Bitmap[wordPos] = 4 ^ mask -> (20) 

## **Finding Next Initialized Tick Within One Word Step**

    tick = 111
    tickSpacing = 10
    zeroForOne = true

    compressed = tick / tickSpacing -> (11)

    zeroForOne == true

        wordPos = int(compressed) >> 8 -> 0
        bitPos = int(compressed) % 256 -> (11)
        mask = (1 << int(bitPos)) - 1 + (1 << int(bitPos))
        1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 0 0 1 0 0 1 1 0 1 0 0 -> bitmap
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 -> mask
        ----------------------------------------------------------------------------------
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 1 1 0 1 0 0 -> masked = bitmap & mask

        masked != 0
            most_significant_bit_of_masked = (11)
            nextTick = (compressed - bitPos - most_significant_bit_of_masked) * tickSpacing
        
        masked == 0
            nextTick = (compressed - bitPos) * _tickSpacing

    zeroForOne == false

        wordPos = int(compressed + 1) >> 8 -> (0)
        bitPos = int(compressed + 1) % 256 -> (12)
        mask = ~((1 << bitPos) - 1) -> (-4096)
        1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 0 0 1 0 0 1 1 0 1 0 0 -> bitmap
        1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 -> mask
        -------------------------------------------------------------------------
        1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 -> masked = bitmap & mask (1074802688)

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
