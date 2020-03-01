/* Custom configuration file for Musashi */
/* See Musashi/m68kconf.h for explanation */


#ifndef M68KCONF__HEADER
#define M68KCONF__HEADER


#define OPT_OFF             0
#define OPT_ON              1
#define OPT_SPECIFY_HANDLER 2


#define M68K_COMPILE_FOR_MAME      OPT_OFF


#define M68K_EMULATE_010            OPT_ON
#define M68K_EMULATE_EC020          OPT_ON
#define M68K_EMULATE_020            OPT_ON
#define M68K_EMULATE_030            OPT_ON
#define M68K_EMULATE_040            OPT_ON


#define M68K_SEPARATE_READS         OPT_OFF
#define M68K_SIMULATE_PD_WRITES     OPT_OFF
#define M68K_EMULATE_INT_ACK        OPT_OFF
#define M68K_INT_ACK_CALLBACK(A)    cpu_int_ack_handler_function(A)
#define M68K_EMULATE_BKPT_ACK       OPT_OFF
#define M68K_BKPT_ACK_CALLBACK()    cpu_bkpt_ack_handler_function()
#define M68K_EMULATE_TRACE          OPT_OFF
#define M68K_EMULATE_RESET          OPT_SPECIFY_HANDLER
#define M68K_RESET_CALLBACK()       cpu_reset_handler()
#define M68K_CMPILD_HAS_CALLBACK     OPT_OFF
#define M68K_CMPILD_CALLBACK(v,r)    cpu_cmpild_handler_function(v,r)
#define M68K_RTE_HAS_CALLBACK       OPT_OFF
#define M68K_RTE_CALLBACK()         cpu_rte_handler_function()
#define M68K_TAS_HAS_CALLBACK       OPT_OFF
#define M68K_TAS_CALLBACK()         cpu_tas_handler_function()
#define M68K_ILLG_HAS_CALLBACK	    OPT_SPECIFY_HANDLER
#define M68K_ILLG_CALLBACK(opcode)  cpu_illegalinstr_handler(opcode)
#define M68K_EMULATE_FC             OPT_OFF
#define M68K_SET_FC_CALLBACK(A)     cpu_set_fc_handler_function(A)
#define M68K_MONITOR_PC             OPT_OFF
#define M68K_SET_PC_CALLBACK(A)     cpu_pc_changed_handler_function(A)
#define M68K_INSTRUCTION_HOOK       OPT_OFF
#define M68K_INSTRUCTION_CALLBACK(pc) cpu_instruction_hook_function(pc)
#define M68K_EMULATE_PREFETCH       OPT_OFF
#define M68K_EMULATE_ADDRESS_ERROR  OPT_OFF
#define M68K_LOG_ENABLE             OPT_OFF
#define M68K_LOG_1010_1111          OPT_OFF
#define M68K_LOG_FILEHANDLE         some_file_handle
#define M68K_EMULATE_PMMU           OPT_OFF
#define M68K_USE_64_BIT             OPT_ON


#endif /* M68KCONF__HEADER */
