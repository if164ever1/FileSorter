
import os

class DirectoryScanner:
    """Scans a directory and creates a map of its structure."""

    def __init__(self, base_path: str):
        """Initializes the DirectoryScanner.

        Args:
            base_path (str): The base path of the directory to scan.
        """
        self.base_path = base_path
        self.directory_map = {}

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

    def get_map(self) -> dict:
        """Returns the generated directory map.

        Returns:
            dict: The directory map.
        """
        return self.directory_map
