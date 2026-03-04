#!/usr/bin/env python3
"""
ULTIMATE 8-bit Computer GUI - Complete System
Multiple windows, extensive widgets, settings, and layouts
ALL switches, LCDs, LEDs, and controls included
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, colorchooser
import threading
import time
import json
import os

try:
    import pyaudio
    import wave
    import io
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

from sound_effects import SoundEffects


# ============================================================================
# WIDGET COMPONENTS
# ============================================================================

class LED:
    """Enhanced LED with multiple colors and effects"""
    def __init__(self, parent, label="", color="red", size=15, shape="circle"):
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
        self.shape = shape
        self.size = size
        self.blinking = False
        
        if shape == "circle":
            self.item = self.canvas.create_oval(2, 2, size-2, size-2,
                                               fill=self.off_color, outline="#333")
        elif shape == "square":
            self.item = self.canvas.create_rectangle(2, 2, size-2, size-2,
                                                     fill=self.off_color, outline="#333")
        elif shape == "triangle":
            mid = size // 2
            self.item = self.canvas.create_polygon(mid, 2, size-2, size-2, 2, size-2,
                                                   fill=self.off_color, outline="#333")
    
    def set_state(self, state, brightness=1.0):
        self.state = state
        color = self.color if state else self.off_color
        outline = self.color if state else "#333"
        self.canvas.itemconfig(self.item, fill=color, outline=outline)
    
    def pulse(self, duration=100):
        self.set_state(True)
        self.canvas.after(duration, lambda: self.set_state(False))
    
    def start_blink(self, interval=500):
        self.blinking = True
        self._blink(interval)
    
    def stop_blink(self):
        self.blinking = False
        self.set_state(False)
    
    def _blink(self, interval):
        if self.blinking:
            self.set_state(not self.state)
            self.canvas.after(interval, lambda: self._blink(interval))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class Switch:
    """Multi-state switch with labels"""
    def __init__(self, parent, label="", states=2, callback=None, labels=None):
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        if label:
            self.label = tk.Label(self.frame, text=label, fg="white", bg="#1a1a1a",
                                 font=("Courier", 7))
            self.label.pack()
        
        self.states = states
        self.current_state = 0
        self.callback = callback
        self.labels = labels or [str(i) for i in range(states)]
        
        self.button = tk.Button(self.frame, text=self.labels[0], width=3, height=1,
                               bg="#222", fg="#666", font=("Courier", 9, "bold"),
                               command=self.toggle, relief=tk.RAISED)
        self.button.pack()
    
    def toggle(self):
        self.current_state = (self.current_state + 1) % self.states
        self.update_display()
        if self.callback:
            self.callback(self.current_state)
    
    def update_display(self):
        colors = ["#222", "#00ff00", "#ffff00", "#ff6600", "#ff0000"]
        fg_colors = ["#666", "black", "black", "white", "white"]
        reliefs = [tk.RAISED, tk.SUNKEN, tk.FLAT, tk.SUNKEN, tk.SUNKEN]
        
        idx = min(self.current_state, len(colors) - 1)
        self.button.config(
            text=self.labels[self.current_state],
            bg=colors[idx],
            fg=fg_colors[idx],
            relief=reliefs[idx]
        )
    
    def set_state(self, state):
        self.current_state = state % self.states
        self.update_display()
    
    def get_state(self):
        return self.current_state
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class LCDDisplay:
    """LCD display with customizable colors"""
    def __init__(self, parent, label="", width=20, height=2, bg_color="#0a3d0a", fg_color="#00ff00"):
        self.frame = tk.LabelFrame(parent, text=label, fg=fg_color, bg="#1a1a1a",
                                  font=("Courier", 9, "bold"))
        
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        self.text = tk.Text(self.frame, width=width, height=height,
                           bg=bg_color, fg=fg_color, font=("Courier", 10, "bold"),
                           relief=tk.SUNKEN, borderwidth=2)
        self.text.pack(padx=5, pady=5)
        self.text.config(state=tk.DISABLED)
    
    def set_text(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, text)
        self.text.config(state=tk.DISABLED)
    
    def set_colors(self, bg, fg):
        self.bg_color = bg
        self.fg_color = fg
        self.text.config(bg=bg, fg=fg)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class SevenSegmentDisplay:
    """7-segment display with color options"""
    def __init__(self, parent, size=1.0, color="#ff0000"):
        w, h = int(120 * size), int(180 * size)
        self.canvas = tk.Canvas(parent, width=w, height=h,
                               bg="#0a0a0a", highlightthickness=2,
                               highlightbackground="#333")
        self.color = color
        self.size = size
        
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
            seg_id = self.canvas.create_polygon(coords, fill="#1a0000", outline="#333")
            self.segment_ids[name] = seg_id
        
        self.patterns = {
            0: ['a','b','c','d','e','f'], 1: ['b','c'], 2: ['a','b','d','e','g'],
            3: ['a','b','c','d','g'], 4: ['b','c','f','g'], 5: ['a','c','d','f','g'],
            6: ['a','c','d','e','f','g'], 7: ['a','b','c'], 8: ['a','b','c','d','e','f','g'],
            9: ['a','b','c','d','f','g'], 'A': ['a','b','c','e','f','g'],
            'b': ['c','d','e','f','g'], 'C': ['a','d','e','f'], 'd': ['b','c','d','e','g'],
            'E': ['a','d','e','f','g'], 'F': ['a','e','f','g'], '-': ['g']
        }
    
    def display(self, value):
        for seg_id in self.segment_ids.values():
            self.canvas.itemconfig(seg_id, fill="#1a0000")
        
        if value in self.patterns:
            for seg_name in self.patterns[value]:
                self.canvas.itemconfig(self.segment_ids[seg_name], fill=self.color)
    
    def set_color(self, color):
        self.color = color


class Slider:
    """Custom slider with label and value display"""
    def __init__(self, parent, label="", from_=0, to=100, callback=None):
        self.frame = tk.Frame(parent, bg="#1a1a1a")
        self.callback = callback
        
        tk.Label(self.frame, text=label, fg="white", bg="#1a1a1a",
                font=("Courier", 9, "bold")).pack()
        
        self.scale = tk.Scale(self.frame, from_=from_, to=to, orient=tk.HORIZONTAL,
                             length=200, bg="#1a1a1a", fg="white",
                             font=("Courier", 8), command=self._on_change)
        self.scale.pack()
        
        self.value_label = tk.Label(self.frame, text=str(from_), fg="#00ff00",
                                    bg="#0a0a0a", font=("Courier", 10, "bold"),
                                    width=10, relief=tk.SUNKEN)
        self.value_label.pack(pady=2)
    
    def _on_change(self, value):
        self.value_label.config(text=str(float(value)))
        if self.callback:
            self.callback(float(value))
    
    def get(self):
        return self.scale.get()
    
    def set(self, value):
        self.scale.set(value)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)



class Meter:
    """Analog-style meter display"""
    def __init__(self, parent, label="", max_value=255):
        self.frame = tk.LabelFrame(parent, text=label, fg="white", bg="#1a1a1a",
                                  font=("Courier", 9, "bold"))
        self.max_value = max_value
        
        self.canvas = tk.Canvas(self.frame, width=150, height=100,
                               bg="#0a0a0a", highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        
        # Draw meter arc
        self.canvas.create_arc(10, 20, 140, 150, start=0, extent=180,
                              outline="#333", width=2, style=tk.ARC)
        
        # Draw scale marks
        for i in range(11):
            angle = 180 - (i * 18)
            x1 = 75 + 60 * tk.math.cos(tk.math.radians(angle))
            y1 = 85 - 60 * tk.math.sin(tk.math.radians(angle))
            x2 = 75 + 50 * tk.math.cos(tk.math.radians(angle))
            y2 = 85 - 50 * tk.math.sin(tk.math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill="#666", width=2)
        
        # Needle
        self.needle = self.canvas.create_line(75, 85, 75, 35,
                                              fill="#ff0000", width=3)
        
        # Value label
        self.value_label = tk.Label(self.frame, text="0", fg="#00ff00",
                                    bg="#0a0a0a", font=("Courier", 12, "bold"))
        self.value_label.pack()
    
    def set_value(self, value):
        value = max(0, min(value, self.max_value))
        angle = 180 - (180 * value / self.max_value)
        x = 75 + 50 * tk.math.cos(tk.math.radians(angle))
        y = 85 - 50 * tk.math.sin(tk.math.radians(angle))
        self.canvas.coords(self.needle, 75, 85, x, y)
        self.value_label.config(text=str(value))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


class BarGraph:
    """Vertical bar graph"""
    def __init__(self, parent, label="", max_value=255, color="#00ff00"):
        self.frame = tk.LabelFrame(parent, text=label, fg="white", bg="#1a1a1a",
                                  font=("Courier", 9, "bold"))
        self.max_value = max_value
        self.color = color
        
        self.canvas = tk.Canvas(self.frame, width=40, height=150,
                               bg="#0a0a0a", highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        
        # Background bar
        self.canvas.create_rectangle(10, 10, 30, 140, outline="#333", fill="#1a1a1a")
        
        # Value bar
        self.bar = self.canvas.create_rectangle(10, 140, 30, 140,
                                                fill=color, outline=color)
        
        # Value label
        self.value_label = tk.Label(self.frame, text="0", fg=color,
                                    bg="#0a0a0a", font=("Courier", 9, "bold"))
        self.value_label.pack()
    
    def set_value(self, value):
        value = max(0, min(value, self.max_value))
        height = int(130 * value / self.max_value)
        self.canvas.coords(self.bar, 10, 140 - height, 30, 140)
        self.value_label.config(text=str(value))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


# ============================================================================
# COMPUTER SYSTEM
# ============================================================================

class Computer:
    """Enhanced computer with all features"""
    def __init__(self):
        self.memory = [0] * 16
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.bus = 0
        self.sp = 15
        self.output = 0
        
        self.carry_flag = False
        self.zero_flag = False
        self.negative_flag = False
        self.overflow_flag = False
        
        self.halted = False
        self.running = False
        
        self.control_signals = {
            'MI': False, 'RI': False, 'RO': False, 'II': False, 'IO': False,
            'AI': False, 'AO': False, 'EO': False, 'SU': False, 'BI': False,
            'OI': False, 'CE': False, 'CO': False, 'J': False, 'FI': False
        }
        
        self.instruction_count = 0
        self.cycle_count = 0
    
    def reset(self):
        self.reg_a = 0
        self.reg_b = 0
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.bus = 0
        self.sp = 15
        self.output = 0
        self.carry_flag = False
        self.zero_flag = False
        self.negative_flag = False
        self.overflow_flag = False
        self.halted = False
        self.running = False
        self.instruction_count = 0
        self.cycle_count = 0
        for key in self.control_signals:
            self.control_signals[key] = False
    
    def load_program(self, program):
        for addr, value in program.items():
            if 0 <= addr < 16:
                self.memory[addr] = value & 0xFF
    
    def step(self):
        if self.halted:
            return False
        
        for key in self.control_signals:
            self.control_signals[key] = False
        
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
        
        # Execute
        opcode = (self.ir >> 4) & 0x0F
        operand = self.ir & 0x0F
        
        if opcode == 0x1:  # LDA
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
            self.overflow_flag = result > 255
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
            self.negative_flag = result < 0
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
            self.output = self.reg_a
        elif opcode == 0xF:  # HLT
            self.halted = True
            return False
        
        self.instruction_count += 1
        self.cycle_count += 1
        return True



# ============================================================================
# SETTINGS WINDOW
# ============================================================================

class SettingsWindow:
    """Settings and preferences window"""
    def __init__(self, parent, settings):
        self.window = tk.Toplevel(parent)
        self.window.title("Settings & Preferences")
        self.window.configure(bg="#1a1a1a")
        self.window.geometry("600x700")
        
        self.settings = settings
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display Settings Tab
        display_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(display_frame, text="Display")
        self.create_display_settings(display_frame)
        
        # Sound Settings Tab
        sound_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(sound_frame, text="Sound")
        self.create_sound_settings(sound_frame)
        
        # Color Settings Tab
        color_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(color_frame, text="Colors")
        self.create_color_settings(color_frame)
        
        # Performance Settings Tab
        perf_frame = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(perf_frame, text="Performance")
        self.create_performance_settings(perf_frame)
        
        # Buttons
        btn_frame = tk.Frame(self.window, bg="#1a1a1a")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Save", command=self.save_settings,
                 bg="#00ff00", fg="black", font=("Courier", 11, "bold"),
                 width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=self.window.destroy,
                 bg="#ff0000", fg="white", font=("Courier", 11, "bold"),
                 width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Reset Defaults", command=self.reset_defaults,
                 bg="#ffff00", fg="black", font=("Courier", 11, "bold"),
                 width=15).pack(side=tk.LEFT, padx=5)
    
    def create_display_settings(self, parent):
        """Display settings"""
        tk.Label(parent, text="Display Settings", fg="#00ff00", bg="#1a1a1a",
                font=("Courier", 14, "bold")).pack(pady=10)
        
        # LED size
        frame = tk.Frame(parent, bg="#1a1a1a")
        frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(frame, text="LED Size:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT)
        self.led_size_var = tk.IntVar(value=self.settings.get('led_size', 15))
        tk.Scale(frame, from_=10, to=30, orient=tk.HORIZONTAL,
                variable=self.led_size_var, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
        
        # LCD font size
        frame = tk.Frame(parent, bg="#1a1a1a")
        frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(frame, text="LCD Font Size:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT)
        self.lcd_font_var = tk.IntVar(value=self.settings.get('lcd_font', 10))
        tk.Scale(frame, from_=8, to=16, orient=tk.HORIZONTAL,
                variable=self.lcd_font_var, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
        
        # Show tooltips
        self.tooltips_var = tk.BooleanVar(value=self.settings.get('tooltips', True))
        tk.Checkbutton(parent, text="Show Tooltips", variable=self.tooltips_var,
                      fg="white", bg="#1a1a1a", selectcolor="#0a0a0a",
                      font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
        
        # Show grid
        self.grid_var = tk.BooleanVar(value=self.settings.get('show_grid', False))
        tk.Checkbutton(parent, text="Show Grid Lines", variable=self.grid_var,
                      fg="white", bg="#1a1a1a", selectcolor="#0a0a0a",
                      font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
        
        # Animation speed
        frame = tk.Frame(parent, bg="#1a1a1a")
        frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(frame, text="Animation Speed:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT)
        self.anim_speed_var = tk.DoubleVar(value=self.settings.get('anim_speed', 1.0))
        tk.Scale(frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                variable=self.anim_speed_var, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
    
    def create_sound_settings(self, parent):
        """Sound settings"""
        tk.Label(parent, text="Sound Settings", fg="#00ff00", bg="#1a1a1a",
                font=("Courier", 14, "bold")).pack(pady=10)
        
        # Master volume
        frame = tk.Frame(parent, bg="#1a1a1a")
        frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(frame, text="Master Volume:", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT)
        self.volume_var = tk.DoubleVar(value=self.settings.get('volume', 0.5))
        tk.Scale(frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                variable=self.volume_var, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
        
        # Individual sound toggles
        self.sound_click_var = tk.BooleanVar(value=self.settings.get('sound_click', True))
        tk.Checkbutton(parent, text="Click Sounds", variable=self.sound_click_var,
                      fg="white", bg="#1a1a1a", selectcolor="#0a0a0a",
                      font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
        
        self.sound_read_var = tk.BooleanVar(value=self.settings.get('sound_read', True))
        tk.Checkbutton(parent, text="Read Sounds", variable=self.sound_read_var,
                      fg="white", bg="#1a1a1a", selectcolor="#0a0a0a",
                      font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
        
        self.sound_write_var = tk.BooleanVar(value=self.settings.get('sound_write', True))
        tk.Checkbutton(parent, text="Write Sounds", variable=self.sound_write_var,
                      fg="white", bg="#1a1a1a", selectcolor="#0a0a0a",
                      font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
        
        self.sound_pong_var = tk.BooleanVar(value=self.settings.get('sound_pong', True))
        tk.Checkbutton(parent, text="Pong Sounds", variable=self.sound_pong_var,
                      fg="white", bg="#1a1a1a", selectcolor="#0a0a0a",
                      font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
    
    def create_color_settings(self, parent):
        """Color settings"""
        tk.Label(parent, text="Color Settings", fg="#00ff00", bg="#1a1a1a",
                font=("Courier", 14, "bold")).pack(pady=10)
        
        colors = [
            ("Bus LEDs", "bus_color", "#00ff00"),
            ("Register LEDs", "reg_color", "#ff0000"),
            ("PC LEDs", "pc_color", "#ffff00"),
            ("Control Signals", "control_color", "#ffff00"),
            ("LCD Background", "lcd_bg", "#0a3d0a"),
            ("LCD Foreground", "lcd_fg", "#00ff00")
        ]
        
        self.color_vars = {}
        for label, key, default in colors:
            frame = tk.Frame(parent, bg="#1a1a1a")
            frame.pack(pady=5, fill=tk.X, padx=20)
            
            tk.Label(frame, text=label + ":", fg="white", bg="#1a1a1a",
                    font=("Courier", 10), width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            color = self.settings.get(key, default)
            self.color_vars[key] = tk.StringVar(value=color)
            
            color_btn = tk.Button(frame, text="  ", bg=color, width=3,
                                 command=lambda k=key: self.choose_color(k))
            color_btn.pack(side=tk.LEFT, padx=5)
            
            tk.Label(frame, textvariable=self.color_vars[key], fg="white",
                    bg="#1a1a1a", font=("Courier", 9)).pack(side=tk.LEFT)
    
    def create_performance_settings(self, parent):
        """Performance settings"""
        tk.Label(parent, text="Performance Settings", fg="#00ff00", bg="#1a1a1a",
                font=("Courier", 14, "bold")).pack(pady=10)
        
        # Max clock speed
        frame = tk.Frame(parent, bg="#1a1a1a")
        frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(frame, text="Max Clock Speed (Hz):", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT)
        self.max_clock_var = tk.DoubleVar(value=self.settings.get('max_clock', 10.0))
        tk.Scale(frame, from_=1.0, to=100.0, resolution=1.0, orient=tk.HORIZONTAL,
                variable=self.max_clock_var, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
        
        # Update rate
        frame = tk.Frame(parent, bg="#1a1a1a")
        frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(frame, text="Display Update Rate (ms):", fg="white", bg="#1a1a1a",
                font=("Courier", 10)).pack(side=tk.LEFT)
        self.update_rate_var = tk.IntVar(value=self.settings.get('update_rate', 50))
        tk.Scale(frame, from_=10, to=200, resolution=10, orient=tk.HORIZONTAL,
                variable=self.update_rate_var, bg="#1a1a1a", fg="white").pack(side=tk.LEFT)
        
        # Enable optimizations
        self.optimize_var = tk.BooleanVar(value=self.settings.get('optimize', True))
        tk.Checkbutton(parent, text="Enable Performance Optimizations",
                      variable=self.optimize_var, fg="white", bg="#1a1a1a",
                      selectcolor="#0a0a0a", font=("Courier", 10)).pack(pady=5, anchor=tk.W, padx=20)
    
    def choose_color(self, key):
        """Choose color"""
        color = colorchooser.askcolor(self.color_vars[key].get())[1]
        if color:
            self.color_vars[key].set(color)
    
    def save_settings(self):
        """Save settings"""
        self.settings['led_size'] = self.led_size_var.get()
        self.settings['lcd_font'] = self.lcd_font_var.get()
        self.settings['tooltips'] = self.tooltips_var.get()
        self.settings['show_grid'] = self.grid_var.get()
        self.settings['anim_speed'] = self.anim_speed_var.get()
        self.settings['volume'] = self.volume_var.get()
        self.settings['sound_click'] = self.sound_click_var.get()
        self.settings['sound_read'] = self.sound_read_var.get()
        self.settings['sound_write'] = self.sound_write_var.get()
        self.settings['sound_pong'] = self.sound_pong_var.get()
        self.settings['max_clock'] = self.max_clock_var.get()
        self.settings['update_rate'] = self.update_rate_var.get()
        self.settings['optimize'] = self.optimize_var.get()
        
        for key, var in self.color_vars.items():
            self.settings[key] = var.get()
        
        # Save to file
        with open('computer_settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)
        
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
        self.window.destroy()
    
    def reset_defaults(self):
        """Reset to defaults"""
        if messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            self.settings.clear()
            self.settings.update({
                'led_size': 15, 'lcd_font': 10, 'tooltips': True,
                'show_grid': False, 'anim_speed': 1.0, 'volume': 0.5,
                'sound_click': True, 'sound_read': True, 'sound_write': True,
                'sound_pong': True, 'max_clock': 10.0, 'update_rate': 50,
                'optimize': True
            })
            self.window.destroy()
            SettingsWindow(self.window.master, self.settings)



# ============================================================================
# MEMORY EDITOR WINDOW
# ============================================================================

class MemoryEditorWindow:
    """Advanced memory editor window"""
    def __init__(self, parent, computer):
        self.window = tk.Toplevel(parent)
        self.window.title("Memory Editor")
        self.window.configure(bg="#1a1a1a")
        self.window.geometry("800x600")
        
        self.computer = computer
        
        # Toolbar
        toolbar = tk.Frame(self.window, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(toolbar, text="Load", command=self.load_memory,
                 bg="#00ff00", fg="black", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Save", command=self.save_memory,
                 bg="#0066ff", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Clear", command=self.clear_memory,
                 bg="#ff0000", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Fill", command=self.fill_memory,
                 bg="#ffff00", fg="black", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Memory grid
        grid_frame = tk.Frame(self.window, bg="#1a1a1a")
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Headers
        tk.Label(grid_frame, text="Addr", fg="#ffff00", bg="#1a1a1a",
                font=("Courier", 10, "bold"), width=6).grid(row=0, column=0)
        tk.Label(grid_frame, text="Hex", fg="#00ff00", bg="#1a1a1a",
                font=("Courier", 10, "bold"), width=6).grid(row=0, column=1)
        tk.Label(grid_frame, text="Dec", fg="#00ffff", bg="#1a1a1a",
                font=("Courier", 10, "bold"), width=6).grid(row=0, column=2)
        tk.Label(grid_frame, text="Bin", fg="#ff00ff", bg="#1a1a1a",
                font=("Courier", 10, "bold"), width=12).grid(row=0, column=3)
        tk.Label(grid_frame, text="ASCII", fg="#ff6600", bg="#1a1a1a",
                font=("Courier", 10, "bold"), width=6).grid(row=0, column=4)
        tk.Label(grid_frame, text="Edit", fg="white", bg="#1a1a1a",
                font=("Courier", 10, "bold"), width=10).grid(row=0, column=5)
        
        # Memory cells
        self.entries = []
        for addr in range(16):
            # Address
            tk.Label(grid_frame, text=f"{addr:02d}", fg="#ffff00", bg="#0a0a0a",
                    font=("Courier", 9), width=6, relief=tk.SUNKEN).grid(row=addr+1, column=0, padx=2, pady=2)
            
            # Hex
            hex_label = tk.Label(grid_frame, text="00", fg="#00ff00", bg="#0a0a0a",
                                font=("Courier", 9), width=6, relief=tk.SUNKEN)
            hex_label.grid(row=addr+1, column=1, padx=2, pady=2)
            
            # Dec
            dec_label = tk.Label(grid_frame, text="0", fg="#00ffff", bg="#0a0a0a",
                                font=("Courier", 9), width=6, relief=tk.SUNKEN)
            dec_label.grid(row=addr+1, column=2, padx=2, pady=2)
            
            # Bin
            bin_label = tk.Label(grid_frame, text="00000000", fg="#ff00ff", bg="#0a0a0a",
                                font=("Courier", 9), width=12, relief=tk.SUNKEN)
            bin_label.grid(row=addr+1, column=3, padx=2, pady=2)
            
            # ASCII
            ascii_label = tk.Label(grid_frame, text=".", fg="#ff6600", bg="#0a0a0a",
                                   font=("Courier", 9), width=6, relief=tk.SUNKEN)
            ascii_label.grid(row=addr+1, column=4, padx=2, pady=2)
            
            # Edit entry
            entry = tk.Entry(grid_frame, width=10, bg="#0a0a0a", fg="white",
                           font=("Courier", 9), relief=tk.SUNKEN)
            entry.grid(row=addr+1, column=5, padx=2, pady=2)
            entry.bind('<Return>', lambda e, a=addr: self.update_memory(a))
            
            self.entries.append({
                'hex': hex_label, 'dec': dec_label, 'bin': bin_label,
                'ascii': ascii_label, 'entry': entry
            })
        
        # Update button
        tk.Button(self.window, text="Refresh Display", command=self.refresh,
                 bg="#0066ff", fg="white", font=("Courier", 11, "bold"),
                 width=20).pack(pady=10)
        
        self.refresh()
    
    def refresh(self):
        """Refresh memory display"""
        for addr in range(16):
            value = self.computer.memory[addr]
            self.entries[addr]['hex'].config(text=f"{value:02X}")
            self.entries[addr]['dec'].config(text=str(value))
            self.entries[addr]['bin'].config(text=f"{value:08b}")
            ascii_char = chr(value) if 32 <= value < 127 else '.'
            self.entries[addr]['ascii'].config(text=ascii_char)
            self.entries[addr]['entry'].delete(0, tk.END)
            self.entries[addr]['entry'].insert(0, str(value))
    
    def update_memory(self, addr):
        """Update memory from entry"""
        try:
            value_str = self.entries[addr]['entry'].get()
            if value_str.startswith('0x'):
                value = int(value_str, 16)
            elif value_str.startswith('0b'):
                value = int(value_str, 2)
            else:
                value = int(value_str)
            
            self.computer.memory[addr] = value & 0xFF
            self.refresh()
        except ValueError:
            messagebox.showerror("Error", "Invalid value")
    
    def load_memory(self):
        """Load memory from file"""
        filename = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'rb') as f:
                    data = f.read()
                    for i, byte in enumerate(data[:16]):
                        self.computer.memory[i] = byte
                self.refresh()
                messagebox.showinfo("Success", f"Loaded {len(data)} bytes")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def save_memory(self):
        """Save memory to file"""
        filename = filedialog.asksaveasfilename(defaultextension=".bin",
                                               filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'wb') as f:
                    f.write(bytes(self.computer.memory))
                messagebox.showinfo("Success", "Memory saved")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def clear_memory(self):
        """Clear all memory"""
        if messagebox.askyesno("Clear Memory", "Clear all memory locations?"):
            for i in range(16):
                self.computer.memory[i] = 0
            self.refresh()
    
    def fill_memory(self):
        """Fill memory with pattern"""
        value = tk.simpledialog.askinteger("Fill Memory", "Enter fill value (0-255):",
                                          minvalue=0, maxvalue=255)
        if value is not None:
            for i in range(16):
                self.computer.memory[i] = value
            self.refresh()
