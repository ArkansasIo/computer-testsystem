# Complete Guide: Ben Eater 8-bit Computer & Mathematical Libraries

## Overview

This repository contains a complete implementation of:
1. Assembly programs for the Ben Eater 8-bit breadboard computer
2. Comprehensive mathematical and computer science libraries
3. Logic gates, Boolean algebra, and computer architecture components
4. Calculus, number theory, and statistical functions

---

## Part 1: Ben Eater 8-bit Computer

### Architecture
- **SAP-1** (Simple As Possible) architecture
- 4-bit address space (16 memory locations)
- 8-bit data bus
- Two 8-bit registers (A and B)
- ALU with add/subtract operations
- Flags: Carry and Zero

### Assembly Programs

| File | Description | Demonstrates |
|------|-------------|--------------|
| `add_two_numbers.asm` | Adds 28 + 14 = 42 | Basic arithmetic |
| `fibonacci.asm` | Fibonacci sequence | Loops, overflow detection |
| `multiply.asm` | 5 × 7 = 35 | Repeated addition |
| `countdown.asm` | Counts 10 to 0 | Decrement, conditional jump |
| `blink_pattern.asm` | Powers of 2 pattern | Bit shifting simulation |
| `sum_sequence.asm` | 1+2+3+4+5 = 15 | Accumulation |

### Logic Gate Programs

| File | Description |
|------|-------------|
| `logic_gates.asm` | AND gate implementation |
| `logic_or.asm` | OR gate implementation |
| `logic_xor.asm` | XOR gate implementation |
| `logic_not.asm` | NOT gate implementation |

### Math Programs

| File | Description |
|------|-------------|
| `math_gcd.asm` | Greatest Common Divisor |
| `math_power.asm` | Exponentiation (2^5) |
| `math_modulo.asm` | Modulo operation |
| `math_factorial.asm` | Factorial calculation |
| `math_division.asm` | Integer division |

### Tools

**Assembler** (`assembler.py`):
```bash
python assembler.py fibonacci.asm
# Outputs: fibonacci.bin
```

**Simulator** (`simulator.py`):
```bash
python simulator.py fibonacci.bin --verbose
# Simulates program execution
```

---

## Part 2: Mathematical Libraries

### Boolean Algebra (`boolean_algebra.py`)

**Features:**
- All basic logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR)
- Boolean algebra laws verification
- Truth table generation
- De Morgan's laws
- Distributive, associative, commutative laws

**Usage:**
```python
from boolean_algebra import BooleanAlgebra

ba = BooleanAlgebra()
result = ba.XOR(True, False)  # True
ba.truth_table(ba.AND)  # Display truth table
```

**Run demo:**
```bash
python boolean_algebra.py
```

### Calculus (`calculus.py`)

