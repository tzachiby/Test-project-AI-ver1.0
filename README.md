# ThunderCat6 (TC6) Test Card Project

## Project Overview
ThunderCat6 is the next generation test card for Thunderbolt/USB4 validation, designed to address TC5 limitations and support new platform requirements.

## Key Improvements over TC5
- **FX20** replaces FX3 for enhanced USB synthetic traffic generation with LPM support
- **KR (Kite Ridge)** integration for USB4 support alongside BR (Barlow Ridge)
- **Direct UFP-DFP bypass** via high-speed mux for commercial device testing
- **Native USB speed downgrade** support (Gen1x1, 1x2, 2x1, 2x2)
- **DP SST mode** support in addition to MST
- **Faster mode switching** (<0.5 seconds target)
- **Variable LTTPR configuration** support

## Project Structure
```
TC6/
├── docs/                    # Documentation
│   ├── requirements/        # Requirements documents
│   ├── architecture/        # Architecture documents
│   └── design/              # Design documents
├── hw/                      # Hardware design
│   ├── schematics/          # Schematic files
│   ├── pcb/                 # PCB layout files
│   └── bom/                 # Bill of Materials
├── fw/                      # Firmware
│   ├── pd/                  # PD controller firmware
│   ├── ftdi/                # FTDI backdoor firmware
│   └── fx20/                # FX20 firmware
├── sw/                      # Software
│   ├── api/                 # Host API
│   ├── tools/               # Tools and utilities
│   └── tests/               # Test scripts
└── manufacturing/           # Manufacturing files
```

## Team Roles
- **Project Manager (PM)**: Overall project coordination and schedule
- **Architecture Lead**: System architecture and component selection
- **HW Design Lead**: PCB and schematic design
- **SW Lead**: Firmware and host software development

## Quick Links
- [Requirements Analysis](docs/requirements/TC6_Requirements_Analysis.md)
- [Architecture Overview](docs/architecture/TC6_Architecture.md)
- [Project Schedule](docs/TC6_Schedule.md)

## Getting Started
See [Development Setup](docs/DEVELOPMENT.md) for environment setup instructions.

## License
Intel Confidential - Internal Use Only
