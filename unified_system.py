#!/usr/bin/env python3
"""
ULTIMATE UNIFIED COMPUTER SIMULATION SYSTEM
Complete integration of all features into one program:
- Multi-Architecture Computer (8/16/32/64/128/256-bit)
- Punch Card Reader/Writer System
- Logic Gate Simulator (7 gate types)
- Keyboard Input Mapping (16-bit)
- I/O Function Processor (BitShift, Bitwise, Rotate, Chains)
- Integrated Debugger with Breakpoints
- Memory Management
- Configuration System
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import json
import os
from enum import Enum
from typing import List, Dict, Tuple, Callable
from dataclasses import dataclass
from computer_architectures import *


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class LogicGateType(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    XOR = "XOR"
    NAND = "NAND"
    NOR = "NOR"
    XNOR = "XNOR"


@dataclass
class PunchCardBit:
    row: int
    column: int
    punched: bool = False
    value: int = 0


# ============================================================================
# LOGIC GATES
# ============================================================================

class LogicGate:
    def __init__(self, gate_type: LogicGateType, name: str = None):
        self.gate_type = gate_type
        self.name = name or gate_type.value
        self.inputs = []
        self.output = 0
    
    def set_inputs(self, *inputs):
        self.inputs = list(inputs)
        self.compute()
        return self.output
    
    def compute(self):
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
        input_count = 2
        table = []
        for i in range(2 ** input_count):
            inputs = [(i >> j) & 1 for j in range(input_count)]
            output = self.set_inputs(*inputs)
            table.append((inputs, output))
        return table


# ============================================================================
# PUNCH CARD SYSTEM
# ============================================================================

class PunchCard:
    ROWS = 12
    COLUMNS = 80
    
    def __init__(self, card_id: str = ""):
        self.card_id = card_id
        self.bits = []
        self.metadata = {}
        
        for row in range(self.ROWS):
            row_data = []
            for col in range(self.COLUMNS):
                row_data.append(PunchCardBit(row, col))
            self.bits.append(row_data)
    
    def punch(self, row: int, column: int):
        if 0 <= row < self.ROWS and 0 <= column < self.COLUMNS:
            self.bits[row][column].punched = True
            self.bits[row][column].value = 1
    
    def unpunch(self, row: int, column: int):
        if 0 <= row < self.ROWS and 0 <= column < self.COLUMNS:
            self.bits[row][column].punched = False
            self.bits[row][column].value = 0
    
    def read_column(self, column: int) -> int:
        value = 0
        for row in range(min(8, self.ROWS)):
            if self.bits[row][column].punched:
                value |= (1 << row)
        return value
    
    def write_column(self, column: int, value: int):
        for row in range(8):
            if value & (1 << row):
                self.punch(row, column)
            else:
                self.unpunch(row, column)
    
    def to_bytes(self) -> bytes:
        data = bytearray()
        for col in range(self.COLUMNS):
            data.append(self.read_column(col))
        return bytes(data)
    
    def from_bytes(self, data: bytes):
        for col, byte in enumerate(data):
            if col < self.COLUMNS:
                self.write_column(col, byte)
    
    def to_json(self) -> str:
        card_data = {
            "card_id": self.card_id,
            "data": [self.read_column(c) for c in range(self.COLUMNS)],
            "metadata": self.metadata
        }
        return json.dumps(card_data, indent=2)
    
    def from_json(self, json_str: str):
        card_data = json.loads(json_str)
        self.card_id = card_data.get("card_id", "")
        self.metadata = card_data.get("metadata", {})
        for col, value in enumerate(card_data.get("data", [])):
            if col < self.COLUMNS:
                self.write_column(col, value)
    
    def visual_representation(self) -> str:
        output = f"\nPunch Card: {self.card_id}\n"
        output += "   " + "".join([str(i % 10) for i in range(self.COLUMNS)]) + "\n"
        for row in range(self.ROWS):
            output += f"{row:2d}:"
            for col in range(self.COLUMNS):
                output += "●" if self.bits[row][col].punched else "·"
            output += "\n"
        return output


# ============================================================================
# I/O FUNCTIONS
# ============================================================================

class IOFunction:
    def __init__(self, name: str):
        self.name = name
        self.input_value = 0
        self.output_value = 0
    
    def execute(self, input_value: int) -> int:
        self.input_value = input_value
        return self.output_value


class BitShiftFunction(IOFunction):
    def __init__(self, name: str, shift_direction: str = "left", shift_amount: int = 1):
        super().__init__(name)
        self.shift_direction = shift_direction
        self.shift_amount = shift_amount
    
    def execute(self, input_value: int) -> int:
        if self.shift_direction == "left":
            self.output_value = (input_value << self.shift_amount) & 0xFF
        else:
            self.output_value = (input_value >> self.shift_amount) & 0xFF
        return self.output_value


class BitwiseFunction(IOFunction):
    def __init__(self, name: str, operation: str = "and", operand: int = 0xFF):
        super().__init__(name)
        self.operation = operation
        self.operand = operand
    
    def execute(self, input_value: int) -> int:
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
    def __init__(self, name: str, rotate_direction: str = "left", amount: int = 1):
        super().__init__(name)
        self.rotate_direction = rotate_direction
        self.amount = amount
    
    def execute(self, input_value: int) -> int:
        amount = self.amount % 8
        if self.rotate_direction == "left":
            self.output_value = ((input_value << amount) | (input_value >> (8 - amount))) & 0xFF
        else:
            self.output_value = ((input_value >> amount) | (input_value << (8 - amount))) & 0xFF
        return self.output_value


class FunctionChain:
    def __init__(self, name: str = "Chain"):
        self.name = name
        self.functions: List[IOFunction] = []
    
    def add_function(self, func: IOFunction):
        self.functions.append(func)
    
    def execute(self, input_value: int) -> int:
        output = input_value
        for func in self.functions:
            output = func.execute(output)
        return output


# ============================================================================
# KEYBOARD MAPPING
# ============================================================================

class KeyboardMapping:
    DEFAULT_MAPPING = {
        'q': 0,   'w': 1,   'e': 2,   'r': 3,
        'a': 4,   's': 5,   'd': 6,   'f': 7,
        'z': 8,   'x': 9,   'c': 10,  'v': 11,
        '1': 12,  '2': 13,  '3': 14,  '4': 15
    }
    
    def __init__(self):
        self.mapping = self.DEFAULT_MAPPING.copy()
        self.pressed_keys = set()
    
    def on_key_press(self, char: str):
        if char.lower() in self.mapping:
            self.pressed_keys.add(self.mapping[char.lower()])
    
    def on_key_release(self, char: str):
        if char.lower() in self.mapping:
            self.pressed_keys.discard(self.mapping[char.lower()])
    
    def get_value(self) -> int:
        value = 0
        for bit in self.pressed_keys:
            if 0 <= bit < 16:
                value |= (1 << bit)
        return value
    
    def get_mapping_display(self) -> str:
        output = "KEYBOARD MAPPING:\n"
        output += "=" * 80 + "\n"
        for key, bit in sorted(self.mapping.items(), key=lambda x: x[1]):
            output += f"Key '{key}' -> Bit {bit:2d}\n"
        return output


# ============================================================================
# UNIFIED GUI APPLICATION
# ============================================================================

class UnifiedComputerSystem:
    """Complete unified computer simulation system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ULTIMATE UNIFIED COMPUTER SIMULATION SYSTEM v2.0")
        self.root.configure(bg="#1a1a1a")
        self.root.geometry("1800x1100")
        
        # Systems
        self.computer = Computer8Bit()
        self.arch_type = "8-bit"
        self.current_punch_card = None
        self.keyboard = KeyboardMapping()
        self.input_switches = [0] * 16
        self.breakpoints = set()
        self.watch_expressions = {}
        self.functions = {}
        self.logic_gates = {}
        
        self.settings = self.load_settings()
        self.running = False
        self.paused = False
        
        # Initialize display dictionaries
        self.reg_display = None
        self.info_text = None
        self.card_display = None
        self.gate_display = None
        self.func_display = None
        self.watch_display = None
        self.mem_display = None
        self.settings_display = None
        self.output_labels = {}
        self.input_labels = {}
        
        # Create UI
        self.create_notebook()
        self.create_all_tabs()
        
    def load_settings(self):
        default_settings = {
            "sound_enabled": False,
            "refresh_rate": 100,
            "display_format": "all",
            "theme": "dark"
        }
        if os.path.exists("config.json"):
            try:
                with open("config.json", 'r') as f:
                    return {**default_settings, **json.load(f)}
            except:
                pass
        return default_settings
    
    def save_settings(self):
        with open("config.json", 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
    
    def create_all_tabs(self):
        """Create all system tabs"""
        self.create_computer_tab()
        self.create_io_tab()
        self.create_punch_card_tab()
        self.create_logic_tab()
        self.create_keyboard_tab()
        self.create_functions_tab()
        self.create_debugger_tab()
        self.create_memory_tab()
        self.create_settings_tab()
    
    # ========== COMPUTER TAB ==========
    def create_computer_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Computer")
        
        # Title
        title = tk.Label(frame, text="MULTI-ARCHITECTURE COMPUTER SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Architecture selector
        arch_frame = tk.Frame(frame, bg="#1a1a1a")
        arch_frame.pack(pady=10)
        
        for arch in ["8-bit", "16-bit", "32-bit", "64-bit", "128-bit", "256-bit"]:
            tk.Button(arch_frame, text=arch, command=lambda a=arch: self.switch_architecture(a),
                     bg="#333", fg="white", font=("Courier", 9, "bold"), width=10).pack(side=tk.LEFT, padx=5)
        
        self.arch_label = tk.Label(frame, text="Current: 8-bit", 
                                   fg="#00ff00", bg="#1a1a1a", font=("Courier", 12, "bold"))
        self.arch_label.pack(pady=5)
        
        # System info
        info_frame = tk.LabelFrame(frame, text="SYSTEM INFO", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        info_frame.pack(pady=10, padx=20, fill="x")
        
        self.info_text = tk.Text(info_frame, height=6, width=180, bg="#000", fg="#00ff00",
                                font=("Courier", 9), relief=tk.FLAT)
        self.info_text.pack(pady=5, padx=5)
        
        # Registers
        reg_frame = tk.LabelFrame(frame, text="REGISTERS (ALL FORMATS)", 
                                 fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        reg_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.reg_display = scrolledtext.ScrolledText(reg_frame, height=12, width=180,
                                                     bg="#000", fg="#00ff00",
                                                     font=("Courier", 8))
        self.reg_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Control buttons
        button_frame = tk.Frame(frame, bg="#1a1a1a")
        button_frame.pack(pady=10)
        
        for text, cmd, color in [("STEP", self.step, "#0066ff"),
                                 ("RUN", self.run, "#00ff00"),
                                 ("PAUSE", self.pause, "#ff9900"),
                                 ("RESET", self.reset, "#ff0000"),
                                 ("LOAD", self.load_program, "#ffff00")]:
            tk.Button(button_frame, text=text, command=cmd, bg=color,
                     fg="black" if color in ["#ffff00", "#00ff00"] else "white",
                     font=("Courier", 10, "bold"), width=10).pack(side=tk.LEFT, padx=5)
        
        self.update_display()
    
    # ========== INPUT/OUTPUT TAB ==========
    def create_io_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Input/Output")
        
        title = tk.Label(frame, text="INPUT/OUTPUT SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Input switches
        input_frame = tk.LabelFrame(frame, text="16-BIT INPUT SWITCHES", 
                                   fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        input_frame.pack(pady=10, padx=20, fill="x")
        
        switches_container = tk.Frame(input_frame, bg="#1a1a1a")
        switches_container.pack(pady=10)
        
        self.switch_buttons = []
        self.switch_labels = {}
        
        for i in range(15, -1, -1):
            frame_bit = tk.Frame(switches_container, bg="#1a1a1a")
            frame_bit.pack(side=tk.LEFT, padx=2)
            
            tk.Label(frame_bit, text=f"B{i}", fg="#ffff00", bg="#1a1a1a",
                    font=("Courier", 9, "bold")).pack()
            
            btn = tk.Button(frame_bit, text="OFF", command=lambda idx=i: self.toggle_switch(idx),
                          bg="#333", fg="#00ff00", font=("Courier", 9, "bold"),
                          width=4, height=2, relief=tk.SUNKEN)
            btn.pack()
            self.switch_buttons.append(btn)
            
            val_label = tk.Label(frame_bit, text="0", fg="#00ff00", bg="#000",
                               font=("Courier", 8, "bold"), width=3)
            val_label.pack()
            self.switch_labels[i] = (val_label, btn)
        
        # Input displays
        display_frame = tk.Frame(input_frame, bg="#1a1a1a")
        display_frame.pack(pady=5)
        
        self.input_labels = {}
        for fmt, color in [("BIN", "#00ff00"), ("HEX", "#ffff00"), ("DEC", "#00ffff")]:
            tk.Label(display_frame, text=f"{fmt}:", fg=color, bg="#1a1a1a",
                    font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
            label = tk.Label(display_frame, text="0", fg=color, bg="#000",
                           font=("Courier", 10, "bold"), width=20)
            label.pack(side=tk.LEFT, padx=5)
            self.input_labels[fmt] = label
        
        # Output displays
        output_frame = tk.LabelFrame(frame, text="OUTPUT", 
                                    fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        output_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.output_labels = {}
        for fmt, color in [("BIN", "#00ff00"), ("HEX", "#ffff00"), 
                          ("DEC", "#00ffff"), ("OCT", "#ff00ff")]:
            frame_out = tk.Frame(output_frame, bg="#1a1a1a")
            frame_out.pack(fill="x", pady=5)
            
            tk.Label(frame_out, text=f"{fmt}:", fg=color, bg="#1a1a1a",
                    font=("Courier", 10, "bold"), width=10).pack(side=tk.LEFT, padx=5)
            
            label = tk.Label(frame_out, text="0", fg=color, bg="#000",
                           font=("Courier", 10, "bold"), relief=tk.SUNKEN, padx=10)
            label.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
            self.output_labels[fmt] = label
    
    # ========== PUNCH CARD TAB ==========
    def create_punch_card_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Punch Cards")
        
        title = tk.Label(frame, text="PUNCH CARD SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        button_frame = tk.Frame(frame, bg="#1a1a1a")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="NEW CARD", command=self.new_punch_card,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="LOAD", command=self.load_punch_card,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="SAVE", command=self.save_punch_card,
                 bg="#ff9900", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="VISUALIZE", command=self.visualize_punch_card,
                 bg="#ff00ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.card_display = scrolledtext.ScrolledText(frame, height=25, width=180,
                                                      bg="#000", fg="#00ff00",
                                                      font=("Courier", 7))
        self.card_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    # ========== LOGIC GATES TAB ==========
    def create_logic_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Logic Gates")
        
        title = tk.Label(frame, text="LOGIC GATE SIMULATOR", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        selector_frame = tk.Frame(frame, bg="#1a1a1a")
        selector_frame.pack(pady=10)
        
        tk.Label(selector_frame, text="Gate:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.gate_selector = ttk.Combobox(selector_frame,
                                          values=[g.value for g in LogicGateType],
                                          state="readonly", width=15)
        self.gate_selector.set("AND")
        self.gate_selector.pack(side=tk.LEFT, padx=5)
        
        tk.Button(selector_frame, text="CREATE", command=self.create_logic_gate,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.gate_display = scrolledtext.ScrolledText(frame, height=25, width=180,
                                                      bg="#000", fg="#ffff00",
                                                      font=("Courier", 9))
        self.gate_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    # ========== KEYBOARD TAB ==========
    def create_keyboard_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Keyboard Input")
        
        title = tk.Label(frame, text="KEYBOARD INPUT SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        self.keyboard_display = scrolledtext.ScrolledText(frame, height=30, width=180,
                                                          bg="#000", fg="#00ffff",
                                                          font=("Courier", 9))
        self.keyboard_display.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.keyboard_display.insert(1.0, self.keyboard.get_mapping_display())
        self.keyboard_display.config(state=tk.DISABLED)
    
    # ========== FUNCTIONS TAB ==========
    def create_functions_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="I/O Functions")
        
        title = tk.Label(frame, text="I/O FUNCTION SYSTEM", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        control_frame = tk.Frame(frame, bg="#1a1a1a")
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Function:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.func_selector = ttk.Combobox(control_frame,
                                          values=["BitShift", "Bitwise", "Rotate"],
                                          state="readonly", width=15)
        self.func_selector.set("BitShift")
        self.func_selector.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="CREATE", command=self.create_function,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="Test:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.func_input = tk.Entry(control_frame, width=5, bg="#000", fg="#00ff00",
                                  font=("Courier", 10))
        self.func_input.insert(0, "255")
        self.func_input.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="TEST", command=self.test_function,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.func_display = scrolledtext.ScrolledText(frame, height=25, width=180,
                                                      bg="#000", fg="#ff00ff",
                                                      font=("Courier", 9))
        self.func_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    # ========== DEBUGGER TAB ==========
    def create_debugger_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Debugger")
        
        title = tk.Label(frame, text="DEBUGGER & ANALYZER", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Breakpoints
        bp_frame = tk.LabelFrame(frame, text="BREAKPOINTS", 
                                fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        bp_frame.pack(pady=10, padx=20, fill="x")
        
        bp_input = tk.Frame(bp_frame, bg="#1a1a1a")
        bp_input.pack(pady=5)
        
        tk.Label(bp_input, text="Address:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        
        self.bp_entry = tk.Entry(bp_input, width=10, bg="#000", fg="#00ff00",
                                font=("Courier", 10))
        self.bp_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(bp_input, text="ADD", command=self.add_breakpoint,
                 bg="#ff0066", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(bp_input, text="CLEAR ALL", command=self.clear_breakpoints,
                 bg="#ff0000", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.bp_display = tk.Label(bp_frame, text="Breakpoints: None", 
                                   fg="#ff0066", bg="#000", font=("Courier", 9),
                                   anchor="w", justify=tk.LEFT, padx=5, pady=5)
        self.bp_display.pack(fill="x")
        
        # Watch expressions
        watch_frame = tk.LabelFrame(frame, text="WATCH EXPRESSIONS", 
                                   fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        watch_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        watch_input = tk.Frame(watch_frame, bg="#1a1a1a")
        watch_input.pack(pady=5)
        
        tk.Label(watch_input, text="Expression:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        
        self.watch_entry = tk.Entry(watch_input, width=30, bg="#000", fg="#00ffff",
                                   font=("Courier", 10))
        self.watch_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(watch_input, text="ADD", command=self.add_watch,
                 bg="#0066ff", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.watch_display = scrolledtext.ScrolledText(watch_frame, height=15, width=180,
                                                       bg="#000", fg="#00ffff",
                                                       font=("Courier", 9))
        self.watch_display.pack(pady=5, padx=5, fill="both", expand=True)
    
    # ========== MEMORY TAB ==========
    def create_memory_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Memory")
        
        title = tk.Label(frame, text="MEMORY EDITOR & VIEWER", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        control_frame = tk.Frame(frame, bg="#1a1a1a")
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Address (Hex):", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.mem_addr = tk.Entry(control_frame, width=10, bg="#000", fg="#00ff00",
                                font=("Courier", 10))
        self.mem_addr.insert(0, "0000")
        self.mem_addr.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="VIEW", command=self.view_memory,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="FILL", command=self.fill_memory,
                 bg="#ff9900", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="CLEAR", command=self.clear_memory,
                 bg="#ff0000", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.mem_display = scrolledtext.ScrolledText(frame, height=25, width=180,
                                                     bg="#000", fg="#00ff00",
                                                     font=("Courier", 8))
        self.mem_display.pack(pady=10, padx=20, fill="both", expand=True)
    
    # ========== SETTINGS TAB ==========
    def create_settings_tab(self):
        frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(frame, text="Settings")
        
        title = tk.Label(frame, text="SYSTEM CONFIGURATION", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        button_frame = tk.Frame(frame, bg="#1a1a1a")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="REFRESH", command=self.refresh_settings,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="SAVE", command=self.save_settings,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="RESET", command=self.reset_settings,
                 bg="#ff0000", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.settings_display = scrolledtext.ScrolledText(frame, height=30, width=180,
                                                          bg="#000", fg="#00ff00",
                                                          font=("Courier", 9))
        self.settings_display.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.refresh_settings()
    
    # ========== METHODS ==========
    
    def switch_architecture(self, arch_type):
        if arch_type == "8-bit":
            self.computer = Computer8Bit()
        elif arch_type == "16-bit":
            self.computer = Computer16Bit()
        elif arch_type == "32-bit":
            self.computer = Computer32Bit()
        elif arch_type == "64-bit":
            self.computer = Computer64Bit()
        elif arch_type == "128-bit":
            self.computer = Computer128Bit()
        elif arch_type == "256-bit":
            self.computer = Computer256Bit()
        
        self.arch_type = arch_type
        self.arch_label.config(text=f"Current: {arch_type}")
        self.update_display()
    
    def update_display(self):
        if not self.info_text or not self.reg_display:
            return
        
        # System info
        self.info_text.delete(1.0, tk.END)
        info = f"Architecture: {self.arch_type} | Bit Width: {self.computer.bit_width} | "
        info += f"Memory: {self.computer.memory_size:,} bytes | Registers: {self.computer.num_registers}"
        self.info_text.insert(1.0, info)
        
        # Registers
        self.reg_display.delete(1.0, tk.END)
        reg_text = ""
        for i in range(self.computer.num_registers):
            reg_name = chr(ord('A') + i)
            value = self.computer.registers[i]
            binary = bin(value)[2:].zfill(self.computer.bit_width)
            hexval = f"0x{value:0{self.computer.bit_width//4}X}"
            reg_text += f"{reg_name}: BIN: {binary}  HEX: {hexval}  DEC: {value}\n"
        self.reg_display.insert(1.0, reg_text)
        
        # Output displays
        if self.output_labels:
            output_val = self.computer.registers[0]
            self.output_labels['BIN'].config(text=bin(output_val)[2:].zfill(8))
            self.output_labels['HEX'].config(text=f"0x{output_val:02X}")
            self.output_labels['DEC'].config(text=str(output_val))
            self.output_labels['OCT'].config(text=f"0o{oct(output_val)[2:].upper()}")
    
    def toggle_switch(self, bit_index):
        self.input_switches[bit_index] = 1 - self.input_switches[bit_index]
        _, btn = self.switch_labels[bit_index]
        if self.input_switches[bit_index]:
            btn.config(bg="#00ff00", fg="black", text="ON")
        else:
            btn.config(bg="#333", fg="#00ff00", text="OFF")
        self.update_input_display()
    
    def update_input_display(self):
        value = 0
        for i, switch_val in enumerate(self.input_switches):
            if switch_val:
                value |= (1 << i)
        
        self.input_labels['BIN'].config(text=bin(value)[2:].zfill(16))
        self.input_labels['HEX'].config(text=f"0x{value:04X}")
        self.input_labels['DEC'].config(text=str(value))
    
    def new_punch_card(self):
        card_id = simpledialog.askstring("New Card", "Enter card ID:", parent=self.root)
        if card_id:
            self.current_punch_card = PunchCard(card_id)
            messagebox.showinfo("Success", f"Created card: {card_id}")
    
    def load_punch_card(self):
        filename = filedialog.askopenfilename(
            title="Load Punch Card",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.current_punch_card = PunchCard()
                with open(filename, 'r') as f:
                    self.current_punch_card.from_json(f.read())
                messagebox.showinfo("Success", f"Loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def save_punch_card(self):
        if not self.current_punch_card:
            messagebox.showerror("Error", "No card loaded")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.current_punch_card.to_json())
                messagebox.showinfo("Success", "Card saved")
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")
    
    def visualize_punch_card(self):
        if not self.current_punch_card:
            messagebox.showerror("Error", "No card loaded")
            return
        
        self.card_display.delete(1.0, tk.END)
        self.card_display.insert(1.0, self.current_punch_card.visual_representation())
    
    def create_logic_gate(self):
        gate_type_str = self.gate_selector.get()
        gate_type = LogicGateType[gate_type_str]
        gate = LogicGate(gate_type, f"{gate_type_str}_1")
        self.logic_gates[gate.name] = gate
        
        self.gate_display.delete(1.0, tk.END)
        display = f"LOGIC GATE: {gate.name}\n"
        display += "=" * 100 + "\n\nTruth Table:\n"
        display += "-" * 50 + "\n"
        
        for inputs, output in gate.truth_table():
            display += f"{inputs} -> {output}\n"
        
        self.gate_display.insert(1.0, display)
    
    def create_function(self):
        func_type = self.func_selector.get()
        
        if func_type == "BitShift":
            func = BitShiftFunction("BitShift_1", "left", 1)
        elif func_type == "Bitwise":
            func = BitwiseFunction("Bitwise_1", "and", 0xFF)
        else:
            func = RotateFunction("Rotate_1", "left", 1)
        
        self.functions[func.name] = func
        self.display_function_info(func)
    
    def test_function(self):
        try:
            input_val = int(self.func_input.get())
            if not self.functions:
                messagebox.showerror("Error", "No functions created")
                return
            
            func_name = list(self.functions.keys())[-1]
            func = self.functions[func_name]
            output = func.execute(input_val)
            
            self.func_display.delete(1.0, tk.END)
            display = f"Function: {func.name}\n"
            display += f"Input:  {input_val:3d} (0b{input_val:08b})\n"
            display += f"Output: {output:3d} (0b{output:08b})\n"
            
            self.func_display.insert(1.0, display)
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
    
    def display_function_info(self, func):
        self.func_display.delete(1.0, tk.END)
        display = f"Function: {func.name}\n"
        display += f"Type: {type(func).__name__}\n"
        if hasattr(func, 'shift_direction'):
            display += f"Direction: {func.shift_direction}, Amount: {func.shift_amount}\n"
        self.func_display.insert(1.0, display)
    
    def add_breakpoint(self):
        try:
            addr = int(self.bp_entry.get(), 16)
            self.breakpoints.add(addr)
            self.update_breakpoints_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid hex address")
    
    def clear_breakpoints(self):
        self.breakpoints.clear()
        self.update_breakpoints_display()
    
    def update_breakpoints_display(self):
        if self.breakpoints:
            bp_text = "Breakpoints: " + ", ".join([f"0x{a:X}" for a in sorted(self.breakpoints)])
        else:
            bp_text = "Breakpoints: None"
        self.bp_display.config(text=bp_text)
    
    def add_watch(self):
        expr = self.watch_entry.get()
        if expr:
            self.watch_expressions[expr] = None
            self.watch_entry.delete(0, tk.END)
            self.update_watch_display()
    
    def update_watch_display(self):
        self.watch_display.delete(1.0, tk.END)
        watch_text = "WATCH EXPRESSIONS:\n" + "=" * 100 + "\n\n"
        for expr in self.watch_expressions.keys():
            watch_text += f"{expr}: (monitoring)\n"
        self.watch_display.insert(1.0, watch_text)
    
    def view_memory(self):
        try:
            start_addr = int(self.mem_addr.get(), 16)
            self.mem_display.delete(1.0, tk.END)
            
            mem_text = f"Memory from 0x{start_addr:08X}:\n" + "=" * 150 + "\n\n"
            
            for row in range(16):
                addr = start_addr + (row * 16)
                if addr >= self.computer.memory_size:
                    break
                
                mem_text += f"{addr:08X}: "
                for col in range(16):
                    if addr + col < self.computer.memory_size:
                        mem_text += f"{self.computer.memory[addr + col]:02X} "
                mem_text += "\n"
            
            self.mem_display.insert(1.0, mem_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid address")
    
    def fill_memory(self):
        value = simpledialog.askinteger("Fill Memory", "Value (0-255):", minvalue=0, maxvalue=255)
        if value is not None:
            for i in range(self.computer.memory_size):
                self.computer.memory[i] = value
            messagebox.showinfo("Success", "Memory filled")
            self.view_memory()
    
    def clear_memory(self):
        self.computer.memory = [0] * self.computer.memory_size
        messagebox.showinfo("Success", "Memory cleared")
        self.view_memory()
    
    def refresh_settings(self):
        self.settings_display.delete(1.0, tk.END)
        settings_text = "SYSTEM CONFIGURATION:\n" + "=" * 150 + "\n\n"
        for key, value in self.settings.items():
            settings_text += f"{key:30} : {value}\n"
        self.settings_display.insert(1.0, settings_text)
    
    def reset_settings(self):
        self.settings = self.load_settings()
        self.refresh_settings()
    
    def step(self):
        if not self.computer.halted:
            self.computer.pc = (self.computer.pc + 1) % self.computer.memory_size
            self.update_display()
    
    def run(self):
        self.running = True
        self.paused = False
    
    def pause(self):
        self.running = False
        self.paused = True
    
    def reset(self):
        self.computer.reset()
        self.running = False
        self.paused = False
        self.update_display()
    
    def load_program(self):
        filename = filedialog.askopenfilename(
            title="Load Program",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'rb') as f:
                    data = f.read()
                    for i, byte in enumerate(data):
                        if i < self.computer.memory_size:
                            self.computer.memory[i] = byte
                    messagebox.showinfo("Success", f"Loaded {len(data)} bytes")
                    self.update_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")


def main():
    root = tk.Tk()
    app = UnifiedComputerSystem(root)
    
    def on_closing():
        app.save_settings()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
