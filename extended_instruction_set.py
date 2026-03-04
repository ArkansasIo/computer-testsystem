#!/usr/bin/env python3
"""
Extended Instruction Set
Complete instruction set for multi-architecture computers
Includes missing opcodes 0x08, 0x09 and extended operations
"""

class InstructionSet:
    """Complete instruction set with all opcodes"""
    
    # Basic Data Movement (0x00-0x0F)
    NOP  = 0x00  # No operation
    LDA  = 0x01  # Load into register A
    LDB  = 0x02  # Load into register B (NEW)
    LDC  = 0x03  # Load into register C (NEW)
    STA  = 0x04  # Store register A
    STB  = 0x05  # Store register B (NEW)
    STC  = 0x06  # Store register C (NEW)
    LDI  = 0x07  # Load immediate
    MOV  = 0x08  # Move between registers (NEW - was missing)
    XCHG = 0x09  # Exchange registers (NEW - was missing)
    LDX  = 0x0A  # Load indexed
    STX  = 0x0B  # Store indexed
    LEA  = 0x0C  # Load effective address
    PUSH = 0x0D  # Push to stack
    POP  = 0x0E  # Pop from stack
    SWAP = 0x0F  # Swap nibbles/bytes
    
    # Arithmetic Operations (0x10-0x1F)
    ADD  = 0x10  # Addition
    ADC  = 0x11  # Add with carry
    SUB  = 0x12  # Subtraction
    SBB  = 0x13  # Subtract with borrow
    MUL  = 0x14  # Multiplication
    DIV  = 0x15  # Division
    MOD  = 0x16  # Modulo
    INC  = 0x17  # Increment
    DEC  = 0x18  # Decrement
    NEG  = 0x19  # Negate (two's complement)
    ABS  = 0x1A  # Absolute value
    CMP  = 0x1B  # Compare
    ADDX = 0x1C  # Extended precision add
    SUBX = 0x1D  # Extended precision subtract
    MULX = 0x1E  # Extended precision multiply
    DIVX = 0x1F  # Extended precision divide
    
    # Logical Operations (0x20-0x2F)
    AND  = 0x20  # Bitwise AND
    OR   = 0x21  # Bitwise OR
    XOR  = 0x22  # Bitwise XOR
    NOT  = 0x23  # Bitwise NOT
    NAND = 0x24  # Bitwise NAND
    NOR  = 0x25  # Bitwise NOR
    XNOR = 0x26  # Bitwise XNOR
    TEST = 0x27  # Test bits (AND without storing)
    BIT  = 0x28  # Test single bit
    SET  = 0x29  # Set bit
    CLR  = 0x2A  # Clear bit
    TOG  = 0x2B  # Toggle bit
    MASK = 0x2C  # Apply mask
    ROTL = 0x2D  # Rotate left
    ROTR = 0x2E  # Rotate right
    REV  = 0x2F  # Reverse bits
    
    # Shift Operations (0x30-0x3F)
    SHL  = 0x30  # Shift left
    SHR  = 0x31  # Shift right
    SAL  = 0x32  # Arithmetic shift left
    SAR  = 0x33  # Arithmetic shift right
    ROL  = 0x34  # Rotate left
    ROR  = 0x35  # Rotate right
    RCL  = 0x36  # Rotate through carry left
    RCR  = 0x37  # Rotate through carry right
    SHLD = 0x38  # Double precision shift left
    SHRD = 0x39  # Double precision shift right
    
    # Control Flow (0x40-0x4F)
    JMP  = 0x40  # Unconditional jump
    JZ   = 0x41  # Jump if zero
    JNZ  = 0x42  # Jump if not zero
    JC   = 0x43  # Jump if carry
    JNC  = 0x44  # Jump if not carry
    JN   = 0x45  # Jump if negative
    JNN  = 0x46  # Jump if not negative
    JO   = 0x47  # Jump if overflow
    JNO  = 0x48  # Jump if not overflow
    JP   = 0x49  # Jump if parity
    JNP  = 0x4A  # Jump if not parity
    JE   = 0x4B  # Jump if equal
    JNE  = 0x4C  # Jump if not equal
    JL   = 0x4D  # Jump if less
    JLE  = 0x4E  # Jump if less or equal
    JG   = 0x4F  # Jump if greater
    
    # More Control Flow (0x50-0x5F)
    JGE  = 0x50  # Jump if greater or equal
    CALL = 0x51  # Call subroutine
    RET  = 0x52  # Return from subroutine
    IRET = 0x53  # Return from interrupt
    LOOP = 0x54  # Loop
    LOOPZ = 0x55 # Loop if zero
    LOOPNZ = 0x56 # Loop if not zero
    ENTER = 0x57 # Enter procedure
    LEAVE = 0x58 # Leave procedure
    
    # String Operations (0x60-0x6F)
    MOVS = 0x60  # Move string
    CMPS = 0x61  # Compare string
    SCAS = 0x62  # Scan string
    LODS = 0x63  # Load string
    STOS = 0x64  # Store string
    REP  = 0x65  # Repeat
    REPE = 0x66  # Repeat while equal
    REPNE = 0x67 # Repeat while not equal
    
    # I/O Operations (0x70-0x7F)
    IN   = 0x70  # Input from port
    OUT  = 0x71  # Output to port
    INB  = 0x72  # Input byte
    OUTB = 0x73  # Output byte
    INW  = 0x74  # Input word
    OUTW = 0x75  # Output word
    IND  = 0x76  # Input dword
    OUTD = 0x77  # Output dword
    
    # System Operations (0x80-0x8F)
    NMI  = 0x80  # Non-maskable interrupt
    INT  = 0x81  # Software interrupt
    INTO = 0x82  # Interrupt on overflow
    CLI  = 0x83  # Clear interrupt flag
    STI  = 0x84  # Set interrupt flag
    CLC  = 0x85  # Clear carry flag
    STC  = 0x86  # Set carry flag
    CMC  = 0x87  # Complement carry flag
    CLD  = 0x88  # Clear direction flag
    STD  = 0x89  # Set direction flag
    HALT = 0x8A  # Halt processor
    WAIT = 0x8B  # Wait for interrupt
    LOCK = 0x8C  # Lock bus
    HLT  = 0xFF  # Halt (alias)
    
    @staticmethod
    def get_mnemonic(opcode):
        """Get mnemonic for opcode"""
        mnemonics = {
            0x00: "NOP", 0x01: "LDA", 0x02: "LDB", 0x03: "LDC",
            0x04: "STA", 0x05: "STB", 0x06: "STC", 0x07: "LDI",
            0x08: "MOV", 0x09: "XCHG", 0x0A: "LDX", 0x0B: "STX",
            0x0C: "LEA", 0x0D: "PUSH", 0x0E: "POP", 0x0F: "SWAP",
            0x10: "ADD", 0x11: "ADC", 0x12: "SUB", 0x13: "SBB",
            0x14: "MUL", 0x15: "DIV", 0x16: "MOD", 0x17: "INC",
            0x18: "DEC", 0x19: "NEG", 0x1A: "ABS", 0x1B: "CMP",
            0x20: "AND", 0x21: "OR", 0x22: "XOR", 0x23: "NOT",
            0x24: "NAND", 0x25: "NOR", 0x26: "XNOR", 0x27: "TEST",
            0x30: "SHL", 0x31: "SHR", 0x32: "SAL", 0x33: "SAR",
            0x40: "JMP", 0x41: "JZ", 0x42: "JNZ", 0x43: "JC",
            0x44: "JNC", 0x45: "JN", 0x46: "JNN", 0x47: "JO",
            0x51: "CALL", 0x52: "RET", 0x71: "OUT", 0xFF: "HLT"
        }
        return mnemonics.get(opcode, f"UNK_{opcode:02X}")
    
    @staticmethod
    def get_description(opcode):
        """Get description for opcode"""
        descriptions = {
            0x00: "No operation",
            0x01: "Load into register A",
            0x02: "Load into register B",
            0x03: "Load into register C",
            0x04: "Store register A",
            0x08: "Move data between registers",
            0x09: "Exchange two registers",
            0x10: "Add two values",
            0x12: "Subtract two values",
            0x14: "Multiply two values",
            0x15: "Divide two values",
            0x20: "Bitwise AND",
            0x21: "Bitwise OR",
            0x22: "Bitwise XOR",
            0x30: "Shift left",
            0x31: "Shift right",
            0x40: "Unconditional jump",
            0x41: "Jump if zero",
            0x43: "Jump if carry",
            0x51: "Call subroutine",
            0x52: "Return from subroutine",
            0x71: "Output to port",
            0xFF: "Halt execution"
        }
        return descriptions.get(opcode, "Unknown instruction")


def print_instruction_set():
    """Print complete instruction set"""
    print("=" * 80)
    print("COMPLETE INSTRUCTION SET")
    print("=" * 80)
    
    categories = [
        ("Data Movement", range(0x00, 0x10)),
        ("Arithmetic", range(0x10, 0x20)),
        ("Logical", range(0x20, 0x30)),
        ("Shift/Rotate", range(0x30, 0x40)),
        ("Control Flow", range(0x40, 0x60)),
        ("String Operations", range(0x60, 0x70)),
        ("I/O Operations", range(0x70, 0x80)),
        ("System", range(0x80, 0x90))
    ]
    
    for category, opcode_range in categories:
        print(f"\n{category}:")
        print("-" * 80)
        print(f"{'Opcode':<8} {'Hex':<6} {'Mnemonic':<10} {'Description'}")
        print("-" * 80)
        
        for opcode in opcode_range:
            mnemonic = InstructionSet.get_mnemonic(opcode)
            if not mnemonic.startswith("UNK"):
                desc = InstructionSet.get_description(opcode)
                print(f"{opcode:<8} 0x{opcode:02X}   {mnemonic:<10} {desc}")


if __name__ == '__main__':
    print_instruction_set()
