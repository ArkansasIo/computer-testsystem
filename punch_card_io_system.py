#!/usr/bin/env python3
"""
Punch Card and Keyboard Input Systems
Implements punch card reader/writer, keyboard switch mapping, logic gates, and I/O functions
Supports multiple input types and logic gate configurations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import json
import os
from enum import Enum
from typing import List, Dict, Tuple, Callable
from dataclasses import dataclass


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class LogicGateType(Enum):
    """Logic gate types"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    XOR = "XOR"
    NAND = "NAND"
    NOR = "NOR"
    XNOR = "XNOR"


class InputType(Enum):
    """Input system types"""
    PUNCH_CARD = "PUNCH_CARD"
    KEYBOARD = "KEYBOARD"
    SWITCH = "SWITCH"
    MOUSE = "MOUSE"
    SERIAL = "SERIAL"


class OutputType(Enum):
    """Output system types"""
    PUNCH_CARD = "PUNCH_CARD"
    LED = "LED"
    PRINTER = "PRINTER"
    DISPLAY = "DISPLAY"
    SERIAL = "SERIAL"


@dataclass
class LogicGateConfig:
    """Configuration for logic gates"""
    gate_type: LogicGateType
    input_count: int
    delay_ns: float = 1.0


@dataclass
class PunchCardBit:
    """Single punch position on a card"""
    row: int
    column: int
    punched: bool = False
    value: int = 0


# ============================================================================
# LOGIC GATES
# ============================================================================

class LogicGate:
    """Base class for logic gates"""
    
    def __init__(self, gate_type: LogicGateType, name: str = None):
        self.gate_type = gate_type
        self.name = name or gate_type.value
        self.inputs = []
        self.output = 0
        self.delay_ns = 1.0
    
    def set_inputs(self, *inputs):
        """Set input values"""
        self.inputs = list(inputs)
        self.compute()
        return self.output
    
    def compute(self):
        """Compute gate output based on inputs"""
        if self.gate_type == LogicGateType.AND:
            self.output = 1 if all(self.inputs) else 0
        elif self.gate_type == LogicGateType.OR:
            self.output = 1 if any(self.inputs) else 0
        elif self.gate_type == LogicGateType.NOT:
            self.output = 0 if self.inputs[0] else 1
        elif self.gate_type == LogicGateType.XOR:
            self.output = 1 if sum(self.inputs) % 2 == 1 else 0
        elif self.gate_type == LogicGateType.NAND:
            self.output = 0 if all(self.inputs) else 1
        elif self.gate_type == LogicGateType.NOR:
            self.output = 0 if any(self.inputs) else 1
        elif self.gate_type == LogicGateType.XNOR:
            self.output = 0 if sum(self.inputs) % 2 == 1 else 1
        
        return self.output
    
    def truth_table(self):
        """Generate truth table for gate"""
        input_count = len(self.inputs) or 2
        table = []
        
        for i in range(2 ** input_count):
            inputs = [(i >> j) & 1 for j in range(input_count)]
            output = self.set_inputs(*inputs)
            table.append((inputs, output))
        
        return table
    
    def __repr__(self):
        return f"LogicGate({self.name}, inputs={self.inputs}, output={self.output})"


