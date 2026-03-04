; Sum of Sequence
; Calculates 1 + 2 + 3 + 4 + 5 = 15
; Demonstrates accumulation pattern
;
; Memory layout:
; 0-9: Program
; 13: Counter (starts at 5, counts down)
; 14: Accumulator (sum result)
; 15: Constant 1 for decrementing

0:  LDA 14   ; 0001 1110 - Load accumulator
1:  ADD 13   ; 0010 1101 - Add current counter value
2:  STA 14   ; 0100 1110 - Store back to accumulator
3:  LDA 13   ; 0001 1101 - Load counter
4:  SUB 15   ; 0011 1111 - Decrement counter
5:  STA 13   ; 0100 1101 - Store decremented counter
6:  JZ 9     ; 1000 1001 - If zero, jump to output
7:  JMP 0    ; 0110 0000 - Loop back
9:  LDA 14   ; 0001 1110 - Load final sum
10: OUT      ; 1110 0000 - Display result (15)
11: HLT      ; 1111 0000 - Halt

; Data section
13: 5        ; 0000 0101 - Counter (start at 5)
14: 0        ; 0000 0000 - Accumulator (starts at 0)
15: 1        ; 0000 0001 - Decrement constant

; Machine code (binary):
; Address | Binary      | Hex | Decimal
; --------|-------------|-----|--------
; 0       | 0001 1110   | 1E  | 30
; 1       | 0010 1101   | 2D  | 45
; 2       | 0100 1110   | 4E  | 78
; 3       | 0001 1101   | 1D  | 29
; 4       | 0011 1111   | 3F  | 63
; 5       | 0100 1101   | 4D  | 77
; 6       | 1000 1001   | 89  | 137
; 7       | 0110 0000   | 60  | 96
; 9       | 0001 1110   | 1E  | 30
; 10      | 1110 0000   | E0  | 224
; 11      | 1111 0000   | F0  | 240
; 13      | 0000 0101   | 05  | 5
; 14      | 0000 0000   | 00  | 0
; 15      | 0000 0001   | 01  | 1
