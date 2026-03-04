# Complete 8-bit Computer GUI - User Guide

## Overview

The Complete GUI (`computer_gui_complete.py`) is the most comprehensive interface for the 8-bit computer, featuring:

- **Individual LED components** for every bit of every register
- **LCD-style displays** with multi-format output (Binary, Hex, Decimal, Octal)
- **Interactive toggle switches** for memory programming
- **Control signal LEDs** showing internal CPU operations
- **Instruction decode display** showing current operation
- **Memory viewer** with live updates
- **Sound effects** for all operations
- **Step-by-step execution** with visual feedback

## Running the GUI

```bash
python computer_gui_complete.py
```

## GUI Components

### 1. Control Signals (Top Row)

15 yellow LEDs showing active control signals:

| Signal | Description |
|--------|-------------|
| MI | Memory address In (MAR ← Bus) |
| RI | RAM In (Memory[MAR] ← Bus) |
| RO | RAM Out (Bus ← Memory[MAR]) |
| II | Instruction In (IR ← Bus) |
| IO | Instruction Out (Bus ← IR operand) |
| AI | A register In (A ← Bus) |
| AO | A register Out (Bus ← A) |
| EO | ALU Out (Bus ← ALU result) |
| SU | Subtract mode (ALU does A - B) |
| BI | B register In (B ← Bus) |
| OI | Output In (Output ← Bus) |
| CE | Counter Enable (PC++) |
| CO | Counter Out (Bus ← PC) |
| J  | Jump (PC ← Bus) |
| FI | Flags In (Update flags) |

These LEDs light up during instruction execution to show exactly what the CPU is doing internally.

### 2. 8-bit Bus Display

- **8 green LEDs** (B7-B0) showing current bus value
- **LCD display** showing bus value in Binary, Hex, and Decimal

The bus is the main data highway connecting all components.

### 3. Register A (Red LEDs)

- **8 red LEDs** showing each bit
- **LCD display** with:
  - Binary representation
  - Hexadecimal value
  - Decimal value

### 4. Register B (Red LEDs)

- **8 red LEDs** showing each bit
- **LCD display** with multi-format output
- Used as second operand for ALU operations

### 5. Program Counter (Yellow LEDs)

- **4 yellow LEDs** (PC3-PC0)
- **LCD display** showing current instruction address
- Automatically increments after each instruction

### 6. Instruction Register (Cyan LEDs)

- **8 cyan LEDs** showing instruction bits
- **LCD display** showing:
  - Decoded instruction (e.g., "LDA 5")
  - Binary and Hex values
  - Opcode and operand breakdown

### 7. Memory Address Register (Magenta LEDs)

- **4 magenta LEDs** (MAR3-MAR0)
- **LCD display** showing current memory address being accessed
- Points to memory location for read/write operations

### 8. Flags

Two large LEDs showing CPU status:

- **CARRY** (Magenta) - Set when arithmetic overflow occurs
- **ZERO** (Cyan) - Set when result is zero

### 9. Output Display

- **7-segment LED display** showing last digit of output
- **LCD panel** with all formats:
  - Binary (8 bits)
  - Hexadecimal (0x__)
  - Decimal (0-255)
  - Octal (0o___)

### 10. Memory Programming Switches

Interactive switches for manual memory programming:

**Address Switches (4-bit):**
- A3, A2, A1, A0
- Set address (0-15)

**Data Switches (8-bit):**
- D7, D6, D5, D4, D3, D2, D1, D0
- Set data value (0-255)

**PROGRAM MEMORY Button:**
- Click to write data to selected address
- Plays write sound effect
- Updates memory viewer

### 11. Memory Viewer

Live display of all 16 memory locations showing:
- Address (0-15)
- Hexadecimal value
- Binary representation
- Decimal value

Updates in real-time as memory changes.

### 12. Control Buttons

**STEP** (Blue)
- Execute one instruction
- Shows control signals
- Plays step sound

**RUN** (Green)
- Continuous execution
- Changes to STOP when running
- Speed controlled by slider

**RESET** (Red)
- Clear all registers
- Reset PC to 0
- Clear flags

**LOAD** (Yellow)
- Load program from .bin file
- Resets computer after loading

**SOUND** (Green/Gray)
- Toggle sound effects on/off
- Shows 🔊 when on, 🔇 when off

### 13. Clock Speed Control

Slider to adjust execution speed:
- Range: 0.1 Hz to 10 Hz
- Default: 1 Hz (1 instruction per second)
- Higher values = faster execution

### 14. Status Bar

Bottom bar showing current operation status:
- "Ready" - Waiting for input
- "Executed: PC=X" - After step
- "Running..." - During auto-run
- "HALTED" - Program finished
- Error messages

## Using the GUI

### Programming Memory Manually

1. Set address using A3-A0 switches (click to toggle)
2. Set data using D7-D0 switches
3. Click "PROGRAM MEMORY"
4. Verify in memory viewer

Example: Store value 42 at address 5
- A3=0, A2=1, A1=0, A0=1 (binary 0101 = 5)
- D7-D0 = 00101010 (binary = 42)
- Click PROGRAM MEMORY

