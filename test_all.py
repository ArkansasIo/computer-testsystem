#!/usr/bin/env python3
"""
Comprehensive Test Suite
Tests all mathematical and computer science libraries
"""

import math
from boolean_algebra import BooleanAlgebra
from calculus import Calculus
from math_library import MathLibrary
from computer_architecture import LogicGates, Adders, ALU, Register, RAM

def test_boolean_algebra():
    """Test Boolean algebra operations"""
    print("\n" + "="*70)
    print("TESTING BOOLEAN ALGEBRA")
    print("="*70)
    
    ba = BooleanAlgebra()
    
    # Test basic gates
    assert ba.AND(True, True) == True
    assert ba.AND(True, False) == False
    assert ba.OR(False, False) == False
    assert ba.OR(True, False) == True
    assert ba.NOT(True) == False
    assert ba.XOR(True, False) == True
    assert ba.XOR(True, True) == False
    
    # Test De Morgan's laws
    for a in [False, True]:
        for b in [False, True]:
            laws = ba.de_morgan_law(a, b)
            assert all(laws.values()), f"De Morgan's law failed for {a}, {b}"
    
    print("✓ All Boolean algebra tests passed")

def test_logic_gates():
    """Test logic gate implementations"""
    print("\n" + "="*70)
    print("TESTING LOGIC GATES")
    print("="*70)
    
    # Test XOR
    assert LogicGates.XOR(0, 0) == 0
    assert LogicGates.XOR(0, 1) == 1
    assert LogicGates.XOR(1, 0) == 1
    assert LogicGates.XOR(1, 1) == 0
    
    # Test NAND (universal gate)
    assert LogicGates.NAND(1, 1) == 0
    assert LogicGates.NAND(0, 1) == 1
    
    print("✓ All logic gate tests passed")

def test_adders():
    """Test adder circuits"""
    print("\n" + "="*70)
    print("TESTING ADDERS")
    print("="*70)
    
    # Test half adder
    sum_bit, carry = Adders.half_adder(1, 1)
    assert sum_bit == 0 and carry == 1, "Half adder failed"
    
    # Test full adder
    sum_bit, carry = Adders.full_adder(1, 1, 1)
    assert sum_bit == 1 and carry == 1, "Full adder failed"
    
    # Test ripple carry adder: 15 + 27 = 42
    a = [1, 1, 1, 1, 0, 0, 0, 0]  # 15
    b = [1, 1, 0, 1, 1, 0, 0, 0]  # 27
    sum_bits, carry = Adders.ripple_carry_adder(a, b)
    result = sum(bit << i for i, bit in enumerate(sum_bits))
    assert result == 42, f"Ripple carry adder failed: got {result}, expected 42"
    
    print("✓ All adder tests passed")

def test_alu():
    """Test ALU operations"""
    print("\n" + "="*70)
    print("TESTING ALU")
    print("="*70)
    
    alu = ALU(8)
    
    # Test addition
    result = alu.add(25, 17)
    assert result == 42, f"ALU add failed: {result}"
    
    # Test subtraction
    result = alu.subtract(50, 20)
    assert result == 30, f"ALU subtract failed: {result}"
    
    # Test bitwise operations
    result = alu.AND(0b11110000, 0b10101010)
    assert result == 0b10100000, f"ALU AND failed: {result:08b}"
    
    result = alu.OR(0b11110000, 0b00001111)
    assert result == 0b11111111, f"ALU OR failed: {result:08b}"
    
    # Test shift
    result = alu.shift_left(0b00001111, 2)
    assert result == 0b00111100, f"ALU shift left failed: {result:08b}"
    
    print("✓ All ALU tests passed")

def test_number_theory():
    """Test number theory functions"""
    print("\n" + "="*70)
    print("TESTING NUMBER THEORY")
    print("="*70)
    
    ml = MathLibrary()
    
    # Test GCD
    assert ml.gcd(48, 18) == 6, "GCD failed"
    assert ml.gcd(100, 35) == 5, "GCD failed"
    
    # Test LCM
    assert ml.lcm(12, 18) == 36, "LCM failed"
    
    # Test factorial
    assert ml.factorial(5) == 120, "Factorial failed"
    assert ml.factorial(0) == 1, "Factorial(0) failed"
    
    # Test Fibonacci
    assert ml.fibonacci(10) == 55, "Fibonacci failed"
    assert ml.fibonacci(0) == 0, "Fibonacci(0) failed"
    
    # Test primality
    assert ml.is_prime(17) == True, "Prime test failed"
    assert ml.is_prime(18) == False, "Prime test failed"
    
    # Test prime factorization
    assert ml.prime_factors(60) == [2, 2, 3, 5], "Prime factorization failed"
    
    print("✓ All number theory tests passed")

