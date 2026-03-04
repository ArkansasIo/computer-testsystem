#!/usr/bin/env python3
"""
Calculus Library
Implements differentiation, integration, limits, and series
Based on fundamental calculus principles
"""

import math

class Calculus:
    """Calculus operations: derivatives, integrals, limits, series"""
    
    # ===== DIFFERENTIATION =====
    
    @staticmethod
    def derivative(f, x, h=1e-7):
        """
        Numerical derivative using central difference method
        f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
        """
        return (f(x + h) - f(x - h)) / (2 * h)
    
    @staticmethod
    def partial_derivative(f, x, y, var='x', h=1e-7):
        """
        Partial derivative with respect to specified variable
        ∂f/∂x or ∂f/∂y
        """
        if var == 'x':
            return (f(x + h, y) - f(x - h, y)) / (2 * h)
        elif var == 'y':
            return (f(x, y + h) - f(x, y - h)) / (2 * h)
    
    @staticmethod
    def gradient(f, x, y, h=1e-7):
        """
        Gradient vector: ∇f = (∂f/∂x, ∂f/∂y)
        """
        dx = Calculus.partial_derivative(f, x, y, 'x', h)
        dy = Calculus.partial_derivative(f, x, y, 'y', h)
        return (dx, dy)
    
    @staticmethod
    def second_derivative(f, x, h=1e-5):
        """
        Second derivative: f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h²
        """
        return (f(x + h) - 2*f(x) + f(x - h)) / (h * h)
    
    # ===== INTEGRATION =====
    
    @staticmethod
    def integrate_trapezoidal(f, a, b, n=1000):
        """
        Trapezoidal rule for numerical integration
        ∫[a,b] f(x)dx ≈ h/2 * [f(a) + 2∑f(xi) + f(b)]
        """
        h = (b - a) / n
        result = 0.5 * (f(a) + f(b))
        
        for i in range(1, n):
            x = a + i * h
            result += f(x)
        
        return result * h
    
    @staticmethod
    def integrate_simpson(f, a, b, n=1000):
        """
        Simpson's rule for numerical integration (more accurate)
        ∫[a,b] f(x)dx ≈ h/3 * [f(a) + 4∑f(x_odd) + 2∑f(x_even) + f(b)]
        """
        if n % 2 == 1:
            n += 1  # Must be even
        
        h = (b - a) / n
        result = f(a) + f(b)
        
        for i in range(1, n):
            x = a + i * h
            if i % 2 == 0:
                result += 2 * f(x)
            else:
                result += 4 * f(x)
        
        return result * h / 3
    
    @staticmethod
    def integrate_monte_carlo(f, a, b, n=10000):
        """
        Monte Carlo integration
        ∫[a,b] f(x)dx ≈ (b-a) * average(f(random points))
        """
        import random
        total = sum(f(random.uniform(a, b)) for _ in range(n))
        return (b - a) * total / n
    
    # ===== LIMITS =====
    
    @staticmethod
    def limit(f, x0, direction='both', h=1e-10):
        """
        Numerical limit: lim(x→x0) f(x)
        direction: 'left', 'right', or 'both'
        """
        if direction == 'left':
            return f(x0 - h)
        elif direction == 'right':
            return f(x0 + h)
        else:  # both
            left = f(x0 - h)
            right = f(x0 + h)
            if abs(left - right) < 1e-6:
                return (left + right) / 2
            else:
                return None  # Limit does not exist
    
    # ===== SERIES =====
    
    @staticmethod
    def taylor_series(f, x0, x, n=10):
        """
        Taylor series expansion around x0
        f(x) ≈ ∑[n=0 to ∞] f⁽ⁿ⁾(x0)/n! * (x-x0)ⁿ
        """
        result = 0
        h = 1e-5
        
        for i in range(n):
            # Compute i-th derivative at x0
            if i == 0:
                deriv = f(x0)
            else:
                # Numerical higher-order derivatives
                deriv = Calculus._nth_derivative(f, x0, i, h)
            
            # Add term to series
            factorial = math.factorial(i)
            result += deriv / factorial * (x - x0)**i
        
        return result
    
    @staticmethod
    def _nth_derivative(f, x, n, h=1e-5):
        """Helper: compute n-th derivative numerically"""
        if n == 0:
            return f(x)
        elif n == 1:
            return Calculus.derivative(f, x, h)
        else:
            # Recursive numerical differentiation
            def f_deriv(t):
                return Calculus._nth_derivative(f, t, n-1, h)
            return Calculus.derivative(f_deriv, x, h)
    
    @staticmethod
    def power_series(coefficients, x, x0=0):
        """
        Evaluate power series: ∑ aₙ(x-x0)ⁿ
        coefficients: list [a0, a1, a2, ...]
        """
        result = 0
        for n, coeff in enumerate(coefficients):
            result += coeff * (x - x0)**n
        return result
    
    # ===== SPECIAL FUNCTIONS =====
    
    @staticmethod
    def exp_series(x, n=20):
        """
        Exponential function using Taylor series
        e^x = ∑[n=0 to ∞] xⁿ/n!
        """
        result = 0
        for i in range(n):
            result += x**i / math.factorial(i)
        return result
    
    @staticmethod
    def sin_series(x, n=15):
        """
        Sine function using Taylor series
        sin(x) = ∑[n=0 to ∞] (-1)ⁿ * x^(2n+1) / (2n+1)!
        """
        result = 0
        for i in range(n):
            sign = (-1)**i
            result += sign * x**(2*i + 1) / math.factorial(2*i + 1)
        return result
    
    @staticmethod
    def cos_series(x, n=15):
        """
        Cosine function using Taylor series
        cos(x) = ∑[n=0 to ∞] (-1)ⁿ * x^(2n) / (2n)!
        """
        result = 0
        for i in range(n):
            sign = (-1)**i
            result += sign * x**(2*i) / math.factorial(2*i)
        return result
    
    # ===== OPTIMIZATION =====
    
    @staticmethod
    def find_critical_points(f, a, b, n=100):
        """
        Find critical points where f'(x) = 0
        Returns list of x values where derivative is approximately zero
        """
        critical_points = []
        h = (b - a) / n
        
        for i in range(n):
            x = a + i * h
            deriv = Calculus.derivative(f, x)
            if abs(deriv) < 1e-4:
                critical_points.append(x)
        
        return critical_points
    
    @staticmethod
    def newton_method(f, x0, max_iter=50, tol=1e-7):
        """
        Newton's method for finding roots
        x_{n+1} = x_n - f(x_n)/f'(x_n)
        """
        x = x0
        for _ in range(max_iter):
            fx = f(x)
            if abs(fx) < tol:
                return x
            
            fpx = Calculus.derivative(f, x)
            if abs(fpx) < 1e-10:
                return None  # Derivative too small
            
            x = x - fx / fpx
        
        return x


