# Multi-Architecture Computer Systems & Comprehensive Math Libraries

Complete implementation from 8-bit to 256-bit computer architectures with extended register sets (A-Z), assembly programming environments, interactive GUIs, and comprehensive mathematical libraries built from first principles.

Based on the [Ben Eater 8-bit breadboard computer](https://eater.net/8bit) and extended to modern architectures.

## 🎯 What's Included

### Part 1: Complete GUI with ALL Features (NEW!)
- **Individual LED components** - Every bit of every register visible
- **LCD-style displays** - Multi-format output (Binary, Hex, Decimal, Octal)
- **Interactive switches** - Manual memory programming with toggle switches
- **Control signal LEDs** - 15 signals (MI, RI, RO, II, IO, AI, AO, EO, SU, BI, OI, CE, CO, J, FI)
- **Instruction decode** - See current operation in real-time
- **Memory viewer** - Live display of all 16 memory locations
- **Sound effects** - Authentic retro computer sounds integrated
- **Step-by-step execution** - Watch CPU internals during each instruction
- **7-segment display** - Classic LED output display
- **Status bar** - Real-time operation feedback

### Part 1b: Enhanced GUI with Sound & Multi-Format Displays
- **11 authentic sound effects** - Pong, printer, read/write, load/run/halt
- **4 display formats** - Binary, Hexadecimal, Decimal, Octal
- **Multi-format panels** - Every value shown in all 4 formats simultaneously
- **Sound toggle** - Enable/disable audio feedback
- **Test sounds** - Preview all sound effects
- **Color-coded displays** - Green (BIN), Yellow (HEX), Cyan (DEC), Magenta (OCT)
- **Large output display** - 36pt decimal readout
- **Real-time updates** - All formats update together

### Part 2: Multi-Architecture Computer Systems
- **6 architectures:** 8-bit, 16-bit, 32-bit, 64-bit, 128-bit, 256-bit
- **26 registers (A-Z)** - Extended from original A-B to full A-Z set
- **100+ instructions** - Complete instruction set including missing opcodes 0x08 (MOV) and 0x09 (XCHG)
- **Advanced GUI** - Switch architectures on-the-fly, view all registers
- **Extended memory** - From 256 bytes (8-bit) to 16 MB (256-bit)
- **5 CPU flags** - Zero, Carry, Negative, Overflow, Parity

### Part 3: 8-bit Computer Assembly Programs
- **15+ assembly programs** for the SAP-1 architecture
- Logic gates (AND, OR, XOR, NOT)
- Math operations (GCD, power, modulo, factorial, division)
- Example programs (Fibonacci, multiply, countdown)
- **Assembler** - converts assembly to machine code
- **Simulator** - test programs before hardware
- **Original GUI** - Authentic Ben Eater interface with LEDs and switches

### Part 4: Mathematical Libraries
- **Boolean Algebra** - Logic gates, truth tables, Boolean laws
- **Calculus** - Derivatives, integrals, Taylor series, limits
- **Math Library** - Number theory, trigonometry, statistics, complex numbers
- **Computer Architecture** - Logic gates, adders, ALU, CPU components

### Part 5: Complete Documentation
- Instruction reference for all architectures
- Mathematical formulas and algorithms
- Comprehensive guides with examples
- Sound effects and display format guides
- Full test suite

## 🚀 Quick Start

### Run Complete GUI with ALL Features (NEW!)
```bash
# Complete GUI with LEDs, LCDs, switches, and control signals
python computer_gui_complete.py

# Features:
# - Individual LED components for every bit
# - LCD-style displays with multi-format output
# - Interactive toggle switches for memory programming
# - Control signal LEDs (MI, RI, RO, II, IO, AI, AO, EO, SU, BI, OI, CE, CO, J, FI)
# - Instruction decode display
# - Memory viewer with live updates
# - Sound effects integrated with visual feedback
# - Step-by-step execution visualization
```

### Run Enhanced GUI with Sound Effects
```bash
# Enhanced GUI with sound effects and multi-format displays
python computer_gui_enhanced.py

# Features:
# - Authentic retro computer sounds (pong, printer, read/write)
# - Binary, Hex, Decimal, Octal displays
# - Sound effects for load/run/halt operations
# - Multi-format register displays
```

### Run Multi-Architecture GUI
```bash
# Advanced GUI with 8/16/32/64/128/256-bit architectures
python multi_arch_gui.py

# Features:
# - Switch between architectures
# - View all 26 registers (A-Z)
# - Memory viewer
# - 5 CPU flags
# - Load programs
```

### Run Original 8-bit GUI
```bash
# Authentic Ben Eater interface with LEDs and switches
python computer_gui.py
```

### Run an Assembly Program
```bash
# Assemble and simulate Fibonacci sequence
python assembler.py fibonacci.asm
python simulator.py fibonacci.bin --verbose
```

### Use Math Libraries
```python
from math_library import MathLibrary
from calculus import Calculus

ml = MathLibrary()
print(f"GCD(48, 18) = {ml.gcd(48, 18)}")  # 6
print(f"10! = {ml.factorial(10)}")         # 3628800

calc = Calculus()
f = lambda x: x**2
print(f"f'(3) = {calc.derivative(f, 3)}")  # 6.0
```

### Test All Systems
```bash
# Run comprehensive test suite
python test_all.py

# Test architectures
python computer_architectures.py

# View complete instruction set
python extended_instruction_set.py
```

## 📁 File Structure

### Multi-Architecture Systems (NEW!)
- `computer_architectures.py` - 8/16/32/64/128/256-bit implementations
- `extended_instruction_set.py` - Complete instruction set (100+ opcodes)
- `multi_arch_gui.py` - Advanced GUI for all architectures
- `computer_gui_complete.py` - **Complete GUI with ALL features** (NEW!)
- `computer_gui_enhanced.py` - **Enhanced GUI with sound effects**
- `sound_effects.py` - **Retro computer sound generator**
- `*.wav` - **11 authentic sound effect files**

### Assembly Programs (8-bit Computer)
- `add_two_numbers.asm` - Basic addition (28 + 14 = 42)
- `fibonacci.asm` - Fibonacci sequence with overflow detection
- `multiply.asm` - Multiplication via repeated addition
- `countdown.asm` - Countdown from 10 to 0
- `sum_sequence.asm` - Sum 1+2+3+4+5 = 15
- `logic_gates.asm`, `logic_or.asm`, `logic_xor.asm`, `logic_not.asm`
- `math_gcd.asm`, `math_power.asm`, `math_modulo.asm`, `math_division.asm`

### Tools
- `assembler.py` - Assembly to machine code converter
- `simulator.py` - Software simulator for testing

### Mathematical Libraries
- `boolean_algebra.py` - Logic gates & Boolean algebra laws
- `calculus.py` - Differentiation, integration, series
- `math_library.py` - Number theory, trig, stats, matrices
- `computer_architecture.py` - Gates, adders, ALU, CPU

### Documentation
- `README.md` - Project overview
- `COMPLETE_GUI_GUIDE.md` - **Complete GUI user guide** (NEW!)
- `INSTRUCTION_REFERENCE.md` - 8-bit instruction set
- `MATH_REFERENCE.md` - Mathematical formulas
- `COMPLETE_GUIDE.md` - Comprehensive guide
- `GUI_GUIDE.md` - Original GUI usage
- `MULTI_ARCH_GUIDE.md` - Multi-architecture guide
- `ENHANCED_FEATURES_GUIDE.md` - **Sound effects & displays guide**
- `PROJECT_SUMMARY.md` - Complete project summary
- `SYSTEM_ARCHITECTURE.md` - System architecture diagrams
- `test_all.py` - Full test suite

## 🎓 Architecture Comparison

| Architecture | Bit Width | Max Value | Memory | Registers | Use Case |
|--------------|-----------|-----------|--------|-----------|----------|
| 8-bit | 8 | 255 | 256 B | 26 (A-Z) | Learning, embedded |
| 16-bit | 16 | 65,535 | 64 KB | 26 (A-Z) | Retro computing |
| 32-bit | 32 | 4.3B | 1 MB | 26 (A-Z) | General purpose |
| 64-bit | 64 | 18.4E | 16 MB | 26 (A-Z) | Modern computing |
| 128-bit | 128 | 3.4E38 | 16 MB | 26 (A-Z) | Cryptography |
| 256-bit | 256 | 1.2E77 | 16 MB | 26 (A-Z) | Advanced crypto |

## 🔧 Extended Features

### Register Set (A-Z)
All architectures support 26 general-purpose registers:
```
A, B, C, D, E, F, G, H, I, J, K, L, M,
N, O, P, Q, R, S, T, U, V, W, X, Y, Z
```

**Special Registers:** PC, SP, MAR, IR

### Complete Instruction Set
- **Data Movement:** NOP, LDA-LDZ, STA-STZ, MOV, XCHG, PUSH, POP
- **Arithmetic:** ADD, SUB, MUL, DIV, MOD, INC, DEC, NEG
- **Logical:** AND, OR, XOR, NOT, NAND, NOR, XNOR
- **Shift/Rotate:** SHL, SHR, ROL, ROR, SAL, SAR
- **Control Flow:** JMP, JZ, JC, JN, CALL, RET, LOOP
- **I/O:** IN, OUT, INB, OUTB
- **System:** INT, CLI, STI, HALT

**Total: 100+ opcodes including previously missing 0x08 (MOV) and 0x09 (XCHG)**

## 🎓 8-bit Computer Architecture

**SAP-1 (Simple As Possible):**
- 4-bit address space (16 memory locations)
- 8-bit data bus
- Two 8-bit registers (A and B)
- ALU with add/subtract
- Flags: Carry and Zero

**Instruction Set:**
| Mnemonic | Description |
|----------|-------------|
| LDA addr | Load from memory into A |
| ADD addr | Add memory to A |
| SUB addr | Subtract memory from A |
| STA addr | Store A to memory |
| LDI val  | Load immediate value |
| JMP addr | Unconditional jump |
| JC addr  | Jump if carry |
| JZ addr  | Jump if zero |
| OUT      | Display A |
| HLT      | Halt |

## 🧮 Mathematical Features

### Boolean Algebra
- All logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR)
- Boolean laws verification (De Morgan's, distributive, etc.)
- Truth table generation

### Calculus
- Numerical derivatives (first, second, partial)
- Integration (Trapezoidal, Simpson's, Monte Carlo)
- Taylor series expansion
- Newton's method for root finding

### Number Theory
- GCD (Euclidean algorithm)
- Prime testing and factorization
- Fibonacci sequence
- Factorial, permutations, combinations

### Computer Architecture
- Half adder, full adder, ripple carry adder
- 8-bit ALU with flags
- Registers, RAM, program counter
- Complete CPU simulation

## 🧪 Testing

Run comprehensive test suite:
```bash
python test_all.py
```

Tests all libraries with assertions for correctness.

## 📚 Documentation

- **INSTRUCTION_REFERENCE.md** - Detailed instruction set with examples
- **MATH_REFERENCE.md** - Mathematical formulas and algorithms
- **COMPLETE_GUIDE.md** - Full guide with usage examples

## 🎯 Learning Path

**Beginner:**
1. Run `add_two_numbers.asm` 
2. Explore `python boolean_algebra.py`
3. Try basic math functions

**Intermediate:**
1. Study `fibonacci.asm` and `multiply.asm`
2. Use calculus library
3. Build logic circuits

**Advanced:**
1. Modify ALU operations
2. Create custom assembly programs
3. Extend math libraries

## 🔗 References

- [Ben Eater's YouTube Series](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU)
- [Ben Eater's Website](https://eater.net/8bit)
- [SAP-1 Documentation](https://www.ullright.org/ullWiki/show/ben-eater-8-bit-computer-sap1)

## ✨ Features

✓ Complete 8-bit computer programming environment  
✓ Multi-architecture systems (8/16/32/64/128/256-bit)  
✓ Extended register set (A-Z, 26 registers)  
✓ Complete instruction set (100+ opcodes)  
✓ Missing opcodes 0x08 (MOV) and 0x09 (XCHG) implemented  
✓ **Complete GUI with LEDs, LCDs, switches, control signals** (NEW!)  
✓ **Authentic retro sound effects** (pong, printer, read/write)  
✓ **Multi-format displays** (Binary, Hex, Decimal, Octal)  
✓ **Control signal visualization** (MI, RI, RO, II, IO, AI, AO, EO, SU, BI, OI, CE, CO, J, FI)  
✓ **Instruction decode display** with real-time updates  
✓ **Memory viewer** with live monitoring  
✓ Interactive GUIs with LEDs and switches  
✓ Assembler and simulator tools  
✓ Logic gates and Boolean algebra  
✓ Calculus (derivatives, integrals, series)  
✓ Number theory and combinatorics  
✓ Computer architecture from first principles  
✓ Comprehensive test suite  
✓ Extensive documentation  

All implementations built from fundamental principles, perfect for learning computer science and mathematics!
