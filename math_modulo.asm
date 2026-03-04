; Modulo Operation (Remainder)
; Calculates A mod B (remainder of A divided by B)
; Example: 17 mod 5 = 2 (because 17 = 3×5 + 2)
; Uses repeated subtraction
;
; Memory layout:
; 0-9: Program
; 12: Dividend (A) - modified during calculation
; 13: Divisor (B)
; 14: Quotient counter
; 15: Constant 1

0:  LDA 12   ; Load dividend
1:  SUB 13   ; Subtract divisor
2:  JC 5     ; If carry (no underflow), continue
3:  ADD 13   ; Restore (went negative)
4:  JMP 8    ; Done
5:  STA 12   ; Store reduced dividend
6:  JMP 0    ; Loop
8:  OUT      ; Display remainder
9:  HLT

; Data (17 mod 5 = 2)
12: 17       ; Dividend
13: 5        ; Divisor
14: 0        ; Quotient (not used here)
15: 1        ; Constant 1
