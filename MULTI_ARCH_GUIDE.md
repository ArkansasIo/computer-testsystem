# Multi-Architecture Computer Systems Guide

## Overview

Complete implementation of 8-bit through 256-bit computer architectures with extended register sets (A-Z), enhanced instruction sets, and advanced GUI interfaces.

## Architectures Supported

### 8-bit Computer
- **Bit Width:** 8 bits
- **Max Value:** 255
- **Memory:** 256 bytes
- **Registers:** 26 (A-Z)
- **Address Space:** 8-bit (256 locations)
- **Compatible with:** Original Ben Eater SAP-1

### 16-bit Computer
- **Bit Width:** 16 bits
- **Max Value:** 65,535
- **Memory:** 64 KB (65,536 bytes)
- **Registers:** 26 (A-Z)
- **Address Space:** 16-bit
- **Features:** Extended instruction set, stack operations, subroutines

### 32-bit Computer
- **Bit Width:** 32 bits
- **Max Value:** 4,294,967,295
- **Memory:** 1 MB (1,048,576 bytes)
- **Registers:** 26 (A-Z)
- **Address Space:** 32-bit
- **Features:** Full arithmetic, floating point support (future)

### 64-bit Computer
- **Bit Width:** 64 bits
- **Max Value:** 18,446,744,073,709,551,615
- **Memory:** 16 MB
- **Registers:** 26 (A-Z)
- **Address Space:** 64-bit
- **Features:** Large data processing, extended precision

### 128-bit Computer
- **Bit Width:** 128 bits
- **Max Value:** 340,282,366,920,938,463,463,374,607,431,768,211,455
- **Memory:** 16 MB
- **Registers:** 26 (A-Z)
- **Address Space:** 128-bit
- **Features:** Cryptographic operations, SIMD

### 256-bit Computer
- **Bit Width:** 256 bits
- **Max Value:** 2^256 - 1
- **Memory:** 16 MB
- **Registers:** 26 (A-Z)
- **Address Space:** 256-bit
- **Features:** Advanced cryptography, quantum-resistant algorithms

## Extended Register Set

All architectures support 26 general-purpose registers:

```
A, B, C, D, E, F, G, H, I, J, K, L, M,
N, O, P, Q, R, S, T, U, V, W, X, Y, Z
```

### Special Registers

- **PC** - Program Counter (instruction pointer)
- **SP** - Stack Pointer
- **MAR** - Memory Address Register
- **IR** - Instruction Register

### Flags

- **Z** - Zero Flag (result is zero)
- **C** - Carry Flag (arithmetic carry/borrow)
- **N** - Negative Flag (result is negative)
- **O** - Overflow Flag (signed overflow)
- **P** - Parity Flag (even number of 1 bits)

## Complete Instruction Set

### Data Movement (0x00-0x0F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x00 | NOP | No operation |
| 0x01 | LDA | Load into register A |
| 0x02 | LDB | Load into register B |
| 0x03 | LDC | Load into register C |
| 0x04 | STA | Store register A |
| 0x05 | STB | Store register B |
| 0x06 | STC | Store register C |
| 0x07 | LDI | Load immediate value |
| 0x08 | MOV | Move between registers |
| 0x09 | XCHG | Exchange two registers |
| 0x0A | LDX | Load indexed |
| 0x0B | STX | Store indexed |
| 0x0C | LEA | Load effective address |
| 0x0D | PUSH | Push to stack |
| 0x0E | POP | Pop from stack |
| 0x0F | SWAP | Swap nibbles/bytes |

