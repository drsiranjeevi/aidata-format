# AIDATA CLI TOOL DOCUMENTATION

This document provides detailed information about the `aidata_cli.py` tool, which is designed to process and manage `.aidata` files based on the specifications in `base.aidata`.

## Overview

The `aidata_cli.py` tool is a command-line interface for validating, updating, and processing `.aidata` files. It provides essential functions for maintaining the integrity and quality of these files. The tool is built around the `AIDataProcessor` class, which encapsulates all the functionality for working with `.aidata` files.

## Installation and Setup

The tool is located in the `C:\ai_learnings` directory as `aidata_cli.py`. To use it, you need to have Python installed on your system.

## Usage

The general syntax for using the tool is:
```bash
python C:\ai_learnings\aidata_cli.py [command] [file]
```

### Available Commands

1. **validate**: Checks if a .aidata file has all mandatory sections and proper syntax.
2. **generate-hash**: Automatically calculates and updates the integrity hash.
3. **deduplicate**: Removes duplicate entries from the AUTOMATED LEARNINGS section.
4. **to-json**: Converts the .aidata file to JSON format for database integration.

### Command Details

#### validate
Checks that the .aidata file conforms to the required structure defined in base.aidata.

Example:
```bash
python C:\ai_learnings\aidata_cli.py validate base.aidata
```

This command will verify:
- Presence of all mandatory sections as defined in base.aidata:
  - FILE METADATA
  - DOMAIN CONTEXT
  - KNOWLEDGE REPRESENTATION
  - VALIDATION FRAMEWORK
  - APPLICATION CONTEXT
  - EVOLUTION TRACKING
  - AUTOMATED LEARNINGS
- Proper file header (must start with '# AI LEARNING FILE:')
- Correct format of the CREATED section

#### generate-hash
Calculates and updates the SHA256 integrity hash in the FILE METADATA section.

Example:
```bash
python C:\ai_learnings\aidata_cli.py generate-hash base.aidata
```

This command will:
- Calculate the SHA256 hash of the file content (excluding the hash line itself to avoid circular dependency)
- Update the "Integrity Hash" field in the FILE METADATA section
- Report the new hash value

If no hash line exists, it will be added to the FILE METADATA section.

#### deduplicate
Removes duplicate entries from the AUTOMATED LEARNINGS section to maintain file quality.

Example:
```bash
python C:\ai_learnings\aidata_cli.py deduplicate base.aidata
```

This command will:
- Identify learning entries with identical content using SHA256 hashing
- Remove duplicates, keeping only the first occurrence
- Report the number of duplicates removed

The deduplication process uses the same algorithm as the `deduplicate_automated_learnings.py` script.

#### to-json
Converts the .aidata file to JSON format for easier processing by other tools or database integration.

Example:
```bash
python C:\ai_learnings\aidata_cli.py to-json base.aidata
```

This command will:
- Parse the .aidata file structure
- Create a JSON representation of the content
- Save the JSON to a file with the same name but .json extension

The JSON file will have the following structure:
```json
{
  "file_name": "base.aidata",
  "file_title": "base.aidata",
  "sections": {
    "FILE METADATA": "...",
    "DOMAIN CONTEXT": "...",
    // ... other sections
  }
}
```

## AIDataProcessor Class

The core functionality of the CLI tool is implemented in the `AIDataProcessor` class, which provides methods for each command:

### Constructor
```python
processor = AIDataProcessor(file_path)
```

### Methods
- `validate_syntax()`: Validates the syntax of the .aidata file
- `generate_hash()`: Generates and updates the integrity hash
- `deduplicate_learnings()`: Removes duplicate entries from the AUTOMATED LEARNINGS section
- `to_json()`: Converts the .aidata file to JSON format

## Error Handling

The tool provides informative error messages for common issues:
- File not found
- Permission denied
- Invalid file format
- Processing errors

If an error occurs, the tool will exit with a non-zero status code and display an error message.

## Cross-Platform Compatibility

The tool is designed to work on Windows, Linux, and macOS. When using it on different platforms, ensure that:
- Python 3 is installed
- The file paths use appropriate separators for the platform
- The file encoding is UTF-8

## Integration with base.aidata Specifications

This tool directly implements several features described in the `base.aidata` file:
- Syntax validation corresponds to the mandatory sections defined in base.aidata
- Hash generation automates the process described in the "Automating Integrity Hash Generation" section
- Deduplication addresses the "Deduplicating Automated Learnings" section
- The JSON conversion supports integration with other systems as mentioned in various sections

For the most up-to-date information about .aidata file specifications, refer to the `base.aidata` file in the same directory.

## Relationship to Other Scripts

This tool incorporates functionality from other scripts in the ecosystem:
- The deduplication functionality is based on `deduplicate_automated_learnings.py`
- It provides a unified interface for various .aidata processing tasks

When you run:
```bash
python C:\ai_learnings\deduplicate_automated_learnings.py path/to/your/file.aidata
```

It's equivalent to running:
```bash
python C:\ai_learnings\aidata_cli.py deduplicate path/to/your/file.aidata
```

However, the CLI tool offers additional functionality beyond just deduplication.