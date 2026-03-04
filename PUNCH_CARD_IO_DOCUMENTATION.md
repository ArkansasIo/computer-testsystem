# PUNCH CARD & I/O SYSTEM - COMPLETE DOCUMENTATION

## Overview

The Punch Card & I/O System is a comprehensive implementation of vintage computer input/output mechanisms, integrated logic gate simulation, keyboard-to-switch mapping, and advanced function processing capabilities.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  INTEGRATED I/O CONTROL SYSTEM                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  INPUT       │  │  PROCESSING  │  │  OUTPUT      │           │
│  │  SYSTEMS     │  │  LOGIC       │  │  SYSTEMS     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│       │                    │                 │                   │
│  • Keyboard         • Logic Gates     • Display              │
│  • Punch Cards      • Functions       • Punch Cards          │
│  • Switches         • Chains          • LED                  │
│  • Serial Port      • Circuits        • Printer              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. PUNCH CARD SYSTEM

### 1.1 Historical Background

Punch cards are rectangular pieces of stiff paper used to contain digital information. The most common format was the IBM card:
- **Dimensions**: 80 columns × 12 rows
- **Punch Positions**: 1,920 total
- **Standard Data**: EBCDIC or ASCII encoded data

### 1.2 Punch Card Class

```python
class PunchCard:
    ROWS = 12       # Card rows (0-11)
    COLUMNS = 80    # Card columns (0-79)
```

#### Card Layout:
```
Column:  0         1         2         3
         0123456789012345678901234567890123456789
Row  0:  ·●·······●·······●·······●·······●····
Row  1:  ●········●·······●·······●·······●····
Row  2:  ·········●················●·······●····
Row  3:  ·········●········································
Row  4:  ·········●········································
Row  5:  ·········●········································
Row  6:  ·········●········································
Row  7:  ·········●········································
Row  8:  ·········●········································
Row  9:  ·········●········································
Row 10:  ·········●········································
Row 11:  ·········●········································

Legend: ● = Punched hole, · = Empty space
```

### 1.3 Operations

#### Creating a Card
```python
card = PunchCard("CARD001")
card.punch(row=2, column=5)      # Punch single hole
card.write_column(column=0, value=0xFF)  # Write byte to column
```

#### Reading Data
```python
byte_value = card.read_column(column=10)    # Read single column as byte
row_value = card.read_row(row=5)            # Read row as value
all_data = card.to_bytes()                  # Get entire card as bytes
```

#### Persistence
```python
card.save("card.json")                      # Save to file
card.load("card.json")                      # Load from file
print(card.visual_representation())         # Display ASCII art
```

### 1.4 Card JSON Format

```json
{
  "card_id": "CARD001",
  "rows": 12,
  "columns": 80,
  "data": [255, 170, 85, 0, 127, ...],
  "metadata": {
    "date_created": "2026-03-04",
    "purpose": "test_program"
  }
}
```

### 1.5 Punch Card Reader

```python
reader = PunchCardReader()
reader.load_card(card)
byte1 = reader.read_byte()      # Read next byte
all_data = reader.read_all()    # Read entire card
```

### 1.6 Punch Card Writer

```python
writer = PunchCardWriter()
card = writer.create_card("OUTPUT001")
writer.write_byte(0xFF)
writer.write_data(b'\x00\x01\x02\x03')
```

---

## 2. LOGIC GATE SYSTEM

### 2.1 Supported Logic Gates

#### 2.1.1 Basic Gates

**AND Gate**
- Output: 1 only if ALL inputs are 1
- Truth Table (2-input):
  ```
  A | B | Q
  -----------
  0 | 0 | 0
  0 | 1 | 0
  1 | 0 | 0
  1 | 1 | 1
  ```

**OR Gate**
- Output: 1 if ANY input is 1
- Truth Table (2-input):
  ```
  A | B | Q
  -----------
  0 | 0 | 0
  0 | 1 | 1
  1 | 0 | 1
  1 | 1 | 1
  ```

