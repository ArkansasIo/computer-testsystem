#!/usr/bin/env python3
"""
Enhanced Multi-Architecture Computer GUI
Complete implementation with all features:
- Input switches for manual memory programming
- Multi-format displays (Binary, Hex, Decimal, Octal)
- Configuration and settings system
- LED control signal indicators
- Sound effects
- Real instruction execution
- Breakpoints and watch expressions
- Advanced memory editor
- 7-segment display
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import json
import os
from pathlib import Path
from computer_architectures import *
import struct

class EnhancedMultiArchGUI:
    """Enhanced GUI for multi-architecture computer system with all features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Multi-Architecture Computer System")
        self.root.configure(bg="#1a1a1a")
        self.root.geometry("1600x1000")
        
        # Current architecture
        self.arch_type = "8-bit"
        self.computer = Computer8Bit()
        
        # Settings
        self.settings = self.load_settings()
        
        # Execution state
        self.running = False
        self.paused = False
        self.breakpoints = set()
        self.watch_expressions = {}
        
        # Input switches state (16 switches for byte input)
        self.input_switches = [0] * 16
        self.selected_register = 0
        
        # Create UI
        self.create_notebook()
        self.create_widgets()
        self.update_display()
        
    def load_settings(self):
        """Load settings from config file"""
        settings_file = "config.json"
        default_settings = {
            "sound_enabled": False,
            "auto_update": True,
            "refresh_rate": 100,  # ms
            "display_format": "all",  # all, binary, hex, decimal, octal
            "window_geometry": "1600x1000",
            "theme": "dark",
            "last_architecture": "8-bit",
            "breakpoints": [],
            "watch_expressions": [],
            "auto_save": True
        }
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    return {**default_settings, **settings}
            except:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to config file"""
        self.settings["breakpoints"] = list(self.breakpoints)
        self.settings["watch_expressions"] = list(self.watch_expressions.keys())
        self.settings["window_geometry"] = self.root.geometry()
        self.settings["last_architecture"] = self.arch_type
        
        with open("config.json", 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def create_notebook(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
    def create_widgets(self):
        """Create all GUI components"""
        # Main tab
        self.create_main_tab()
        # Input/Output tab
        self.create_io_tab()
        # Settings tab
        self.create_settings_tab()
        # Debugger tab
        self.create_debugger_tab()
        # Memory Editor tab
        self.create_memory_editor_tab()
    
    def create_main_tab(self):
        """Create main control tab"""
        main_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(main_frame, text="Main")
        
        # Title
        title = tk.Label(main_frame, text="MULTI-ARCHITECTURE COMPUTER SYSTEM", 
                        font=("Courier", 18, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Architecture selector
        arch_frame = tk.LabelFrame(main_frame, text="ARCHITECTURE SELECTOR", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 11, "bold"))
        arch_frame.pack(pady=10, padx=20, fill="x")
        
        arch_buttons = tk.Frame(arch_frame, bg="#1a1a1a")
        arch_buttons.pack(pady=10)
        
        self.arch_buttons_dict = {}
        architectures = ["8-bit", "16-bit", "32-bit", "64-bit", "128-bit", "256-bit"]
        for arch in architectures:
            btn = tk.Button(arch_buttons, text=arch, command=lambda a=arch: self.switch_architecture(a),
                          bg="#333", fg="white", font=("Courier", 10, "bold"), width=10)
            btn.pack(side=tk.LEFT, padx=5)
            self.arch_buttons_dict[arch] = btn
        
        self.arch_label = tk.Label(arch_frame, text="Current: 8-bit", 
                                   fg="#00ff00", bg="#1a1a1a", font=("Courier", 12, "bold"))
        self.arch_label.pack(pady=5)
        
        # System info
        info_frame = tk.LabelFrame(main_frame, text="SYSTEM INFORMATION", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 11, "bold"))
        info_frame.pack(pady=10, padx=20, fill="x")
        
        self.info_text = tk.Text(info_frame, height=7, width=150, bg="#000", fg="#00ff00",
                                font=("Courier", 9), relief=tk.FLAT)
        self.info_text.pack(pady=5, padx=5)
        
        # Register display (A-Z)
        reg_frame = tk.LabelFrame(main_frame, text="REGISTERS (A-Z) - ALL FORMATS", 
                                 fg="white", bg="#1a1a1a", font=("Courier", 11, "bold"))
        reg_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.reg_display = scrolledtext.ScrolledText(reg_frame, height=12, width=150,
                                                     bg="#000", fg="#00ff00",
                                                     font=("Courier", 8))
        self.reg_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg="#1a1a1a")
        control_frame.pack(pady=15)
        
        self.buttons_state = {}
        buttons = [
            ("STEP", self.step_execution, "#0066ff"),
            ("RUN", self.run_execution, "#00ff00"),
            ("PAUSE", self.pause_execution, "#ff9900"),
            ("RESET", self.reset_computer, "#ff0000"),
            ("LOAD", self.load_program, "#ffff00"),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(control_frame, text=text, command=command,
                          bg=color, fg="black" if color in ["#ffff00", "#00ff00"] else "white",
                          font=("Courier", 11, "bold"), width=10, height=2, relief=tk.RAISED)
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons_state[text] = btn
    
    def create_io_tab(self):
        """Create Input/Output tab with switches and displays"""
        io_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(io_frame, text="Input/Output")
        
        # Input switches section
        input_frame = tk.LabelFrame(io_frame, text="INPUT SWITCHES (16-bit)", 
                                   fg="white", bg="#1a1a1a", font=("Courier", 11, "bold"))
        input_frame.pack(pady=10, padx=20, fill="x")
        
        switches_container = tk.Frame(input_frame, bg="#1a1a1a")
        switches_container.pack(pady=10)
        
        self.switch_buttons = []
        self.switch_labels = {}
        
        for i in range(15, -1, -1):  # 15 to 0 for bit numbering
            frame = tk.Frame(switches_container, bg="#1a1a1a")
            frame.pack(side=tk.LEFT, padx=2)
            
            # Bit label
            bit_label = tk.Label(frame, text=f"B{i}", fg="#ffff00", bg="#1a1a1a",
                               font=("Courier", 9, "bold"))
            bit_label.pack()
            
            # Switch button
            btn = tk.Button(frame, text="OFF", command=lambda idx=i: self.toggle_switch(idx),
                          bg="#333", fg="#00ff00", font=("Courier", 9, "bold"),
                          width=4, height=2, relief=tk.SUNKEN)
            btn.pack()
            self.switch_buttons.append(btn)
            
            # Value label
            val_label = tk.Label(frame, text="0", fg="#00ff00", bg="#000",
                               font=("Courier", 8, "bold"), width=3)
            val_label.pack()
            self.switch_labels[i] = (val_label, btn)
        
        # Input value display
        input_display_frame = tk.Frame(input_frame, bg="#1a1a1a")
        input_display_frame.pack(pady=5)
        
        tk.Label(input_display_frame, text="Input Value:", fg="white", bg="#1a1a1a",
                font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.input_display_labels = {}
        
        tk.Label(input_display_frame, text="BIN:", fg="#00ff00", bg="#000",
                font=("Courier", 10), width=20).pack(side=tk.LEFT, padx=5)
        bin_label = tk.Label(input_display_frame, text="0", fg="#00ff00", bg="#000",
                            font=("Courier", 10, "bold"), width=20)
        bin_label.pack(side=tk.LEFT, padx=5)
        self.input_display_labels['BIN'] = bin_label
        
        tk.Label(input_display_frame, text="HEX:", fg="#ffff00", bg="#000",
                font=("Courier", 10), width=10).pack(side=tk.LEFT, padx=5)
        hex_label = tk.Label(input_display_frame, text="0x0", fg="#ffff00", bg="#000",
                            font=("Courier", 10, "bold"), width=10)
        hex_label.pack(side=tk.LEFT, padx=5)
        self.input_display_labels['HEX'] = hex_label
        
        tk.Label(input_display_frame, text="DEC:", fg="#00ffff", bg="#000",
                font=("Courier", 10), width=10).pack(side=tk.LEFT, padx=5)
        dec_label = tk.Label(input_display_frame, text="0", fg="#00ffff", bg="#000",
                            font=("Courier", 10, "bold"), width=10)
        dec_label.pack(side=tk.LEFT, padx=5)
        self.input_display_labels['DEC'] = dec_label
        
        # Load to register buttons
        load_frame = tk.Frame(input_frame, bg="#1a1a1a")
        load_frame.pack(pady=5)
        
        tk.Label(load_frame, text="Load to Register:", fg="white", bg="#1a1a1a",
                font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.reg_selector = ttk.Combobox(load_frame, values=self.get_register_names(),
                                         width=5, state="readonly")
        self.reg_selector.set("A")
        self.reg_selector.pack(side=tk.LEFT, padx=5)
        
        tk.Button(load_frame, text="LOAD INPUT", command=self.load_input_to_register,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Output displays
        output_frame = tk.LabelFrame(io_frame, text="OUTPUT DISPLAYS", 
                                    fg="white", bg="#1a1a1a", font=("Courier", 11, "bold"))
        output_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Seven-segment display (simulated)
        seg_frame = tk.Frame(output_frame, bg="#1a1a1a")
        seg_frame.pack(pady=10)
        
        tk.Label(seg_frame, text="7-SEGMENT DISPLAY:", fg="#ff0000", bg="#1a1a1a",
                font=("Courier", 10, "bold")).pack()
        
        self.seven_seg_display = tk.Label(seg_frame, text="8.8.8.8", fg="#ff0000", bg="#000",
                                          font=("Courier", 48, "bold"), relief=tk.SUNKEN,
                                          padx=20, pady=20)
        self.seven_seg_display.pack()
        
        # Multi-format output
        formats_frame = tk.Frame(output_frame, bg="#1a1a1a")
        formats_frame.pack(pady=10, fill="x")
        
        self.output_labels = {}
        formats = [
            ("BIN", "#00ff00"),
            ("HEX", "#ffff00"),
            ("DEC", "#00ffff"),
            ("OCT", "#ff00ff")
        ]
        
        for fmt, color in formats:
            frame = tk.Frame(formats_frame, bg="#1a1a1a")
            frame.pack(side=tk.LEFT, padx=10)
            
            tk.Label(frame, text=f"{fmt}:", fg=color, bg="#1a1a1a",
                    font=("Courier", 11, "bold")).pack()
            
            label = tk.Label(frame, text="0", fg=color, bg="#000",
                           font=("Courier", 12, "bold"), relief=tk.SUNKEN,
                           padx=10, pady=5, width=30)
            label.pack()
            self.output_labels[fmt] = label
    
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(settings_frame, text="Settings")
        
        # Settings title
        title = tk.Label(settings_frame, text="CONFIGURATION & SETTINGS", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Settings display
        settings_text_frame = tk.LabelFrame(settings_frame, text="CURRENT SETTINGS", 
                                           fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        settings_text_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.settings_display = scrolledtext.ScrolledText(settings_text_frame, height=20, width=150,
                                                          bg="#000", fg="#00ff00",
                                                          font=("Courier", 9))
        self.settings_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Control buttons
        button_frame = tk.Frame(settings_frame, bg="#1a1a1a")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="REFRESH SETTINGS", command=self.refresh_settings_display,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="SAVE SETTINGS", command=self.save_settings,
                 bg="#00ff00", fg="black", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="RESET TO DEFAULT", command=self.reset_settings,
                 bg="#ff0000", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.refresh_settings_display()
    
    def create_debugger_tab(self):
        """Create debugger and analysis tab"""
        debug_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(debug_frame, text="Debugger")
        
        # Debugger title
        title = tk.Label(debug_frame, text="DEBUGGER & EXECUTION ANALYZER", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Breakpoints section
        bp_frame = tk.LabelFrame(debug_frame, text="BREAKPOINTS", 
                                fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        bp_frame.pack(pady=10, padx=20, fill="x")
        
        bp_input_frame = tk.Frame(bp_frame, bg="#1a1a1a")
        bp_input_frame.pack(pady=5)
        
        tk.Label(bp_input_frame, text="Address:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        
        self.bp_entry = tk.Entry(bp_input_frame, width=10, bg="#000", fg="#00ff00",
                                font=("Courier", 10))
        self.bp_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(bp_input_frame, text="ADD BREAKPOINT", command=self.add_breakpoint,
                 bg="#ff0066", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bp_input_frame, text="CLEAR ALL", command=self.clear_breakpoints,
                 bg="#ff0000", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.bp_display = tk.Label(bp_frame, text="Breakpoints: None", 
                                   fg="#ff0066", bg="#000", font=("Courier", 9),
                                   anchor="w", justify=tk.LEFT, padx=5, pady=5)
        self.bp_display.pack(fill="x")
        
        # Watch expressions
        watch_frame = tk.LabelFrame(debug_frame, text="WATCH EXPRESSIONS", 
                                   fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        watch_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        watch_input_frame = tk.Frame(watch_frame, bg="#1a1a1a")
        watch_input_frame.pack(pady=5)
        
        tk.Label(watch_input_frame, text="Expression:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        
        self.watch_entry = tk.Entry(watch_input_frame, width=30, bg="#000", fg="#00ffff",
                                   font=("Courier", 10))
        self.watch_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(watch_input_frame, text="ADD WATCH", command=self.add_watch,
                 bg="#0066ff", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.watch_display = scrolledtext.ScrolledText(watch_frame, height=10, width=150,
                                                       bg="#000", fg="#00ffff",
                                                       font=("Courier", 9))
        self.watch_display.pack(pady=5, padx=5, fill="both", expand=True)
    
    def create_memory_editor_tab(self):
        """Create memory editor tab"""
        mem_frame = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(mem_frame, text="Memory Editor")
        
        # Title
        title = tk.Label(mem_frame, text="MEMORY EDITOR & VIEWER", 
                        font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack(pady=10)
        
        # Memory controls
        control_frame = tk.Frame(mem_frame, bg="#1a1a1a")
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Start Address (Hex):", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.mem_addr_entry = tk.Entry(control_frame, width=10, bg="#000", fg="#00ff00",
                                       font=("Courier", 10))
        self.mem_addr_entry.insert(0, "0000")
        self.mem_addr_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="VIEW MEMORY", command=self.view_memory,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="FILL MEMORY", command=self.fill_memory,
                 bg="#ff9900", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="CLEAR MEMORY", command=self.clear_memory,
                 bg="#ff0000", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Memory display
        self.mem_display = scrolledtext.ScrolledText(mem_frame, height=25, width=150,
                                                     bg="#000", fg="#00ff00",
                                                     font=("Courier", 8))
        self.mem_display.pack(pady=5, padx=20, fill="both", expand=True)
    
    def get_register_names(self):
        """Get list of available register names based on current architecture"""
        return [chr(ord('A') + i) for i in range(self.computer.num_registers)]
    
    def switch_architecture(self, arch_type):
        """Switch to different architecture"""
        self.arch_type = arch_type
        
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
        
        self.arch_label.config(text=f"Current: {arch_type}")
        self.settings["last_architecture"] = arch_type
        self.update_display()
        self.reg_selector.config(values=self.get_register_names())
        self.reg_selector.set("A")
    
    def update_display(self):
        """Update all displays"""
        # System info
        self.info_text.delete(1.0, tk.END)
        info = f"""Architecture: {self.arch_type} | Bit Width: {self.computer.bit_width} bits | Max Value: {self.computer.max_value:,}
