#!/usr/bin/env python3
"""
Enhanced Computer GUI with Sound Effects and Multiple Display Formats
Includes: Binary, Hex, Decimal, Octal displays
Sound effects for read/write/load/run operations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time

# Try to import sound playback
try:
    import pyaudio
    import wave
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("PyAudio not available. Install with: pip install pyaudio")

from sound_effects import SoundEffects


class AudioPlayer:
    """Simple audio player for sound effects"""
    
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
            
            # Play in separate thread to avoid blocking
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
    
    def play_pong(self):
        self.play_sound(self.sfx.generate_pong_sound())
    
    def play_printer(self):
        self.play_sound(self.sfx.generate_printer_sound())
    
    def play_load(self):
        self.play_sound(self.sfx.generate_load_sound())
    
    def play_run(self):
        self.play_sound(self.sfx.generate_run_sound())
    
    def play_unload(self):
        self.play_sound(self.sfx.generate_unload_sound())
    
    def play_halt(self):
        self.play_sound(self.sfx.generate_halt_sound())
    
    def play_click(self):
        self.play_sound(self.sfx.generate_click())


class MultiFormatDisplay:
    """Display value in multiple formats"""
    
    def __init__(self, parent, label="Value", bit_width=8):
        self.frame = tk.LabelFrame(parent, text=label, fg="white", bg="#1a1a1a",
                                  font=("Courier", 10, "bold"))
        self.bit_width = bit_width
        self.max_value = (1 << bit_width) - 1
        
        # Create display labels
        display_frame = tk.Frame(self.frame, bg="#1a1a1a")
        display_frame.pack(pady=5, padx=5)
        
        # Binary
        tk.Label(display_frame, text="BIN:", fg="#00ff00", bg="#1a1a1a",
                font=("Courier", 9)).grid(row=0, column=0, sticky="e", padx=5)
        self.bin_label = tk.Label(display_frame, text="0" * bit_width,
                                  fg="#00ff00", bg="#000", font=("Courier", 9, "bold"),
                                  width=bit_width + 2, anchor="w")
        self.bin_label.grid(row=0, column=1, padx=5, pady=2)
        
        # Hexadecimal
        tk.Label(display_frame, text="HEX:", fg="#ffff00", bg="#1a1a1a",
                font=("Courier", 9)).grid(row=1, column=0, sticky="e", padx=5)
        hex_width = (bit_width + 3) // 4
        self.hex_label = tk.Label(display_frame, text="0x" + "0" * hex_width,
                                  fg="#ffff00", bg="#000", font=("Courier", 9, "bold"),
                                  width=hex_width + 4, anchor="w")
        self.hex_label.grid(row=1, column=1, padx=5, pady=2)
        
        # Decimal
        tk.Label(display_frame, text="DEC:", fg="#00ffff", bg="#1a1a1a",
                font=("Courier", 9)).grid(row=2, column=0, sticky="e", padx=5)
        self.dec_label = tk.Label(display_frame, text="0",
                                  fg="#00ffff", bg="#000", font=("Courier", 9, "bold"),
                                  width=12, anchor="w")
        self.dec_label.grid(row=2, column=1, padx=5, pady=2)
        
        # Octal
        tk.Label(display_frame, text="OCT:", fg="#ff00ff", bg="#1a1a1a",
                font=("Courier", 9)).grid(row=3, column=0, sticky="e", padx=5)
        self.oct_label = tk.Label(display_frame, text="0o0",
                                  fg="#ff00ff", bg="#000", font=("Courier", 9, "bold"),
                                  width=12, anchor="w")
        self.oct_label.grid(row=3, column=1, padx=5, pady=2)
        
    def set_value(self, value):
        """Update all format displays"""
        value = value & self.max_value
        
        # Binary
        bin_str = format(value, f'0{self.bit_width}b')
        self.bin_label.config(text=bin_str)
        
        # Hexadecimal
        hex_width = (self.bit_width + 3) // 4
        hex_str = f"0x{value:0{hex_width}X}"
        self.hex_label.config(text=hex_str)
        
        # Decimal
        self.dec_label.config(text=str(value))
        
        # Octal
        oct_str = f"0o{value:o}"
        self.oct_label.config(text=oct_str)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class Computer:
    """8-bit computer simulation with sound effects"""
    def __init__(self):
        self.memory = [0] * 256
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.carry_flag = False
        self.zero_flag = False
        self.halted = False
        self.running = False
        
    def reset(self):
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
        for addr, value in program.items():
            if 0 <= addr < 256:
                self.memory[addr] = value & 0xFF
                
    def step(self):
        if self.halted:
            return False
            
        self.mar = self.pc
        self.ir = self.memory[self.mar]
        self.pc = (self.pc + 1) & 0xFF
        
        opcode = (self.ir >> 4) & 0x0F
        operand = self.ir & 0x0F
        
        if opcode == 0x0:
            pass
        elif opcode == 0x1:
            self.reg_a = self.memory[operand]
        elif opcode == 0x2:
            self.reg_b = self.memory[operand]
            result = self.reg_a + self.reg_b
            self.carry_flag = result > 255
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
        elif opcode == 0x3:
            self.reg_b = self.memory[operand]
            result = self.reg_a - self.reg_b
            self.carry_flag = result >= 0
            self.reg_a = result & 0xFF
            self.zero_flag = (self.reg_a == 0)
        elif opcode == 0x4:
            self.memory[operand] = self.reg_a
        elif opcode == 0x5:
            self.reg_a = operand
        elif opcode == 0x6:
            self.pc = operand
        elif opcode == 0x7:
            if self.carry_flag:
                self.pc = operand
        elif opcode == 0x8:
            if self.zero_flag:
                self.pc = operand
        elif opcode == 0xE:
            pass
        elif opcode == 0xF:
            self.halted = True
            return False
            
        return True


class EnhancedComputerGUI:
    """Enhanced GUI with sound effects and multi-format displays"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced 8-bit Computer with Sound Effects")
        self.root.configure(bg="#1a1a1a")
        
        self.computer = Computer()
        self.audio = AudioPlayer()
        self.clock_speed = 1.0
        self.auto_clock = False
        self.sound_enabled = True
        
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a1a", padx=20, pady=20)
        main_frame.pack()
        
        # Title
        title = tk.Label(main_frame, text="8-BIT COMPUTER WITH SOUND", 
                        font=("Courier", 20, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Sound control
        sound_frame = tk.Frame(main_frame, bg="#1a1a1a")
        sound_frame.grid(row=1, column=0, columnspan=3, pady=5)
        
        self.sound_btn = tk.Button(sound_frame, text="🔊 SOUND ON", 
                                   command=self.toggle_sound,
                                   bg="#00ff00", fg="black", font=("Courier", 10, "bold"))
        self.sound_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(sound_frame, text="Test Sounds", command=self.test_sounds,
                 bg="#0066ff", fg="white", font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Multi-format displays
        display_row = tk.Frame(main_frame, bg="#1a1a1a")
        display_row.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.reg_a_display = MultiFormatDisplay(display_row, "REGISTER A", 8)
        self.reg_a_display.pack(side=tk.LEFT, padx=10)
        
        self.reg_b_display = MultiFormatDisplay(display_row, "REGISTER B", 8)
        self.reg_b_display.pack(side=tk.LEFT, padx=10)
        
        # PC and Address displays
        addr_row = tk.Frame(main_frame, bg="#1a1a1a")
        addr_row.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.pc_display = MultiFormatDisplay(addr_row, "PROGRAM COUNTER", 8)
        self.pc_display.pack(side=tk.LEFT, padx=10)
        
        self.mar_display = MultiFormatDisplay(addr_row, "MEMORY ADDRESS", 8)
        self.mar_display.pack(side=tk.LEFT, padx=10)
        
        # Output display
        output_frame = tk.LabelFrame(main_frame, text="OUTPUT", 
                                    fg="white", bg="#1a1a1a", font=("Courier", 12, "bold"))
        output_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.output_display = MultiFormatDisplay(output_frame, "OUTPUT VALUE", 8)
        self.output_display.pack(pady=10)
        
        # Large decimal display
        self.output_label = tk.Label(output_frame, text="0", fg="#ff0000", bg="#000",
                                    font=("Courier", 36, "bold"), width=10)
        self.output_label.pack(pady=10)
        
        # Flags
        flag_frame = tk.LabelFrame(main_frame, text="FLAGS", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        flag_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        flag_container = tk.Frame(flag_frame, bg="#1a1a1a")
        flag_container.pack(pady=5)
        
        self.carry_label = tk.Label(flag_container, text="CARRY: 0", fg="#ff00ff", bg="#000",
                                   font=("Courier", 12, "bold"), width=12)
        self.carry_label.pack(side=tk.LEFT, padx=10)
        
        self.zero_label = tk.Label(flag_container, text="ZERO: 0", fg="#00ffff", bg="#000",
                                  font=("Courier", 12, "bold"), width=12)
        self.zero_label.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg="#1a1a1a")
        control_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        self.step_btn = tk.Button(control_frame, text="STEP", 
                                  command=self.step_execution,
                                  bg="#0066ff", fg="white", 
                                  font=("Courier", 12, "bold"), width=10, height=2)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.run_btn = tk.Button(control_frame, text="RUN", 
                                command=self.toggle_run,
                                bg="#00ff00", fg="black", 
                                font=("Courier", 12, "bold"), width=10, height=2)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(control_frame, text="RESET", 
                                   command=self.reset_computer,
                                   bg="#ff0000", fg="white", 
                                   font=("Courier", 12, "bold"), width=10, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = tk.Button(control_frame, text="LOAD", 
                                  command=self.load_program,
                                  bg="#ffff00", fg="black", 
                                  font=("Courier", 12, "bold"), width=10, height=2)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Clock speed
        speed_frame = tk.Frame(main_frame, bg="#1a1a1a")
        speed_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        tk.Label(speed_frame, text="CLOCK SPEED (Hz):", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=10, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=300, bg="#1a1a1a",
                                   fg="white", font=("Courier", 10))
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.config(text="🔊 SOUND ON", bg="#00ff00")
            self.audio.play_click()
        else:
            self.sound_btn.config(text="🔇 SOUND OFF", bg="#666")
    
    def test_sounds(self):
        """Test all sound effects"""
        if not self.sound_enabled:
            return
        
        def play_sequence():
            sounds = [
                ("Read", self.audio.play_read),
                ("Write", self.audio.play_write),
                ("Pong", self.audio.play_pong),
                ("Printer", self.audio.play_printer),
                ("Load", self.audio.play_load),
                ("Run", self.audio.play_run),
                ("Halt", self.audio.play_halt)
            ]
            
            for name, sound_func in sounds:
                print(f"Playing: {name}")
                sound_func()
                time.sleep(0.7)
        
        thread = threading.Thread(target=play_sequence, daemon=True)
        thread.start()
    
    def update_display(self):
        # Update multi-format displays
        self.reg_a_display.set_value(self.computer.reg_a)
        self.reg_b_display.set_value(self.computer.reg_b)
        self.pc_display.set_value(self.computer.pc)
        self.mar_display.set_value(self.computer.mar)
        self.output_display.set_value(self.computer.reg_a)
        
        # Update large output
        self.output_label.config(text=str(self.computer.reg_a))
        
        # Update flags
        self.carry_label.config(text=f"CARRY: {int(self.computer.carry_flag)}")
        self.zero_label.config(text=f"ZERO: {int(self.computer.zero_flag)}")
        
    def step_execution(self):
        if not self.computer.halted:
            if self.sound_enabled:
                self.audio.play_pong()
            
            self.computer.step()
            self.update_display()
            
            if self.sound_enabled:
                self.audio.play_read()
        else:
            if self.sound_enabled:
                self.audio.play_halt()
            messagebox.showinfo("Halted", "Computer is halted.")
            
    def toggle_run(self):
        self.auto_clock = not self.auto_clock
        
        if self.auto_clock:
            self.run_btn.config(text="STOP", bg="#ff0000", fg="white")
            if self.sound_enabled:
                self.audio.play_run()
            self.run_computer()
        else:
            self.run_btn.config(text="RUN", bg="#00ff00", fg="black")
            
    def run_computer(self):
        if self.auto_clock and not self.computer.halted:
            if self.sound_enabled and self.computer.pc % 4 == 0:
                self.audio.play_printer()
            
            self.computer.step()
            self.update_display()
            
            delay = int(1000 / self.speed_scale.get())
            self.root.after(delay, self.run_computer)
        else:
            self.auto_clock = False
            self.run_btn.config(text="RUN", bg="#00ff00", fg="black")
            if self.computer.halted and self.sound_enabled:
                self.audio.play_halt()
            
    def reset_computer(self):
        self.auto_clock = False
        self.run_btn.config(text="RUN", bg="#00ff00", fg="black")
        self.computer.reset()
        self.update_display()
        if self.sound_enabled:
            self.audio.play_click()
        
    def load_program(self):
        filename = filedialog.askopenfilename(
            title="Load Program",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if self.sound_enabled:
                    self.audio.play_load()
                
                with open(filename, 'rb') as f:
                    data = f.read()
                    program = {i: byte for i, byte in enumerate(data)}
                    self.computer.load_program(program)
                    self.reset_computer()
                    messagebox.showinfo("Success", f"Loaded {len(data)} bytes")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")


def main():
    import io  # Add missing import
    root = tk.Tk()
    app = EnhancedComputerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
