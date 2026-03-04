#!/usr/bin/env python3
"""
Simulator for Ben Eater's 8-bit computer
Executes machine code and shows register states
"""

class Computer:
    def __init__(self):
        self.memory = [0] * 16  # 16 bytes of RAM
        self.reg_a = 0          # Register A
        self.reg_b = 0          # Register B
        self.pc = 0             # Program counter
        self.carry_flag = False # Carry flag
        self.zero_flag = False  # Zero flag
        self.halted = False     # Halt flag
        self.output = None      # Output register
        
    def load_program(self, machine_code):
        """Load machine code into memory"""
        for addr, value in machine_code.items():
            if 0 <= addr < 16:
                self.memory[addr] = value & 0xFF
    
    def fetch(self):
        """Fetch instruction from memory"""
        instruction = self.memory[self.pc]
        self.pc = (self.pc + 1) & 0x0F  # 4-bit counter wraps at 16
        return instruction
    
    def execute(self, instruction):
        """Execute a single instruction"""
        opcode = (instruction >> 4) & 0x0F
        operand = instruction & 0x0F
        
        if opcode == 0x0:  # NOP
            pass
        
        elif opcode == 0x1:  # LDA
            self.reg_a = self.memory[operand]
        
        elif opcode == 0x2:  # ADD
            self.reg_b = self.memory[operand]
            result = self.reg_a + self.reg_b
            self.carry_flag = result > 255
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
        
        elif opcode == 0x3:  # SUB
            self.reg_b = self.memory[operand]
            result = self.reg_a - self.reg_b
            self.carry_flag = result >= 0
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
        
        elif opcode == 0x4:  # STA
            self.memory[operand] = self.reg_a
        
        elif opcode == 0x5:  # LDI
            self.reg_a = operand
        
        elif opcode == 0x6:  # JMP
            self.pc = operand
        
        elif opcode == 0x7:  # JC
            if self.carry_flag:
                self.pc = operand
        
        elif opcode == 0x8:  # JZ
            if self.zero_flag:
                self.pc = operand
        
        elif opcode == 0xE:  # OUT
            self.output = self.reg_a
            print(f"OUTPUT: {self.reg_a}")
        
        elif opcode == 0xF:  # HLT
            self.halted = True
    
    def print_state(self):
        """Print current state of the computer"""
        print(f"PC: {self.pc:2d} | A: {self.reg_a:3d} (0x{self.reg_a:02X}) | "
              f"B: {self.reg_b:3d} (0x{self.reg_b:02X}) | "
              f"Flags: C={int(self.carry_flag)} Z={int(self.zero_flag)}")
    
    def run(self, max_steps=1000, verbose=False):
        """Run the program"""
        steps = 0
        print("Starting execution...\n")
        
        while not self.halted and steps < max_steps:
            if verbose:
                self.print_state()
            
            instruction = self.fetch()
            self.execute(instruction)
            steps += 1
        
        print(f"\nExecution completed in {steps} steps")
        self.print_state()
        
        if self.output is not None:
            print(f"\nFinal output: {self.output}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simulator.py <filename.bin> [--verbose]")
        sys.exit(1)
    
    filename = sys.argv[1]
    verbose = '--verbose' in sys.argv
    
    # Load binary file
    machine_code = {}
    with open(filename, 'rb') as f:
        data = f.read()
        for i, byte in enumerate(data):
            machine_code[i] = byte
    
    # Create and run computer
    computer = Computer()
    computer.load_program(machine_code)
    computer.run(verbose=verbose)

if __name__ == '__main__':
    main()
