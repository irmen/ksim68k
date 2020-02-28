#!/bin/sh
cd Musashi && make m68kops.c && cd ..

cpp -nostdinc -E -P Musashi/m68k.h >m68k_stripped.h
