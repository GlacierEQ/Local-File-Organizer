import os
import hashlib
import json
import datetime
from typing import Dict, List, Optional
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import docx
import pandas as pd
from pptx import Presentation
import magic
import stat
import pwd
import grp

class FileScanner:
    """Forensic-level file system scanner with detailed metadata collection."""
    
    def __init__(self):
        self.scan_results = []
        self.exclude_dirs = {
            'Windows', 'Program Files', 'Program Files (x86)', 
            'ProgramData', '$Recycle.Bin', 'System Volume Information',
            'Recovery', 'Config.Msi'
        }
        self.exclude_files = {
            'pagefile.sys', 'hiberfil.sys', 'swapfile.sys'
        }
        self.stop_scan = False  # Added to support cancelling a scan
    
    def get_file_metadata(self, file_path: str) -> Dict:h protection checks."""
        """Collect comprehensive metadata for a file."""
        try:les
            stat_info = os.stat(file_path)
            file_type = magic.from_file(file_path, mime=True)    return {
            h': file_path,
            metadata = {ss denied - system/protected file'
                'path': file_path,
                'size': stat_info.st_size,
                'created': datetime.datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'modified': datetime.datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'accessed': datetime.datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                'permissions': stat.filemode(stat_info.st_mode),
                'owner': pwd.getpwuid(stat_info.st_uid).pw_name,ssions'
                'group': grp.getgrgid(stat_info.st_gid).gr_name,
                'file_type': file_type,
                'md5_hash': self.calculate_hash(file_path, 'md5'),
                'sha256_hash': self.calculate_hash(file_path, 'sha256'),True)
                'is_symlink': os.path.islink(file_path),
                'inode': stat_info.st_ino,
                'device': stat_info.st_dev,
                'hard_links': stat_info.st_nlink,
                'blocks': stat_info.st_blocks,imestamp(stat_info.st_ctime).isoformat(),
                'block_size': stat_info.st_blksize   'modified': datetime.datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            }    'accessed': datetime.datetime.fromtimestamp(stat_info.st_atime).isoformat(),
            e(stat_info.st_mode),
            # Add content-specific metadatao.st_uid).pw_name,
            if file_type.startswith('image/'):
                metadata.update(self.get_image_metadata(file_path))
            elif file_type.startswith('text/'):
                metadata.update(self.get_text_metadata(file_path))    'sha256_hash': self.calculate_hash(file_path, 'sha256'),
            ': os.path.islink(file_path),
            return metadatainfo.st_ino,
        except Exception as e:
            print(f"Error collecting metadata for {file_path}: {e}")_links': stat_info.st_nlink,
            return {}            'blocks': stat_info.st_blocks,
    
    def calculate_hash(self, file_path: str, algorithm: str) -> str:
        """Calculate file hash using specified algorithm."""
        hash_func = getattr(hashlib, algorithm)()# Add content-specific metadata
        try:):
            with open(file_path, 'rb') as f:path))
                for chunk in iter(lambda: f.read(4096), b""):/'):
                    hash_func.update(chunk)_text_metadata(file_path))
            return hash_func.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")ion as e:
            return ''        print(f"Error collecting metadata for {file_path}: {e}")
    
    def scan_directory(self, path: str, exhaustive: bool = False) -> List[Dict]:
        """Recursively scan a directory and collect metadata.calculate_hash(self, file_path: str, algorithm: str) -> str:
        
        If exhaustive is True, scan all directories and files without exclusions.h_func = getattr(hashlib, algorithm)()
        """
        results = []with open(file_path, 'rb') as f:
        try:96), b""):
            for root, dirs, files in os.walk(path):te(chunk)
                if self.stop_scan:
                    break
                if not exhaustive:t(f"Error calculating hash for {file_path}: {e}")
                    # Remove excluded directories and hidden directories
                    dirs[:] = [d for d in dirs if d not in self.exclude_dirs and not d.startswith('.')]
                tr, exhaustive: bool = False) -> List[Dict]:
                for file in files:checks.
                    if self.stop_scan:
                        breakt exclusions,
                    if not exhaustive and file in self.exclude_files:file protections.
                        continue
                    file_path = os.path.join(root, file)
                    try:
                        metadata = self.get_file_metadata(file_path)ermission to scan this directory
                        if metadata:
                            results.append(metadata) [{
                    except Exception as e:                'path': path,
                        print(f"Error scanning file {file_path}: {e}")'
                if self.stop_scan:
                    break
        except Exception as e:h):
            print(f"Error scanning directory {path}: {e}")tive:
        return resultsRemove excluded directories and hidden directories
    r d in dirs if d not in self.exclude_dirs and not d.startswith('.')]
    def generate_report(self, results: List[Dict], format: str = 'json') -> str:
        """Generate scan report in specified format."""
        if format == 'json':stive and file in self.exclude_files:
            return json.dumps(results, indent=2)
        elif format == 'csv':ath.join(root, file)
            import csv       try:
            from io import StringIOdata(file_path)
            output = StringIO()                        if metadata:
            writer = csv.DictWriter(output, fieldnames=results[0].keys())tadata)
            writer.writeheader()                    except Exception as e:







# Existing file utilities remain unchanged...            return '\n'\n'.join(str(r) for r in results)        else:            return output.getvalue()            writer.writerows(results)                        print(f"Error scanning file {file_path}: {e}")
        except Exception as e:
            print(f"Error scanning directory {path}: {e}")
        return results
    
    def generate_report(self, results: List[Dict], format: str = 'json') -> str:
        """Generate scan report in specified format."""
        if format == 'json':
            return json.dumps(results, indent=2)
        elif format == 'csv':
            import csv
            from io import StringIO
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
            return output.getvalue()
        else:
            return '\n'.join(str(r) for r in results)

# Existing file utilities remain unchanged...
