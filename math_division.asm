; Division Operation (Integer Division)
; Calculates A / B (quotient only, no remainder)
; Example: 20 / 4 = 5
; Uses repeated subtraction
;
; Memory layout:
; 0-10: Program
; 12: Dividend (A) - modified during calculation
; 13: Divisor (B)
; 14: Quotient counter
; 15: Constant 1

0:  LDA 12   ; Load dividend
1:  SUB 13   ; Subtract divisor
2:  JC 7     ; If carry (no underflow), continue
3:  LDA 14   ; Load quotient
4:  OUT      ; Display result
5:  HLT      ; Done
7:  STA 12   ; Store reduced dividend
8:  LDA 14   ; Load quotient
9:  ADD 15   ; Increment quotient
10: STA 14   ; Store quotient
11: JMP 0    ; Loop

; Data (20 / 4 = 5)
12: 20       ; Dividend
13: 4        ; Divisor
14: 0        ; Quotient counter
15: 1        ; Constant 1