**Features:**
- Numerical differentiation (first, second, partial derivatives)
- Gradient computation
- Numerical integration (Trapezoidal, Simpson's, Monte Carlo)
- Limits
- Taylor series expansion
- Special functions (exp, sin, cos via series)
- Newton's method for root finding
- Critical point detection

**Usage:**
```python
from calculus import Calculus

calc = Calculus()

# Derivative
f = lambda x: x**2
deriv = calc.derivative(f, 3)  # f'(3) = 6

# Integration
integral = calc.integrate_simpson(f, 0, 1)  # ∫[0,1] x² dx = 1/3

# Taylor series
exp_val = calc.exp_series(1)  # e^1 ≈ 2.71828
```

**Run demo:**
```bash
python calculus.py
```

### Math Library (`math_library.py`)

**Features:**

**Number Theory:**
- GCD (Euclidean algorithm)
- LCM
- Factorial
- Fibonacci sequence
- Primality testing
- Prime factorization

**Exponentiation & Roots:**
- Fast exponentiation
- Newton's method for square root
- N-th root calculation
- Natural logarithm

**Trigonometry:**
- Sin, cos, tan (Taylor series)
- Arctan (inverse tangent)

**Combinatorics:**
- Binomial coefficients
- Permutations

**Statistics:**
- Mean, median
- Variance, standard deviation

**Complex Numbers:**
- Addition, multiplication
- Magnitude, conjugate

**Matrix Operations:**
- Matrix multiplication
- Determinant (2×2)
- Transpose

**Usage:**
```python
from math_library import MathLibrary

ml = MathLibrary()

# Number theory
gcd = ml.gcd(48, 18)  # 6
fib = ml.fibonacci(10)  # 55
is_prime = ml.is_prime(17)  # True

# Trigonometry
sin_val = ml.sin_taylor(3.14159/6)  # 0.5

# Statistics
data = [2, 4, 4, 4, 5, 5, 7, 9]
mean = ml.mean(data)  # 5.0
```

**Run demo:**
```bash
python math_library.py
```

### Computer Architecture (`computer_architecture.py`)

**Features:**

**Logic Gates:**
- AND, OR, NOT, NAND, NOR, XOR, XNOR

**Adder Circuits:**
- Half adder
- Full adder
- Ripple carry adder (n-bit)
- Subtractor (2's complement)

**ALU (Arithmetic Logic Unit):**
- Addition, subtraction
- Bitwise operations (AND, OR, XOR, NOT)
- Shift operations (left, right)
- Flag management (Zero, Carry, Negative)

**Memory Components:**
- Register (n-bit storage)
- RAM (random access memory)
- Program counter

**CPU:**
- Simple CPU combining all components

**Usage:**
```python
from computer_architecture import ALU, Adders, LogicGates

# Logic gates
result = LogicGates.XOR(1, 0)  # 1

# Adders
sum_bit, carry = Adders.half_adder(1, 1)  # sum=0, carry=1

# ALU
alu = ALU(8)
result = alu.add(25, 17)  # 42
print(f"Carry: {alu.carry_flag}, Zero: {alu.zero_flag}")
```

**Run demo:**
```bash
python computer_architecture.py
```

---

## Part 3: Testing

### Comprehensive Test Suite (`test_all.py`)

Tests all libraries with assertions:
- Boolean algebra laws
- Logic gates
- Adder circuits
- ALU operations
- Number theory functions
- Calculus operations
- Trigonometry
- Combinatorics
- Statistics
- Complex numbers
- Memory components

**Run tests:**
```bash
python test_all.py
```

Expected output:
```
COMPREHENSIVE TEST SUITE
Running all tests...
======================================================================

TESTING BOOLEAN ALGEBRA
======================================================================
✓ All Boolean algebra tests passed

TESTING LOGIC GATES
======================================================================
✓ All logic gate tests passed

...

======================================================================
✓✓✓ ALL TESTS PASSED ✓✓✓
======================================================================
```

---

## Part 4: Documentation

### Reference Documents

1. **README.md** - Quick start guide
2. **INSTRUCTION_REFERENCE.md** - Complete 8-bit computer instruction set
3. **MATH_REFERENCE.md** - Mathematical formulas and algorithms
4. **COMPLETE_GUIDE.md** - This comprehensive guide

---

## Quick Start Examples

### Example 1: Run an Assembly Program
```bash
# Assemble the Fibonacci program
python assembler.py fibonacci.asm

# Simulate execution
python simulator.py fibonacci.bin --verbose
```

### Example 2: Use Math Libraries
```python
from math_library import MathLibrary
from calculus import Calculus

ml = MathLibrary()
calc = Calculus()

# Calculate factorial
print(f"10! = {ml.factorial(10)}")

# Find derivative
f = lambda x: x**3 - 2*x
print(f"f'(2) = {calc.derivative(f, 2)}")

# Integrate
area = calc.integrate_simpson(f, 0, 2)
print(f"Area under curve: {area}")
```

### Example 3: Build Computer Components
```python
from computer_architecture import ALU, RAM, Register

# Create 8-bit ALU
alu = ALU(8)

# Perform operations
result = alu.add(100, 50)
print(f"100 + 50 = {result}")

# Create memory
ram = RAM(256, 8)
ram.write(0, 42)
print(f"RAM[0] = {ram.read(0)}")
```

---

## File Structure

```
.
├── README.md                    # Project overview
├── INSTRUCTION_REFERENCE.md     # 8-bit computer instruction set
├── MATH_REFERENCE.md            # Mathematical reference
├── COMPLETE_GUIDE.md            # This guide
│
├── Assembly Programs (8-bit computer)
│   ├── add_two_numbers.asm
│   ├── fibonacci.asm
│   ├── multiply.asm
│   ├── countdown.asm
│   ├── blink_pattern.asm
│   ├── sum_sequence.asm
│   ├── logic_gates.asm
│   ├── logic_or.asm
│   ├── logic_xor.asm
│   ├── logic_not.asm
│   ├── math_gcd.asm
│   ├── math_power.asm
│   ├── math_modulo.asm
│   ├── math_factorial.asm
│   └── math_division.asm
│
├── Tools
│   ├── assembler.py             # Assembly to machine code
│   └── simulator.py             # Software simulator
│
├── Mathematical Libraries
│   ├── boolean_algebra.py       # Logic gates & Boolean laws
│   ├── calculus.py              # Derivatives, integrals, series
│   ├── math_library.py          # Number theory, trig, stats
│   └── computer_architecture.py # Gates, adders, ALU, CPU
│
└── Testing
    └── test_all.py              # Comprehensive test suite
```

---

## Mathematical Foundations

### Implemented Algorithms

**Number Theory:**
- Euclidean algorithm (GCD)
- Sieve of Eratosthenes concept (primality)
- Trial division (prime factorization)

**Calculus:**
- Central difference method (derivatives)
- Trapezoidal rule (integration)
- Simpson's rule (integration)
- Taylor series expansion

**Numerical Methods:**
- Newton's method (root finding, square root)
- Binary exponentiation (fast power)
- Monte Carlo integration

**Computer Architecture:**
- Boolean logic synthesis
- Ripple carry addition
- Two's complement arithmetic
- ALU design patterns

---

## Learning Path

### Beginner
1. Start with `add_two_numbers.asm`
2. Run `python boolean_algebra.py` to see truth tables
3. Explore basic math functions in `math_library.py`

### Intermediate
1. Study `fibonacci.asm` and `multiply.asm`
2. Implement custom logic gates
3. Use calculus library for derivatives and integrals

### Advanced
1. Modify ALU to add new operations
2. Implement additional assembly programs
3. Extend math library with new algorithms
4. Build upon computer architecture components

---

## References

**Ben Eater's 8-bit Computer:**
- [YouTube Series](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU)
- [Official Website](https://eater.net/8bit)

**Mathematical Foundations:**
- Digital Computer Electronics by Malvino & Brown
- Introduction to Algorithms by CLRS
- Calculus by Stewart
- Concrete Mathematics by Knuth, Graham, Patashnik

**Computer Architecture:**
- Computer Organization and Design by Patterson & Hennessy
- The Elements of Computing Systems by Nisan & Schocken

---

## Contributing

To extend this project:

1. **Add new assembly programs** - Follow existing format
2. **Implement new math functions** - Add to appropriate library
3. **Create new computer components** - Extend `computer_architecture.py`
4. **Write tests** - Add to `test_all.py`

---

## License

Educational project based on Ben Eater's 8-bit computer design and fundamental mathematical principles.

---

## Summary

This repository provides:
- ✓ Complete 8-bit computer assembly programming environment
- ✓ Assembler and simulator tools
- ✓ Comprehensive mathematical libraries
- ✓ Computer architecture components from first principles
- ✓ Full test suite
- ✓ Extensive documentation

All implementations are built from fundamental principles, suitable for learning and experimentation.
