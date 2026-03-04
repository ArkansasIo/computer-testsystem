#!/usr/bin/env python3
"""
Complete 8-bit Computer GUI with ALL Features
- Individual LED components for bus, registers, PC, MAR, IR
- LCD-style displays with proper formatting
- Interactive toggle switches for memory programming
- Control signal LEDs (MI, RI, RO, II, IO, AI, AO, EO, SU, BI, OI, CE, CO, J, FI)
- Instruction decode display
- Step-by-step execution with visual feedback
- Clock module visualization
- Sound effects integrated with visual changes
- Multi-format displays (Binary, Hex, Decimal, Octal)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

# Try to import sound playback
try:
    import pyaudio
    import wave
    import io
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

from sound_effects import SoundEffects


class LED:
    """Individual LED component"""
    def __init__(self, parent, label="", color="red", size=15):
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        if label:
            self.label = tk.Label(self.frame, text=label, fg="white", bg="#1a1a1a",
                                 font=("Courier", 7))
            self.label.pack()
        
        self.canvas = tk.Canvas(self.frame, width=size, height=size,
                               bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()
        
        self.color = color
        self.off_color = "#0a0a0a"
        self.state = False
        
        self.circle = self.canvas.create_oval(2, 2, size-2, size-2,
                                              fill=self.off_color,
                                              outline="#333")
        
    def set_state(self, state):
        """Set LED on/off"""
        self.state = state
        color = self.color if state else self.off_color
        self.canvas.itemconfig(self.circle, fill=color)
        if state:
            # Add glow effect
            self.canvas.itemconfig(self.circle, outline=self.color)
        else:
            self.canvas.itemconfig(self.circle, outline="#333")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class Switch:
    """Toggle switch component"""
    def __init__(self, parent, label="", callback=None):
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        if label:
            self.label = tk.Label(self.frame, text=label, fg="white", bg="#1a1a1a",
                                 font=("Courier", 7))
            self.label.pack()
        
        self.state = False
        self.callback = callback
        
        self.button = tk.Button(self.frame, text="0", width=2, height=1,
                               bg="#222", fg="#666", font=("Courier", 10, "bold"),
                               command=self.toggle, relief=tk.RAISED)
        self.button.pack()
    
    def toggle(self):
        """Toggle switch state"""
        self.state = not self.state
        self.button.config(
            text="1" if self.state else "0",
            bg="#00ff00" if self.state else "#222",
            fg="black" if self.state else "#666",
            relief=tk.SUNKEN if self.state else tk.RAISED
        )
        if self.callback:
            self.callback(self.state)
    
    def set_state(self, state):
        """Set switch state programmatically"""
        self.state = state
        self.button.config(
            text="1" if state else "0",
            bg="#00ff00" if state else "#222",
            fg="black" if state else "#666",
            relief=tk.SUNKEN if state else tk.RAISED
        )
    
    def get_state(self):
        return self.state
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class LCDDisplay:
    """LCD-style display panel"""
    def __init__(self, parent, label="", width=20, height=2):
        self.frame = tk.LabelFrame(parent, text=label, fg="#00ff00", bg="#1a1a1a",
                                  font=("Courier", 9, "bold"))
        
        self.text = tk.Text(self.frame, width=width, height=height,
                           bg="#0a3d0a", fg="#00ff00", font=("Courier", 10, "bold"),
                           relief=tk.SUNKEN, borderwidth=2)
        self.text.pack(padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
    
    def set_text(self, text):
        """Update LCD text"""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, text)
        self.text.config(state=tk.DISABLED)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class SevenSegmentDisplay:
    """7-segment LED display"""
    def __init__(self, parent, size=1.0):
        w, h = int(120 * size), int(180 * size)
        self.canvas = tk.Canvas(parent, width=w, height=h,
                               bg="#0a0a0a", highlightthickness=2,
                               highlightbackground="#333")
        
        # Segment positions scaled
        s = size
        self.segments = {
            'a': [(20*s, 10*s), (100*s, 10*s), (90*s, 20*s), (30*s, 20*s)],
            'b': [(100*s, 10*s), (110*s, 20*s), (110*s, 80*s), (100*s, 90*s)],
            'c': [(100*s, 90*s), (110*s, 100*s), (110*s, 160*s), (100*s, 170*s)],
            'd': [(20*s, 170*s), (100*s, 170*s), (90*s, 160*s), (30*s, 160*s)],
            'e': [(10*s, 100*s), (20*s, 90*s), (20*s, 160*s), (10*s, 170*s)],
            'f': [(10*s, 20*s), (20*s, 10*s), (20*s, 80*s), (10*s, 90*s)],
            'g': [(20*s, 90*s), (100*s, 90*s), (90*s, 80*s), (30*s, 80*s)]
        }
        
        self.segment_ids = {}
        for name, coords in self.segments.items():
            seg_id = self.canvas.create_polygon(coords, fill="#1a0000",
                                               outline="#333")
            self.segment_ids[name] = seg_id
        
        # Digit patterns
        self.patterns = {
            0: ['a', 'b', 'c', 'd', 'e', 'f'],
            1: ['b', 'c'],
            2: ['a', 'b', 'd', 'e', 'g'],
            3: ['a', 'b', 'c', 'd', 'g'],
            4: ['b', 'c', 'f', 'g'],
            5: ['a', 'c', 'd', 'f', 'g'],
            6: ['a', 'c', 'd', 'e', 'f', 'g'],
            7: ['a', 'b', 'c'],
            8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            9: ['a', 'b', 'c', 'd', 'f', 'g']
        }
    
    def display_digit(self, digit):
        """Display a digit (0-9)"""
        for seg_id in self.segment_ids.values():
            self.canvas.itemconfig(seg_id, fill="#1a0000")
        
        if digit in self.patterns:
            for seg_name in self.patterns[digit]:
                self.canvas.itemconfig(self.segment_ids[seg_name], fill="#ff0000")
    
    def display_number(self, number):
        """Display number (last digit)"""
        digit = number % 10
        self.display_digit(digit)
    
    def clear(self):
        """Clear display"""
        for seg_id in self.segment_ids.values():
            self.canvas.itemconfig(seg_id, fill="#1a0000")



class AudioPlayer:
    """Audio player for sound effects"""
    def __init__(self):
        self.enabled = AUDIO_AVAILABLE
        if self.enabled:
            try:
                self.pyaudio = pyaudio.PyAudio()
            except:
                self.enabled = False
        self.sfx = SoundEffects()
    
    def play_sound(self, samples):
        """Play sound from samples"""
        if not self.enabled:
            return
        
        try:
            wav_data = self.sfx.get_wav_data(samples)
            
            def play():
                try:
                    wf = wave.open(io.BytesIO(wav_data), 'rb')
                    stream = self.pyaudio.open(
                        format=self.pyaudio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True
                    )
                    
                    data = wf.readframes(1024)
                    while data:
                        stream.write(data)
                        data = wf.readframes(1024)
                    
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
            
            thread = threading.Thread(target=play, daemon=True)
            thread.start()
        except:
            pass
    
    def play_read(self):
        self.play_sound(self.sfx.generate_read_sound())
    
    def play_write(self):
        self.play_sound(self.sfx.generate_write_sound())
    
    def play_click(self):
        self.play_sound(self.sfx.generate_click())
    
    def play_pong(self):
        self.play_sound(self.sfx.generate_pong_sound())


class Computer:
    """8-bit computer with control signals"""
    def __init__(self):
        self.memory = [0] * 16
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.bus = 0
        self.carry_flag = False
        self.zero_flag = False
        self.halted = False
        
        # Control signals
        self.control_signals = {
            'MI': False,  # Memory address in
            'RI': False,  # RAM in
            'RO': False,  # RAM out
            'II': False,  # Instruction in
            'IO': False,  # Instruction out
            'AI': False,  # A register in
            'AO': False,  # A register out
            'EO': False,  # ALU out
            'SU': False,  # Subtract
            'BI': False,  # B register in
            'OI': False,  # Output in
            'CE': False,  # Counter enable
            'CO': False,  # Counter out
            'J':  False,  # Jump
            'FI': False   # Flags in
        }
    
    def reset(self):
        """Reset computer"""
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.bus = 0
        self.carry_flag = False
        self.zero_flag = False
        self.halted = False
        self.clear_control_signals()
    
    def clear_control_signals(self):
        """Clear all control signals"""
        for key in self.control_signals:
            self.control_signals[key] = False
    
    def load_program(self, program):
        """Load program into memory"""
        for addr, value in program.items():
            if 0 <= addr < 16:
                self.memory[addr] = value & 0xFF
    
    def step(self):
        """Execute one instruction with control signals"""
        if self.halted:
            return False
        
        self.clear_control_signals()
        
        # Fetch cycle
        # T1: PC -> MAR
        self.control_signals['CO'] = True
        self.control_signals['MI'] = True
        self.bus = self.pc
        self.mar = self.pc
        
        # T2: RAM -> IR, PC++
        self.control_signals['RO'] = True
        self.control_signals['II'] = True
        self.control_signals['CE'] = True
        self.bus = self.memory[self.mar]
        self.ir = self.bus
        self.pc = (self.pc + 1) & 0x0F
        
        # Decode and Execute
        opcode = (self.ir >> 4) & 0x0F
        operand = self.ir & 0x0F
        
        if opcode == 0x0:  # NOP
            pass
        elif opcode == 0x1:  # LDA
            self.control_signals['IO'] = True
            self.control_signals['MI'] = True
            self.mar = operand
            self.control_signals['RO'] = True
            self.control_signals['AI'] = True
            self.bus = self.memory[self.mar]
            self.reg_a = self.bus
        elif opcode == 0x2:  # ADD
            self.control_signals['IO'] = True
            self.control_signals['MI'] = True
            self.mar = operand
            self.control_signals['RO'] = True
            self.control_signals['BI'] = True
            self.reg_b = self.memory[self.mar]
            self.control_signals['EO'] = True
            self.control_signals['AI'] = True
            self.control_signals['FI'] = True
            result = self.reg_a + self.reg_b
            self.carry_flag = result > 255
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
            self.bus = self.reg_a
        elif opcode == 0x3:  # SUB
            self.control_signals['IO'] = True
            self.control_signals['MI'] = True
            self.mar = operand
            self.control_signals['RO'] = True
            self.control_signals['BI'] = True
            self.reg_b = self.memory[self.mar]
            self.control_signals['SU'] = True
            self.control_signals['EO'] = True
            self.control_signals['AI'] = True
            self.control_signals['FI'] = True
            result = self.reg_a - self.reg_b
            self.carry_flag = result >= 0
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
            self.bus = self.reg_a
        elif opcode == 0x4:  # STA
            self.control_signals['IO'] = True
            self.control_signals['MI'] = True
            self.mar = operand
            self.control_signals['AO'] = True
            self.control_signals['RI'] = True
            self.bus = self.reg_a
            self.memory[self.mar] = self.reg_a
        elif opcode == 0x5:  # LDI
            self.control_signals['IO'] = True
            self.control_signals['AI'] = True
            self.bus = operand
            self.reg_a = operand
        elif opcode == 0x6:  # JMP
            self.control_signals['IO'] = True
            self.control_signals['J'] = True
            self.pc = operand
        elif opcode == 0x7:  # JC
            if self.carry_flag:
                self.control_signals['IO'] = True
                self.control_signals['J'] = True
                self.pc = operand
        elif opcode == 0x8:  # JZ
            if self.zero_flag:
                self.control_signals['IO'] = True
                self.control_signals['J'] = True
                self.pc = operand
        elif opcode == 0xE:  # OUT
            self.control_signals['AO'] = True
            self.control_signals['OI'] = True
            self.bus = self.reg_a
        elif opcode == 0xF:  # HLT
            self.halted = True
            return False
        
        return True


class CompleteComputerGUI:
    """Complete GUI with all features"""
    def __init__(self, root):
        self.root = root
        self.root.title("Complete 8-bit Computer - All Features")
        self.root.configure(bg="#0a0a0a")
        
        self.computer = Computer()
        self.audio = AudioPlayer()
        self.sound_enabled = True
        self.clock_speed = 1.0
        self.auto_clock = False
        
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        """Create all GUI components"""
        # Main container with scrollbar
        canvas = tk.Canvas(self.root, bg="#0a0a0a")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = scrollable_frame
        
        # === TITLE ===
        title = tk.Label(main_frame, text="8-BIT COMPUTER - COMPLETE SYSTEM",
                        font=("Courier", 20, "bold"), fg="#00ff00", bg="#0a0a0a")
        title.pack(pady=10)
        
        # === TOP ROW: CONTROL SIGNALS ===
        control_frame = tk.LabelFrame(main_frame, text="CONTROL SIGNALS",
                                     fg="#ffff00", bg="#0a0a0a",
                                     font=("Courier", 12, "bold"))
        control_frame.pack(pady=10, padx=10, fill="x")
        
        signals_container = tk.Frame(control_frame, bg="#0a0a0a")
        signals_container.pack(pady=10)
        
        self.control_leds = {}
        signal_names = ['MI', 'RI', 'RO', 'II', 'IO', 'AI', 'AO', 'EO',
                       'SU', 'BI', 'OI', 'CE', 'CO', 'J', 'FI']
        
        for i, name in enumerate(signal_names):
            led = LED(signals_container, label=name, color="#ffff00", size=12)
            led.grid(row=0, column=i, padx=3)
            self.control_leds[name] = led
        
        # === BUS DISPLAY ===
        bus_frame = tk.LabelFrame(main_frame, text="8-BIT BUS",
                                 fg="#00ff00", bg="#0a0a0a",
                                 font=("Courier", 12, "bold"))
        bus_frame.pack(pady=10, padx=10, fill="x")
        
        bus_container = tk.Frame(bus_frame, bg="#0a0a0a")
        bus_container.pack(pady=10)
        
        self.bus_leds = []
        for i in range(7, -1, -1):
            led = LED(bus_container, label=f"B{i}", color="#00ff00", size=18)
            led.pack(side=tk.LEFT, padx=4)
            self.bus_leds.insert(0, led)
        
        # Bus value display
        self.bus_lcd = LCDDisplay(bus_frame, "BUS VALUE", width=30, height=1)
        self.bus_lcd.pack(pady=5)
        
        # === REGISTERS ROW ===
        reg_row = tk.Frame(main_frame, bg="#0a0a0a")
        reg_row.pack(pady=10, fill="x")
        
        # Register A
        reg_a_frame = tk.LabelFrame(reg_row, text="REGISTER A",
                                   fg="#ff0000", bg="#0a0a0a",
                                   font=("Courier", 11, "bold"))
        reg_a_frame.pack(side=tk.LEFT, padx=10, expand=True, fill="both")
        
        a_leds = tk.Frame(reg_a_frame, bg="#0a0a0a")
        a_leds.pack(pady=5)
        
        self.reg_a_leds = []
        for i in range(7, -1, -1):
            led = LED(a_leds, label=f"{i}", color="#ff0000", size=15)
            led.pack(side=tk.LEFT, padx=2)
            self.reg_a_leds.insert(0, led)
        
        self.reg_a_lcd = LCDDisplay(reg_a_frame, "", width=25, height=2)
        self.reg_a_lcd.pack(pady=5)
        
        # Register B
        reg_b_frame = tk.LabelFrame(reg_row, text="REGISTER B",
                                   fg="#ff0000", bg="#0a0a0a",
                                   font=("Courier", 11, "bold"))
        reg_b_frame.pack(side=tk.LEFT, padx=10, expand=True, fill="both")
        
        b_leds = tk.Frame(reg_b_frame, bg="#0a0a0a")
        b_leds.pack(pady=5)
        
        self.reg_b_leds = []
        for i in range(7, -1, -1):
            led = LED(b_leds, label=f"{i}", color="#ff0000", size=15)
            led.pack(side=tk.LEFT, padx=2)
            self.reg_b_leds.insert(0, led)
        
        self.reg_b_lcd = LCDDisplay(reg_b_frame, "", width=25, height=2)
        self.reg_b_lcd.pack(pady=5)
        
        # === PROGRAM COUNTER & INSTRUCTION ===
        pc_ir_row = tk.Frame(main_frame, bg="#0a0a0a")
        pc_ir_row.pack(pady=10, fill="x")
        
        # Program Counter
        pc_frame = tk.LabelFrame(pc_ir_row, text="PROGRAM COUNTER",
                                fg="#ffff00", bg="#0a0a0a",
                                font=("Courier", 11, "bold"))
        pc_frame.pack(side=tk.LEFT, padx=10, expand=True, fill="both")
        
        pc_leds = tk.Frame(pc_frame, bg="#0a0a0a")
        pc_leds.pack(pady=5)
        
        self.pc_leds = []
        for i in range(3, -1, -1):
            led = LED(pc_leds, label=f"{i}", color="#ffff00", size=15)
            led.pack(side=tk.LEFT, padx=3)
            self.pc_leds.insert(0, led)
        
        self.pc_lcd = LCDDisplay(pc_frame, "", width=20, height=1)
        self.pc_lcd.pack(pady=5)
        
        # Instruction Register
        ir_frame = tk.LabelFrame(pc_ir_row, text="INSTRUCTION REGISTER",
                                fg="#00ffff", bg="#0a0a0a",
                                font=("Courier", 11, "bold"))
        ir_frame.pack(side=tk.LEFT, padx=10, expand=True, fill="both")
        
        ir_leds = tk.Frame(ir_frame, bg="#0a0a0a")
        ir_leds.pack(pady=5)
        
        self.ir_leds = []
        for i in range(7, -1, -1):
            led = LED(ir_leds, label=f"{i}", color="#00ffff", size=15)
            led.pack(side=tk.LEFT, padx=2)
            self.ir_leds.insert(0, led)
        
        self.ir_lcd = LCDDisplay(ir_frame, "", width=25, height=2)
        self.ir_lcd.pack(pady=5)
        
        # === MEMORY ADDRESS REGISTER ===
        mar_frame = tk.LabelFrame(main_frame, text="MEMORY ADDRESS REGISTER (MAR)",
                                 fg="#ff00ff", bg="#0a0a0a",
                                 font=("Courier", 11, "bold"))
        mar_frame.pack(pady=10, padx=10, fill="x")
        
        mar_leds = tk.Frame(mar_frame, bg="#0a0a0a")
        mar_leds.pack(pady=5)
        
        self.mar_leds = []
        for i in range(3, -1, -1):
            led = LED(mar_leds, label=f"{i}", color="#ff00ff", size=15)
            led.pack(side=tk.LEFT, padx=3)
            self.mar_leds.insert(0, led)
        
        self.mar_lcd = LCDDisplay(mar_frame, "", width=20, height=1)
        self.mar_lcd.pack(pady=5)
        
        # === FLAGS ===
        flag_frame = tk.LabelFrame(main_frame, text="FLAGS",
                                  fg="white", bg="#0a0a0a",
                                  font=("Courier", 11, "bold"))
        flag_frame.pack(pady=10, padx=10, fill="x")
        
        flag_container = tk.Frame(flag_frame, bg="#0a0a0a")
        flag_container.pack(pady=10)
        
        self.carry_led = LED(flag_container, label="CARRY", color="#ff00ff", size=20)
        self.carry_led.pack(side=tk.LEFT, padx=20)
        
        self.zero_led = LED(flag_container, label="ZERO", color="#00ffff", size=20)
        self.zero_led.pack(side=tk.LEFT, padx=20)
        
        # === OUTPUT DISPLAY ===
        output_frame = tk.LabelFrame(main_frame, text="OUTPUT DISPLAY",
                                    fg="#ff0000", bg="#0a0a0a",
                                    font=("Courier", 12, "bold"))
        output_frame.pack(pady=10, padx=10, fill="x")
        
        output_container = tk.Frame(output_frame, bg="#0a0a0a")
        output_container.pack(pady=10)
        
        # 7-segment display
        self.seven_seg = SevenSegmentDisplay(output_container, size=0.8)
        self.seven_seg.canvas.pack(side=tk.LEFT, padx=20)
        
        # Multi-format display
        format_frame = tk.Frame(output_container, bg="#0a0a0a")
        format_frame.pack(side=tk.LEFT, padx=20)
        
        self.output_lcd = LCDDisplay(format_frame, "OUTPUT VALUE", width=30, height=4)
        self.output_lcd.pack()
        
        # === MEMORY PROGRAMMING SWITCHES ===
        mem_frame = tk.LabelFrame(main_frame, text="MEMORY PROGRAMMING",
                                 fg="#ff6600", bg="#0a0a0a",
                                 font=("Courier", 12, "bold"))
        mem_frame.pack(pady=10, padx=10, fill="x")
        
        switch_container = tk.Frame(mem_frame, bg="#0a0a0a")
        switch_container.pack(pady=10)
        
        # Address switches (4-bit)
        addr_frame = tk.Frame(switch_container, bg="#0a0a0a")
        addr_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(addr_frame, text="ADDRESS (4-bit)", fg="#ffff00", bg="#0a0a0a",
                font=("Courier", 10, "bold")).pack()
        
        addr_switch_frame = tk.Frame(addr_frame, bg="#0a0a0a")
        addr_switch_frame.pack(pady=5)
        
        self.addr_switches = []
        for i in range(3, -1, -1):
            sw = Switch(addr_switch_frame, label=f"A{i}")
            sw.pack(side=tk.LEFT, padx=3)
            self.addr_switches.insert(0, sw)
        
        # Data switches (8-bit)
        data_frame = tk.Frame(switch_container, bg="#0a0a0a")
        data_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(data_frame, text="DATA (8-bit)", fg="#00ff00", bg="#0a0a0a",
                font=("Courier", 10, "bold")).pack()
        
        data_switch_frame = tk.Frame(data_frame, bg="#0a0a0a")
        data_switch_frame.pack(pady=5)
        
        self.data_switches = []
        for i in range(7, -1, -1):
            sw = Switch(data_switch_frame, label=f"D{i}")
            sw.pack(side=tk.LEFT, padx=2)
            self.data_switches.insert(0, sw)
        
        # Program button
        prog_btn = tk.Button(mem_frame, text="PROGRAM MEMORY",
                           command=self.program_memory,
                           bg="#ff6600", fg="white",
                           font=("Courier", 12, "bold"),
                           width=20, height=2)
        prog_btn.pack(pady=10)
        
        # === MEMORY VIEWER ===
        mem_view_frame = tk.LabelFrame(main_frame, text="MEMORY VIEWER",
                                      fg="#00ffff", bg="#0a0a0a",
                                      font=("Courier", 11, "bold"))
        mem_view_frame.pack(pady=10, padx=10, fill="x")
        
        self.mem_lcd = LCDDisplay(mem_view_frame, "", width=60, height=8)
        self.mem_lcd.pack(pady=10)
        
        # === CONTROL BUTTONS ===
        control_btn_frame = tk.Frame(main_frame, bg="#0a0a0a")
        control_btn_frame.pack(pady=20)
        
        self.step_btn = tk.Button(control_btn_frame, text="STEP",
                                  command=self.step_execution,
                                  bg="#0066ff", fg="white",
                                  font=("Courier", 14, "bold"),
                                  width=12, height=2)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.run_btn = tk.Button(control_btn_frame, text="RUN",
                                command=self.toggle_run,
                                bg="#00ff00", fg="black",
                                font=("Courier", 14, "bold"),
                                width=12, height=2)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(control_btn_frame, text="RESET",
                                   command=self.reset_computer,
                                   bg="#ff0000", fg="white",
                                   font=("Courier", 14, "bold"),
                                   width=12, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = tk.Button(control_btn_frame, text="LOAD",
                                  command=self.load_program,
                                  bg="#ffff00", fg="black",
                                  font=("Courier", 14, "bold"),
                                  width=12, height=2)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Sound toggle
        self.sound_btn = tk.Button(control_btn_frame, text="🔊 SOUND",
                                   command=self.toggle_sound,
                                   bg="#00ff00", fg="black",
                                   font=("Courier", 12, "bold"),
                                   width=12, height=2)
        self.sound_btn.pack(side=tk.LEFT, padx=5)
        
        # === CLOCK SPEED ===
        speed_frame = tk.Frame(main_frame, bg="#0a0a0a")
        speed_frame.pack(pady=10)
        
        tk.Label(speed_frame, text="CLOCK SPEED (Hz):", fg="white", bg="#0a0a0a",
                font=("Courier", 11, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=10, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=400,
                                   bg="#0a0a0a", fg="white",
                                   font=("Courier", 10))
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
        # === STATUS BAR ===
        status_frame = tk.Frame(main_frame, bg="#1a1a1a", relief=tk.SUNKEN, bd=2)
        status_frame.pack(pady=10, fill="x")
        
        self.status_label = tk.Label(status_frame, text="Ready",
                                     fg="#00ff00", bg="#1a1a1a",
                                     font=("Courier", 10), anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)
    
    def update_display(self):
        """Update all displays"""
        # Control signals
        for name, led in self.control_leds.items():
            led.set_state(self.computer.control_signals[name])
        
        # Bus LEDs
        for i in range(8):
            self.bus_leds[i].set_state((self.computer.bus >> i) & 1)
        
        bus_text = f"BIN:{format(self.computer.bus, '08b')} HEX:0x{self.computer.bus:02X} DEC:{self.computer.bus}"
        self.bus_lcd.set_text(bus_text)
        
        # Register A
        for i in range(8):
            self.reg_a_leds[i].set_state((self.computer.reg_a >> i) & 1)
        
        a_text = f"BIN: {format(self.computer.reg_a, '08b')}\nHEX: 0x{self.computer.reg_a:02X}  DEC: {self.computer.reg_a}"
        self.reg_a_lcd.set_text(a_text)
        
        # Register B
        for i in range(8):
            self.reg_b_leds[i].set_state((self.computer.reg_b >> i) & 1)
        
        b_text = f"BIN: {format(self.computer.reg_b, '08b')}\nHEX: 0x{self.computer.reg_b:02X}  DEC: {self.computer.reg_b}"
        self.reg_b_lcd.set_text(b_text)
        
        # Program Counter
        for i in range(4):
            self.pc_leds[i].set_state((self.computer.pc >> i) & 1)
        
        pc_text = f"BIN:{format(self.computer.pc, '04b')} DEC:{self.computer.pc}"
        self.pc_lcd.set_text(pc_text)
        
        # Instruction Register
        for i in range(8):
            self.ir_leds[i].set_state((self.computer.ir >> i) & 1)
        
        opcode = (self.computer.ir >> 4) & 0x0F
        operand = self.computer.ir & 0x0F
        opcodes = {0x0:'NOP', 0x1:'LDA', 0x2:'ADD', 0x3:'SUB', 0x4:'STA',
                  0x5:'LDI', 0x6:'JMP', 0x7:'JC', 0x8:'JZ', 0xE:'OUT', 0xF:'HLT'}
        opcode_name = opcodes.get(opcode, 'UNK')
        ir_text = f"{opcode_name} {operand}\nBIN:{format(self.computer.ir, '08b')} HEX:0x{self.computer.ir:02X}"
        self.ir_lcd.set_text(ir_text)
        
        # Memory Address Register
        for i in range(4):
            self.mar_leds[i].set_state((self.computer.mar >> i) & 1)
        
        mar_text = f"BIN:{format(self.computer.mar, '04b')} DEC:{self.computer.mar}"
        self.mar_lcd.set_text(mar_text)
        
        # Flags
        self.carry_led.set_state(self.computer.carry_flag)
        self.zero_led.set_state(self.computer.zero_flag)
        
        # Output display
        self.seven_seg.display_number(self.computer.reg_a)
        
        output_text = f"BIN: {format(self.computer.reg_a, '08b')}\n"
        output_text += f"HEX: 0x{self.computer.reg_a:02X}\n"
        output_text += f"DEC: {self.computer.reg_a}\n"
        output_text += f"OCT: 0o{self.computer.reg_a:o}"
        self.output_lcd.set_text(output_text)
        
        # Memory viewer
        mem_text = "ADDR | HEX  BIN      DEC\n"
        mem_text += "-----+-------------------\n"
        for addr in range(16):
            val = self.computer.memory[addr]
            mem_text += f" {addr:2d}  | 0x{val:02X} {format(val, '08b')} {val:3d}\n"
        self.mem_lcd.set_text(mem_text)
    
    def program_memory(self):
        """Program memory from switches"""
        addr = 0
        for i, sw in enumerate(self.addr_switches):
            if sw.get_state():
                addr |= (1 << i)
        
        data = 0
        for i, sw in enumerate(self.data_switches):
            if sw.get_state():
                data |= (1 << i)
        
        self.computer.memory[addr] = data
        
        if self.sound_enabled:
            self.audio.play_write()
        
        self.update_display()
        self.status_label.config(text=f"Programmed: Addr {addr} = {data} (0x{data:02X})")
        messagebox.showinfo("Memory Programmed",
                          f"Address {addr}: {data} (0x{data:02X}, {format(data, '08b')})")
    
    def step_execution(self):
        """Execute one instruction"""
        if not self.computer.halted:
            if self.sound_enabled:
                self.audio.play_pong()
            
            self.computer.step()
            self.update_display()
            
            if self.sound_enabled:
                self.audio.play_read()
            
            self.status_label.config(text=f"Executed: PC={self.computer.pc}")
        else:
            if self.sound_enabled:
                self.audio.play_click()
            self.status_label.config(text="Computer is HALTED")
            messagebox.showinfo("Halted", "Computer is halted. Press RESET to restart.")
    
    def toggle_run(self):
        """Toggle auto-run mode"""
        self.auto_clock = not self.auto_clock
        
        if self.auto_clock:
            self.run_btn.config(text="STOP", bg="#ff0000", fg="white")
            self.status_label.config(text="Running...")
            self.run_computer()
        else:
            self.run_btn.config(text="RUN", bg="#00ff00", fg="black")
            self.status_label.config(text="Stopped")
    
    def run_computer(self):
        """Run computer automatically"""
        if self.auto_clock and not self.computer.halted:
            self.computer.step()
            self.update_display()
            
            delay = int(1000 / self.speed_scale.get())
            self.root.after(delay, self.run_computer)
        else:
            self.auto_clock = False
            self.run_btn.config(text="RUN", bg="#00ff00", fg="black")
            if self.computer.halted:
                self.status_label.config(text="HALTED")
    
    def reset_computer(self):
        """Reset computer"""
        self.auto_clock = False
        self.run_btn.config(text="RUN", bg="#00ff00", fg="black")
        self.computer.reset()
        self.update_display()
        
        if self.sound_enabled:
            self.audio.play_click()
        
        self.status_label.config(text="Reset complete")
    
    def load_program(self):
        """Load program from binary file"""
        filename = filedialog.askopenfilename(
            title="Load Program",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'rb') as f:
                    data = f.read()
                    program = {i: byte for i, byte in enumerate(data)}
                    self.computer.load_program(program)
                    self.reset_computer()
                    
                    if self.sound_enabled:
                        self.audio.play_read()
                    
                    self.status_label.config(text=f"Loaded: {filename} ({len(data)} bytes)")
                    messagebox.showinfo("Success", f"Loaded {len(data)} bytes from {filename}")
            except Exception as e:
                self.status_label.config(text=f"Error: {e}")
                messagebox.showerror("Error", f"Failed to load program: {e}")
    
    def toggle_sound(self):
        """Toggle sound effects"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.config(text="🔊 SOUND", bg="#00ff00")
            self.audio.play_click()
            self.status_label.config(text="Sound enabled")
        else:
            self.sound_btn.config(text="🔇 MUTE", bg="#666")
            self.status_label.config(text="Sound disabled")


def main():
    root = tk.Tk()
    app = CompleteComputerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
