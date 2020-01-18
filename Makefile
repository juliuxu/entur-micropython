.PHONY: install compile all clean

BUILD_DIR = ./build
TOP_DIR = $(shell pwd)
export PATH := $(TOP_DIR)/$(BUILD_DIR)/xtensa-lx106-elf/bin:$(PATH)
export FROZEN_MANIFEST = $(TOP_DIR)/manifest.py
export CODE_SRC_DIR = $(TOP_DIR)/src

MAKEOPTS = "-j4"

all: clean make_build_dir install compile

make_build_dir:
	mkdir $(BUILD_DIR)

install:
	git clone --depth=1 https://github.com/micropython/micropython.git $(BUILD_DIR)/micropython
	git clone --depth=1 https://github.com/micropython/micropython-lib.git $(BUILD_DIR)/micropython-lib
	curl -L https://github.com/jepler/esp-open-sdk/releases/download/2018-06-10/xtensa-lx106-elf-standalone.tar.gz | tar xz -C $(BUILD_DIR)

compile:
	$(MAKE) $(MAKEOPTS) -C $(BUILD_DIR)/micropython/mpy-cross
	$(MAKE) $(MAKEOPTS) -C $(BUILD_DIR)/micropython/ports/esp8266 submodules
	$(MAKE) $(MAKEOPTS) -C $(BUILD_DIR)/micropython/ports/esp8266

clean:
	$(RM) -rf $(BUILD_DIR) 2> /dev/null


