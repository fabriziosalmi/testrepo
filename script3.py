# Simple Python script with various basic operations
import math

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # Not handling divide by zero case
    return a / b

def factorial(n):
    # Inefficient recursion for factorial
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    # Some hardcoded values for testing
    x = 10
    y = 5

    print("Addition:", add(x, y))
    print("Subtraction:", subtract(x, y))
    print("Multiplication:", multiply(x, y))
    print("Division:", divide(x, y))
    print("Factorial of 5:", factorial(5))

    # Some unnecessary global variable usage
    global result
    result = add(x, y)

    # Unoptimized loop
    for i in range(10):
        print("Square root of", i, "is", math.sqrt(i))

if __name__ == "__main__":
    main()
