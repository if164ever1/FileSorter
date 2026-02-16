#!/usr/bin/env python3
"""
Script to scan directory structure and generate map.json
Reads configuration from .env file for security
"""

import os
import sys
from dotenv import load_dotenv
from src.filesorter.core.scanner import DirectoryScanner

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Read configuration from environment variables
    source_dir = os.getenv("SOURCE_DIR")
    output_file = os.path.join("config", "map.json")
    
    if not source_dir:
        print("Error: SOURCE_DIR not found in .env file")
        print("Please copy .env.example to .env and set your SOURCE_DIR path")
        return False

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory does not exist: {source_dir}")
        return False

    print(f"Scanning directory: {source_dir}")
    print("This may take a while depending on the size of the directory tree...")
    print()

    # Create scanner and scan the directory
    scanner = DirectoryScanner(source_dir)

    # Scan and generate map
    print("Building map structure...")
    map_data = scanner.build_map_json(source_dir)
    print(f"Found {len(map_data)} leaf folders")
    print()

    # Display first few entries as preview
    print("Preview of first 5 entries:")
    for i, entry in enumerate(map_data[:5]):
        print(f"  {i+1}. {entry['path']}")
        print(f"     Keywords: {', '.join(entry['keywords'])}")
    print()

    # Save to JSON file
    print(f"Saving map to {output_file}...")
    success = scanner.save_map_json(output_file, source_dir)

    if success:
        print("✓ Map successfully generated and saved!")
        return True
    else:
        print("✗ Failed to save map")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
