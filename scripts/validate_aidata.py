# AIDATA VALIDATION SCRIPT
# This script validates .aidata files against the base.aidata template

import argparse
import re
from pathlib import Path

class AIDataValidator:
    def __init__(self):
        # Define the mandatory sections as they should appear in a .aidata file
        self.mandatory_sections = [
            "FILE METADATA",
            "DOMAIN CONTEXT", 
            "KNOWLEDGE REPRESENTATION",
            "VALIDATION FRAMEWORK",
            "APPLICATION CONTEXT",
            "EVOLUTION TRACKING",
            "AUTOMATED LEARNINGS"
        ]
        
        # Define optional sections
        self.optional_sections = [
            "CROSS-DOMAIN LINKING",
            "AI-SPECIFIC FEATURES", 
            "SESSION MANAGEMENT",
            "CHAT SESSION INTEGRATION",
            "EXECUTION STATE REPRESENTATION"
        ]
    
    def validate_sections(self, file_path):
        """Validate that a .aidata file contains all mandatory sections."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return False, []
        
        missing_sections = []
        present_sections = []
        
        # Check for mandatory sections
        for section in self.mandatory_sections:
            # Look for section header (## SECTION NAME)
            if f"## {section}" not in content:
                missing_sections.append(section)
            else:
                present_sections.append(section)
        
        # Report results
        if not missing_sections:
            print(f"[PASS] All mandatory sections present in {file_path}")
            return True, present_sections
        else:
            print(f"[FAIL] Missing mandatory sections in {file_path}:")
            for section in missing_sections:
                print(f"  - {section}")
            return False, present_sections
    
    def validate_file_header(self, file_path):
        """Validate that the file starts with the correct header."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return False
        
        if first_line.startswith("# AI LEARNING FILE:"):
            print(f"[PASS] Correct file header in {file_path}")
            return True
        else:
            print(f"[FAIL] Incorrect file header in {file_path}")
            print(f"  Expected to start with '# AI LEARNING FILE:', got '{first_line[:50]}...'")
            return False
    
    def validate_created_section(self, file_path):
        """Validate that the file has a CREATED section."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return False
        
        if "## CREATED" in content:
            print(f"[PASS] CREATED section present in {file_path}")
            return True
        else:
            print(f"[FAIL] Missing CREATED section in {file_path}")
            return False
    
    def validate_file_structure(self, file_path):
        """Validate the overall file structure."""
        print(f"\nValidating structure of {file_path}:")
        print("-" * 50)
        
        # Check file header
        header_valid = self.validate_file_header(file_path)
        
        # Check CREATED section
        created_valid = self.validate_created_section(file_path)
        
        # Check mandatory sections
        sections_valid, present_sections = self.validate_sections(file_path)
        
        # Overall validation
        overall_valid = header_valid and created_valid and sections_valid
        
        if overall_valid:
            print(f"\n[PASS] {file_path} passed all structural validation checks")
        else:
            print(f"\n[FAIL] {file_path} failed one or more validation checks")
        
        return overall_valid
    
    def list_sections(self, file_path):
        """List all sections found in the file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
        
        # Find all section headers (## ...)
        sections = re.findall(r"^## (.+)$", content, re.MULTILINE)
        return sections
    
    def compare_with_template(self, file_path, template_path="C:\\ai_learnings\\base.aidata"):
        """Compare sections in a file with the base template."""
        # Get sections from the file being validated
        file_sections = self.list_sections(file_path)
        
        # Get sections from the template
        template_sections = self.list_sections(template_path)
        
        # Identify differences
        extra_sections = [s for s in file_sections if s not in template_sections]
        missing_sections = [s for s in template_sections if s not in file_sections and s in self.mandatory_sections]
        
        print(f"\nComparison with base template ({template_path}):")
        print("-" * 50)
        
        if extra_sections:
            print("Extra sections not in template:")
            for section in extra_sections:
                print(f"  + {section}")
        
        if missing_sections:
            print("Missing mandatory sections:")
            for section in missing_sections:
                print(f"  - {section}")
        elif not extra_sections:
            print("File structure matches template exactly")
        
        return len(extra_sections) == 0 and len(missing_sections) == 0

def main():
    parser = argparse.ArgumentParser(description="Validate .aidata files against the base template")
    parser.add_argument("file", help="Path to the .aidata file to validate")
    parser.add_argument("--template", "-t", help="Path to the base template file", 
                        default="C:\\ai_learnings\\base.aidata")
    parser.add_argument("--list", "-l", action="store_true", 
                        help="List all sections found in the file")
    parser.add_argument("--compare", "-c", action="store_true",
                        help="Compare file structure with base template")
    
    args = parser.parse_args()
    
    validator = AIDataValidator()
    
    # Validate file structure
    is_valid = validator.validate_file_structure(args.file)
    
    # List sections if requested
    if args.list:
        sections = validator.list_sections(args.file)
        print(f"\nSections found in {args.file}:")
        print("-" * 30)
        for i, section in enumerate(sections, 1):
            print(f"{i:2d}. {section}")
    
    # Compare with template if requested
    if args.compare:
        validator.compare_with_template(args.file, args.template)
    
    # Return appropriate exit code
    return 0 if is_valid else 1

if __name__ == "__main__":
    exit(main())