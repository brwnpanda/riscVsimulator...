"""
RISC-V Instruction Decoder and Executor
Supports RV32I base instruction set
"""

class InstructionDecoder:
    """Decode and execute RISC-V instructions"""
    
    def __init__(self, cpu):
        self.cpu = cpu
        
    def decode_and_execute(self, instruction):
        """Decode and execute a single instruction"""
        # Extract opcode (bits 0-6)
        opcode = instruction & 0x7F
        
        # R-type: funct7[31:25] rs2[24:20] rs1[19:15] funct3[14:12] rd[11:7] opcode[6:0]
        # I-type: imm[31:20] rs1[19:15] funct3[14:12] rd[11:7] opcode[6:0]
        # S-type: imm[31:25] rs2[24:20] rs1[19:15] funct3[14:12] imm[11:7] opcode[6:0]
        # B-type: imm[31] imm[30:25] rs2[24:20] rs1[19:15] funct3[14:12] imm[11:8] imm[7] opcode[6:0]
        # U-type: imm[31:12] rd[11:7] opcode[6:0]
        # J-type: imm[31] imm[30:21] imm[20] imm[19:12] rd[11:7] opcode[6:0]
        
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        
        if opcode == 0b0110011:  # R-type (register-register operations)
            self.execute_r_type(rd, funct3, rs1, rs2, funct7)
        elif opcode == 0b0010011:  # I-type (immediate operations)
            imm = self.cpu.sign_extend((instruction >> 20) & 0xFFF, 12)
            self.execute_i_type(rd, funct3, rs1, imm, funct7)
        elif opcode == 0b0000011:  # Load instructions
            imm = self.cpu.sign_extend((instruction >> 20) & 0xFFF, 12)
            self.execute_load(rd, funct3, rs1, imm)
        elif opcode == 0b0100011:  # Store instructions
            imm = self.cpu.sign_extend(((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F), 12)
            self.execute_store(funct3, rs1, rs2, imm)
        elif opcode == 0b1100011:  # Branch instructions
            imm = self.extract_b_immediate(instruction)
            self.execute_branch(funct3, rs1, rs2, imm)
        elif opcode == 0b1101111:  # JAL
            imm = self.extract_j_immediate(instruction)
            self.execute_jal(rd, imm)
        elif opcode == 0b1100111:  # JALR
            imm = self.cpu.sign_extend((instruction >> 20) & 0xFFF, 12)
            self.execute_jalr(rd, rs1, imm)
        elif opcode == 0b0110111:  # LUI
            imm = instruction & 0xFFFFF000
            self.execute_lui(rd, imm)
        elif opcode == 0b0010111:  # AUIPC
            imm = instruction & 0xFFFFF000
            self.execute_auipc(rd, imm)
        elif opcode == 0b1110011:  # ECALL/EBREAK
            self.execute_system(instruction)
        else:
            raise ValueError(f"Unknown opcode: {opcode:#x}")
        
        self.cpu.instruction_count += 1
    
    def extract_b_immediate(self, instruction):
        """Extract B-type immediate"""
        imm = (
            ((instruction >> 31) & 0x1) << 12 |
            ((instruction >> 7) & 0x1) << 11 |
            ((instruction >> 25) & 0x3F) << 5 |
            ((instruction >> 8) & 0xF) << 1
        )
        return self.cpu.sign_extend(imm, 13)
    
    def extract_j_immediate(self, instruction):
        """Extract J-type immediate"""
        imm = (
            ((instruction >> 31) & 0x1) << 20 |
            ((instruction >> 12) & 0xFF) << 12 |
            ((instruction >> 20) & 0x1) << 11 |
            ((instruction >> 21) & 0x3FF) << 1
        )
        return self.cpu.sign_extend(imm, 21)
    
    def execute_r_type(self, rd, funct3, rs1, rs2, funct7):
        """Execute R-type instructions"""
        val1 = self.cpu.read_register(rs1)
        val2 = self.cpu.read_register(rs2)
        
        if funct3 == 0b000:  # ADD/SUB
            if funct7 == 0b0000000:  # ADD
                result = (val1 + val2) & 0xFFFFFFFF
            elif funct7 == 0b0100000:  # SUB
                result = (val1 - val2) & 0xFFFFFFFF
            else:
                raise ValueError(f"Unknown funct7 for ADD/SUB: {funct7:#x}")
        elif funct3 == 0b001:  # SLL (shift left logical)
            result = (val1 << (val2 & 0x1F)) & 0xFFFFFFFF
        elif funct3 == 0b010:  # SLT (set less than)
            result = 1 if self.signed(val1) < self.signed(val2) else 0
        elif funct3 == 0b011:  # SLTU (set less than unsigned)
            result = 1 if val1 < val2 else 0
        elif funct3 == 0b100:  # XOR
            result = val1 ^ val2
        elif funct3 == 0b101:  # SRL/SRA (shift right)
            if funct7 == 0b0000000:  # SRL (logical)
                result = val1 >> (val2 & 0x1F)
            elif funct7 == 0b0100000:  # SRA (arithmetic)
                result = self.signed(val1) >> (val2 & 0x1F)
                result = result & 0xFFFFFFFF
            else:
                raise ValueError(f"Unknown funct7 for SRL/SRA: {funct7:#x}")
        elif funct3 == 0b110:  # OR
            result = val1 | val2
        elif funct3 == 0b111:  # AND
            result = val1 & val2
        else:
            raise ValueError(f"Unknown funct3 for R-type: {funct3:#x}")
        
        self.cpu.write_register(rd, result)
        self.cpu.pc += 4
    
    def execute_i_type(self, rd, funct3, rs1, imm, funct7):
        """Execute I-type instructions"""
        val = self.cpu.read_register(rs1)
        
        if funct3 == 0b000:  # ADDI
            result = (val + imm) & 0xFFFFFFFF
        elif funct3 == 0b010:  # SLTI (set less than immediate)
            result = 1 if self.signed(val) < self.signed(imm) else 0
        elif funct3 == 0b011:  # SLTIU (set less than immediate unsigned)
            result = 1 if val < (imm & 0xFFFFFFFF) else 0
        elif funct3 == 0b100:  # XORI
            result = val ^ imm
        elif funct3 == 0b110:  # ORI
            result = val | imm
        elif funct3 == 0b111:  # ANDI
            result = val & imm
        elif funct3 == 0b001:  # SLLI (shift left logical immediate)
            shamt = imm & 0x1F
            result = (val << shamt) & 0xFFFFFFFF
        elif funct3 == 0b101:  # SRLI/SRAI (shift right immediate)
            shamt = imm & 0x1F
            if (imm >> 10) & 0x1:  # SRAI (arithmetic)
                result = self.signed(val) >> shamt
                result = result & 0xFFFFFFFF
            else:  # SRLI (logical)
                result = val >> shamt
        else:
            raise ValueError(f"Unknown funct3 for I-type: {funct3:#x}")
        
        self.cpu.write_register(rd, result)
        self.cpu.pc += 4
    
    def execute_load(self, rd, funct3, rs1, imm):
        """Execute load instructions"""
        addr = (self.cpu.read_register(rs1) + imm) & 0xFFFFFFFF
        
        if funct3 == 0b000:  # LB (load byte)
            value = self.cpu.read_memory(addr, 1)
            value = self.cpu.sign_extend(value, 8)
        elif funct3 == 0b001:  # LH (load halfword)
            value = self.cpu.read_memory(addr, 2)
            value = self.cpu.sign_extend(value, 16)
        elif funct3 == 0b010:  # LW (load word)
            value = self.cpu.read_memory(addr, 4)
        elif funct3 == 0b100:  # LBU (load byte unsigned)
            value = self.cpu.read_memory(addr, 1)
        elif funct3 == 0b101:  # LHU (load halfword unsigned)
            value = self.cpu.read_memory(addr, 2)
        else:
            raise ValueError(f"Unknown funct3 for load: {funct3:#x}")
        
        self.cpu.write_register(rd, value)
        self.cpu.pc += 4
    
    def execute_store(self, funct3, rs1, rs2, imm):
        """Execute store instructions"""
        addr = (self.cpu.read_register(rs1) + imm) & 0xFFFFFFFF
        value = self.cpu.read_register(rs2)
        
        if funct3 == 0b000:  # SB (store byte)
            self.cpu.write_memory(addr, value, 1)
        elif funct3 == 0b001:  # SH (store halfword)
            self.cpu.write_memory(addr, value, 2)
        elif funct3 == 0b010:  # SW (store word)
            self.cpu.write_memory(addr, value, 4)
        else:
            raise ValueError(f"Unknown funct3 for store: {funct3:#x}")
        
        self.cpu.pc += 4
    
    def execute_branch(self, funct3, rs1, rs2, imm):
        """Execute branch instructions"""
        val1 = self.cpu.read_register(rs1)
        val2 = self.cpu.read_register(rs2)
        branch_taken = False
        
        if funct3 == 0b000:  # BEQ (branch if equal)
            branch_taken = (val1 == val2)
        elif funct3 == 0b001:  # BNE (branch if not equal)
            branch_taken = (val1 != val2)
        elif funct3 == 0b100:  # BLT (branch if less than)
            branch_taken = (self.signed(val1) < self.signed(val2))
        elif funct3 == 0b101:  # BGE (branch if greater than or equal)
            branch_taken = (self.signed(val1) >= self.signed(val2))
        elif funct3 == 0b110:  # BLTU (branch if less than unsigned)
            branch_taken = (val1 < val2)
        elif funct3 == 0b111:  # BGEU (branch if greater than or equal unsigned)
            branch_taken = (val1 >= val2)
        else:
            raise ValueError(f"Unknown funct3 for branch: {funct3:#x}")
        
        if branch_taken:
            self.cpu.pc = (self.cpu.pc + imm) & 0xFFFFFFFF
        else:
            self.cpu.pc += 4
    
    def execute_jal(self, rd, imm):
        """Execute JAL (jump and link)"""
        self.cpu.write_register(rd, self.cpu.pc + 4)
        self.cpu.pc = (self.cpu.pc + imm) & 0xFFFFFFFF
    
    def execute_jalr(self, rd, rs1, imm):
        """Execute JALR (jump and link register)"""
        target = (self.cpu.read_register(rs1) + imm) & 0xFFFFFFFE  # Clear LSB
        self.cpu.write_register(rd, self.cpu.pc + 4)
        self.cpu.pc = target
    
    def execute_lui(self, rd, imm):
        """Execute LUI (load upper immediate)"""
        self.cpu.write_register(rd, imm)
        self.cpu.pc += 4
    
    def execute_auipc(self, rd, imm):
        """Execute AUIPC (add upper immediate to PC)"""
        result = (self.cpu.pc + imm) & 0xFFFFFFFF
        self.cpu.write_register(rd, result)
        self.cpu.pc += 4
    
    def execute_system(self, instruction):
        """Execute ECALL/EBREAK"""
        imm = (instruction >> 20) & 0xFFF
        if imm == 0:  # ECALL
            # Stop execution on ECALL
            self.cpu.running = False
        elif imm == 1:  # EBREAK
            # Treat as halt for simulation
            self.cpu.running = False
        else:
            raise ValueError(f"Unknown system instruction: {imm:#x}")
        self.cpu.pc += 4
    
    def signed(self, value):
        """Convert unsigned 32-bit value to signed"""
        if value & 0x80000000:
            return value - 0x100000000
        return value
