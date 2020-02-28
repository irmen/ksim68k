import ksim68k


def test_basics():
    ksim68k.init(ksim68k.Cpu.M68030)
    assert ksim68k.cycles_remaining() == 0
    assert ksim68k.cycles_run() == 0
