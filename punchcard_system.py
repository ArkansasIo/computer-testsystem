#!/usr/bin/env python3
"""
Punch Card Assembly Input System
Retro-style punch card interface for programming the 8-bit computer
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json


class PunchCard:
    """Single punch card representation"""
    def __init__(self, parent, card_number=0, callback=None):
        self.frame = tk.Frame(parent, bg="#d4c5a0", relief=tk.RAISED, bd=3)
        self.card_number = card_number
        self.callback = callback
        
        # Card header
        header = tk.Frame(self.frame, bg="#b8a080")
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"CARD #{card_number:03d}", 
                font=("Courier", 10, "bold"), bg="#b8a080").pack(side=tk.LEFT, padx=5)
        
        # Punch area (8 columns for 8-bit data)
        punch_frame = tk.Frame(self.frame, bg="#d4c5a0")
        punch_frame.pack(pady=10, padx=10)
        
        # Column labels
        label_frame = tk.Frame(punch_frame, bg="#d4c5a0")
        label_frame.pack()
        
        for i in range(7, -1, -1):
            tk.Label(label_frame, text=f"B{i}", font=("Courier", 8, "bold"),
                    bg="#d4c5a0", width=4).pack(side=tk.LEFT, padx=2)
        
        # Punch holes
        self.holes = []
        hole_frame = tk.Frame(punch_frame, bg="#d4c5a0")
        hole_frame.pack()
        
        for i in range(7, -1, -1):
            canvas = tk.Canvas(hole_frame, width=30, height=30, bg="#d4c5a0",
                             highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=2)
            
            # Draw hole
            hole = canvas.create_oval(5, 5, 25, 25, fill="#d4c5a0", 
                                     outline="#8b7355", width=2)
            canvas.bind('<Button-1>', lambda e, idx=i: self.toggle_hole(idx))
            
            self.holes.insert(0, {'canvas': canvas, 'hole': hole, 'punched': False})
        
        # Value display
        self.value_label = tk.Label(self.frame, text="Value: 0x00 (0)",
                                   font=("Courier", 9), bg="#d4c5a0")
        self.value_label.pack(pady=5)
        
        # Instruction display
        self.instr_label = tk.Label(self.frame, text="NOP",
                                    font=("Courier", 9, "bold"), bg="#d4c5a0",
                                    fg="#8b0000")
        self.instr_label.pack(pady=2)
