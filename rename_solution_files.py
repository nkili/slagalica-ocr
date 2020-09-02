import sys
import os
from shutil import copyfile

def rename_file(filePath):
    with open(filePath) as f:
        file_text = f.read();
    file_lines = file_text.splitlines()
    while "циклус" not in file_lines[0].lower():
        file_lines = file_lines[1:] 
    season = "%03d" % int(file_lines[0].split()[0].strip('.'))
    episode = "%02d" % int(file_lines[1].split()[0].strip('.'))
    return "c" + season + "e" + episode + "a.txt"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python rename_solution_files.py SOLUTION_FILE... SAVE_DIR/")
        exit()
    solution_files = sys.argv[1:-1]
    save_dir = sys.argv[-1]
    if not os.path.isdir(save_dir):
        print("Usage: python rename_solution_files.py SOLUTION_FILE... SAVE_DIR/")
        print(f"{solved_file_path} is not a valid directory path")
        exit()
    for solved_file_path in solution_files:
        if not os.path.isfile(solved_file_path):
            print("Usage: python rename_solution_files.py SOLUTION_FILE... SAVE_DIR/")
            print(f"{solved_file_path} is not a valid file path")
            exit()
    for solved_file_path in solution_files:
        full_renamed_file_path = os.path.join(save_dir, rename_file(solved_file_path))
        copyfile(solved_file_path, full_renamed_file_path)
