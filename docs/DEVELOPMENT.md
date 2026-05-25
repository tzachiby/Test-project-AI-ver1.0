# Development Setup Guide

## Prerequisites

### Software Requirements
- Git 2.x+
- Python 3.10+
- VS Code (recommended IDE)
- GitHub account with repository access

### Hardware Requirements
- ThunderCat6 test card
- Mini-USB cable (backdoor connection)
- 12V power supply
- Type-C cables for DUT connection

---

## Repository Setup

### Clone the Repository
```bash
git clone https://github.com/bytzachi/Test-project-AI-ver1.0.git
cd Test-project-AI-ver1.0
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## Project Structure

```
Test-project-AI-ver1.0/
├── README.md                 # Project overview
├── docs/                     # Documentation
│   ├── requirements/         # Requirements documents
│   ├── architecture/         # Architecture documents
│   └── design/               # Design documents
├── hw/                       # Hardware design
│   ├── schematics/           # Schematic files
│   ├── pcb/                  # PCB layout files
│   └── bom/                  # Bill of Materials
├── fw/                       # Firmware
│   ├── pd/                   # PD controller firmware
│   ├── ftdi/                 # FTDI backdoor firmware
│   └── fx20/                 # FX20 firmware
├── sw/                       # Software
│   ├── api/                  # Host API
│   │   └── tc6_api/          # Python API package
│   ├── tools/                # Tools and utilities
│   └── tests/                # Test scripts
└── manufacturing/            # Manufacturing files
```

---

## Development Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `release/*` - Release preparation

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(api): add mode switching function

Implement mode_switch() function to support dynamic mode changes
between DP, USB, and TBT modes.

Resolves: TC6-123
```

---

## Building & Testing

### Firmware Build
```bash
cd fw/ftdi
make all
```

### Run Tests
```bash
cd sw/tests
pytest -v
```

### API Documentation
```bash
cd sw/api
sphinx-build -b html docs/ docs/_build/
```

---

## Connecting to Hardware

### FTDI Backdoor Connection
1. Connect Mini-USB cable from TC6 to Host PC
2. Verify FTDI device appears in Device Manager
3. Note COM port number

### Initialize TC6 Connection
```python
from tc6_api import ThunderCat6

tc6 = ThunderCat6(port="COM3")  # Adjust port as needed
tc6.connect()
print(tc6.get_card_info())
```

---

## Troubleshooting

### FTDI Not Detected
- Check USB cable connection
- Verify FTDI drivers installed
- Check Device Manager for errors

### Mode Switch Fails
- Verify power supply is connected
- Check DIP switch settings
- Review error LEDs on card

---

## Support

- **Documentation**: See `docs/` folder
- **Issues**: GitHub Issues
- **Wiki**: GitHub Wiki
