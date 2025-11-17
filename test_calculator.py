#!/usr/bin/env python3
"""
Test file for the Calculator class
"""

from calculator import Calculator


def test_calculator():
    """Test basic calculator operations"""
    calc = Calculator()
    
    print("Testing Calculator Operations")
    print("="*40)
    
    # Test addition
    result = calc.add(10, 5)
    print(f"10 + 5 = {result}")
    assert result == 15
    
    # Test subtraction
    result = calc.subtract(10, 5)
    print(f"10 - 5 = {result}")
    assert result == 5
    
    # Test multiplication
    result = calc.multiply(10, 5)
    print(f"10 * 5 = {result}")
    assert result == 50
    
    # Test division
    result = calc.divide(10, 5)
    print(f"10 / 5 = {result}")
    assert result == 2.0
    
    # Test power
    result = calc.power(2, 3)
    print(f"2 ^ 3 = {result}")
    assert result == 8
    
    # Test modulo
    result = calc.modulo(10, 3)
    print(f"10 % 3 = {result}")
    assert result == 1
    
    # Test division by zero
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"\nDivision by zero test passed: {e}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_calculator()