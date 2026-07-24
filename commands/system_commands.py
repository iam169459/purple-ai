"""
System Command Processing
Handles system-level operations like file management, application launching, etc.
"""
import os
import subprocess
import datetime
import platform
from typing import List, Dict, Any
from logger import logger

class SystemCommands:
    """Handles system-level commands and operations"""
    
    @staticmethod
    def search_files(query: str, directory: str = None) -> List[str]:
        """Search for files containing the query"""
        if directory is None:
            directory = os.getcwd()
        
        results = []
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if query.lower() in file.lower():
                        results.append(os.path.join(root, file))
                        
            logger.info(f"Found {len(results)} files matching '{query}'")
            return results[:10]  # Return top 10 results
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []
    
    @staticmethod
    def list_directory_contents(path: str = ".") -> List[str]:
        """List contents of a directory"""
        try:
            contents = os.listdir(path)
            logger.info(f"Listed {len(contents)} items in directory")
            return contents
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return [f"Error accessing directory: {str(e)}"]
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Get basic system information"""
        try:
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "node": platform.node(),
                "python_version": platform.python_version()
            }
            logger.info("System information retrieved")
            return info
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def create_note(content: str, filename: str = None) -> str:
        """Create a note with the given content"""
        try:
            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"note_{timestamp}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Note saved as {filename}")
            return f"Note saved as {filename}"
        except Exception as e:
            logger.error(f"Error creating note: {e}")
            return f"Error saving note: {str(e)}"
    
    @staticmethod
    def open_application(app_name: str) -> str:
        """Open system applications"""
        try:
            if os.name == 'nt':  # Windows
                if app_name.lower() == 'notepad':
                    subprocess.run(["notepad.exe"])
                    return "Opening Notepad"
                elif app_name.lower() == 'calculator':
                    subprocess.run(["calc.exe"])
                    return "Opening Calculator"
                else:
                    return f"Application '{app_name}' not supported"
            else:  # Linux/Mac
                if app_name.lower() == 'notepad':
                    subprocess.run(["nano"])  # Using nano as text editor
                    return "Opening text editor"
                elif app_name.lower() == 'calculator':
                    subprocess.run(["gnome-calculator"])
                    return "Opening calculator"
                else:
                    return f"Application '{app_name}' not supported"
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return f"Could not open {app_name}: {str(e)}"
    
    @staticmethod
    def system_control(action: str) -> str:
        """Handle system control commands"""
        try:
            if action.lower() == 'shutdown':
                confirmation = input("Do you really want to shut down your computer? (y/n): ")
                if confirmation.lower() == 'y':
                    if os.name == 'nt':  # Windows
                        subprocess.run(["shutdown", "/s", "/t", "1"])
                    else:  # Linux/Mac
                        subprocess.run(["sudo", "shutdown", "-h", "now"])
                    return "Shutting down the computer now"
                else:
                    return "Shutdown cancelled"
            
            elif action.lower() == 'restart':
                confirmation = input("Do you really want to restart your computer? (y/n): ")
                if confirmation.lower() == 'y':
                    if os.name == 'nt':  # Windows
                        subprocess.run(["shutdown", "/r", "/t", "1"])
                    else:  # Linux/Mac
                        subprocess.run(["sudo", "reboot"])
                    return "Restarting the computer now"
                else:
                    return "Restart cancelled"
            
            else:
                return f"System action '{action}' not supported"
                
        except Exception as e:
            logger.error(f"Error in system control: {e}")
            return f"Error performing system action: {str(e)}"