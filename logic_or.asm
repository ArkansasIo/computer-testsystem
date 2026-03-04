; OR GATE Implementation
; Output = 1 if at least one input is 1
; Truth table: 0 OR 0 = 0, 0 OR 1 = 1, 1 OR 0 = 1, 1 OR 1 = 1
; Implementation: A + B >= 1 means at least one is 1

0:  LDA 12   ; Load input A
1:  ADD 13   ; Add input B
2:  JZ 5     ; If sum is zero, both inputs are 0
3:  LDI 1    ; At least one input is 1
4:  JMP 6
5:  LDI 0    ; Both inputs are 0
6:  STA 14   ; Store result
7:  OUT      ; Display result
8:  HLT

; Data
12: 1        ; Input A
13: 0        ; Input B
14: 0        ; Result
15: 0        ; Unused
