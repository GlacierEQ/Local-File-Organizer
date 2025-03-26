import os
import sys
from typing import Optional, Dict, Any
from config import Config
from database import Database
from error_handler import ErrorHandler, RecoveryManager
from performance import PerformanceOptimizer, MemoryManager

class SystemManager:
    """Manages system initialization, configuration, and shutdown"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.json"
        self.config: Optional[Config] = None
        self.database: Optional[Database] = None
        self.error_handler: Optional[ErrorHandler] = None
        self.recovery_manager: Optional[RecoveryManager] = None
        self.performance_optimizer: Optional[PerformanceOptimizer] = None
        self.memory_manager: Optional[MemoryManager] = None
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize all system components"""
        try:
            # Initialize configuration
            self.config = Config(self.config_path)
            
            # Initialize database
            self.database = Database("file_organizer.db")
            
            # Initialize error handling
            self.error_handler = ErrorHandler(self.database)
            self.recovery_manager = RecoveryManager(self.database)
            
            # Initialize performance optimization
            self.performance_optimizer = PerformanceOptimizer(self.config, self.database)
            self.memory_manager = MemoryManager()
            
            self._initialized = True
            return True
        except Exception as e:
            print(f"Error initializing system: {str(e)}")
            return False

    def check_dependencies(self) -> Dict[str, bool]:
        """Check if all required dependencies are installed"""
        dependencies = {
            'rich': True,
            'psutil': True,
            'nltk': True,
            'PIL': True,
            'fitz': True,
            'docx': True,
            'pandas': True,
            'pptx': True,
            'pytesseract': True
        }

        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                dependencies[dep] = False

        return dependencies

    def install_missing_dependencies(self):
        """Install missing dependencies"""
        import subprocess
        import sys

        dependencies = self.check_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]

        if missing:
            print("Installing missing dependencies...")
            for dep in missing:
                try:
                    subprocess.check_call([
                        sys.executable, 
                        "-m", 
                        "pip", 
                        "install", 
                        dep
                    ])
                    print(f"Successfully installed {dep}")
                except subprocess.CalledProcessError:
                    print(f"Failed to install {dep}")

    def validate_environment(self) -> Dict[str, Any]:
        """Validate the system environment"""
        environment = {
            'python_version': sys.version,
            'os_platform': sys.platform,
            'working_directory': os.getcwd(),
            'dependencies': self.check_dependencies(),
            'database_connected': False,
            'config_loaded': False
        }

        if self.database:
            try:
                # Test database connection
                with self.database.connect() as cursor:
                    cursor.execute("SELECT 1")
                environment['database_connected'] = True
            except Exception:
                pass

            if self.config:
                try:
                    # Test config loading
                    self.config.load_config()
                    environment['config_loaded'] = True
                except Exception:
                    pass

            return environment

    def cleanup(self):
        """Clean up system resources"""
        if self.database:
            # Clean up old cache entries
            self.database.cleanup_old_cache()
            
        if self.performance_optimizer:
            # Clear all caches
            self.performance_optimizer.clear_all_caches()

    def shutdown(self):
        """Shutdown the system gracefully"""
        if not self._initialized:
            return

        try:
            # Save current configuration
            if self.config:
                self.config.save_config()

            # Clean up resources
            self.cleanup()

            # Close database connection
            if self.database:
                try:
                    self.database.cleanup_old_cache()  # Final cleanup
                except Exception:
                    pass

            self._initialized = False
        except Exception as e:
            print(f"Error during shutdown: {str(e)}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        if not self._initialized:
            return {'status': 'not_initialized'}

        status = {
            'initialized': self._initialized,
            'environment': self.validate_environment(),
            'memory_usage': self.memory_manager.get_memory_usage() if self.memory_manager else None,
            'database_status': 'connected' if self.database else 'disconnected',
            'config_status': 'loaded' if self.config else 'not_loaded'
        }

        return status

    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
        if exc_type is not None:
            # Log the error if one occurred
            if self.error_handler:
                self.error_handler.log_error(
                    exc_val,
                    {'context': 'system_shutdown'}
                )
            return False  # Re-raise the exception
        return True
