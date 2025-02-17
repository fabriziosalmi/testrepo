import logging
import math

# Configure logging with a more appropriate level for production environments
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)


def add(a: int, b: int) -> int:
    """Return the sum of a and b.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.
    """
    return a + b


def subtract(a: int, b: int) -> int:
    """Return the difference of a and b.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The difference of a and b.
    """
    return a - b


def multiply(a: int, b: int) -> int:
    """Return the product of a and b.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of a and b.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of a and b. Handles division by zero.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The quotient of a and b.

    Raises:
        ValueError: If division by zero is attempted.
    """
    if b == 0:
        raise ValueError("Cannot perform division by zero")
    return a / b


def factorial(n: int) -> int:
    """Return the factorial of n using an iterative approach. More efficient for large n.

    Args:
        n (int): The number to calculate the factorial of.

    Returns:
        int: The factorial of n.
    """
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


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