class LogicCircuit:
    """Composite logic circuit with multiple gates"""
    
    def __init__(self, name: str = "Circuit"):
        self.name = name
        self.gates: Dict[str, LogicGate] = {}
        self.wiring: Dict[str, List[str]] = {}  # gate_name -> [target_gates]
        self.inputs = {}
        self.outputs = {}
    
    def add_gate(self, name: str, gate_type: LogicGateType):
        """Add gate to circuit"""
        self.gates[name] = LogicGate(gate_type, name)
        self.wiring[name] = []
        return self.gates[name]
    
    def connect(self, source: str, target: str):
        """Connect output of source gate to target gate input"""
        if source in self.gates and target in self.gates:
            self.wiring[source].append(target)
    
    def set_input(self, name: str, value: int):
        """Set circuit input"""
        self.inputs[name] = value
    
    def evaluate(self):
        """Evaluate circuit"""
        results = {}
        
        # Process gates in order
        for gate_name, gate in self.gates.items():
            inputs = []
            
            # Collect inputs from connected gates or circuit inputs
            for i in range(len(self.gates)):
                if f"input_{i}" in self.inputs:
                    inputs.append(self.inputs[f"input_{i}"])
            
            if inputs:
                gate.set_inputs(*inputs)
            
            results[gate_name] = gate.output
        
        self.outputs = results
        return results
    
    def get_output(self, gate_name: str = None):
        """Get circuit output"""
        if gate_name:
            return self.outputs.get(gate_name, 0)
        
        # Return last gate output if no gate specified
        if self.gates:
            last_gate = list(self.gates.values())[-1]
            return last_gate.output
        return 0


# ============================================================================
# PUNCH CARD SYSTEM
# ============================================================================

class PunchCard:
    """Represents a punch card"""
    
    # Standard IBM card dimensions
    ROWS = 12  # Including X, Y, and zones
    COLUMNS = 80
    
    def __init__(self, card_id: str = ""):
        self.card_id = card_id
        self.bits: List[List[PunchCardBit]] = []
        self.data = bytearray()
        self.metadata = {}
        
        # Initialize card grid
        for row in range(self.ROWS):
            row_data = []
            for col in range(self.COLUMNS):
                row_data.append(PunchCardBit(row, col))
            self.bits.append(row_data)
    
    def punch(self, row: int, column: int):
        """Punch a hole in the card"""
        if 0 <= row < self.ROWS and 0 <= column < self.COLUMNS:
            self.bits[row][column].punched = True
            self.bits[row][column].value = 1
    
    def unpunch(self, row: int, column: int):
        """Remove a punch from the card"""
        if 0 <= row < self.ROWS and 0 <= column < self.COLUMNS:
            self.bits[row][column].punched = False
            self.bits[row][column].value = 0
    
    def toggle_punch(self, row: int, column: int):
        """Toggle punch at position"""
        if 0 <= row < self.ROWS and 0 <= column < self.COLUMNS:
            bit = self.bits[row][column]
            bit.punched = not bit.punched
            bit.value = 1 if bit.punched else 0
    
    def read_column(self, column: int) -> int:
        """Read entire column as byte"""
        value = 0
        for row in range(min(8, self.ROWS)):
            if self.bits[row][column].punched:
                value |= (1 << row)
        return value
    
    def read_row(self, row: int) -> int:
        """Read entire row as integer"""
        value = 0
        for col in range(min(16, self.COLUMNS)):
            if self.bits[row][col].punched:
                value |= (1 << col)
        return value
    
    def write_column(self, column: int, value: int):
        """Write byte to column"""
        for row in range(8):
            if value & (1 << row):
                self.punch(row, column)
            else:
                self.unpunch(row, column)
    
    def to_bytes(self) -> bytes:
        """Convert card to byte sequence"""
        data = bytearray()
        for col in range(self.COLUMNS):
            data.append(self.read_column(col))
        return bytes(data)
    
    def from_bytes(self, data: bytes):
        """Load card from byte sequence"""
        for col, byte in enumerate(data):
            if col < self.COLUMNS:
                self.write_column(col, byte)
    
    def to_json(self) -> str:
        """Serialize to JSON"""
        card_data = {
            "card_id": self.card_id,
            "rows": self.ROWS,
            "columns": self.COLUMNS,
            "data": [self.read_column(c) for c in range(self.COLUMNS)],
            "metadata": self.metadata
        }
        return json.dumps(card_data, indent=2)
    
    def from_json(self, json_str: str):
        """Deserialize from JSON"""
        card_data = json.loads(json_str)
        self.card_id = card_data.get("card_id", "")
        self.metadata = card_data.get("metadata", {})
        
        for col, value in enumerate(card_data.get("data", [])):
            if col < self.COLUMNS:
                self.write_column(col, value)
    
    def save(self, filename: str):
        """Save card to file"""
        with open(filename, 'w') as f:
            f.write(self.to_json())
    
    def load(self, filename: str):
        """Load card from file"""
        with open(filename, 'r') as f:
            self.from_json(f.read())
    
    def visual_representation(self) -> str:
        """Get visual ASCII representation"""
        output = f"\nPunch Card: {self.card_id}\n"
        output += "   " + "".join([str(i % 10) for i in range(self.COLUMNS)]) + "\n"
        
        for row in range(self.ROWS):
            output += f"{row:2d}:"
            for col in range(self.COLUMNS):
                if self.bits[row][col].punched:
                    output += "●"
                else:
                    output += "·"
            output += "\n"
        
        return output