**NOT Gate**
- Output: Opposite of input
- Truth Table:
  ```
  A | Q
  ------
  0 | 1
  1 | 0
  ```

#### 2.1.2 Complex Gates

**XOR (Exclusive-OR)**
- Output: 1 if inputs differ
- Truth Table (2-input):
  ```
  A | B | Q
  -----------
  0 | 0 | 0
  0 | 1 | 1
  1 | 0 | 1
  1 | 1 | 0
  ```

**NAND (Not-AND)**
- Output: 0 only if ALL inputs are 1
- Truth Table (2-input):
  ```
  A | B | Q
  -----------
  0 | 0 | 1
  0 | 1 | 1
  1 | 0 | 1
  1 | 1 | 0
  ```

**NOR (Not-OR)**
- Output: 0 if ANY input is 1
- Truth Table (2-input):
  ```
  A | B | Q
  -----------
  0 | 0 | 1
  0 | 1 | 0
  1 | 0 | 0
  1 | 1 | 0
  ```

**XNOR (Exclusive-NOR)**
- Output: 1 if inputs match
- Truth Table (2-input):
  ```
  A | B | Q
  -----------
  0 | 0 | 1
  0 | 1 | 0
  1 | 0 | 0
  1 | 1 | 1
  ```

### 2.2 Logic Gate Class

```python
class LogicGate:
    def __init__(self, gate_type: LogicGateType, name: str = None)
    def set_inputs(self, *inputs)           # Set input values
    def compute()                           # Calculate output
    def truth_table()                       # Generate truth table
```

#### Usage

```python
# Create AND gate
and_gate = LogicGate(LogicGateType.AND, "AND_1")

# Set inputs and compute
output = and_gate.set_inputs(1, 1)  # Returns: 1
output = and_gate.set_inputs(1, 0)  # Returns: 0

# Generate truth table
table = and_gate.truth_table()
for inputs, output in table:
    print(f"{inputs} -> {output}")
```

### 2.3 Logic Circuit (Advanced)

```python
class LogicCircuit:
    def add_gate(name, gate_type)       # Add gate to circuit
    def connect(source, target)         # Wire gates together
    def set_input(name, value)          # Set circuit input
    def evaluate()                      # Evaluate circuit
```

#### Building a Circuit

```python
circuit = LogicCircuit("Half Adder")

# Add gates
circuit.add_gate("A1", LogicGateType.XOR)   # Sum bit
circuit.add_gate("A2", LogicGateType.AND)   # Carry bit

# Connect gates
circuit.connect("input", "A1")
circuit.connect("input", "A2")

# Evaluate
circuit.set_input("input_0", 1)
circuit.set_input("input_1", 1)
results = circuit.evaluate()
```

---

## 3. KEYBOARD INPUT SYSTEM

### 3.1 Default Key Mapping

```
┌─────────────────────────────────────────┐
│  Keyboard Layout → Bit Assignment       │
├─────────────────────────────────────────┤
│  Q W E R          Bits 0-3              │
│  A S D F          Bits 4-7              │
│  Z X C V          Bits 8-11             │
│  1 2 3 4          Bits 12-15            │
└─────────────────────────────────────────┘
```

### 3.2 Keyboard Mapping Class

```python
class KeyboardMapping:
    DEFAULT_MAPPING = {
        'q': 0,  'w': 1,  'e': 2,  'r': 3,
        'a': 4,  's': 5,  'd': 6,  'f': 7,
        'z': 8,  'x': 9,  'c': 10, 'v': 11,
        '1': 12, '2': 13, '3': 14, '4': 15
    }
```

#### Operations

```python
mapping = KeyboardMapping()

# Custom mapping
custom = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
mapping.set_mapping(custom)

# Handlers
mapping.on_key_press('q')    # Press key Q
mapping.on_key_release('q')  # Release key Q
value = mapping.get_value()  # Get 16-bit value

# Event listener
def on_input_changed(value):
    print(f"Input: 0x{value:04X}")

mapping.add_listener(on_input_changed)
```

### 3.3 Key Combinations

