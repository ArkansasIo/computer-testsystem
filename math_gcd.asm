; Greatest Common Divisor (GCD)
; Euclidean algorithm: GCD(a,b) = GCD(b, a mod b)
; Example: GCD(48, 18) = 6
;
; Simplified version using subtraction method:
; Repeatedly subtract smaller from larger until equal
;
; Memory layout:
; 0-11: Program
; 12: Value A
; 13: Value B
; 14: Temp
; 15: Constant 1

0:  LDA 12   ; Load A
1:  SUB 13   ; A - B
2:  JZ 11    ; If equal, found GCD
3:  JC 7     ; If A > B, continue
4:  ADD 13   ; Restore A (was smaller)
5:  STA 13   ; B = old A
6:  JMP 0    ; Swap and retry
7:  STA 12   ; A = A - B
8:  JMP 0    ; Loop
11: LDA 12   ; Load GCD
12: OUT      ; Display
13: HLT

; Data (GCD of 12 and 8 = 4)
12: 12       ; Value A
13: 8        ; Value B
14: 0        ; Temp
15: 1        ; Constant 1
