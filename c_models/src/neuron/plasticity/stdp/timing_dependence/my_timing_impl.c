#include "my_timing_impl.h"

int16_t sin_lookup[SIN_SIZE];
int32_t peak_time;

//---------------------------------------
// Functions
//---------------------------------------
address_t timing_initialise(address_t address) {

    log_info("timing_initialise: starting");
    log_info("\tSTDP my timing rule");

    // TODO: copy parameters from memory
    peak_time = address[0];
    log_info("\t\tPeak time:%d timesteps", peak_time);

    // Copy LUTs from following memory
    address_t lut_address = maths_copy_int16_lut(&address[1], SIN_SIZE, &sin_lookup[0]);

    log_info("timing_initialise: completed successfully");

    // TODO: Return the address after the last one read
    return lut_address;
//    return &(address[2]);
}
