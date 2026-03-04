; Blink Pattern Generator
; Displays a sequence of numbers: 1, 2, 4, 8 (powers of 2)
; Creates a visual pattern on the 7-segment display
;
; Memory layout:
; 0-10: Program
; 13: Current value
; 14: Maximum value (8)
; 15: Constant 1 for reset

0:  LDA 13   ; 0001 1101 - Load current value
1:  OUT      ; 1110 0000 - Display value
2:  ADD 13   ; 0010 1101 - Double the value (shift left)
3:  STA 13   ; 0100 1101 - Store doubled value
4:  SUB 14   ; 0011 1110 - Compare with max (8)
5:  JZ 8     ; 1000 1000 - If equal to 8, reset
6:  JMP 0    ; 0110 0000 - Continue pattern
8:  LDA 15   ; 0001 1111 - Load 1
9:  STA 13   ; 0100 1101 - Reset to 1
10: JMP 0    ; 0110 0000 - Restart pattern

; Data section
13: 1        ; 0000 0001 - Current value (start with 1)
14: 9        ; 0000 1001 - Maximum value + 1 (for comparison)
15: 1        ; 0000 0001 - Reset value

; Machine code (binary):
; Address | Binary      | Hex | Decimal
; --------|-------------|-----|--------
; 0       | 0001 1101   | 1D  | 29
; 1       | 1110 0000   | E0  | 224
; 2       | 0010 1101   | 2D  | 45
; 3       | 0100 1101   | 4D  | 77
; 4       | 0011 1110   | 3E  | 62
; 5       | 1000 1000   | 88  | 136
; 6       | 0110 0000   | 60  | 96
; 8       | 0001 1111   | 1F  | 31
; 9       | 0100 1101   | 4D  | 77
; 10      | 0110 0000   | 60  | 96
; 13      | 0000 0001   | 01  | 1
; 14      | 0000 1001   | 09  | 9
; 15      | 0000 0001   | 01  | 1
