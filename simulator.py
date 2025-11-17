"""
RISC-V Simulator Main Class
Combines CPU core, decoder, and assembler
"""

from cpu_core import RISCVCPUCore
from instruction_decoder import InstructionDecoder
from assembler import RISCVAssembler


class RISCVSimulator:
    """Complete RISC-V Simulator"""
    
    def __init__(self):
        self.cpu = RISCVCPUCore()
        self.decoder = InstructionDecoder(self.cpu)
        self.assembler = RISCVAssembler()
        self.execution_log = []
        
    def load_assembly(self, code):
        """Load and assemble RISC-V assembly code"""
        try:
            instructions = self.assembler.assemble(code)
            self.cpu.load_program(instructions)
            return True, f"Loaded {len(instructions)} instructions"
        except Exception as e:
            return False, f"Assembly error: {str(e)}"
    
    def load_machine_code(self, instructions):
        """Load machine code directly"""
        try:
            self.cpu.load_program(instructions)
            return True, f"Loaded {len(instructions)} instructions"
        except Exception as e:
            return False, f"Load error: {str(e)}"
    
    def step(self):
        """Execute one instruction"""
        if self.cpu.instruction_count >= self.cpu.max_instructions:
            return False, "Maximum instruction count reached"
        
        # Check if PC is within program bounds
        if self.cpu.pc >= self.cpu.program_size:
            return False, "Program counter out of bounds (end of program)"
        
        try:
            # Fetch instruction
            instruction = self.cpu.read_memory(self.cpu.pc, 4)
            
            # Check for invalid instruction (all zeros)
            if instruction == 0:
                return False, "Invalid instruction (0x0) - end of program"
            
            # Record state before execution
            old_pc = self.cpu.pc
            old_regs = [self.cpu.read_register(i) for i in range(32)]
            
            # Execute instruction
            self.decoder.decode_and_execute(instruction)
            
            # Log execution
            log_entry = {
                'pc': old_pc,
                'instruction': instruction,
                'instruction_hex': f"0x{instruction:08x}",
                'registers_changed': []
            }
            
            # Find changed registers
            for i in range(32):
                new_val = self.cpu.read_register(i)
                if old_regs[i] != new_val:
                    log_entry['registers_changed'].append({
                        'reg': i,
                        'old': old_regs[i],
                        'new': new_val
                    })
            
            self.execution_log.append(log_entry)
            
            return True, "Step executed"
        except Exception as e:
            return False, f"Execution error: {str(e)}"
    
    def run(self, max_steps=None):
        """Run until halt or error"""
        self.cpu.running = True
        steps = 0
        max_steps = max_steps or self.cpu.max_instructions
        
        while self.cpu.running and steps < max_steps:
            success, message = self.step()
            if not success:
                return False, message
            steps += 1
            
            # Check if PC is out of bounds or at end of program
            if self.cpu.pc >= len([i for i in range(self.cpu.memory_size) if self.cpu.memory[i] != 0]) * 4:
                break
        
        return True, f"Executed {steps} instructions"
    
    def reset(self):
        """Reset simulator"""
        self.cpu.reset()
        self.execution_log = []
        return True, "Simulator reset"
    
    def get_state(self):
        """Get current CPU state"""
        state = self.cpu.get_state()
        state['execution_log'] = self.execution_log[-10:]  # Last 10 entries
        return state
    
    def get_register_names(self):
        """Get register names for display"""
        return [
            'x0/zero', 'x1/ra', 'x2/sp', 'x3/gp', 'x4/tp', 'x5/t0', 'x6/t1', 'x7/t2',
            'x8/s0/fp', 'x9/s1', 'x10/a0', 'x11/a1', 'x12/a2', 'x13/a3', 'x14/a4', 'x15/a5',
            'x16/a6', 'x17/a7', 'x18/s2', 'x19/s3', 'x20/s4', 'x21/s5', 'x22/s6', 'x23/s7',
            'x24/s8', 'x25/s9', 'x26/s10', 'x27/s11', 'x28/t3', 'x29/t4', 'x30/t5', 'x31/t6'
        ]
    
    def get_memory_dump(self, start=0, size=256):
        """Get memory dump for display"""
        end = min(start + size, self.cpu.memory_size)
        dump = []
        for addr in range(start, end, 4):
            try:
                value = self.cpu.read_memory(addr, 4)
                dump.append({
                    'address': f"0x{addr:08x}",
                    'value': f"0x{value:08x}",
                    'decimal': value
                })
            except:
                break
        return dump
