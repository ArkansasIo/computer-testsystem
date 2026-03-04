; Logic Gates Implementation
; Implements basic logic operations using the 8-bit computer
; All operations work on single bits (0 or 1)
;
; Memory layout:
; 12: Input A (0 or 1)
; 13: Input B (0 or 1)
; 14: Result
; 15: Temporary/Constants

; ===== AND GATE =====
; Output = 1 only if both inputs are 1
; Truth table: 0 AND 0 = 0, 0 AND 1 = 0, 1 AND 0 = 0, 1 AND 1 = 1
; Implementation: A + B = 2 when both are 1
0:  LDA 12   ; Load input A
1:  ADD 13   ; Add input B
2:  SUB 15   ; Subtract 2 (stored at address 15)
3:  JZ 6     ; If zero, both inputs were 1
4:  LDI 0    ; Otherwise result is 0
5:  JMP 7
6:  LDI 1    ; Both inputs are 1, result is 1
7:  STA 14   ; Store result
8:  OUT      ; Display result
9:  HLT

; Data
12: 1        ; Input A (change to test)
13: 1        ; Input B (change to test)
14: 0        ; Result
15: 2        ; Constant for AND operation
