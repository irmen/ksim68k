import sys
import ksim68k

CHROUT = 0x00fff002


class ObservableMemory(ksim68k.Memory):
    def write8(self, address: int, value: int):
        if address == CHROUT:
            print(chr(value), end="")


keep_running = True


def illegalinstr_handler(opcode: int) -> None:
    # illegal instruction encountered. Ending program. (expected)
    global keep_running
    keep_running = False


ksim68k.illegalinstr_handler = illegalinstr_handler


def run(program: str) -> None:
    with open(program, "rb") as f:
        data = f.read()

    memory = ObservableMemory(0x8000)
    memory.load(0, data)
    ksim68k.use_memory(memory)

    ksim68k.init(ksim68k.Cpu.M68000)
    ksim68k.pulse_reset()

    while keep_running:
        ksim68k.execute(16)
        sr = ksim68k.get_reg(ksim68k.Register.IR)
        if sr == 0x4e72:    # STOP opcode
            raise SystemExit("STOP instruction executed.")


if __name__ == "__main__":
    run("testprog.bin")
