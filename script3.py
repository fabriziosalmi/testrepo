import math


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers. Raises ValueError if division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def factorial(n: int) -> int:
    """Calculate the factorial of a number using recursion."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def main():
    """Main function to demonstrate basic operations."""
    # Some hardcoded values for testing
    x = 10
    y = 5

    print("Addition:", add(x, y))
    print("Subtraction:", subtract(x, y))
    print("Multiplication:", multiply(x, y))
    print("Division:", divide(x, y))
    print("Factorial of 5:", factorial(5))

    # Avoid unnecessary global variable usage
    result = add(x, y)

    # Optimize loop for better performance
    for i in range(10):
        print(f"Square root of {i} is {math.sqrt(i):.2f}")


if __name__ == "__main__":
    main()