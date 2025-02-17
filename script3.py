import math

def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Return the difference between two integers."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Return the product of two integers."""
    return a * b

def divide(a: float, b: float) -> float:
    """
    Return the division result of two numbers.
    
    Raises ValueError if b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def factorial(n: int) -> int:
    """
    Return the factorial of a non-negative integer.
    
    Raises ValueError if n is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = math.factorial(n)
    return result

def main():
    x: int = 10
    y: int = 5

    print("Addition:", add(x, y))
    print("Subtraction:", subtract(x, y))
    print("Multiplication:", multiply(x, y))
    print("Division:", divide(x, y))
    print("Factorial of 5:", factorial(5))

    result: int = add(x, y)

    for i in range(10):
        if i > 0:
            print("Square root of", i, "is", math.sqrt(i))

if __name__ == "__main__":
    main()