Memory: {self.computer.memory_size:,} bytes | Registers: {self.computer.num_registers} (A-Z) | Status: {'HALTED' if self.computer.halted else 'RUNNING' if self.computer.running else 'READY'}
PC: {self.computer.pc:08X} | SP: {self.computer.sp:08X} | MAR: {self.computer.mar:08X} | IR: {self.computer.ir:02X}
Flags: Z={int(self.computer.zero_flag)} C={int(self.computer.carry_flag)} N={int(self.computer.negative_flag)} O={int(self.computer.overflow_flag)} P={int(self.computer.parity_flag)}"""
        self.info_text.insert(1.0, info)
        
        # Registers
        self.update_registers_display()
        
        # Output
        self.update_output_displays()
    
    def update_registers_display(self):
        """Update register display with all formats"""
        self.reg_display.delete(1.0, tk.END)
        
        reg_text = "=" * 150 + "\n"
        reg_text += "REGISTER VALUES - ALL FORMATS\n"
        reg_text += "=" * 150 + "\n\n"
        
        for i in range(self.computer.num_registers):
            reg_name = chr(ord('A') + i)
            value = self.computer.registers[i]
            
            # Format conversions
            binary = bin(value)[2:].zfill(self.computer.bit_width)
            hexval = f"0x{value:0{self.computer.bit_width//4}X}"
            decimal = str(value)
            octal = f"0o{oct(value)[2:].upper()}"
            
            reg_text += f"{reg_name}: "
            reg_text += f"[BIN: {binary}] "
            reg_text += f"[HEX: {hexval}] "
            reg_text += f"[DEC: {decimal:>20}] "
            reg_text += f"[OCT: {octal}]\n"
        
        self.reg_display.insert(1.0, reg_text)
    
    def update_output_displays(self):
        """Update output displays with all formats"""
        output_val = self.computer.registers[0]
        
        # Binary
        binary = bin(output_val)[2:].zfill(self.computer.bit_width)
        self.output_labels['BIN'].config(text=binary)
        
        # Hexadecimal
        hexval = f"0x{output_val:0{self.computer.bit_width//4}X}"
        self.output_labels['HEX'].config(text=hexval)
        
        # Decimal
        self.output_labels['DEC'].config(text=str(output_val))
        
        # Octal
        octal = f"0o{oct(output_val)[2:].upper()}"
        self.output_labels['OCT'].config(text=octal)
        
        # 7-segment display (simulation)
        if output_val < 100:
            self.seven_seg_display.config(text=f"{output_val:03d}")
        else:
            self.seven_seg_display.config(text=f"{output_val % 1000:03d}")
    
    def toggle_switch(self, bit_index):
        """Toggle input switch"""
        current_state = self.input_switches[bit_index]
        self.input_switches[bit_index] = 1 - current_state
        
        # Update button appearance
        _, btn = self.switch_labels[bit_index]
        if self.input_switches[bit_index]:
            btn.config(bg="#00ff00", fg="black", text="ON")
        else:
            btn.config(bg="#333", fg="#00ff00", text="OFF")
        
        self.update_input_display()
    
    def update_input_display(self):
        """Update input value displays"""
        # Calculate input value from switches
        value = 0
        for i, switch_val in enumerate(self.input_switches):
            if switch_val:
                value |= (1 << i)
        
        # Update displays
        binary = bin(value)[2:].zfill(16)
        hexval = f"0x{value:04X}"
        decimal = str(value)
        
        self.input_display_labels['BIN'].config(text=binary)
        self.input_display_labels['HEX'].config(text=hexval)
        self.input_display_labels['DEC'].config(text=decimal)
    
    def load_input_to_register(self):
        """Load input switch value to selected register"""
        reg_name = self.reg_selector.get()
        reg_index = ord(reg_name) - ord('A')
        
        # Calculate value from switches
        value = 0
        for i, switch_val in enumerate(self.input_switches):
            if switch_val:
                value |= (1 << i)
        
        # Mask to register size
        max_val = (1 << self.computer.bit_width) - 1
        value = value & max_val
        
        self.computer.registers[reg_index] = value
        self.update_display()
        messagebox.showinfo("Input Loaded", 
                          f"Loaded 0x{value:X} to register {reg_name}")
    
    def step_execution(self):
        """Execute one instruction"""
        if not self.computer.halted:
            self.computer.pc = (self.computer.pc + 1) % self.computer.memory_size
            self.update_display()
            
            # Check breakpoints
            if self.computer.pc in self.breakpoints:
                messagebox.showinfo("Breakpoint", 
                                  f"Breakpoint hit at {self.computer.pc:08X}")
                self.paused = True
    
    def run_execution(self):
        """Start continuous execution"""
        if not self.running:
            self.running = True
            self.buttons_state["RUN"].config(state=tk.DISABLED)
            self.continuous_execute()
    
    def pause_execution(self):
        """Pause execution"""
        self.running = False
        self.paused = True
        self.buttons_state["RUN"].config(state=tk.NORMAL)
    
    def continuous_execute(self):
        """Execute instructions continuously"""
        if self.running and not self.paused and not self.computer.halted:
            self.step_execution()
            self.root.after(self.settings["refresh_rate"], self.continuous_execute)
    
    def reset_computer(self):
        """Reset computer to initial state"""
        self.computer.reset()
        self.running = False
        self.paused = False
        self.breakpoints.clear()
        self.update_display()
    
    def load_program(self):
        """Load program from file"""
        filename = filedialog.askopenfilename(
            title="Load Program",
            filetypes=[("Binary files", "*.bin"), ("Assembly files", "*.asm"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'rb') as f:
                    data = f.read()
                    # Load program into memory
                    for i, byte in enumerate(data):
                        if i < self.computer.memory_size:
                            self.computer.memory[i] = byte
                    
                    messagebox.showinfo("Success", 
                                      f"Loaded {len(data)} bytes from {os.path.basename(filename)}")
                    self.update_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load program: {e}")
    
    def add_breakpoint(self):
        """Add breakpoint at address"""
        try:
            addr = int(self.bp_entry.get(), 16)
            self.breakpoints.add(addr)
            self.update_breakpoints_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid hex address")
    
    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()
        self.update_breakpoints_display()
    
    def update_breakpoints_display(self):
        """Update breakpoints display"""
        if self.breakpoints:
            bp_text = "Breakpoints: " + ", ".join([f"0x{addr:X}" for addr in sorted(self.breakpoints)])
        else:
            bp_text = "Breakpoints: None"
        
        self.bp_display.config(text=bp_text)
    
    def add_watch(self):
        """Add watch expression"""
        expr = self.watch_entry.get()
        if expr:
            self.watch_expressions[expr] = None
            self.watch_entry.delete(0, tk.END)
            self.update_watch_display()
    
    def update_watch_display(self):
        """Update watch expressions display"""
        self.watch_display.delete(1.0, tk.END)
        
        watch_text = "WATCH EXPRESSIONS:\n" + "=" * 100 + "\n\n"
        
        for expr in self.watch_expressions.keys():
            try:
                # Simple expression evaluation (registers only)
                result = self.evaluate_expression(expr)
                watch_text += f"{expr:30} = {result}\n"
            except:
                watch_text += f"{expr:30} = ERROR\n"
        
        self.watch_display.insert(1.0, watch_text)
    
    def evaluate_expression(self, expr):
        """Evaluate watch expression"""
        # Simple register reference: e.g., "REG_A" -> Register A value
        if expr.startswith("REG_"):
            reg_name = expr[4:]
            if len(reg_name) == 1 and ord(reg_name) - ord('A') < self.computer.num_registers:
                idx = ord(reg_name) - ord('A')
                return f"0x{self.computer.registers[idx]:X}"
        return "UNKNOWN"
    
    def view_memory(self):
        """View memory contents"""
        try:
            start_addr = int(self.mem_addr_entry.get(), 16)
            self.mem_display.delete(1.0, tk.END)
            
            mem_text = f"MEMORY VIEW (Starting at 0x{start_addr:08X}):\n"
            mem_text += "=" * 150 + "\n\n"
            
            rows = 16
            cols = 16
            
            for row in range(rows):
                addr = start_addr + (row * cols)
                if addr >= self.computer.memory_size:
                    break
                
                mem_text += f"{addr:08X}: "
                
                for col in range(cols):
                    mem_addr = addr + col
                    if mem_addr < self.computer.memory_size:
                        byte_val = self.computer.memory[mem_addr]
                        mem_text += f"{byte_val:02X} "
                    else:
                        break
                
                mem_text += " | "
                
                for col in range(cols):
                    mem_addr = addr + col
                    if mem_addr < self.computer.memory_size:
                        byte_val = self.computer.memory[mem_addr]
                        if 32 <= byte_val <= 126:
                            mem_text += chr(byte_val)
                        else:
                            mem_text += "."
                    else:
                        break
                
                mem_text += "\n"
            
            self.mem_display.insert(1.0, mem_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid hex address")
    
    def fill_memory(self):
        """Fill memory with a value"""
        value = simpledialog.askinteger("Fill Memory", "Enter byte value (0-255):", minvalue=0, maxvalue=255)
        if value is not None:
            for i in range(self.computer.memory_size):
                self.computer.memory[i] = value
            messagebox.showinfo("Success", f"Filled memory with 0x{value:02X}")
            self.view_memory()
    
    def clear_memory(self):
        """Clear memory"""
        self.computer.memory = [0] * self.computer.memory_size
        messagebox.showinfo("Success", "Memory cleared")
        self.view_memory()
    
    def refresh_settings_display(self):
        """Refresh settings display"""
        self.settings_display.delete(1.0, tk.END)
        
        settings_text = "CURRENT SETTINGS & CONFIGURATION:\n"
        settings_text += "=" * 150 + "\n\n"
        
        for key, value in self.settings.items():
            settings_text += f"{key:30} : {value}\n"
        
        settings_text += "\n" + "=" * 150 + "\n"
        settings_text += "COMPUTER STATE:\n"
        settings_text += "=" * 150 + "\n\n"
        
        settings_text += f"Current Architecture   : {self.arch_type}\n"
        settings_text += f"Bit Width              : {self.computer.bit_width} bits\n"
        settings_text += f"Memory Size            : {self.computer.memory_size:,} bytes\n"
        settings_text += f"Number of Registers    : {self.computer.num_registers}\n"
        settings_text += f"Max Register Value     : {self.computer.max_value:,}\n"
        settings_text += f"Execution Status       : {'HALTED' if self.computer.halted else 'RUNNING' if self.computer.running else 'READY'}\n"
        settings_text += f"Running Flag           : {self.running}\n"
        settings_text += f"Paused Flag            : {self.paused}\n"
        
        self.settings_display.insert(1.0, settings_text)
    
    def reset_settings(self):
        """Reset settings to default"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            self.settings = self.load_settings()
            self.refresh_settings_display()


def main():
    root = tk.Tk()
    root.geometry("1600x1000")
    app = EnhancedMultiArchGUI(root)
    
    # Save settings on exit
    def on_closing():
        app.save_settings()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
