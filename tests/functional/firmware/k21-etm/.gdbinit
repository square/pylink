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

# monitor SWO EnableTarget <CPUFreqHz> <SWOFreqHz> <PortMask> <Mode>
# If 0 is given for the CPU and SWO frequency, it is determined automatically.
monitor SWO EnableTarget 20958600 0 0xFFFFFFFF 0

# Continue
c
