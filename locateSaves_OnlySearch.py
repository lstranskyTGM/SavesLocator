import os

def search_for_level_dat(starting_directories, output_file):
    with open(output_file, 'w') as result_file:
        for starting_directory in starting_directories:
            for root, dirs, files in os.walk(starting_directory):
                if 'level.dat' in files:
                    result_file.write(os.path.abspath(root) + '\n')

if __name__ == "__main__":
    # Provide a list of starting directories and the output file path
    starting_directories = input("Enter the starting directories (comma-separated, e.g., C:/,D:/): ").split(',')
    output_file = input("Enter the output file path (e.g., results.txt): ")

    try:
        search_for_level_dat(starting_directories, output_file)
        print("Search completed. Results saved to", output_file)
    except Exception as e:
        print("An error occurred:", str(e))
