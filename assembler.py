#!/usr/bin/env python3
"""
Simple assembler for Ben Eater's 8-bit computer
Converts assembly mnemonics to machine code
"""

# Instruction set mapping
OPCODES = {
    'NOP': 0x0,
    'LDA': 0x1,
    'ADD': 0x2,
    'SUB': 0x3,
    'STA': 0x4,
    'LDI': 0x5,
    'JMP': 0x6,
    'JC':  0x7,
    'JZ':  0x8,
    'OUT': 0xE,
    'HLT': 0xF
}

def parse_line(line):
    """Parse a single line of assembly code"""
    # Remove comments
    if ';' in line:
        line = line.split(';')[0]
    
    line = line.strip()
    if not line:
        return None
    
    parts = line.split()
    if len(parts) < 2:
        return None
    
    # Extract address and instruction/data
    addr_str = parts[0].rstrip(':')
    try:
        address = int(addr_str)
    except ValueError:
        return None
    
    # Check if it's an instruction or just data
    if parts[1].isdigit():
        # It's just a data value
        return address, None, int(parts[1])
    
    mnemonic = parts[1].upper()
    operand = int(parts[2]) if len(parts) > 2 else 0
    
    return address, mnemonic, operand

def assemble(filename):
    """Assemble a .asm file to machine code"""
    machine_code = {}
    
    with open(filename, 'r') as f:
        for line in f:
            result = parse_line(line)
            if result:
                address, mnemonic, operand = result
                
                if mnemonic is None:
                    # It's a data value
                    machine_code[address] = operand & 0xFF
                elif mnemonic in OPCODES:
                    opcode = OPCODES[mnemonic]
                    instruction = (opcode << 4) | (operand & 0x0F)
                    machine_code[address] = instruction
    
    return machine_code

def print_machine_code(machine_code):
    """Print machine code in various formats"""
    print("Address | Binary      | Hex | Decimal")
    print("--------|-------------|-----|--------")
    
    for addr in sorted(machine_code.keys()):
        value = machine_code[addr]
        binary = format(value, '08b')
        binary_formatted = f"{binary[:4]} {binary[4:]}"
        hex_val = format(value, '02X')
        
        print(f"{addr:2d}      | {binary_formatted} | {hex_val}  | {value}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <filename.asm>")
        sys.exit(1)
    
    filename = sys.argv[1]
    machine_code = assemble(filename)
    print(f"\nAssembled: {filename}\n")
    print_machine_code(machine_code)
    
    # Save binary output
    output_file = filename.replace('.asm', '.bin')
    with open(output_file, 'wb') as f:
        for addr in range(16):
            value = machine_code.get(addr, 0)
            f.write(bytes([value]))
    
    print(f"\nBinary output saved to: {output_file}")

if __name__ == '__main__':
    main()
