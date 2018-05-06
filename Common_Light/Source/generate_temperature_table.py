#!/usr/bin/env python
#
# generate_temp_table.py
#
# This will generate temp_table.h, which contains a definition of the lookup
# table used to convert from ADC readings to temperature (in degrees Celsius).

from __future__ import print_function
from __future__ import division
import math

# Constants are defined here. If you modify the schematic, check if these
# are still correct.

# These values are for the NTCG163JH103 thermistor
# Thermistor nominal resistance, in ohm
NOMINAL_RESISTANCE = 10000.0
# Thermistor nominal temperature, in kelvin
NOMINAL_TEMPERATURE = 298.15
# "B" constant for NTC thermistor (at nominal temperature), in kelvin
B_CONSTANT = 3435.0

# Resistor on top of voltage divider (R1 on schematic), in ohm
TOP_RESISTANCE = 10000.0
# Voltage on top of voltage divider, in volt
TOP_VOLTAGE = 3.3
# Reference voltage for ADC, in volt
ADC_REFERENCE_VOLTAGE = 2.47
# Maximum value for a single ADC reading
ADC_MAX = 1023
# Number of samples the ADC will accumulate
ADC_ACCUMULATE = 16
# Number of entries in table - the table will start from 0 (0 degrees Celsius)
# with each entry going up in 1 degree Celsius increments. So for a table
# length of 150, the table will handle temperatures of 0 - 149 degrees Celsius.
TABLE_LENGTH = 150

f = open("temperature_table.h", "w")
f.write("/* temperature_table.h\n")
f.write(" *\n")
f.write(" * Temperature to ADC value lookup tables.\n")
f.write(" * This file was generated by generate_temperature_table.py.\n")
f.write(" */\n")
f.write("\n")
f.write("#include <stdint.h>\n")
f.write("\n")
f.write("#define TEMPERATURE_LOOKUP_LENGTH {}\n".format(int(TABLE_LENGTH)))
f.write("\n")
f.write("static const uint16_t temperature_lookup[{}] = ".format(int(TABLE_LENGTH)))
f.write("{\n")

r_infinity = NOMINAL_RESISTANCE * math.exp(-B_CONSTANT / NOMINAL_TEMPERATURE)
for temperature in range(0, TABLE_LENGTH):
    # Calculate resistance of thermistor
    r = r_infinity * math.exp(B_CONSTANT / (temperature + 273.15))
    # Calculate voltage on voltage divider
    v = TOP_VOLTAGE * r / (r + TOP_RESISTANCE)
    # Scale to ADC reading
    s = (v / ADC_REFERENCE_VOLTAGE) * ADC_MAX
    # Clamp to ADC range
    if s < 0: s = 0
    if s > ADC_MAX: s = float(ADC_MAC)
    # Scale to accumulated reading
    s *= ADC_ACCUMULATE
    f.write("{}".format(int(round(s))))
    if temperature != (TABLE_LENGTH - 1):
        f.write(",")
    if (temperature % 10) == 9:
        f.write("\n")
    else:
        f.write(" ")

f.write("};\n")
f.write("\n")
f.close()