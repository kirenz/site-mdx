import os
import datetime

def should_process_file(file_path):
    """
    Determine if a file should be processed based on its extension and path.
    Include hidden files but not files in hidden directories.
    Excludes specific files and extensions.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        bool: True if file should be processed, False otherwise
    """
    # List of extensions to include
    valid_extensions = (
        '.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.json',
        '.env', '.eslintrc', '.prettierrc', '.babelrc', '.mjs', 
        '.env.local', '.env.development', '.env.production',
        '.yml', '.py', '.sh', '.html', '.md', '.txt', '.xml', '.mdx'
    )
    
    # List of specific files to exclude
    excluded_files = {
        'package-lock.json',
        'README.md',
        '.gitignore',
        '.gitattributes',
        '.DS_Store'
    }
    
    # Get the filename
    filename = os.path.basename(file_path)
    
    # Check if file is in a hidden directory
    path_parts = os.path.normpath(file_path).split(os.sep)
    for part in path_parts[:-1]:  # Exclude the filename itself
        if part.startswith('.'):
            return False
    
    # Exclude specific files
    if filename in excluded_files:
        return False
        
    # Exclude .sh files
    if filename.endswith('.sh'):
        return False
    
    # Include the file if it has a relevant extension or is a hidden file
    # (except for the specifically excluded ones)
    return file_path.endswith(valid_extensions) or (
        os.path.basename(file_path).startswith('.') and 
        filename not in excluded_files
    )

def generate_project_knowledge(root_directory, output_file):
    """
    Generates a single text file containing all source code from both root and src directory
    with file paths as comments.
    
    Args:
        root_directory (str): Path to the project root directory
        output_file (str): Path where the output file should be saved
    """
    # Create a list to store all file contents
    all_contents = []
    
    # Add timestamp at the beginning
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_contents.append(f"# Project Knowledge Generated at: {timestamp}\n\n")
    
    # Keep track of processed files for reporting
    processed_files = []
    skipped_files = []
    
    # Function to process a directory
    def process_directory(directory, is_root=False):
        # Process files in the current directory first
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            relative_path = os.path.relpath(item_path, root_directory)
            
            # Skip if it's a directory
            if os.path.isdir(item_path):
                # If it's src directory or we're in root, process it
                if item == 'src' or not is_root:
                    process_directory(item_path)
                continue
            
            # Check if we should process this file
            if should_process_file(item_path):
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add file header with path information
                    all_contents.append(f"{'=' * 80}")
                    all_contents.append(f"# File: {relative_path}")
                    all_contents.append(f"# Full Path: {item_path}")
                    all_contents.append(f"{'=' * 80}\n")
                    
                    # Add the file content
                    all_contents.append(content)
                    all_contents.append("\n\n")
                    
                    processed_files.append(relative_path)
                except Exception as e:
                    all_contents.append(f"# Error reading {item_path}: {str(e)}\n\n")
            else:
                skipped_files.append(relative_path)
    
    # Start processing from root
    process_directory(root_directory, is_root=True)
    
    # Write everything to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_contents))
        
        # Print statistics and file lists
        print(f"\nSuccessfully generated project knowledge file: {output_file}")
        print(f"Total files processed: {len(processed_files)}")
        
        print("\nProcessed files:")
        for file in sorted(processed_files):
            print(f"+ {file}")
            
        print("\nSkipped files:")
        for file in sorted(skipped_files):
            print(f"- {file}")
        
    except Exception as e:
        print(f"Error writing output file: {str(e)}")

if __name__ == "__main__":
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Define output file path
    output_file = os.path.join(current_dir, "project_knowledge.txt")
    
    # Generate the project knowledge file
    generate_project_knowledge(current_dir, output_file)