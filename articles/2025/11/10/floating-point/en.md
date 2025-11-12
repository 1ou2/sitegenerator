---
title: Floating point
date: 2025-11-11
tags: byte, fp, int
thumbnail: IEEE754-fp32.png
abstract: A concrete overview of IEEE 754 representation: mantissa, exponent, precision, rounding errors. We dismantle the machine and look exactly at how numbers are stored in memory and why `0.1` doesn't really exist in binary.
language: en
---

# The bug: 0.1 + 0.1 + 0.1 != 0.3
Let's test some basic calculations in Python:
- Verify that `0.1 + 0.1` equals `0.2`
- That `0.1 + 0.1 + 0.1 = 0.3`
- Or that we can change the order of calculations in an addition (that addition is commutative)

[![Floating point bug](bug-fp-python.png)](bug-fp-python.png)
That's the drama! When we test, we have `0.1 + 0.1 = 0.2` but on the other hand `0.1 + 0.1 + 0.1 != 0.3`.
We have `0.1 + (1e20 - 1e20) = 0.1` but on the other hand `(0.1 + 1e20) - 1e20 = 0.0`.

A Python bug? A problem in the code? No, it's related to number representation.
Let's explore how machines store numbers!

# Base 10 vs Base 2
Let's start with the base...
We use the decimal system (`base 10`) daily, with 10 digits (`0` to `9`). In computing, we use binary (`base 2`), with only two digits: `0` and `1`.
Each position in a binary number represents a power of 2, similar to how each position in a decimal number represents a power of 10.
For example, in our decimal system `123.45` actually corresponds to:

    1 × 10² + 2 × 10¹ + 3 × 10⁰ + 4 × 10⁻¹ + 5 × 10⁻²

In binary, the number `1101.101` corresponds to:
    
    1 × 2³ + 1 × 2² + 0 × 2¹ + 1 x 2⁰ + 1 x 2⁻¹ + 0 * 2⁻² + 1 x 2⁻³

## Integer representation in base 2
In binary, integers are represented using bits (`0` and `1`). For example, the decimal number 13 is written in binary as `1101`:
    
    1 × 2³ + 1 × 2² + 0 × 2¹ + 1 × 2⁰ = 8 + 4 + 0 + 1 = 13

If we look at what this gives in Python:
```python
>>> bin(13)
'0b1101'
```

# Dtype
In Python, floating point numbers are represented using the `float` type, which corresponds to a double precision floating point format (64 bits) according to the `IEEE 754` standard.
However, for applications requiring more precise decimal number handling, Python also offers the `decimal` module which allows working with decimal numbers using a base 10 representation.

# The IEEE 754 standard
The IEEE 754 standard defines how floating point numbers are represented in memory. It's the universal standard used by virtually all modern processors and programming languages.

## Structure of a floating point number
A floating point number in IEEE 754 format consists of three parts:
1. **Sign bit** (1 bit): Determines if the number is positive (0) or negative (1)
2. **Exponent** (8 bits for float32, 11 bits for float64): Represents the power of 2
3. **Mantissa/Fraction** (23 bits for float32, 52 bits for float64): The significant digits

The actual formula is:
    (-1)^sign × (1 + mantissa) × 2^(exponent - bias)

Where the bias is 127 for float32 and 1023 for float64.

## Why 0.1 doesn't exist in binary
The problem comes from the fact that 0.1 in decimal cannot be exactly represented in binary, just like 1/3 cannot be exactly represented in decimal (0.333...).

In binary, 0.1 decimal becomes an infinite repeating fraction:
    0.1₁₀ = 0.0001100110011...₂

Since we only have a finite number of bits to store the mantissa, we must round, which introduces a small error.

```python
>>> 0.1
0.1
>>> format(0.1, '.17f')
'0.10000000000000001'
```

This is why `0.1 + 0.1 + 0.1` doesn't exactly equal `0.3` - each 0.1 has a tiny error that accumulates.

# Practical implications
Understanding floating point representation is crucial for:
- Financial calculations (use `decimal` module instead)
- Scientific computing (be aware of precision limits)
- Equality comparisons (never use `==` with floats)

Instead of:
```python
if a == 0.3:  # Don't do this!
    print("Equal")
```

Use:
```python
import math
if math.isclose(a, 0.3):
    print("Equal")
```

# Conclusion
Floating point numbers are an approximation of real numbers, constrained by the finite precision of computer memory. The IEEE 754 standard provides a consistent way to represent these approximations, but understanding its limitations is essential for writing robust numerical code.

The next time you see floating point "bugs", remember: it's not a bug, it's a feature of how computers represent infinite precision mathematics in finite memory!