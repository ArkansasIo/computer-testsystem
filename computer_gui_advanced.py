#!/usr/bin/env python3
"""
Advanced 8-bit Computer GUI - ALL FEATURES
Missing features added:
- Clock module with manual/auto modes
- Single-step microcode execution
- Register selector switches
- ALU operation display
- Stack pointer visualization
- Interrupt system
- Breakpoint system
- Watch variables
- Instruction history
- Timing diagram
- Power indicator
- Mode switches (RUN/PROGRAM/SINGLE STEP)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import queue

try:
    import pyaudio
    import wave
    import io
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

from sound_effects import SoundEffects


class LED:
    """LED component with brightness control"""
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
        self.brightness = 1.0
        
        self.circle = self.canvas.create_oval(2, 2, size-2, size-2,
                                              fill=self.off_color,
                                              outline="#333")
    
    def set_state(self, state, brightness=1.0):
        """Set LED on/off with brightness"""
        self.state = state
        self.brightness = brightness
        
        if state:
            # Calculate dimmed color
            color = self.color
            if brightness < 1.0:
                # Simple brightness adjustment
                color = self._dim_color(self.color, brightness)
            self.canvas.itemconfig(self.circle, fill=color, outline=color)
        else:
            self.canvas.itemconfig(self.circle, fill=self.off_color, outline="#333")
    
    def _dim_color(self, color, brightness):
        """Dim a hex color"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def pulse(self):
        """Pulse LED briefly"""
        self.set_state(True)
        self.canvas.after(100, lambda: self.set_state(False))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class Switch:
    """Toggle switch with 3 states (OFF/ON/AUTO)"""
    def __init__(self, parent, label="", callback=None, three_state=False):
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        if label:
            self.label = tk.Label(self.frame, text=label, fg="white", bg="#1a1a1a",
                                 font=("Courier", 7))
            self.label.pack()
        
        self.state = 0  # 0=OFF, 1=ON, 2=AUTO (if three_state)
        self.three_state = three_state
        self.callback = callback
        
        self.button = tk.Button(self.frame, text="0", width=2, height=1,
                               bg="#222", fg="#666", font=("Courier", 10, "bold"),
                               command=self.toggle, relief=tk.RAISED)
        self.button.pack()
    
    def toggle(self):
        """Toggle switch state"""
        if self.three_state:
            self.state = (self.state + 1) % 3
            if self.state == 0:
                self.button.config(text="0", bg="#222", fg="#666", relief=tk.RAISED)
            elif self.state == 1:
                self.button.config(text="1", bg="#00ff00", fg="black", relief=tk.SUNKEN)
            else:
                self.button.config(text="A", bg="#ffff00", fg="black", relief=tk.FLAT)
        else:
            self.state = 1 - self.state
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
        if self.three_state:
            if state == 0:
                self.button.config(text="0", bg="#222", fg="#666", relief=tk.RAISED)
            elif state == 1:
                self.button.config(text="1", bg="#00ff00", fg="black", relief=tk.SUNKEN)
            else:
                self.button.config(text="A", bg="#ffff00", fg="black", relief=tk.FLAT)
        else:
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