class PunchCardReader:
    """Reads punch cards"""
    
    def __init__(self):
        self.current_card = None
        self.current_column = 0
        self.read_data = bytearray()
    
    def load_card(self, card: PunchCard):
        """Load card to reader"""
        self.current_card = card
        self.current_column = 0
        self.read_data = bytearray()
    
    def read_byte(self) -> int:
        """Read next byte from card"""
        if self.current_card and self.current_column < self.current_card.COLUMNS:
            byte = self.current_card.read_column(self.current_column)
            self.read_data.append(byte)
            self.current_column += 1
            return byte
        return 0
    
    def read_all(self) -> bytes:
        """Read entire card"""
        if self.current_card:
            self.read_data = bytearray(self.current_card.to_bytes())
            return bytes(self.read_data)
        return b''


class PunchCardWriter:
    """Writes punch cards"""
    
    def __init__(self):
        self.current_card = None
        self.current_column = 0
    
    def create_card(self, card_id: str = "") -> PunchCard:
        """Create new card"""
        self.current_card = PunchCard(card_id)
        self.current_column = 0
        return self.current_card
    
    def write_byte(self, value: int):
        """Write byte to card"""
        if self.current_card and self.current_column < self.current_card.COLUMNS:
            self.current_card.write_column(self.current_column, value)
            self.current_column += 1
    
    def write_data(self, data: bytes):
        """Write data to card"""
        for byte in data:
            self.write_byte(byte)


# ============================================================================
# KEYBOARD INPUT SYSTEM
# ============================================================================

class KeyboardMapping:
    """Maps keyboard keys to switch inputs"""
    
    # Default QWERTY mapping for 16-bit input
    DEFAULT_MAPPING = {
        'q': 0,   'w': 1,   'e': 2,   'r': 3,
        'a': 4,   's': 5,   'd': 6,   'f': 7,
        'z': 8,   'x': 9,   'c': 10,  'v': 11,
        '1': 12,  '2': 13,  '3': 14,  '4': 15
    }
    
    def __init__(self):
        self.mapping = self.DEFAULT_MAPPING.copy()
        self.pressed_keys = set()
        self.callbacks = []
    
    def set_mapping(self, mapping: Dict[str, int]):
        """Set custom key mapping"""
        self.mapping = mapping
    
    def on_key_press(self, char: str):
        """Handle key press"""
        if char.lower() in self.mapping:
            bit = self.mapping[char.lower()]
            self.pressed_keys.add(bit)
            self.notify_listeners()
    
    def on_key_release(self, char: str):
        """Handle key release"""
        if char.lower() in self.mapping:
            bit = self.mapping[char.lower()]
            self.pressed_keys.discard(bit)
            self.notify_listeners()
    
    def get_value(self) -> int:
        """Get current input value from pressed keys"""
        value = 0
        for bit in self.pressed_keys:
            if 0 <= bit < 16:
                value |= (1 << bit)
        return value
    
    def add_listener(self, callback: Callable):
        """Add callback for input changes"""
        self.callbacks.append(callback)
    
    def notify_listeners(self):
        """Notify all listeners of input change"""
        for callback in self.callbacks:
            callback(self.get_value())
    
    def get_mapping_display(self) -> str:
        """Get display of current key mapping"""
        output = "KEYBOARD MAPPING:\n"
        output += "=" * 50 + "\n"
        
        for key, bit in sorted(self.mapping.items(), key=lambda x: x[1]):
            output += f"Key '{key}' -> Bit {bit:2d}\n"
        
        return output


