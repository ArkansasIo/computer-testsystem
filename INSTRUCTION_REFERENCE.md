# Ben Eater 8-bit Computer - Instruction Reference

## Architecture Overview

The computer is based on the SAP-1 (Simple As Possible) architecture with these characteristics:

- 8-bit data bus
- 4-bit address space (16 memory locations)
- 4-bit program counter
- Two 8-bit registers (A and B)
- ALU supporting addition and subtraction
- Two flags: Carry and Zero
- 7-segment display output

## Instruction Format

Each instruction is 8 bits:
```
[7:4] Opcode (4 bits)
[3:0] Operand (4 bits) - address or immediate value
```

## Complete Instruction Set

### Data Movement Instructions

#### LDA - Load Accumulator
```
Opcode: 0001 (0x1)
Format: LDA address
Description: Load value from memory address into register A
Example: LDA 14 ; Load value from address 14 into A
Flags: None affected
```

#### STA - Store Accumulator
```
Opcode: 0100 (0x4)
Format: STA address
Description: Store register A value to memory address
Example: STA 15 ; Store A to address 15
Flags: None affected
```

#### LDI - Load Immediate
```
Opcode: 0101 (0x5)
Format: LDI value
Description: Load 4-bit immediate value into register A
Example: LDI 7 ; Load value 7 into A
Flags: None affected
Range: 0-15 only (4-bit value)
```

### Arithmetic Instructions

#### ADD - Addition
```
Opcode: 0010 (0x2)
Format: ADD address
Description: Add memory value to register A
Operation: A = A + memory[address]
Example: ADD 14 ; A = A + memory[14]
Flags: Carry (if result > 255), Zero (if result = 0)
```

#### SUB - Subtraction
```
Opcode: 0011 (0x3)
Format: SUB address
Description: Subtract memory value from register A
Operation: A = A - memory[address]
Example: SUB 15 ; A = A - memory[15]
Flags: Carry (if result >= 0), Zero (if result = 0)
Note: Result wraps around (255 if negative)
```

### Control Flow Instructions

#### JMP - Unconditional Jump
```
Opcode: 0110 (0x6)
Format: JMP address
Description: Jump to address unconditionally
Example: JMP 0 ; Jump to address 0
Flags: None affected
```

#### JC - Jump if Carry
```
Opcode: 0111 (0x7)
Format: JC address
Description: Jump to address if carry flag is set
Example: JC 12 ; Jump to address 12 if carry flag set
Flags: None affected
Use: Detect overflow in addition, or positive result in subtraction
```

#### JZ - Jump if Zero
```
Opcode: 1000 (0x8)
Format: JZ address
Description: Jump to address if zero flag is set
Example: JZ 10 ; Jump to address 10 if zero flag set
Flags: None affected
Use: Loop termination, equality testing
```

### I/O and Control Instructions

#### OUT - Output
```
Opcode: 1110 (0xE)
Format: OUT
Description: Display register A on 7-segment display
Example: OUT ; Display A value
Flags: None affected
Display: Shows decimal value 0-255
```

#### HLT - Halt
```
Opcode: 1111 (0xF)
Format: HLT
Description: Stop program execution
Example: HLT ; Stop the computer
Flags: None affected
```

#### NOP - No Operation
```
Opcode: 0000 (0x0)
Format: NOP
Description: Do nothing, advance to next instruction
Example: NOP ; No operation
Flags: None affected
```

## Flag Behavior

### Carry Flag
- Set by ADD when result exceeds 255
- Set by SUB when result is non-negative (no borrow)
- Used for multi-byte arithmetic and overflow detection

### Zero Flag
- Set when arithmetic result equals zero
- Used for loop termination and equality testing

## Programming Patterns

### Loop Pattern
```assembly
0: LDA counter
1: JZ end      ; Exit if counter is zero
2: ; ... loop body ...
5: SUB one     ; Decrement counter
6: STA counter
7: JMP 0       ; Repeat
end: HLT
```

### Accumulation Pattern
```assembly
0: LDA sum
1: ADD value
2: STA sum
3: ; ... continue ...
```

### Conditional Execution
```assembly
0: LDA value1
1: SUB value2
2: JZ equal    ; Jump if values are equal
3: ; ... not equal code ...
5: JMP done
equal: ; ... equal code ...
done: HLT
```

## Memory Layout Best Practices

- Addresses 0-11: Program code
- Addresses 12-15: Data storage
- Keep frequently accessed data in lower addresses
- Reserve address 15 for constants (like 1 for decrementing)

## Limitations

- Only 16 memory locations total
- 4-bit immediate values (0-15 range)
- No stack or subroutines
- No indirect addressing
- Single accumulator architecture
- Programs must fit in available memory including data

## Tips for Programming

1. Plan memory layout before coding
2. Use LDI for small constants (0-15)
3. Store frequently used values like 1 in memory
4. Minimize jumps for better readability
5. Comment your code extensively
6. Test with simulator before hardware

## References

Based on the SAP-1 architecture described in:
- [Ben Eater's YouTube series](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU)
- Digital Computer Electronics by Malvino & Brown
