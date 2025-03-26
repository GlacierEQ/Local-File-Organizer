import os
import sys
import traceback
import logging
from typing import Optional, Callable, Any, Dict, List
from functools import wraps
from datetime import datetime
try:
    from rich.console import Console
except ImportError:
    print("Warning: rich package not installed. Install with: pip install rich")
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
from database import Database

class ErrorHandler:
    """Handles errors and exceptions in the file organization system"""
    
    def __init__(self, database: Database, log_file: str = "file_organizer.log"):
        self.database = database
        self.console = Console()
        self.setup_logging(log_file)

    def setup_logging(self, log_file: str):
        """Set up logging configuration"""
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def log_error(self, error: Exception, context: Dict[str, Any]):
        """Log error details to file and database"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now(),
            'context': context
        }

        # Log to file
        logging.error(
            f"Error: {error_info['error_type']}\n"
            f"Message: {error_info['error_message']}\n"
            f"Context: {error_info['context']}\n"
            f"Traceback:\n{error_info['traceback']}"
        )

        # Store in database
        if 'file_path' in context:
            self.database.log_operation(
                file_id=context.get('file_id'),
                operation_type=context.get('operation_type', 'unknown'),
                source=context.get('source', ''),
                destination=context.get('destination', ''),
                status='error',
                error=str(error)
            )

    def handle_error(self, error: Exception, context: Dict[str, Any], 
                    recovery_func: Optional[Callable] = None):
        """Handle an error with optional recovery"""
        self.log_error(error, context)

        # Display error to user
        self.console.print(f"[red]Error: {str(error)}[/red]")

        if recovery_func:
            try:
                recovery_func()
                self.console.print("[green]Recovery successful[/green]")
            except Exception as recovery_error:
                self.log_error(recovery_error, {
                    'context': 'recovery_attempt',
                    'original_error': str(error),
                    **context
                })
                self.console.print("[red]Recovery failed[/red]")

    def error_decorator(self, operation_type: str):
        """Decorator for error handling in file operations"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    context = {
                        'operation_type': operation_type,
                        'function_name': func.__name__,
                        'args': args,
                        'kwargs': kwargs
                    }
                    self.handle_error(e, context)
                    raise
            return wrapper
        return decorator

class RecoveryManager:
    """Manages recovery operations for failed file operations"""
    
    def __init__(self, database: Database):
        self.database = database

    def create_backup(self, file_path: str) -> str:
        """Create a backup of a file before modification"""
        import shutil
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def restore_from_backup(self, backup_path: str, original_path: str):
        """Restore a file from its backup"""
        import shutil
        shutil.copy2(backup_path, original_path)

    def cleanup_failed_operation(self, operation: Dict[str, Any]):
        """Clean up after a failed operation"""
        # Remove any partially created files
        if 'destination' in operation and os.path.exists(operation['destination']):
            try:
                os.remove(operation['destination'])
            except Exception:
                pass

        # Remove any empty directories
        if 'destination' in operation:
            dir_path = os.path.dirname(operation['destination'])
            try:
                os.rmdir(dir_path)  # Will only remove if empty
            except Exception:
                pass

    def get_failed_operations(self) -> List[Dict[str, Any]]:
        """Get list of failed operations from database"""
        with self.database.connect() as cursor:
            cursor.execute('''
                SELECT * FROM operations 
                WHERE status = 'error'
                ORDER BY timestamp DESC
            ''')
            return cursor.fetchall()

    def retry_failed_operation(self, operation: Dict[str, Any]):
        """Retry a failed operation"""
        # Implement retry logic based on operation type
        if operation['operation_type'] == 'move':
            import shutil
            shutil.move(operation['source'], operation['destination'])
        elif operation['operation_type'] == 'copy':
            import shutil
            shutil.copy2(operation['source'], operation['destination'])
        elif operation['operation_type'] == 'link':
            os.link(operation['source'], operation['destination'])
        
        # Update operation status in database
        self.database.update_operation_status(
            operation['id'], 
            'completed',
            error_message=None
        )

def setup_exception_handling():
    """Set up global exception handling"""
    def global_exception_handler(exctype, value, tb):
        """Global exception handler"""
        logging.error(
            "Uncaught exception:",
            exc_info=(exctype, value, tb)
        )
        # Display error to user
        Console().print(
            "[red]An unexpected error occurred. "
            "Check the log file for details.[/red]"
        )
        sys.__excepthook__(exctype, value, tb)  # Call original handler

    sys.excepthook = global_exception_handler