class KeyboardInputSystem:
    """Keyboard-based input system"""
    
    def __init__(self, switch_count: int = 16):
        self.switch_count = switch_count
        self.switches = [0] * switch_count
        self.mapping = KeyboardMapping()
        self.input_value = 0
    
    def bind_key(self, root: tk.Widget):
        """Bind keyboard events to Tkinter widget"""
        for key in self.mapping.mapping.keys():
            root.bind(f'<KeyPress-{key}>', self.on_key_event)
            root.bind(f'<KeyRelease-{key}>', self.on_key_event)
    
    def on_key_event(self, event):
        """Handle keyboard event"""
        if event.type == tk.EventType.KeyPress:
            self.mapping.on_key_press(event.char)
        else:
            self.mapping.on_key_release(event.char)
        
        self.update_switches()
    
    def update_switches(self):
        """Update switch states from keyboard"""
        self.input_value = self.mapping.get_value()
        
        for i in range(self.switch_count):
            self.switches[i] = (self.input_value >> i) & 1
    
    def get_switch(self, index: int) -> int:
        """Get switch state"""
        if 0 <= index < self.switch_count:
            return self.switches[index]
        return 0
    
    def get_value(self) -> int:
        """Get combined input value"""
        return self.input_value


# ============================================================================
# I/O FUNCTION SYSTEM
# ============================================================================

class IOFunction:
    """Base class for I/O functions"""
    
    def __init__(self, name: str):
        self.name = name
        self.input_value = 0
        self.output_value = 0
    
    def execute(self, input_value: int) -> int:
        """Execute function"""
        self.input_value = input_value
        return self.output_value


class LogicFunction(IOFunction):
    """Function that applies logic gate to input"""
    
    def __init__(self, name: str, gate: LogicGate):
        super().__init__(name)
        self.gate = gate
    
    def execute(self, input_value: int) -> int:
        """Apply logic gate to input"""
        bits = [(input_value >> i) & 1 for i in range(8)]
        self.output_value = self.gate.set_inputs(*bits[:self.gate.inputs.__len__() + 1])
        return self.output_value


class BitShiftFunction(IOFunction):
    """Bit shift function"""
    
    def __init__(self, name: str, shift_direction: str = "left", shift_amount: int = 1):
        super().__init__(name)
        self.shift_direction = shift_direction
        self.shift_amount = shift_amount
    
    def execute(self, input_value: int) -> int:
        """Shift bits left or right"""
        if self.shift_direction == "left":
            self.output_value = (input_value << self.shift_amount) & 0xFF
        else:  # right
            self.output_value = (input_value >> self.shift_amount) & 0xFF
        return self.output_value


class BitwiseFunction(IOFunction):
    """Bitwise operation function"""
    
    def __init__(self, name: str, operation: str = "and", operand: int = 0xFF):
        super().__init__(name)
        self.operation = operation
        self.operand = operand
    
    def execute(self, input_value: int) -> int:
        """Apply bitwise operation"""
        if self.operation == "and":
            self.output_value = input_value & self.operand
        elif self.operation == "or":
            self.output_value = input_value | self.operand
        elif self.operation == "xor":
            self.output_value = input_value ^ self.operand
        elif self.operation == "not":
            self.output_value = (~input_value) & 0xFF
        
        return self.output_value


