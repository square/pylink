target remote :2331
monitor speed auto
monitor endian little
monitor flash device $DEVICE
monitor flash breakpoints = 1
monitor semihosting enable
monitor semihosting IOClient = 2
monitor reset 6
load build/firmware.elf
file build/firmware.elf
monitor reset 6
monitor reset 6

# Continue
c
