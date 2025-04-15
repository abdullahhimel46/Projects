import platform
import re

class CommandMapper:
    def __init__(self):
        self.os_type = platform.system().lower()
        
        # Define command mappings from Linux to Windows
        self.windows_mappings = {
            r'^ls\b': 'dir',
            r'^pwd\b': 'cd',
            r'^clear\b': 'cls',
            r'^cat\b': 'type',
            r'^cp\b': 'copy',
            r'^mv\b': 'move',
            r'^rm\b': 'del',
            r'^touch\b': 'echo.>',
            r'^mkdir\b': 'mkdir',
            r'^rmdir\b': 'rmdir',
            r'^grep\b': 'findstr',
            r'^kill\b': 'taskkill',
            r'^ps\b': 'tasklist',
            r'^date\b': 'date /t',
            r'^time\b': 'time /t',
            r'^whoami\b': 'whoami',
            r'^echo\b': 'echo',
            r'^df\b': 'wmic logicaldisk get size,freespace,caption',
            r'^top\b': 'tasklist',
            r'^wget\b': 'curl',
        }
        
        # Define command mappings from Windows to Linux
        self.linux_mappings = {
            r'^dir\b': 'ls',
            r'^type\b': 'cat',
            r'^copy\b': 'cp',
            r'^move\b': 'mv',
            r'^del\b': 'rm',
            r'^cls\b': 'clear',
            r'^findstr\b': 'grep',
            r'^taskkill\b': 'kill',
            r'^tasklist\b': 'ps',
        }
    
    def map_command(self, command):
        """Map commands between platforms if necessary"""
        if not command:
            return command
            
        # If we're on Windows and the command looks like a Linux command
        if self.os_type == 'windows':
            for pattern, windows_cmd in self.windows_mappings.items():
                if re.match(pattern, command):
                    # Replace just the command part, preserve arguments
                    base_cmd = command.split()[0]
                    args = command[len(base_cmd):].strip()
                    return f"{windows_cmd} {args}".strip()
                    
        # If we're on Linux and the command looks like a Windows command
        elif self.os_type == 'linux':
            for pattern, linux_cmd in self.linux_mappings.items():
                if re.match(pattern, command):
                    # Replace just the command part, preserve arguments
                    base_cmd = command.split()[0]
                    args = command[len(base_cmd):].strip()
                    return f"{linux_cmd} {args}".strip()
        
        # If no mapping is found, return the original command
        return command
    
    def get_alternative_command(self, command):
        """Get alternative command suggestions for unsupported commands"""
        alternatives = {
            'top': 'Use tasklist or Task Manager on Windows',
            'ps': 'Use tasklist on Windows',
            'df': 'Use wmic logicaldisk get size,freespace,caption on Windows',
            'grep': 'Use findstr on Windows',
            'kill': 'Use taskkill on Windows',
        }
        
        base_cmd = command.split()[0]
        return alternatives.get(base_cmd, None) 
