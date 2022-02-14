.PHONY:	copylib all clean


CSRCDIR=src/main/c
MUSASHISRC=$(CSRCDIR)/Musashi
CFLAGS=-O3 -fPIC -Wall

all:  libmusashi.so  copylib

clean:
	make -C src/main/c/Musashi clean

libmusashi.so:  m68kconf_custom.h $(MUSASHISRC)/m68kcpu.o $(MUSASHISRC)/m68kdasm.o $(MUSASHISRC)/m68kops.o $(MUSASHISRC)/softfloat/softfloat.o $(CSRCDIR)/memreadwrite.o
	gcc -shared -fPIC -o libmusashi.so $^


copylib: libmusashi.so
	python copynativelib.py


$(MUSASHISRC)/m68kcpu.o: $(MUSASHISRC)/m68kconf.h $(MUSASHISRC)/m68kcpu.c
	cp m68kconf_custom.h $(MUSASHISRC)/m68kconf.h
	make -C src/main/c/Musashi CFLAGS="$(CFLAGS)"

$(MUSASHISRC)/m68kdasm.o:
	make -C src/main/c/Musashi CFLAGS="$(CFLAGS)"

$(MUSASHISRC)/m68kops.o:
	make -C src/main/c/Musashi CFLAGS="$(CFLAGS)"

$(MUSASHISRC)/softfloat/softfloat.o:
	make -C src/main/c/Musashi CFLAGS="$(CFLAGS)"

$(CSRCDIR)/memreadwrite.o:  $(CSRCDIR)/memreadwrite.c
	gcc -fPIC -c -o $@ $<
