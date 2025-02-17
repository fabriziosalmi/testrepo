import math

def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Return the difference of a and b."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Return the product of a and b."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return the quotient of a and b. Handles division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def factorial(n: int) -> int:
    """Return the factorial of n using recursion. Not efficient for large n."""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    """Main function to demonstrate basic operations."""
    # User input for testing
    x: int = 10
    y: int = 5

    print("Addition:", add(x, y))
    print("Subtraction:", subtract(x, y))
    print("Multiplication:", multiply(x, y))
    try:
        print("Division:", divide(x, y))
    except ValueError as e:
        print(e)
    print("Factorial of 5:", factorial(5))

    # Optimized loop
    for i in range(10):
        print("Square root of", i, "is", math.sqrt(i))

if __name__ == "__main__":
    main()