class RotateFunction(IOFunction):
    """Bit rotation function"""
    
    def __init__(self, name: str, rotate_direction: str = "left", amount: int = 1):
        super().__init__(name)
        self.rotate_direction = rotate_direction
        self.amount = amount
    
    def execute(self, input_value: int) -> int:
        """Rotate bits"""
        amount = self.amount % 8
        
        if self.rotate_direction == "left":
            self.output_value = ((input_value << amount) | (input_value >> (8 - amount))) & 0xFF
        else:  # right
            self.output_value = ((input_value >> amount) | (input_value << (8 - amount))) & 0xFF
        
        return self.output_value


class FunctionChain:
    """Chain multiple functions together"""
    
    def __init__(self, name: str = "Chain"):
        self.name = name
        self.functions: List[IOFunction] = []
    
    def add_function(self, func: IOFunction):
        """Add function to chain"""
        self.functions.append(func)
    
    def execute(self, input_value: int) -> int:
        """Execute all functions in chain"""
        output = input_value
        for func in self.functions:
            output = func.execute(output)
        return output


# ============================================================================
# INTEGRATED I/O CONTROL SYSTEM
# ============================================================================

class IntegratedIOSystem:
    """Integrated input/output control system"""
    
    def __init__(self):
        self.input_systems: Dict[str, any] = {}
        self.output_systems: Dict[str, any] = {}
        self.functions: Dict[str, IOFunction] = {}
        self.logic_gates: Dict[str, LogicGate] = {}
        self.punch_cards: Dict[str, PunchCard] = {}
    
    def register_input(self, name: str, system: any):
        """Register input system"""
        self.input_systems[name] = system
    
    def register_output(self, name: str, system: any):
        """Register output system"""
        self.output_systems[name] = system
    
    def register_function(self, name: str, func: IOFunction):
        """Register I/O function"""
        self.functions[name] = func
    
    def register_gate(self, name: str, gate: LogicGate):
        """Register logic gate"""
        self.logic_gates[name] = gate
    
    def add_punch_card(self, name: str, card: PunchCard):
        """Add punch card"""
        self.punch_cards[name] = card
    
    def execute_function_chain(self, chain_name: str, input_value: int):
        """Execute function chain"""
        if chain_name in self.functions:
            func = self.functions[chain_name]
            if isinstance(func, FunctionChain):
                return func.execute(input_value)
        return input_value
    
    def get_status(self) -> str:
        """Get system status"""
        status = "INTEGRATED I/O SYSTEM STATUS:\n"
        status += "=" * 80 + "\n\n"
        
        status += f"Input Systems: {len(self.input_systems)}\n"
        for name in self.input_systems:
            status += f"  - {name}\n"
        
        status += f"\nOutput Systems: {len(self.output_systems)}\n"
        for name in self.output_systems:
            status += f"  - {name}\n"
        
        status += f"\nFunctions: {len(self.functions)}\n"
        for name in self.functions:
            status += f"  - {name}\n"
        
        status += f"\nLogic Gates: {len(self.logic_gates)}\n"
        for name in self.logic_gates:
            status += f"  - {name}\n"
        
        status += f"\nPunch Cards: {len(self.punch_cards)}\n"
        for name in self.punch_cards:
            status += f"  - {name}\n"
        
        return status


# ============================================================================
# GUI FOR PUNCH CARD AND I/O SYSTEM
# ============================================================================

