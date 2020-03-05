
//    fun m68k_set_instr_hook_callback(void (*callback)(unsigned int pc))


int (*read_memory_8_callback)(unsigned int address) = 0;
int (*read_memory_16_callback)(unsigned int address) = 0;
int (*read_memory_32_callback)(unsigned int address) = 0;
void (*write_memory_8_callback)(unsigned int address, unsigned int value) = 0;
void (*write_memory_16_callback)(unsigned int address, unsigned int value) = 0;
void (*write_memory_32_callback)(unsigned int address, unsigned int value) = 0;


void set_read_memory_8_callback( int (*callback)(unsigned int address) ) {
    read_memory_8_callback = callback;
}

void set_read_memory_16_callback( int (*callback)(unsigned int address) ) {
    read_memory_16_callback = callback;
}

void set_read_memory_32_callback( int (*callback)(unsigned int address) ) {
    read_memory_32_callback = callback;
}

void set_write_memory_8_callback( void (*callback)(unsigned int address, unsigned int value) ) {
    write_memory_8_callback = callback;
}

void set_write_memory_16_callback( void (*callback)(unsigned int address, unsigned int value) ) {
    write_memory_16_callback = callback;
}

void set_write_memory_32_callback( void (*callback)(unsigned int address, unsigned int value) ) {
    write_memory_32_callback = callback;
}


unsigned int m68k_read_memory_8(unsigned int address) {
    return read_memory_8_callback(address);
}

unsigned int m68k_read_memory_16(unsigned int address) {
    return read_memory_16_callback(address);
}

unsigned int m68k_read_memory_32(unsigned int address) {
    return read_memory_32_callback(address);
}


void m68k_write_memory_8(unsigned int address, unsigned int value) {
    write_memory_8_callback(address, value);
}

void m68k_write_memory_16(unsigned int address, unsigned int value) {
    write_memory_16_callback(address, value);
}

void m68k_write_memory_32(unsigned int address, unsigned int value) {
    write_memory_32_callback(address, value);
}


unsigned int m68k_read_immediate_16(unsigned int address) {
    return read_memory_16_callback(address);
}

unsigned int m68k_read_immediate_32(unsigned int address) {
    return read_memory_32_callback(address);
}

unsigned int m68k_read_pcrelative_8(unsigned int address) {
    return read_memory_8_callback(address);
}

unsigned int m68k_read_pcrelative_16(unsigned int address) {
    return read_memory_16_callback(address);
}

unsigned int m68k_read_pcrelative_32(unsigned int address) {
    return read_memory_32_callback(address);
}

unsigned int m68k_read_disassembler_8 (unsigned int address) {
    return read_memory_8_callback(address);
}

unsigned int m68k_read_disassembler_16 (unsigned int address) {
    return read_memory_16_callback(address);
}

unsigned int m68k_read_disassembler_32 (unsigned int address) {
    return read_memory_32_callback(address);
}

void m68k_write_memory_32_pd(unsigned int address, unsigned int value) {
    write_memory_32_callback(address, value);
}
