# Ben Eater 8-bit Computer GUI Guide

## Overview

The GUI replicates the physical Ben Eater 8-bit computer with authentic switches, LEDs, and controls from the video series.

## Features

### Visual Components

1. **BUS Display (8 LEDs)** - Shows current data on the bus
2. **Register A (8 LEDs)** - Shows Register A contents
3. **Register B (8 LEDs)** - Shows Register B contents
4. **Program Counter (4 LEDs)** - Shows current instruction address
5. **Flags (2 LEDs)** - Carry and Zero flags
6. **7-Segment Display** - Shows output value
7. **Memory Programming Switches** - Manual memory programming

### Controls

#### Main Control Buttons

- **STEP** - Execute one instruction (single clock cycle)
- **RUN** - Start automatic execution
- **STOP** - Stop automatic execution (appears when running)
- **RESET** - Reset computer to initial state
- **LOAD** - Load program from .bin file

#### Memory Programming

1. **Address Switches (4-bit)** - Set memory address (0-15)
2. **Data Switches (8-bit)** - Set data value (0-255)
3. **PROGRAM Button** - Write data to selected address

#### Clock Speed Control

- Slider to adjust execution speed (0.1 - 10 Hz)
- Default: 1 Hz (1 instruction per second)

## Usage Examples

### Example 1: Load and Run a Program

1. Click **LOAD** button
2. Select a .bin file (e.g., `fibonacci.bin`)
3. Click **RUN** to start execution
4. Watch the LEDs and 7-segment display update
5. Click **STOP** to pause
6. Click **RESET** to restart

### Example 2: Manual Memory Programming

Program a simple addition (28 + 14 = 42):

**Address 0: LDA 14** (Load from address 14)
1. Set address switches: 0000 (address 0)
2. Set data switches: 0001 1110 (0x1E = LDA 14)
3. Click **PROGRAM**

**Address 1: ADD 15** (Add from address 15)
1. Set address switches: 0001 (address 1)
2. Set data switches: 0010 1111 (0x2F = ADD 15)
3. Click **PROGRAM**

**Address 2: OUT** (Output result)
1. Set address switches: 0010 (address 2)
2. Set data switches: 1110 0000 (0xE0 = OUT)
3. Click **PROGRAM**

**Address 3: HLT** (Halt)
1. Set address switches: 0011 (address 3)
2. Set data switches: 1111 0000 (0xF0 = HLT)
3. Click **PROGRAM**

**Address 14: Data 28**
1. Set address switches: 1110 (address 14)
2. Set data switches: 0001 1100 (28)
3. Click **PROGRAM**

**Address 15: Data 14**
1. Set address switches: 1111 (address 15)
2. Set data switches: 0000 1110 (14)
3. Click **PROGRAM**

Now click **RESET** then **STEP** through each instruction, or **RUN** to execute automatically.

### Example 3: Step-by-Step Debugging

1. Load a program
2. Click **STEP** to execute one instruction
3. Observe:
   - Program Counter increments
   - Bus shows current instruction
   - Registers update
   - Flags change
   - Output displays result
4. Continue stepping to trace program execution

## LED Color Coding

- **Green** - Bus data lines
- **Red** - Register A and B
- **Yellow** - Program Counter
- **Magenta** - Carry Flag
- **Cyan** - Zero Flag

## Understanding the Display

### Bus LEDs (B7-B0)
Shows the current value on the data bus. During instruction fetch, this shows the instruction being executed.

### Register LEDs
- **Bit 7** (leftmost) = Most Significant Bit (MSB)
- **Bit 0** (rightmost) = Least Significant Bit (LSB)

### Program Counter
- 4-bit counter (0-15)
- Shows which memory address will be executed next

### Flags
- **Carry Flag** - Lights when:
  - Addition produces carry (result > 255)
  - Subtraction has no borrow (result ≥ 0)
- **Zero Flag** - Lights when arithmetic result equals zero

### 7-Segment Display
Shows the decimal value of Register A (0-255). Only displays last digit for values > 9.

## Keyboard Shortcuts

(Can be added in future versions)
- Space: STEP
- R: RUN/STOP
- Esc: RESET

## Tips

1. **Slow Down Execution** - Set clock speed to 0.1 Hz to watch each step
2. **Speed Up** - Set to 10 Hz for faster execution
3. **Watch the Bus** - The bus LEDs show data movement
4. **Monitor Flags** - Flags help understand program flow
5. **Use STEP Mode** - Best for learning and debugging

## Troubleshooting

**Program doesn't run:**
- Check if program is loaded
- Press RESET before running
- Verify memory is programmed correctly

**Display shows wrong value:**
- 7-segment only shows last digit
- Check full value in output label below display

**LEDs don't update:**
- Click STEP or RUN to execute instructions
- RESET clears all LEDs

## Technical Details

### Memory Layout
- 16 bytes of RAM (addresses 0-15)
- Typically:
  - 0-11: Program code
  - 12-15: Data storage

### Instruction Format
```
[7:4] Opcode (4 bits)
[3:0] Operand (4 bits)
```

### Switch Values
- **1** (green) = High/True
- **0** (gray) = Low/False

## Creating Programs

### Method 1: Use Assembler
```bash
python assembler.py myprogram.asm
python computer_gui.py
# Click LOAD and select myprogram.bin
```

### Method 2: Manual Programming
Use the address and data switches to program memory directly through the GUI.

## Example Programs to Try

All included .bin files can be loaded:
- `add_two_numbers.bin` - Simple addition
- `fibonacci.bin` - Fibonacci sequence
- `multiply.bin` - Multiplication
- `countdown.bin` - Countdown timer
- `sum_sequence.bin` - Sum of sequence

## Advanced Features

### Clock Speed Adjustment
- Adjust during execution
- Useful for demonstrations
- Range: 0.1 Hz (slow) to 10 Hz (fast)

### Real-time Monitoring
- All registers update in real-time
- Bus activity visible
- Flag changes immediate

## Comparison to Physical Computer

This GUI replicates:
✓ LED indicators for all registers
✓ Memory programming switches
✓ Clock control (manual step and auto-run)
✓ 7-segment output display
✓ Flag indicators
✓ Program counter display

Not included (physical computer has):
- Individual module separation
- Clock module with manual/auto modes
- Instruction register display
- Memory address register display
- Control signals visualization

## Future Enhancements

Possible additions:
- Control signal LEDs (MI, RI, RO, etc.)
- Instruction register display
- Memory address register display
- Clock module visualization
- Waveform display
- Instruction decode visualization
- Memory viewer panel
- Breakpoint support

## Running the GUI

```bash
python computer_gui.py
```

Requires:
- Python 3.x
- tkinter (usually included with Python)

## See Also

- `INSTRUCTION_REFERENCE.md` - Complete instruction set
- `COMPLETE_GUIDE.md` - Full project documentation
- `README.md` - Project overview
