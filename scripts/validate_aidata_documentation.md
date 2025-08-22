# AIDATA VALIDATION SCRIPT DOCUMENTATION

This document provides detailed information about the `validate_aidata.py` script, which is designed to validate `.aidata` files against the base template to ensure they adhere to the required structure.

## Overview

The `validate_aidata.py` script implements a validation system for `.aidata` files. It provides functionalities for:
- Validating that files contain all mandatory sections
- Checking file header format
- Verifying the presence of required structural elements
- Comparing file structure with the base template
- Listing all sections found in a file

This tool is part of the broader AI learning ecosystem that works with `.aidata` files and enhances their quality assurance as described in the `base.aidata` Quality Assurance Framework.

## Installation and Setup

The script is located in the `C:\ai_learnings` directory as `validate_aidata.py`. To use it, you need to have Python installed on your system.

## Usage

The script is designed to be run from the command line:

```bash
python C:\ai_learnings\validate_aidata.py [file] [options]
```

### Basic Validation
To validate a `.aidata` file:
```bash
python C:\ai_learnings\validate_aidata.py my_file.aidata
```

### List Sections
To list all sections found in a file:
```bash
python C:\ai_learnings\validate_aidata.py my_file.aidata --list
```

### Compare with Template
To compare a file's structure with the base template:
```bash
python C:\ai_learnings\validate_aidata.py my_file.aidata --compare
```

### Combined Options
You can combine options:
```bash
python C:\ai_learnings\validate_aidata.py my_file.aidata --list --compare
```

## AIDataValidator Class

The core functionality is implemented in the `AIDataValidator` class.

### Constructor
```python
validator = AIDataValidator()
```

### Key Methods
- `validate_sections(file_path)`: Validates that a file contains all mandatory sections
- `validate_file_header(file_path)`: Validates the file header format
- `validate_created_section(file_path)`: Validates the presence of a CREATED section
- `validate_file_structure(file_path)`: Performs comprehensive file structure validation
- `list_sections(file_path)`: Lists all sections found in a file
- `compare_with_template(file_path, template_path)`: Compares file structure with a template

## Validation Features

### Mandatory Section Validation
The script checks that all mandatory sections are present:
1. FILE METADATA
2. DOMAIN CONTEXT
3. KNOWLEDGE REPRESENTATION
4. VALIDATION FRAMEWORK
5. APPLICATION CONTEXT
6. EVOLUTION TRACKING
7. AUTOMATED LEARNINGS

### File Header Validation
The script verifies that the file starts with the correct header:
```
# AI LEARNING FILE: [filename]
```

### CREATED Section Validation
The script checks for the presence of a CREATED section, which is required for all `.aidata` files.

### Template Comparison
The script can compare a file's structure with the base template to identify:
- Extra sections not in the template
- Missing mandatory sections

## Integration with .aidata Ecosystem

This tool is part of the broader `.aidata` ecosystem and works alongside:
- `aidata_cli.py`: For command-line processing of files
- `advanced_aidata_manager.py`: For advanced file management
- The quality assurance framework described in `base.aidata`

The validation script directly implements the "Validation Layers" described in the Quality Assurance Framework section of `base.aidata`:
1. **Syntax Validation**: Ensure proper file structure
2. **Semantic Validation**: Check meaning and consistency (partially)
3. **Cross-Reference Validation**: Verify links and connections (future enhancement)
4. **Completeness Validation**: Ensure required sections are present
5. **Integrity Validation**: Confirm file hasn't been corrupted (partially)

## Error Handling

The tool includes error handling for:
- File not found errors
- Permission errors
- General exceptions during file processing

If an error occurs, the tool will display an informative error message.

## Cross-Platform Compatibility

The tool is designed to work on Windows, Linux, and macOS. When using it on different platforms, ensure that:
- Python 3 is installed
- The file paths use appropriate separators for the platform

## Relationship to Base Specification

This tool implements the validation capabilities described in the `base.aidata` file:
1. **Quality Assurance Framework**: The script provides automated validation of file structure
2. **Completeness Validation**: It ensures all mandatory sections are present
3. **Syntax Validation**: It checks for proper file header format

For the most up-to-date information about `.aidata` file specifications, refer to the `base.aidata` file in the same directory.