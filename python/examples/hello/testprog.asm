
; simple test program
; assemble with vasm: http://sun.hasenbraten.de/vasm/
; $ vasmm68k_mot -Fbin  testprog.asm -o testprog.bin


STACK_AREA = $00008000

	org 	$0		; vector jump table

	dc.l	STACK_AREA		;  0: SP
	dc.l	program_start		;  1: PC
	dc.l	$000ff000	;  2: bus error
	dc.l	$000ff000	;  3: address error
	dc.l	$000ff000	;  4: illegal instruction
	dc.l	$000ff000	;  5: zero divide
	dc.l	$000ff000	;  6: chk
	dc.l	$000ff000	;  7: trapv
	dc.l	$000ff000	;  8: privilege violation
	dc.l	$000ff000	;  9: trace
	dc.l	$000ff000	; 10: 1010
	dc.l	$000ff000	; 11: 1111
	dc.l	$000ff000	; 12: -
	dc.l	$000ff000	; 13: coprocessor protocol violation
	dc.l	$000ff000	; 14: format error
	dc.l	$000ff000	; 15: uninitialized interrupt
	dc.l	$000ff000	; 16: -
	dc.l	$000ff000	; 17: -
	dc.l	$000ff000	; 18: -
	dc.l	$000ff000	; 19: -
	dc.l	$000ff000	; 20: -
	dc.l	$000ff000	; 21: -
	dc.l	$000ff000	; 22: -
	dc.l	$000ff000	; 23: -
	dc.l	$000ff000	; 24: spurious interrupt
	dc.l	$000ff000	; 25: l1 irq
	dc.l	$000ff000	; 26: l2 irq
	dc.l	$000ff000	; 27: l3 irq
	dc.l	$000ff000	; 28: l4 irq
	dc.l	$000ff000	; 29: l5 irq
	dc.l	$000ff000	; 30: l6 irq
	dc.l	$000ff000	; 31: l7 irq
	dc.l	$000ff000	; 32: trap 0
	dc.l	$000ff000	; 33: trap 1
	dc.l	$000ff000	; 34: trap 2
	dc.l	$000ff000	; 35: trap 3
	dc.l	$000ff000	; 36: trap 4
	dc.l	$000ff000	; 37: trap 5
	dc.l	$000ff000	; 38: trap 6
	dc.l	$000ff000	; 39: trap 7
	dc.l	$000ff000	; 40: trap 8
	dc.l	$000ff000	; 41: trap 9
	dc.l	$000ff000	; 42: trap 10
	dc.l	$000ff000	; 43: trap 11
	dc.l	$000ff000	; 44: trap 12
	dc.l	$000ff000	; 45: trap 13
	dc.l	$000ff000	; 46: trap 14
	dc.l	$000ff222	; 47: trap 15   [ends program]
        dc.l    $000ff000     ; 48: (FP) Branch or Set on Unordered Condition */
        dc.l    $000ff000     ; 49: (FP) Inexact Result */
        dc.l    $000ff000     ; 50: (FP) Divide by Zero */
        dc.l    $000ff000     ; 51: (FP) Underflow */
        dc.l    $000ff000     ; 52: (FP) Operand Error */
        dc.l    $000ff000     ; 53: (FP) Overflow */
        dc.l    $000ff000     ; 54: (FP) Signaling NAN */
        dc.l    $000ff000     ; 55: (FP) Unimplemented Data Type */
        dc.l    $000ff000     ; 56: MMU Configuration Error */
        dc.l    $000ff000     ; 57: MMU Illegal Operation Error */
        dc.l    $000ff000     ; 58: MMU Access Violation Error */
        dc.l    $000ff000     ; 59: Reserved (NOT USED) */
        dc.l    $000ff000     ; 60: Reserved (NOT USED) */
        dc.l    $000ff000     ; 61: Reserved (NOT USED) */
        dc.l    $000ff000     ; 62: Reserved (NOT USED) */
        dc.l    $000ff000     ; 63: Reserved (NOT USED) */

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
	trap		#15		; end program trap


string:
	dc.b	"Hello, world! From the 68000 assembly program.",10,0


