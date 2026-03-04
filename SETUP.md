# Setup Guide

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Git (for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/multi-arch-computer.git
   cd multi-arch-computer
   ```

2. **No additional dependencies required!**
   - tkinter is included with Python
   - PyAudio is optional (for sound effects)

3. **Test the installation**
   ```bash
   python test_all.py
   ```

### Optional: Install PyAudio for Sound Effects

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## Running the Project

### GUIs

**Enhanced GUI with Sound:**
```bash
python computer_gui_enhanced.py
```

**Multi-Architecture GUI:**
```bash
python multi_arch_gui.py
```

**Original 8-bit GUI:**
```bash
python computer_gui.py
```

### Assembly Programming

**Assemble a program:**
```bash
python assembler.py fibonacci.asm
```

**Simulate execution:**
```bash
python simulator.py fibonacci.bin
```

**With verbose output:**
```bash
python simulator.py fibonacci.bin --verbose
```

### Generate Sound Effects

```bash
python sound_effects.py
```

### Run Tests

```bash
python test_all.py
```

### Mathematical Libraries

```bash
python boolean_algebra.py
python calculus.py
python math_library.py
python computer_architecture.py
```

## Project Structure

```
.
├── README.md                    # Project overview
├── SETUP.md                     # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
│
├── Assembly Programs/
│   ├── *.asm                    # 15 assembly programs
│   └── *.bin                    # Compiled binaries
│
├── Computer Systems/
│   ├── computer_architectures.py
│   ├── extended_instruction_set.py
│   ├── assembler.py
│   └── simulator.py
│
├── GUIs/
│   ├── computer_gui.py
│   ├── computer_gui_enhanced.py
│   └── multi_arch_gui.py
│
├── Sound Effects/
│   ├── sound_effects.py
│   └── *.wav                    # 11 sound files
│
├── Mathematical Libraries/
│   ├── boolean_algebra.py
│   ├── calculus.py
│   ├── math_library.py
│   └── computer_architecture.py
│
├── Documentation/
│   ├── *.md                     # 10+ guide files
│   └── test_all.py
│
└── Tests/
    └── test_all.py
```

## Troubleshooting

### Python Not Found
- Ensure Python 3.7+ is installed
- Check PATH environment variable
- Try `python3` instead of `python`

### tkinter Not Available
- **Windows:** Reinstall Python with tkinter option checked
- **macOS:** `brew install python-tk`
- **Linux:** `sudo apt-get install python3-tk`

### PyAudio Installation Issues
- See optional installation steps above
- The project works without PyAudio (no sound)

### Permission Errors
- **Windows:** Run as administrator
- **Linux/Mac:** Use `sudo` if needed

### Import Errors
- Ensure you're in the project directory
- Check Python version: `python --version`

## Development Setup

### For Contributors

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/multi-arch-computer.git
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature
   ```

4. **Make changes and test**
   ```bash
   python test_all.py
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature"
   git push origin feature/your-feature
   ```

6. **Create Pull Request**

## System Requirements

### Minimum
- Python 3.7+
- 100 MB disk space
- 512 MB RAM

### Recommended
- Python 3.10+
- 200 MB disk space
- 1 GB RAM
- Audio output device (for sound effects)

## Platform Support

- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, Debian, Fedora)

## Getting Help

- Read the documentation in `/docs`
- Check existing GitHub issues
- Create a new issue for bugs
- See CONTRIBUTING.md for guidelines

## Next Steps

After setup, check out:
- `COMPLETE_GUIDE.md` - Comprehensive project guide
- `ENHANCED_FEATURES_GUIDE.md` - Sound and display features
- `MULTI_ARCH_GUIDE.md` - Multi-architecture systems
- `GUI_GUIDE.md` - GUI usage instructions

Enjoy exploring computer architecture!
