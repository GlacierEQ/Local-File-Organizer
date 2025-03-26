import os
import logging
import logging.config
from typing import Optional, Dict, Any
import json
from datetime import datetime
from pathlib import Path

class LoggingManager:
    """Manages application logging configuration"""
    
    DEFAULT_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - "
                    "%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "logs/file_organizer.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": "logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "file_organizer": {
                "level": "DEBUG",
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "file_organizer.performance": {
                "level": "INFO",
                "handlers": ["file"],
                "propagate": False
            },
            "file_organizer.database": {
                "level": "INFO",
                "handlers": ["file"],
                "propagate": False
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"]
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.logs_dir = Path("logs")
        self._ensure_logs_directory()
        self._configure_logging()

    def _ensure_logs_directory(self):
        """Ensure logs directory exists"""
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create .gitignore for logs directory
        gitignore_path = self.logs_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text("*\n!.gitignore\n")

    def _configure_logging(self):
        """Configure logging using either file config or defaults"""
        config = self.DEFAULT_CONFIG.copy()
        
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path) as f:
                    file_config = json.load(f)
                config.update(file_config)
            except Exception as e:
                print(f"Error loading logging config: {str(e)}")
                print("Using default configuration")

        # Update log filenames with timestamp if specified
        if config.get("timestamp_files", False):
            timestamp = datetime.now().strftime("%Y%m%d")
            for handler in config["handlers"].values():
                if "filename" in handler:
                    filename = Path(handler["filename"])
                    handler["filename"] = str(
                        filename.parent / f"{filename.stem}_{timestamp}{filename.suffix}"
                    )

        # Ensure all log file paths are within logs directory
        for handler in config["handlers"].values():
            if "filename" in handler:
                handler["filename"] = str(self.logs_dir / Path(handler["filename"]).name)

        try:
            logging.config.dictConfig(config)
        except Exception as e:
            print(f"Error applying logging config: {str(e)}")
            print("Falling back to basic configuration")
            logging.basicConfig(level=logging.INFO)

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with the specified name"""
        return logging.getLogger(name)

    def update_log_level(self, logger_name: str, level: str):
        """Update the log level for a specific logger"""
        logger = logging.getLogger(logger_name)
        logger.setLevel(level.upper())

    def add_file_handler(self, logger_name: str, filename: str, 
                        level: str = "DEBUG", formatter: str = "detailed"):
        """Add a new file handler to a logger"""
        logger = logging.getLogger(logger_name)
        
        handler = logging.handlers.RotatingFileHandler(
            filename=str(self.logs_dir / filename),
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding="utf8"
        )
        
        handler.setLevel(level.upper())
        handler.setFormatter(
            logging.Formatter(
                self.DEFAULT_CONFIG["formatters"][formatter]["format"],
                datefmt=self.DEFAULT_CONFIG["formatters"][formatter]["datefmt"]
            )
        )
        
        logger.addHandler(handler)

    def remove_file_handler(self, logger_name: str, filename: str):
        """Remove a file handler from a logger"""
        logger = logging.getLogger(logger_name)
        
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler) and handler.baseFilename == str(self.logs_dir / filename):
                logger.removeHandler(handler)
                handler.close()

    def rotate_logs(self):
        """Force rotation of all log files"""
        for handler in logging._handlerList:
            handler = handler()  # Get actual handler from weak ref
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.doRollover()

    def cleanup_old_logs(self, days: int = 30):
        """Clean up log files older than specified days"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for file in self.logs_dir.glob("*.log.*"):
            if file.stat().st_mtime < cutoff:
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Error deleting old log file {file}: {str(e)}")

def setup_logging(config_path: Optional[str] = None) -> LoggingManager:
    """Setup logging for the application"""
    return LoggingManager(config_path)
