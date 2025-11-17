"""
RISC-V CPU Simulator Core
Implements RV32I base instruction set
"""

class RISCVCPUCore:
    """RISC-V CPU Core with 32 registers and memory"""
    
    def __init__(self, memory_size=1024*1024):  # 1MB default memory
        # 32 general-purpose registers (x0-x31)
        self.registers = [0] * 32
        self.registers[0] = 0  # x0 is always 0
        
        # Program counter
        self.pc = 0
        
        # Memory (byte-addressable)
        self.memory = bytearray(memory_size)
        self.memory_size = memory_size
        
        # Execution state
        self.running = False
        self.instruction_count = 0
        self.max_instructions = 10000  # Safety limit
        
    def reset(self):
        """Reset CPU state"""
        self.registers = [0] * 32
        self.pc = 0
        self.running = False
        self.instruction_count = 0
        
    def read_register(self, reg_num):
        """Read from a register"""
        if reg_num < 0 or reg_num >= 32:
            raise ValueError(f"Invalid register number: {reg_num}")
        return self.registers[reg_num] & 0xFFFFFFFF
    
    def write_register(self, reg_num, value):
        """Write to a register (x0 is always 0)"""
        if reg_num < 0 or reg_num >= 32:
            raise ValueError(f"Invalid register number: {reg_num}")
        if reg_num != 0:  # x0 is hardwired to 0
            self.registers[reg_num] = value & 0xFFFFFFFF
    
    def read_memory(self, address, size=4):
        """Read from memory (size: 1, 2, or 4 bytes)"""
        if address < 0 or address + size > self.memory_size:
            raise ValueError(f"Memory access out of bounds: {address}")
        
        if size == 1:
            return self.memory[address]
        elif size == 2:
            return int.from_bytes(self.memory[address:address+2], byteorder='little')
        elif size == 4:
            return int.from_bytes(self.memory[address:address+4], byteorder='little')
        else:
            raise ValueError(f"Invalid memory read size: {size}")
    
    def write_memory(self, address, value, size=4):
        """Write to memory (size: 1, 2, or 4 bytes)"""
        if address < 0 or address + size > self.memory_size:
            raise ValueError(f"Memory access out of bounds: {address}")
        
        if size == 1:
            self.memory[address] = value & 0xFF
        elif size == 2:
            self.memory[address:address+2] = (value & 0xFFFF).to_bytes(2, byteorder='little')
        elif size == 4:
            self.memory[address:address+4] = (value & 0xFFFFFFFF).to_bytes(4, byteorder='little')
        else:
            raise ValueError(f"Invalid memory write size: {size}")
    
    def load_program(self, instructions, start_address=0):
        """Load a program into memory"""
        for i, instruction in enumerate(instructions):
            addr = start_address + (i * 4)
            self.write_memory(addr, instruction, 4)
        self.pc = start_address
        
    def sign_extend(self, value, bits):
        """Sign extend a value from 'bits' bits to 32 bits"""
        sign_bit = 1 << (bits - 1)
        if value & sign_bit:
            return value | (~((1 << bits) - 1) & 0xFFFFFFFF)
        return value
    
    def get_state(self):
        """Get current CPU state"""
        return {
            'pc': self.pc,
            'registers': [self.read_register(i) for i in range(32)],
            'instruction_count': self.instruction_count,
            'running': self.running
        }
