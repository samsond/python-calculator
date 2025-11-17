#!/usr/bin/env python3
"""
Simple Calculator Application
Supports basic arithmetic operations: addition, subtraction, multiplication, and division
"""

import sys


class Calculator:
    """Calculator class with basic arithmetic operations"""
    
    def add(self, a, b):
        """Add two numbers"""
        return a + b
    
    def subtract(self, a, b):
        """Subtract b from a"""
        return a - b
    
    def multiply(self, a, b):
        """Multiply two numbers"""
        return a * b
    
    def divide(self, a, b):
        """Divide a by b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, a, b):
        """Raise a to the power of b"""
        return a ** b
    
    def modulo(self, a, b):
        """Calculate a modulo b"""
        if b == 0:
            raise ValueError("Cannot calculate modulo with zero")
        return a % b


def get_number(prompt):
    """Get a valid number from user input"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def display_menu():
    """Display the calculator menu"""
    print("\n" + "="*40)
    print("       PYTHON CALCULATOR")
    print("="*40)
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Power (^)")
    print("6. Modulo (%)")
    print("7. Exit")
    print("="*40)


def main():
    """Main calculator loop"""
    calc = Calculator()
    
    operations = {
        '1': (calc.add, "Addition", "+"),
        '2': (calc.subtract, "Subtraction", "-"),
        '3': (calc.multiply, "Multiplication", "*"),
        '4': (calc.divide, "Division", "/"),
        '5': (calc.power, "Power", "^"),
        '6': (calc.modulo, "Modulo", "%")
    }
    
    print("Welcome to Python Calculator!")
    
    while True:
        display_menu()
        choice = input("\nSelect operation (1-7): ").strip()
        
        if choice == '7':
            print("\nThank you for using Python Calculator. Goodbye!")
            sys.exit(0)
        
        if choice not in operations:
            print("\nInvalid choice. Please select a valid option.")
            continue
        
        operation, name, symbol = operations[choice]
        print(f"\n{name} selected")
        
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
        
        try:
            result = operation(num1, num2)
            print(f"\nResult: {num1} {symbol} {num2} = {result}")
        except ValueError as e:
            print(f"\nError: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()