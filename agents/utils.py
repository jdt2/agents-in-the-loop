"""
Utility functions for agents
"""

import os
import json
from typing import Dict, List, Any, Optional


def ensure_directory(path: str) -> None:
    """Ensure a directory exists, creating it if necessary"""
    os.makedirs(path, exist_ok=True)


def read_file_safely(file_path: str) -> Optional[str]:
    """Safely read a file, returning None if file doesn't exist"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError, UnicodeDecodeError):
        return None


def write_file_safely(file_path: str, content: str) -> bool:
    """Safely write content to a file, creating directories if needed"""
    try:
        # Ensure parent directory exists
        parent_dir = os.path.dirname(file_path)
        if parent_dir:
            ensure_directory(parent_dir)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except (IOError, UnicodeEncodeError):
        return False


def load_json_safely(file_path: str) -> Optional[Dict[str, Any]]:
    """Safely load JSON from a file"""
    content = read_file_safely(file_path)
    if content is None:
        return None
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def save_json_safely(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """Safely save data as JSON to a file"""
    try:
        json_content = json.dumps(data, indent=indent, ensure_ascii=False)
        return write_file_safely(file_path, json_content)
    except (TypeError, ValueError):
        return False


def get_file_tree(directory: str, ignore_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get a tree structure of files in a directory"""
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', 'node_modules', '.DS_Store']
    
    def should_ignore(name: str) -> bool:
        return any(pattern in name for pattern in ignore_patterns)
    
    def build_tree(path: str) -> Dict[str, Any]:
        tree = {'type': 'directory', 'children': {}}
        
        try:
            for item in os.listdir(path):
                if should_ignore(item):
                    continue
                
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    tree['children'][item] = build_tree(item_path)
                else:
                    tree['children'][item] = {'type': 'file'}
        except PermissionError:
            tree['error'] = 'Permission denied'
        
        return tree
    
    if not os.path.exists(directory):
        return {'type': 'directory', 'error': 'Directory does not exist'}
    
    return build_tree(directory)


def format_file_list(files: List[str], max_display: int = 20) -> str:
    """Format a list of files for display"""
    if not files:
        return "No files found"
    
    if len(files) <= max_display:
        return "\n".join(f"  - {file}" for file in sorted(files))
    else:
        displayed = sorted(files)[:max_display]
        remaining = len(files) - max_display
        return "\n".join(f"  - {file}" for file in displayed) + f"\n  ... and {remaining} more files"


def get_project_info(directory: str) -> Dict[str, Any]:
    """Get basic information about a project directory"""
    info = {
        'directory': directory,
        'exists': os.path.exists(directory),
        'is_directory': os.path.isdir(directory) if os.path.exists(directory) else False,
        'file_count': 0,
        'has_package_json': False,
        'has_readme': False,
        'has_git': False
    }
    
    if not info['is_directory']:
        return info
    
    try:
        files = []
        for root, dirs, filenames in os.walk(directory):
            files.extend(filenames)
        
        info['file_count'] = len(files)
        info['has_package_json'] = 'package.json' in files
        info['has_readme'] = any(f.lower().startswith('readme') for f in files)
        info['has_git'] = os.path.exists(os.path.join(directory, '.git'))
        
    except PermissionError:
        info['error'] = 'Permission denied'
    
    return info