class PunchCardIOGUI:
    """GUI for punch card and I/O system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Punch Card & I/O System")
        self.root.configure(bg="#1a1a1a")
        
        # Systems
        self.io_system = IntegratedIOSystem()
        self.current_card = None
        self.reader = PunchCardReader()
        self.writer = PunchCardWriter()
        self.keyboard = KeyboardInputSystem()
        
        # Create notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_punch_card_tab()
        self.create_logic_gates_tab()
        self.create_keyboard_tab()
        self.create_functions_tab()
        self.create_system_status_tab()
    
    def create_punch_card_tab(self):
        """Create punch card tab"""
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Punch Cards")
        
        # Title
        title = tk.Label(frame, text="PUNCH CARD SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Controls
        control_frame = tk.Frame(frame, bg="#1a1a1a")
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="NEW CARD", command=self.new_card,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="LOAD CARD", command=self.load_card,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="SAVE CARD", command=self.save_card,
                 bg="#ff9900", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="VISUALIZE", command=self.visualize_card,
                 bg="#ff00ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Card display
        self.card_display = scrolledtext.ScrolledText(frame, height=25, width=150,
                                                      bg="#000", fg="#00ff00",
                                                      font=("Courier", 8))
        self.card_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_logic_gates_tab(self):
        """Create logic gates tab"""
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Logic Gates")
        
        # Title
        title = tk.Label(frame, text="LOGIC GATE SIMULATOR", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Gate selector
        selector_frame = tk.Frame(frame, bg="#1a1a1a")
        selector_frame.pack(pady=10)
        
        tk.Label(selector_frame, text="Gate Type:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.gate_selector = ttk.Combobox(selector_frame, 
                                          values=[g.value for g in LogicGateType],
                                          state="readonly", width=15)
        self.gate_selector.set("AND")
        self.gate_selector.pack(side=tk.LEFT, padx=5)
        
        tk.Button(selector_frame, text="CREATE GATE", command=self.create_gate,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Gate display
        self.gate_display = scrolledtext.ScrolledText(frame, height=20, width=150,
                                                      bg="#000", fg="#ffff00",
                                                      font=("Courier", 9))
        self.gate_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_keyboard_tab(self):
        """Create keyboard input tab"""
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Keyboard Input")
        
        # Title
        title = tk.Label(frame, text="KEYBOARD INPUT SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Mapping display
        self.keyboard_display = scrolledtext.ScrolledText(frame, height=25, width=150,
                                                          bg="#000", fg="#00ffff",
                                                          font=("Courier", 9))
        self.keyboard_display.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.update_keyboard_display()
    
    def create_functions_tab(self):
        """Create functions tab"""
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="I/O Functions")
        
        # Title
        title = tk.Label(frame, text="I/O FUNCTION SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Function controls
        control_frame = tk.Frame(frame, bg="#1a1a1a")
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Function:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.func_selector = ttk.Combobox(control_frame,
                                          values=["BitShift", "Bitwise", "Rotate"],
                                          state="readonly", width=15)
        self.func_selector.set("BitShift")
        self.func_selector.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="CREATE FUNCTION", command=self.create_function,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Test input
        tk.Label(control_frame, text="Test Input:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.func_input = tk.Entry(control_frame, width=5, bg="#000", fg="#00ff00",
                                  font=("Courier", 10))
        self.func_input.insert(0, "255")
        self.func_input.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="TEST", command=self.test_function,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Function display
        self.func_display = scrolledtext.ScrolledText(frame, height=20, width=150,
                                                      bg="#000", fg="#ff00ff",
                                                      font=("Courier", 9))
        self.func_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_system_status_tab(self):
        """Create system status tab"""
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="System Status")
        
        # Title
        title = tk.Label(frame, text="INTEGRATED I/O SYSTEM STATUS", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Status display
        self.status_display = scrolledtext.ScrolledText(frame, height=25, width=150,
                                                        bg="#000", fg="#00ff00",
                                                        font=("Courier", 9))
        self.status_display.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.update_status_display()
    
    def new_card(self):
        """Create new punch card"""
        card_id = tk.simpledialog.askstring("New Card", "Enter card ID:", parent=self.root)
        if card_id:
            self.current_card = PunchCard(card_id)
            self.visualize_card()
            messagebox.showinfo("Success", f"Created card: {card_id}")
    
    def load_card(self):
        """Load punch card from file"""
        filename = filedialog.askopenfilename(
            title="Load Punch Card",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_card = PunchCard()
                self.current_card.load(filename)
                self.visualize_card()
                messagebox.showinfo("Success", f"Loaded card: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load card: {e}")
    
    def save_card(self):
        """Save punch card to file"""
        if not self.current_card:
            messagebox.showerror("Error", "No card loaded")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Punch Card",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_card.save(filename)
                messagebox.showinfo("Success", f"Saved card: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save card: {e}")
    
    def visualize_card(self):
        """Display card visualization"""
        if not self.current_card:
            messagebox.showerror("Error", "No card loaded")
            return
        
        self.card_display.delete(1.0, tk.END)
        self.card_display.insert(1.0, self.current_card.visual_representation())
    
    def create_gate(self):
        """Create logic gate"""
        gate_type_str = self.gate_selector.get()
        gate_type = LogicGateType[gate_type_str]
        
        gate_name = f"{gate_type_str}_1"
        gate = LogicGate(gate_type, gate_name)
        
        self.io_system.register_gate(gate_name, gate)
        
        self.gate_display.delete(1.0, tk.END)
        display = f"CREATED LOGIC GATE: {gate_name}\n"
        display += "=" * 100 + "\n\n"
        display += f"Gate Type: {gate.gate_type.value}\n"
        display += f"Inputs: {gate.inputs}\n"
        display += f"Output: {gate.output}\n\n"
        display += "TRUTH TABLE:\n"
        display += "-" * 50 + "\n"
        
        for inputs, output in gate.truth_table():
            display += f"Inputs: {inputs} -> Output: {output}\n"
        
        self.gate_display.insert(1.0, display)
    
    def update_keyboard_display(self):
        """Update keyboard display"""
        self.keyboard_display.delete(1.0, tk.END)
        self.keyboard_display.insert(1.0, self.keyboard.mapping.get_mapping_display())
    
    def create_function(self):
        """Create I/O function"""
        func_type = self.func_selector.get()
        
        if func_type == "BitShift":
            func = BitShiftFunction("BitShift_1", "left", 1)
        elif func_type == "Bitwise":
            func = BitwiseFunction("Bitwise_1", "and", 0xFF)
        else:  # Rotate
            func = RotateFunction("Rotate_1", "left", 1)
        
        self.io_system.register_function(func.name, func)
        self.display_function_info(func)
    
    def test_function(self):
        """Test I/O function"""
        try:
            input_val = int(self.func_input.get())
            
            if not self.io_system.functions:
                messagebox.showerror("Error", "No functions registered")
                return
            
            func_name = list(self.io_system.functions.keys())[-1]
            func = self.io_system.functions[func_name]
            output = func.execute(input_val)
            
            self.func_display.delete(1.0, tk.END)
            display = f"FUNCTION TEST: {func.name}\n"
            display += "=" * 100 + "\n\n"
            display += f"Function Type: {type(func).__name__}\n"
            display += f"Input Value: {input_val} (0x{input_val:02X}, 0b{input_val:08b})\n"
            display += f"Output Value: {output} (0x{output:02X}, 0b{output:08b})\n"
            
            self.func_display.insert(1.0, display)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input value")
    
    def display_function_info(self, func: IOFunction):
        """Display function information"""
        self.func_display.delete(1.0, tk.END)
        
        display = f"CREATED FUNCTION: {func.name}\n"
        display += "=" * 100 + "\n\n"
        display += f"Function Type: {type(func).__name__}\n"
        display += f"Input: {func.input_value}\n"
        display += f"Output: {func.output_value}\n"
        
        if hasattr(func, 'shift_direction'):
            display += f"Shift Direction: {func.shift_direction}\n"
            display += f"Shift Amount: {func.shift_amount}\n"
        
        if hasattr(func, 'operation'):
            display += f"Operation: {func.operation}\n"
            display += f"Operand: 0x{func.operand:02X}\n"
        
        if hasattr(func, 'rotate_direction'):
            display += f"Rotate Direction: {func.rotate_direction}\n"
            display += f"Rotate Amount: {func.amount}\n"
        
        self.func_display.insert(1.0, display)
    
    def update_status_display(self):
        """Update system status display"""
        self.status_display.delete(1.0, tk.END)
        self.status_display.insert(1.0, self.io_system.get_status())


def main():
    root = tk.Tk()
    root.geometry("1700x1000")
    app = PunchCardIOGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
