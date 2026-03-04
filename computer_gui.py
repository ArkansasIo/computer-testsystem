#!/usr/bin/env python3
"""
Ben Eater 8-bit Computer GUI
Replicates the physical computer interface with switches, LEDs, and controls
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

class LED:
    """LED indicator widget"""
    def __init__(self, parent, label="", color="red"):
        self.frame = tk.Frame(parent, bg="#2b2b2b")
        self.label = tk.Label(self.frame, text=label, fg="white", bg="#2b2b2b", 
                             font=("Arial", 8))
        self.label.pack()
        
        self.canvas = tk.Canvas(self.frame, width=20, height=20, 
                               bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack()
        
        self.color = color
        self.off_color = "#1a1a1a"
        self.state = False
        
        self.circle = self.canvas.create_oval(2, 2, 18, 18, 
                                              fill=self.off_color, 
                                              outline="#555")
        
    def set_state(self, state):
        """Set LED on/off"""
        self.state = state
        color = self.color if state else self.off_color
        self.canvas.itemconfig(self.circle, fill=color)
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class Switch:
    """Toggle switch widget"""
    def __init__(self, parent, label="", callback=None):
        self.frame = tk.Frame(parent, bg="#2b2b2b")
        self.label = tk.Label(self.frame, text=label, fg="white", bg="#2b2b2b",
                             font=("Arial", 8))
        self.label.pack()
        
        self.state = False
        self.callback = callback
        
        self.button = tk.Button(self.frame, text="0", width=3, height=1,
                               bg="#333", fg="white", font=("Arial", 12, "bold"),
                               command=self.toggle)
        self.button.pack()
        
    def toggle(self):
        """Toggle switch state"""
        self.state = not self.state
        self.button.config(text="1" if self.state else "0",
                          bg="#00ff00" if self.state else "#333")
        if self.callback:
            self.callback(self.state)
            
    def set_state(self, state):
        """Set switch state programmatically"""
        self.state = state
        self.button.config(text="1" if state else "0",
                          bg="#00ff00" if state else "#333")
        
    def get_state(self):
        """Get current state"""
        return self.state
        
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class SevenSegmentDisplay:
    """7-segment display for output"""
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=120, height=180, 
                               bg="#1a1a1a", highlightthickness=2,
                               highlightbackground="#555")
        
        # Segment positions (a, b, c, d, e, f, g)
        self.segments = {
            'a': [(20, 10), (100, 10), (90, 20), (30, 20)],
            'b': [(100, 10), (110, 20), (110, 80), (100, 90)],
            'c': [(100, 90), (110, 100), (110, 160), (100, 170)],
            'd': [(20, 170), (100, 170), (90, 160), (30, 160)],
            'e': [(10, 100), (20, 90), (20, 160), (10, 170)],
            'f': [(10, 20), (20, 10), (20, 80), (10, 90)],
            'g': [(20, 90), (100, 90), (90, 80), (30, 80)]
        }
        
        self.segment_ids = {}
        for name, coords in self.segments.items():
            seg_id = self.canvas.create_polygon(coords, fill="#2a0000", 
                                               outline="#555")
            self.segment_ids[name] = seg_id
        
        # Digit patterns (which segments to light for each digit)
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
        # Turn off all segments
        for seg_id in self.segment_ids.values():
            self.canvas.itemconfig(seg_id, fill="#2a0000")
        
        # Turn on segments for this digit
        if digit in self.patterns:
            for seg_name in self.patterns[digit]:
                self.canvas.itemconfig(self.segment_ids[seg_name], fill="#ff0000")
                
    def display_number(self, number):
        """Display a number (shows last digit only for now)"""
        digit = number % 10
        self.display_digit(digit)
        
    def clear(self):
        """Clear display"""
        for seg_id in self.segment_ids.values():
            self.canvas.itemconfig(seg_id, fill="#2a0000")


class Computer:
    """8-bit computer simulation"""
    def __init__(self):
        self.memory = [0] * 16
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0  # Memory Address Register
        self.ir = 0   # Instruction Register
        self.carry_flag = False
        self.zero_flag = False
        self.halted = False
        self.running = False
        
    def reset(self):
        """Reset computer to initial state"""
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.carry_flag = False
        self.zero_flag = False
        self.halted = False
        self.running = False
        
    def load_program(self, program):
        """Load program into memory"""
        for addr, value in program.items():
            if 0 <= addr < 16:
                self.memory[addr] = value & 0xFF
                
    def step(self):
        """Execute one instruction"""
        if self.halted:
            return False
            
        # Fetch
        self.mar = self.pc
        self.ir = self.memory[self.mar]
        self.pc = (self.pc + 1) & 0x0F
        
        # Decode and Execute
        opcode = (self.ir >> 4) & 0x0F
        operand = self.ir & 0x0F
        
        if opcode == 0x0:  # NOP
            pass
        elif opcode == 0x1:  # LDA
            self.reg_a = self.memory[operand]
        elif opcode == 0x2:  # ADD
            self.reg_b = self.memory[operand]
            result = self.reg_a + self.reg_b
            self.carry_flag = result > 255
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
        elif opcode == 0x3:  # SUB
            self.reg_b = self.memory[operand]
            result = self.reg_a - self.reg_b
            self.carry_flag = result >= 0
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
        elif opcode == 0x4:  # STA
            self.memory[operand] = self.reg_a
        elif opcode == 0x5:  # LDI
            self.reg_a = operand
        elif opcode == 0x6:  # JMP
            self.pc = operand
        elif opcode == 0x7:  # JC
            if self.carry_flag:
                self.pc = operand
        elif opcode == 0x8:  # JZ
            if self.zero_flag:
                self.pc = operand
        elif opcode == 0xE:  # OUT
            pass  # Output handled by GUI
        elif opcode == 0xF:  # HLT
            self.halted = True
            return False
            
        return True


class ComputerGUI:
    """Main GUI for the 8-bit computer"""
    def __init__(self, root):
        self.root = root
        self.root.title("Ben Eater 8-bit Computer Simulator")
        self.root.configure(bg="#2b2b2b")
        
        self.computer = Computer()
        self.clock_speed = 1.0  # Hz
        self.auto_clock = False
        
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#2b2b2b", padx=20, pady=20)
        main_frame.pack()
        
        # Title
        title = tk.Label(main_frame, text="8-BIT COMPUTER", 
                        font=("Arial", 24, "bold"), fg="#00ff00", bg="#2b2b2b")
        title.grid(row=0, column=0, columnspan=4, pady=10)
        
        # === BUS DISPLAY ===
        bus_frame = tk.LabelFrame(main_frame, text="BUS (8-bit)", 
                                 fg="white", bg="#2b2b2b", font=("Arial", 12, "bold"))
        bus_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky="ew")
        
        self.bus_leds = []
        led_container = tk.Frame(bus_frame, bg="#2b2b2b")
        led_container.pack(pady=10)
        
        for i in range(7, -1, -1):
            led = LED(led_container, label=f"B{i}", color="#00ff00")
            led.pack(side=tk.LEFT, padx=5)
            self.bus_leds.append(led)
        self.bus_leds.reverse()  # Index 0 = bit 0
        
        # === REGISTERS ===
        reg_frame = tk.Frame(main_frame, bg="#2b2b2b")
        reg_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Register A
        a_frame = tk.LabelFrame(reg_frame, text="REGISTER A", 
                               fg="white", bg="#2b2b2b", font=("Arial", 10, "bold"))
        a_frame.pack(side=tk.LEFT, padx=10)
        
        self.reg_a_leds = []
        a_led_container = tk.Frame(a_frame, bg="#2b2b2b")
        a_led_container.pack(pady=5)
        
        for i in range(7, -1, -1):
            led = LED(a_led_container, label=f"{i}", color="#ff0000")
            led.pack(side=tk.LEFT, padx=2)
            self.reg_a_leds.append(led)
        self.reg_a_leds.reverse()
        
        self.reg_a_label = tk.Label(a_frame, text="0 (0x00)", 
                                   fg="white", bg="#2b2b2b", font=("Arial", 12))
        self.reg_a_label.pack(pady=5)
        
        # Register B
        b_frame = tk.LabelFrame(reg_frame, text="REGISTER B", 
                               fg="white", bg="#2b2b2b", font=("Arial", 10, "bold"))
        b_frame.pack(side=tk.LEFT, padx=10)
        
        self.reg_b_leds = []
        b_led_container = tk.Frame(b_frame, bg="#2b2b2b")
        b_led_container.pack(pady=5)
        
        for i in range(7, -1, -1):
            led = LED(b_led_container, label=f"{i}", color="#ff0000")
            led.pack(side=tk.LEFT, padx=2)
            self.reg_b_leds.append(led)
        self.reg_b_leds.reverse()
        
        self.reg_b_label = tk.Label(b_frame, text="0 (0x00)", 
                                   fg="white", bg="#2b2b2b", font=("Arial", 12))
        self.reg_b_label.pack(pady=5)
        
        # === PROGRAM COUNTER & FLAGS ===
        control_frame = tk.Frame(main_frame, bg="#2b2b2b")
        control_frame.grid(row=2, column=2, columnspan=2, pady=10, sticky="ew")
        
        # Program Counter
        pc_frame = tk.LabelFrame(control_frame, text="PROGRAM COUNTER", 
                                fg="white", bg="#2b2b2b", font=("Arial", 10, "bold"))
        pc_frame.pack(pady=5)
        
        self.pc_leds = []
        pc_led_container = tk.Frame(pc_frame, bg="#2b2b2b")
        pc_led_container.pack(pady=5)
        
        for i in range(3, -1, -1):
            led = LED(pc_led_container, label=f"{i}", color="#ffff00")
            led.pack(side=tk.LEFT, padx=3)
            self.pc_leds.append(led)
        self.pc_leds.reverse()
        
        self.pc_label = tk.Label(pc_frame, text="0", 
                                fg="white", bg="#2b2b2b", font=("Arial", 12))
        self.pc_label.pack(pady=5)
        
        # Flags
        flag_frame = tk.LabelFrame(control_frame, text="FLAGS", 
                                  fg="white", bg="#2b2b2b", font=("Arial", 10, "bold"))
        flag_frame.pack(pady=5)
        
        flag_container = tk.Frame(flag_frame, bg="#2b2b2b")
        flag_container.pack(pady=5)
        
        self.carry_led = LED(flag_container, label="CARRY", color="#ff00ff")
        self.carry_led.pack(side=tk.LEFT, padx=10)
        
        self.zero_led = LED(flag_container, label="ZERO", color="#00ffff")
        self.zero_led.pack(side=tk.LEFT, padx=10)
        
        # === OUTPUT DISPLAY ===
        output_frame = tk.LabelFrame(main_frame, text="OUTPUT", 
                                    fg="white", bg="#2b2b2b", font=("Arial", 12, "bold"))
        output_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        self.seven_seg = SevenSegmentDisplay(output_frame)
        self.seven_seg.canvas.pack(pady=10)
        
        self.output_label = tk.Label(output_frame, text="0", 
                                    fg="#ff0000", bg="#2b2b2b", 
                                    font=("Arial", 24, "bold"))
        self.output_label.pack(pady=5)
        
        # === MEMORY PROGRAMMING SWITCHES ===
        mem_frame = tk.LabelFrame(main_frame, text="MEMORY PROGRAMMING", 
                                 fg="white", bg="#2b2b2b", font=("Arial", 12, "bold"))
        mem_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        switch_container = tk.Frame(mem_frame, bg="#2b2b2b")
        switch_container.pack(pady=10)
        
        # Address switches (4-bit)
        addr_frame = tk.Frame(switch_container, bg="#2b2b2b")
        addr_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(addr_frame, text="ADDRESS", fg="white", bg="#2b2b2b",
                font=("Arial", 10, "bold")).pack()
        
        addr_switch_frame = tk.Frame(addr_frame, bg="#2b2b2b")
        addr_switch_frame.pack()
        
        self.addr_switches = []
        for i in range(3, -1, -1):
            sw = Switch(addr_switch_frame, label=f"A{i}")
            sw.pack(side=tk.LEFT, padx=3)
            self.addr_switches.append(sw)
        self.addr_switches.reverse()
        
        # Data switches (8-bit)
        data_frame = tk.Frame(switch_container, bg="#2b2b2b")
        data_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(data_frame, text="DATA", fg="white", bg="#2b2b2b",
                font=("Arial", 10, "bold")).pack()
        
        data_switch_frame = tk.Frame(data_frame, bg="#2b2b2b")
        data_switch_frame.pack()
        
        self.data_switches = []
        for i in range(7, -1, -1):
            sw = Switch(data_switch_frame, label=f"D{i}")
            sw.pack(side=tk.LEFT, padx=2)
            self.data_switches.append(sw)
        self.data_switches.reverse()
        
        # Program button
        prog_btn = tk.Button(mem_frame, text="PROGRAM", command=self.program_memory,
                           bg="#ff6600", fg="white", font=("Arial", 12, "bold"),
                           width=15, height=2)
        prog_btn.pack(pady=10)
        
        # === CONTROL BUTTONS ===
        control_btn_frame = tk.Frame(main_frame, bg="#2b2b2b")
        control_btn_frame.grid(row=5, column=0, columnspan=4, pady=20)
        
        self.step_btn = tk.Button(control_btn_frame, text="STEP", 
                                  command=self.step_execution,
                                  bg="#0066ff", fg="white", 
                                  font=("Arial", 12, "bold"), width=10, height=2)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.run_btn = tk.Button(control_btn_frame, text="RUN", 
                                command=self.toggle_run,
                                bg="#00ff00", fg="black", 
                                font=("Arial", 12, "bold"), width=10, height=2)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(control_btn_frame, text="RESET", 
                                   command=self.reset_computer,
                                   bg="#ff0000", fg="white", 
                                   font=("Arial", 12, "bold"), width=10, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = tk.Button(control_btn_frame, text="LOAD", 
                                  command=self.load_program,
                                  bg="#ffff00", fg="black", 
                                  font=("Arial", 12, "bold"), width=10, height=2)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Clock speed control
        speed_frame = tk.Frame(main_frame, bg="#2b2b2b")
        speed_frame.grid(row=6, column=0, columnspan=4, pady=10)
        
        tk.Label(speed_frame, text="CLOCK SPEED (Hz):", fg="white", bg="#2b2b2b",
                font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=10, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=300, bg="#2b2b2b",
                                   fg="white", font=("Arial", 10))
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
    def update_display(self):
        """Update all LEDs and displays"""
        # Update bus LEDs (show current instruction or data)
        bus_value = self.computer.ir
        for i in range(8):
            self.bus_leds[i].set_state((bus_value >> i) & 1)
        
        # Update Register A
        for i in range(8):
            self.reg_a_leds[i].set_state((self.computer.reg_a >> i) & 1)
        self.reg_a_label.config(text=f"{self.computer.reg_a} (0x{self.computer.reg_a:02X})")
        
        # Update Register B
        for i in range(8):
            self.reg_b_leds[i].set_state((self.computer.reg_b >> i) & 1)
        self.reg_b_label.config(text=f"{self.computer.reg_b} (0x{self.computer.reg_b:02X})")
        
        # Update Program Counter
        for i in range(4):
            self.pc_leds[i].set_state((self.computer.pc >> i) & 1)
        self.pc_label.config(text=str(self.computer.pc))
        
        # Update Flags
        self.carry_led.set_state(self.computer.carry_flag)
        self.zero_led.set_state(self.computer.zero_flag)
        
        # Update Output Display
        self.seven_seg.display_number(self.computer.reg_a)
        self.output_label.config(text=str(self.computer.reg_a))
        
    def program_memory(self):
        """Program memory from switches"""
        # Get address from switches
        addr = 0
        for i, sw in enumerate(self.addr_switches):
            if sw.get_state():
                addr |= (1 << i)
        
        # Get data from switches
        data = 0
        for i, sw in enumerate(self.data_switches):
            if sw.get_state():
                data |= (1 << i)
        
        # Program memory
        self.computer.memory[addr] = data
        messagebox.showinfo("Memory Programmed", 
                          f"Address {addr}: {data} (0x{data:02X})")
        
    def step_execution(self):
        """Execute one instruction"""
        if not self.computer.halted:
            self.computer.step()
            self.update_display()
        else:
            messagebox.showinfo("Halted", "Computer is halted. Press RESET to restart.")
            
    def toggle_run(self):
        """Toggle auto-run mode"""
        self.auto_clock = not self.auto_clock
        
        if self.auto_clock:
            self.run_btn.config(text="STOP", bg="#ff0000")
            self.run_computer()
        else:
            self.run_btn.config(text="RUN", bg="#00ff00")
            
    def run_computer(self):
        """Run computer automatically"""
        if self.auto_clock and not self.computer.halted:
            self.computer.step()
            self.update_display()
            
            delay = int(1000 / self.speed_scale.get())
            self.root.after(delay, self.run_computer)
        else:
            self.auto_clock = False
            self.run_btn.config(text="RUN", bg="#00ff00")
            
    def reset_computer(self):
        """Reset computer"""
        self.auto_clock = False
        self.run_btn.config(text="RUN", bg="#00ff00")
        self.computer.reset()
        self.update_display()
        self.seven_seg.clear()
        
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
                    messagebox.showinfo("Success", f"Loaded {len(data)} bytes")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load program: {e}")


def main():
    root = tk.Tk()
    app = ComputerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
