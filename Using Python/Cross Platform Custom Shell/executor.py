import subprocess
import shlex
import platform
import re

class ShellExecutor:
    DANGEROUS_COMMANDS = {
        'rm -rf': 'File deletion',
        'format': 'Disk formatting',
        'shutdown': 'System shutdown',
        'del /': 'File deletion',
        'rd /': 'Directory deletion',
    }
    
    TIMEOUT_SECONDS = 10
    
    def __init__(self):
        self.os_type = platform.system().lower()
    
    def is_dangerous_command(self, command):
        """Check if the command is potentially dangerous"""
        command_lower = command.lower()
        return any(dangerous_cmd in command_lower for dangerous_cmd in self.DANGEROUS_COMMANDS)
    
    def sanitize_command(self, command):
        """Basic command sanitization"""
        # Remove any attempts to chain commands
        if self.os_type == 'windows':
            # Remove Windows command chaining operators
            command = re.sub(r'[&|><]', '', command)
        else:
            # Remove Unix command chaining operators
            command = re.sub(r'[;&|><]', '', command)
        return command.strip()
    
    def execute(self, command):
        """Execute a shell command safely and return the output"""
        if not command:
            raise ValueError("No command provided")
        
        # Check for dangerous commands
        if self.is_dangerous_command(command):
            raise ValueError(f"Command '{command}' is not allowed for security reasons")
        
        # Sanitize the command
        command = self.sanitize_command(command)
        
        try:
            # Execute the command with timeout
            if self.os_type == 'windows':
                # For Windows, use shell=True to handle built-in commands
                process = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT_SECONDS
                )
            else:
                # For Unix-like systems, split command and use shell=False
                process = subprocess.run(
                    shlex.split(command),
                    shell=False,
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT_SECONDS
                )
            
            # Combine stdout and stderr
            output = process.stdout
            if process.stderr:
                output += "\n" + process.stderr
                
            return output.strip()
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Command timed out after {self.TIMEOUT_SECONDS} seconds")
        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Error executing command: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}") 
