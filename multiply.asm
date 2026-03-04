; Multiply Two Numbers
; Multiplies 5 × 7 = 35 using repeated addition
; Algorithm: result = 0; for(i=0; i<multiplier; i++) result += multiplicand
;
; Memory layout:
; 0-11: Program
; 12: Counter (multiplier = 7)
; 13: Multiplicand (5)
; 14: Result accumulator (starts at 0)
; 15: Constant 1 for decrementing

0:  LDA 12   ; 0001 1100 - Load counter into A
1:  JZ 11    ; 1000 1011 - If counter is zero, jump to output
2:  LDA 14   ; 0001 1110 - Load result into A
3:  ADD 13   ; 0010 1101 - Add multiplicand to result
4:  STA 14   ; 0100 1110 - Store back to result
5:  LDA 12   ; 0001 1100 - Load counter
6:  SUB 15   ; 0011 1111 - Subtract 1 from counter
7:  STA 12   ; 0100 1100 - Store decremented counter
8:  JMP 0    ; 0110 0000 - Loop back to start
11: LDA 14   ; 0001 1110 - Load final result
12: OUT      ; 1110 0000 - Display result (35)
13: HLT      ; 1111 0000 - Halt

; Data section
12: 7        ; 0000 0111 - Multiplier (7)
13: 5        ; 0000 0101 - Multiplicand (5)
14: 0        ; 0000 0000 - Result accumulator
15: 1        ; 0000 0001 - Constant 1 for decrementing

; Machine code (binary):
; Address | Binary      | Hex | Decimal
; --------|-------------|-----|--------
; 0       | 0001 1100   | 1C  | 28
; 1       | 1000 1011   | 8B  | 139
; 2       | 0001 1110   | 1E  | 30
; 3       | 0010 1101   | 2D  | 45
; 4       | 0100 1110   | 4E  | 78
; 5       | 0001 1100   | 1C  | 28
; 6       | 0011 1111   | 3F  | 63
; 7       | 0100 1100   | 4C  | 76
; 8       | 0110 0000   | 60  | 96
; 11      | 0001 1110   | 1E  | 30
; 12      | 1110 0000   | E0  | 224
; 13      | 1111 0000   | F0  | 240
; 12      | 0000 0111   | 07  | 7
; 13      | 0000 0101   | 05  | 5
; 14      | 0000 0000   | 00  | 0
; 15      | 0000 0001   | 01  | 1
