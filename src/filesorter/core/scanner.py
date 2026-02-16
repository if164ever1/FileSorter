
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class DirectoryScanner:
    """Scans a directory and creates a map of its structure."""

    def __init__(self, base_path: str):
        """Initializes the DirectoryScanner.

        Args:
            base_path (str): The base path of the directory to scan.
        """
        self.base_path = base_path
        self.directory_map = {}
        self.file_list = []

    def scan(self):
        """Scans the directory and builds the directory map."""
        for root, dirs, _ in os.walk(self.base_path):
            for dir_name in dirs:
                full_path = os.path.join(root, dir_name)
                # Use the relative path from the base as the key
                relative_path = os.path.relpath(full_path, self.base_path)
                self.directory_map[relative_path] = {
                    "path": full_path,
                    "depth": relative_path.count(os.sep)
                }

    def recursive_scan(self, path: str = None, depth: int = 0) -> Dict:
        """Recursively scans a directory and returns structure with files and subdirectories.

        Args:
            path (str): The path to scan. If None, uses self.base_path.
            depth (int): The current recursion depth.

        Returns:
            Dict: A dictionary containing the directory structure with files and subdirectories.
        """
        if path is None:
            path = self.base_path

        if not os.path.exists(path):
            return {"error": f"Path does not exist: {path}"}

        structure = {
            "name": os.path.basename(path) or path,
            "path": path,
            "type": "directory",
            "depth": depth,
            "files": [],
            "subdirectories": []
        }

        try:
            entries = os.listdir(path)
        except PermissionError:
            structure["error"] = "Permission denied"
            return structure

        for entry in entries:
            full_entry_path = os.path.join(path, entry)

            try:
                if os.path.isfile(full_entry_path):
                    file_info = {
                        "name": entry,
                        "path": full_entry_path,
                        "type": "file",
                        "size": os.path.getsize(full_entry_path)
                    }
                    structure["files"].append(file_info)
                    self.file_list.append(full_entry_path)

                elif os.path.isdir(full_entry_path):
                    subdir_structure = self.recursive_scan(full_entry_path, depth + 1)
                    structure["subdirectories"].append(subdir_structure)

            except (PermissionError, OSError) as e:
                structure["errors"] = structure.get("errors", [])
                structure["errors"].append(f"Error accessing {entry}: {str(e)}")

        return structure

    def get_map(self) -> dict:
        """Returns the generated directory map.

        Returns:
            dict: The directory map.
        """
        return self.directory_map

    def get_files(self) -> List[str]:
        """Returns the list of files found during recursive scan.

        Returns:
            List[str]: A list of file paths.
        """
        return self.file_list
    def _extract_keywords(self, path: str) -> List[str]:
        """Extracts keywords from a folder path.

        Keywords are extracted from folder names in the path by:
        - Splitting by spaces, hyphens, and underscores
        - Converting to lowercase
        - Removing empty strings

        Args:
            path (str): The folder path.

        Returns:
            List[str]: A list of keywords.
        """
        # Get all folder names in the path
        path_parts = path.replace("\\", "/").split("/")
        
        keywords = []
        for part in path_parts:
            # Skip empty parts and single letters
            if part and len(part) > 1:
                # Split by spaces, hyphens, and underscores
                words = re.split(r'[\s\-_]+', part)
                # Convert to lowercase and filter empty strings
                words = [word.lower() for word in words if word]
                keywords.extend(words)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)
        
        return unique_keywords

    def get_leaf_folders(self, path: str = None) -> List[str]:
        """Gets all leaf folders (folders with no subdirectories) in the directory tree.

        Args:
            path (str): The path to scan. If None, uses self.base_path.

        Returns:
            List[str]: A list of leaf folder paths.
        """
        if path is None:
            path = self.base_path

        leaf_folders = []

        try:
            for root, dirs, _ in os.walk(path):
                # If no subdirectories, this is a leaf folder
                if not dirs:
                    leaf_folders.append(root)
        except (PermissionError, OSError) as e:
            print(f"Error accessing {path}: {str(e)}")

        return leaf_folders

    def build_map_json(self, path: str = None) -> List[Dict]:
        """Builds a map structure with leaf folders and their keywords for JSON export.

        Args:
            path (str): The path to scan. If None, uses self.base_path.

        Returns:
            List[Dict]: A list of dictionaries with 'path' and 'keywords' entries.
        """
        if path is None:
            path = self.base_path

        leaf_folders = self.get_leaf_folders(path)
        map_data = []

        for folder in leaf_folders:
            # Convert backslashes to forward slashes for consistency
            normalized_path = folder.replace("\\", "/")
            keywords = self._extract_keywords(folder)

            map_data.append({
                "path": normalized_path,
                "keywords": keywords
            })

        return map_data

    def save_map_json(self, output_path: str, path: str = None) -> bool:
        """Saves the directory map to a JSON file.

        Args:
            output_path (str): The file path where the JSON should be saved (e.g., 'config/map.json').
            path (str): The path to scan. If None, uses self.base_path.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure the output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Build the map data
            map_data = self.build_map_json(path)

            # Save to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(map_data, f, indent=2)

            print(f"Map saved successfully to {output_path}")
            print(f"Total leaf folders: {len(map_data)}")
            return True

        except (IOError, OSError) as e:
            print(f"Error saving map to {output_path}: {str(e)}")
            return False