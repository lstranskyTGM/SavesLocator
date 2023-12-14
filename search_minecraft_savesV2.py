import os
import shutil
import zipfile

def search_for_level_dat(starting_directories, output_file):
    # Search for 'level.dat' files in specified directories and save the paths to a file.
    print("Calculating the total number of directories...")

    total_directories = sum(len(list(os.walk(directory))) for directory in starting_directories)
    processed_directories = 0

    with open(output_file, 'w') as result_file:
        for starting_directory in starting_directories:
            for root, dirs, files in os.walk(starting_directory):
                if 'level.dat' in files:
                    result_file.write(os.path.abspath(root) + '\n')

                processed_directories += 1
                progress_percentage = (processed_directories / total_directories) * 100
                print(f"Progress: {progress_percentage:.2f}% ({processed_directories}/{total_directories} directories processed)", end='\r')

    print("\nSearch completed. Results saved to", output_file)

def calculate_size(paths):
    # Calculate the total size of all files in the specified paths.
    total_size = 0
    for path in paths:
        total_size += sum(os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(path) for file in files)
    return total_size

def format_size(size_bytes):
    # Format size in a human-readable format (KB, MB, GB).
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def copy_game_files(output_file):
    # Copy game files to a new directory or ask if the user wants to zip them.
    with open(output_file, 'r') as result_file:
        paths = result_file.read().splitlines()

    total_files = sum(len(files) for _, _, files in map(lambda path: (path, [], os.listdir(path)), paths))
    total_size = calculate_size(paths)

    print(f"Total size of files: {format_size(total_size)}")

    # Ask the user if they want to copy the files
    copy_files_option = input("Do you want to copy the game files to a new directory? (yes/no): ").lower()

    if copy_files_option == 'yes':
        # Ask for the name of the directory to create
        directory_name = input("Enter the name of the directory for game files: ")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory_name)
        
        try:
            copy_files(paths, output_directory, total_size)
        except Exception as e:
            print("An error occurred:", str(e))
    elif copy_files_option == 'no':
        print("Copy operation skipped. Exiting.")
        exit()
    else:
        # Ask for the name of the zip file to create
        zip_name = input("Enter the name of the zip file (e.g., my_files): ")
        try:
            zip_files(paths, zip_name, total_size)
        except Exception as e:
            print("An error occurred:", str(e))

def copy_files(paths, output_directory, total_size):
    # Copy files to a new directory.
    total_files = sum(len(files) for _, _, files in map(lambda path: (path, [], os.listdir(path)), paths))
    processed_files = 0

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for src_path in paths:
        dst_path = os.path.join(output_directory, os.path.relpath(src_path, os.path.commonprefix([os.path.dirname(p) for p in paths])))
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        for root, dirs, files in os.walk(src_path):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_path, file)

                if os.path.isfile(src_file):
                    copy_file(src_file, dst_file)

                processed_files += 1
                progress_percentage = (processed_files / total_files) * 100
                print(f"Progress: {progress_percentage:.2f}% ({processed_files}/{total_files} files processed)", end='\r')

    print("\nCopy completed. Files saved to", output_directory)

def copy_file(src, dst):
    # Custom copy function to handle cross-mount copy
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst)
    shutil.copystat(src, dst)


def zip_files(paths, zip_name, total_size):
    # Zip files in the specified paths.
    print(f"Zipping files. Total size before zip: {format_size(total_size)}")

    with zipfile.ZipFile(f"{zip_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in paths:
            for root, _, files in os.walk(path):
                for file in tqdm(files, unit="B", unit_scale=True, unit_divisor=1024, desc="Zipping", leave=False):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.commonprefix(paths))
                    zipf.write(file_path, arcname=arcname)

    print("\nZip completed. Zip file saved as", f"{zip_name}.zip")

if __name__ == "__main__":
    # Search for level.dat files
    starting_directories = input("Enter the starting directories (comma-separated, e.g., C:/,D:/): ").split(',')
    output_file = input("Enter the output file path for level.dat results (e.g., results.txt): ")

    try:
        search_for_level_dat(starting_directories, output_file)
    except Exception as e:
        print("An error occurred:", str(e))
        exit()

    # Calculate size and ask the user if they want to copy or zip the files
    copy_game_files(output_file)
