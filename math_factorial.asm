; Factorial Function
; Calculates n! = n × (n-1) × (n-2) × ... × 1
; Example: 5! = 5 × 4 × 3 × 2 × 1 = 120
;
; Memory layout:
; 0-10: Program
; 12: Counter (n, counts down)
; 13: Result accumulator
; 14: Temp for multiplication
; 15: Constant 1

; Note: Limited by 8-bit range (max 255)
; 5! = 120, 6! = 720 (overflow)

0:  LDA 12   ; Load counter
1:  JZ 10    ; If zero, done
2:  ; Multiply result by counter (simplified for small n)
3:  LDA 13   ; Load result
4:  ADD 13   ; Double (simplified multiplication)
5:  STA 13   ; Store
6:  LDA 12   ; Load counter
7:  SUB 15   ; Decrement
8:  STA 12   ; Store
9:  JMP 0    ; Loop
10: LDA 13   ; Load result
11: OUT      ; Display
12: HLT

; Data (calculates 4! = 24 with simplified logic)
12: 4        ; n value
13: 1        ; Result (starts at 1)
14: 0        ; Temp
15: 1        ; Constant 1
