#!/usr/bin/env python3
"""
Multi-Architecture Computer Systems
Implements 8, 16, 32, 64, 128, and 256-bit computer architectures
with extended register sets (A-Z) and enhanced instruction sets
"""

class BaseComputer:
    """Base class for all computer architectures"""
    
    def __init__(self, bit_width, memory_size, num_registers=26):
        self.bit_width = bit_width
        self.max_value = (1 << bit_width) - 1
        self.memory_size = memory_size
        self.memory = [0] * memory_size
        
        # Extended register set: A-Z (26 registers)
        self.num_registers = num_registers
        self.registers = [0] * num_registers
        
        # Special registers
        self.pc = 0  # Program counter
        self.sp = memory_size - 1  # Stack pointer
        self.mar = 0  # Memory address register
        self.ir = 0  # Instruction register
        
        # Flags
        self.zero_flag = False
        self.carry_flag = False
        self.negative_flag = False
        self.overflow_flag = False
        self.parity_flag = False
        
        # Control
        self.halted = False
        self.running = False
        
    def reset(self):
        """Reset computer to initial state"""
        self.registers = [0] * self.num_registers
        self.pc = 0
        self.sp = self.memory_size - 1
        self.mar = 0
        self.ir = 0
        self.zero_flag = False
        self.carry_flag = False
        self.negative_flag = False
        self.overflow_flag = False
        self.parity_flag = False
        self.halted = False
        self.running = False
        
    def load_program(self, program):
        """Load program into memory"""
        for addr, value in program.items():
            if 0 <= addr < self.memory_size:
                self.memory[addr] = value & self.max_value
                
    def get_register(self, reg_id):
        """Get register value by ID (0=A, 1=B, ..., 25=Z)"""
        if 0 <= reg_id < self.num_registers:
            return self.registers[reg_id]
        return 0
        
    def set_register(self, reg_id, value):
        """Set register value"""
        if 0 <= reg_id < self.num_registers:
            self.registers[reg_id] = value & self.max_value
            
    def update_flags(self, result):
        """Update CPU flags based on result"""
        self.zero_flag = (result == 0)
        self.negative_flag = (result & (1 << (self.bit_width - 1))) != 0
        
        # Parity flag (even number of 1 bits)
        bits = bin(result).count('1')
        self.parity_flag = (bits % 2 == 0)
        
    def push(self, value):
        """Push value onto stack"""
        if self.sp > 0:
            self.memory[self.sp] = value & self.max_value
            self.sp -= 1
            
    def pop(self):
        """Pop value from stack"""
        if self.sp < self.memory_size - 1:
            self.sp += 1
            return self.memory[self.sp]
        return 0


class Computer8Bit(BaseComputer):
    """8-bit computer (original SAP-1 compatible)"""
    
    def __init__(self):
        super().__init__(bit_width=8, memory_size=256, num_registers=26)
        
    def execute_instruction(self, opcode, operand1, operand2=0):
        """Execute instruction"""
        if opcode == 0x00:  # NOP
            pass
        elif opcode == 0x01:  # LDA - Load into A
            self.registers[0] = self.memory[operand1]
        elif opcode == 0x02:  # ADD - Add to A
            result = self.registers[0] + self.memory[operand1]
            self.carry_flag = result > 255
            self.registers[0] = result & 0xFF
            self.update_flags(self.registers[0])
        elif opcode == 0x03:  # SUB - Subtract from A
            result = self.registers[0] - self.memory[operand1]
            self.carry_flag = result >= 0
            self.registers[0] = result & 0xFF
            self.update_flags(self.registers[0])
        elif opcode == 0x04:  # STA - Store A
            self.memory[operand1] = self.registers[0]
        elif opcode == 0x05:  # LDI - Load immediate
            self.registers[0] = operand1
        elif opcode == 0x06:  # JMP - Jump
            self.pc = operand1
        elif opcode == 0x07:  # JC - Jump if carry
            if self.carry_flag:
                self.pc = operand1
        elif opcode == 0x08:  # JZ - Jump if zero
            if self.zero_flag:
                self.pc = operand1
        elif opcode == 0x09:  # JN - Jump if negative
            if self.negative_flag:
                self.pc = operand1
        elif opcode == 0x0E:  # OUT - Output
            pass  # Handled by GUI
        elif opcode == 0x0F:  # HLT - Halt
            self.halted = True


