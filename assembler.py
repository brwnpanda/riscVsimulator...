"""
RISC-V Assembler
Converts RISC-V assembly code to machine code
"""

class RISCVAssembler:
    """Simple RISC-V assembler for RV32I"""
    
    # Register name to number mapping
    REGISTERS = {
        'x0': 0, 'zero': 0,
        'x1': 1, 'ra': 1,
        'x2': 2, 'sp': 2,
        'x3': 3, 'gp': 3,
        'x4': 4, 'tp': 4,
        'x5': 5, 't0': 5,
        'x6': 6, 't1': 6,
        'x7': 7, 't2': 7,
        'x8': 8, 's0': 8, 'fp': 8,
        'x9': 9, 's1': 9,
        'x10': 10, 'a0': 10,
        'x11': 11, 'a1': 11,
        'x12': 12, 'a2': 12,
        'x13': 13, 'a3': 13,
        'x14': 14, 'a4': 14,
        'x15': 15, 'a5': 15,
        'x16': 16, 'a6': 16,
        'x17': 17, 'a7': 17,
        'x18': 18, 's2': 18,
        'x19': 19, 's3': 19,
        'x20': 20, 's4': 20,
        'x21': 21, 's5': 21,
        'x22': 22, 's6': 22,
        'x23': 23, 's7': 23,
        'x24': 24, 's8': 24,
        'x25': 25, 's9': 25,
        'x26': 26, 's10': 26,
        'x27': 27, 's11': 27,
        'x28': 28, 't3': 28,
        'x29': 29, 't4': 29,
        'x30': 30, 't5': 30,
        'x31': 31, 't6': 31,
    }
    
    def __init__(self):
        self.labels = {}
        self.instructions = []
        
    def parse_register(self, reg_str):
        """Parse register name to number"""
        reg_str = reg_str.strip().lower()
        if reg_str in self.REGISTERS:
            return self.REGISTERS[reg_str]
        raise ValueError(f"Unknown register: {reg_str}")
    
    def parse_immediate(self, imm_str):
        """Parse immediate value"""
        imm_str = imm_str.strip()
        if imm_str.startswith('0x'):
            return int(imm_str, 16)
        elif imm_str.startswith('0b'):
            return int(imm_str, 2)
        else:
            return int(imm_str)
    
    def encode_r_type(self, opcode, rd, funct3, rs1, rs2, funct7):
        """Encode R-type instruction"""
        return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    
    def encode_i_type(self, opcode, rd, funct3, rs1, imm):
        """Encode I-type instruction"""
        imm = imm & 0xFFF
        return (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    
    def encode_s_type(self, opcode, funct3, rs1, rs2, imm):
        """Encode S-type instruction"""
        imm = imm & 0xFFF
        imm_11_5 = (imm >> 5) & 0x7F
        imm_4_0 = imm & 0x1F
        return (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
    
    def encode_b_type(self, opcode, funct3, rs1, rs2, imm):
        """Encode B-type instruction"""
        imm = imm & 0x1FFF
        imm_12 = (imm >> 12) & 0x1
        imm_10_5 = (imm >> 5) & 0x3F
        imm_4_1 = (imm >> 1) & 0xF
        imm_11 = (imm >> 11) & 0x1
        return (imm_12 << 31) | (imm_10_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_1 << 8) | (imm_11 << 7) | opcode
    
    def encode_u_type(self, opcode, rd, imm):
        """Encode U-type instruction"""
        imm = imm & 0xFFFFF000
        return imm | (rd << 7) | opcode
    
    def encode_j_type(self, opcode, rd, imm):
        """Encode J-type instruction"""
        imm = imm & 0x1FFFFF
        imm_20 = (imm >> 20) & 0x1
        imm_10_1 = (imm >> 1) & 0x3FF
        imm_11 = (imm >> 11) & 0x1
        imm_19_12 = (imm >> 12) & 0xFF
        return (imm_20 << 31) | (imm_19_12 << 12) | (imm_11 << 20) | (imm_10_1 << 21) | (rd << 7) | opcode
    
    def assemble_instruction(self, line, pc):
        """Assemble a single instruction"""
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')]
        
        parts = line.replace(',', ' ').split()
        if not parts:
            return None
        
        op = parts[0].lower()
        
        # R-type instructions
        if op == 'add':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b000, rs1, rs2, 0b0000000)
        elif op == 'sub':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b000, rs1, rs2, 0b0100000)
        elif op == 'xor':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b100, rs1, rs2, 0b0000000)
        elif op == 'or':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b110, rs1, rs2, 0b0000000)
        elif op == 'and':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b111, rs1, rs2, 0b0000000)
        elif op == 'sll':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b001, rs1, rs2, 0b0000000)
        elif op == 'srl':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b101, rs1, rs2, 0b0000000)
        elif op == 'sra':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b101, rs1, rs2, 0b0100000)
        elif op == 'slt':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b010, rs1, rs2, 0b0000000)
        elif op == 'sltu':
            rd, rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2, 3]]
            return self.encode_r_type(0b0110011, rd, 0b011, rs1, rs2, 0b0000000)
        
        # I-type instructions
        elif op == 'addi':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b000, rs1, imm)
        elif op == 'xori':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b100, rs1, imm)
        elif op == 'ori':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b110, rs1, imm)
        elif op == 'andi':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b111, rs1, imm)
        elif op == 'slti':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b010, rs1, imm)
        elif op == 'sltiu':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b011, rs1, imm)
        elif op == 'slli':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            shamt = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b001, rs1, shamt)
        elif op == 'srli':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            shamt = self.parse_immediate(parts[3])
            return self.encode_i_type(0b0010011, rd, 0b101, rs1, shamt)
        elif op == 'srai':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            shamt = self.parse_immediate(parts[3]) | 0x400
            return self.encode_i_type(0b0010011, rd, 0b101, rs1, shamt)
        
        # Load instructions
        elif op == 'lb':
            rd = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_i_type(0b0000011, rd, 0b000, rs1, imm)
        elif op == 'lh':
            rd = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_i_type(0b0000011, rd, 0b001, rs1, imm)
        elif op == 'lw':
            rd = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_i_type(0b0000011, rd, 0b010, rs1, imm)
        elif op == 'lbu':
            rd = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_i_type(0b0000011, rd, 0b100, rs1, imm)
        elif op == 'lhu':
            rd = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_i_type(0b0000011, rd, 0b101, rs1, imm)
        
        # Store instructions
        elif op == 'sb':
            rs2 = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_s_type(0b0100011, 0b000, rs1, rs2, imm)
        elif op == 'sh':
            rs2 = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_s_type(0b0100011, 0b001, rs1, rs2, imm)
        elif op == 'sw':
            rs2 = self.parse_register(parts[1])
            offset_base = parts[2].split('(')
            imm = self.parse_immediate(offset_base[0])
            rs1 = self.parse_register(offset_base[1].rstrip(')'))
            return self.encode_s_type(0b0100011, 0b010, rs1, rs2, imm)
        
        # Branch instructions
        elif op in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']:
            rs1, rs2 = [self.parse_register(parts[i]) for i in [1, 2]]
            if parts[3] in self.labels:
                imm = self.labels[parts[3]] - pc
            else:
                imm = self.parse_immediate(parts[3])
            
            funct3_map = {'beq': 0b000, 'bne': 0b001, 'blt': 0b100, 'bge': 0b101, 'bltu': 0b110, 'bgeu': 0b111}
            return self.encode_b_type(0b1100011, funct3_map[op], rs1, rs2, imm)
        
        # Jump instructions
        elif op == 'jal':
            rd = self.parse_register(parts[1])
            if parts[2] in self.labels:
                imm = self.labels[parts[2]] - pc
            else:
                imm = self.parse_immediate(parts[2])
            return self.encode_j_type(0b1101111, rd, imm)
        elif op == 'jalr':
            rd, rs1 = [self.parse_register(parts[i]) for i in [1, 2]]
            imm = self.parse_immediate(parts[3]) if len(parts) > 3 else 0
            return self.encode_i_type(0b1100111, rd, 0b000, rs1, imm)
        
        # Upper immediate instructions
        elif op == 'lui':
            rd = self.parse_register(parts[1])
            imm = self.parse_immediate(parts[2])
            return self.encode_u_type(0b0110111, rd, imm)
        elif op == 'auipc':
            rd = self.parse_register(parts[1])
            imm = self.parse_immediate(parts[2])
            return self.encode_u_type(0b0010111, rd, imm)
        
        # System instructions
        elif op == 'ecall':
            return 0b1110011
        elif op == 'ebreak':
            return 0b1110011 | (1 << 20)
        
        else:
            raise ValueError(f"Unknown instruction: {op}")
    
    def assemble(self, code):
        """Assemble RISC-V assembly code to machine code"""
        lines = code.split('\n')
        self.labels = {}
        self.instructions = []
        
        # First pass: collect labels
        pc = 0
        for line in lines:
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                label = line.split(':')[0].strip()
                self.labels[label] = pc
                line = line.split(':', 1)[1].strip() if ':' in line else ''
            
            if line and not line.startswith('#'):
                if '#' in line:
                    line = line[:line.index('#')]
                parts = line.replace(',', ' ').split()
                if parts:
                    pc += 4
        
        # Second pass: assemble instructions
        pc = 0
        for line in lines:
            if ':' in line:
                line = line.split(':', 1)[1].strip() if ':' in line else ''
            
            instruction = self.assemble_instruction(line, pc)
            if instruction is not None:
                self.instructions.append(instruction)
                pc += 4
        
        return self.instructions
