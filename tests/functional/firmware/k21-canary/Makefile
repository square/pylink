# Copyright 2016 Square, Inc.

# Commands
TARGET_PREFIX = arm-none-eabi-
AS            = $(TARGET_PREFIX)as
LD            = $(TARGET_PREFIX)ld
CC            = $(TARGET_PREFIX)gcc
CPP           = $(TARGET_PREFIX)g++
OBJCOPY       = $(TARGET_PREFIX)objcopy
CP            = cp
MKDIR         = mkdir

# Directories
BUILDDIR      = build
ASMDIR        = asm
SRCDIR        = src

# Flags
ASFLAGS       = -g -mthumb -mcpu=cortex-m4
LDFLAGS       = -T$(ASMDIR)/gcc.ld --specs=nosys.specs -mthumb -mcpu=cortex-m4
CCFLAGS       = -S -Wall -O0 -mcpu=cortex-m4 -mthumb -g -fstack-protector-all

# Output Files
BIN           = $(BUILDDIR)/firmware.bin
ELF           = $(BUILDDIR)/firmware.elf
ASOURCES      = $(notdir $(wildcard $(ASMDIR)/*.s))
CSOURCES      = $(notdir $(wildcard $(SRCDIR)/*.c))
OBJS          = $(addprefix $(BUILDDIR)/,$(ASOURCES:.s=.o)) $(addprefix $(BUILDDIR)/,$(CSOURCES:.c=.o))

.PHONY:	all clean

all:	$(BIN)

clean:
	-$(RM) -rf $(BUILDDIR)

$(ELF):	$(OBJS)
	@$(MKDIR) -p $(BUILDDIR)
	$(CC) $(LDFLAGS) -o $@ $^

$(BUILDDIR)/%.o: $(BUILDDIR)/%.s
	@$(MKDIR) -p $(BUILDDIR)
	$(AS) $(ASFLAGS) -o $@ $<

$(BUILDDIR)/%.s: $(ASMDIR)/%.s
	@$(MKDIR) -p $(BUILDDIR)
	$(CP) $< $(BUILDDIR)/

$(BUILDDIR)/%.s: $(SRCDIR)/%.c
	@$(MKDIR) -p $(BUILDDIR)
	$(CC) $(CCFLAGS) -o $@ $<

%.bin:	%.elf
	$(OBJCOPY) -O binary $< $@