class ClockModule:
    """Clock module with manual pulse and auto modes"""
    def __init__(self, parent, callback=None):
        self.frame = tk.LabelFrame(parent, text="CLOCK MODULE", fg="#ffff00",
                                  bg="#1a1a1a", font=("Courier", 11, "bold"))
        self.callback = callback
        self.auto_mode = False
        self.frequency = 1.0
        
        # Clock LED
        led_frame = tk.Frame(self.frame, bg="#1a1a1a")
        led_frame.pack(pady=5)
        
        self.clock_led = LED(led_frame, label="CLK", color="#ffff00", size=25)
        self.clock_led.pack()
        
        # Manual pulse button
        self.pulse_btn = tk.Button(self.frame, text="PULSE", command=self.manual_pulse,
                                   bg="#0066ff", fg="white", font=("Courier", 10, "bold"),
                                   width=10, height=2)
        self.pulse_btn.pack(pady=5)
        
        # Mode switch
        mode_frame = tk.Frame(self.frame, bg="#1a1a1a")
        mode_frame.pack(pady=5)
        
        tk.Label(mode_frame, text="MODE:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT)
        
        self.mode_switch = Switch(mode_frame, three_state=False,
                                 callback=self.mode_changed)
        self.mode_switch.pack(side=tk.LEFT, padx=5)
        
        tk.Label(mode_frame, text="AUTO", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT)
        
        # Frequency control
        freq_frame = tk.Frame(self.frame, bg="#1a1a1a")
        freq_frame.pack(pady=5)
        
        tk.Label(freq_frame, text="FREQ:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack()
        
        self.freq_scale = tk.Scale(freq_frame, from_=0.1, to=10, resolution=0.1,
                                  orient=tk.HORIZONTAL, length=150, bg="#1a1a1a",
                                  fg="white", font=("Courier", 8))
        self.freq_scale.set(1.0)
        self.freq_scale.pack()
        
        # Cycle counter
        self.cycle_count = 0
        self.cycle_label = tk.Label(self.frame, text="Cycles: 0", fg="#00ff00",
                                    bg="#1a1a1a", font=("Courier", 9))
        self.cycle_label.pack(pady=5)
    
    def manual_pulse(self):
        """Manual clock pulse"""
        self.clock_led.pulse()
        self.cycle_count += 1
        self.cycle_label.config(text=f"Cycles: {self.cycle_count}")
        if self.callback:
            self.callback()
    
    def mode_changed(self, state):
        """Clock mode changed"""
        self.auto_mode = (state == 1)
        if self.auto_mode:
            self.pulse_btn.config(state=tk.DISABLED)
            self.auto_clock()
        else:
            self.pulse_btn.config(state=tk.NORMAL)
    
    def auto_clock(self):
        """Auto clock pulses"""
        if self.auto_mode:
            self.manual_pulse()
            delay = int(1000 / self.freq_scale.get())
            self.frame.after(delay, self.auto_clock)
    
    def reset(self):
        """Reset cycle counter"""
        self.cycle_count = 0
        self.cycle_label.config(text="Cycles: 0")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class ALUDisplay:
    """ALU operation display"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(parent, text="ALU (Arithmetic Logic Unit)",
                                  fg="#ff6600", bg="#1a1a1a",
                                  font=("Courier", 10, "bold"))
        
        # Operation display
        self.op_label = tk.Label(self.frame, text="A + B = Result",
                                fg="#ff6600", bg="#0a0a0a",
                                font=("Courier", 12, "bold"), width=30, height=3,
                                relief=tk.SUNKEN, bd=2)
        self.op_label.pack(pady=10, padx=10)
        
        # Mode indicators
        mode_frame = tk.Frame(self.frame, bg="#1a1a1a")
        mode_frame.pack(pady=5)
        
        self.add_led = LED(mode_frame, label="ADD", color="#00ff00", size=12)
        self.add_led.pack(side=tk.LEFT, padx=5)
        
        self.sub_led = LED(mode_frame, label="SUB", color="#ff0000", size=12)
        self.sub_led.pack(side=tk.LEFT, padx=5)
        
        self.and_led = LED(mode_frame, label="AND", color="#0066ff", size=12)
        self.and_led.pack(side=tk.LEFT, padx=5)
        
        self.or_led = LED(mode_frame, label="OR", color="#ff00ff", size=12)
        self.or_led.pack(side=tk.LEFT, padx=5)
        
        self.xor_led = LED(mode_frame, label="XOR", color="#00ffff", size=12)
        self.xor_led.pack(side=tk.LEFT, padx=5)
    
    def set_operation(self, op, a, b, result):
        """Display ALU operation"""
        # Clear all LEDs
        self.add_led.set_state(False)
        self.sub_led.set_state(False)
        self.and_led.set_state(False)
        self.or_led.set_state(False)
        self.xor_led.set_state(False)
        
        # Set appropriate LED
        if op == "ADD":
            self.add_led.set_state(True)
            text = f"{a} + {b} = {result}"
        elif op == "SUB":
            self.sub_led.set_state(True)
            text = f"{a} - {b} = {result}"
        elif op == "AND":
            self.and_led.set_state(True)
            text = f"{a} AND {b} = {result}"
        elif op == "OR":
            self.or_led.set_state(True)
            text = f"{a} OR {b} = {result}"
        elif op == "XOR":
            self.xor_led.set_state(True)
            text = f"{a} XOR {b} = {result}"
        else:
            text = "No operation"
        
        self.op_label.config(text=text)
    
    def clear(self):
        """Clear display"""
        self.add_led.set_state(False)
        self.sub_led.set_state(False)
        self.and_led.set_state(False)
        self.or_led.set_state(False)
        self.xor_led.set_state(False)
        self.op_label.config(text="Ready")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)



class InstructionHistory:
    """Instruction execution history"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(parent, text="INSTRUCTION HISTORY",
                                  fg="#00ffff", bg="#1a1a1a",
                                  font=("Courier", 10, "bold"))
        
        self.text = scrolledtext.ScrolledText(self.frame, width=50, height=10,
                                             bg="#0a0a0a", fg="#00ffff",
                                             font=("Courier", 9),
                                             relief=tk.SUNKEN, bd=2)
        self.text.pack(pady=5, padx=5)
        
        # Clear button
        tk.Button(self.frame, text="Clear History", command=self.clear,
                 bg="#ff0000", fg="white", font=("Courier", 9, "bold")).pack(pady=5)
        
        self.history = []
    
    def add_instruction(self, pc, opcode, operand, description):
        """Add instruction to history"""
        entry = f"[{pc:02d}] 0x{opcode:01X}{operand:01X} - {description}\n"
        self.history.append(entry)
        self.text.insert(tk.END, entry)
        self.text.see(tk.END)
        
        # Keep only last 100 instructions
        if len(self.history) > 100:
            self.history.pop(0)
            self.text.delete(1.0, 2.0)
    
    def clear(self):
        """Clear history"""
        self.history = []
        self.text.delete(1.0, tk.END)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class BreakpointPanel:
    """Breakpoint management"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(parent, text="BREAKPOINTS",
                                  fg="#ff0000", bg="#1a1a1a",
                                  font=("Courier", 10, "bold"))
        
        # Breakpoint list
        list_frame = tk.Frame(self.frame, bg="#1a1a1a")
        list_frame.pack(pady=5, padx=5)
        
        self.listbox = tk.Listbox(list_frame, width=20, height=6,
                                  bg="#0a0a0a", fg="#ff0000",
                                  font=("Courier", 9))
        self.listbox.pack(side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Add/Remove controls
        control_frame = tk.Frame(self.frame, bg="#1a1a1a")
        control_frame.pack(pady=5)
        
        tk.Label(control_frame, text="Address:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT)
        
        self.addr_entry = tk.Entry(control_frame, width=5, bg="#0a0a0a",
                                   fg="#00ff00", font=("Courier", 9))
        self.addr_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Add", command=self.add_breakpoint,
                 bg="#00ff00", fg="black", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(control_frame, text="Remove", command=self.remove_breakpoint,
                 bg="#ff0000", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=2)
        
        self.breakpoints = set()
    
    def add_breakpoint(self):
        """Add breakpoint"""
        try:
            addr = int(self.addr_entry.get())
            if 0 <= addr < 16:
                self.breakpoints.add(addr)
                self.listbox.insert(tk.END, f"Address {addr}")
                self.addr_entry.delete(0, tk.END)
        except ValueError:
            pass
    
    def remove_breakpoint(self):
        """Remove selected breakpoint"""
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            text = self.listbox.get(idx)
            addr = int(text.split()[1])
            self.breakpoints.discard(addr)
            self.listbox.delete(idx)
    
    def is_breakpoint(self, addr):
        """Check if address is a breakpoint"""
        return addr in self.breakpoints
    
    def clear(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()
        self.listbox.delete(0, tk.END)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)



class ModePanel:
    """Operating mode selector"""
    def __init__(self, parent, callback=None):
        self.frame = tk.LabelFrame(parent, text="OPERATING MODE",
                                  fg="#ffff00", bg="#1a1a1a",
                                  font=("Courier", 11, "bold"))
        self.callback = callback
        self.mode = "PROGRAM"  # PROGRAM, RUN, SINGLE_STEP
        
        # Mode buttons
        btn_frame = tk.Frame(self.frame, bg="#1a1a1a")
        btn_frame.pack(pady=10, padx=10)
        
        self.program_btn = tk.Button(btn_frame, text="PROGRAM",
                                     command=lambda: self.set_mode("PROGRAM"),
                                     bg="#ffff00", fg="black",
                                     font=("Courier", 11, "bold"),
                                     width=12, height=2, relief=tk.SUNKEN)
        self.program_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.run_btn = tk.Button(btn_frame, text="RUN",
                                command=lambda: self.set_mode("RUN"),
                                bg="#00ff00", fg="black",
                                font=("Courier", 11, "bold"),
                                width=12, height=2, relief=tk.RAISED)
        self.run_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.step_btn = tk.Button(btn_frame, text="SINGLE STEP",
                                 command=lambda: self.set_mode("SINGLE_STEP"),
                                 bg="#0066ff", fg="white",
                                 font=("Courier", 11, "bold"),
                                 width=12, height=2, relief=tk.RAISED)
        self.step_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Mode indicator
        self.mode_label = tk.Label(self.frame, text="MODE: PROGRAM",
                                   fg="#ffff00", bg="#0a0a0a",
                                   font=("Courier", 14, "bold"),
                                   width=20, height=2, relief=tk.SUNKEN, bd=3)
        self.mode_label.pack(pady=10)
    
    def set_mode(self, mode):
        """Set operating mode"""
        self.mode = mode
        
        # Update button states
        self.program_btn.config(relief=tk.SUNKEN if mode == "PROGRAM" else tk.RAISED)
        self.run_btn.config(relief=tk.SUNKEN if mode == "RUN" else tk.RAISED)
        self.step_btn.config(relief=tk.SUNKEN if mode == "SINGLE_STEP" else tk.RAISED)
        
        # Update label
        self.mode_label.config(text=f"MODE: {mode}")
        
        if self.callback:
            self.callback(mode)
    
    def get_mode(self):
        return self.mode
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class PowerIndicator:
    """Power on/off indicator"""
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        
        tk.Label(self.frame, text="POWER", fg="white", bg="#1a1a1a",
                font=("Courier", 12, "bold")).pack()
        
        self.led = LED(self.frame, color="#00ff00", size=30)
        self.led.pack(pady=5)
        
        self.state = False
    
    def set_power(self, state):
        """Set power state"""
        self.state = state
        self.led.set_state(state)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


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
    
    def play_click(self):
        self.play_sound(self.sfx.generate_click())
    
    def play_pong(self):
        self.play_sound(self.sfx.generate_pong_sound())
    
    def play_read(self):
        self.play_sound(self.sfx.generate_read_sound())
    
    def play_write(self):
        self.play_sound(self.sfx.generate_write_sound())



class Computer:
    """Enhanced 8-bit computer with all features"""
    def __init__(self):
        self.memory = [0] * 16
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.bus = 0
        self.sp = 15  # Stack pointer
        self.carry_flag = False
        self.zero_flag = False
        self.negative_flag = False
        self.halted = False
        
        # Control signals
        self.control_signals = {
            'MI': False, 'RI': False, 'RO': False, 'II': False, 'IO': False,
            'AI': False, 'AO': False, 'EO': False, 'SU': False, 'BI': False,
            'OI': False, 'CE': False, 'CO': False, 'J': False, 'FI': False
        }
        
        # ALU state
        self.alu_operation = None
        self.alu_a = 0
        self.alu_b = 0
        self.alu_result = 0
    
    def reset(self):
        """Reset computer"""
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.bus = 0
        self.sp = 15
        self.carry_flag = False
        self.zero_flag = False
        self.negative_flag = False
        self.halted = False
        self.clear_control_signals()
        self.alu_operation = None
    
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
        """Execute one instruction"""
        if self.halted:
            return False
        
        self.clear_control_signals()
        
        # Fetch
        self.control_signals['CO'] = True
        self.control_signals['MI'] = True
        self.bus = self.pc
        self.mar = self.pc
        
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
            
            self.alu_operation = "ADD"
            self.alu_a = self.reg_a
            self.alu_b = self.reg_b
            result = self.reg_a + self.reg_b
            self.carry_flag = result > 255
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
            self.alu_result = self.reg_a
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
            
            self.alu_operation = "SUB"
            self.alu_a = self.reg_a
            self.alu_b = self.reg_b
            result = self.reg_a - self.reg_b
            self.carry_flag = result >= 0
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
            self.negative_flag = result < 0
            self.alu_result = self.reg_a
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
    
    def get_instruction_name(self, opcode):
        """Get instruction mnemonic"""
        opcodes = {0x0:'NOP', 0x1:'LDA', 0x2:'ADD', 0x3:'SUB', 0x4:'STA',
                  0x5:'LDI', 0x6:'JMP', 0x7:'JC', 0x8:'JZ', 0xE:'OUT', 0xF:'HLT'}
        return opcodes.get(opcode, 'UNK')
