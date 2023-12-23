import os
import shutil
import sys
import zipfile


class FileProcessor:
    # Class to handle file processing operations like searching, copying, and zipping game files.

    def __init__(self, output_file):
        # Initialize with the specified output file for results.
        self.output_file = output_file
        self.paths = []
        self.total_size = 0

    def search_for_level_dat(self, starting_directories):
        # Search for directories containing exactly one 'level.dat' file and save their paths.
        total_directories = sum(len(list(os.walk(directory))) for directory in starting_directories)
        processed_directories = 0

        with open(self.output_file, 'w') as result_file:
            for starting_directory in starting_directories:
                for root, dirs, files in os.walk(starting_directory):
                    level_dat_count = files.count('level.dat')
                    # Check if there is exactly one 'level.dat' file
                    if level_dat_count == 1:
                        result_file.write(os.path.abspath(root) + '\n')

                    processed_directories += 1
                    self.simple_progress_bar(total_directories, processed_directories, "directories")

        print("\nSearch completed. Results saved to", self.output_file)

    def calculate_total_size(self):
        # Calculate the total size of all files in the specified paths.
        self.paths = self._read_paths()
        self.total_size = sum(os.path.getsize(os.path.join(root, file)) for path in self.paths for root, _, files in os.walk(path) for file in files)
        return self.total_size

    def _read_paths(self):
        # Read paths from the output file.
        with open(self.output_file, 'r') as result_file:
            return result_file.read().splitlines()

    @staticmethod
    def format_size(size_bytes):
        # Format size in a human-readable format (KB, MB, GB).
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0

    def copy_files(self, output_directory, copy_only_saves=False):
        # Copy files to a new directory, with an option to copy only the save directories.
        total_files = sum(len(files) for path in self.paths for _, _, files in os.walk(path))
        processed_files = 0

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for src_path in self.paths:
            if copy_only_saves:
                dst_path = os.path.join(output_directory, os.path.basename(src_path))
                # Handle existing directories by renaming
                counter = 1
                original_dst_path = dst_path
                while os.path.exists(dst_path):
                    dst_path = f"{original_dst_path}_{counter}"
                    counter += 1
            else:
                dst_path = os.path.join(output_directory, os.path.relpath(src_path, os.path.commonprefix(
                    [os.path.dirname(p) for p in self.paths])))

            if not os.path.exists(dst_path):
                os.makedirs(dst_path)

            for root, dirs, files in os.walk(src_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst_path, file)

                    if os.path.isfile(src_file):
                        self._copy_file(src_file, dst_file)

                    processed_files += 1
                    self.simple_progress_bar(total_files, processed_files, "files")

        print("\nCopy completed. Files saved to", output_directory)

    @staticmethod
    def _copy_file(src, dst):
        # Copy a single file from src to dst.
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst)
        shutil.copystat(src, dst)

    @staticmethod
    def simple_progress_bar(total, progress, item_name):
        # Displays a simple progress bar along with current progress out of total.
        percent = 100 * (progress / total)
        bar = '#' * int(percent / 2) + '-' * (50 - int(percent / 2))
        sys.stdout.write(f"\r[{bar}] {percent:.2f}% ({progress}/{total} {item_name})")
        sys.stdout.flush()

    def zip_files(self, zip_name):
        # Zip files in the specified paths.
        total_files = sum(len(files) for path in self.paths for _, _, files in os.walk(path))
        processed_files = 0

        with zipfile.ZipFile(f"{zip_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for path in self.paths:
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.commonprefix(self.paths))
                        zipf.write(file_path, arcname=arcname)

                        processed_files += 1
                        self.simple_progress_bar(total_files, processed_files, "files")

        print("\nZip completed. Zip file saved as", f"{zip_name}.zip")


def main():
    # Main function to handle user inputs and initiate file processing.
    starting_directories = input("Enter the starting directories (comma-separated, e.g., C:/,D:/): ").split(',')

    # Check for an existing 'saves.txt' file and rename if necessary
    output_file = "saves.txt"
    if os.path.exists(output_file):
        base, extension = os.path.splitext(output_file)
        counter = 1
        while os.path.exists(f"{base}_{counter}{extension}"):
            counter += 1
        output_file = f"{base}_{counter}{extension}"

    file_processor = FileProcessor(output_file)
    file_processor.search_for_level_dat(starting_directories)

    total_size = file_processor.calculate_total_size()
    print(f"Total size of files: {file_processor.format_size(total_size)}")

    copy_files_option = input(
        "Do you want to copy the game files to a new directory, zip them, or exit? (c/z/e): ").lower()

    if copy_files_option == 'c':
        directory_name = input("Enter the name of the directory for game files: ")
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory_name)
        copy_structure_option = input("Copy entire directory structure? (y/n): ").lower()
        file_processor.copy_files(output_directory, copy_structure_option != 'y')
    elif copy_files_option == 'z':
        zip_name = input("Enter the name of the zip file: ")
        file_processor.zip_files(zip_name)
    else:
        print("Exiting script.")
        exit()


if __name__ == "__main__":
    main()
