#!/usr/bin/env python3
"""
Comprehensive Mathematics Library
Implements fundamental mathematical functions from first principles
Inspired by WolframAlpha's computational capabilities
"""

import math

class MathLibrary:
    """Core mathematical functions and algorithms"""
    
    # ===== BASIC ARITHMETIC =====
    
    @staticmethod
    def gcd(a, b):
        """
        Greatest Common Divisor using Euclidean algorithm
        GCD(a, b) = GCD(b, a mod b)
        """
        while b:
            a, b = b, a % b
        return abs(a)
    
    @staticmethod
    def lcm(a, b):
        """
        Least Common Multiple
        LCM(a, b) = |a * b| / GCD(a, b)
        """
        return abs(a * b) // MathLibrary.gcd(a, b)
    
    @staticmethod
    def factorial(n):
        """
        Factorial: n! = n × (n-1) × ... × 1
        """
        if n < 0:
            raise ValueError("Factorial undefined for negative numbers")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    @staticmethod
    def fibonacci(n):
        """
        Fibonacci sequence: F(n) = F(n-1) + F(n-2)
        F(0) = 0, F(1) = 1
        """
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def is_prime(n):
        """
        Primality test using trial division
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # Check odd divisors up to √n
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def prime_factors(n):
        """
        Prime factorization of n
        Returns list of prime factors
        """
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    # ===== EXPONENTIATION & LOGARITHMS =====
    
    @staticmethod
    def power(base, exp):
        """
        Fast exponentiation using binary method
        Computes base^exp in O(log exp) time
        """
        if exp == 0:
            return 1
        if exp < 0:
            return 1 / MathLibrary.power(base, -exp)
        
        result = 1
        while exp > 0:
            if exp % 2 == 1:
                result *= base
            base *= base
            exp //= 2
        return result
    
    @staticmethod
    def sqrt_newton(x, tol=1e-10):
        """
        Square root using Newton's method
        x_{n+1} = (x_n + a/x_n) / 2
        """
        if x < 0:
            raise ValueError("Square root of negative number")
        if x == 0:
            return 0
        
        guess = x
        while True:
            next_guess = (guess + x / guess) / 2
            if abs(next_guess - guess) < tol:
                return next_guess
            guess = next_guess
    
    @staticmethod
    def nth_root(x, n, tol=1e-10):
        """
        N-th root using Newton's method
        """
        if n == 0:
            raise ValueError("0-th root undefined")
        if x < 0 and n % 2 == 0:
            raise ValueError("Even root of negative number")
        
        guess = x / n
        while True:
            next_guess = ((n - 1) * guess + x / (guess ** (n - 1))) / n
            if abs(next_guess - guess) < tol:
                return next_guess
            guess = next_guess
    
    @staticmethod
    def log_natural(x, terms=100):
        """
        Natural logarithm using Taylor series
        ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...  for |x| < 1
        """
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        
        # Transform to range where series converges
        if x > 2:
            return MathLibrary.log_natural(x / math.e) + 1
        
        x = x - 1  # ln(x) = ln(1 + (x-1))
        result = 0
        for n in range(1, terms + 1):
            result += ((-1) ** (n + 1)) * (x ** n) / n
        return result
    
    # ===== TRIGONOMETRY =====
    
    @staticmethod
    def sin_taylor(x, terms=15):
        """
        Sine using Taylor series
        sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
        """
        # Normalize to [-π, π]
        x = x % (2 * math.pi)
        if x > math.pi:
            x -= 2 * math.pi
        
        result = 0
        for n in range(terms):
            sign = (-1) ** n
            result += sign * (x ** (2*n + 1)) / MathLibrary.factorial(2*n + 1)
        return result
    
    @staticmethod
    def cos_taylor(x, terms=15):
        """
        Cosine using Taylor series
        cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
        """
        x = x % (2 * math.pi)
        if x > math.pi:
            x -= 2 * math.pi
        
        result = 0
        for n in range(terms):
            sign = (-1) ** n
            result += sign * (x ** (2*n)) / MathLibrary.factorial(2*n)
        return result
    
    @staticmethod
    def tan(x):
        """Tangent: tan(x) = sin(x) / cos(x)"""
        return MathLibrary.sin_taylor(x) / MathLibrary.cos_taylor(x)
    
    @staticmethod
    def arctan_series(x, terms=50):
        """
        Arctangent using Taylor series
        arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...  for |x| ≤ 1
        """
        if abs(x) > 1:
            # Use identity: arctan(x) = π/2 - arctan(1/x) for x > 0
            sign = 1 if x > 0 else -1
            return sign * math.pi / 2 - MathLibrary.arctan_series(1/x, terms)
        
        result = 0
        for n in range(terms):
            sign = (-1) ** n
            result += sign * (x ** (2*n + 1)) / (2*n + 1)
        return result
    
    # ===== COMBINATORICS =====
    
    @staticmethod
    def binomial_coefficient(n, k):
        """
        Binomial coefficient: C(n,k) = n! / (k! * (n-k)!)
        Number of ways to choose k items from n items
        """
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        
        # Optimize: C(n,k) = C(n, n-k)
        k = min(k, n - k)
        
        result = 1
        for i in range(k):
            result = result * (n - i) // (i + 1)
        return result
    
    @staticmethod
    def permutations(n, r):
        """
        Permutations: P(n,r) = n! / (n-r)!
        Number of ways to arrange r items from n items
        """
        if r < 0 or r > n:
            return 0
        result = 1
        for i in range(n, n - r, -1):
            result *= i
        return result
    
    # ===== STATISTICS =====
    
    @staticmethod
    def mean(data):
        """Arithmetic mean (average)"""
        return sum(data) / len(data)
    
    @staticmethod
    def median(data):
        """Median (middle value)"""
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    
    @staticmethod
    def variance(data):
        """Variance: average of squared deviations from mean"""
        m = MathLibrary.mean(data)
        return sum((x - m) ** 2 for x in data) / len(data)
    
    @staticmethod
    def std_deviation(data):
        """Standard deviation: square root of variance"""
        return math.sqrt(MathLibrary.variance(data))
    
    # ===== COMPLEX NUMBERS =====
    
    @staticmethod
    def complex_add(a, b):
        """Add complex numbers: (a+bi) + (c+di) = (a+c) + (b+d)i"""
        return (a[0] + b[0], a[1] + b[1])
    
    @staticmethod
    def complex_multiply(a, b):
        """
        Multiply complex numbers
        (a+bi)(c+di) = (ac-bd) + (ad+bc)i
        """
        real = a[0] * b[0] - a[1] * b[1]
        imag = a[0] * b[1] + a[1] * b[0]
        return (real, imag)
    
    @staticmethod
    def complex_magnitude(z):
        """Magnitude: |a+bi| = √(a²+b²)"""
        return math.sqrt(z[0]**2 + z[1]**2)
    
    @staticmethod
    def complex_conjugate(z):
        """Conjugate: conj(a+bi) = a-bi"""
        return (z[0], -z[1])
    
    # ===== MATRIX OPERATIONS =====
    
    @staticmethod
    def matrix_multiply(A, B):
        """Matrix multiplication"""
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        
        if cols_A != rows_B:
            raise ValueError("Incompatible matrix dimensions")
        
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    @staticmethod
    def matrix_determinant_2x2(matrix):
        """Determinant of 2x2 matrix: ad - bc"""
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    @staticmethod
    def matrix_transpose(matrix):
        """Transpose: swap rows and columns"""
        rows, cols = len(matrix), len(matrix[0])
        return [[matrix[i][j] for i in range(rows)] for j in range(cols)]


def main():
    """Demonstrate math library functions"""
    print("=" * 70)
    print("COMPREHENSIVE MATHEMATICS LIBRARY")
    print("=" * 70)
    
    ml = MathLibrary()
    
    print("\n1. NUMBER THEORY")
    print("-" * 70)
    print(f"GCD(48, 18) = {ml.gcd(48, 18)}")
    print(f"LCM(12, 18) = {ml.lcm(12, 18)}")
    print(f"10! = {ml.factorial(10)}")
    print(f"Fibonacci(15) = {ml.fibonacci(15)}")
    print(f"Is 17 prime? {ml.is_prime(17)}")
    print(f"Prime factors of 60: {ml.prime_factors(60)}")
    
    print("\n2. ROOTS & POWERS")
    print("-" * 70)
    print(f"2^10 = {ml.power(2, 10)}")
    print(f"sqrt(2) = {ml.sqrt_newton(2):.10f}")
    print(f"cbrt(27) = {ml.nth_root(27, 3):.10f}")
    
    print("\n3. TRIGONOMETRY")
    print("-" * 70)
    print(f"sin(pi/6) = {ml.sin_taylor(math.pi/6):.6f} (expected: 0.5)")
    print(f"cos(pi/3) = {ml.cos_taylor(math.pi/3):.6f} (expected: 0.5)")
    print(f"tan(pi/4) = {ml.tan(math.pi/4):.6f} (expected: 1.0)")
    print(f"arctan(1) = {ml.arctan_series(1):.6f} (expected: pi/4 = 0.785398)")
    
    print("\n4. COMBINATORICS")
    print("-" * 70)
    print(f"C(10, 3) = {ml.binomial_coefficient(10, 3)} (ways to choose 3 from 10)")
    print(f"P(10, 3) = {ml.permutations(10, 3)} (ways to arrange 3 from 10)")
    
    print("\n5. STATISTICS")
    print("-" * 70)
    data = [2, 4, 4, 4, 5, 5, 7, 9]
    print(f"Data: {data}")
    print(f"Mean: {ml.mean(data):.2f}")
    print(f"Median: {ml.median(data):.2f}")
    print(f"Variance: {ml.variance(data):.2f}")
    print(f"Std Dev: {ml.std_deviation(data):.2f}")
    
    print("\n6. COMPLEX NUMBERS")
    print("-" * 70)
    z1 = (3, 4)  # 3 + 4i
    z2 = (1, 2)  # 1 + 2i
    print(f"z1 = {z1[0]} + {z1[1]}i")
    print(f"z2 = {z2[0]} + {z2[1]}i")
    print(f"z1 + z2 = {ml.complex_add(z1, z2)}")
    print(f"z1 × z2 = {ml.complex_multiply(z1, z2)}")
    print(f"|z1| = {ml.complex_magnitude(z1):.2f}")
    
    print("\n7. MATRIX OPERATIONS")
    print("-" * 70)
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"A x B = {ml.matrix_multiply(A, B)}")
    print(f"det(A) = {ml.matrix_determinant_2x2(A)}")
    print(f"A^T = {ml.matrix_transpose(A)}")


if __name__ == '__main__':
    main()
