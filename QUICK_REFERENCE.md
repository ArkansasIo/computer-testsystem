# Quick Reference Card - Complete 8-bit Computer GUI

## Launch Command
```bash
python computer_gui_complete.py
```

## Control Buttons

| Button | Color | Function |
|--------|-------|----------|
| STEP | Blue | Execute one instruction |
| RUN | Green | Start continuous execution |
| STOP | Red | Pause execution (RUN changes to STOP) |
| RESET | Red | Clear all registers, reset PC |
| LOAD | Yellow | Load program from .bin file |
| SOUND | Green/Gray | Toggle sound effects on/off |

## LED Colors

| Color | Component |
|-------|-----------|
| Green | Bus (8-bit data highway) |
| Red | Registers A and B |
| Yellow | Program Counter, Control Signals |
| Cyan | Instruction Register |
| Magenta | Memory Address Register, Carry Flag |
| Cyan | Zero Flag |

## Control Signals (Yellow LEDs)

| Signal | Meaning |
|--------|---------|
| MI | Memory address In |
| RI | RAM In (write) |
| RO | RAM Out (read) |
| II | Instruction In |
| IO | Instruction Out |
| AI | A register In |
| AO | A register Out |
| EO | ALU (adder) Out |
| SU | Subtract mode |
| BI | B register In |
| OI | Output In |
| CE | Counter Enable (PC++) |
| CO | Counter Out |
| J | Jump |
| FI | Flags In |

## Instruction Set

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x0 | NOP | No operation |
| 0x1 | LDA addr | Load A from memory |
| 0x2 | ADD addr | Add memory to A |
| 0x3 | SUB addr | Subtract memory from A |
| 0x4 | STA addr | Store A to memory |
| 0x5 | LDI val | Load immediate value |
| 0x6 | JMP addr | Jump to address |
| 0x7 | JC addr | Jump if carry |
| 0x8 | JZ addr | Jump if zero |
| 0xE | OUT | Output A to display |
| 0xF | HLT | Halt execution |

## Memory Programming

1. Set address switches (A3-A0)
2. Set data switches (D7-D0)
3. Click "PROGRAM MEMORY"

Example: Store 42 at address 5
- A3=0, A2=1, A1=0, A0=1 (binary 0101)
- D7-D0 = 00101010 (binary 42)

## Display Formats

All values shown in:
- **BIN** - Binary (8 bits)
- **HEX** - Hexadecimal (0x00-0xFF)
- **DEC** - Decimal (0-255)
- **OCT** - Octal (0o000-0o377)

## Clock Speed

Slider range: 0.1 Hz to 10 Hz
- 0.1 Hz = 1 instruction per 10 seconds (slow, educational)
- 1 Hz = 1 instruction per second (default)
- 10 Hz = 10 instructions per second (fast)

## Sound Effects

| Sound | Trigger |
|-------|---------|
| Pong | Step execution |
| Read | Memory read |
| Write | Memory write |
| Click | Button press, reset |

## Example Programs

### Add Two Numbers (28 + 14 = 42)
```
0: LDI 28    (0x51C)
1: STA 14    (0x4E)
2: LDI 14    (0x50E)
3: STA 15    (0x4F)
4: LDA 14    (0x1E)
5: ADD 15    (0x2F)
6: OUT       (0xE0)
7: HLT       (0xF0)
```

### Countdown from 10
```
0: LDI 10    (0x50A)
1: OUT       (0xE0)
2: SUB 15    (0x3F)
3: JZ 7      (0x87)
4: JMP 1     (0x61)
7: HLT       (0xF0)
15: 1        (0x01)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No sound | Install pyaudio or disable sound |
| Can't see all components | Scroll down or resize window |
| Program won't load | Use .bin files from assembler.py |
| GUI won't start | Install tkinter: `pip install tk` |

## Learning Tips

1. **Start slow** - Set clock to 0.1 Hz
2. **Watch control signals** - See CPU internals
3. **Use STEP** - Understand each instruction
4. **Check memory viewer** - Verify program behavior
5. **Monitor flags** - Understand carry and zero

## File Locations

- Programs: `*.asm` (source), `*.bin` (compiled)
- Assembler: `assembler.py`
- Simulator: `simulator.py`
- Documentation: `COMPLETE_GUI_GUIDE.md`

## Quick Start

1. Launch GUI: `python computer_gui_complete.py`
2. Click LOAD, select `fibonacci.bin`
3. Set clock speed to 1 Hz
4. Click RUN
5. Watch the magic happen!

## Advanced Usage

- **Debug programs**: Use STEP and watch control signals
- **Learn architecture**: Study signal patterns for each instruction
- **Create programs**: Use switches to program memory manually
- **Experiment**: Try different clock speeds and observe behavior

## Resources

- Full guide: `COMPLETE_GUI_GUIDE.md`
- Instruction reference: `INSTRUCTION_REFERENCE.md`
- Ben Eater videos: https://eater.net/8bit

---

**Pro Tip**: Set clock speed to 0.1 Hz and watch control signals during execution to understand how the CPU works internally!
