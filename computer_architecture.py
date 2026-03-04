#!/usr/bin/env python3
"""
Computer Architecture Components
Implements fundamental computer building blocks:
- Logic gates
- Adders (half, full, ripple-carry)
- ALU (Arithmetic Logic Unit)
- Memory (registers, RAM)
- CPU components
"""

class LogicGates:
    """Fundamental logic gates"""
    
    @staticmethod
    def AND(a, b):
        return int(a and b)
    
    @staticmethod
    def OR(a, b):
        return int(a or b)
    
    @staticmethod
    def NOT(a):
        return int(not a)
    
    @staticmethod
    def NAND(a, b):
        return LogicGates.NOT(LogicGates.AND(a, b))
    
    @staticmethod
    def NOR(a, b):
        return LogicGates.NOT(LogicGates.OR(a, b))
    
    @staticmethod
    def XOR(a, b):
        return int(a != b)
    
    @staticmethod
    def XNOR(a, b):
        return int(a == b)


class Adders:
    """Adder circuits"""
    
    @staticmethod
    def half_adder(a, b):
        """
        Half Adder: adds two bits
        Returns: (sum, carry)
        sum = a XOR b
        carry = a AND b
        """
        sum_bit = LogicGates.XOR(a, b)
        carry = LogicGates.AND(a, b)
        return (sum_bit, carry)
    
    @staticmethod
    def full_adder(a, b, carry_in):
        """
        Full Adder: adds three bits (a, b, carry_in)
        Returns: (sum, carry_out)
        """
        # First half adder
        sum1, carry1 = Adders.half_adder(a, b)
        # Second half adder
        sum_out, carry2 = Adders.half_adder(sum1, carry_in)
        # Combine carries
        carry_out = LogicGates.OR(carry1, carry2)
        return (sum_out, carry_out)
    
    @staticmethod
    def ripple_carry_adder(a_bits, b_bits):
        """
        Ripple Carry Adder: adds two n-bit numbers
        a_bits, b_bits: lists of bits (LSB first)
        Returns: (sum_bits, carry_out)
        """
        n = max(len(a_bits), len(b_bits))
        # Pad to same length
        a_bits = a_bits + [0] * (n - len(a_bits))
        b_bits = b_bits + [0] * (n - len(b_bits))
        
        sum_bits = []
        carry = 0
        
        for i in range(n):
            sum_bit, carry = Adders.full_adder(a_bits[i], b_bits[i], carry)
            sum_bits.append(sum_bit)
        
        return (sum_bits, carry)
    
    @staticmethod
    def subtractor(a_bits, b_bits):
        """
        Subtractor using two's complement
        a - b = a + (-b) = a + (NOT b + 1)
        """
        # Invert b_bits (one's complement)
        b_inverted = [LogicGates.NOT(bit) for bit in b_bits]
        # Add 1 (two's complement)
        one = [1] + [0] * (len(b_inverted) - 1)
        b_negated, _ = Adders.ripple_carry_adder(b_inverted, one)
        # Add a + (-b)
        result, borrow = Adders.ripple_carry_adder(a_bits, b_negated)
        return (result, borrow)


class ALU:
    """Arithmetic Logic Unit"""
    
    def __init__(self, bit_width=8):
        self.bit_width = bit_width
        self.zero_flag = False
        self.carry_flag = False
        self.negative_flag = False
    
    def _to_bits(self, value):
        """Convert integer to bit list (LSB first)"""
        bits = []
        for _ in range(self.bit_width):
            bits.append(value & 1)
            value >>= 1
        return bits
    
    def _from_bits(self, bits):
        """Convert bit list to integer"""
        value = 0
        for i, bit in enumerate(bits):
            value |= (bit << i)
        return value
    
    def _update_flags(self, result, carry):
        """Update ALU flags"""
        self.zero_flag = (result == 0)
        self.carry_flag = carry
        self.negative_flag = (result & (1 << (self.bit_width - 1))) != 0
    
    def add(self, a, b):
        """Add two numbers"""
        a_bits = self._to_bits(a)
        b_bits = self._to_bits(b)
        sum_bits, carry = Adders.ripple_carry_adder(a_bits, b_bits)
        result = self._from_bits(sum_bits)
        self._update_flags(result, carry)
        return result
    
    def subtract(self, a, b):
        """Subtract b from a"""
        a_bits = self._to_bits(a)
        b_bits = self._to_bits(b)
        diff_bits, borrow = Adders.subtractor(a_bits, b_bits)
        result = self._from_bits(diff_bits)
        self._update_flags(result, not borrow)
        return result
    
    def AND(self, a, b):
        """Bitwise AND"""
        result = a & b & ((1 << self.bit_width) - 1)
        self._update_flags(result, False)
        return result
    
    def OR(self, a, b):
        """Bitwise OR"""
        result = (a | b) & ((1 << self.bit_width) - 1)
        self._update_flags(result, False)
        return result
    
    def XOR(self, a, b):
        """Bitwise XOR"""
        result = (a ^ b) & ((1 << self.bit_width) - 1)
        self._update_flags(result, False)
        return result
    
    def NOT(self, a):
        """Bitwise NOT"""
        result = (~a) & ((1 << self.bit_width) - 1)
        self._update_flags(result, False)
        return result
    
    def shift_left(self, a, positions=1):
        """Logical shift left"""
        result = (a << positions) & ((1 << self.bit_width) - 1)
        carry = (a >> (self.bit_width - positions)) & 1
        self._update_flags(result, carry)
        return result
    
    def shift_right(self, a, positions=1):
        """Logical shift right"""
        carry = (a >> (positions - 1)) & 1
        result = a >> positions
        self._update_flags(result, carry)
        return result


