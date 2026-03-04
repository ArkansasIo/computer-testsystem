# System Architecture Overview

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MULTI-ARCHITECTURE COMPUTER SYSTEM                    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│  8-bit    16-bit    32-bit    64-bit    128-bit    256-bit             │
│  ┌────┐  ┌─────┐  ┌─────┐  ┌─────┐   ┌──────┐   ┌──────┐             │
│  │256B│  │64 KB│  │ 1MB │  │16MB │   │ 16MB │   │ 16MB │             │
│  └────┘  └─────┘  └─────┘  └─────┘   └──────┘   └──────┘             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         REGISTER SET (A-Z)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  General Purpose Registers (26):                                        │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐               │
│  │ A │ B │ C │ D │ E │ F │ G │ H │ I │ J │ K │ L │ M │               │
│  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘               │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐               │
│  │ N │ O │ P │ Q │ R │ S │ T │ U │ V │ W │ X │ Y │ Z │               │
│  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘               │
│                                                                          │
│  Special Registers:                                                     │
│  ┌────┬────┬─────┬────┐                                                │
│  │ PC │ SP │ MAR │ IR │                                                │
│  └────┴────┴─────┴────┘                                                │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      INSTRUCTION SET (100+ OPCODES)                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Data Movement (0x00-0x0F)                                              │
│  ┌─────┬─────┬─────┬─────┬─────┬──────┬──────┬─────┐                  │
│  │ NOP │ LDA │ LDB │ STA │ LDI │ MOV* │ XCHG*│ ... │                  │
│  └─────┴─────┴─────┴─────┴─────┴──────┴──────┴─────┘                  │
│                                                                          │
│  Arithmetic (0x10-0x1F)                                                 │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐                    │
│  │ ADD │ SUB │ MUL │ DIV │ MOD │ INC │ DEC │ ... │                    │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘                    │
│                                                                          │
│  Logical (0x20-0x2F)                                                    │
│  ┌─────┬─────┬─────┬─────┬──────┬─────┬──────┬─────┐                  │
│  │ AND │ OR  │ XOR │ NOT │ NAND │ NOR │ XNOR │ ... │                  │
│  └─────┴─────┴─────┴─────┴──────┴─────┴──────┴─────┘                  │
│                                                                          │
│  Control Flow (0x40-0x5F)                                               │
│  ┌─────┬────┬─────┬────┬──────┬─────┬──────┬─────┐                    │
│  │ JMP │ JZ │ JNZ │ JC │ CALL │ RET │ LOOP │ ... │                    │
│  └─────┴────┴─────┴────┴──────┴─────┴──────┴─────┘                    │
│                                                                          │
│  * Previously missing, now implemented                                  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            CPU FLAGS (5)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────┬───────┬──────────┬──────────┬────────┐                       │
│  │ Zero │ Carry │ Negative │ Overflow │ Parity │                       │
│  │  (Z) │  (C)  │   (N)    │   (O)    │  (P)   │                       │
│  └──────┴───────┴──────────┴──────────┴────────┘                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         GUI INTERFACES                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────┐  ┌──────────────────────────┐           │
│  │   Original 8-bit GUI     │  │  Multi-Architecture GUI  │           │
│  ├──────────────────────────┤  ├──────────────────────────┤           │
│  │ • Bus LEDs (8)           │  │ • Architecture Selector  │           │
│  │ • Register A/B LEDs      │  │ • All 26 Registers (A-Z) │           │
│  │ • Program Counter LEDs   │  │ • 5 CPU Flags            │           │
│  │ • Carry/Zero Flags       │  │ • Memory Viewer          │           │
│  │ • 7-Segment Display      │  │ • System Info            │           │
│  │ • Memory Switches        │  │ • Special Registers      │           │
│  │ • Step/Run/Reset         │  │ • Load Programs          │           │
│  │ • Clock Speed Control    │  │ • Step Execution         │           │
│  └──────────────────────────┘  └──────────────────────────┘           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      MATHEMATICAL LIBRARIES                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │ Boolean Algebra  │  │    Calculus      │  │   Math Library   │    │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤    │
│  │ • Logic Gates    │  │ • Derivatives    │  │ • Number Theory  │    │
│  │ • Truth Tables   │  │ • Integration    │  │ • Trigonometry   │    │
│  │ • Boolean Laws   │  │ • Taylor Series  │  │ • Statistics     │    │
│  │ • De Morgan's    │  │ • Limits         │  │ • Combinatorics  │    │
│  └──────────────────┘  │ • Newton Method  │  │ • Complex Nums   │    │
│                         └──────────────────┘  │ • Matrices       │    │
│  ┌──────────────────┐                         └──────────────────┘    │
│  │  Computer Arch   │                                                  │
│  ├──────────────────┤                                                  │
│  │ • Logic Gates    │                                                  │
│  │ • Adders         │                                                  │
│  │ • ALU            │                                                  │
│  │ • CPU Simulation │                                                  │
│  └──────────────────┘                                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      DEVELOPMENT TOOLS                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │  Assembler   │  │  Simulator   │  │  Test Suite  │                 │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤                 │
│  │ • ASM → BIN  │  │ • Execute    │  │ • Unit Tests │                 │
│  │ • Hex Output │  │ • Step Mode  │  │ • Integration│                 │
│  │ • Validation │  │ • Verbose    │  │ • Coverage   │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      ASSEMBLY PROGRAMS (15+)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Examples:          Logic Gates:        Math Operations:                │
│  • Fibonacci        • AND               • GCD                           │
│  • Multiply         • OR                • Power                         │
│  • Countdown        • XOR               • Modulo                        │
│  • Add Numbers      • NOT               • Factorial                     │
│  • Sum Sequence                         • Division                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐
│  Memory  │
│ (256B-   │
│  16MB)   │
└────┬─────┘
     │
     ├──────────────┐
     │              │
     ▼              ▼