def test_calculus():
    """Test calculus operations"""
    print("\n" + "="*70)
    print("TESTING CALCULUS")
    print("="*70)
    
    calc = Calculus()
    
    # Test derivative: d/dx(x²) = 2x, at x=3 should be 6
    f = lambda x: x**2
    deriv = calc.derivative(f, 3)
    assert abs(deriv - 6) < 0.001, f"Derivative failed: {deriv}"
    
    # Test second derivative: d²/dx²(x²) = 2
    second_deriv = calc.second_derivative(f, 3)
    assert abs(second_deriv - 2) < 0.01, f"Second derivative failed: {second_deriv}"
    
    # Test integration: ∫[0,1] x² dx = 1/3
    integral = calc.integrate_simpson(f, 0, 1)
    assert abs(integral - 1/3) < 0.001, f"Integration failed: {integral}"
    
    # Test Taylor series for e^x
    exp_approx = calc.exp_series(1, 20)
    assert abs(exp_approx - math.e) < 0.0001, f"Exp series failed: {exp_approx}"
    
    # Test sin series
    sin_approx = calc.sin_series(math.pi/6, 15)
    assert abs(sin_approx - 0.5) < 0.0001, f"Sin series failed: {sin_approx}"
    
    print("✓ All calculus tests passed")

def test_trigonometry():
    """Test trigonometric functions"""
    print("\n" + "="*70)
    print("TESTING TRIGONOMETRY")
    print("="*70)
    
    ml = MathLibrary()
    
    # Test sin
    result = ml.sin_taylor(math.pi/6)
    assert abs(result - 0.5) < 0.0001, f"Sin failed: {result}"
    
    # Test cos
    result = ml.cos_taylor(math.pi/3)
    assert abs(result - 0.5) < 0.0001, f"Cos failed: {result}"
    
    # Test tan
    result = ml.tan(math.pi/4)
    assert abs(result - 1.0) < 0.001, f"Tan failed: {result}"
    
    # Test arctan
    result = ml.arctan_series(1, 100)  # Need more terms for x=1
    assert abs(result - math.pi/4) < 0.01, f"Arctan failed: {result}"
    
    print("✓ All trigonometry tests passed")

def test_combinatorics():
    """Test combinatorial functions"""
    print("\n" + "="*70)
    print("TESTING COMBINATORICS")
    print("="*70)
    
    ml = MathLibrary()
    
    # Test binomial coefficient
    assert ml.binomial_coefficient(10, 3) == 120, "Binomial coefficient failed"
    assert ml.binomial_coefficient(5, 2) == 10, "Binomial coefficient failed"
    
    # Test permutations
    assert ml.permutations(10, 3) == 720, "Permutations failed"
    assert ml.permutations(5, 5) == 120, "Permutations failed"
    
    print("✓ All combinatorics tests passed")

def test_statistics():
    """Test statistical functions"""
    print("\n" + "="*70)
    print("TESTING STATISTICS")
    print("="*70)
    
    ml = MathLibrary()
    
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    
    # Test mean
    assert ml.mean(data) == 5.0, "Mean failed"
    
    # Test median
    assert ml.median(data) == 4.5, "Median failed"
    
    # Test variance
    var = ml.variance(data)
    assert abs(var - 4.0) < 0.01, f"Variance failed: {var}"
    
    print("✓ All statistics tests passed")

def test_complex_numbers():
    """Test complex number operations"""
    print("\n" + "="*70)
    print("TESTING COMPLEX NUMBERS")
    print("="*70)
    
    ml = MathLibrary()
    
    z1 = (3, 4)  # 3 + 4i
    z2 = (1, 2)  # 1 + 2i
    
    # Test addition
    result = ml.complex_add(z1, z2)
    assert result == (4, 6), f"Complex add failed: {result}"
    
    # Test multiplication: (3+4i)(1+2i) = -5+10i
    result = ml.complex_multiply(z1, z2)
    assert result == (-5, 10), f"Complex multiply failed: {result}"
    
    # Test magnitude: |3+4i| = 5
    mag = ml.complex_magnitude(z1)
    assert abs(mag - 5.0) < 0.001, f"Complex magnitude failed: {mag}"
    
    print("✓ All complex number tests passed")

def test_memory():
    """Test memory components"""
    print("\n" + "="*70)
    print("TESTING MEMORY COMPONENTS")
    print("="*70)
    
    # Test register
    reg = Register(8)
    reg.load(42)
    assert reg.read() == 42, "Register failed"
    
    # Test RAM
    ram = RAM(256, 8)
    ram.write(100, 123)
    assert ram.read(100) == 123, "RAM failed"
    
    print("✓ All memory tests passed")

def run_all_tests():
    """Run all test suites"""
    print("\n" + "="*70)
    print("COMPREHENSIVE TEST SUITE")
    print("Running all tests...")
    print("="*70)
    
    try:
        test_boolean_algebra()
        test_logic_gates()
        test_adders()
        test_alu()
        test_number_theory()
        test_calculus()
        test_trigonometry()
        test_combinatorics()
        test_statistics()
        test_complex_numbers()
        test_memory()
        
        print("\n" + "="*70)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("="*70)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