Press multiple keys simultaneously:
- Press Q + A = Bits 0 and 4 set = 0x11
- Press R + F + 1 = Bits 3, 7, 12 set = 0x10A8
- All 16 keys together = 0xFFFF

### 3.4 Keyboard Input System

```python
class KeyboardInputSystem:
    def __init__(self, switch_count: int = 16)
    def bind_key(root: tk.Widget)       # Bind to Tkinter window
    def get_value() -> int              # Get current input
    def get_switch(index: int) -> int   # Get single switch state
```

#### Integration with GUI

```python
keyboard = KeyboardInputSystem(16)
keyboard.bind_key(root)      # Bind to main window

# In your update loop:
input_value = keyboard.get_value()
bit_3_state = keyboard.get_switch(3)
```

---

## 4. I/O FUNCTION SYSTEM

### 4.1 Function Types

#### 4.1.1 BitShift Function

Shifts bits left or right

```python
shift_func = BitShiftFunction("Shift1", shift_direction="left", shift_amount=2)
result = shift_func.execute(0b10101010)  # Input
# Output: 0b10101000 (left shift by 2)
```

**Examples:**
```
Left Shift by 1:
  Input:  10101010
  Output: 01010100 (MSB lost, LSB becomes 0)

Right Shift by 1:
  Input:  10101010
  Output: 01010101 (LSB lost, MSB becomes 0)
```

#### 4.1.2 Bitwise Function

Applies logical operations

```python
bitwise_func = BitwiseFunction("AND1", operation="and", operand=0x0F)
result = bitwise_func.execute(0xFF)  # Returns: 0x0F
```

**Operations:**
- `"and"` - Bitwise AND with operand
- `"or"` - Bitwise OR with operand
- `"xor"` - Bitwise XOR with operand
- `"not"` - Bitwise NOT (negation)

**Examples:**
```
AND with 0x0F:
  Input:  11111111
  Mask:   00001111
  Output: 00001111

OR with 0xF0:
  Input:  00110011
  Mask:   11110000
  Output: 11110011
```

#### 4.1.3 Rotate Function

Rotates bits with wrap-around

```python
rotate_func = RotateFunction("Rotate1", rotate_direction="left", amount=3)
result = rotate_func.execute(0b10001010)  # Returns: 0b01010100
```

**Examples:**
```
Rotate Left by 2:
  Input:  10100011
  Output: 10001110 (bits rotate with wrap)

Rotate Right by 1:
  Input:  10100011
  Output: 11010001 (bits rotate with wrap)
```

### 4.2 Function Class Hierarchy

```
IOFunction (Base Class)
├── LogicFunction (applies logic gates)
├── BitShiftFunction (shifts bits)
├── BitwiseFunction (bitwise operations)
├── RotateFunction (bit rotation)
└── CustomFunction (user-defined)
```

### 4.3 Function Chain

Chain multiple functions together

```python
chain = FunctionChain("ComplexOperation")
chain.add_function(BitShiftFunction("Shift", "left", 2))
chain.add_function(BitwiseFunction("AND", "and", 0x0F))
chain.add_function(RotateFunction("Rotate", "right", 1))

# Execute chain
result = chain.execute(0xFF)
# 0xFF -> 0xFC (shift left 2)
# 0xFC -> 0x0C (AND with 0x0F)
# 0x0C -> 0x06 (rotate right 1)
```

### 4.4 Integrated I/O System

```python
class IntegratedIOSystem:
    def register_input(name, system)     # Register input source
    def register_output(name, system)    # Register output target
    def register_function(name, func)    # Register function
    def register_gate(name, gate)        # Register logic gate
    def add_punch_card(name, card)       # Add punch card
```

---

## 5. ADVANCED FEATURES

### 5.1 Complex Logic Circuits

**Example: Binary Half Adder**

```python
# A half adder adds two bits and produces sum and carry

circuit = LogicCircuit("HalfAdder")
circuit.add_gate("XOR", LogicGateType.XOR)   # Sum = A XOR B
circuit.add_gate("AND", LogicGateType.AND)   # Carry = A AND B
circuit.connect("A", "XOR")
circuit.connect("B", "XOR")
circuit.connect("A", "AND")
circuit.connect("B", "AND")
```