def main():
    """Demonstrate calculus operations"""
    print("=" * 60)
    print("CALCULUS LIBRARY DEMONSTRATION")
    print("=" * 60)
    
    # Test functions
    f1 = lambda x: x**2
    f2 = lambda x: math.sin(x)
    f3 = lambda x: math.exp(x)
    f4 = lambda x, y: x**2 + y**2
    
    print("\n1. DERIVATIVES")
    print("-" * 60)
    print(f"f(x) = x²")
    print(f"f'(2) = {Calculus.derivative(f1, 2):.6f} (expected: 4)")
    print(f"f''(2) = {Calculus.second_derivative(f1, 2):.6f} (expected: 2)")
    
    print(f"\nf(x) = sin(x)")
    print(f"f'(pi/2) = {Calculus.derivative(f2, math.pi/2):.6f} (expected: 0)")
    
    print(f"\n2. PARTIAL DERIVATIVES & GRADIENT")
    print("-" * 60)
    print(f"f(x,y) = x^2 + y^2")
    x, y = 3, 4
    grad = Calculus.gradient(f4, x, y)
    print(f"grad f({x},{y}) = {grad} (expected: (6, 8))")
    
    print("\n3. INTEGRATION")
    print("-" * 60)
    print(f"Integral [0,1] x^2 dx")
    result_trap = Calculus.integrate_trapezoidal(f1, 0, 1)
    result_simp = Calculus.integrate_simpson(f1, 0, 1)
    print(f"Trapezoidal: {result_trap:.6f}")
    print(f"Simpson's:   {result_simp:.6f}")
    print(f"Exact:       {1/3:.6f}")
    
    print(f"\nIntegral [0,pi] sin(x) dx")
    result = Calculus.integrate_simpson(f2, 0, math.pi)
    print(f"Result: {result:.6f} (expected: 2)")
    
    print("\n4. TAYLOR SERIES")
    print("-" * 60)
    x = 0.5
    print(f"e^{x} using Taylor series:")
    print(f"Result: {Calculus.exp_series(x):.6f}")
    print(f"Exact:  {math.exp(x):.6f}")
    
    print(f"\nsin({x}) using Taylor series:")
    print(f"Result: {Calculus.sin_series(x):.6f}")
    print(f"Exact:  {math.sin(x):.6f}")
    
    print("\n5. NEWTON'S METHOD (Finding Roots)")
    print("-" * 60)
    f_root = lambda x: x**2 - 2  # Find sqrt(2)
    root = Calculus.newton_method(f_root, 1.0)
    print(f"Root of x^2 - 2 = 0")
    print(f"Result: {root:.10f}")
    print(f"sqrt(2): {math.sqrt(2):.10f}")
    
    print("\n6. CRITICAL POINTS")
    print("-" * 60)
    f_crit = lambda x: x**3 - 3*x  # Has critical points at x = +/-1
    critical = Calculus.find_critical_points(f_crit, -2, 2, 200)
    print(f"f(x) = x^3 - 3x")
    print(f"Critical points: {[f'{x:.2f}' for x in critical]}")
    print(f"Expected: [-1.00, 1.00]")


if __name__ == '__main__':
    main()
