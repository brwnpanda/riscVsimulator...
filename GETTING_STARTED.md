# Getting Started with RISC-V Simulator

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests** (Optional but recommended)
   ```bash
   python test_simulator.py
   ```
   You should see all 10 tests pass.

3. **Start the Web Server**
   ```bash
   python app.py
   ```

4. **Open Your Browser**
   Navigate to: `http://localhost:5000`

## Using the Simulator

### Loading and Running Code

1. **Write or Load Code**: 
   - Type RISC-V assembly code in the editor, or
   - Click one of the example buttons (fibonacci, factorial, array_sum, simple_add)

2. **Load the Code**:
   - Click "Load Code" to assemble and load the program

3. **Execute**:
   - Click "Step" to execute one instruction at a time
   - Click "Run" to execute until the program halts
   - Click "Reset" to clear CPU state and start over

### Understanding the Interface

**Assembly Code Editor**: Write RISC-V assembly code here
- Supports all RV32I instructions
- Use `#` for comments
- Labels can be used for branches and jumps

**Registers Panel**: Shows all 32 registers
- Changed registers are highlighted in yellow
- Values shown in both hex and decimal

**Execution Log**: Shows last 10 instructions executed
- PC (Program Counter) address
- Instruction hex encoding
- Register changes

**CPU Info**: Shows current CPU state
- Program Counter
- Instructions Executed count
- Status (Running/Halted)

## RISC-V Assembly Syntax

### Register Names

You can use either numeric names (x0-x31) or ABI names:
- `x0` or `zero` - always zero
- `x1` or `ra` - return address
- `x2` or `sp` - stack pointer
- `x10-x11` or `a0-a1` - function arguments/return values
- See README for complete list

### Instruction Examples

```assembly
# Arithmetic
addi x1, x0, 10      # x1 = 0 + 10
add x3, x1, x2       # x3 = x1 + x2
sub x4, x2, x1       # x4 = x2 - x1

# Logical
and x5, x1, x2       # x5 = x1 & x2
or x6, x1, x2        # x6 = x1 | x2
xor x7, x1, x2       # x7 = x1 ^ x2

# Shifts
slli x8, x1, 2       # x8 = x1 << 2
srli x9, x2, 1       # x9 = x2 >> 1

# Memory
sw x1, 0(x2)         # store word: mem[x2+0] = x1
lw x3, 4(x2)         # load word: x3 = mem[x2+4]

# Branches
beq x1, x2, label    # if x1 == x2, goto label
bne x1, x2, label    # if x1 != x2, goto label
blt x1, x2, label    # if x1 < x2, goto label

# Jumps
jal x1, label        # x1 = PC+4, PC = label
jalr x1, x2, 0       # x1 = PC+4, PC = x2+0

# Labels
loop:
    addi x1, x1, 1
    bne x1, x10, loop

# Halt
ecall                # stop execution
```

### Immediate Values

Supports multiple formats:
- Decimal: `10`, `-5`
- Hexadecimal: `0xFF`, `0x1234`
- Binary: `0b1010`, `0b11110000`

## Example Programs

### 1. Simple Addition
```assembly
addi x1, x0, 10    # x1 = 10
addi x2, x0, 20    # x2 = 20
add x3, x1, x2     # x3 = 30
ecall
```

### 2. Fibonacci Sequence
```assembly
addi x10, x0, 0    # n-2 = 0
addi x11, x0, 1    # n-1 = 1
addi x12, x0, 10   # counter = 10

loop:
add x13, x10, x11  # n = n-2 + n-1
addi x10, x11, 0   # n-2 = n-1
addi x11, x13, 0   # n-1 = n
addi x12, x12, -1  # counter--
bne x12, x0, loop  # if counter != 0, loop

ecall              # result in x11
```

### 3. Array Sum
```assembly
addi x10, x0, 0    # sum = 0
addi x11, x0, 100  # array base
addi x12, x0, 5    # size

# Initialize array
addi x13, x0, 10
sw x13, 0(x11)
addi x13, x0, 20
sw x13, 4(x11)
# ... more values

# Sum loop
addi x14, x0, 0    # index = 0
loop:
beq x14, x12, done
slli x15, x14, 2   # offset = index * 4
add x15, x11, x15  # address = base + offset
lw x16, 0(x15)     # load value
add x10, x10, x16  # sum += value
addi x14, x14, 1   # index++
jal x0, loop

done:
ecall              # sum in x10
```

## Tips and Tricks

1. **Use Step Mode for Debugging**: Step through code one instruction at a time to understand execution flow

2. **Watch Register Changes**: Changed registers are highlighted to help track data flow

3. **Check the Execution Log**: Review recent instructions to debug issues

4. **Start Simple**: Begin with simple programs and gradually add complexity

5. **Use Examples**: Load examples to see working code patterns

6. **Comments Are Your Friend**: Use `#` to document your code

## Troubleshooting

**Assembly Error**: Check instruction syntax and register names
- Make sure all registers are valid (x0-x31)
- Check that immediate values are in valid ranges
- Verify branch/jump labels are defined

**Execution Error**: Check for invalid memory access
- Memory addresses must be within bounds (0 to 1MB)
- Memory access must be aligned for word/halfword operations

**Infinite Loop**: Use the Reset button
- The simulator has a safety limit (10,000 instructions)
- Check loop conditions and counter updates

## Development Mode

For development with automatic reloading:
```bash
FLASK_DEBUG=true python app.py
```

**Warning**: Never use debug mode in production!

## Next Steps

- Try modifying the example programs
- Write your own RISC-V programs
- Explore different instruction types
- Learn about computer architecture concepts

## Resources

- [RISC-V Specification](https://riscv.org/technical/specifications/)
- [RISC-V Assembly Programmer's Manual](https://github.com/riscv-non-isa/riscv-asm-manual/blob/master/riscv-asm.md)
- Project README.md for detailed documentation

Happy Coding! 🚀
