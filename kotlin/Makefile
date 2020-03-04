.PHONY:	all
.PHONY:	copylib


CSRCDIR=src/main/c
MUSASHISRC=$(CSRCDIR)/Musashi

all:  libmusashi.so  copylib

libmusashi.so:  $(MUSASHISRC)/m68kconf.h $(MUSASHISRC)/m68kcpu.o $(MUSASHISRC)/m68kdasm.o $(MUSASHISRC)/m68kops.o $(MUSASHISRC)/softfloat/softfloat.o $(CSRCDIR)/memreadwrite.o
	gcc -shared -o libmusashi.so $^


copylib:
	cp libmusashi.so src/main/resources/linux-x86-64/


$(MUSASHISRC)/m68kcpu.o: $(MUSASHISRC)/m68kconf.h $(MUSASHISRC)/m68kcpu.c
	make -C src/main/c/Musashi

$(MUSASHISRC)/m68kdasm.o:
	make -C src/main/c/Musashi

$(MUSASHISRC)/m68kops.o:
	make -C src/main/c/Musashi

$(MUSASHISRC)/softfloat/softfloat.o:
	make -C src/main/c/Musashi

$(CSRCDIR)/memreadwrite.o:  $(CSRCDIR)/memreadwrite.c
	gcc -fPIC -c -o $@ $<
