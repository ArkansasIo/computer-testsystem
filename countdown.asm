; Countdown Timer
; Counts down from 10 to 0 and displays each number
;
; Memory layout:
; 0-7: Program
; 14: Counter (starts at 10)
; 15: Constant 1 for decrementing

0:  LDA 14   ; 0001 1110 - Load counter into A
1:  OUT      ; 1110 0000 - Display current count
2:  JZ 7     ; 1000 0111 - If zero, jump to halt
3:  SUB 15   ; 0011 1111 - Subtract 1 from counter
4:  STA 14   ; 0100 1110 - Store decremented value
5:  JMP 0    ; 0110 0000 - Loop back to start
7:  HLT      ; 1111 0000 - Halt when countdown reaches 0

; Data section
14: 10       ; 0000 1010 - Starting count value
15: 1        ; 0000 0001 - Decrement value

; Machine code (binary):
; Address | Binary      | Hex | Decimal
; --------|-------------|-----|--------
; 0       | 0001 1110   | 1E  | 30
; 1       | 1110 0000   | E0  | 224
; 2       | 1000 0111   | 87  | 135
; 3       | 0011 1111   | 3F  | 63
; 4       | 0100 1110   | 4E  | 78
; 5       | 0110 0000   | 60  | 96
; 7       | 1111 0000   | F0  | 240
; 14      | 0000 1010   | 0A  | 10
; 15      | 0000 0001   | 01  | 1