class Computer16Bit(BaseComputer):
    """16-bit computer with extended features"""
    
    def __init__(self):
        super().__init__(bit_width=16, memory_size=65536, num_registers=26)
        
    def execute_instruction(self, opcode, operand1, operand2=0):
        """Execute 16-bit instruction"""
        # Basic operations (0x00-0x0F)
        if opcode == 0x00:  # NOP
            pass
        elif opcode == 0x01:  # LDR - Load register
            reg = operand1 & 0x1F  # 5 bits for register (0-25)
            addr = operand2
            self.registers[reg] = self.memory[addr]
        elif opcode == 0x02:  # STR - Store register
            reg = operand1 & 0x1F
            addr = operand2
            self.memory[addr] = self.registers[reg]
        elif opcode == 0x03:  # ADD - Add registers
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            result = self.registers[reg_dest] + self.registers[reg_src]
            self.carry_flag = result > self.max_value
            self.registers[reg_dest] = result & self.max_value
            self.update_flags(self.registers[reg_dest])
        elif opcode == 0x04:  # SUB - Subtract
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            result = self.registers[reg_dest] - self.registers[reg_src]
            self.carry_flag = result >= 0
            self.registers[reg_dest] = result & self.max_value
            self.update_flags(self.registers[reg_dest])
        elif opcode == 0x05:  # MUL - Multiply
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            result = self.registers[reg_dest] * self.registers[reg_src]
            self.overflow_flag = result > self.max_value
            self.registers[reg_dest] = result & self.max_value
            self.update_flags(self.registers[reg_dest])
        elif opcode == 0x06:  # DIV - Divide
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            if self.registers[reg_src] != 0:
                self.registers[reg_dest] = self.registers[reg_dest] // self.registers[reg_src]
                self.update_flags(self.registers[reg_dest])
        elif opcode == 0x07:  # AND - Bitwise AND
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            self.registers[reg_dest] &= self.registers[reg_src]
            self.update_flags(self.registers[reg_dest])
        elif opcode == 0x08:  # OR - Bitwise OR
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            self.registers[reg_dest] |= self.registers[reg_src]
            self.update_flags(self.registers[reg_dest])
        elif opcode == 0x09:  # XOR - Bitwise XOR
            reg_dest = operand1 & 0x1F
            reg_src = operand2 & 0x1F
            self.registers[reg_dest] ^= self.registers[reg_src]
            self.update_flags(self.registers[reg_dest])
        elif opcode == 0x0A:  # SHL - Shift left
            reg = operand1 & 0x1F
            self.registers[reg] = (self.registers[reg] << 1) & self.max_value
            self.update_flags(self.registers[reg])
        elif opcode == 0x0B:  # SHR - Shift right
            reg = operand1 & 0x1F
            self.registers[reg] >>= 1
            self.update_flags(self.registers[reg])
        elif opcode == 0x0C:  # PUSH - Push to stack
            reg = operand1 & 0x1F
            self.push(self.registers[reg])
        elif opcode == 0x0D:  # POP - Pop from stack
            reg = operand1 & 0x1F
            self.registers[reg] = self.pop()
        elif opcode == 0x0E:  # CALL - Call subroutine
            self.push(self.pc)
            self.pc = operand1
        elif opcode == 0x0F:  # RET - Return from subroutine
            self.pc = self.pop()
        elif opcode == 0x10:  # JMP - Jump
            self.pc = operand1
        elif opcode == 0x11:  # JZ - Jump if zero
            if self.zero_flag:
                self.pc = operand1
        elif opcode == 0x12:  # JNZ - Jump if not zero
            if not self.zero_flag:
                self.pc = operand1
        elif opcode == 0x13:  # JC - Jump if carry
            if self.carry_flag:
                self.pc = operand1
        elif opcode == 0xFE:  # OUT - Output
            pass
        elif opcode == 0xFF:  # HLT - Halt
            self.halted = True


class Computer32Bit(BaseComputer):
    """32-bit computer"""
    
    def __init__(self):
        super().__init__(bit_width=32, memory_size=1048576, num_registers=26)
        
    def execute_instruction(self, opcode, operand1, operand2=0):
        """Execute 32-bit instruction (similar to 16-bit but wider)"""
        # Reuse 16-bit logic with 32-bit values
        comp16 = Computer16Bit()
        comp16.bit_width = 32
        comp16.max_value = self.max_value
        comp16.registers = self.registers
        comp16.memory = self.memory
        comp16.execute_instruction(opcode, operand1, operand2)
        self.registers = comp16.registers
        self.update_flags(self.registers[0])


class Computer64Bit(BaseComputer):
    """64-bit computer"""
    
    def __init__(self):
        super().__init__(bit_width=64, memory_size=16777216, num_registers=26)


class Computer128Bit(BaseComputer):
    """128-bit computer"""
    
    def __init__(self):
        super().__init__(bit_width=128, memory_size=16777216, num_registers=26)


class Computer256Bit(BaseComputer):
    """256-bit computer"""
    
    def __init__(self):
        super().__init__(bit_width=256, memory_size=16777216, num_registers=26)


def main():
    """Demonstrate different architectures"""
    print("=" * 70)
    print("MULTI-ARCHITECTURE COMPUTER SYSTEMS")
    print("=" * 70)
    
    architectures = [
        ("8-bit", Computer8Bit()),
        ("16-bit", Computer16Bit()),
        ("32-bit", Computer32Bit()),
        ("64-bit", Computer64Bit()),
        ("128-bit", Computer128Bit()),
        ("256-bit", Computer256Bit())
    ]
    
    for name, computer in architectures:
        print(f"\n{name} Computer:")
        print(f"  Bit Width: {computer.bit_width}")
        print(f"  Max Value: {computer.max_value:,}")
        print(f"  Memory Size: {computer.memory_size:,} bytes")
        print(f"  Registers: {computer.num_registers} (A-Z)")
        print(f"  Address Space: {computer.bit_width}-bit")
        
        # Test basic operation
        computer.registers[0] = 42  # Set register A
        computer.registers[1] = 8   # Set register B
        print(f"  Register A: {computer.registers[0]}")
        print(f"  Register B: {computer.registers[1]}")


if __name__ == '__main__':
    main()
