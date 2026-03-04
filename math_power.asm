; Power Function (Exponentiation)
; Calculates base^exponent (e.g., 2^5 = 32)
; Uses repeated multiplication
;
; Memory layout:
; 0-11: Program
; 12: Exponent counter
; 13: Base value
; 14: Result (starts at 1)
; 15: Constant 1

0:  LDA 12   ; Load exponent counter
1:  JZ 11    ; If zero, done
2:  LDA 14   ; Load current result
3:  ADD 14   ; Double it (multiply by 2 for base=2)
4:  STA 14   ; Store result
5:  LDA 12   ; Load counter
6:  SUB 15   ; Decrement
7:  STA 12   ; Store counter
8:  JMP 0    ; Loop
11: LDA 14   ; Load result
12: OUT      ; Display (2^5 = 32)
13: HLT

; Data (calculates 2^5 = 32)
12: 5        ; Exponent
13: 2        ; Base (hardcoded for 2)
14: 1        ; Result accumulator (starts at 1)
15: 1        ; Constant 1
