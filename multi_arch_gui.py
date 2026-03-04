#!/usr/bin/env python3
"""
Multi-Architecture Computer GUI
Supports 8, 16, 32, 64, 128, and 256-bit architectures
with extended register sets (A-Z) and enhanced features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from computer_architectures import *

class MultiArchGUI:
    """GUI for multi-architecture computer system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Architecture Computer System")
        self.root.configure(bg="#1a1a1a")
        
        # Current architecture
        self.arch_type = "8-bit"
        self.computer = Computer8Bit()
        
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container with scrollbar
        main_canvas = tk.Canvas(self.root, bg="#1a1a1a")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#1a1a1a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        title_frame = tk.Frame(scrollable_frame, bg="#1a1a1a")
        title_frame.pack(pady=10)
        
        title = tk.Label(title_frame, text="MULTI-ARCHITECTURE COMPUTER", 
                        font=("Courier", 20, "bold"), fg="#00ff00", bg="#1a1a1a")
        title.pack()
        
        # Architecture selector
        arch_frame = tk.LabelFrame(scrollable_frame, text="ARCHITECTURE", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 12, "bold"))
        arch_frame.pack(pady=10, padx=20, fill="x")
        
        arch_buttons = tk.Frame(arch_frame, bg="#1a1a1a")
        arch_buttons.pack(pady=10)
        
        architectures = ["8-bit", "16-bit", "32-bit", "64-bit", "128-bit", "256-bit"]
        for arch in architectures:
            btn = tk.Button(arch_buttons, text=arch, command=lambda a=arch: self.switch_architecture(a),
                          bg="#333", fg="white", font=("Courier", 10, "bold"), width=10)
            btn.pack(side=tk.LEFT, padx=5)
        
        self.arch_label = tk.Label(arch_frame, text="Current: 8-bit", 
                                   fg="#00ff00", bg="#1a1a1a", font=("Courier", 12))
        self.arch_label.pack(pady=5)
        
        # System info
        info_frame = tk.LabelFrame(scrollable_frame, text="SYSTEM INFO", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        info_frame.pack(pady=10, padx=20, fill="x")
        
        self.info_text = tk.Text(info_frame, height=6, width=80, bg="#000", fg="#00ff00",
                                font=("Courier", 9), relief=tk.FLAT)
        self.info_text.pack(pady=5, padx=5)
        
        # Register display (A-Z)
        reg_frame = tk.LabelFrame(scrollable_frame, text="REGISTERS (A-Z)", 
                                 fg="white", bg="#1a1a1a", font=("Courier", 12, "bold"))
        reg_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Create scrolled text for registers
        self.reg_display = scrolledtext.ScrolledText(reg_frame, height=15, width=100,
                                                     bg="#000", fg="#00ff00",
                                                     font=("Courier", 9))
        self.reg_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Special registers
        special_frame = tk.LabelFrame(scrollable_frame, text="SPECIAL REGISTERS", 
                                     fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        special_frame.pack(pady=10, padx=20, fill="x")
        
        special_grid = tk.Frame(special_frame, bg="#1a1a1a")
        special_grid.pack(pady=5)
        
        self.pc_label = tk.Label(special_grid, text="PC: 0", fg="#ffff00", bg="#000",
                                font=("Courier", 10, "bold"), width=20, anchor="w")
        self.pc_label.grid(row=0, column=0, padx=5, pady=2)
        
        self.sp_label = tk.Label(special_grid, text="SP: 0", fg="#ffff00", bg="#000",
                                font=("Courier", 10, "bold"), width=20, anchor="w")
        self.sp_label.grid(row=0, column=1, padx=5, pady=2)
        
        self.mar_label = tk.Label(special_grid, text="MAR: 0", fg="#ffff00", bg="#000",
                                 font=("Courier", 10, "bold"), width=20, anchor="w")
        self.mar_label.grid(row=1, column=0, padx=5, pady=2)
        
        self.ir_label = tk.Label(special_grid, text="IR: 0", fg="#ffff00", bg="#000",
                                font=("Courier", 10, "bold"), width=20, anchor="w")
        self.ir_label.grid(row=1, column=1, padx=5, pady=2)
        
        # Flags
        flag_frame = tk.LabelFrame(scrollable_frame, text="FLAGS", 
                                  fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        flag_frame.pack(pady=10, padx=20, fill="x")
        
        flag_grid = tk.Frame(flag_frame, bg="#1a1a1a")
        flag_grid.pack(pady=5)
        
        self.flag_labels = {}
        flags = [("Zero", "Z"), ("Carry", "C"), ("Negative", "N"), 
                ("Overflow", "O"), ("Parity", "P")]
        
        for i, (name, abbr) in enumerate(flags):
            label = tk.Label(flag_grid, text=f"{abbr}: 0", fg="#ff00ff", bg="#000",
                           font=("Courier", 10, "bold"), width=10)
            label.grid(row=0, column=i, padx=5)
            self.flag_labels[abbr] = label
        
        # Memory viewer
        mem_frame = tk.LabelFrame(scrollable_frame, text="MEMORY VIEWER", 
                                 fg="white", bg="#1a1a1a", font=("Courier", 10, "bold"))
        mem_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        mem_controls = tk.Frame(mem_frame, bg="#1a1a1a")
        mem_controls.pack(pady=5)
        
        tk.Label(mem_controls, text="Address:", fg="white", bg="#1a1a1a",
                font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        
        self.mem_addr_entry = tk.Entry(mem_controls, width=10, bg="#000", fg="#00ff00",
                                       font=("Courier", 10))
        self.mem_addr_entry.insert(0, "0")
        self.mem_addr_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(mem_controls, text="View", command=self.view_memory,
                 bg="#0066ff", fg="white", font=("Courier", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.mem_display = scrolledtext.ScrolledText(mem_frame, height=10, width=100,
                                                     bg="#000", fg="#00ff00",
                                                     font=("Courier", 8))
        self.mem_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Output display
        output_frame = tk.LabelFrame(scrollable_frame, text="OUTPUT", 
                                    fg="white", bg="#1a1a1a", font=("Courier", 12, "bold"))
        output_frame.pack(pady=10, padx=20, fill="x")
        
        self.output_label = tk.Label(output_frame, text="0", fg="#ff0000", bg="#000",
                                    font=("Courier", 24, "bold"), width=20)
        self.output_label.pack(pady=10)
        
        # Control buttons
        control_frame = tk.Frame(scrollable_frame, bg="#1a1a1a")
        control_frame.pack(pady=20)
        
        buttons = [
            ("STEP", self.step, "#0066ff"),
            ("RUN", self.run, "#00ff00"),
            ("RESET", self.reset, "#ff0000"),
            ("LOAD", self.load_program, "#ffff00")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(control_frame, text=text, command=command,
                          bg=color, fg="black" if color == "#ffff00" or color == "#00ff00" else "white",
                          font=("Courier", 12, "bold"), width=10, height=2)
            btn.pack(side=tk.LEFT, padx=5)
        
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
        self.update_display()
        messagebox.showinfo("Architecture Changed", 
                          f"Switched to {arch_type} architecture\n"
                          f"Bit Width: {self.computer.bit_width}\n"
                          f"Memory: {self.computer.memory_size:,} bytes\n"
                          f"Registers: {self.computer.num_registers}")
    
    def update_display(self):
        """Update all displays"""
        # System info
        self.info_text.delete(1.0, tk.END)
        info = f"""Architecture: {self.arch_type}
Bit Width: {self.computer.bit_width} bits
Max Value: {self.computer.max_value:,}
Memory Size: {self.computer.memory_size:,} bytes
Registers: {self.computer.num_registers} (A-Z)
Status: {'HALTED' if self.computer.halted else 'RUNNING' if self.computer.running else 'READY'}"""
        self.info_text.insert(1.0, info)
        
        # Registers (A-Z)
        self.reg_display.delete(1.0, tk.END)
        reg_text = "Register Values:\n" + "=" * 80 + "\n"
        
        for i in range(self.computer.num_registers):
            reg_name = chr(ord('A') + i)
            value = self.computer.registers[i]
            hex_val = f"0x{value:0{self.computer.bit_width//4}X}"
            
            reg_text += f"{reg_name}: {value:20,} {hex_val:>20}    "
            
            if (i + 1) % 3 == 0:
                reg_text += "\n"
        
        self.reg_display.insert(1.0, reg_text)
        
        # Special registers
        self.pc_label.config(text=f"PC: {self.computer.pc}")
        self.sp_label.config(text=f"SP: {self.computer.sp}")
        self.mar_label.config(text=f"MAR: {self.computer.mar}")
        self.ir_label.config(text=f"IR: 0x{self.computer.ir:02X}")
        
        # Flags
        self.flag_labels['Z'].config(text=f"Z: {int(self.computer.zero_flag)}")
        self.flag_labels['C'].config(text=f"C: {int(self.computer.carry_flag)}")
        self.flag_labels['N'].config(text=f"N: {int(self.computer.negative_flag)}")
        self.flag_labels['O'].config(text=f"O: {int(self.computer.overflow_flag)}")
        self.flag_labels['P'].config(text=f"P: {int(self.computer.parity_flag)}")
        
        # Output
        self.output_label.config(text=str(self.computer.registers[0]))
        
    def view_memory(self):
        """View memory contents"""
        try:
            start_addr = int(self.mem_addr_entry.get())
            self.mem_display.delete(1.0, tk.END)
            
            mem_text = f"Memory View (starting at {start_addr}):\n" + "=" * 80 + "\n"
            
            for i in range(min(256, self.computer.memory_size - start_addr)):
                addr = start_addr + i
                value = self.computer.memory[addr]
                
                if i % 16 == 0:
                    mem_text += f"\n{addr:08X}: "
                
                mem_text += f"{value:02X} "
            
            self.mem_display.insert(1.0, mem_text)
        except ValueError:
            messagebox.showerror("Error", "Invalid address")
    
    def step(self):
        """Execute one instruction"""
        if not self.computer.halted:
            # Simplified step for demo
            self.computer.pc = (self.computer.pc + 1) % self.computer.memory_size
            self.update_display()
    
    def run(self):
        """Run program"""
        messagebox.showinfo("Run", "Run mode not fully implemented in this demo")
    
    def reset(self):
        """Reset computer"""
        self.computer.reset()
        self.update_display()
    
    def load_program(self):
        """Load program"""
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
                    self.reset()
                    messagebox.showinfo("Success", f"Loaded {len(data)} bytes")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")


def main():
    root = tk.Tk()
    root.geometry("1200x900")
    app = MultiArchGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
