
; simple test program
; assemble with vasm: http://sun.hasenbraten.de/vasm/
; $ vasmm68k_mot -Fbin  testprog.asm -o testprog.bin


STACK_AREA = $00008000

	org 	$0		; vector jump table

	dc.l	STACK_AREA		;  0: SP
	dc.l	program_start		;  1: PC
	dc.l	unhandled_exception	;  2: bus error
	dc.l	unhandled_exception	;  3: address error
	dc.l	unhandled_exception	;  4: illegal instruction
	dc.l	unhandled_exception	;  5: zero divide
	dc.l	unhandled_exception	;  6: chk
	dc.l	unhandled_exception	;  7: trapv
	dc.l	unhandled_exception	;  8: privilege violation
	dc.l	unhandled_exception	;  9: trace
	dc.l	unhandled_exception	; 10: 1010
	dc.l	unhandled_exception	; 11: 1111
	dc.l	unhandled_exception	; 12: -
	dc.l	unhandled_exception	; 13: coprocessor protocol violation
	dc.l	unhandled_exception	; 14: format error
	dc.l	unhandled_exception	; 15: uninitialized interrupt
	dc.l	unhandled_exception	; 16: -
	dc.l	unhandled_exception	; 17: -
	dc.l	unhandled_exception	; 18: -
	dc.l	unhandled_exception	; 19: -
	dc.l	unhandled_exception	; 20: -
	dc.l	unhandled_exception	; 21: -
	dc.l	unhandled_exception	; 22: -
	dc.l	unhandled_exception	; 23: -
	dc.l	unhandled_exception	; 24: spurious interrupt
	dc.l	unhandled_exception	; 25: l1 irq
	dc.l	unhandled_exception	; 26: l2 irq
	dc.l	unhandled_exception	; 27: l3 irq
	dc.l	unhandled_exception	; 28: l4 irq
	dc.l	unhandled_exception	; 29: l5 irq
	dc.l	unhandled_exception	; 30: l6 irq
	dc.l	unhandled_exception	; 31: l7 irq
	dc.l	unhandled_exception	; 32: trap 0
	dc.l	unhandled_exception	; 33: trap 1
	dc.l	unhandled_exception	; 34: trap 2
	dc.l	unhandled_exception	; 35: trap 3
	dc.l	unhandled_exception	; 36: trap 4
	dc.l	unhandled_exception	; 37: trap 5
	dc.l	unhandled_exception	; 38: trap 6
	dc.l	unhandled_exception	; 39: trap 7
	dc.l	unhandled_exception	; 40: trap 8
	dc.l	unhandled_exception	; 41: trap 9
	dc.l	unhandled_exception	; 42: trap 10
	dc.l	unhandled_exception	; 43: trap 11
	dc.l	unhandled_exception	; 44: trap 12
	dc.l	unhandled_exception	; 45: trap 13
	dc.l	unhandled_exception	; 46: trap 14
	dc.l	$00			; 47: trap 15   [ends program]
        dc.l    unhandled_exception     ; 48: (FP) Branch or Set on Unordered Condition */
        dc.l    unhandled_exception     ; 49: (FP) Inexact Result */
        dc.l    unhandled_exception     ; 50: (FP) Divide by Zero */
        dc.l    unhandled_exception     ; 51: (FP) Underflow */
        dc.l    unhandled_exception     ; 52: (FP) Operand Error */
        dc.l    unhandled_exception     ; 53: (FP) Overflow */
        dc.l    unhandled_exception     ; 54: (FP) Signaling NAN */
        dc.l    unhandled_exception     ; 55: (FP) Unimplemented Data Type */
        dc.l    unhandled_exception     ; 56: MMU Configuration Error */
        dc.l    unhandled_exception     ; 57: MMU Illegal Operation Error */
        dc.l    unhandled_exception     ; 58: MMU Access Violation Error */
        dc.l    unhandled_exception     ; 59: Reserved (NOT USED) */
        dc.l    unhandled_exception     ; 60: Reserved (NOT USED) */
        dc.l    unhandled_exception     ; 61: Reserved (NOT USED) */
        dc.l    unhandled_exception     ; 62: Reserved (NOT USED) */
        dc.l    unhandled_exception     ; 63: Reserved (NOT USED) */

	; user interrupt vectors follow: $0100-$03ff
	blk.l	192, $0


CHROUT = $00fff002		; note: 68000 only has 24 bits address bus

program_start:
	lea.l		string,a0
.loop	move.b		(a0)+,d0
	beq.s		.stop
	move.b		d0,CHROUT
	bra.s		.loop
.stop	moveq.l		#99,d0
	illegal				; forcibly end program


unhandled_exception:
	stop	#$2700			; wait for NMI
	bra.s	unhandled_exception


string:
	dc.b	"Hello, world! From the 68000 assembly program.",10,0


