# Kotlin m68k cpu simulator

Uses the [Musashi](https://github.com/kstenerud/Musashi) C library to do the actual emulation.

Simulates Motorola 68000 / 68010 / 68020 / 68030 / 68040 CPU.


First build the C emulation library with `make`.
It will copy the resulting library to the `src/main/resources` folder so that the Kotlin library can find and use it.