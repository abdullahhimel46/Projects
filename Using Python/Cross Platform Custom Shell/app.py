from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
import platform
from datetime import datetime
from shell.executor import ShellExecutor
from shell.mapper import CommandMapper

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize our shell components
shell_executor = ShellExecutor()
command_mapper = CommandMapper()

@app.route('/')
def index():
    return render_template('index.html', os_type=platform.system())

@app.route('/api/execute', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        # Map the command based on the OS
        mapped_command = command_mapper.map_command(command)
        # Execute the mapped command
        result = shell_executor.execute(mapped_command)
        
        # Store in session history
        if 'command_history' not in session:
            session['command_history'] = []
        
        session['command_history'].append({
            'command': command,
            'output': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'command': command,
            'mapped_command': mapped_command,
            'output': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    return jsonify(session.get('command_history', []))

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    session['command_history'] = []
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 
