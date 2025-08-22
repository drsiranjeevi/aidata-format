import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

class AIDataProcessor:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = self._read_file()
    
    def _read_file(self):
        """Read the content of the .aidata file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {self.file_path}: {e}")
            return None
    
    def _write_file(self, content):
        """Write content to the .aidata file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing to file {self.file_path}: {e}")
            return False
    
    def validate_syntax(self):
        """Validate the syntax of the .aidata file."""
        if not self.content:
            return False, "Could not read file content."
        
        # Check for mandatory sections
        mandatory_sections = [
            "FILE METADATA",
            "DOMAIN CONTEXT",
            "KNOWLEDGE REPRESENTATION",
            "VALIDATION FRAMEWORK",
            "APPLICATION CONTEXT",
            "EVOLUTION TRACKING",
            "AUTOMATED LEARNINGS"
        ]
        
        missing_sections = []
        for section in mandatory_sections:
            if f"## {section}" not in self.content:
                missing_sections.append(section)
        
        if missing_sections:
            return False, f"Missing mandatory sections: {', '.join(missing_sections)}"
        
        # Check for proper file header
        if not self.content.startswith("# AI LEARNING FILE:"):
            return False, "File must start with '# AI LEARNING FILE:'"
        
        # Check for CREATED section
        if "## CREATED" not in self.content:
            return False, "Missing 'CREATED' section"
        
        # Enhanced validation: Check for valid timestamp in CREATED section
        created_match = re.search(r"## CREATED\n(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", self.content)
        if created_match:
            try:
                datetime.strptime(created_match.group(1), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return False, "Invalid timestamp format in CREATED section"
        
        # Enhanced validation: Check for required fields in FILE METADATA
        metadata_match = re.search(r"## FILE METADATA\n([\\s\\S]*?)(?=\\n## |\\Z)", self.content)
        if metadata_match:
            metadata_content = metadata_match.group(1)
            required_metadata_fields = [
                "Schema Version",
                "Confidence Level",
                "Classification"
            ]
            
            missing_fields = []
            for field in required_metadata_fields:
                if f"- **{field}**:" not in metadata_content:
                    missing_fields.append(field)
            
            if missing_fields:
                return False, f"Missing required metadata fields: {', '.join(missing_fields)}"
        
        return True, "Syntax validation passed."
    
    def generate_hash(self):
        """Generate and update the integrity hash in the file."""
        if not self.content:
            return False, "Could not read file content."
        
        # Generate SHA256 hash of the file content (excluding the hash line itself)
        # First, we need to temporarily remove the existing hash line to calculate the hash
        lines = self.content.split('\n')
        filtered_lines = []
        hash_line_index = -1
        
        for i, line in enumerate(lines):
            if line.startswith("- **Integrity Hash**: SHA256-"):
                hash_line_index = i
            else:
                filtered_lines.append(line)
        
        # Join the lines without the hash line
        content_without_hash = '\n'.join(filtered_lines)
        
        # Calculate the hash
        sha256_hash = hashlib.sha256(content_without_hash.encode('utf-8')).hexdigest()
        
        # Update the hash line
        if hash_line_index != -1:
            lines[hash_line_index] = f"- **Integrity Hash**: SHA256-{sha256_hash}"
        else:
            # If no hash line exists, we need to add it to the FILE METADATA section
            # Find the FILE METADATA section and add the hash line after the other metadata
            for i, line in enumerate(lines):
                if line == "## FILE METADATA":
                    # Find the end of the FILE METADATA section
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("## "):
                        j += 1
                    # Insert the hash line before the next section
                    lines.insert(j, f"- **Integrity Hash**: SHA256-{sha256_hash}")
                    break
        
        # Join all lines back together
        updated_content = '\n'.join(lines)
        
        # Write the updated content back to the file
        if self._write_file(updated_content):
            return True, f"Integrity hash updated: SHA256-{sha256_hash}"
        else:
            return False, "Failed to write updated content to file."
    
    def deduplicate_learnings(self, auto_confirm=False):
        """Remove duplicate entries from the AUTOMATED LEARNINGS section."""
        if not self.content:
            return False, "Could not read file content."
        
        # Find the AUTOMATED LEARNINGS section
        learnings_section_match = re.search(r'(## AUTOMATED LEARNINGS\n)(.*)', self.content, re.DOTALL)
        if not learnings_section_match:
            return False, "No AUTOMATED LEARNINGS section found."
        
        # Extract the section header and content
        section_header = learnings_section_match.group(1)
        section_content = learnings_section_match.group(2)
        
        # Split into individual learning entries
        # This regex looks for the pattern of a learning entry header
        entries = re.split(r'(\n### Learning Entry - \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\n)', section_content)
        
        # Reconstruct entries with their headers
        reconstructed_entries = []
        seen_hashes = set()
        
        # Handle the first part (before any entries)
        if entries and entries[0].strip():
            reconstructed_entries.append(entries[0])
        
        # Process entries in pairs (header, content)
        duplicate_count = 0
        for i in range(1, len(entries), 2):
            if i + 1 < len(entries):
                header = entries[i]
                entry_content = entries[i + 1]
                
                # Create a unique identifier for the entry
                # We'll hash only key fields for better performance
                timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', header)
                timestamp = timestamp_match.group(0) if timestamp_match else ""
                
                # Extract a summary of the content (first few lines)
                content_lines = entry_content.strip().split('\n')
                content_summary = '\n'.join(content_lines[:5])  # First 5 lines as summary
                
                entry_identifier = f"{timestamp}|{content_summary}"
                entry_hash = hashlib.sha256(entry_identifier.encode('utf-8')).hexdigest()
                
                if entry_hash not in seen_hashes:
                    seen_hashes.add(entry_hash)
                    reconstructed_entries.append(header)
                    reconstructed_entries.append(entry_content)
                else:
                    duplicate_count += 1
        
        # If there are duplicates and auto_confirm is False, ask for confirmation
        if duplicate_count > 0 and not auto_confirm:
            response = input(f"Found {duplicate_count} duplicate entries. Remove them? (y/N): ")
            if response.lower() != 'y':
                return False, "Operation cancelled by user."
        
        # Reconstruct the section content
        new_section_content = ''.join(reconstructed_entries).strip()
        
        # Replace the old section with the new one
        # We need to be careful to only replace the content, not the header
        new_content = self.content.replace(
            section_header + learnings_section_match.group(2),
            section_header + new_section_content
        )
        
        # Write back to file
        if self._write_file(new_content):
            return True, f"Successfully deduplicated. Removed {duplicate_count} duplicate entries."
        else:
            return False, "Failed to write updated content to file."
    
    def add_checkpoint(self, description):
        """Add a timestamped checkpoint to the EVOLUTION TRACKING section."""
        if not self.content:
            return False, "Could not read file content."
        
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        checkpoint_entry = f"- **{timestamp}**: {description}\n"
        
        # Read the file
        lines = self.content.split('\n')
        
        # Find the Checkpoint History section within EVOLUTION TRACKING and insert the new entry
        in_evolution_tracking = False
        in_checkpoint_section = False
        checkpoint_section_found = False
        
        for i, line in enumerate(lines):
            if "## EVOLUTION TRACKING" in line:
                in_evolution_tracking = True
            elif in_evolution_tracking and "### Checkpoint History" in line:
                in_checkpoint_section = True
                checkpoint_section_found = True
            elif in_evolution_tracking and in_checkpoint_section and line.startswith("## ") and "### Checkpoint History" not in line:
                # We've reached the end of the Checkpoint History section
                lines.insert(i, checkpoint_entry)
                break
            elif in_evolution_tracking and in_checkpoint_section and "- ****:" in line:
                # Insert after the last checkpoint entry
                lines.insert(i + 1, checkpoint_entry)
                break
        
        # If no Checkpoint History section exists, create one
        if not checkpoint_section_found:
            for i, line in enumerate(lines):
                if "## EVOLUTION TRACKING" in line:
                    # Find the end of the EVOLUTION TRACKING section
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith("## ") or "## EVOLUTION TRACKING" in lines[j]:
                        j += 1
                    # Insert the Checkpoint History section
                    checkpoint_lines = [
                        "\n### Checkpoint History",
                        checkpoint_entry.rstrip()
                    ]
                    for k, checkpoint_line in enumerate(checkpoint_lines):
                        lines.insert(j + k, checkpoint_line)
                    break
        
        # Write the updated file
        updated_content = '\n'.join(lines)
        if self._write_file(updated_content):
            return True, f"Checkpoint added: {description}"
        else:
            return False, "Failed to write updated content to file."
    
    def to_json(self):
        """Convert the .aidata file to JSON format with structured metadata."""
        if not self.content:
            return False, "Could not read file content."
        
        # Parse the .aidata content into a structured format
        json_data = {
            "file_name": self.file_path.name,
            "metadata": {},
            "sections": {}
        }
        
        # Extract file header
        header_match = re.match(r"# AI LEARNING FILE: (.+)", self.content)
        if header_match:
            json_data["file_title"] = header_match.group(1)
        
        # Parse FILE METADATA into key-value pairs
        metadata_match = re.search(r'## FILE METADATA\n([\\s\\S]*?)(?=\\n## |\\Z)', self.content)
        if metadata_match:
            metadata_content = metadata_match.group(1)
            for line in metadata_content.split('\n'):
                if line.startswith('- **'):
                    # Handle simple key-value pairs
                    match = re.match(r'- \*\*([^:]+)\*\*: (.*)', line)
                    if match:
                        key, value = match.groups()
                        json_data["metadata"][key] = value
                    # Handle nested structures like Processing AI
                    elif '- name:' in line:
                        # This is a more complex structure, we'll handle it as text for now
                        pass
        
        # Split content into sections
        sections = re.split(r"(## .+)", self.content)
        
        # Process sections
        for i in range(1, len(sections), 2):  # Skip the first element which is before the first header
            if i + 1 < len(sections):
                header = sections[i].strip()
                content = sections[i + 1].strip()
                
                # Remove the '#' from the header to get the section name
                section_name = header[3:]  # Remove "## "
                
                # For subsections, we might want to parse them differently
                # For now, we'll just store the content as text
                json_data["sections"][section_name] = content
        
        # Write JSON to file
        json_file_path = self.file_path.with_suffix('.json')
        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            return True, f"Converted to JSON: {json_file_path}"
        except Exception as e:
            return False, f"Error writing JSON file: {e}"

def main():
    parser = argparse.ArgumentParser(description="Process .aidata files")
    parser.add_argument("command", choices=["validate", "generate-hash", "deduplicate", "to-json", "add-checkpoint"], 
                        help="Command to execute")
    parser.add_argument("file", help="Path to the .aidata file")
    parser.add_argument("--description", help="Description for checkpoint (required for add-checkpoint)")
    parser.add_argument("--auto-confirm", action="store_true", help="Automatically confirm deduplication")
    
    args = parser.parse_args()
    
    processor = AIDataProcessor(args.file)
    
    if args.command == "validate":
        success, message = processor.validate_syntax()
    elif args.command == "generate-hash":
        success, message = processor.generate_hash()
    elif args.command == "deduplicate":
        success, message = processor.deduplicate_learnings(args.auto_confirm)
    elif args.command == "to-json":
        success, message = processor.to_json()
    elif args.command == "add-checkpoint":
        if not args.description:
            parser.error("--description is required for add-checkpoint")
        success, message = processor.add_checkpoint(args.description)
    
    if success:
        print(message)
    else:
        print(f"Error: {message}")
        sys.exit(1)

if __name__ == "__main__":
    main()