┌─────────┐    ┌─────────┐
│   MAR   │    │   Bus   │
│ (Addr)  │    │ (Data)  │
└─────────┘    └────┬────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
     ▼              ▼              ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│   IR    │    │ Reg A-Z │    │   ALU   │
│ (Instr) │    │  (26)   │    │         │
└─────────┘    └─────────┘    └────┬────┘
                                    │
                                    ▼
                               ┌─────────┐
                               │  Flags  │
                               │ Z C N O │
                               └─────────┘
```

## Component Hierarchy

```
Computer System
├── Architecture Layer
│   ├── 8-bit Computer
│   ├── 16-bit Computer
│   ├── 32-bit Computer
│   ├── 64-bit Computer
│   ├── 128-bit Computer
│   └── 256-bit Computer
│
├── Register Set
│   ├── General Purpose (A-Z)
│   └── Special (PC, SP, MAR, IR)
│
├── Instruction Set
│   ├── Data Movement (0x00-0x0F)
│   ├── Arithmetic (0x10-0x1F)
│   ├── Logical (0x20-0x2F)
│   ├── Shift/Rotate (0x30-0x3F)
│   ├── Control Flow (0x40-0x5F)
│   ├── String Ops (0x60-0x6F)
│   ├── I/O (0x70-0x7F)
│   └── System (0x80-0x8F)
│
├── Memory System
│   ├── RAM
│   ├── Stack
│   └── Program Space
│
├── GUI Interfaces
│   ├── Original 8-bit GUI
│   └── Multi-Architecture GUI
│
├── Development Tools
│   ├── Assembler
│   ├── Simulator
│   └── Test Suite
│
└── Mathematical Libraries
    ├── Boolean Algebra
    ├── Calculus
    ├── Math Library
    └── Computer Architecture
```

## Execution Pipeline

```
1. FETCH
   ┌─────────────────┐
   │ PC → MAR        │
   │ Memory[MAR] → IR│
   │ PC++            │
   └─────────────────┘
          ↓
2. DECODE
   ┌─────────────────┐
   │ IR[7:4] → Opcode│
   │ IR[3:0] → Operand│
   └─────────────────┘
          ↓
3. EXECUTE
   ┌─────────────────┐
   │ Perform Operation│
   │ Update Registers│
   │ Set Flags       │
   └─────────────────┘
          ↓
4. WRITEBACK
   ┌─────────────────┐
   │ Store Result    │
   │ Update Memory   │
   └─────────────────┘
```

## System Integration

```
┌─────────────────────────────────────────────┐
│              User Interface                  │
│  (GUI with LEDs, Switches, Displays)        │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│         Computer Architecture                │
│  (8/16/32/64/128/256-bit Systems)           │
└──────────────┬──────────────────────────────┘
               │
               ├──────────┬──────────┬─────────┐
               ▼          ▼          ▼         ▼
         ┌─────────┐ ┌────────┐ ┌──────┐ ┌────────┐
         │Registers│ │ Memory │ │ ALU  │ │ Flags  │
         │  (A-Z)  │ │        │ │      │ │ (ZCNOP)│
         └─────────┘ └────────┘ └──────┘ └────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│         Instruction Execution                │
│  (100+ Opcodes, Full ISA)                   │
└─────────────────────────────────────────────┘
```

## Feature Matrix

| Feature | 8-bit | 16-bit | 32-bit | 64-bit | 128-bit | 256-bit |
|---------|-------|--------|--------|--------|---------|---------|
| Registers (A-Z) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Special Regs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 Flags | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stack Ops | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Subroutines | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| MOV (0x08) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| XCHG (0x09) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Full ISA | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| GUI Support | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Summary

This system provides a complete computer architecture implementation from 8-bit to 256-bit, with:
- ✅ All 26 registers (A-Z)
- ✅ Complete instruction set (100+ opcodes)
- ✅ Missing opcodes implemented (0x08, 0x09)
- ✅ Interactive GUIs
- ✅ Mathematical libraries
- ✅ Development tools
- ✅ Comprehensive documentation

**Everything is interconnected and fully functional!**
