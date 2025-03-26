import os
import time
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from system_manager_new import SystemManager
from file_utils import (
    display_directory_tree,
    collect_file_paths,
    separate_files_by_type,
    read_file_data
)
from data_processing_common import (
    compute_operations,
    execute_operations,
    process_files_by_date,
    process_files_by_type,
)
from text_data_processing import process_text_files
from image_data_processing import process_image_files
from legal_data_processing import LegalDocumentProcessor
from output_filter import filter_specific_output

class FileOrganizer:
    """Main file organization system"""
    
    def __init__(self):
        self.system = SystemManager()
        self.system.initialize()
        self.silent_mode = False
        self.log_file = None
        self._initialize_system()

    def _initialize_system(self):
        """Initialize the system and its dependencies"""
        # Check and install dependencies
        missing_deps = [
            dep for dep, installed in self.system.check_dependencies().items() 
            if not installed
        ]
        if missing_deps:
            self.system.install_missing_dependencies()

        # Initialize NLTK data if available
        try:
            import nltk
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            nltk.download('wordnet', quiet=True)
        except ImportError:
            self.log_message("NLTK not installed. Some text processing features may be limited.")
        except Exception as e:
            self.system.error_handler.log_error(
                e, {'context': 'nltk_initialization'}
            )
            self.log_message("Warning: Error initializing NLTK. Some text processing features may be limited.")

    def set_silent_mode(self, enabled: bool):
        """Set silent mode and configure logging"""
        self.silent_mode = enabled
        if enabled:
            self.log_file = 'operation_log.txt'
        else:
            self.log_file = None

    def log_message(self, message: str):
        """Log a message based on silent mode setting"""
        if self.silent_mode:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')
        else:
            print(message)

    @contextmanager
    def error_handling(self, context: Dict[str, Any]):
        """Context manager for error handling"""
        try:
            yield
        except Exception as e:
            self.system.error_handler.handle_error(e, context)
            raise

    def organize_directory(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Organize files in the specified directory"""
        with self.error_handling({'operation': 'organize_directory', 'input_path': input_path}):
            # Validate input path
            if not os.path.exists(input_path):
                raise ValueError(f"Input path {input_path} does not exist")

            # Set default output path if not provided
            if not output_path:
                output_path = os.path.join(os.path.dirname(input_path), 'organized_folder')

            self.log_message(f"Input path: {input_path}")
            self.log_message(f"Output path: {output_path}")

            # Collect and process files
            start_time = time.time()
            file_paths = collect_file_paths(input_path)
            end_time = time.time()

            self.log_message(f"Time taken to load file paths: {end_time - start_time:.2f} seconds")

            if not self.silent_mode:
                print("Directory tree before organizing:")
                display_directory_tree(input_path)

            return self._process_files(file_paths, output_path)

    def _get_organization_mode(self) -> str:
        """Get the organization mode from user input"""
        while True:
            print("\nPlease choose the mode to organize your files:")
            print("1. By Content")
            print("2. By Date")
            print("3. By Type")
            print("4. Checklist Mode")
            
            response = input("Enter 1-4 (or '/exit' to quit): ").strip()
            
            if response == '/exit':
                raise SystemExit("User requested exit")
            elif response in {'1', '2', '3', '4'}:
                return {
                    '1': 'content',
                    '2': 'date',
                    '3': 'type',
                    '4': 'checklist'
                }[response]
            
            print("Invalid selection. Please enter 1, 2, 3, or 4.")

    def _process_files(self, file_paths: List[str], output_path: str) -> bool:
        """Process files based on selected organization mode"""
        mode = self._get_organization_mode()
        
        try:
            operations = self._generate_operations(mode, file_paths, output_path)
            if not operations:
                return False

            # Show preview and get confirmation
            self._preview_operations(operations, output_path)
            if not self._confirm_operations():
                return False

            # Execute operations
            self._execute_operations(operations, output_path)
            return True

        except Exception as e:
            self.system.error_handler.handle_error(
                e, 
                {
                    'operation': 'process_files',
                    'mode': mode,
                    'output_path': output_path
                }
            )
            return False

    def _generate_content_operations(self, file_paths: List[str], output_path: str) -> List[Dict[str, Any]]:
        """Generate operations for content-based organization"""
        # Separate files by type
        image_files, text_files, legal_files = separate_files_by_type(file_paths)

        # Process text files
        text_tuples = []
        for fp in text_files:
            content = read_file_data(fp)
            if content is not None:
                text_tuples.append((fp, content))
            else:
                self.log_message(f"Unsupported or unreadable text file format: {fp}")

        # Process files by type
        with filter_specific_output():
            data_images = process_image_files(
                image_files, 
                self.system.config.model_config.image_model_path,
                self.system.config.model_config.text_model_path,
                silent=self.silent_mode,
                log_file=self.log_file
            )
            data_texts = process_text_files(
                text_tuples,
                self.system.config.model_config.text_model_path,
                silent=self.silent_mode,
                log_file=self.log_file
            )

        # Process legal files
        data_legal = []
        if legal_files:
            legal_processor = LegalDocumentProcessor()
            for legal_file in legal_files:
                content = read_file_data(legal_file)
                if content:
                    metadata = legal_processor.extract_metadata(content)
                    folder_structure = legal_processor.suggest_folder_structure()
                    filename = legal_processor.suggest_filename()
                    if filename:
                        filename += os.path.splitext(legal_file)[1]
                    data_legal.append({
                        'file_path': legal_file,
                        'foldername': folder_structure,
                        'filename': filename,
                        'description': legal_processor.generate_summary()
                    })

        # Combine all data and compute operations
        all_data = data_images + data_texts + data_legal
        renamed_files = set()
        processed_files = set()

        return compute_operations(
            all_data,
            output_path,
            renamed_files,
            processed_files
        )

    def _generate_operations(self, mode: str, file_paths: List[str], 
                           output_path: str) -> List[Dict[str, Any]]:
        """Generate file operations based on selected mode"""
        if mode == 'content':
            return self._generate_content_operations(file_paths, output_path)
        elif mode == 'date':
            return process_files_by_date(file_paths, output_path)
        elif mode == 'type':
            return process_files_by_type(file_paths, output_path)
        elif mode == 'checklist':
            return process_files_by_type(file_paths, output_path)
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def _simulate_directory_tree(self, operations: List[Dict[str, Any]], base_path: str) -> Dict[str, Any]:
        """Simulate the directory tree based on the proposed operations"""
        tree = {}
        for op in operations:
            rel_path = os.path.relpath(op['destination'], base_path)
            parts = rel_path.split(os.sep)
            current_level = tree
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        return tree

    def _print_tree(self, tree: Dict[str, Any], prefix: str = ''):
        """Print the simulated directory tree"""
        pointers = ['├── '] * (len(tree) - 1) + ['└── '] if tree else []
        for pointer, key in zip(pointers, tree):
            print(prefix + pointer + key)
            if tree[key]:  # If there are subdirectories or files
                extension = '│   ' if pointer == '├── ' else '    '
                self._print_tree(tree[key], prefix + extension)

    def _preview_operations(self, operations: List[Dict[str, Any]], output_path: str):
        """Preview the proposed file operations"""
        self.log_message("\nProposed directory structure:")
        if not self.silent_mode:
            print(os.path.abspath(output_path))
            tree = self._simulate_directory_tree(operations, output_path)
            self._print_tree(tree)

    def _confirm_operations(self) -> bool:
        """Get user confirmation for operations"""
        while True:
            response = input("\nProceed with these changes? (yes/no): ").strip().lower()
            if response in {'yes', 'y'}:
                return True
            elif response in {'no', 'n'}:
                return False
            print("Please enter 'yes' or 'no'")

    def _execute_operations(self, operations: List[Dict[str, Any]], output_path: str):
        """Execute the file operations"""
        os.makedirs(output_path, exist_ok=True)
        self.log_message("Performing file operations...")
        
        execute_operations(
            operations,
            dry_run=False,
            silent=self.silent_mode,
            log_file=self.log_file
        )
        
        self.log_message("Files have been organized successfully")

def main():
    """Main entry point"""
    organizer = FileOrganizer()
    
    # Configure silent mode
    print("-" * 50)
    print("**NOTE: Silent mode logs outputs to a file instead of displaying them.")
    silent_mode = input("Enable silent mode? (yes/no): ").strip().lower() in {'yes', 'y'}
    organizer.set_silent_mode(silent_mode)

    # Main organization loop
    while True:
        try:
            # Get input path
            input_path = input("\nEnter directory path to organize: ").strip()
            if input_path.lower() == '/exit':
                break

            # Organize directory
            if organizer.organize_directory(input_path):
                print("\nOrganization completed successfully!")
            else:
                print("\nOrganization failed or was cancelled.")

            # Check for another directory
            if input("Organize another directory? (yes/no): ").strip().lower() not in {'yes', 'y'}:
                break

        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            if input("\nContinue with another directory? (yes/no): ").strip().lower() not in {'yes', 'y'}:
                break

    print("\nExiting program.")

if __name__ == '__main__':
    main()
