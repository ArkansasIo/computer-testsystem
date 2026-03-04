; NOT GATE Implementation
; Output = opposite of input
; Truth table: NOT 0 = 1, NOT 1 = 0
; Implementation: 1 - A

0:  LDA 15   ; Load 1
1:  SUB 12   ; Subtract input A
2:  STA 14   ; Store result
3:  OUT      ; Display result
4:  HLT

; Data
12: 0        ; Input A (change to test)
13: 0        ; Unused
14: 0        ; Result
15: 1        ; Constant 1