### Loading a Program

1. Click "LOAD" button
2. Select .bin file (e.g., fibonacci.bin)
3. Computer resets automatically
4. Memory viewer shows loaded program

### Running a Program

**Step-by-step:**
1. Click "STEP" to execute one instruction
2. Watch control signals light up
3. See registers update
4. Observe bus activity

**Continuous:**
1. Adjust clock speed slider
2. Click "RUN"
3. Watch program execute
4. Click "STOP" to pause

### Understanding Control Signals

Watch the yellow control signal LEDs during execution:

**Fetch Cycle (every instruction):**
1. CO + MI: PC → MAR
2. RO + II + CE: Memory → IR, PC++

**LDA 5 (Load from address 5):**
1. IO + MI: 5 → MAR
2. RO + AI: Memory[5] → A

**ADD 6 (Add from address 6):**
1. IO + MI: 6 → MAR
2. RO + BI: Memory[6] → B
3. EO + AI + FI: A+B → A, update flags

**STA 7 (Store to address 7):**
1. IO + MI: 7 → MAR
2. AO + RI: A → Memory[7]

## Sound Effects

The GUI plays authentic retro computer sounds:

- **Pong** - Step execution start
- **Read** - Memory read operation
- **Write** - Memory write operation
- **Click** - Button presses, reset

Toggle sounds with the SOUND button.

## Keyboard Shortcuts

(Future enhancement - not yet implemented)

## Example Programs

### Simple Addition (28 + 14 = 42)

```
Address | Instruction | Description
--------|-------------|-------------
0       | LDI 28      | Load 28 into A
1       | STA 14      | Store at address 14
2       | LDI 14      | Load 14 into A
3       | STA 15      | Store at address 15
4       | LDA 14      | Load first number
5       | ADD 15      | Add second number
6       | OUT         | Display result
7       | HLT         | Stop
```

### Countdown from 10

```
Address | Instruction | Description
--------|-------------|-------------
0       | LDI 10      | Start at 10
1       | OUT         | Display
2       | SUB 15      | Subtract 1
3       | JZ 7        | If zero, halt
4       | JMP 1       | Loop back
7       | HLT         | Stop
15      | 1           | Constant 1
```

## Troubleshooting

**GUI doesn't start:**
- Check Python version (3.6+)
- Install tkinter: `pip install tk`

**No sound:**
- Install pyaudio: `pip install pyaudio`
- Or disable sound with SOUND button

**Program doesn't load:**
- Verify .bin file format
- Check file size (max 16 bytes for 8-bit)
- Use assembler.py to create valid .bin files

**Display issues:**
- Resize window if components overlap
- Scroll down to see all components
- Check screen resolution (1920x1080+ recommended)

## Advanced Features

### Control Signal Analysis

Study how instructions work by watching control signals:

1. Load a simple program
2. Set clock speed to 0.1 Hz (slow)
3. Click RUN
4. Watch control signals light up in sequence
5. Correlate with instruction decode display

### Memory Inspection

Monitor memory changes:

1. Program some values manually
2. Run a program that modifies memory
3. Watch memory viewer update in real-time
4. Verify program behavior

### Flag Behavior

Understand CPU flags:

1. Load program with ADD/SUB instructions
2. Step through execution
3. Watch CARRY flag (arithmetic overflow)
4. Watch ZERO flag (result = 0)
5. See how JC/JZ use these flags

## Comparison with Other GUIs

| Feature | computer_gui.py | computer_gui_enhanced.py | computer_gui_complete.py |
|---------|----------------|-------------------------|-------------------------|
| LED indicators | ✓ | ✓ | ✓✓✓ (All components) |
| Multi-format displays | - | ✓ | ✓✓ (LCD panels) |
| Sound effects | - | ✓ | ✓ |
| Control signals | - | - | ✓ |
| Memory viewer | - | - | ✓ |
| Instruction decode | - | - | ✓ |
| Programming switches | ✓ | - | ✓ |
| 7-segment display | ✓ | - | ✓ |

**Use computer_gui_complete.py for:**
- Learning how CPUs work internally
- Understanding instruction execution
- Debugging programs
- Educational demonstrations

**Use computer_gui_enhanced.py for:**
- Quick program testing
- Multi-format value display
- Sound feedback

**Use computer_gui.py for:**
- Authentic Ben Eater experience
- Manual memory programming
- Basic operation

## Educational Value

This GUI is perfect for:

1. **Computer Science Students** - See CPU internals
2. **Educators** - Demonstrate computer architecture
3. **Hobbyists** - Learn digital logic
4. **Programmers** - Understand low-level operations

## References

- [Ben Eater's 8-bit Computer](https://eater.net/8bit)
- [SAP-1 Architecture](https://en.wikipedia.org/wiki/Simple-As-Possible_computer)
- Project README.md for instruction set

## Next Steps

1. Load fibonacci.bin and watch it execute
2. Write your own program with the switches
3. Study control signals during different instructions
4. Experiment with clock speeds
5. Create custom programs with assembler.py

Enjoy exploring computer architecture!
