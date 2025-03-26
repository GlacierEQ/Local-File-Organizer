import os
import sys
from typing import Optional, Dict, Any
from config import Config
from database_new import Database
from error_handler import ErrorHandler, RecoveryManager
from performance import PerformanceOptimizer, MemoryManager
from migrations.migration_manager import MigrationManager
from logging_config import setup_logging

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
        self.migration_manager: Optional[MigrationManager] = None
        self.logger = None
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize all system components"""
        try:
            # Set up logging first
            logging_manager = setup_logging()
            self.logger = logging_manager.get_logger("file_organizer")
            self.logger.info("Initializing system...")

            # Initialize configuration
            self.config = Config(self.config_path)
            self.logger.info("Configuration loaded")
            
            # Initialize database and run migrations
            self.database = Database("file_organizer.db")
            self.migration_manager = MigrationManager(self.database.db_path)
            self._run_migrations()
            self.logger.info("Database initialized and migrations applied")
            
            # Initialize error handling
            self.error_handler = ErrorHandler(self.database)
            self.recovery_manager = RecoveryManager(self.database)
            self.logger.info("Error handling system initialized")
            
            # Initialize performance optimization
            self.performance_optimizer = PerformanceOptimizer(self.config, self.database)
            self.memory_manager = MemoryManager()
            self.logger.info("Performance optimization system initialized")
            
            self._initialized = True
            self.logger.info("System initialization completed successfully")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error initializing system: {str(e)}", exc_info=True)
            else:
                print(f"Error initializing system: {str(e)}")
            return False

    def _run_migrations(self):
        """Run any pending database migrations"""
        try:
            pending = self.migration_manager.get_pending_migrations()
            if pending:
                self.logger.info(f"Applying {len(pending)} pending migrations...")
                self.migration_manager.migrate()
                self.logger.info("Migrations completed successfully")
        except Exception as e:
            self.logger.error(f"Error applying migrations: {str(e)}", exc_info=True)
            raise

    def check_dependencies(self) -> Dict[str, bool]:
        """Check if all required dependencies are installed"""
        self.logger.info("Checking system dependencies...")
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
                self.logger.warning(f"Dependency '{dep}' not found")

        return dependencies

    def install_missing_dependencies(self):
        """Install missing dependencies"""
        self.logger.info("Installing missing dependencies...")
        import subprocess

        dependencies = self.check_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]

        if missing:
            for dep in missing:
                try:
                    self.logger.info(f"Installing {dep}...")
                    subprocess.check_call([
                        sys.executable, 
                        "-m", 
                        "pip", 
                        "install", 
                        dep
                    ])
                    self.logger.info(f"Successfully installed {dep}")
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Failed to install {dep}: {str(e)}")

    def validate_environment(self) -> Dict[str, Any]:
        """Validate the system environment"""
        self.logger.info("Validating system environment...")
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
                with self.database.connect() as cursor:
                    cursor.execute("SELECT 1")
                environment['database_connected'] = True
                self.logger.info("Database connection verified")
            except Exception as e:
                self.logger.error(f"Database connection failed: {str(e)}")

        if self.config:
            try:
                self.config.load_config()
                environment['config_loaded'] = True
                self.logger.info("Configuration verified")
            except Exception as e:
                self.logger.error(f"Configuration validation failed: {str(e)}")

        return environment

    def cleanup(self):
        """Clean up system resources"""
        if not self._initialized:
            return

        self.logger.info("Cleaning up system resources...")
        
        if self.database:
            try:
                self.database.cleanup_old_cache()
                self.logger.info("Database cache cleaned")
            except Exception as e:
                self.logger.error(f"Error cleaning database cache: {str(e)}")
            
        if self.performance_optimizer:
            try:
                self.performance_optimizer.clear_all_caches()
                self.logger.info("Performance caches cleared")
            except Exception as e:
                self.logger.error(f"Error clearing performance caches: {str(e)}")

    def shutdown(self):
        """Shutdown the system gracefully"""
        if not self._initialized:
            return

        self.logger.info("Initiating system shutdown...")

        try:
            # Save current configuration
            if self.config:
                self.config.save_config()
                self.logger.info("Configuration saved")

            # Clean up resources
            self.cleanup()
            self.logger.info("Resource cleanup completed")

            self._initialized = False
            self.logger.info("System shutdown completed successfully")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {str(e)}", exc_info=True)

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        if not self._initialized:
            return {'status': 'not_initialized'}

        self.logger.debug("Retrieving system status...")
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
