; Add Two Numbers
; Adds 28 + 14 and displays result (42)
; 
; Memory layout:
; 0-2: Program instructions
; 14-15: Data values

0: LDA 14    ; 0001 1110 - Load value 28 from address 14 into A
1: ADD 15    ; 0010 1111 - Add value 14 from address 15 to A
2: OUT       ; 1110 0000 - Display result (42) on 7-segment display
3: HLT       ; 1111 0000 - Halt execution

; Data section
14: 28       ; 0001 1100 - First number (decimal 28)
15: 14       ; 0000 1110 - Second number (decimal 14)

; Machine code (binary):
; Address | Binary      | Hex | Decimal
; --------|-------------|-----|--------
; 0       | 0001 1110   | 1E  | 30
; 1       | 0010 1111   | 2F  | 47
; 2       | 1110 0000   | E0  | 224
; 3       | 1111 0000   | F0  | 240
; 14      | 0001 1100   | 1C  | 28
; 15      | 0000 1110   | 0E  | 14
