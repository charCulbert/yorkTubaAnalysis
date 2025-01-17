import os
import re
import sys
from pathlib import Path

def get_note_index(note):
    """Convert a note (e.g., 'C#4') to its position in the chromatic scale"""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # Extract note and octave
    if '#' in note:
        base_note = note[:2]
        octave = int(note[2])
    else:
        base_note = note[0]
        octave = int(note[1])
    
    return octave * 12 + notes.index(base_note)

def get_files_to_rename(directory='.', mic_type=None):
    """Get all matching .wav files in the directory"""
    files = []
    # Flexible pattern to match various prefixes and mic types
    if mic_type:
        pattern = re.compile(rf'([a-zA-Z]+)_([A-G]#?\d)_{mic_type}\.wav')
        file_glob = f'*_{mic_type}.wav'
    else:
        # If no mic type specified, try both sm57 and aom5024
        sm57_files = list(Path(directory).glob('*_sm57.wav'))
        aom5024_files = list(Path(directory).glob('*_aom5024.wav'))
        files = []

        for file_list, mic_type in [(sm57_files, 'sm57'), (aom5024_files, 'aom5024')]:
            for file in file_list:
                match = re.match(rf'([a-zA-Z]+)_([A-G]#?\d)_{mic_type}\.wav', file.name)
                if match:
                    prefix = match.group(1)
                    note = match.group(2)
                    files.append((file, note, prefix))
                    print(f"Found file: {file.name}")
                    print(f"  Prefix: {prefix}")
                    print(f"  Note: {note}")
        
        return files

    # If mic type is specified or no files found, use the specific pattern
    for file in Path(directory).glob(file_glob):
        match = pattern.match(file.name)
        if match:
            prefix = match.group(1)  # e.g., 'york' or 'yamaha'
            note = match.group(2)    # e.g., 'C#4'
            files.append((file, note, prefix))
            print(f"Found file: {file.name}")
            print(f"  Prefix: {prefix}")
            print(f"  Note: {note}")
    return files

def main():
    # Check if a directory path is provided as an argument
    directory = '.'  # Default to current directory
    mic_type = None  # Optional mic type filter
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        # Check if a specific mic type is passed as a second argument
        if len(sys.argv) > 2:
            mic_type = sys.argv[2]
        print(f"Processing directory: {directory}")
        if mic_type:
            print(f"Filtering for mic type: {mic_type}")
    
    # Validate the directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    
    print("Starting note renaming script...")
    
    # Get all matching files and their notes
    files = get_files_to_rename(directory, mic_type)
    if not files:
        print("No matching files found!")
        return
    
    # Group files by prefix
    prefixes = set(f[2] for f in files)
    if len(prefixes) > 1:
        print(f"\nWarning: Multiple prefixes found: {', '.join(prefixes)}")
    
    # Find the lowest note
    lowest_note = min(files, key=lambda x: get_note_index(x[1]))[1]
    print(f"\nLowest note found: {lowest_note}")
    
    print("\nPlanned renaming operations:")
    print("-" * 50)
    
    # Store planned operations
    rename_operations = []
    # Sort files by note
    sorted_files = sorted(files, key=lambda x: get_note_index(x[1]))
    
    count = 1
    
    for file_path, note, prefix in sorted_files:
        new_number = f"{count:03d}"
        new_name = f"{prefix}_{new_number}_{note}_{file_path.name.split('_')[-1]}"
        print(f"{file_path.name} → {new_name}")
        rename_operations.append((file_path, new_name))
        count += 1
    
    print("\nDo you want to proceed with renaming? (y/n): ", end='')
    response = input().lower().strip()
    
    if response == 'y':
        print("\nRenaming files...")
        for file_path, new_name in rename_operations:
            try:
                # Explicitly use os.rename for more control
                os.rename(str(file_path), str(file_path.parent / new_name))
                print(f"Renamed: {file_path.name} → {new_name}")
            
            except PermissionError:
                print(f"Permission error renaming {file_path.name}. Check file permissions.")
            except FileExistsError:
                print(f"Error: A file named {new_name} already exists.")
            except Exception as e:
                print(f"Unexpected error renaming {file_path.name}: {e}")
        
        print("\nAll files have been renamed!")
    else:
        print("\nOperation cancelled. No files were renamed.")

if __name__ == "__main__":
    main()