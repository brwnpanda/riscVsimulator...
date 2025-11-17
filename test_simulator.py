"""
Test cases for RISC-V Simulator
Tests various instruction types and functionality
"""

import sys
sys.path.append('.')

from simulator import RISCVSimulator


def test_basic_arithmetic():
    """Test basic arithmetic instructions"""
    print("Testing basic arithmetic instructions...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 10
    addi x2, x0, 20
    add x3, x1, x2
    sub x4, x2, x1
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(1) == 10, "x1 should be 10"
    assert sim.cpu.read_register(2) == 20, "x2 should be 20"
    assert sim.cpu.read_register(3) == 30, "x3 should be 30"
    assert sim.cpu.read_register(4) == 10, "x4 should be 10"
    
    print("✓ Basic arithmetic test passed")


def test_logical_operations():
    """Test logical operations"""
    print("Testing logical operations...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 0b1100
    addi x2, x0, 0b1010
    and x3, x1, x2
    or x4, x1, x2
    xor x5, x1, x2
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(1) == 0b1100, "x1 should be 0b1100"
    assert sim.cpu.read_register(2) == 0b1010, "x2 should be 0b1010"
    assert sim.cpu.read_register(3) == 0b1000, "x3 should be 0b1000 (AND)"
    assert sim.cpu.read_register(4) == 0b1110, "x4 should be 0b1110 (OR)"
    assert sim.cpu.read_register(5) == 0b0110, "x5 should be 0b0110 (XOR)"
    
    print("✓ Logical operations test passed")


def test_shift_operations():
    """Test shift operations"""
    print("Testing shift operations...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 8
    slli x2, x1, 2
    srli x3, x1, 1
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(1) == 8, "x1 should be 8"
    assert sim.cpu.read_register(2) == 32, "x2 should be 32 (8 << 2)"
    assert sim.cpu.read_register(3) == 4, "x3 should be 4 (8 >> 1)"
    
    print("✓ Shift operations test passed")


def test_load_store():
    """Test load and store operations"""
    print("Testing load and store operations...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 42
    addi x2, x0, 100
    sw x1, 0(x2)
    lw x3, 0(x2)
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(1) == 42, "x1 should be 42"
    assert sim.cpu.read_register(3) == 42, "x3 should be 42 (loaded from memory)"
    
    print("✓ Load/store test passed")


def test_branches():
    """Test branch instructions"""
    print("Testing branch instructions...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 10
    addi x2, x0, 10
    addi x3, x0, 0
    beq x1, x2, equal
    addi x3, x0, 1
    equal:
    addi x4, x0, 100
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(3) == 0, "x3 should be 0 (branch taken)"
    assert sim.cpu.read_register(4) == 100, "x4 should be 100"
    
    print("✓ Branch test passed")


def test_jump_instructions():
    """Test jump instructions"""
    print("Testing jump instructions...")
    sim = RISCVSimulator()
    
    code = """
    jal x1, target
    addi x2, x0, 99
    target:
    addi x3, x0, 50
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(2) == 0, "x2 should be 0 (instruction skipped)"
    assert sim.cpu.read_register(3) == 50, "x3 should be 50"
    
    print("✓ Jump test passed")


def test_upper_immediate():
    """Test upper immediate instructions"""
    print("Testing upper immediate instructions...")
    sim = RISCVSimulator()
    
    code = """
    lui x1, 0x12345000
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    expected = 0x12345000
    assert sim.cpu.read_register(1) == expected, f"x1 should be {expected:#x}"
    
    print("✓ Upper immediate test passed")


def test_comparison():
    """Test comparison instructions"""
    print("Testing comparison instructions...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 5
    addi x2, x0, 10
    slt x3, x1, x2
    slt x4, x2, x1
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    assert sim.cpu.read_register(3) == 1, "x3 should be 1 (5 < 10)"
    assert sim.cpu.read_register(4) == 0, "x4 should be 0 (10 not < 5)"
    
    print("✓ Comparison test passed")


def test_fibonacci():
    """Test Fibonacci calculation"""
    print("Testing Fibonacci calculation...")
    sim = RISCVSimulator()
    
    code = """
    addi x10, x0, 0
    addi x11, x0, 1
    addi x12, x0, 10
    
    loop:
    add x13, x10, x11
    addi x10, x11, 0
    addi x11, x13, 0
    addi x12, x12, -1
    bne x12, x0, loop
    
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    # After 10 iterations, x11 should contain the 11th Fibonacci number
    assert sim.cpu.read_register(11) == 89, "x11 should be 89 (11th Fibonacci)"
    
    print("✓ Fibonacci test passed")


def test_memory_operations():
    """Test various memory operations"""
    print("Testing memory operations...")
    sim = RISCVSimulator()
    
    code = """
    addi x1, x0, 0xFF
    addi x2, x0, 100
    sb x1, 0(x2)
    lb x3, 0(x2)
    lbu x4, 0(x2)
    ecall
    """
    
    success, msg = sim.load_assembly(code)
    assert success, f"Failed to load code: {msg}"
    
    success, msg = sim.run()
    assert success, f"Failed to run: {msg}"
    
    # lb should sign-extend, lbu should not
    assert sim.cpu.read_register(3) == 0xFFFFFFFF, "x3 should be sign-extended"
    assert sim.cpu.read_register(4) == 0xFF, "x4 should not be sign-extended"
    
    print("✓ Memory operations test passed")


def run_all_tests():
    """Run all test cases"""
    print("=" * 50)
    print("RISC-V Simulator Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_basic_arithmetic,
        test_logical_operations,
        test_shift_operations,
        test_load_store,
        test_branches,
        test_jump_instructions,
        test_upper_immediate,
        test_comparison,
        test_fibonacci,
        test_memory_operations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
