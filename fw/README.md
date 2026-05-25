# Firmware

This directory contains ThunderCat6 firmware source code.

## Structure

- `pd/` - PD Controller (PMG1-S3) firmware
- `ftdi/` - FTDI backdoor controller firmware
- `fx20/` - FX20 USB traffic generator firmware

## Build Requirements

- ARM GCC toolchain
- CMake 3.20+
- Python 3.10+ (for build scripts)

## Build Instructions

```bash
cd <component>
mkdir build && cd build
cmake ..
make
```

## Programming

See individual component directories for programming instructions.
