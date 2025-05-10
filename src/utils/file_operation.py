import os
import pandas as pd

INDEX_FILE_NAME = 'log/process.index'

# region Function Definitions for File Operations

def map_directory(root_path, file_extension='.xml', index_file_name=INDEX_FILE_NAME):
    """
    Maps the directory structure starting from the given root path and filters files by extension.

    Args:
        root_path (str): The root directory to start mapping.
        file_extension (str): The file extension to filter files. Default is '.xml'.
        index_file_name (str): The name of the index file to check IDs against.

    Returns:
        list: A list of dictionaries containing file metadata.
    """
    directory_list = []
    for root, dirs, files in os.walk(root_path):
        for name in dirs + files:
            if name.endswith(file_extension):
                file_id = os.path.splitext(name)[0]
                directory_list.append({
                    'id': file_id,
                    'path': os.path.join(root, name),
                    'filename': name,
                    'process': check_id_in_process_index(file_id, index_file_name),
                })
    return directory_list


def map_directory_to_dataframe(root_path=None, file_extension='.xml', index_file_name=INDEX_FILE_NAME):
    """
    Converts the directory structure into a pandas DataFrame.

    Args:
        root_path (str): The root directory to start mapping. Defaults to the current working directory.
        file_extension (str): The file extension to filter files. Default is '.xml'.
        index_file_name (str): The name of the index file to check IDs against.

    Returns:
        pd.DataFrame: A DataFrame containing file metadata.
    """
    if root_path is None:
        root_path = os.getcwd()

    directory_list = map_directory(root_path, file_extension, index_file_name)
    return pd.DataFrame(directory_list)


def check_id_in_process_index(file_id, index_file_name=INDEX_FILE_NAME):
    """
    Checks if a file ID exists in the process index file.

    Args:
        file_id (str): The file ID to check.
        index_file_name (str): The name of the index file.

    Returns:
        bool: True if the ID exists in the index file, False otherwise.
    """
    if not os.path.exists(index_file_name):
        # Create the file if it doesn't exist and return False
        with open(index_file_name, 'w') as f:
            pass
        return False
    else:
        # Check if the file contains the ID
        with open(index_file_name, 'r') as f:
            lines = f.readlines()
        return file_id in [line.strip() for line in lines]


def add_id_to_process_index(file_id, index_file_name=INDEX_FILE_NAME):
    """
    Adds a file ID to the process index file.

    Args:
        file_id (str): The file ID to add.
        index_file_name (str): The name of the index file.
    """
    with open(index_file_name, 'a') as f:
        f.write(file_id + '\n')

# endregion