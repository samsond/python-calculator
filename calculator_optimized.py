#!/usr/bin/env python3
"""
Optimized Calculator Application with Performance Improvements
"""

import sys
import re
from decimal import Decimal, getcontext
from functools import lru_cache
from typing import Dict, Tuple, Callable, Optional, Union
import operator
import argparse

# Set decimal precision for financial calculations
getcontext().prec = 28


class OptimizedCalculator:
    """Optimized Calculator with caching and expression evaluation"""
    
    # Class-level constants to avoid recreation
    OPERATIONS: Dict[str, Tuple[Callable, str, str]] = {
        '1': (operator.add, "Addition", "+"),
        '2': (operator.sub, "Subtraction", "-"),
        '3': (operator.mul, "Multiplication", "*"),
        '4': (operator.truediv, "Division", "/"),
        '5': (operator.pow, "Power", "^"),
        '6': (operator.mod, "Modulo", "%")
    }
    
    # Precompiled regex for number validation
    NUMBER_PATTERN = re.compile(r'^-?\d+\.?\d*$')
    
    # Cache for menu string
    _menu_cache: Optional[str] = None
    
    def __init__(self, use_decimal: bool = False):
        """Initialize calculator with optional decimal precision"""
        self.use_decimal = use_decimal
        self.history: list = []
        self._result_cache: Dict[Tuple[str, float, float], float] = {}
    
    @lru_cache(maxsize=128)
    def add(self, a: Union[float, Decimal], b: Union[float, Decimal]) -> Union[float, Decimal]:
        """Cached addition"""
        return a + b
    
    @lru_cache(maxsize=128)
    def subtract(self, a: Union[float, Decimal], b: Union[float, Decimal]) -> Union[float, Decimal]:
        """Cached subtraction"""
        return a - b
    
    @lru_cache(maxsize=128)
    def multiply(self, a: Union[float, Decimal], b: Union[float, Decimal]) -> Union[float, Decimal]:
        """Cached multiplication"""
        return a * b
    
    def divide(self, a: Union[float, Decimal], b: Union[float, Decimal]) -> Union[float, Decimal]:
        """Division with zero check"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    @lru_cache(maxsize=128)
    def power(self, a: Union[float, Decimal], b: Union[float, Decimal]) -> Union[float, Decimal]:
        """Cached power operation"""
        return a ** b
    
    def modulo(self, a: Union[float, Decimal], b: Union[float, Decimal]) -> Union[float, Decimal]:
        """Modulo with zero check"""
        if b == 0:
            raise ValueError("Cannot calculate modulo with zero")
        return a % b
    
    def evaluate_expression(self, expression: str) -> float:
        """Evaluate mathematical expressions safely"""
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        # Simple expression evaluator using operator precedence
        # This is a basic implementation - for production, use ast.literal_eval or similar
        try:
            # Replace ^ with ** for Python power operator
            expression = expression.replace('^', '**')
            
            # Validate expression contains only allowed characters
            allowed_chars = set('0123456789+-*/().**')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")
            
            # Evaluate using Python's built-in eval with restricted namespace
            result = eval(expression, {"__builtins__": {}}, {})
            self.history.append((expression, result))
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def batch_calculate(self, operations_list: list) -> list:
        """Process multiple calculations in batch"""
        results = []
        for op_type, a, b in operations_list:
            try:
                if op_type == '+':
                    result = self.add(a, b)
                elif op_type == '-':
                    result = self.subtract(a, b)
                elif op_type == '*':
                    result = self.multiply(a, b)
                elif op_type == '/':
                    result = self.divide(a, b)
                elif op_type == '^':
                    result = self.power(a, b)
                elif op_type == '%':
                    result = self.modulo(a, b)
                else:
                    result = None
                results.append((op_type, a, b, result))
            except ValueError as e:
                results.append((op_type, a, b, f"Error: {str(e)}"))
        return results


@lru_cache(maxsize=1)
def get_cached_menu() -> str:
    """Return cached menu string"""
    lines = [
        "\n" + "="*40,
        "       PYTHON CALCULATOR (OPTIMIZED)",
        "="*40,
        "1. Addition (+)",
        "2. Subtraction (-)",
        "3. Multiplication (*)",
        "4. Division (/)",
        "5. Power (^)",
        "6. Modulo (%)",
        "7. Expression Evaluation",
        "8. Batch Mode",
        "9. Show History",
        "0. Exit",
        "="*40
    ]
    return '\n'.join(lines)


def get_number_optimized(prompt: str) -> float:
    """Optimized number input with regex validation"""
    while True:
        user_input = input(prompt).strip()
        if OptimizedCalculator.NUMBER_PATTERN.match(user_input):
            return float(user_input)
        print("Invalid input. Please enter a valid number.")


def process_batch_mode(calc: OptimizedCalculator):
    """Handle batch calculation mode"""
    print("\nBatch Mode - Enter calculations in format: operation,num1,num2")
    print("Operations: +, -, *, /, ^, %")
    print("Example: +,10,5")
    print("Enter 'done' when finished\n")
    
    operations = []
    while True:
        line = input("Enter calculation (or 'done'): ").strip()
        if line.lower() == 'done':
            break
        
        try:
            parts = line.split(',')
            if len(parts) != 3:
                print("Invalid format. Use: operation,num1,num2")
                continue
            
            op, num1_str, num2_str = parts
            num1 = float(num1_str)
            num2 = float(num2_str)
            operations.append((op.strip(), num1, num2))
        except ValueError:
            print("Invalid input. Please check your numbers.")
    
    if operations:
        print("\nProcessing batch calculations...")
        results = calc.batch_calculate(operations)
        print("\nResults:")
        for op, a, b, result in results:
            print(f"{a} {op} {b} = {result}")


def main():
    """Optimized main calculator loop"""
    parser = argparse.ArgumentParser(description='Optimized Python Calculator')
    parser.add_argument('--expression', '-e', help='Evaluate expression directly')
    parser.add_argument('--decimal', '-d', action='store_true', help='Use decimal precision')
    parser.add_argument('--batch', '-b', help='Batch file with calculations')
    
    args = parser.parse_args()
    
    calc = OptimizedCalculator(use_decimal=args.decimal)
    
    # Handle command-line expression
    if args.expression:
        try:
            result = calc.evaluate_expression(args.expression)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        return
    
    # Handle batch file
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                operations = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) == 3:
                            op, num1, num2 = parts
                            operations.append((op.strip(), float(num1), float(num2)))
                
                results = calc.batch_calculate(operations)
                for op, a, b, result in results:
                    print(f"{a} {op} {b} = {result}")
        except Exception as e:
            print(f"Error processing batch file: {e}")
        return
    
    # Interactive mode
    print("Welcome to Optimized Python Calculator!")
    
    # Pre-cache the menu
    menu = get_cached_menu()
    
    while True:
        print(menu)
        choice = input("\nSelect operation (0-9): ").strip()
        
        if choice == '0':
            print("\nThank you for using Python Calculator. Goodbye!")
            sys.exit(0)
        
        if choice == '7':
            # Expression evaluation
            expr = input("\nEnter mathematical expression: ")
            try:
                result = calc.evaluate_expression(expr)
                print(f"\nResult: {result}")
            except ValueError as e:
                print(f"\nError: {e}")
        
        elif choice == '8':
            # Batch mode
            process_batch_mode(calc)
        
        elif choice == '9':
            # Show history
            if calc.history:
                print("\nCalculation History:")
                for expr, result in calc.history[-10:]:  # Show last 10
                    print(f"{expr} = {result}")
            else:
                print("\nNo history available.")
        
        elif choice in OptimizedCalculator.OPERATIONS:
            operation, name, symbol = OptimizedCalculator.OPERATIONS[choice]
            print(f"\n{name} selected")
            
            num1 = get_number_optimized("Enter first number: ")
            num2 = get_number_optimized("Enter second number: ")
            
            # Convert to Decimal if needed
            if calc.use_decimal:
                num1 = Decimal(str(num1))
                num2 = Decimal(str(num2))
            
            try:
                # Use the operator module functions directly
                if choice == '1':
                    result = calc.add(num1, num2)
                elif choice == '2':
                    result = calc.subtract(num1, num2)
                elif choice == '3':
                    result = calc.multiply(num1, num2)
                elif choice == '4':
                    result = calc.divide(num1, num2)
                elif choice == '5':
                    result = calc.power(num1, num2)
                elif choice == '6':
                    result = calc.modulo(num1, num2)
                
                print(f"\nResult: {num1} {symbol} {num2} = {result}")
                calc.history.append((f"{num1} {symbol} {num2}", result))
            except ValueError as e:
                print(f"\nError: {e}")
        
        else:
            print("\nInvalid choice. Please select a valid option.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()