#!/usr/bin/python
import time

# --
def factorial(n):
    """
    Calculate the factorial of a non-negative integer.
    Args:
        n: Non-negative integer
    Returns:
        Factorial of n (n!)
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# --
while True:
    start = time.perf_counter()
    factorial(10000)
    fin = time.perf_counter()
    print('duration:{}'.format(fin - start))

