#!/usr/bin/env python3
"""
Performance benchmark comparing original and optimized calculator implementations
"""

import time
import random
import statistics
from calculator import Calculator
from calculator_optimized import OptimizedCalculator, get_cached_menu


def benchmark_basic_operations(iterations=10000):
    """Benchmark basic arithmetic operations"""
    print(f"\nBenchmarking basic operations ({iterations} iterations)...")
    
    # Generate random test data
    test_data = [(random.uniform(1, 1000), random.uniform(1, 1000)) 
                 for _ in range(iterations)]
    
    # Test original calculator
    calc_original = Calculator()
    start_time = time.perf_counter()
    for a, b in test_data:
        calc_original.add(a, b)
        calc_original.subtract(a, b)
        calc_original.multiply(a, b)
        calc_original.divide(a, b)
    original_time = time.perf_counter() - start_time
    
    # Test optimized calculator
    calc_optimized = OptimizedCalculator()
    start_time = time.perf_counter()
    for a, b in test_data:
        calc_optimized.add(a, b)
        calc_optimized.subtract(a, b)
        calc_optimized.multiply(a, b)
        calc_optimized.divide(a, b)
    optimized_time = time.perf_counter() - start_time
    
    print(f"Original Calculator: {original_time:.4f} seconds")
    print(f"Optimized Calculator: {optimized_time:.4f} seconds")
    print(f"Speed improvement: {((original_time - optimized_time) / original_time * 100):.2f}%")


def benchmark_cached_operations(iterations=1000):
    """Benchmark operations with repeated values to test caching"""
    print(f"\nBenchmarking cached operations ({iterations} iterations with repeated values)...")
    
    # Generate limited set of values to test caching
    values = [(random.uniform(1, 100), random.uniform(1, 100)) for _ in range(10)]
    test_data = [random.choice(values) for _ in range(iterations)]
    
    # Test original calculator
    calc_original = Calculator()
    start_time = time.perf_counter()
    for a, b in test_data:
        calc_original.add(a, b)
        calc_original.multiply(a, b)
        calc_original.power(a, b % 10)  # Limit power to avoid large numbers
    original_time = time.perf_counter() - start_time
    
    # Test optimized calculator with caching
    calc_optimized = OptimizedCalculator()
    start_time = time.perf_counter()
    for a, b in test_data:
        calc_optimized.add(a, b)
        calc_optimized.multiply(a, b)
        calc_optimized.power(a, b % 10)
    optimized_time = time.perf_counter() - start_time
    
    print(f"Original Calculator: {original_time:.4f} seconds")
    print(f"Optimized Calculator (with caching): {optimized_time:.4f} seconds")
    print(f"Speed improvement: {((original_time - optimized_time) / original_time * 100):.2f}%")


def benchmark_menu_display(iterations=1000):
    """Benchmark menu display performance"""
    print(f"\nBenchmarking menu display ({iterations} iterations)...")
    
    # Test original menu display
    from calculator import display_menu
    import io
    import sys
    
    # Redirect output to avoid printing
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    start_time = time.perf_counter()
    for _ in range(iterations):
        display_menu()
    original_time = time.perf_counter() - start_time
    
    # Test optimized cached menu
    start_time = time.perf_counter()
    for _ in range(iterations):
        menu = get_cached_menu()
    optimized_time = time.perf_counter() - start_time
    
    sys.stdout = old_stdout
    
    print(f"Original menu display: {original_time:.4f} seconds")
    print(f"Optimized cached menu: {optimized_time:.4f} seconds")
    print(f"Speed improvement: {((original_time - optimized_time) / original_time * 100):.2f}%")


def benchmark_batch_operations():
    """Benchmark batch processing capabilities"""
    print(f"\nBenchmarking batch operations (1000 calculations)...")
    
    # Generate batch data
    operations = []
    for _ in range(1000):
        op = random.choice(['+', '-', '*', '/', '^', '%'])
        a = random.uniform(1, 100)
        b = random.uniform(1, 100) if op not in ['^'] else random.uniform(1, 5)
        if op == '/' or op == '%':
            b = max(b, 0.1)  # Avoid division by zero
        operations.append((op, a, b))
    
    # Test individual operations (simulating original)
    calc_original = Calculator()
    start_time = time.perf_counter()
    results_original = []
    for op, a, b in operations:
        try:
            if op == '+':
                result = calc_original.add(a, b)
            elif op == '-':
                result = calc_original.subtract(a, b)
            elif op == '*':
                result = calc_original.multiply(a, b)
            elif op == '/':
                result = calc_original.divide(a, b)
            elif op == '^':
                result = calc_original.power(a, b)
            elif op == '%':
                result = calc_original.modulo(a, b)
            results_original.append(result)
        except:
            results_original.append(None)
    original_time = time.perf_counter() - start_time
    
    # Test batch processing
    calc_optimized = OptimizedCalculator()
    start_time = time.perf_counter()
    results_optimized = calc_optimized.batch_calculate(operations)
    optimized_time = time.perf_counter() - start_time
    
    print(f"Original (individual operations): {original_time:.4f} seconds")
    print(f"Optimized (batch processing): {optimized_time:.4f} seconds")
    print(f"Speed improvement: {((original_time - optimized_time) / original_time * 100):.2f}%")


def benchmark_expression_evaluation():
    """Benchmark expression evaluation feature"""
    print(f"\nBenchmarking expression evaluation (100 complex expressions)...")
    
    expressions = [
        "10 + 5 * 2",
        "100 / 5 - 3",
        "2 ^ 3 + 4 * 5",
        "(10 + 5) * 2",
        "100 - 50 / 2",
        "3 * 4 + 5 * 6",
        "2 ^ 4 - 10",
        "(100 + 200) / 3",
        "50 % 7 + 10",
        "25 * 4 / 2"
    ]
    
    calc_optimized = OptimizedCalculator()
    
    # Generate 100 test expressions
    test_expressions = [random.choice(expressions) for _ in range(100)]
    
    start_time = time.perf_counter()
    for expr in test_expressions:
        try:
            calc_optimized.evaluate_expression(expr)
        except:
            pass
    eval_time = time.perf_counter() - start_time
    
    print(f"Expression evaluation time: {eval_time:.4f} seconds")
    print(f"Average per expression: {(eval_time / 100 * 1000):.2f} ms")


def main():
    """Run all benchmarks"""
    print("="*60)
    print("CALCULATOR PERFORMANCE BENCHMARK")
    print("="*60)
    
    benchmark_basic_operations()
    benchmark_cached_operations()
    benchmark_menu_display()
    benchmark_batch_operations()
    benchmark_expression_evaluation()
    
    print("\n" + "="*60)
    print("PERFORMANCE IMPROVEMENTS SUMMARY:")
    print("="*60)
    print("1. Caching with @lru_cache for repeated calculations")
    print("2. Pre-compiled regex for number validation")
    print("3. Cached menu string to avoid recreation")
    print("4. Batch processing for multiple calculations")
    print("5. Expression evaluation for complex calculations")
    print("6. Command-line argument support for automation")
    print("7. History tracking for result reuse")
    print("8. Decimal precision option for financial calculations")
    print("="*60)


if __name__ == "__main__":
    main()