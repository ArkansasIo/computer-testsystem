; XOR GATE Implementation
; Output = 1 if inputs are different
; Truth table: 0 XOR 0 = 0, 0 XOR 1 = 1, 1 XOR 0 = 1, 1 XOR 1 = 0
; Implementation: A + B = 1 means exactly one is 1

0:  LDA 12   ; Load input A
1:  ADD 13   ; Add input B
2:  SUB 15   ; Subtract 1
3:  JZ 6     ; If zero, exactly one input is 1
4:  LDI 0    ; Inputs are same (both 0 or both 1)
5:  JMP 7
6:  LDI 1    ; Inputs are different
7:  STA 14   ; Store result
8:  OUT      ; Display result
9:  HLT

; Data
12: 1        ; Input A
13: 0        ; Input B
14: 0        ; Result
15: 1        ; Constant 1