class Register:
    """Register - stores n-bit value"""
    
    def __init__(self, bit_width=8):
        self.bit_width = bit_width
        self.value = 0
        self.max_value = (1 << bit_width) - 1
    
    def load(self, value):
        """Load value into register"""
        self.value = value & self.max_value
    
    def read(self):
        """Read value from register"""
        return self.value
    
    def clear(self):
        """Clear register to 0"""
        self.value = 0


class RAM:
    """Random Access Memory"""
    
    def __init__(self, size=256, word_size=8):
        self.size = size
        self.word_size = word_size
        self.memory = [0] * size
        self.max_value = (1 << word_size) - 1
    
    def write(self, address, value):
        """Write value to address"""
        if 0 <= address < self.size:
            self.memory[address] = value & self.max_value
        else:
            raise IndexError(f"Address {address} out of range")
    
    def read(self, address):
        """Read value from address"""
        if 0 <= address < self.size:
            return self.memory[address]
        else:
            raise IndexError(f"Address {address} out of range")
    
    def clear(self):
        """Clear all memory"""
        self.memory = [0] * self.size


class ProgramCounter:
    """Program Counter - tracks current instruction address"""
    
    def __init__(self, bit_width=8):
        self.bit_width = bit_width
        self.value = 0
        self.max_value = (1 << bit_width) - 1
    
    def increment(self):
        """Increment counter"""
        self.value = (self.value + 1) & self.max_value
    
    def jump(self, address):
        """Jump to address"""
        self.value = address & self.max_value
    
    def reset(self):
        """Reset to 0"""
        self.value = 0
    
    def read(self):
        """Read current value"""
        return self.value


class SimpleCPU:
    """Simple CPU combining all components"""
    
    def __init__(self):
        self.alu = ALU(8)
        self.reg_a = Register(8)
        self.reg_b = Register(8)
        self.pc = ProgramCounter(8)
        self.ram = RAM(256, 8)
        self.halted = False
    
    def reset(self):
        """Reset CPU to initial state"""
        self.reg_a.clear()
        self.reg_b.clear()
        self.pc.reset()
        self.halted = False
    
    def get_state(self):
        """Get current CPU state"""
        return {
            'PC': self.pc.read(),
            'A': self.reg_a.read(),
            'B': self.reg_b.read(),
            'Zero': self.alu.zero_flag,
            'Carry': self.alu.carry_flag,
            'Negative': self.alu.negative_flag
        }


def main():
    """Demonstrate computer architecture components"""
    print("=" * 70)
    print("COMPUTER ARCHITECTURE COMPONENTS")
    print("=" * 70)
    
    print("\n1. LOGIC GATES")
    print("-" * 70)
    print("Truth table for XOR:")
    for a in [0, 1]:
        for b in [0, 1]:
            result = LogicGates.XOR(a, b)
            print(f"  {a} XOR {b} = {result}")
    
    print("\n2. HALF ADDER")
    print("-" * 70)
    print("Truth table:")
    for a in [0, 1]:
        for b in [0, 1]:
            sum_bit, carry = Adders.half_adder(a, b)
            print(f"  {a} + {b} = sum:{sum_bit}, carry:{carry}")
    
    print("\n3. FULL ADDER")
    print("-" * 70)
    a, b, cin = 1, 1, 1
    sum_bit, cout = Adders.full_adder(a, b, cin)
    print(f"  {a} + {b} + {cin}(carry) = sum:{sum_bit}, carry:{cout}")
    
    print("\n4. RIPPLE CARRY ADDER (8-bit)")
    print("-" * 70)
    # Add 15 + 27 = 42
    a = [1, 1, 1, 1, 0, 0, 0, 0]  # 15 in binary (LSB first)
    b = [1, 1, 0, 1, 1, 0, 0, 0]  # 27 in binary
    sum_bits, carry = Adders.ripple_carry_adder(a, b)
    
    # Convert back to decimal
    a_dec = sum(bit << i for i, bit in enumerate(a))
    b_dec = sum(bit << i for i, bit in enumerate(b))
    sum_dec = sum(bit << i for i, bit in enumerate(sum_bits))
    
    print(f"  {a_dec} + {b_dec} = {sum_dec}, carry:{carry}")
    
    print("\n5. ALU OPERATIONS")
    print("-" * 70)
    alu = ALU(8)
    
    result = alu.add(25, 17)
    print(f"  25 + 17 = {result}, Flags: Z={alu.zero_flag}, C={alu.carry_flag}")
    
    result = alu.subtract(50, 20)
    print(f"  50 - 20 = {result}, Flags: Z={alu.zero_flag}, C={alu.carry_flag}")
    
    result = alu.AND(0b11110000, 0b10101010)
    print(f"  0b11110000 AND 0b10101010 = 0b{result:08b}")
    
    result = alu.shift_left(0b00001111, 2)
    print(f"  0b00001111 << 2 = 0b{result:08b}")
    
    print("\n6. REGISTERS & MEMORY")
    print("-" * 70)
    reg = Register(8)
    reg.load(42)
    print(f"  Register value: {reg.read()}")
    
    ram = RAM(16, 8)
    ram.write(5, 123)
    print(f"  RAM[5] = {ram.read(5)}")
    
    print("\n7. SIMPLE CPU")
    print("-" * 70)
    cpu = SimpleCPU()
    cpu.reg_a.load(10)
    cpu.reg_b.load(20)
    result = cpu.alu.add(cpu.reg_a.read(), cpu.reg_b.read())
    print(f"  CPU State: {cpu.get_state()}")
    print(f"  A + B = {result}")


if __name__ == '__main__':
    main()
