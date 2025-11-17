# RISC-V Simulator

A complete, web-based RISC-V (RV32I) instruction set simulator built with Python and Flask. This simulator provides an interactive interface to write, assemble, and execute RISC-V assembly code with real-time visualization of CPU state.

## Features

- **Complete RV32I Support**: Implements all base RISC-V 32-bit integer instructions
- **Web-Based Interface**: Modern, responsive UI built with Flask
- **Interactive Execution**: Step-by-step or continuous execution with state visualization
- **Built-in Assembler**: Write assembly code directly in the browser
- **Register Visualization**: Real-time display of all 32 registers
- **Execution Logging**: Track instruction execution and register changes
- **Example Programs**: Pre-loaded examples including Fibonacci, factorial, and array operations
- **Comprehensive Testing**: Full test suite covering all instruction types

## Supported Instructions

### Arithmetic Instructions
- `ADD`, `SUB`, `ADDI`
- `SLT`, `SLTI`, `SLTU`, `SLTIU` (Set Less Than)

### Logical Instructions
- `AND`, `ANDI`, `OR`, `ORI`, `XOR`, `XORI`

### Shift Instructions
- `SLL`, `SLLI` (Shift Left Logical)
- `SRL`, `SRLI` (Shift Right Logical)
- `SRA`, `SRAI` (Shift Right Arithmetic)

### Memory Instructions
- `LW`, `LH`, `LB` (Load Word/Halfword/Byte)
- `LHU`, `LBU` (Load Unsigned)
- `SW`, `SH`, `SB` (Store Word/Halfword/Byte)

### Branch Instructions
- `BEQ`, `BNE` (Branch Equal/Not Equal)
- `BLT`, `BGE` (Branch Less Than/Greater Equal)
- `BLTU`, `BGEU` (Unsigned comparisons)

### Jump Instructions
- `JAL` (Jump and Link)
- `JALR` (Jump and Link Register)

### Upper Immediate Instructions
- `LUI` (Load Upper Immediate)
- `AUIPC` (Add Upper Immediate to PC)

### System Instructions
- `ECALL` (System call / halt)
- `EBREAK` (Breakpoint / halt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/brwnpanda/riscVsimulator...git
cd riscVsimulator...
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Interface

Start the Flask server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

### Using the Simulator

1. **Write Code**: Enter RISC-V assembly code in the editor or load an example
2. **Load**: Click "Load Code" to assemble and load the program
3. **Execute**:
   - **Step**: Execute one instruction at a time
   - **Run**: Execute until halt or completion
4. **Reset**: Clear CPU state and start over

### Example Program

```assembly
# Calculate Fibonacci numbers
addi x10, x0, 0    # n-2 = 0
addi x11, x0, 1    # n-1 = 1
addi x12, x0, 10   # counter = 10

loop:
add x13, x10, x11  # n = n-2 + n-1
addi x10, x11, 0   # n-2 = n-1
addi x11, x13, 0   # n-1 = n
addi x12, x12, -1  # counter--
bne x12, x0, loop  # if counter != 0, loop

ecall              # halt
```

## Testing

Run the test suite to verify all instructions work correctly:

```bash
python test_simulator.py
```

The test suite includes:
- Basic arithmetic operations
- Logical operations
- Shift operations
- Load/store instructions
- Branch instructions
- Jump instructions
- Upper immediate instructions
- Comparison operations
- Complex programs (Fibonacci, factorial)
- Memory operations with sign extension

## Project Structure

```
riscVsimulator.../
├── app.py                   # Flask web application
├── simulator.py             # Main simulator class
├── cpu_core.py             # CPU core with registers and memory
├── instruction_decoder.py  # Instruction decoder and executor
├── assembler.py            # RISC-V assembler
├── test_simulator.py       # Test suite
├── templates/
│   └── index.html          # Web interface
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Architecture

### CPU Core
- 32 general-purpose registers (x0-x31)
- Program counter (PC)
- 1MB byte-addressable memory
- Register x0 hardwired to zero

### Instruction Decoder
- Decodes all RV32I instruction formats (R, I, S, B, U, J)
- Executes instructions with proper sign extension
- Handles immediate value encoding

### Assembler
- Supports register names (x0-x31) and ABI names (zero, ra, sp, etc.)
- Handles labels and branch targets
- Supports hex (0x), binary (0b), and decimal immediates
- Includes comments with `#`

## Register ABI Names

| Register | ABI Name | Description |
|----------|----------|-------------|
| x0 | zero | Hard-wired zero |
| x1 | ra | Return address |
| x2 | sp | Stack pointer |
| x3 | gp | Global pointer |
| x4 | tp | Thread pointer |
| x5-x7 | t0-t2 | Temporaries |
| x8 | s0/fp | Saved register / Frame pointer |
| x9 | s1 | Saved register |
| x10-x11 | a0-a1 | Function arguments / Return values |
| x12-x17 | a2-a7 | Function arguments |
| x18-x27 | s2-s11 | Saved registers |
| x28-x31 | t3-t6 | Temporaries |

## Technical Details

### Memory Layout
- Memory is byte-addressable
- Default size: 1MB
- Little-endian byte order
- Programs loaded starting at address 0x0

### Execution Model
- Sequential execution with PC increment
- Branch/jump instructions update PC
- ECALL/EBREAK halt execution
- Maximum instruction limit for safety (10,000 by default)

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional instruction sets (M, A, F, D extensions)
- Performance optimizations
- Enhanced debugging features
- More example programs

## License

This project is open source and available for educational purposes.

## Acknowledgments

Built as a comprehensive RISC-V educational tool with clean, well-documented code suitable for learning computer architecture and assembly programming.