### 5.2 Custom Function Chains

**Example: Data Encryption Simulation**

```python
encrypt_chain = FunctionChain("Encryption")
encrypt_chain.add_function(BitwiseFunction("XOR", "xor", 0xAA))
encrypt_chain.add_function(BitShiftFunction("Shift", "left", 3))
encrypt_chain.add_function(RotateFunction("Rotate", "right", 2))
encrypt_chain.add_function(BitwiseFunction("AND", "and", 0xFF))

encrypted = encrypt_chain.execute(plaintext)
```

### 5.3 Punch Card Programs

**Example: Fibonacci Number Generation**

```python
# Create card for Fibonacci program
card = PunchCard("FIBONACCI")

# Load program data (pseudo-machine code)
program = bytes([
    0xA0, 0x01,  # Load 1 to register A
    0xB0, 0x01,  # Load 1 to register B
    0xC0, 0x00,  # Load 0 to register C
    0x10, 0x02,  # Add A + B
    # ... more instructions
])

card.from_bytes(program)
card.save("fibonacci.json")
```

---

## 6. DATA FORMAT CONVERSIONS

All systems support automatic conversion between number formats:

### 6.1 8-bit Value Example: 170

| Format      | Representation | Notes                    |
|-------------|----------------|------------------------|
| Binary      | 10101010       | 8 bits                 |
| Hexadecimal | 0xAA           | Base-16                |
| Decimal     | 170            | Base-10                |
| Octal       | 0o252          | Base-8                 |

### 6.2 Format Conversion Functions

```python
value = 170

# To Binary
binary = bin(value)[2:].zfill(8)      # "10101010"

# To Hex
hexval = f"0x{value:02X}"              # "0xAA"

# To Decimal (already)
decimal = str(value)                   # "170"

# To Octal
octal = f"0o{oct(value)[2:].upper()}"  # "0o252"
```

---

## 7. SYSTEM INTERACTION EXAMPLES

### 7.1 Complete Workflow

```
1. INPUT
   └─ Keyboard (Q pressed) → Bit 0 set to 1

2. CONVERSION
   └─ Single bit → 8-bit value: 0x01

3. PROCESSING
   └─ Apply BitShift(left, 2) → 0x04
   └─ Apply Bitwise(AND, 0x0F) → 0x04
   └─ Apply Rotate(right, 1) → 0x02

4. OUTPUT
   └─ Display: BIN: 00000010
                HEX: 0x02
                DEC: 2
                OCT: 0o2
```

### 7.2 Punch Card Processing

```
1. LOAD
   └─ Read punch card file
   └─ Extract data (80 columns × 12 rows)
   └─ Convert to byte array

2. PROCESS
   └─ Pass through function chain
   └─ Apply logic gates
   └─ Generate results

3. STORE
   └─ Write results to new punch card
   └─ Save to file
   └─ Display visualization
```

---

## 8. GUI OPERATIONS

### 8.1 Punch Card Tab

```
┌──────────────────────────────┐
│ NEW CARD  LOAD  SAVE  VISUAL │
├──────────────────────────────┤
│                              │
│ Punch Card Visualization:    │
│ (ASCII art display)          │
│                              │
│ Column:  0         1         2│
│ Row  0:  ·●·······●·········│
│ Row  1:  ●········●·········│
│ ...                          │
│                              │
└──────────────────────────────┘
```

### 8.2 Logic Gates Tab

```
┌──────────────────────────────┐
│ AND ▼  CREATE GATE           │
├──────────────────────────────┤
│                              │
│ Truth Table for AND Gate:    │
│ A B Q                        │
│ 0 0 0                        │
│ 0 1 0                        │
│ 1 0 0                        │
│ 1 1 1                        │
│                              │
└──────────────────────────────┘
```

### 8.3 I/O Functions Tab

