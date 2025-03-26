import os
import json
from typing import Dict, List, Optional

class PathManager:
    """Manages and organizes all path configurations in the project."""
    
    def __init__(self, config_file: str = 'path_config.json'):
        self.config_file = config_file
        self.paths: Dict[str, str] = {}
        self.load_paths()
    
    def load_paths(self) -> None:
        """Load paths from config file if it exists."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.paths = json.load(f)
    
    def save_paths(self) -> None:
        """Save current paths to config file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.paths, f, indent=2)
    
    def scan_project(self, root_dir: str = '.') -> List[Dict[str, str]]:
        """Scan project for path-related configurations."""
        path_references = []
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(('.py', '.json', '.yml', '.yaml')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Look for path-like strings and assignments
                            if any(keyword in content.lower() for keyword in 
                                ['path', 'dir', 'directory', 'folder', 'location']):
                                path_references.append({
                                    'file': file_path,
                                    'type': os.path.splitext(file)[1],
                                    'relative_path': os.path.relpath(file_path, root_dir)
                                })
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        return path_references
    
    def update_paths(self, root_dir: str = '.') -> Dict[str, List[str]]:
        """Update path configurations across the project."""
        # Scan for path references
        references = self.scan_project(root_dir)
        
        # Group paths by type
        grouped_paths = {
            'python_files': [],
            'config_files': [],
            'other_files': []
        }
        
        for ref in references:
            if ref['type'] == '.py':
                grouped_paths['python_files'].append(ref['relative_path'])
            elif ref['type'] in ['.json', '.yml', '.yaml']:
                grouped_paths['config_files'].append(ref['relative_path'])
            else:
                grouped_paths['other_files'].append(ref['relative_path'])
        
        # Update paths dictionary
        self.paths.update({
            'project_root': os.path.abspath(root_dir),
            'input_paths': {
                'sample_data': 'sample_data',
                'legal_documents': os.path.join('sample_data', 'legal_documents')
            },
            'output_paths': {
                'organized_by_type': 'organized_by_type',
                'organized_by_date': 'organized_by_date',
                'organized_by_size': 'organized_by_size',
                'organized_by_type_and_date': 'organized_by_type_and_date'
            },
            'config_paths': {
                'main_config': 'config.json',
                'ai_config': 'config_ai.json',
                'path_config': self.config_file
            },
            'path_references': grouped_paths
        })
        
        # Save updated paths
        self.save_paths()
        return grouped_paths
    
    def get_path(self, path_key: str, category: Optional[str] = None) -> str:
        """Get a path by its key and optional category."""
        if category:
            return self.paths.get(category, {}).get(path_key, '')
        return self.paths.get(path_key, '')
    
    def add_path(self, path_key: str, path_value: str, category: Optional[str] = None) -> None:
        """Add or update a path."""
        if category:
            if category not in self.paths:
                self.paths[category] = {}
            self.paths[category][path_key] = path_value
        else:
            self.paths[path_key] = path_value
        self.save_paths()
    
    def generate_report(self) -> str:
        """Generate a report of all paths in the project."""
        report = ["=== Path Configuration Report ===\n"]
        
        # Project root
        report.append(f"Project Root: {self.paths.get('project_root', 'Not set')}\n")
        
        # Input paths
        report.append("\nInput Paths:")
        for key, path in self.paths.get('input_paths', {}).items():
            report.append(f"  {key}: {path}")
        
        # Output paths
        report.append("\nOutput Paths:")
        for key, path in self.paths.get('output_paths', {}).items():
            report.append(f"  {key}: {path}")
        
        # Config paths
        report.append("\nConfig Paths:")
        for key, path in self.paths.get('config_paths', {}).items():
            report.append(f"  {key}: {path}")
        
        # Path references
        report.append("\nPath References:")
        for category, paths in self.paths.get('path_references', {}).items():
            report.append(f"\n  {category}:")
            for path in paths:
                report.append(f"    - {path}")
        
        return '\n'.join(report)

def main():
    """Main function to demonstrate path manager usage."""
    manager = PathManager()
    print("Scanning project for path references...")
    manager.update_paths()
    print("\nGenerated path report:")
    print(manager.generate_report())

if __name__ == "__main__":
    main()
