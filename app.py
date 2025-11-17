"""
RISC-V Simulator Web Application
Flask-based web interface for the RISC-V simulator
"""

from flask import Flask, render_template, request, jsonify
from simulator import RISCVSimulator

app = Flask(__name__)
simulator = RISCVSimulator()

# Example programs
EXAMPLE_PROGRAMS = {
    'fibonacci': '''# Calculate Fibonacci numbers
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
''',
    'factorial': '''# Calculate 5! (factorial)
addi x10, x0, 5    # n = 5
addi x11, x0, 1    # result = 1

loop:
beq x10, x0, done  # if n == 0, done
mul:
add x12, x0, x0    # temp = 0
add x13, x0, x11   # copy result

mult_loop:
beq x10, x0, mult_done
add x12, x12, x13  # temp += result
addi x10, x10, -1  # n--
jal x0, mult_loop

mult_done:
addi x11, x12, 0   # result = temp
jal x0, loop

done:
ecall              # halt
''',
    'array_sum': '''# Sum array elements
addi x10, x0, 0    # sum = 0
addi x11, x0, 100  # array base address
addi x12, x0, 5    # array size

# Initialize array in memory
addi x13, x0, 10
sw x13, 0(x11)
addi x13, x0, 20
sw x13, 4(x11)
addi x13, x0, 30
sw x13, 8(x11)
addi x13, x0, 40
sw x13, 12(x11)
addi x13, x0, 50
sw x13, 16(x11)

# Sum loop
addi x14, x0, 0    # index = 0
loop:
beq x14, x12, done # if index == size, done
slli x15, x14, 2   # offset = index * 4
add x15, x11, x15  # address = base + offset
lw x16, 0(x15)     # load value
add x10, x10, x16  # sum += value
addi x14, x14, 1   # index++
jal x0, loop

done:
ecall              # halt (sum in x10)
''',
    'simple_add': '''# Simple addition example
addi x1, x0, 10    # x1 = 10
addi x2, x0, 20    # x2 = 20
add x3, x1, x2     # x3 = x1 + x2 = 30
ecall              # halt
'''
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', examples=EXAMPLE_PROGRAMS.keys())

@app.route('/api/load', methods=['POST'])
def load_code():
    """Load assembly code"""
    data = request.json
    code = data.get('code', '')
    
    simulator.reset()
    success, message = simulator.load_assembly(code)
    
    if success:
        state = simulator.get_state()
        return jsonify({
            'success': True,
            'message': message,
            'state': state,
            'register_names': simulator.get_register_names()
        })
    else:
        return jsonify({
            'success': False,
            'message': message
        })

@app.route('/api/step', methods=['POST'])
def step():
    """Execute one instruction"""
    success, message = simulator.step()
    
    state = simulator.get_state()
    return jsonify({
        'success': success,
        'message': message,
        'state': state,
        'register_names': simulator.get_register_names()
    })

@app.route('/api/run', methods=['POST'])
def run():
    """Run until halt"""
    data = request.json
    max_steps = data.get('max_steps', 1000)
    
    success, message = simulator.run(max_steps)
    
    state = simulator.get_state()
    return jsonify({
        'success': success,
        'message': message,
        'state': state,
        'register_names': simulator.get_register_names()
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset simulator"""
    success, message = simulator.reset()
    
    state = simulator.get_state()
    return jsonify({
        'success': success,
        'message': message,
        'state': state,
        'register_names': simulator.get_register_names()
    })

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current state"""
    state = simulator.get_state()
    return jsonify({
        'state': state,
        'register_names': simulator.get_register_names()
    })

@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get memory dump"""
    start = int(request.args.get('start', 0))
    size = int(request.args.get('size', 256))
    
    memory = simulator.get_memory_dump(start, size)
    return jsonify({
        'memory': memory
    })

@app.route('/api/example/<name>', methods=['GET'])
def get_example(name):
    """Get example program"""
    if name in EXAMPLE_PROGRAMS:
        return jsonify({
            'success': True,
            'code': EXAMPLE_PROGRAMS[name]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Example not found'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