### Arithmetic (0x10-0x1F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x10 | ADD | Addition |
| 0x11 | ADC | Add with carry |
| 0x12 | SUB | Subtraction |
| 0x13 | SBB | Subtract with borrow |
| 0x14 | MUL | Multiplication |
| 0x15 | DIV | Division |
| 0x16 | MOD | Modulo |
| 0x17 | INC | Increment |
| 0x18 | DEC | Decrement |
| 0x19 | NEG | Negate (two's complement) |
| 0x1A | ABS | Absolute value |
| 0x1B | CMP | Compare |

### Logical (0x20-0x2F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x20 | AND | Bitwise AND |
| 0x21 | OR | Bitwise OR |
| 0x22 | XOR | Bitwise XOR |
| 0x23 | NOT | Bitwise NOT |
| 0x24 | NAND | Bitwise NAND |
| 0x25 | NOR | Bitwise NOR |
| 0x26 | XNOR | Bitwise XNOR |
| 0x27 | TEST | Test bits (AND without storing) |
| 0x28 | BIT | Test single bit |
| 0x29 | SET | Set bit |
| 0x2A | CLR | Clear bit |
| 0x2B | TOG | Toggle bit |

### Shift/Rotate (0x30-0x3F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x30 | SHL | Shift left |
| 0x31 | SHR | Shift right |
| 0x32 | SAL | Arithmetic shift left |
| 0x33 | SAR | Arithmetic shift right |
| 0x34 | ROL | Rotate left |
| 0x35 | ROR | Rotate right |
| 0x36 | RCL | Rotate through carry left |
| 0x37 | RCR | Rotate through carry right |

### Control Flow (0x40-0x5F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x40 | JMP | Unconditional jump |
| 0x41 | JZ | Jump if zero |
| 0x42 | JNZ | Jump if not zero |
| 0x43 | JC | Jump if carry |
| 0x44 | JNC | Jump if not carry |
| 0x45 | JN | Jump if negative |
| 0x46 | JNN | Jump if not negative |
| 0x47 | JO | Jump if overflow |
| 0x48 | JNO | Jump if not overflow |
| 0x51 | CALL | Call subroutine |
| 0x52 | RET | Return from subroutine |
| 0x54 | LOOP | Loop |

### I/O (0x70-0x7F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x70 | IN | Input from port |
| 0x71 | OUT | Output to port |
| 0x72 | INB | Input byte |
| 0x73 | OUTB | Output byte |

### System (0x80-0x8F)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x81 | INT | Software interrupt |
| 0x83 | CLI | Clear interrupt flag |
| 0x84 | STI | Set interrupt flag |
| 0x85 | CLC | Clear carry flag |
| 0x86 | STC | Set carry flag |
| 0x8A | HALT | Halt processor |
| 0xFF | HLT | Halt (alias) |

## GUI Features

### Multi-Architecture GUI (`multi_arch_gui.py`)

Features:
- Switch between architectures on-the-fly
- View all 26 registers (A-Z) in real-time
- Monitor special registers (PC, SP, MAR, IR)
- Track all 5 flags (Z, C, N, O, P)
- Memory viewer with hex dump
- System information display
- Load programs from binary files
- Step-by-step execution
- Reset and run controls

### Usage

```bash
python multi_arch_gui.py
```

#### Switching Architectures

1. Click architecture button (8-bit, 16-bit, 32-bit, etc.)
2. System automatically reconfigures
3. All displays update to show new architecture

#### Viewing Registers

- All 26 registers displayed in grid format
- Shows decimal and hexadecimal values
- Updates in real-time during execution

#### Memory Viewer

1. Enter starting address
2. Click "View" button
3. See hex dump of memory contents
4. 16 bytes per line format

## Programming Examples

### Example 1: Using Extended Registers (16-bit)

```assembly
; Load values into multiple registers
LDR A, 100    ; Load 100 into register A
LDR B, 200    ; Load 200 into register B
LDR C, 300    ; Load 300 into register C

; Perform operations
ADD A, B      ; A = A + B (300)
ADD A, C      ; A = A + C (600)

; Store result
STR A, 500    ; Store result at address 500

OUT A         ; Output result
HLT           ; Halt
```

### Example 2: Using MOV and XCHG (NEW opcodes 0x08, 0x09)

```assembly
; MOV instruction (0x08)
LDI A, 42     ; Load 42 into A
MOV B, A      ; Copy A to B (B = 42)
MOV C, B      ; Copy B to C (C = 42)

; XCHG instruction (0x09)
LDI D, 10     ; D = 10
LDI E, 20     ; E = 20
XCHG D, E     ; Swap D and E (D=20, E=10)

OUT D         ; Output 20
HLT
```

### Example 3: Stack Operations

```assembly
; Push values onto stack
LDI A, 10
PUSH A
LDI A, 20
PUSH A
LDI A, 30
PUSH A

; Pop values (reverse order)
POP B         ; B = 30
POP C         ; C = 20
POP D         ; D = 10

OUT B         ; Output 30
HLT
```

### Example 4: Subroutine Call

```assembly
; Main program
LDI A, 5
CALL 100      ; Call subroutine at address 100
OUT A         ; Output result
HLT

; Subroutine at address 100
100: MUL A, A  ; Square the value
     RET       ; Return to caller
```

## File Structure

```
.
├── computer_architectures.py    # All architecture implementations
├── extended_instruction_set.py  # Complete instruction set
├── multi_arch_gui.py           # Advanced GUI
├── computer_gui.py             # Original 8-bit GUI
├── MULTI_ARCH_GUIDE.md         # This guide
└── GUI_GUIDE.md                # Original GUI guide
```

## Running the Systems

### Test Architectures
```bash
python computer_architectures.py
```

### View Instruction Set
```bash
python extended_instruction_set.py
```

### Run Multi-Architecture GUI
```bash
python multi_arch_gui.py
```

### Run Original 8-bit GUI
```bash
python computer_gui.py
```

## Technical Specifications

### Memory Organization

**8-bit:**
- 256 bytes total
- 0-191: Program space
- 192-255: Stack space

**16-bit:**
- 64 KB total
- 0-32767: Program space
- 32768-65535: Stack and data

**32-bit and above:**
- 1 MB+ total
- Flexible memory layout
- Large stack space

### Register Usage Conventions

- **A-D:** General purpose, arithmetic
- **E-H:** General purpose, data movement
- **I-L:** Loop counters, indices
- **M-P:** Temporary storage
- **Q-T:** Function parameters
- **U-X:** Function return values
- **Y-Z:** Reserved for system use

## Performance Characteristics

| Architecture | Max Value | Memory | Registers | Typical Use |
|--------------|-----------|--------|-----------|-------------|
| 8-bit | 255 | 256 B | 26 | Learning, embedded |
| 16-bit | 65K | 64 KB | 26 | Retro computing |
| 32-bit | 4.3B | 1 MB | 26 | General purpose |
| 64-bit | 18.4E | 16 MB | 26 | Modern computing |
| 128-bit | 3.4E38 | 16 MB | 26 | Cryptography |
| 256-bit | 1.2E77 | 16 MB | 26 | Advanced crypto |

## Future Enhancements

Planned features:
- Floating point operations
- SIMD instructions
- Virtual memory
- Cache simulation
- Pipeline visualization
- Interrupt handling
- DMA operations
- Multi-core support

## Comparison to Real Architectures

### 8-bit: Similar to
- Intel 8080
- Zilog Z80
- MOS 6502

### 16-bit: Similar to
- Intel 8086
- Zilog Z8000

### 32-bit: Similar to
- Intel 80386
- ARM7

### 64-bit: Similar to
- x86-64
- ARM64

## See Also

- `INSTRUCTION_REFERENCE.md` - Original 8-bit instruction set
- `COMPLETE_GUIDE.md` - Full project documentation
- `GUI_GUIDE.md` - Original GUI usage
- `MATH_REFERENCE.md` - Mathematical foundations
