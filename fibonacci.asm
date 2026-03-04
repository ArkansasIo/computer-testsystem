; Fibonacci Sequence Generator
; Generates Fibonacci numbers: 1, 1, 2, 3, 5, 8, 13, 21...
; Displays each number and halts when overflow occurs
;
; Memory layout:
; 0-12: Program
; 13: Current Fibonacci number (starts at 1)
; 14: Previous Fibonacci number (starts at 0)
; 15: Temporary storage

0:  LDA 13   ; 0001 1101 - Load current number into A
1:  OUT      ; 1110 0000 - Display current Fibonacci number
2:  ADD 14   ; 0010 1110 - Add previous number to current
3:  JC 12    ; 0111 1100 - If overflow (carry), jump to halt
4:  STA 15   ; 0100 1111 - Store new number in temp
5:  LDA 13   ; 0001 1101 - Load current into A
6:  STA 14   ; 0100 1110 - Store as previous
7:  LDA 15   ; 0001 1111 - Load new number from temp
8:  STA 13   ; 0100 1101 - Store as current
9:  JMP 0    ; 0110 0000 - Loop back to start
12: HLT      ; 1111 0000 - Halt when overflow

; Data section
13: 1        ; 0000 0001 - Current Fibonacci number (start with 1)
14: 0        ; 0000 0000 - Previous Fibonacci number (start with 0)
15: 0        ; 0000 0000 - Temporary storage

; Machine code (binary):
; Address | Binary      | Hex | Decimal
; --------|-------------|-----|--------
; 0       | 0001 1101   | 1D  | 29
; 1       | 1110 0000   | E0  | 224
; 2       | 0010 1110   | 2E  | 46
; 3       | 0111 1100   | 7C  | 124
; 4       | 0100 1111   | 4F  | 79
; 5       | 0001 1101   | 1D  | 29
; 6       | 0100 1110   | 4E  | 78
; 7       | 0001 1111   | 1F  | 31
; 8       | 0100 1101   | 4D  | 77
; 9       | 0110 0000   | 60  | 96
; 12      | 1111 0000   | F0  | 240
; 13      | 0000 0001   | 01  | 1
; 14      | 0000 0000   | 00  | 0
; 15      | 0000 0000   | 00  | 0
