# Comprehensive Mathematics & Computer Science Reference

## Table of Contents
1. [Logic Gates & Boolean Algebra](#logic-gates)
2. [Computer Architecture](#computer-architecture)
3. [Number Theory](#number-theory)
4. [Calculus](#calculus)
5. [Linear Algebra](#linear-algebra)
6. [Statistics](#statistics)
7. [Algorithms](#algorithms)

---

## Logic Gates & Boolean Algebra

### Basic Logic Gates

| Gate | Symbol | Truth Table | Boolean Expression |
|------|--------|-------------|-------------------|
| AND  | ∧      | 1∧1=1, else 0 | A·B or A∧B |
| OR   | ∨      | 0∨0=0, else 1 | A+B or A∨B |
| NOT  | ¬      | ¬0=1, ¬1=0 | Ā or ¬A |
| NAND | ⊼      | ¬(A∧B) | A̅·̅B̅ |
| NOR  | ⊽      | ¬(A∨B) | A̅+̅B̅ |
| XOR  | ⊕      | A≠B | A⊕B |
| XNOR | ⊙      | A=B | A⊙B |

### Boolean Algebra Laws

**Identity Laws:**
- A ∧ 1 = A
- A ∨ 0 = A

**Null Laws:**
- A ∧ 0 = 0
- A ∨ 1 = 1

**Idempotent Laws:**
- A ∧ A = A
- A ∨ A = A

**Complement Laws:**
- A ∧ ¬A = 0
- A ∨ ¬A = 1
- ¬(¬A) = A

**Commutative Laws:**
- A ∧ B = B ∧ A
- A ∨ B = B ∨ A

**Associative Laws:**
- (A ∧ B) ∧ C = A ∧ (B ∧ C)
- (A ∨ B) ∨ C = A ∨ (B ∨ C)

**Distributive Laws:**
- A ∧ (B ∨ C) = (A ∧ B) ∨ (A ∧ C)
- A ∨ (B ∧ C) = (A ∨ B) ∧ (A ∨ C)

**De Morgan's Laws:**
- ¬(A ∧ B) = ¬A ∨ ¬B
- ¬(A ∨ B) = ¬A ∧ ¬B

**Absorption Laws:**
- A ∨ (A ∧ B) = A
- A ∧ (A ∨ B) = A

---

## Computer Architecture

### Adder Circuits

**Half Adder:**
- Inputs: A, B
- Outputs: Sum = A ⊕ B, Carry = A ∧ B

**Full Adder:**
- Inputs: A, B, Carry_in
- Outputs: Sum = A ⊕ B ⊕ Carry_in
- Carry_out = (A ∧ B) ∨ (Carry_in ∧ (A ⊕ B))

**Ripple Carry Adder:**
- Chains multiple full adders
- Adds n-bit numbers
- Carry propagates through all stages

### ALU Operations

| Operation | Description | Formula |
|-----------|-------------|---------|
| ADD | Addition | A + B |
| SUB | Subtraction | A - B (using 2's complement) |
| AND | Bitwise AND | A ∧ B |
| OR | Bitwise OR | A ∨ B |
| XOR | Bitwise XOR | A ⊕ B |
| NOT | Bitwise NOT | ¬A |
| SHL | Shift Left | A << n |
| SHR | Shift Right | A >> n |

### CPU Flags

- **Zero (Z):** Set when result is zero
- **Carry (C):** Set when operation produces carry/borrow
- **Negative (N):** Set when result is negative (MSB = 1)
- **Overflow (V):** Set when signed arithmetic overflows

---

## Number Theory

### Divisibility & Primes

**Greatest Common Divisor (GCD):**
```
Euclidean Algorithm:
GCD(a, b) = GCD(b, a mod b)
GCD(a, 0) = a
```

**Least Common Multiple (LCM):**
```
LCM(a, b) = |a × b| / GCD(a, b)
```

**Prime Numbers:**
- A number p > 1 with only divisors 1 and p
- Fundamental Theorem: Every integer > 1 has unique prime factorization

**Modular Arithmetic:**
- a ≡ b (mod n) means n divides (a - b)
- (a + b) mod n = ((a mod n) + (b mod n)) mod n
- (a × b) mod n = ((a mod n) × (b mod n)) mod n

### Sequences

**Fibonacci Sequence:**
```
F(0) = 0, F(1) = 1
F(n) = F(n-1) + F(n-2)
Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...
```

**Factorial:**
```
n! = n × (n-1) × (n-2) × ... × 2 × 1
0! = 1
```

---

## Calculus

### Differentiation

**Definition:**
```
f'(x) = lim[h→0] (f(x+h) - f(x)) / h
```

**Common Derivatives:**
- d/dx(xⁿ) = n·xⁿ⁻¹
- d/dx(eˣ) = eˣ
- d/dx(ln x) = 1/x
- d/dx(sin x) = cos x
- d/dx(cos x) = -sin x
- d/dx(tan x) = sec²x

**Rules:**
- Sum: (f + g)' = f' + g'
- Product: (fg)' = f'g + fg'
- Quotient: (f/g)' = (f'g - fg') / g²
- Chain: (f∘g)' = f'(g(x))·g'(x)

### Integration

**Definition:**
```
∫[a,b] f(x)dx = lim[n→∞] Σ f(xᵢ)Δx
```

**Common Integrals:**
- ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ -1)
- ∫ 1/x dx = ln|x| + C
- ∫ eˣ dx = eˣ + C
- ∫ sin x dx = -cos x + C
- ∫ cos x dx = sin x + C

**Numerical Methods:**
- Trapezoidal Rule: ∫[a,b] f(x)dx ≈ h/2[f(a) + 2Σf(xᵢ) + f(b)]
- Simpson's Rule: More accurate, uses parabolic approximation

### Taylor Series

**General Form:**
```
f(x) = Σ[n=0 to ∞] f⁽ⁿ⁾(a)/n! · (x-a)ⁿ
```

**Common Series:**
- eˣ = Σ xⁿ/n! = 1 + x + x²/2! + x³/3! + ...
- sin x = Σ (-1)ⁿx^(2n+1)/(2n+1)! = x - x³/3! + x⁵/5! - ...
- cos x = Σ (-1)ⁿx^(2n)/(2n)! = 1 - x²/2! + x⁴/4! - ...
- ln(1+x) = Σ (-1)ⁿ⁺¹xⁿ/n = x - x²/2 + x³/3 - ... (|x| < 1)

---

## Linear Algebra

### Matrices

**Matrix Multiplication:**
```
(AB)ᵢⱼ = Σₖ Aᵢₖ·Bₖⱼ
```

**Properties:**
- Not commutative: AB ≠ BA (generally)
- Associative: (AB)C = A(BC)
- Distributive: A(B+C) = AB + AC

**Determinant (2×2):**
```
det([a b]) = ad - bc
    [c d]
```

**Transpose:**
```
(Aᵀ)ᵢⱼ = Aⱼᵢ
```

### Vectors

**Dot Product:**
```
a · b = |a||b|cos θ = Σ aᵢbᵢ
```

**Cross Product (3D):**
```
a × b = |a||b|sin θ · n̂
```

**Magnitude:**
```
|v| = √(v₁² + v₂² + ... + vₙ²)
```

---

## Statistics

### Measures of Central Tendency

**Mean (Average):**
```
μ = (Σ xᵢ) / n
```

**Median:**
- Middle value when data is sorted
- For even n: average of two middle values

**Mode:**
- Most frequently occurring value

### Measures of Spread

**Variance:**
```
σ² = Σ(xᵢ - μ)² / n
```

**Standard Deviation:**
```
σ = √(variance)
```

**Range:**
```
Range = max - min
```

### Probability

**Basic Rules:**
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- P(A ∩ B) = P(A) · P(B|A)
- P(Ā) = 1 - P(A)

**Bayes' Theorem:**
```
P(A|B) = P(B|A) · P(A) / P(B)
```

---

## Algorithms

### Combinatorics

**Permutations:**
```
P(n, r) = n! / (n-r)!
Number of ways to arrange r items from n items
```

**Combinations:**
```
C(n, r) = n! / (r!(n-r)!)
Number of ways to choose r items from n items
```

**Binomial Theorem:**
```
(a + b)ⁿ = Σ C(n,k) · aⁿ⁻ᵏ · bᵏ
```

### Complexity

**Big O Notation:**
- O(1): Constant time
- O(log n): Logarithmic
- O(n): Linear
- O(n log n): Linearithmic
- O(n²): Quadratic
- O(2ⁿ): Exponential
- O(n!): Factorial

### Common Algorithms

**Sorting:**
- Bubble Sort: O(n²)
- Quick Sort: O(n log n) average
- Merge Sort: O(n log n)

**Searching:**
- Linear Search: O(n)
- Binary Search: O(log n) (sorted data)

**Graph Algorithms:**
- Dijkstra's: Shortest path
- BFS/DFS: Graph traversal

---

## References

This reference is based on fundamental mathematical and computer science principles, implemented in the accompanying Python libraries:

- `boolean_algebra.py` - Logic gates and Boolean operations
- `calculus.py` - Differentiation, integration, series
- `math_library.py` - Number theory, trigonometry, statistics
- `computer_architecture.py` - Logic gates, adders, ALU, CPU

For interactive demonstrations, run any of the Python files:
```bash
python boolean_algebra.py
python calculus.py
python math_library.py
python computer_architecture.py
```
