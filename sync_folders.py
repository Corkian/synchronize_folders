import os
import shutil
import argparse
import time


def synchronize_folders(source_path, replica_path, log_file_path):

    # Create replica folder if it doesn't exist
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)
        print(f"The replica folder named {replica_path} was created.")
        with open(log_file_path, 'a') as f:
            f.write(f"The replica folder named {replica_path} was created.\n")

    # Creates the log file if it doesn't exist
    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()

    # Iterate through the source folder and copy/update files and directories to the replica folder
    for root_dir, dirs, files in os.walk(source_path):
        replica_root_dir = root_dir.replace(source_path, replica_path)
        # Create directories that exist in the source folder but not in the replica folder
        for dir in dirs:
            replica_dir = os.path.join(replica_root_dir, dir)
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                print(f"Directory {replica_dir} was created in the Replica Folder.")
                with open(log_file_path, 'a') as f:
                    f.write(f"Directory {replica_dir} was created in the Replica Folder.\n")
        # Copy/update files that exist in the source folder but not in the replica folder or that are newer in the source folder
        for file in files:
            source_file = os.path.join(root_dir, file)
            replica_file = os.path.join(replica_root_dir, file)
            if not os.path.exists(replica_file) or (os.path.exists(replica_file) and os.stat(source_file).st_mtime - os.stat(replica_file).st_mtime > 1):
                shutil.copy2(source_file, replica_file)
                print(f"File {replica_file} updated in the Replica Folder.")
                with open(log_file_path, 'a') as f:
                    f.write(f"File {replica_file} updated in the Replica Folder.\n")

    # Iterate through the replica folder and remove directories and files that exist in the replica folder but not in the source folder
    for root_dir, dirs, files in os.walk(replica_path):
        source_root = root_dir.replace(replica_path, source_path)
        # Remove directories that exist in the replica folder but not in the source folder
        for dir in dirs:
            source_dir = os.path.join(source_root, dir)
            if not os.path.exists(source_dir):
                shutil.rmtree(os.path.join(root_dir, dir))
                print(f"Directory {os.path.join(root_dir, dir)} was removed from Replica Folder.")
                with open(log_file_path, 'a') as f:
                    f.write(f"Directory {os.path.join(root_dir, dir)} was removed from Replica Folder.\n")
        # Remove files that exist in the replica folder but not in the source folder
        for file in files:
            replica_file = os.path.join(root_dir, file)
            source_file = os.path.join(source_root, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                print(f"File {replica_file} was removed from Replica Folder.")
                with open(log_file_path, 'a') as f:
                    f.write(f"File {replica_file} was removed from Replica Folder.\n")

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help='Provide path to the source folder')
    parser.add_argument('replica_path', help='Provide path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file_path', help='Provide path to the log file')
    args = parser.parse_args()

    # Start periodic synchronization
    while True:
        synchronize_folders(args.source_path, args.replica_path, args.log_file_path)
        time.sleep(args.interval)