```
┌────────────────────────────────┐
│ BitShift ▼  CREATE  Test: 255 │
├────────────────────────────────┤
│                                │
│ Function Results:              │
│ Input:  0xFF (11111111)        │
│ Output: 0xFC (11111100)        │
│                                │
│ (After BitShift Left by 2)     │
│                                │
└────────────────────────────────┘
```

---

## 9. ERROR HANDLING

### 9.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Punch card not loading | Invalid JSON | Check file format |
| Keyboard input not working | No focus | Click GUI window |
| Logic gate output wrong | Incorrect inputs | Verify bit arrangement |
| Function chain error | Incompatible types | Check data formats |

### 9.2 Debugging

```python
# Enable debug output
gate = LogicGate(LogicGateType.AND, "DEBUG_AND")
print(f"Gate: {gate}")  # LogicGate(DEBUG_AND, inputs=[...], output=...)

# Verify punch card data
card.visualize()        # Print ASCII representation

# Test function
func = BitShiftFunction("TEST", "left", 1)
for i in range(256):
    output = func.execute(i)
    if output > 255:
        print(f"ERROR at {i}: {output}")
```

---

## 10. BEST PRACTICES

### 10.1 Punch Card Management

1. **Use descriptive card IDs**: `PROG001`, `DATA_LOAD`, `RESULT_003`
2. **Save frequently**: Use the Save button regularly
3. **Backup important cards**: Keep copies of critical punch cards
4. **Document metadata**: Add purpose and date to cards
5. **Organize by type**: Separate program and data cards

### 10.2 Logic Gate Design

1. **Start simple**: Test basic gates before complex circuits
2. **Document circuits**: Label inputs and outputs
3. **Verify truth tables**: Check gate behavior thoroughly
4. **Test edge cases**: Try all input combinations
5. **Build incrementally**: Add one gate at a time

### 10.3 Keyboard Input

1. **Familiarize yourself with mapping**: Learn key positions
2. **Use consistent conventions**: Stick to one mapping system
3. **Document custom mappings**: Save non-standard configurations
4. **Test multi-key presses**: Verify simultaneous key handling
5. **Handle edge cases**: Test rapid key transitions

### 10.4 Function Chains

1. **Plan before building**: Sketch the transformation sequence
2. **Test each stage**: Verify output after each function
3. **Use meaningful names**: Label chain for clarity
4. **Keep chains reasonably short**: Avoid excessive complexity
5. **Document transformations**: Record expected values

---

## 11. QUICK REFERENCE

### Commands

```
GUI Operations:
  • [NEW CARD] - Create punch card
  • [LOAD CARD] - Open existing card
  • [SAVE CARD] - Save card to file
  • [VISUALIZE] - Display punch pattern
  • [CREATE GATE] - Add logic gate
  • [CREATE FUNCTION] - Add I/O function
  • [TEST] - Execute function with input

Keyboard Shortcuts:
  Q-R, A-F, Z-V, 1-4 - Toggle switches (bits 0-15)
```

### System Limits

| Component | Limit |
|-----------|-------|
| Punch Card Columns | 80 |
| Punch Card Rows | 12 |
| Bit Width | 8 (byte) |
| Registers (A-Z) | 26 |
| Logic Gates | Unlimited |
| Function Chains | Unlimited |
| Breakpoints | Unlimited |

---

## 12. GLOSSARY

**Bit**: Single binary digit (0 or 1)
**Byte**: 8 bits grouped together
**Punch Card**: Physical medium with punched holes
**Logic Gate**: Fundamental circuit element
**Truth Table**: Complete mapping of inputs to outputs
**Function Chain**: Sequence of operations
**Register**: High-speed storage in CPU
**EBCDIC**: Extended Binary Coded Decimal
**IBM Card**: Standard 80-column punch card format

---

## 13. VERSION HISTORY

- **v1.0** (March 2026): Initial implementation
- **v2.0** (March 2026): Complete integration with multi-architecture system

---

**END OF DOCUMENTATION**

For support and updates, check the system status tab in the GUI.
